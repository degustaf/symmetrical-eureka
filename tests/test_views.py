"""
Classes to test views code.
"""

# from django.contrib.auth.models import User
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
