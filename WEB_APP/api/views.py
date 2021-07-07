from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RoutesSerializer, WeatherSerializer, RoutesStopSerializer, RouteLineSerializer
from .models import SeqRoutes, Routes, Weather, RouteStops
# Create your views here.

import pandas as pd
import os

# from dotenv import load_dotenv
from sqlalchemy import create_engine

local_path = os.path.abspath(os.curdir)


URI = "localhost"
PORT = "3306"
PASSWORD = "123"
DB = "gtfs"

USER = "student"  # note: USER will get user name of this computer.
mysql_url = "mysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB)
# -------------------------------------------------------

# create the connection
engine = create_engine(mysql_url, echo=True)

# from https://www.youtube.com/watch?v=vlxIjXLlmxQ&t=1926s


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'weather': '/weather/',
        'routes': '/routes/'
    }
    return Response(api_urls)

# from https://www.youtube.com/watch?v=vlxIjXLlmxQ&t=1926s


@api_view(['GET'])
def ShowAllRoutes(request):
    routes = Routes.objects.all()
    serializer = RoutesSerializer(routes, many=True)
    return Response(serializer.data)

# from https://www.youtube.com/watch?v=vlxIjXLlmxQ&t=1926s


@api_view(['GET'])
def ShowAllWeather(request):
    weather = Weather.objects.all()
    serializer = WeatherSerializer(weather, many=True)
    return Response(serializer.data)

# from https://www.youtube.com/watch?v=vlxIjXLlmxQ&t=1926s


@api_view(['GET'])
def ShowAllRouteStops(request):
    routestops = RouteStops.objects.all()
    serializer = RoutesStopSerializer(routestops, many=True)
    return Response(serializer.data)

# we get the recently
# current weather from database and return the current time, temperature, description


@api_view(['GET'])
def ShowCurrentWeather(request):
    sql = f'''select current, temperature, description, weather_icon from weather order by current desc limit 1
    '''
    df = pd.read_sql_query(sql, engine)
    return Response(df)

# from https://www.youtube.com/watch?v=vlxIjXLlmxQ&t=1926s


@api_view(['GET'])
def ShowAllRouteLine(request):
    routeline = SeqRoutes.objects.all()
    serializer = RouteLineSerializer(routeline, many=True)
    return Response(serializer.data)
