"""
URL configuration for dashboard_meet_je_stad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from dashboard_meet_je_stad.view.homepage_view import HomepageView
from dashboard_meet_je_stad.view.assign_sensor_view import AssignSensorView
from dashboard_meet_je_stad.view.mailchimp_view import MailchimpView
from dashboard_meet_je_stad.view.dataset_view import DatasetView
from dashboard_meet_je_stad.view.security_view import SecurityView
from django.contrib.sitemaps.views import sitemap
from dashboard_meet_je_stad.page_sitemap import PageSitemap
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', HomepageView().index, name='home'),
    path("inloggen", SecurityView().login, name='login'),
    path("registreren", SecurityView().registrate, name='register'),
    path("verander-wachtwoord", SecurityView().change_password, name='change_password'),
    path("uitloggen", SecurityView().logout, name='logout'),
    path(
        "sitemap.xml",
        cache_page(3600)(sitemap),
        {"sitemaps": {'page' : PageSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path('admin/dataset', DatasetView().index, name='dataset'),
    path('admin/wijs-sensor-toe', AssignSensorView().index, name='assign_sensor'),
    path('admin/mailchimp', MailchimpView().index, name='mailchimp'),
    path('admin/', admin.site.urls),
]
