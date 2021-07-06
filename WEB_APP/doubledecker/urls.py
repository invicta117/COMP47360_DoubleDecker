from django.urls import path

from . import views

app_name = "doubledecker"

urlpatterns = [
    path('', views.main, name='index'),
    path('explore/', views.explore_view, name='explore'),
    path('model/', views.model, name='model'),
]
