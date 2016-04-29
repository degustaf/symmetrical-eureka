"""
Classes to test models code.
"""

from django.test import TestCase
from django.contrib.auth.models import User

from SymmetricalEureka import models


class CharacterTest(TestCase):
    """
    Test Character class
    """

    def test_character_creation(self):
        """
        Test ability to create Character
        """
        test_user = User.objects.create_user("Mike", password="password")
        test_character = models.Character(player=test_user, Name="Zeke")
        self.assertEqual(test_character.Name, "Zeke")
