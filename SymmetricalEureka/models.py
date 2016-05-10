# -*- coding: utf-8 -*-
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
    """
    Class to Hold Character Data.
    """
    player = models.ForeignKey(settings.AUTH_USER_MODEL)
    Char_uuid = models.UUIDField(primary_key=True,
                                 default=uuid4,
                                 editable=False)

    character_name = models.CharField(max_length=256,
                                      db_index=True)
    # Ability Scores
    strength = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(25)])
    dexterity = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(25)])
    constitution = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(25)])
    intelligence = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(25)])
    wisdom = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(25)])
    charisma = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(25)])

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

    @classmethod
    def ability_score_mod(cls, ability_score):
        """ Calculate modifier from ability score."""
        return int(ability_score) // 2 - 5
