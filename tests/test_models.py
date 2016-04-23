"""
Classes to test models code.
"""

from django.test import TestCase
from django.contrib.auth.models import User

from SymmetricalEureka import models


class CredentialsModelTests(TestCase):
    """
    Class of Tests of CredentialsModel class.
    """

    def test_user_credantials(self):
        """
        Test creation of user with Credentials.
        """
        test_user = User.objects.create_user("John")
        self.assertIsNotNone(test_user)
        test_credentials = models.CredentialsModel(
            id=test_user
        )
        # pylint: disable=no-member
        test_credentials.save()
        self.assertIsNotNone(test_credentials)
