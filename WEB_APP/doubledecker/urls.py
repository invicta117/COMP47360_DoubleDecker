from django.urls import path

from . import views
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

app_name = "doubledecker"

urlpatterns = [
    path('', views.main, name='index'),
    path('explore/', views.explore_view, name='explore'),
    path('model/', views.model, name='model'),
    path('tourism/', views.tourism_views, name='tourism'),
    url(r'static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
    # path('explore_vue/', views.explore_vue, name='explore_vue'),

]
