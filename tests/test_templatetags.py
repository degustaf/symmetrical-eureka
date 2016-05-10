# -*- coding: utf-8 -*-
"""
Classes to test templatetags code.
"""

# from __future__ import unicode_literals

# from django.db.utils import IntegrityError
from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
from django.test import TestCase
# from django.utils.html import format_html

from SymmetricalEureka.models import Character
from SymmetricalEureka.templatetags.SymmetricalEureka import\
    _bs_ability_score_display  # _bs_ability_score_field


class AbilityScoreDisplayTest(TestCase):
    """
    Tests for the _bs_ability_score_display function.
    """
    fixtures = ['user_mike.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """ Initialize database for tests."""
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")
        cls.test_character = Character.objects.get(character_name="Zeke")

    def test_p_class_placed_properly(self):
        """test that the appropriate class is placed within p tag."""

        result = _bs_ability_score_display(self.test_character, "strength")
        expected_result = '<p class="{}" id="{}">{}</p>'.format(
            'ability-score-mod badge', 'id_mod_strength',
            Character.ability_score_mod(self.test_character.strength))

        self.assertInHTML(expected_result, result)
