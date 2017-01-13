"""
Classes to test urls code.
"""

from uuid import uuid4

# from django.contrib.auth.models import User
# from django.contrib.auth.views import login
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.contrib.auth import views as auth_views
from social_django import views as social_views

from SymmetricalEureka import views

# For url testing class based views:
# http://stackoverflow.com/questions/27320821/django-how-to-assert-url-pattern-resolves-to-correct-class-based-view-function
# Or use pdb.setbreak.


class UrlTest(TestCase):
    """
    Class of tests for the urls
    """

    def test_home_url_resolves(self):
        """
        Test that index resolves.
        """
        found = resolve(reverse('SE_home'))
        self.assertEqual(found.func.__name__, views.HomeView.__name__)

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

    def test_character_urls_resolve(self):
        """
        Test that Character urls are included.
        """
        found = resolve(reverse('SE_character',
                                kwargs={'Char_uuid': uuid4()}))
        self.assertEqual(found.func.__name__,
                         views.DisplayCharacterView.__name__)

    def test_new_character_url_resolves(self):
        """
        Test that new character url resolves.
        """
        found = resolve(reverse('new_character'))
        self.assertEqual(found.func.__name__, views.NewCharacterView.__name__)
