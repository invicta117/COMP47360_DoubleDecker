# from https://www.youtube.com/watch?v=hA_VxnxCHbo&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=3

from django.test import TestCase, Client
from django.urls import reverse, resolve
from doubledecker.models import Weather
from doubledecker.views import main, explore_view, model, tourism_views


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_url = reverse('doubledecker:index')
        self.explore_url = reverse('doubledecker:explore')
        self.model_url = reverse('doubledecker:model')
        self.tourism_url = reverse('doubledecker:tourism')

    def test_main_GET(self):
        response = self.client.get(self.main_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'doubledecker/index.html')

    def test_explore_GET(self):
        response = self.client.get(self.tourism_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'doubledecker/tourism.html')

    def test_tourism_GET(self):
        response = self.client.get(self.explore_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'doubledecker/explore.html')


    def test_model_POST(self):
        Weather.objects.create(
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
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1628377200000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
                                                     'csrfmiddlewaretoken': [
                                                         'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
                                                     'action': ['post']})
        self.assertEquals(response.status_code, 200)
