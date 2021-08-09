# the following is based on the code presented at https://www.youtube.com/watch?v=28zdhLPZ1Zk&t=422s
import os
import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.support.ui import Select
from model_bakery import baker
from selenium.webdriver.common.keys import Keys
from doubledecker.models import Weather
from selenium.webdriver.common.alert import Alert

class TestProjectSelenium(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('doubledecker/test/chromedriver.exe')
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


    def tearDown(self):
        self.browser.close()

    def test_add_attraction(self):
        self.browser.get(self.live_server_url + reverse('doubledecker:tourism'))
        self.browser.find_element_by_id('add-stop').click()
        self.browser.find_element_by_id('add-stop').click()
        num_attraction = len(self.browser.find_elements_by_class_name('waypoints'))
        self.assertEquals(num_attraction, 3)

    def test_add_multiple_attraction(self):
        self.browser.get(self.live_server_url + reverse('doubledecker:tourism'))
        self.browser.find_element_by_id('add-stop').click()
        self.browser.find_element_by_id('add-stop').click()
        self.browser.find_element_by_id('add-stop').click()
        self.browser.find_element_by_id('add-stop').click()
        num_attraction = len(self.browser.find_elements_by_class_name('waypoints'))
        self.assertEquals(num_attraction, 3)

    def test_remove_attraction(self):
        self.browser.get(self.live_server_url + reverse('doubledecker:tourism'))
        self.browser.find_element_by_id('add-stop').click()
        self.browser.find_element_by_id('remove-stop').click()
        num_attraction = len(self.browser.find_elements_by_class_name('waypoints'))
        self.assertEquals(num_attraction, 1)

    def test_remove_multiple_attraction(self):
        self.browser.get(self.live_server_url + reverse('doubledecker:tourism'))
        self.browser.find_element_by_id('remove-stop').click()
        self.browser.find_element_by_id('remove-stop').click()
        num_attraction = len(self.browser.find_elements_by_class_name('waypoints'))
        self.assertEquals(num_attraction, 1)

    def test_go_tourism(self):
        self.browser.get(self.live_server_url + reverse('doubledecker:tourism'))
        # the following is from https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
        ddelement = Select(self.browser.find_element_by_id('start'))
        ddelement.select_by_value("General Post Office, Dublin, O'Connell Street Lower, North City, Dublin 1, Ireland")
        self.browser.find_element_by_id('submit').click()
        time.sleep(2)
        route = self.browser.find_element_by_id('route4').get_attribute('innerHTML')
        self.assertNotEqual(route, "Directions")

    def test_go_main(self):
        self.browser.get(self.live_server_url)
        # the following is from https://stackoverflow.com/questions/18557275/how-to-locate-and-insert-a-value-in-a-text-box-input-using-python-selenium
        origin = self.browser.find_element_by_id('from')
        origin.send_keys('UCD Sports Centre, Belfield, Dublin, Ireland')
        destination = self.browser.find_element_by_id('to')
        destination.send_keys('Trinity College, College Green, Dublin 2, Ireland')
        self.browser.find_element_by_id('submit').click()
        time.sleep(5)
        result = self.browser.find_element_by_id('result').get_attribute('innerHTML')
        self.assertNotEqual(result, '')

    def test_go_main_error(self):
        self.browser.get(self.live_server_url)
        # the following is from https://stackoverflow.com/questions/18557275/how-to-locate-and-insert-a-value-in-a-text-box-input-using-python-selenium
        origin = self.browser.find_element_by_id('from')
        origin.send_keys('UCD Sports Centre, Belfield, Dublin, Ireland')
        destination = self.browser.find_element_by_id('to')
        destination.send_keys('Aran Islands, County Galway, Ireland')
        self.browser.find_element_by_id('submit').click()
        time.sleep(5)
        result = self.browser.find_element_by_id('result').get_attribute('innerHTML')
        error = self.browser.find_element_by_id('error').get_attribute('innerHTML')
        self.assertEqual(result, '')
        self.assertNotEqual(error, '')

    def test_explore_error(self):
        self.browser.get(self.live_server_url + reverse('doubledecker:explore'))
        # the following is from https://www.geeksforgeeks.org/how-to-handle-alert-prompts-in-selenium-python/
        origin = self.browser.find_element_by_id('searchTxt')
        origin.send_keys('h71')
        self.browser.find_element_by_id('myBtn').click()
        time.sleep(1)
        alert = Alert(self.browser)
        # get alert text
        print(alert.text)
        self.assertEqual(alert.text, 'This route is not in service. INVALID_REQUEST')
        alert.accept()
