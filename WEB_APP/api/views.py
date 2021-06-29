from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RoutesSerializer, WeatherSerializer, RoutesStopSerializer
from .models import Routes, Weather, RouteStops
# Create your views here.

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
