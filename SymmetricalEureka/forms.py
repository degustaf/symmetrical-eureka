"""
This file contains ModelForm classes.
"""

from django.forms import ModelForm

from . import models


class CharacterForm(ModelForm):
    """ ModelForm for models.Character."""
    class Meta:
        model = models.Character
        fields = ['character_name', 'alignment']


class AbilityScoresForm(ModelForm):
    """ ModelForm for models.AbilityScores."""
    class Meta:
        model = models.AbilityScores
        fields = ['value']
