from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns= [
    path('', views.home, name= 'weather-home'),
    path('delete/<city_name>/', views.delete_city, name= 'weather-delete')


]