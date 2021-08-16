# the following is based on https://www.youtube.com/watch?v=0MrgsYswT1c&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=2
from django.test import TestCase,RequestFactory
from rest_framework.response import Response

# Create your test here.
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.urls import resolve, reverse
from api.views import apiOverview,ShowAllRoutes,ShowAllRouteStops,ShowCurrentWeather, ShowAllRouteLine,ShowRouteLine,routeStation
from api.routeStations import explore
# we can import the module we wanna test


class TestViews(TestCase):
    def test_routeStations(self):
        self.explore = explore("Wednesday", "7a")
        self.assertEquals(type(self.explore), list)
        self.assertNotEqual(self.explore, [])
