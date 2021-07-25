from django.urls import path

from . import views

app_name = "doubledecker"

urlpatterns = [
    path('', views.main, name='index'),
    path('explore/', views.explore_view, name='explore'),
    path('model/', views.model, name='model'),
    path('tourism/', views.tourism_views, name='tourism'),
    # path('explore_vue/', views.explore_vue, name='explore_vue'),

]
