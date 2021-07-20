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
from .models import Weather, RouteStops
from math import ceil, floor
import pickle
import pandas as pd
import re

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

loadedmodel = load("../DATA_ANALYTICS/MODELS/january.joblib")


def main(request):  # origionated from  https://docs.djangoproject.com/en/3.2/intro/tutorial01/
    return render(request, 'doubledecker/index.html')


# origionated from  https://docs.djangoproject.com/en/3.2/intro/tutorial01/
def explore_view(request):
    return render(request, 'doubledecker/explore.html')



# from  https://www.youtube.com/watch?v=_3xj9B0qqps&t=1739s and corresponding github https://github.com/veryacademy/YT-Django-Iris-App-3xj9B0qqps/blob/master/templates/predict.html
def model(request):
    if request.POST.get('action') == 'post':
        DayOfService = int(request.POST.get('dayofservice')) *1e6
        day = request.POST.get('day')
        LineId = request.POST.get('line')
        olat = float(request.POST.get('olat'))
        olng = float(request.POST.get('olng'))
        dlat = float(request.POST.get('dlat'))
        dlng =  float(request.POST.get('dlng'))
        #print(olat, olng)
        #print(dlat, dlng)


        departure = int(request.POST.get('departure'))
        departure = datetime.fromtimestamp(departure/ 1e3).strftime("%H:%M:%S")

        #print(DayOfService)
        #print(day)
        #print(LineId)
        #print(departure)

        days = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
        days[day] = 1

        current = Weather.objects.order_by('current').first()
        temp = (getattr(current, 'temperature'))
        rain = getattr(current, 'rain_1h')
        msl = getattr(current, 'pressure')
        rhum = getattr(current, 'humidity')



        routes = get_route(departure, olat, olng, dlat, dlng, day, LineId)
        # from www.mummypages.ie%2Fschool-calendar-and-holidays-20172018-republic-of-ireland&usg=AOvVaw0I7h3OF8HhiK1Om33irR_P
        # assume june july and august all schools off and we are using monthly data so do not need to give model that detail for those months as will be constant col
        holidays = ['2018-01-01','2018-01-02','2018-01-03','2018-01-04','2018-01-05','2018-02-12','2018-02-13','2018-02-14','2018-02-15','2018-02-16','2018-03-23','2018-03-23','2018-03-26','2018-03-27','2018-03-28','2018-03-29','2018-03-30','2018-04-02','2018-04-03','2018-04-04','2018-04-05','2018-04-06','2018-05-01','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-12-24','2018-12-25','2018-12-26','2018-12-27','2018-12-28','2018-12-31']
        holiday = 0
        if datetime.fromtimestamp(1.62639e+18/ 1e9).strftime("%Y-%m-%d") in holidays:
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
                return JsonResponse({'result': "NO PREDICTION AVAILABLE"}, safe=False)

            features = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0,'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0,
            # timetabledtimes
            'timetabledtimes': timetabledjourneytime,
            # distances
            'distance': distance,
            'rain': 0, 'temp': 0, 'rhum': 0, 'msl': 0,
            # holiday
            'holiday': holiday,
            # hour
            "hour_0": 0,"hour_1": 0,"hour_5": 0,"hour_6": 0,"hour_7": 0,"hour_8": 0,
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
        #print(result)
        total_time += sum([math.e ** r for r in result])
    time = str(timedelta(seconds=total_time))
    hours = int(time.split(":")[0])
    mins = int(time.split(":")[1])
    sec = float(time.split(":")[2])
    arrival_time = "{:1} Hours {:2} Mins {:.0f} Seconds".format(hours, mins, sec)
    return JsonResponse({'result': arrival_time}, safe=False)


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
        #print(test[:1]["stop_name"].values[0])
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
        # print(final)
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

