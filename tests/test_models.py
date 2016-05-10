# -*- coding: utf-8 -*-
"""
Classes to test models code.
"""

from __future__ import unicode_literals

from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
# from django.utils.html import format_html

from SymmetricalEureka.models import Character


class CharacterTest(TestCase):
    """
    Test Character class
    """
    fixtures = ['user_mike.json']

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")

    def test_character_creation(self):
        """
        Test ability to create Character
        """
        test_character = Character(player=self.test_user,
                                   character_name="Hrothgar", alignment="CG",
                                   strength=9, dexterity=9, constitution=9,
                                   intelligence=9, wisdom=9, charisma=9)
        # pylint: disable=no-member
        test_character.save()
        self.assertEqual(test_character.character_name, "Hrothgar")
        self.assertEqual(test_character.alignment, "CG")
        self.assertEqual(str(test_character), "Hrothgar")

    def test_unicode_name(self):
        """
        Test that unicode character name is handles properly.
        """
        test_character = Character(player=self.test_user,
                                   character_name="Ráðormsdóttir",
                                   strength=9, dexterity=9, constitution=9,
                                   intelligence=9, wisdom=9, charisma=9)
        # pylint: disable=no-member
        test_character.save()
        self.assertEqual(test_character.character_name, "Ráðormsdóttir")
        # This doesn't work in Python 2.7.  Not sure why.
        # self.assertEqual(str(test_character), format_html("Ráðormsdóttir"))


# pylint: disable=too-many-public-methods
class TestCharacterAbilityScores(TestCase):
    """
    Test character fields by pulling from db.
    """
    fixtures = ['user_mike.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """Initialize database for tests."""
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")
        cls.test_character = Character.objects.get(character_name="Zeke")

    def missing_ability_score_errors(self, ability_score):
        """Test that model errors out if ability_score isn't present."""
        setattr(self.test_character, ability_score, None)
        # pylint: disable=no-member
        with self.assertRaises(IntegrityError):
            self.test_character.save()

    def min_ability_score_value(self, ability_score):
        """Test the ability_score has a minimum value of 1."""
        setattr(self.test_character, ability_score, 0)
        with self.assertRaises(ValidationError):
            self.test_character.clean_fields()

    def max_ability_score_value(self, ability_score):
        """Test the ability_score has a maximum value of 25."""
        setattr(self.test_character, ability_score, 26)
        with self.assertRaises(ValidationError):
            self.test_character.clean_fields()

    def test_missing_strength_errors(self):
        """Test that model errors out if strength isn't present."""
        self.missing_ability_score_errors("strength")

    def test_min_strength_value(self):
        """Test the strength has a minimum value of 1."""
        self.min_ability_score_value("strength")

    def test_max_strength_value(self):
        """Test the strength has a maximum value of 25."""
        self.max_ability_score_value("strength")

    def test_missing_dexterity_errors(self):
        """Test that model errors out if dexterity isn't present."""
        self.missing_ability_score_errors("dexterity")

    def test_min_dexterity_value(self):
        """Test the dexterity has a minimum value of 1."""
        self.min_ability_score_value("dexterity")

    def test_max_dexterity_value(self):
        """Test the dexterity has a maximum value of 25."""
        self.max_ability_score_value("dexterity")

    def test_missing_con_errors(self):
        """Test that model errors out if constitution isn't present."""
        self.missing_ability_score_errors("constitution")

    def test_min_con_value(self):
        """Test the constitution has a minimum value of 1."""
        self.min_ability_score_value("constitution")

    def test_max_con_value(self):
        """Test the constitution has a maximum value of 25."""
        self.max_ability_score_value("constitution")

    def test_missing_int_errors(self):
        """Test that model errors out if intelligence isn't present."""
        self.missing_ability_score_errors("intelligence")

    def test_min_int_value(self):
        """Test the intelligence has a minimum value of 1."""
        self.min_ability_score_value("intelligence")

    def test_max_int_value(self):
        """Test the intelligence has a maximum value of 25."""
        self.max_ability_score_value("intelligence")

    def test_missing_wisdom_errors(self):
        """Test that model errors out if wisdom isn't present."""
        self.missing_ability_score_errors("wisdom")

    def test_min_wisdom_value(self):
        """Test the wisdom has a minimum value of 1."""
        self.min_ability_score_value("wisdom")

    def test_max_wisdom_value(self):
        """Test the wisdom has a maximum value of 25."""
        self.max_ability_score_value("wisdom")

    def test_missing_charisma_errors(self):
        """Test that model errors out if charisma isn't present."""
        self.missing_ability_score_errors("charisma")

    def test_min_charisma_value(self):
        """Test the charisma has a minimum value of 1."""
        self.min_ability_score_value("charisma")

    def test_max_charisma_value(self):
        """Test the charisma has a maximum value of 25."""
        self.max_ability_score_value("charisma")


class TestiCharClassFunctions(TestCase):
    """
    Test Class functions of the Character Class.
    """
    def test_abil_score_mod(self):
        """Test that ability score modifier works properly."""
        self.assertEqual(Character.ability_score_mod(1), -5)
        self.assertEqual(Character.ability_score_mod(3), -4)
        self.assertEqual(Character.ability_score_mod(10), 0)
        self.assertEqual(Character.ability_score_mod(18), 4)
        self.assertEqual(Character.ability_score_mod(19), 4)
        self.assertEqual(Character.ability_score_mod(20), 5)
