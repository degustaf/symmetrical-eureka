# -*- coding: utf-8 -*-
"""
Classes to test views code.
"""

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse  # , resolve
from django.http import HttpResponseRedirect
from django.test import TestCase, Client
from django.utils.html import escape

from SymmetricalEureka.models import AbilityScores, Character, Skills


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
        url = reverse('new_character')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('SE_login') + '?next=' + url)


class OneUserTests(TestCase):
    """
    Tests that require a loggedin user.
    """
    fixtures = ['user_mike.json']

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")

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
        data = {'character_name': ['Hrothgar'],
                'alignment': ['CG'],
                'strength-value': [9],
                'dexterity-value': [9],
                'constitution-value': [9],
                'intelligence-value': [9],
                'wisdom-value': [9],
                'charisma-value': [9],
                'csrfmiddlewaretoken': csrf_token}
        data.update({x: False for x in Skills.SKILLS_2_ABILITY_SCORES.keys()})

        response = csrf_client.post(reverse('new_character'), data)
        self.assertIsInstance(response, HttpResponseRedirect)
        character = Character.objects.get(character_name="Hrothgar")
        self.assertEqual(AbilityScores.objects.filter(
            character=character).count(), len(AbilityScores.WHICH_CHOICES))
        self.assertEqual(Skills.objects.filter(
            ability_score__character=character).count(), len(Skills.CHOICES))

        response = csrf_client.get(response.url).render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hrothgar')
        self.assertNotContains(response, escape("['Hrothgar']"))
        self.assertContains(response, AbilityScores.ability_score_mod(9))

    def test_new_char_bad_validation(self):
        """
        Test that bad validation is handles properly.
        """
        response = self.client.post(reverse('new_character'),
                                    {'character_name': ['Hrothgar'],
                                     'alignment': ['ZZ'],
                                     'strength-value': [9],
                                     'dexterity-value': [9],
                                     'constitution-value': [9],
                                     'intelligence-value': [9],
                                     'wisdom-value': [9],
                                     'charisma-value': [9]})
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(character_name="Hrothgar")


class UserWithCharacterTests(TestCase):
    """
    Class of tests that require a logged in user with a character.
    """
    fixtures = ['user_mike.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")
        cls.test_character = Character.objects.get(character_name="Zeke")

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
                           kwargs={'Char_uuid':
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
    fixtures = ['user_mike.json', 'user_tim.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")
        cls.second_user = User.objects.get(username="Tim")
        cls.test_character = Character.objects.get(character_name="Zeke")

    def setUp(self):
        """ Log user in."""
        try:
            self.client.force_login(self.second_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Tim", password="password")

    def test_cant_access_others_char(self):
        """ Test that a user can't access another user's character."""
        test_url = reverse('SE_character',
                           kwargs={'Char_uuid':
                                   self.test_character.Char_uuid})
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 403)


class TestUnicode(TestCase):
    """ Tests to verify that unicode is being handled properly."""
    fixtures = ['user_mike.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """ Initialize database for tests."""
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")
        cls.test_character = Character.objects.get(character_name="Zeke")
        cls.test_character.character_name = "Ráðormsdóttir"
        cls.test_character.save()
        cls.test_character_url = reverse('SE_character',
                                         kwargs={'Char_uuid':
                                                 cls.test_character.Char_uuid})

    def setUp(self):
        """ Log user in."""
        try:
            self.client.force_login(self.test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Mike", password="password")

    def test_name_in_header(self):
        """ Test that unicode character name appears in header."""
        response = self.client.get(reverse('SE_home'))
        self.assertContains(response, "Ráðormsdóttir")

    def test_name_on_character_page(self):
        """ Test that unicode name appears as title on character page."""
        response = self.client.get(self.test_character_url)
        self.assertContains(response, "<h1>Ráðormsdóttir</h1>".encode('utf-8'))
