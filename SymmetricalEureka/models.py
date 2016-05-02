"""
Django Models
"""
from uuid import uuid4
from django.conf import settings
from django.db import models


class Character(models.Model):
    """
    Class to Hold Character Data.
    """
    player = models.ForeignKey(settings.AUTH_USER_MODEL)
    character_name = models.CharField(max_length=256,
                                      db_index=True)
    Char_uuid = models.UUIDField(primary_key=True,
                                 default=uuid4,
                                 editable=False)
