"""
Classes to test views code.
"""

from django.contrib.auth.models import User
# from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase

from SymmetricalEureka import models  # , views


class IndexPageTest(TestCase):
    """
    Class of tests for the home page.
    """

    def test_home_responds(self):
        """
        Test that home page responds.
        """
        response = self.client.get(reverse('SE_home'))
        # pylint: disable=no-member
        self.assertEqual(response.status_code, 200)

    def test_home_responds_logged_in(self):
        """
        Test that home page responds.
        """
        test_user = User.objects.create_user("Bob", password="password")
        try:
            self.client.force_login(test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Bob", password="password")
        response = self.client.get(reverse('SE_home'))
        # pylint: disable=no-member
        self.assertEqual(response.status_code, 200)


class LoginPageTest(TestCase):
    """
    Class of tests for the login page.
    """

    def test_login_responds(self):
        """
        Test that login page responds.
        """
        response = self.client.get(reverse('SE_login'))
        # pylint: disable=no-member
        self.assertEqual(response.status_code, 200)

    def test_login_redirects(self):
        """
        Test that login page redirects if already logged in.
        """
        test_user = User.objects.create_user("Bob", password="password")
        try:
            self.client.force_login(test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Bob", password="password")
        response = self.client.get(reverse('SE_login'))
        # pylint: disable=no-member
        self.assertRedirects(response, reverse('SE_home'))

    def test_logins_redirect_to_home(self):
        """
        Test that login links tell Oauth providers to redirect back to the home
        page.
        """
        response = self.client.get(reverse('SE_login'))
        self.assertContains(response, "?next={}".format(reverse('SE_home')))


class CharacterPageTests(TestCase):
    """
    Class of tests for the Character page.
    """

    def test_character_responds(self):
        """
        Test that character page responds.
        """
        test_user = User.objects.create_user("Mike", password="password")
        test_character = models.Character(player=test_user,
                                          character_name="Zeke")
        # pylint: disable=no-member
        test_character.save()
        try:
            self.client.force_login(test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Mike", password="password")
        test_url = reverse('SE_character',
                           kwargs={'character_uuid':
                                   test_character.Char_uuid})
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)

    def test_cant_access_others_char(self):
        """
        Test that a user can't access another user's character.
        """
        test_user = User.objects.create_user("Mike", password="password")
        second_user = User.objects.create_user("Tim", password="password")
        test_character = models.Character(player=test_user,
                                          character_name="Zeke")
        # pylint: disable=no-member
        test_character.save()
        try:
            self.client.force_login(second_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Tim", password="password")
        test_url = reverse('SE_character',
                           kwargs={'character_uuid':
                                   test_character.Char_uuid})
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 401)


class NewCharacterPageTests(TestCase):
    """
    Class of tests for the New Character page.
    """

    def test_new_character_responds(self):
        """
        Test that new character page responds.
        """
        response = self.client.get(reverse('new_character'))
        self.assertRedirects(response, reverse('SE_login') + '?next=' +
                             reverse('new_character'))

    def test_new_character_loggedin(self):
        """
        Test that new character page responds when logged in.
        """
        test_user = User.objects.create_user("Mike", password="password")
        try:
            self.client.force_login(test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Mike", password="password")
        response = self.client.get(reverse('new_character'))
        self.assertEqual(response.status_code, 200)

    def test_new_character_created(self):
        """
        Test that new character gets created.
        """
        test_user = User.objects.create_user("Mike", password="password")
        try:
            self.client.force_login(test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Mike", password="password")
        response = self.client.post(reverse('new_character'),
                                    {'character_name': 'Hrothgar'})
        # self.assertEqual(response.status, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
