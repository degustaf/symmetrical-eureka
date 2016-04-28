"""
SymmetricalEureka URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from social.apps.django_app import urls as social_urls
from SymmetricalEureka import views


admin.autodiscover()

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url('', include(social_urls, namespace='social')),
    url('', include(auth_urls, namespace='auth')),
]
