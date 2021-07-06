import datetime
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
        lat = float(request.POST.get('lat'))
        lng = float(request.POST.get('lng'))
        TPlannedTime_Arr = int(request.POST.get('expectedarrival')) * 1e-3

        print(DayOfService)
        print(day)
        print(LineId)
        print(lat)
        print(lng)
        print(TPlannedTime_Arr)

        days = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
        days[day] = 1

        current = Weather.objects.order_by('current').first()
        stop = RouteStops.objects.all().filter(stop_lat__lt=ceil((lat * 1000) / 1000)).filter(stop_lat__gt=floor((lat * 1000) / 1000)).filter(stop_lon__lt=(ceil(lng * 1000) / 1000)).filter(stop_lon__gt=(floor(lng * 1000) / 1000)).first()
        stoppointid = int(getattr(stop, "stop_name").split(" stop ")[1])
        temp = (getattr(current, 'temperature') - 273) # convert to celcius
        rain = getattr(current, 'rain_1h')
        msl = getattr(current, 'pressure')
        rhum = getattr(current, 'humidity')
        features = {'TPlannedTime_Arr': 0, 'stoppointid': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0,
         'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0, 'rain': 0, 'temp': 0, 'rhum': 0, 'msl': 0,
         'LineId_1': 0, 'LineId_102': 0, 'LineId_11': 0, 'LineId_120': 0, 'LineId_123': 0, 'LineId_13': 0,
         'LineId_130': 0, 'LineId_14': 0, 'LineId_140': 0, 'LineId_145': 0, 'LineId_14C': 0, 'LineId_15': 0,
         'LineId_151': 0, 'LineId_16': 0, 'LineId_16C': 0, 'LineId_17A': 0, 'LineId_18': 0, 'LineId_184': 0,
         'LineId_220': 0, 'LineId_25A': 0, 'LineId_25B': 0, 'LineId_26': 0, 'LineId_27': 0, 'LineId_270': 0,
         'LineId_27A': 0, 'LineId_27B': 0, 'LineId_29A': 0, 'LineId_31': 0, 'LineId_32': 0, 'LineId_33': 0,
         'LineId_33A': 0, 'LineId_33B': 0, 'LineId_37': 0, 'LineId_38': 0, 'LineId_38A': 0, 'LineId_39': 0,
         'LineId_39A': 0, 'LineId_4': 0, 'LineId_40': 0, 'LineId_40B': 0, 'LineId_40D': 0, 'LineId_41': 0,
         'LineId_41B': 0, 'LineId_41C': 0, 'LineId_42': 0, 'LineId_44': 0, 'LineId_45A': 0, 'LineId_46A': 0,
         'LineId_47': 0, 'LineId_49': 0, 'LineId_53': 0, 'LineId_56A': 0, 'LineId_61': 0, 'LineId_65': 0,
         'LineId_66': 0, 'LineId_66A': 0, 'LineId_67': 0, 'LineId_68': 0, 'LineId_69': 0, 'LineId_7': 0, 'LineId_75': 0,
         'LineId_76': 0, 'LineId_79': 0, 'LineId_7A': 0, 'LineId_83': 0, 'LineId_83A': 0, 'LineId_84': 0,
         'LineId_9': 0}
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
