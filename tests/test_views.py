"""
Classes to test views code.
"""

from django.contrib.auth.models import User
# from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.test import TestCase

# from SymmetricalEureka import models, views


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
        test_user = User.objects.create_user("Bob")
        self.client.force_login(test_user)
        response = self.client.get(reverse('SE_login'))
        # pylint: disable=no-member
        self.assertRedirects(response, reverse('SE_home'))
