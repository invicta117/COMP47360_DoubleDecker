# from https://www.youtube.com/watch?v=hA_VxnxCHbo&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=3
from model_bakery import baker
from collections import OrderedDict
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from doubledecker.models import Weather
from api.views import ShowAllWeather, apiOverview, ShowAllRoutes, ShowAllRouteStops, ShowCurrentWeather, ShowAllRouteLine, ShowRouteLine, routeStation


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.main = reverse("apiOverview")
        self.weather = reverse("Weather")
        self.cweather = reverse("currentWeather")
        self.weather = reverse("Weather")
        self.weather = reverse("Weather")
        self.factory = RequestFactory()
        self.weather_data = Weather.objects.create(
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
        self.seqRoutes_data = baker.make('doubledecker.SeqRoutes')

    def test_weather_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api/weather/?format=json')
        # Test my_view() as if it were deployed at /customer/details
        response = ShowAllWeather(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [OrderedDict([('current', '2021-06-23T11:58:49Z'), ('lat', 53.344), ('lon', -6.2672), ('timezone', '3600'), ('weather_id', 300), ('weather_icon', '09d'), ('visibility', 7000.0), ('wind_speed', 1.34), ('wind_deg', 265.0), ('wind_gust', 4.47), ('temperature', 287.43), ('feels_like', 287.32), ('temp_min', 286.97), ('temp_max', 288.67), ('pressure', 1024.0), ('humidity', 92.0), ('rain_1h', 0.0), ('snow_1h', 0.0), ('sunrise', '2021-06-23T03:57:17Z'), ('sunset', '2021-06-23T20:57:13Z'), ('description', 'Drizzle')])])

    def test_apiOverview_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        # Test my_view() as if it were deployed at /customer/details
        response = apiOverview(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_ShowAllRoutes_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        # Test my_view() as if it were deployed at /customer/details
        response = ShowAllRoutes(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_ShowAllRouteStops_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        # Test my_view() as if it were deployed at /customer/details
        response = ShowAllRouteStops(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_ShowCurrentWeather_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        # Test my_view() as if it were deployed at /customer/details
        response = ShowCurrentWeather(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_ShowAllRouteLine_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        # Test my_view() as if it were deployed at /customer/details
        response = ShowAllRouteLine(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_ShowRouteLine_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        # Test my_view() as if it were deployed at /customer/details
        response = ShowRouteLine(request, 4)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_routeStation_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        # Test my_view() as if it were deployed at /customer/details
        response = routeStation(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_individual_route_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/', {"station": "7a"})
        # Test my_view() as if it were deployed at /customer/details
        response = routeStation(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_individual_rout_error_GET(self):
        # Create an instance of a GET request.
        request = self.factory.get('/', {"station": "H19"})
        # Test my_view() as if it were deployed at /customer/details
        response = routeStation(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "Error")
