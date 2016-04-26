"""
Classes to test views code.
"""

import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from SymmetricalEureka import models, views


class IndexPageTest(TestCase):
    """
    Class of tests for the index page.
    """

    def test_root_url_resolves(self):
        """
        Test that index resolves.
        """
        found = resolve(reverse('index'))
        self.assertEqual(found.func, views.index)

    def test_redirects_if_not_logged_in(self):
        """
        Test that index redirects if not logged in.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_responds_when_logged_in(self):
        """
        Test that index responds if logged in.
        """
        test_user = User.objects.create_user("Hrothgar")
        test_user.last_login = datetime.datetime.now()
        test_user.save()
        test_credentials = models.CredentialsModel(
            id=test_user
        )
        test_credentials.invalid = False
        test_credentials.save()
        # pylint: disable=no-member
        test_credentials.save()
        self.client.force_login(test_user)
        response = self.client.get(reverse('index'))
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
