from rest_framework import serializers
from .models import Routes, Weather, RouteStops, SeqRoutes


class RoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ['current', 'temperature', 'description', 'weather_icon']


class RoutesStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStops
        fields = '__all__'


class RouteLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeqRoutes
        fields = ['route_id', 'route_short_name',
                  'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence']
