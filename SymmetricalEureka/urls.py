"""
SymmetricalEureka URL Configuration
"""
# import os
from django.conf.urls import url
from django.contrib.auth.views import login
from SymmetricalEureka import views
# from . import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^oauth2callback', views.auth_return, name='auth_return'),
    url(r'^accounts/login/$', login),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    # (r'^accounts/login/$', 'django.contrib.auth.views.login',
    #  {'template_name': 'plus/login.html'}),

    # (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),
]
