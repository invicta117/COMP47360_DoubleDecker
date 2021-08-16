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
# we can import the module we wanna test


class TestViews(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.uri = 'http://127.0.0.1:8000/api/'

    def test_apiOverview_url_is_resolved(self):
        url = reverse('apiOverview')
        self.assertEquals(resolve(url).func, apiOverview)

    def test_api_url_is_resolved(self):
        url = reverse('apiOverview')
        self.assertEquals(resolve(url).route, 'api/')

    def test_Routes_url_is_resolved(self):
        url = reverse('Routes')
        self.assertEquals(resolve(url).func, ShowAllRoutes)


    def test_currentWeather_url_is_resolved(self):
        url = reverse('currentWeather')
        self.assertEquals(resolve(url).func, ShowCurrentWeather)

    def test_route_line_url_is_resolved(self):
        url = reverse('route-line')
        self.assertEquals(resolve(url).func, ShowAllRouteLine)

    def test_line_url_is_resolved(self):
        url = reverse('line', kwargs={'s': 4})
        self.assertEquals(resolve(url).func, ShowRouteLine)

    def test_stations_url_is_resolved(self):
        url = reverse('stations')
        self.assertEquals(resolve(url).func, routeStation)


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






