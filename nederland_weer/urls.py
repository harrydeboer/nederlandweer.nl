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
from nederland_weer.view.security_view import SecurityView
from django.contrib.sitemaps.views import sitemap
from nederland_weer.page_sitemap import PageSitemap


urlpatterns = [
    path('', HomepageView().index, name='home'),
    path("inloggen", SecurityView().login, name='login'),
    path("registreren", SecurityView().registrate, name='register'),
    path("verander-wachtwoord", SecurityView().change_password, name='change_password'),
    path("uitloggen", SecurityView().logout, name='logout'),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {'page' : PageSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
