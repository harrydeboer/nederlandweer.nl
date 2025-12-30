"""nederland weer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
import nederland_weer.views

urlpatterns = [
    path('', nederland_weer.views.index, name='home'),
    path('temperatuur', nederland_weer.views.temperature, name='temperature'),
    path('temperatuur-dag/<int:first_year>/<int:last_year>/', nederland_weer.views.temperature_day, name='temperature_day'),
    path('temperatuur-jaar/<int:first_year>/<int:last_year>/',
         nederland_weer.views.temperature_year, name='temperature_year'),
    path('regen', nederland_weer.views.rain, name='rain'),
    path('regen-hoeveelheid/<int:first_year>/<int:last_year>/', nederland_weer.views.rain_amount, name='rain_amount'),
    path('regen-percentage/<int:first_year>/<int:last_year>/', nederland_weer.views.rain_percentage, name='rain_percentage'),
    path('wind', nederland_weer.views.wind, name='wind'),
    path('wind-snelheid/<int:first_year>/<int:last_year>/', nederland_weer.views.wind_speed, name='wind_speed'),
    path('wind-richting/<int:first_year>/<int:last_year>/', nederland_weer.views.wind_vector, name='wind_vector'),
    path('zon', nederland_weer.views.sunshine, name='sunshine'),
    path('zon-percentage/<int:first_year>/<int:last_year>/',
         nederland_weer.views.sunshine_percentage, name='sunshine_percentage'),
    path('tropisch', nederland_weer.views.tropical, name='tropical'),
    path('tropisch-jaar/<int:first_year>/<int:last_year>/', nederland_weer.views.tropical_year, name='tropical_year'),
    path('extreem', nederland_weer.views.extreme, name='extreme'),
]
