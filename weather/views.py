from os import name
import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from django.contrib import messages

def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
    key= '826bad34a53487455814b855c0a266ec'
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city=  form.cleaned_data['name']
            if len(City.objects.filter(name= new_city)) !=0:
                messages.error(request, 'City exists already!!!')
            
            else:
                r = requests.get(url.format(new_city, key)).json()
                if r['cod']==200:
                    form.save()
                    messages.success(request, 'City saved')
                else:
                    messages.error(request, 'City doesn\'t exist')
 
    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city, key)).json()
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name= city_name).delete()
    return redirect('weather-home')