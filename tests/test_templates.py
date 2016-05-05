"""
Classes to test templates.
"""

from django.contrib.auth.models import User
# from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.test import TestCase

from SymmetricalEureka import models  # , views


class OneUserTemplateTests(TestCase):
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

    def test_homepage_has_new_char_link(self):
        """
        Test that homepage has link to new_character page.
        """
        response = self.client.get(reverse('SE_home'))
        self.assertContains(response, reverse('new_character'))


class OneCharTemplateTests(TestCase):
    """
    Class of tests for the New Character page.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        cls.test_user = User.objects.create_user("Mike", password="password")
        cls.test_character = models.Character(player=cls.test_user,
                                              character_name="Zeke")
        # pylint: disable=no-member
        cls.test_character.save()

    def setUp(self):
        """
        Log user in.
        """
        try:
            self.client.force_login(self.test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Mike", password="password")

    def test_character_shows_in_header(self):
        """
        Test that character shows on homepage.
        """
        response = self.client.get(reverse('SE_home'))
        self.assertContains(response, self.test_character.character_name)
        self.assertContains(response, reverse('SE_character', kwargs={
            'character_uuid': self.test_character.Char_uuid}))
        self.assertContains(response, "Zeke")
