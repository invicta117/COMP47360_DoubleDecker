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
        DayOfService = request.POST.get('dayofservice')
        day = request.POST.get('day')
        LineId = request.POST.get('line')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        TPlannedTime_Arr = request.POST.get('expectedarrival')

        print(DayOfService)
        print(day)
        print(LineId)
        print(lat)
        print(lng)
        print(TPlannedTime_Arr)

        Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday = 0,0,0,0,0,0

        current = Weather.objects.order_by('current').first()
        stop = RouteStops.objects.all().filter(stop_lat__lt=ceil(lat * 1000) / 1000).filter(stop_lat__gt=floor(lat * 1000) / 1000).filter(stop_lon__lt=ceil(lng * 1000) / 1000).filter(stop_lon__gt=floor(lng * 1000) / 1000).first()
        stoppointid = getattr(stop, "stop_name").split(" stop ")[1]
        temp = (getattr(current, 'temperature') - 32) / 1.8 # convert to celcius
        rain = getattr(current, 'rain_1h')
        msl = getattr(current, 'pressure')
        rhum = getattr(current, 'humidity')
        model = load("../DATA_ANALYTICS/MODELS/january.joblib")
        #result = model.predict([DayOfService, TPlannedTime_Arr, stoppointid, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, rain, temp, rhum, msl LineId_1, LineId_102, LineId_11, LineId_120, LineId_123, LineId_13, LineId_130, LineId_14, LineId_140, LineId_145, LineId_14C, LineId_15, LineId_151, LineId_16, LineId_16C, LineId_17A, LineId_18, LineId_184, LineId_220, LineId_25A, LineId_25B, LineId_26, LineId_27, LineId_270, LineId_27A, LineId_27B, LineId_29A, LineId_31, LineId_32, LineId_33, LineId_33A, LineId_33B, LineId_37, LineId_38, LineId_38A, LineId_39, LineId_39A, LineId_4, LineId_40, LineId_40B, LineId_40D, LineId_41, LineId_41B, LineId_41C, LineId_42, LineId_44, LineId_45A, LineId_46A, LineId_47, LineId_49, LineId_53, LineId_56A, LineId_61, LineId_65, LineId_66, LineId_66A, LineId_67, LineId_68, LineId_69, LineId_7, LineId_75, LineId_76, LineId_79, LineId_7A, LineId_83, LineId_83A, LineId_84, LineId_9])
    return JsonResponse({'result': "2020-01-01 00:00:00"}, safe=False)
