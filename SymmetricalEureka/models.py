# -*- coding: utf-8 -*-
"""
Django Models
"""
from __future__ import unicode_literals, division
from re import sub
from uuid import uuid4

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Character(models.Model):
    """ Class to Hold Character Data."""
    player = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    Char_uuid = models.UUIDField(primary_key=True,
                                 default=uuid4,
                                 editable=False)

    character_name = models.CharField(max_length=256,
                                      db_index=True)

    alignment = models.CharField(max_length=2,
                                 choices=(("LG", "Lawful Good"),
                                          ("NG", "Neutral Good"),
                                          ("CG", "Chaotic Good"),
                                          ("LN", "Lawful Neutral"),
                                          ("NN", "True Neutral"),
                                          ("CN", "Chaotic Neutral"),
                                          ("LE", "Lawful Evil"),
                                          ("NE", "Neutral Evil"),
                                          ("CE", "Chaotic Evil"),))

    def get_absolute_url(self):
        """
        returns a string that points to the url to view this object.
        """
        return reverse('SE_character',
                       kwargs={'Char_uuid': self.Char_uuid})

    def __str__(self):
        return self.character_name

    # pylint: disable=no-self-use
    @property
    def proficiency_bonus(self):
        """ Return the bonus based on level."""
        # This should be abstracted once level is included.  pylint can
        # probably be removed at that point.
        return 2


class AbilityScores(models.Model):
    """ Class of ability scores for characters."""
    WHICH_CHOICES = (
        ("0_STR", "strength"),
        ("1_DEX", "dexterity"),
        ("2_CON", "constitution"),
        ("3_INT", "intelligence"),
        ("4_WIS", "wisdom"),
        ("5_CHA", "charisma"),
    )
    WHICH_ENG_2_KEY = {k: v for (v, k) in WHICH_CHOICES}
    WHICH_KEY_2_ENG = {k: v for (k, v) in WHICH_CHOICES}

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    which = models.CharField(max_length=5, choices=WHICH_CHOICES)
    value = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(25)])
    proficient = models.BooleanField(default=False)

    @classmethod
    def ability_score_mod(cls, ability_score):
        """ Calculate modifier from ability score."""
        return int(ability_score) // 2 - 5

    @property
    def saving_throw(self):
        """ Compute Saving throw for this ability score."""
        return self.abs_saving_throw(self.value,
                                     self.proficient,
                                     self.character.proficiency_bonus)

    @classmethod
    def abs_saving_throw(cls, ability_score, proficient, proficiency_bonus=2):
        """
        Compute Saving throw for abstract ability score, where proficient is a
        boolean for if the character is proficient in the ability score.
        """
        mod = AbilityScores.ability_score_mod(ability_score)
        if proficient and proficient != 'false':
            return mod + proficiency_bonus
        return mod

    @classmethod
    def abs_skills_bonus(cls, ability_score, which):
        """
        Identify all skills associated with 'which' and compute the bonus.
        """
        return {s: Skills.abs_bonus(ability_score, False, 2) for s in
                Skills.ABILITY_SCORES_2_SKILLS.get(cls.WHICH_ENG_2_KEY[which],
                                                   [])}


class Skills(models.Model):
    """ Model of Skills based on ability scores."""
    SKILLS_2_ABILITY_SCORES = {'Acrobatics': '1_DEX',
                               'Animal Handling': '4_WIS',
                               'Arcana': '3_INT',
                               'Athletics': '0_STR',
                               'Deception': '5_CHA',
                               'History': '3_INT',
                               'Insight': '4_WIS',
                               'Intimidation': '5_CHA',
                               'Investigation': '3_INT',
                               'Medicine': '4_WIS',
                               'Nature': '3_INT',
                               'Perception': '4_WIS',
                               'Performance': '5_CHA',
                               'Persuasion': '5_CHA',
                               'Religion': '3_INT',
                               'Sleight of Hand': '1_DEX',
                               'Stealth': '1_DEX',
                               'Survival': '4_WIS'}
    CHOICES = sorted([(x, x) for x in SKILLS_2_ABILITY_SCORES.keys()])
    ABILITY_SCORES_2_SKILLS = {}
    for key, val in SKILLS_2_ABILITY_SCORES.items():
        ABILITY_SCORES_2_SKILLS.setdefault(val, []).append(key)
    which = models.CharField(max_length=15, choices=CHOICES)
    ability_score = models.ForeignKey(AbilityScores, on_delete=models.CASCADE)
    proficient = models.BooleanField(default=False)

    @classmethod
    def abs_bonus(cls, ability_score, proficient, proficiency_bonus):
        """ Compute skill bonus for an abstract skill."""
        mod = AbilityScores.ability_score_mod(ability_score)
        if proficient:
            return mod + proficiency_bonus
        return mod

    @property
    def bonus(self):
        """ Compute skill bonus."""
        return self.abs_bonus(self.ability_score.value,
                              self.proficient,
                              self.ability_score.character.proficiency_bonus)

    @property
    def id_name(self):
        """ Create a name that is valid for use as an html id."""
        return sub(' ', '_', self.which)
