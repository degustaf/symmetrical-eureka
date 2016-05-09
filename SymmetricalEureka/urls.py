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
    url(r'^$', views.HomeView.as_view(), name='SE_home'),
    url(r'^login/$', views.LoginView.as_view(), name='SE_login'),
    url(r'^character/(?P<Char_uuid>[-0-9a-f]*)/$',
        views.DisplayCharacterView.as_view(), name='SE_character'),
    url(r'^new_character/', views.NewCharacterView.as_view(),
        name='new_character'),
    url('', include(social_urls, namespace='social')),
    url('', include(auth_urls, namespace='auth')),
]
