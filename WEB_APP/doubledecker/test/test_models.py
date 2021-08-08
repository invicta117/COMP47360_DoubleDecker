# from https://www.youtube.com/watch?v=IKnp2ckuhzg&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=4

from django.test import TestCase, Client
from django.urls import reverse, resolve
from doubledecker.models import Weather


class TestModels(TestCase):

    def setUp(self):
        self.weather = Weather.objects.create(
            lat=53.344,
            lon=-6.2672,
            timezone=3600,
            current='2021-06-23 11:58:49',
            weather_id=300,
            weather_icon='09d',
            visibility=7000,
            wind_speed=1.34,
            wind_deg=265,
            wind_gust=4.47,
            temperature=287.43,
            feels_like=287.32,
            temp_min=286.97,
            temp_max=288.67,
            pressure=1024,
            humidity=92,
            rain_1h=0,
            snow_1h=0,
            sunrise='2021-06-23 03:57:17',
            sunset='2021-06-23 20:57:13',
            description='Drizzle',
        )

    def test_name(self):
        self.assertEquals(self.weather._meta.model_name, "weather")

    def test_lat(self):
        self.assertEquals(self.weather.lat, 53.344)

    def test_lon(self):
        self.assertEquals(self.weather.lon, -6.2672)

    def test_timezone(self):
        self.assertEquals(self.weather.timezone, 3600)

    def test_current(self):
        self.assertEquals(self.weather.current, '2021-06-23 11:58:49')

    def test_weather_id(self):
        self.assertEquals(self.weather.weather_id, 300)

    def test_weather_icon(self):
        self.assertEquals(self.weather.weather_icon, '09d')

    def test_visibility(self):
        self.assertEquals(self.weather.visibility, 7000)

    def test_wind_speed(self):
        self.assertEquals(self.weather.wind_speed, 1.34)

    def test_wind_deg(self):
        self.assertEquals(self.weather.wind_deg, 265)

    def test_wind_gust(self):
        self.assertEquals(self.weather.wind_gust, 4.47)

    def test_temperature(self):
        self.assertEquals(self.weather.temperature, 287.43)

    def test_feels_like(self):
        self.assertEquals(self.weather.feels_like, 287.32)

    def test_temp_min(self):
        self.assertEquals(self.weather.temp_min, 286.97)

    def test_temp_max(self):
        self.assertEquals(self.weather.temp_max, 288.67)

    def test_pressure(self):
        self.assertEquals(self.weather.pressure, 1024)

    def test_humidity(self):
        self.assertEquals(self.weather.humidity, 92)

    def test_rain_1h(self):
        self.assertEquals(self.weather.rain_1h, 0)

    def test_snow_1h(self):
        self.assertEquals(self.weather.snow_1h, 0)

    def test_sunrise(self):
        self.assertEquals(self.weather.sunrise, '2021-06-23 03:57:17')

    def test_sunset(self):
        self.assertEquals(self.weather.sunset, '2021-06-23 20:57:13')

    def test_description(self):
        self.assertEquals(self.weather.description, 'Drizzle')