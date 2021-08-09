# from https://www.youtube.com/watch?v=hA_VxnxCHbo&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=3

from django.test import TestCase, Client
from django.urls import reverse, resolve
from doubledecker.models import Weather
from doubledecker.views import main, explore_view, model, tourism_views


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.main_url = reverse('doubledecker:index')
        self.explore_url = reverse('doubledecker:explore')
        self.model_url = reverse('doubledecker:model')
        self.tourism_url = reverse('doubledecker:tourism')

    def test_index_GET(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'doubledecker/index.html')

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

    def test_model_jan_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1609459200000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_feb_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1612137600000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_march_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1614556800000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_april_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1617231600000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_may_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1619823600000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_june_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1622502000000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_july_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1625094000000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_aug_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1627772400000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_sep_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1630450800000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_oct_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1633042800000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_nov_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1635724800000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_dec_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1638316800000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_holiday_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1609891200000,"line":"155","olat":53.3094124,"olng":-6.218878399999999,"dlat":53.3404818,"dlng":-6.2585706,"departure":1628448638000,"day":"Sunday"}}'],
            'csrfmiddlewaretoken': [
                'MUoGSfSBOChMUGG4cQc1TH4px9b2KwYQL5EMr94HcVLUNdtmbBIiU56Fep2jeNGH'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_multiple_legs_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1628463600000,"line":"7","olat":53.2937826,"olng":-6.1551882,"dlat":53.3525745,"dlng":-6.2641755,"departure":1628519996000,"day":"Monday"},"1":{"dayofservice":1628463600000,"line":"38","olat":53.3522444,"olng":-6.263723199999999,"dlat":53.3733762,"dlng":-6.3584013,"departure":1628523378000,"day":"Monday"}}'],
            'csrfmiddlewaretoken': [
                'G4y67JAsbd9UqOFykq6F6bQecpUEaBfIFfOcGDMyzwD2jlsQjbCW7zSuTFLVESXz'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_partial_incomplete_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1628463600000,"line":"H2","olat":53.4510581,"olng":-6.151088100000001,"dlat":53.3504505,"dlng":-6.25597,"departure":1628519346000,"day":"Monday"},"1":{"dayofservice":1628463600000,"line":"38","olat":53.3503491,"olng":-6.2607209,"dlat":53.3733762,"dlng":-6.3584013,"departure":1628523132000,"day":"Monday"}}'],
            'csrfmiddlewaretoken': ['G4y67JAsbd9UqOFykq6F6bQecpUEaBfIFfOcGDMyzwD2jlsQjbCW7zSuTFLVESXz'],
            'action': ['post']})
        self.assertEquals(response.status_code, 200)

    def test_model_result_POST(self):
        response = self.client.post(self.model_url, {'journeys': [
            '{"0":{"dayofservice":1628463600000,"line":"H2","olat":53.4510581,"olng":-6.151088100000001,"dlat":53.3504505,"dlng":-6.25597,"departure":1628519346000,"day":"Monday"},"1":{"dayofservice":1628463600000,"line":"38","olat":53.3503491,"olng":-6.2607209,"dlat":53.3733762,"dlng":-6.3584013,"departure":1628523132000,"day":"Monday"}}'],
            'csrfmiddlewaretoken': ['G4y67JAsbd9UqOFykq6F6bQecpUEaBfIFfOcGDMyzwD2jlsQjbCW7zSuTFLVESXz'],
            'action': ['post']})
        self.assertEquals(response.json(), {'result': "<p><span class='lineid'>H2 Bus</span> : Prediction not available for this journey</p><p><span class='lineid'>38 Bus</span> : 0 Hours 26 Mins 37 Seconds</p><p><span class='lineid'>Total Time</span> : 0 Hours 26 Mins 37 Seconds</p>"})
