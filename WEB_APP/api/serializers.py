from rest_framework import serializers
from .models import Routes, Weather, RouteStops

class RoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = '__all__'

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'

class RoutesStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStops
        fields = '__all__'