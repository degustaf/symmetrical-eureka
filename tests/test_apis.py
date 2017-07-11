# -*- coding: utf-8 -*-
"""
Classes to test views code.
"""

from __future__ import unicode_literals

from contextlib import contextmanager
from json import loads

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse  # , resolve
from django.http import (HttpResponseBadRequest, HttpResponseForbidden,
                         HttpResponseNotFound, JsonResponse)
from django.test import TestCase, Client

from six import exec_

from SymmetricalEureka.models import AbilityScores, Character, UserProfile
from SymmetricalEureka.views import ClassMethodView


class OneUserGeneric(TestCase):
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
        cls.test_user = UserProfile.objects.get(user__username="Mike")

    def setUp(self):
        """
        Log user in.
        """
        try:
            self.client.force_login(self.test_user.user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Mike", password="password")


class UserWithCharacterGeneric(OneUserGeneric):
    """ Generic Test Class that handles setup of 1 user with 1 character."""
    fixtures = ['user_mike.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """ Initialize database for tests."""
        super(UserWithCharacterGeneric, cls).setUpTestData()
        # pylint: disable=no-member
        cls.test_character = Character.objects.get(character_name="Zeke")


class TwoUsersWithCharacterGeneric(UserWithCharacterGeneric):
    """ Class of tests that require a logged in user with a character."""
    fixtures = ['user_mike.json', 'user_tim.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        super(TwoUsersWithCharacterGeneric, cls).setUpTestData()
        # pylint: disable=no-member
        cls.second_user = User.objects.get(username="Tim")

    def setUp(self):
        """
        Log user in.
        """
        try:
            self.client.force_login(self.second_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Tim", password="password")


@contextmanager
def append_extra_method(method_as_string, method_name, extra_method=None):
    """ Context manager for appending to ClassMethodView.extra_methods"""
    old_method = getattr(ClassMethodView, method_name, None)
    try:
        delattr(ClassMethodView, method_name)
    except AttributeError:
        pass
    if extra_method is not None:
        setattr(ClassMethodView, method_name, extra_method)
    ClassMethodView.extra_methods[method_as_string].append(method_name)

    try:
        yield
    finally:
        try:
            delattr(ClassMethodView, method_name)
        except AttributeError:
            pass
        if old_method is not None:
            setattr(ClassMethodView, method_name, old_method)
        ClassMethodView.extra_methods[method_as_string].pop()


class TestJsonClassViews(TestCase):
    """ Test classmethods that repsond with JSON data."""

    def test_ability_score_mods(self):
        """Test Character.ability_score_mod()."""
        input_val = 18
        output_val = AbilityScores.ability_score_mod(input_val)
        sav = AbilityScores.abs_saving_throw(input_val, False)
        url = reverse('SE_ClassMethod',
                      kwargs={'model': 'AbilityScores',
                              'method': 'ability_score_mod'})
        url = '{}?ability_score={}'.format(url, input_val)

        response = self.client.get(url)
        self.assertIsInstance(response, JsonResponse)

        resp = loads(response.content.decode('utf-8'))
        expected_result = {"ability_score_mod": output_val,
                           "abs_saving_throw": sav}
        self.assertEqual(resp, expected_result)

    def test_bad_class(self):
        """
        Test that we get a 404 response if we pass a class that doesn't exist.
        """
        url = reverse('SE_ClassMethod',
                      kwargs={'model': 'IDontExist',
                              'method': 'ability_score_mod'})
        url = '{}?ability_score={}'.format(url, 0)
        response = self.client.get(url)
        self.assertIsInstance(response, HttpResponseNotFound)

    def test_bad_method(self):
        """
        Test that we get a 404 response if we pass a method that doesn't exist.
        """
        url = reverse('SE_ClassMethod',
                      kwargs={'model': 'Character',
                              'method': 'i_dont_exist'})
        url = '{}?ability_score={}'.format(url, 0)
        response = self.client.get(url)
        self.assertIsInstance(response, HttpResponseNotFound)

    def test_attr_not_class_method(self):
        """
        Test that we get a 404 response if we pass an attribute that isn't a
        classmethod.
        """
        url = reverse('SE_ClassMethod',
                      kwargs={'model': 'Character',
                              'method': 'strength'})
        url = '{}?ability_score={}'.format(url, 0)
        response = self.client.get(url)
        self.assertIsInstance(response, HttpResponseNotFound)

    def test_method_bad_arguments(self):
        """
        Test that we get a 404 response if we pass an unexpected argument to
        the classmethod.
        """
        url = reverse('SE_ClassMethod',
                      kwargs={'model': 'AbilityScores',
                              'method': 'ability_score_mod'})
        url = '{}?i_dont_exist={}'.format(url, 0)
        response = self.client.get(url)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_method_bad_value(self):
        """
        Test that we get a 404 response if we pass an unexpected argument to
        the classmethod.
        """
        url = reverse('SE_ClassMethod',
                      kwargs={'model': 'AbilityScores',
                              'method': 'ability_score_mod'})
        url = '{}?ability_score={}'.format(url, '')
        response = self.client.get(url)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_class_not_model(self):
        """ Test that view filters out non-model classes."""
        url = reverse('SE_ClassMethod',
                      kwargs={'model': 'MinValueValidator',
                              'method': 'compare'})
        response = self.client.get(url)
        self.assertIsInstance(response, HttpResponseNotFound)

    def test_class_bad_extra_method(self):
        """ Test that view handles a bad extra_method."""
        input_val = 18
        url = reverse('SE_ClassMethod',
                      kwargs={'model': 'AbilityScores',
                              'method': 'ability_score_mod'})
        url = '{}?ability_score={}'.format(url, input_val)
        response = self.client.get(url)
        expected_response = loads(response.content.decode('utf-8'))
        expected_response['bad_method'] = None

        with append_extra_method('ability_score_mod', 'bad_method'):
            response = self.client.get(url)
            self.assertEqual(expected_response,
                             loads(response.content.decode('utf-8')))

    def test_class_extra_method_errors(self):
        """ Test that view handles a bad extra_method."""
        input_val = 18
        url = reverse('SE_ClassMethod',
                      kwargs={'model': 'AbilityScores',
                              'method': 'ability_score_mod'})
        url = '{}?ability_score={}'.format(url, input_val)
        response = self.client.get(url)
        expected_response = loads(response.content.decode('utf-8'))
        expected_response['bad_method'] = None

        with append_extra_method('ability_score_mod', 'bad_method',
                                 lambda: exec_('raise ValueError')):
            response = self.client.get(url)
            # pylint: disable=exec-used
            self.assertEqual(expected_response,
                             loads(response.content.decode('utf-8')))


class JsonCharacterViewsTest(UserWithCharacterGeneric):
    """ Test View that exposes Chracter attributes."""

    def setUp(self):
        super(JsonCharacterViewsTest, self).setUp()
        self.url = reverse('SE_character_method',
                           kwargs={'Char_uuid':
                                   self.test_character.Char_uuid,
                                   'attribute': 'strength'})

    def test_get_ability_score(self):
        """ Test """
        self.assertEqual(self.url, "/api/{}/AbilityScores/strength".format(
            self.test_character.Char_uuid))

        response = self.client.get(self.url)
        self.assertIsInstance(response, JsonResponse)

        resp = loads(response.content.decode('utf-8'))
        ability_score = AbilityScores.objects.get(
            character=self.test_character, which='0_STR')
        expected_result = {"strength": ability_score.value}
        self.assertEqual(resp, expected_result)

    def test_get_as_requires_login(self):
        """ Test that you can't get ability score unless logged in."""
        self.client.logout()

        response = self.client.get(self.url)
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_get_bad_as_404s(self):
        """
        Test that attempts to get an ability score that doesn't exist returns
        404.
        """
        url = reverse('SE_character_method',
                      kwargs={'Char_uuid': self.test_character.Char_uuid,
                              'attribute': 'i_dont_exist'})
        response = self.client.get(url)
        self.assertIsInstance(response, HttpResponseNotFound)

    def test_post_as_attr_dont_match(self):
        """
        Test that if the attribute in the url doesn't match the POST data,
        we are returned a 404.
        """
        response = self.client.post(self.url, {'i_dont_exist': 0})
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_post_ability_score(self):
        """ Test that we can post data to the db."""
        val = 11
        mod = AbilityScores.ability_score_mod(val)
        sav = mod + 0
        response = self.client.post(self.url, {'value': val})
        self.assertIsInstance(response, JsonResponse)

        resp = loads(response.content.decode('utf-8'))
        expected_result = {'strength': val, 'ability_score_mod': mod,
                           'saving_throw': sav}
        self.assertEqual(resp, expected_result)

    def test_post_as_bad_data(self):
        """ Test that if bad data is posted, it returns a 404."""
        response = self.client.post(self.url, {'value': 'not a number'})
        self.assertIsInstance(response, HttpResponseBadRequest)

        response = self.client.post(self.url, {'value': -5})
        self.assertIsInstance(response, HttpResponseBadRequest)

        # max value is 25
        response = self.client.post(self.url, {'value': 35})
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_post_bad_as_404s(self):
        """
        Test that attempts to post an ability score that doesn't exist
        returns 404.
        """
        url = reverse('SE_character_method',
                      kwargs={'Char_uuid': self.test_character.Char_uuid,
                              'attribute': 'i_dont_exist'})
        response = self.client.post(url, {'value': 0})
        self.assertIsInstance(response, HttpResponseNotFound)

    def test_post_as_csrf(self):
        """
        Test that posting an ability score properly deals with csrf tokens.
        """
        csrf_client = Client(enforce_csrf_checks=True)
        try:
            csrf_client.force_login(self.test_user.user)
        except AttributeError:
            # For Django 1.8
            csrf_client.login(username="Mike", password="password")
        response = csrf_client.get(reverse('new_character'))
        self.assertEqual(response.status_code, 200)
        csrf_token = csrf_client.cookies['csrftoken'].value
        val = 11
        response = csrf_client.post(self.url,
                                    {'value': val,
                                     'csrfmiddlewaretoken': csrf_token})
        self.assertIsInstance(response, JsonResponse)

        resp = loads(response.content.decode('utf-8'))
        mod = AbilityScores.ability_score_mod(val)
        sav = mod + 0
        expected_result = {'strength': val, 'ability_score_mod': mod,
                           'saving_throw': sav}
        self.assertEqual(resp, expected_result)


# pylint: disable=too-many-ancestors
class JsonCharacterView2UsersTest(TwoUsersWithCharacterGeneric):
    """ Test View that exposes character attributes involving 2 users."""
    def setUp(self):
        super(JsonCharacterView2UsersTest, self).setUp()
        self.url = reverse('SE_character_method',
                           kwargs={'Char_uuid':
                                   self.test_character.Char_uuid,
                                   'attribute': 'strength'})

    def test_other_user_forbidden(self):
        """
        Test that one user cannot get details of another users character.
        """
        response = self.client.get(self.url)
        self.assertIsInstance(response, HttpResponseForbidden)
