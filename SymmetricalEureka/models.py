# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
"""
Django Models
"""
from __future__ import unicode_literals, division
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
        mod = AbilityScores.ability_score_mod(self.value)
        if self.proficient:
            return mod + self.character.proficiency_bonus
        return mod

    @classmethod
    def abs_saving_throw(cls, ability_score, proficient):
        """
        Compute Saving throw for abstract ability score, where proficient is a
        boolean for if the character is proficient in the ability score.
        """
        mod = AbilityScores.ability_score_mod(ability_score)
        if proficient and proficient != 'false':
            return mod + 2
        return mod


COMPONENTS = [('', 'None'), ('V', 'Verbal'), ('S', 'Somatic'),
              ('M', 'Material'), ('VS', 'Verbal, Somatic'),
              ('VM', 'Verbal, Material'), ('SM', 'Somatic, Material'),
              ('VSM', 'Verbal, Somatic, Material')]

SCHOOLS = [('ab', 'Abjuration'), ('cj', 'Conjuration'), ('dv', 'Divination'),
           ('en', 'Enchantment'), ('ev', 'Evocation'), ('il', 'Illusion'),
           ('ne', 'Necromancy'), ('tr', 'Transmutation')]


@python_2_unicode_compatible
class SpellListing(models.Model):
    """ Class of Spell listing."""
    name = models.CharField(max_length=256, primary_key=True)
    page = models.CharField(max_length=10, default='')
    spell_range = models.CharField(max_length=256, default='')
    duration = models.CharField(max_length=256, default='')
    casting_time = models.CharField(max_length=256, default='')

    concentration = models.BooleanField(default=False)
    ritual = models.BooleanField(default=False)

    level = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(9)])

    description = models.TextField(default='', blank=True)
    material_components = models.TextField(default='', blank=True)

    components = models.CharField(max_length=3, default='', choices=COMPONENTS)
    school = models.CharField(max_length=256, choices=SCHOOLS)

    def get_level_display(self):
        if self.level == 0:
            return 'Cantrip'
        return self.level

    def __str__(self):
        return self.name


CASTER_CLASSES = [('bd', 'Bard'), ('cl', 'Cleric'), ('dr', 'Druid'),
                  ('pd', 'Paladin'), ('rg', 'Ranger'), ('sc', 'Sorcerer'),
                  ('wa', 'Warlock'), ('wi', 'Wizard')]


class SpellClasses(models.Model):
    """ Class to contain which classes can select which spells."""
    spell = models.ForeignKey(SpellListing, on_delete=models.CASCADE)
    caster_class = models.CharField(max_length=3, choices=CASTER_CLASSES)
