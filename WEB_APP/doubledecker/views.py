from datetime import datetime, timedelta
import os
import math
from geopy.distance import distance as d
from django.shortcuts import render
# origionated from https://docs.djangoproject.com/en/3.2/intro/tutorial01/
from django.http import HttpResponse
# Create your views here.
from django.http import JsonResponse
from joblib import load
import os
from .models import Weather
from math import ceil, floor
import pickle
import pandas as pd
import re
import json

stop_times = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/stop_times.txt", delimiter=",")
stops = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/stops.txt", delimiter=",")
routes = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/routes.txt", delimiter=",")
trips = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/trips.txt", delimiter=",")
calendar = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/calendar.txt", delimiter=",")
stop_times["arrival_time"] = pd.to_timedelta(stop_times["arrival_time"])

# https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
with open('../DATA_ANALYTICS/journeytimes.pickle', 'rb') as handle:
    journeytimes = pickle.load(handle)
# https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
with open('../DATA_ANALYTICS/distances.pickle', 'rb') as handle:
    distances = pickle.load(handle)

janmodel = load("../DATA_ANALYTICS/MODELS/jangbr.joblib")
febmodel = load("../DATA_ANALYTICS/MODELS/febgbr.joblib")
marchmodel = load("../DATA_ANALYTICS/MODELS/marchgbr.joblib")
aprilmodel = load("../DATA_ANALYTICS/MODELS/aprilgbr.joblib")
maymodel = load("../DATA_ANALYTICS/MODELS/maygbr.joblib")
junemodel = load("../DATA_ANALYTICS/MODELS/junegbr.joblib")
julymodel = load("../DATA_ANALYTICS/MODELS/julygbr.joblib")
augmodel = load("../DATA_ANALYTICS/MODELS/auggbr.joblib")
sepmodel = load("../DATA_ANALYTICS/MODELS/sepgbr.joblib")
octmodel = load("../DATA_ANALYTICS/MODELS/octgbr.joblib")
novmodel = load("../DATA_ANALYTICS/MODELS/novgbr.joblib")
decmodel = load("../DATA_ANALYTICS/MODELS/decgbr.joblib")


class RouteNotAvailable(Exception):
    """Raised when there was no route available from the origin stop to the destination stop"""  # gtfs appraently not complete
    pass


class PartialRouteNotAvailable(Exception):
    """Raised when there was no route available from one stop to another on the journey"""  # gtfs appraently not complete
    pass


def main(request):  # origionated from  https://docs.djangoproject.com/en/3.2/intro/tutorial01/
    return render(request, 'doubledecker/index.html')


# origionated from  https://docs.djangoproject.com/en/3.2/intro/tutorial01/
def explore_view(request):
    return render(request, 'doubledecker/explore.html')


def tourism_views(request):
    return render(request, 'doubledecker/tourism.html')


# from  https://www.youtube.com/watch?v=_3xj9B0qqps&t=1739s and corresponding github https://github.com/veryacademy/YT-Django-Iris-App-3xj9B0qqps/blob/master/templates/predict.html
def model(request):
    def route_journey_time(DayOfService, day, LineId, olat, olng, dlat, dlng, departure):
        month = datetime.fromtimestamp(DayOfService).month
        if month == 1:
            loadedmodel = janmodel
        elif month == 2:
            loadedmodel = febmodel
        elif month == 3:
            loadedmodel = marchmodel
        elif month == 4:
            loadedmodel = aprilmodel
        elif month == 5:
            loadedmodel = maymodel
        elif month == 6:
            loadedmodel = junemodel
        elif month == 7:
            loadedmodel = julymodel
        elif month == 8:
            loadedmodel = augmodel
        elif month == 9:
            loadedmodel = sepmodel
        elif month == 10:
            loadedmodel = octmodel
        elif month == 11:
            loadedmodel = novmodel
        else:
            loadedmodel = decmodel

        days = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
        days[day] = 1
        current = Weather.objects.order_by('current').first()
        temp = (getattr(current, 'temperature'))
        rain = getattr(current, 'rain_1h')
        msl = getattr(current, 'pressure')
        rhum = getattr(current, 'humidity')
        try:
            routes = get_route(departure, olat, olng, dlat, dlng, day, LineId)
        except IndexError as e:
            raise RouteNotAvailable
        # assume june july and august all schools off and we are using monthly data so do not need to give model that detail for those months as will be constant col
        holidays = ["2020-01-06", "2021-02-17", "2021-02-18", "2021-02-19", "2021-02-20", "2021-02-21", "2021-04-03",
                    "2021-04-04", "2021-04-05", "2021-04-06", "2021-04-07", "2021-04-08", "2021-04-09", "2021-04-10",
                    "2021-04-11", "2021-04-12", "2021-04-13", "2021-04-14", "2021-04-15", "2021-04-16", "2021-04-17",
                    "2021-04-18", "2021-04-19", "2020-06-07", "2021-09-25", "2021-09-26", "2021-09-27", "2021-09-28",
                    "2021-09-29", "2021-10-31", "2021-11-07", "2021-11-08", "2021-11-09", "2021-11-10", "2021-11-11",
                    "2021-11-12", "2021-11-13", "2021-11-14", "2021-12-22", "2021-12-23", "2021-12-24", "2021-12-25",
                    "2021-12-26", "2021-12-27", "2021-12-28", "2021-12-29", "2021-12-30", "2021-12-31"]
        holiday = 0
        if datetime.fromtimestamp(1.62639e+18 / 1e9).strftime("%Y-%m-%d") in holidays:
            holiday = 1

        total_time = 0
        df = pd.DataFrame(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
                                   'timetabledtimes',
                                   'distance',
                                   'rain', 'temp', 'rhum', 'msl',
                                   'holiday',
                                   'hour_0', 'hour_1', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9', 'hour_10',
                                   'hour_11', 'hour_12', 'hour_13', 'hour_14',
                                   'hour_15', 'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21',
                                   'hour_22', 'hour_23'])

        for route in routes:
            try:
                timetabledjourneytime = math.log(journeytimes[route])
                distance = math.log(distances[route])
            except IndexError as e:
                raise PartialRouteNotAvailable

            features = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0,
                        'Sunday': 0,
                        # timetabledtimes
                        'timetabledtimes': timetabledjourneytime,
                        # distances
                        'distance': distance,
                        'rain': 0, 'temp': 0, 'rhum': 0, 'msl': 0,
                        # holiday
                        'holiday': holiday,
                        # hour
                        "hour_0": 0, "hour_1": 0, "hour_5": 0, "hour_6": 0, "hour_7": 0, "hour_8": 0,
                        "hour_9": 0,
                        "hour_10": 0,
                        "hour_11": 0,
                        "hour_12": 0,
                        "hour_13": 0,
                        "hour_14": 0,
                        "hour_15": 0,
                        "hour_16": 0,
                        "hour_17": 0,
                        "hour_18": 0,
                        "hour_19": 0,
                        "hour_20": 0,
                        "hour_21": 0,
                        "hour_22": 0,
                        "hour_23": 0,
                        }

            for day in days:
                features[day] = days[day]
            features["rain"] = rain
            features["temp"] = temp
            features["rhum"] = rhum
            features["msl"] = msl
            hour = departure.split(":")[0]
            features["hour" + "_" + hour[1:] if hour.startswith("0") else "hour" + "_" + hour] = 1
            df = df.append(features, ignore_index=True)

        result = loadedmodel.predict(df)
        total_time += sum([math.e ** r for r in result])
        time = timedelta(seconds=total_time)
        return time

    if request.POST.get('action') == 'post':
        journeys = request.POST.get('journeys')
        parsed_j = json.loads(journeys)
        response = ""
        total_journey_time = timedelta(seconds=0)
        for i in range(len(parsed_j)):
            DayOfService = int(parsed_j[str(i)]['dayofservice']) / 1e3
            day = parsed_j[str(i)]['day']
            LineId = parsed_j[str(i)]['line']
            olat = float(parsed_j[str(i)]['olat'])
            olng = float(parsed_j[str(i)]['olng'])
            dlat = float(parsed_j[str(i)]['dlat'])
            dlng = float(parsed_j[str(i)]['dlng'])
            departure = int(parsed_j[str(i)]['departure'])
            departure = datetime.fromtimestamp(departure / 1e3).strftime("%H:%M:%S")
            try:
                journey_time = (route_journey_time(DayOfService, day, LineId, olat, olng, dlat, dlng, departure))
                total_journey_time = total_journey_time + journey_time
                journey_time = str(journey_time)
                hours = int(journey_time.split(":")[0])
                mins = int(journey_time.split(":")[1])
                sec = float(journey_time.split(":")[2])
                arrival_time = "{:1} Hours {:2} Mins {:.0f} Seconds".format(hours, mins, sec)
                response += "<p><span class='lineid'>{} Bus</span> : {}</p>".format(LineId, arrival_time)
            except RouteNotAvailable:
                response += "<p><span class='lineid'>{} Bus</span> : {}</p>".format(LineId,
                                                                                    "Prediction not available for this journey")
            except PartialRouteNotAvailable:
                response += "<p><span class='lineid'>{} Bus</span> : {}</p>".format(LineId,
                                                                                    "Prediction not available for parts of this journey")
        if len(parsed_j) > 1:
            journey_time = str(total_journey_time)
            hours = int(journey_time.split(":")[0])
            mins = int(journey_time.split(":")[1])
            sec = float(journey_time.split(":")[2])
            arrival_time = "{:1} Hours {:2} Mins {:.0f} Seconds".format(hours, mins, sec)
            response += "<p><span class='lineid'>{}</span> : {}</p>".format("Total Time", arrival_time)
        return JsonResponse({'result': response}, safe=False)


def get_route(departure, olat, olng, dlat, dlng, day, bus_route):
    day = day.lower()
    bus_route = bus_route.lower()

    def trips_day(day):
        """Get all trips for that day"""
        days = list(calendar[calendar[day] == 1]["service_id"].values)
        day_trips = set(trips[trips["service_id"].isin(days)]["trip_id"].values)
        return day_trips

    def trips_route(bus_route):
        """Get all the trips for that route"""
        route_trips = set(
            trips[trips["route_id"].isin(list(routes[routes["route_short_name"] == bus_route]["route_id"].values))][
                "trip_id"].values)
        return route_trips

    def best_stop(trips, lat, lon):
        """Get the best corresponding stop for a list of trips"""
        possible_stop_ids = list(stop_times[stop_times["trip_id"].isin(list(trips))]["stop_id"].drop_duplicates())
        test = stops[stops["stop_id"].isin(possible_stop_ids)][["stop_name", "stop_id", "stop_lat", "stop_lon"]]
        test["lat"] = [lat] * len(test)
        test["lon"] = [lon] * len(test)
        distances = []
        for index, row in test.iterrows():
            distance = abs(d((row["stop_lat"], row["stop_lon"]), (row["lat"], row["lon"])).km)
            distances.append(distance)
        test["distances"] = distances
        test = test.sort_values(by="distances")

        return test[:1]["stop_name"].values[0], test[:1]["stop_id"].values[0]

    def trips_with_origin_destination_day_route(trips, o_id, d_id):
        start = set(stop_times[stop_times["stop_id"] == o_id]["trip_id"].values)
        end = set(stop_times[stop_times["stop_id"] == d_id]["trip_id"].values)
        trips = start.intersection(end)
        trips = trips.intersection(trips)
        return trips

    def trips_correct_dir(trips, o_id, d_id):
        I, O = None, None
        for trip in r:
            if re.search(".I$", trip):
                I = trip
                break
        for trip in r:
            if re.search(".O$", trip):
                O = trip
                break

        correct_direction = []
        if O != None and (
                (stop_times[(stop_times["trip_id"] == O) & (stop_times["stop_id"] == o_id)]["stop_sequence"].values[
                    0]) < (stop_times[(stop_times["trip_id"] == O) & (stop_times["stop_id"] == d_id)][
            "stop_sequence"].values[0])):
            correct_direction = [trip for trip in r if re.search(".O$", trip)]
        elif I != None and (
                (stop_times[(stop_times["trip_id"] == I) & (stop_times["stop_id"] == o_id)]["stop_sequence"].values[
                    0]) < (stop_times[(stop_times["trip_id"] == I) & (stop_times["stop_id"] == d_id)][
            "stop_sequence"].values[0])):
            correct_direction = [trip for trip in r if re.search(".I$", trip)]
        return set(correct_direction)

    def best_trip_for_time(r, departure, stop_id):
        final = stop_times[(stop_times["trip_id"].isin(r)) & (stop_times["stop_id"] == stop_id)][
            ["trip_id", "arrival_time"]]
        final["arrival_time"] = abs(final["arrival_time"] - pd.to_timedelta(departure))
        final = final.sort_values(by="arrival_time")
        tripid = final.iloc[0]["trip_id"]
        return tripid

    def station_to_station(tripid, o_id, d_id):
        seq = stop_times[stop_times["trip_id"] == tripid][["stop_id", "stop_sequence"]].sort_values(by="stop_sequence")
        rstart = seq[seq["stop_id"] == o_id].index[0]
        rfin = seq[seq["stop_id"] == d_id].index[0]
        test = seq.loc[rstart:rfin]
        final = test.merge(stops, how='left', on='stop_id')
        flist = list(final["stop_name"].values)
        flist = [stop.split(" stop ")[1] for stop in flist]
        final_routes = []
        for i in range(len(flist) - 1):
            final_routes.append(flist[i] + "_" + flist[i + 1])
        final_routes
        return final_routes

    r = trips_day(day).intersection(trips_route(bus_route))  # get intersection of trips for that route and day
    o_name, o_id = best_stop(r, olat, olng)
    d_name, d_id = best_stop(r, dlat, dlng)
    r = trips_with_origin_destination_day_route(r, o_id, d_id)
    r = trips_correct_dir(r, o_id, d_id)
    tripid = best_trip_for_time(r, departure, o_id)
    station_route = station_to_station(tripid, o_id, d_id)
    return station_route

# def explore_vue(request):
#     return render(request, 'doubledecker/explore_vue.html')
