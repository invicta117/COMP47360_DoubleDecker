from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='index'),
    path('explore/', views.explore_view, name='explore'),
]
