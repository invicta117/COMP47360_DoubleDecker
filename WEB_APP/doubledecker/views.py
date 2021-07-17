from datetime import datetime, timedelta
import os
import math
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
        print(olat, olng)
        print(dlat, dlng)
        origin = stops[(stops["stop_lat"] > floor(olat * 1000)/ 1000) & (stops["stop_lat"] < ceil(olat * 1000) / 1000) & (stops["stop_lon"] < ceil(olng * 1000) / 1000) & (stops["stop_lon"] > floor(olng * 1000) / 1000)][:1]["stop_name"].values[0]

        destination = stops[(stops["stop_lat"] > floor(dlat * 1000)/ 1000) & (stops["stop_lat"] < ceil(dlat * 1000) / 1000) & (stops["stop_lon"] < ceil(dlng * 1000) / 1000) & (stops["stop_lon"] > floor(dlng * 1000) / 1000)][:1]["stop_name"].values[0]

        departure = int(request.POST.get('departure'))
        departure = datetime.fromtimestamp(departure/ 1e3).strftime("%H:%M:%S")

        print(DayOfService)
        print(day)
        print(LineId)
        print(departure)
        print(origin)
        print(destination)

        days = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
        days[day] = 1

        current = Weather.objects.order_by('current').first()
        temp = (getattr(current, 'temperature') - 273) # convert to celcius
        rain = getattr(current, 'rain_1h')
        msl = getattr(current, 'pressure')
        rhum = getattr(current, 'humidity')

        # https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
        with open('../DATA_ANALYTICS/journeytimes.pickle', 'rb') as handle:
            journeytimes = pickle.load(handle)
        # https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
        with open('../DATA_ANALYTICS/distances.pickle', 'rb') as handle:
            distances = pickle.load(handle)

        routes = get_route(departure, origin, destination, day, LineId)
        # from www.mummypages.ie%2Fschool-calendar-and-holidays-20172018-republic-of-ireland&usg=AOvVaw0I7h3OF8HhiK1Om33irR_P
        # assume june july and august all schools off and we are using monthly data so do not need to give model that detail for those months as will be constant col
        holidays = ['2018-01-01','2018-01-02','2018-01-03','2018-01-04','2018-01-05','2018-02-12','2018-02-13','2018-02-14','2018-02-15','2018-02-16','2018-03-23','2018-03-23','2018-03-26','2018-03-27','2018-03-28','2018-03-29','2018-03-30','2018-04-02','2018-04-03','2018-04-04','2018-04-05','2018-04-06','2018-05-01','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-12-24','2018-12-25','2018-12-26','2018-12-27','2018-12-28','2018-12-31']
        holiday = 0
        if datetime.fromtimestamp(1.62639e+18/ 1e9).strftime("%Y-%m-%d") in holidays:
            holiday = 1

        total_time = 0
        for route in routes:
            print(route)
            try:
                timetabledjourneytime = math.log(journeytimes[route])
                distance = math.log(distances[route])
            except IndexError as e:
                return JsonResponse({'result': "NO PREDICTION AVAILABLE"}, safe=False)

            features = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0,
             'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0,
            # timetabledtimes
            'timetabledtimes': timetabledjourneytime,
            # distances
            'distance': distance,
            'rain': 0, 'temp': 0, 'rhum': 0, 'msl': 0,
            # holiday
            'holiday': holiday,
            # hour
            "hour_0": 0,
            "hour_1": 0,
            "hour_5": 0,
            "hour_6": 0,
            "hour_7": 0,
            "hour_8": 0,
            "hour_9": 0,
            "hour_10": 0,
            "hour_11": 0,
            "hour_12": 0,
            "hour_13": 0,
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
            features["hour" + "_" + departure.split(":")[1]] = 1
            model = load("../DATA_ANALYTICS/MODELS/january.joblib")
            extracted_features = list(features.values())
            print(extracted_features)
            result = model.predict([extracted_features])
            total_time += math.e ** result[0]
            print("segment time:", math.e ** result[0])
    print("total time:", total_time)
    arrival_time = str(timedelta(seconds=total_time))
    return JsonResponse({'result': arrival_time}, safe=False)


def get_route(departure, origin, destination, day, bus_route):
    day = day.lower()
    bus_route = bus_route.lower()
    days = list(calendar[calendar[day] == 1]["service_id"].values)
    day_trips = set(trips[trips["service_id"].isin(days)]["trip_id"].values)
    route_trips = set(
        trips[trips["route_id"].isin(list(routes[routes["route_short_name"] == bus_route]["route_id"].values))][
            "trip_id"].values)
    start_trips = stops[stops["stop_name"] == origin]["stop_id"].values[0]
    end_trips = stops[stops["stop_name"] == destination]["stop_id"].values[0]
    start = set(stop_times[stop_times["stop_id"] == start_trips]["trip_id"].values)
    end = set(stop_times[stop_times["stop_id"] == end_trips]["trip_id"].values)

    r = start.intersection(end)
    r = r.intersection(route_trips)
    r = r.intersection(day_trips)
    I = None
    O = None
    for trip in r:
        if re.search(".I$", trip):
            I = trip
            break

    for trip in r:
        if re.search(".O$", trip):
            O = trip
            break
    print(O)
    print(I)
    correct_direction = []
    if O != None and (
            (stop_times[(stop_times["trip_id"] == O) & (stop_times["stop_id"] == start_trips)]["stop_sequence"].values[
                0]) < (
                    stop_times[(stop_times["trip_id"] == O) & (stop_times["stop_id"] == end_trips)][
                        "stop_sequence"].values[0])):
        correct_direction = [trip for trip in r if re.search(".O$", trip)]
    elif I != None and (
            (stop_times[(stop_times["trip_id"] == I) & (stop_times["stop_id"] == start_trips)]["stop_sequence"].values[
                0]) < (
                    stop_times[(stop_times["trip_id"] == I) & (stop_times["stop_id"] == end_trips)][
                        "stop_sequence"].values[0])):
        correct_direction = [trip for trip in r if re.search(".I$", trip)]
    final = stop_times[(stop_times["trip_id"].isin(correct_direction)) & (stop_times["stop_id"] == start_trips)][
        ["trip_id", "arrival_time"]]
    final["arrival_time"] = abs(final["arrival_time"] - pd.to_timedelta(departure))
    final = final.sort_values(by="arrival_time")
    tripid = final.iloc[0]["trip_id"]
    seq = stop_times[stop_times["trip_id"] == tripid][["stop_id", "stop_sequence"]].sort_values(by="stop_sequence")
    rstart = seq[seq["stop_id"] == start_trips].index[0]
    rfin = seq[seq["stop_id"] == end_trips].index[0]
    test = seq.loc[rstart:rfin]
    final = test.merge(stops, how='left', on='stop_id')
    flist = list(final["stop_name"].values)
    flist = [stop.split(" stop ")[1] for stop in flist]
    final_routes = []
    for i in range(len(flist) - 1):
        final_routes.append(flist[i] + "_" + flist[i+1])
    final_routes
    return final_routes