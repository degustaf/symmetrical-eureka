"""
Classes to test views code.
"""

from django.contrib.auth.models import User
# from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase, Client
from django.utils.html import escape

from SymmetricalEureka import models  # , views


class NoUserTests(TestCase):
    """
    Tests that don't require a user in the database.
    """

    def test_home_responds(self):
        """
        Test that home page responds.
        """
        response = self.client.get(reverse('SE_home'))
        # pylint: disable=no-member
        self.assertEqual(response.status_code, 200)

    def test_login_responds(self):
        """
        Test that login page responds.
        """
        response = self.client.get(reverse('SE_login'))
        # pylint: disable=no-member
        self.assertEqual(response.status_code, 200)

    def test_logins_redirect_to_home(self):
        """
        Test that login links tell Oauth providers to redirect back to the home
        page.
        """
        response = self.client.get(reverse('SE_login'))
        self.assertContains(response, "?next={}".format(reverse('SE_home')))

    def test_new_character_responds(self):
        """
        Test that new character page redirects.
        """
        response = self.client.get(reverse('new_character'))
        self.assertRedirects(response, reverse('SE_login') + '?next=' +
                             reverse('new_character'))


class OneUserTests(TestCase):
    """
    Tests that require a loggedin user.
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

    def test_home_responds_logged_in(self):
        """
        Test that home page responds.
        """
        response = self.client.get(reverse('SE_home'))
        # pylint: disable=no-member
        self.assertEqual(response.status_code, 200)

    def test_login_redirects(self):
        """
        Test that login page redirects if already logged in.
        """
        response = self.client.get(reverse('SE_login'))
        # pylint: disable=no-member
        self.assertRedirects(response, reverse('SE_home'))

    def test_new_character_loggedin(self):
        """
        Test that new character page responds when logged in.
        """
        response = self.client.get(reverse('new_character'))
        self.assertEqual(response.status_code, 200)

    def test_new_character_created(self):
        """
        Test that new character gets created.
        """
        csrf_client = Client(enforce_csrf_checks=True)
        try:
            csrf_client.force_login(self.test_user)
        except AttributeError:
            # For Django 1.8
            csrf_client.login(username="Mike", password="password")
        response = csrf_client.get(reverse('new_character'))
        csrf_token = csrf_client.cookies['csrftoken'].value
        response = csrf_client.post(reverse('new_character'),
                                    {'character_name': ['Hrothgar'],
                                     'csrfmiddlewaretoken': csrf_token})
        self.assertIsInstance(response, HttpResponseRedirect)
        response = csrf_client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hrothgar')
        self.assertNotContains(response, escape("['Hrothgar']"))


class UserWithCharacterTests(TestCase):
    """
    Class of tests that require a logged in user with a character.
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

    def test_character_responds(self):
        """
        Test that character page responds.
        """
        test_url = reverse('SE_character',
                           kwargs={'character_uuid':
                                   self.test_character.Char_uuid})
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)

    def test_char_on_new_char(self):
        """
        Test that character name shows up in header of New Character page.
        """
        response = self.client.get(reverse('new_character'))
        self.assertContains(response, "Zeke")
        self.assertNotContains(response, "['Zeke']")


class TwoUsersWithCharacterTests(TestCase):
    """
    Class of tests that require a logged in user with a character.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        cls.test_user = User.objects.create_user("Mike", password="password")
        cls.second_user = User.objects.create_user("Tim", password="password")
        cls.test_character = models.Character(player=cls.test_user,
                                              character_name="Zeke")
        # pylint: disable=no-member
        cls.test_character.save()

    def setUp(self):
        """
        Log user in.
        """
        try:
            self.client.force_login(self.second_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Tim", password="password")

    def test_cant_access_others_char(self):
        """
        Test that a user can't access another user's character.
        """
        test_url = reverse('SE_character',
                           kwargs={'character_uuid':
                                   self.test_character.Char_uuid})
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 401)
