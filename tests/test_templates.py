"""
Classes to test templates.
"""

from django.contrib.auth.models import User
# from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.test import TestCase

# from SymmetricalEureka import models  # , views


class NewCharacterPageTests(TestCase):
    """
    Class of tests for the New Character page.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        cls.test_user = User.objects.create_user("Mike", password="password")

    def setUp(self):
        """
        Log user in.
        """
        try:
            self.client.force_login(self.test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Mike", password="password")

    def test_has_form(self):
        """
        Test that new character page responds.
        """
        response = self.client.get(reverse('new_character'))
        self.assertContains(response, 'html')
        self.assertContains(response, 'Create New Character')
        self.assertContains(response, 'form')
        self.assertContains(response, 'Character Name')
        self.assertContains(response, 'method="post"')
        self.assertContains(response, 'submit')
