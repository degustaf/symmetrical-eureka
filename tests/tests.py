"""
Classes to test code.
"""

from django.test import TestCase
from django.core.urlresolvers import resolve, reverse

from SymmetricalEureka import views


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
