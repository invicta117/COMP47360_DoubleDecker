from django.test import TestCase,RequestFactory
from rest_framework.response import Response

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.urls import resolve
from .views import apiOverview,ShowAllRoutes,ShowAllWeather,ShowAllRouteStops,ShowCurrentWeather, ShowAllRouteLine,ShowRouteLine,routeStation
# we can import the module we wanna test


class TestViews(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.uri = 'http://127.0.0.1:8000/api/'

    ''' test index '''
    def test_index(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'doubledecker/index.html')
        self.assertEqual(response.status_code, 200)

    ''' test base html '''
    def test_base(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'doubledecker/base.html')
        self.assertEqual(response.status_code, 200)






