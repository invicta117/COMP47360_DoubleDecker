# the following is based on https://www.youtube.com/watch?v=0MrgsYswT1c&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=2
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from doubledecker.views import main, explore_view, model, tourism_views

class TestUrls(SimpleTestCase):

    def test_main_url_is_resolved(self):
        url = reverse('doubledecker:index')
        self.assertEquals(resolve(url).func, main)

    def test_explore_view_url_is_resolved(self):
        url = reverse('doubledecker:explore')
        self.assertEquals(resolve(url).func, explore_view)

    def test_model_url_is_resolved(self):
        url = reverse('doubledecker:model')
        self.assertEquals(resolve(url).func, model)

    def test_tourism_url_is_resolved(self):
        url = reverse('doubledecker:tourism')
        self.assertEquals(resolve(url).func, tourism_views)