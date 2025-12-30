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
from django.urls import path
from nederland_weer.view.homepage_view import HomepageView
from nederland_weer.view.temperature_view import TemperatureView
from nederland_weer.view.rain_view import RainView
from nederland_weer.view.wind_view import WindView
from nederland_weer.view.sunshine_view import SunshineView
from nederland_weer.view.tropical_view import TropicalView
from nederland_weer.view.extreme_view import ExtremeView

urlpatterns = [
    path('', HomepageView().index, name='home'),
    path('temperatuur', TemperatureView().temperature, name='temperature'),
    path('temperatuur-dag/<int:first_year>/<int:last_year>/', TemperatureView().temperature_day,
         name='temperature_day'),
    path('temperatuur-jaar/<int:first_year>/<int:last_year>/',
         TemperatureView().temperature_year, name='temperature_year'),
    path('regen', RainView().rain, name='rain'),
    path('regen-hoeveelheid/<int:first_year>/<int:last_year>/', RainView().rain_amount, name='rain_amount'),
    path('regen-percentage/<int:first_year>/<int:last_year>/', RainView().rain_percentage, name='rain_percentage'),
    path('wind', WindView().wind, name='wind'),
    path('wind-snelheid/<int:first_year>/<int:last_year>/', WindView().wind_speed, name='wind_speed'),
    path('wind-richting/<int:first_year>/<int:last_year>/', WindView().wind_vector, name='wind_vector'),
    path('zon', SunshineView().sunshine, name='sunshine'),
    path('zon-percentage/<int:first_year>/<int:last_year>/',
         SunshineView().sunshine_percentage, name='sunshine_percentage'),
    path('tropisch', TropicalView().tropical, name='tropical'),
    path('tropisch-jaar/<int:first_year>/<int:last_year>/', TropicalView().tropical_year, name='tropical_year'),
    path('extreem', ExtremeView().extreme, name='extreme'),
]
