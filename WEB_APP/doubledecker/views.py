from datetime import datetime
import os

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
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
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

        get_route(departure, origin, destination, day, LineId)




        # https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
        with open('distances.pickle', 'rb') as handle:
            distances = pickle.load(handle)

        features = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0,
         'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0,
        # timetabledtimes

        # distances

        'rain': 0, 'temp': 0, 'rhum': 0, 'msl': 0,
        # holiday

        # hour
        }
        features["TPlannedTime_Arr"] = TPlannedTime_Arr
        features["stoppointid"] = stoppointid
        features["TPlannedTime_Arr"] = TPlannedTime_Arr
        for day in days:
            features[day] = days[day]
        features["rain"] = rain
        features["temp"] = temp
        features["rhum"] = rhum
        features["msl"] = msl
        if str("LineId_" + LineId) in features.keys():
            features["LineId_" + LineId] = 1
        else:
            return JsonResponse({'result': "NO PREDICTION AVAILABLE"}, safe=False)
        model = load("../DATA_ANALYTICS/MODELS/january.joblib")
        extracted_features = list(features.values())
        print(extracted_features)
        result = model.predict([extracted_features])
        print("result", result[0])
        arrival_time  = datetime.datetime.fromtimestamp(floor(result[0]) + (DayOfService * 1e-9)).strftime("%m/%d/%Y, %H:%M:%S")
    return JsonResponse({'result': arrival_time}, safe=False)


def get_route(departure, origin, destination, day, bus_route):
    day = day.lower()
    days = list(calendar[calendar[day] == 1]["service_id"].values)
    day_trips = set(trips[trips["service_id"].isin(days)]["trip_id"].values)
    route_trips = set(
        trips[trips["route_id"].isin(list(routes[routes["route_short_name"] == bus_route]["route_id"].values))][
            "trip_id"].values)
    start_trips = stops[stops["stop_name"] == origin]["stop_id"].values[0]
    end_trips = stops[stops["stop_name"] == destination]["stop_id"].values[0]
    start_trips = set(stop_times[stop_times["stop_id"] == start_trips]["trip_id"].values)
    end_trips = set(stop_times[stop_times["stop_id"] == end_trips]["trip_id"].values)
    r = start_trips.intersection(end_trips)
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
    if O != None and (
            (stop_times[(stop_times["trip_id"] == O) & (stop_times["stop_id"] == start_trips)]["stop_sequence"].values[0]) < (
    stop_times[(stop_times["trip_id"] == O) & (stop_times["stop_id"] == end_trips)]["stop_sequence"].values[0])):
        correct_direction = [trip for trip in r if re.search(".O$", trip)]
    elif I != None and (
            (stop_times[(stop_times["trip_id"] == I) & (stop_times["stop_id"] == start_trips)]["stop_sequence"].values[0]) < (
    stop_times[(stop_times["trip_id"] == I) & (stop_times["stop_id"] == end_trips)]["stop_sequence"].values[0])):
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
    return flist

