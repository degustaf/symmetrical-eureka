"""
Classes to test urls code.
"""

# from django.contrib.auth.models import User
# from django.contrib.auth.views import login
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.contrib.auth import views as auth_views
from social.apps.django_app import views as social_views

from SymmetricalEureka import views


class UrlTest(TestCase):
    """
    Class of tests for the urls
    """

    def test_home_url_resolves(self):
        """
        Test that index resolves.
        """
        found = resolve(reverse('home'))
        self.assertEqual(found.func, views.home)

    def test_social_urls_resolve(self):
        """
        Test that social urls are included.
        """
        found = resolve(reverse('social:begin', kwargs={'backend': 'TEST'}))
        self.assertEqual(found.func, social_views.auth)

    def test_auth_urls_resolve(self):
        """
        Test that auth urls are included.
        """
        found = resolve(reverse('auth:logout'))
        self.assertEqual(found.func, auth_views.logout)
