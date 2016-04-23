"""
Classes to test views code.
"""

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

    def test_root_url_redirects_if_not_logged_in(self):
        """
        Test that index redirects if not logged in.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

#     def test_root_url_responds_when_logged_in(self):
#         """
#         Test that index responds if logged in.
#         """
#         test_user = User.objects.create_user("Hrothgar")
#         test_credentials = models.CredentialsModel(
#             id=test_user
#         )
#         # pylint: disable=no-member
#         test_credentials.save()
#         self.client.force_login(test_credentials)
#         response = self.client.get(reverse('index'))
#         self.assertEqual(response.status_code, 200)
