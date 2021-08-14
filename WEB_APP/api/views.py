import datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RoutesSerializer, WeatherSerializer, RoutesStopSerializer, RouteLineSerializer
from .models import SeqRoutes, Routes, Weather, RouteStops
# Create your views here.
from .routeStations import explore
import pandas as pd
import os

# from dotenv import load_dotenv
from sqlalchemy import create_engine

local_path = os.path.abspath(os.curdir)


URI = "localhost"
PORT = "3306"
PASSWORD = os.environ["DBPASS"]
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
        'routes': '/routes/',
        'route-detail': '/route-line/<int:id>'
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
    weather = Weather.objects.order_by('current').first()
    serializer = WeatherSerializer(weather, many=False)
    return Response(serializer.data)

# from https://www.youtube.com/watch?v=vlxIjXLlmxQ&t=1926s


@api_view(['GET'])
def ShowAllRouteLine(request):
    routeline = SeqRoutes.objects.all()
    serializer = RouteLineSerializer(routeline, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ShowRouteLine(request, s):
    routeline = SeqRoutes.objects.filter(route_short_name=s)
    serializer = RouteLineSerializer(routeline, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def routeStation(request):
    try:
        station = request.query_params["station"]
        day = datetime.datetime.today().strftime('%A') # https://stackoverflow.com/questions/9847213/how-do-i-get-the-day-of-week-given-a-date
        routes = explore(day, station)
    except IndexError:
        return Response("Error")
    except KeyError as e:
        return Response("Error")
    return Response(routes)




