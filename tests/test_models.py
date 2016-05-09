# -*- coding: utf-8 -*-
"""
Classes to test models code.
"""

from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User

from SymmetricalEureka import models


class CharacterTest(TestCase):
    """
    Test Character class
    """

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        cls.test_user = User.objects.create_user("Mike", password="password")

    def test_character_creation(self):
        """
        Test ability to create Character
        """
        test_character = models.Character(player=self.test_user,
                                          character_name="Zeke",
                                          alignment="CN")
        self.assertEqual(test_character.character_name, "Zeke")
        self.assertEqual(test_character.alignment, "CN")

    def test_unicode_name(self):
        """
        Test that unicode character name is handles properly.
        """
        test_character = models.Character(player=self.test_user,
                                          character_name="Ráðormsdóttir")
        self.assertEqual(test_character.character_name, "Ráðormsdóttir")
