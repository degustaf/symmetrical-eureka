# -*- coding: utf-8 -*-
"""
Classes to test models code.
"""

from __future__ import unicode_literals

# import pdb
#         pdb.set_trace()

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
# from django.utils.html import format_html

from SymmetricalEureka.models import AbilityScores, Character
from SymmetricalEureka.views import build_kwargs


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
                                   character_name="Hrothgar", alignment="CG")
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
                                   character_name="Ráðormsdóttir")
        # pylint: disable=no-member
        test_character.save()
        self.assertEqual(test_character.character_name, "Ráðormsdóttir")
        # This doesn't work in Python 2.7.  Not sure why.
        # self.assertEqual(str(test_character), format_html("Ráðormsdóttir"))


class TestCharacterAbilityScores(TestCase):
    """
    Test character fields by pulling from db.
    """
    fixtures = ['user_mike.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """Initialize database for tests."""
        # pylint: disable=no-member
        cls.test_character = Character.objects.get(character_name="Zeke")

    def test_max_ability_score(self):
        """" Test that ability scores have a max value of 25."""
        too_big = AbilityScores(character=self.test_character, which="0_STR",
                                value=26)
        with self.assertRaises(ValidationError):
            # pylint: disable=no-member
            too_big.clean_fields()

    def test_min_ability_score(self):
        """" Test that ability scores have a min value of 1."""
        too_small = AbilityScores(character=self.test_character, which="0_STR",
                                  value=0)
        with self.assertRaises(ValidationError):
            # pylint: disable=no-member
            too_small.clean_fields()

    def test_missing_ability_score(self):
        """Test that model errors out if value isn't present."""
        abil_score = AbilityScores(character=self.test_character,
                                   which="0_STR")
        with self.assertRaises(ValidationError):
            # pylint: disable=no-member
            abil_score.clean_fields()


class TestAbilityScoreClassFunctions(TestCase):
    """
    Test Class functions of the Character Class.
    """
    def test_abil_score_mod(self):
        """ Test that ability score modifier works properly."""
        self.assertEqual(AbilityScores.ability_score_mod(1), -5)
        self.assertEqual(AbilityScores.ability_score_mod(3), -4)
        self.assertEqual(AbilityScores.ability_score_mod(10), 0)
        self.assertEqual(AbilityScores.ability_score_mod(18), 4)
        self.assertEqual(AbilityScores.ability_score_mod(19), 4)
        self.assertEqual(AbilityScores.ability_score_mod(20), 5)

    def test_abs_saving_throw(self):
        """ Test abstract saving throw class method."""
        self.assertEqual(AbilityScores.abs_saving_throw(18, False),
                         AbilityScores.ability_score_mod(18))
        self.assertEqual(AbilityScores.abs_saving_throw(14, True),
                         AbilityScores.ability_score_mod(14) + 2)


class TestAbilityScoresClass(TestCase):
    """ Tests of the AbilityScores class."""
    fixtures = ['user_mike.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """Initialize database for tests."""
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")
        cls.test_character = Character.objects.get(character_name="Zeke")

    def test_ability_score_fields(self):
        """ Test that there are ability scores."""
        ab_score = AbilityScores(character=self.test_character,
                                 which=AbilityScores.WHICH_CHOICES[0][0],
                                 value=12,
                                 proficient=True)

        # pylint: disable=no-member
        ab_score.save()
        self.assertEqual(ab_score.character, self.test_character)


class TestCharacter(TestCase):
    """ Tests of the AbilityScores class."""
    fixtures = ['user_mike.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """Initialize database for tests."""
        # pylint: disable=no-member
        cls.test_character = Character.objects.get(character_name="Zeke")

    def test_proficiency_bonus(self):
        """ Test that proficiency bonus function works."""
        bonus = self.test_character.proficiency_bonus
        self.assertEqual(bonus, 2)

    def test_saving_throw_not_prof(self):
        """
        Test that Saving throw returns ability score mod if not proficient.
        """
        ability_score = AbilityScores.objects.get(
            character=self.test_character, which="0_STR")
        ability_score.proficient = False
        self.assertEqual(ability_score.saving_throw,
                         AbilityScores.ability_score_mod(ability_score.value))

    def test_saving_throw_prof(self):
        """
        Test that Saving throw returns ability score mod plus proficiency bonus
        if proficient.
        """
        ability_score = AbilityScores.objects.get(
            character=self.test_character, which="0_STR")
        ability_score.proficient = True
        self.assertEqual(ability_score.saving_throw,
                         AbilityScores.ability_score_mod(ability_score.value)
                         + ability_score.character.proficiency_bonus)


class TestFunctions(TestCase):
    """ Test Bare functions."""

    def test_build_kwargs(self):
        """ Test models.build_kwargs."""
        data = {'func': 'func', 'data': 'data', 'rubbish': 'rubbish'}
        self.assertEqual(build_kwargs(build_kwargs, data),
                         {'func': 'func', 'data': 'data'})

    def test_build_kwargs_method(self):
        """ Test models.build_kwargs doesn't contain self."""
        data = {'raw_password': 'raw_password', 'self': 'self',
                'rubbish': 'rubbish'}
        self.assertEqual(build_kwargs(User().check_password, data),
                         {'raw_password': 'raw_password'})

    def test_build_kwargs_class_method(self):
        """ Test models.build_kwargs doesn't contain cls."""
        data = {'cls': 'cls', 'ability_score': 'ability_score',
                'proficient': 'proficient', 'rubbish': 'rubbish'}
        self.assertEqual(build_kwargs(AbilityScores.abs_saving_throw, data),
                         {'ability_score': 'ability_score',
                          'proficient': 'proficient'})

    def test_build_kwargs_no_args(self):
        """ Test models.build_kwargs returns empty dict if no arguments."""
        # pylint: disable=missing-docstring
        def test_func():
            pass
        data = {'rubbish': 'rubbish'}
        self.assertEqual(build_kwargs(test_func, data), {})
