"""
Django Models
"""
from django.conf import settings
from django.db import models


class Character(models.Model):
    """
    Class to Hold Character Data.
    """
    player = models.ForeignKey(settings.AUTH_USER_MODEL)
    Name = models.CharField(max_length=256)
