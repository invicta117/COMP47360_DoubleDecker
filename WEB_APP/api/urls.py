from django.urls import path

from . import views

urlpatterns = [ # from https://www.youtube.com/watch?v=vlxIjXLlmxQ&t=1926s
    path('', views.apiOverview, name='apiOverview'),
    path('routes/', views.ShowAllRoutes, name='Routes'),
    path('weather/', views.ShowAllWeather, name='Weather'),
]