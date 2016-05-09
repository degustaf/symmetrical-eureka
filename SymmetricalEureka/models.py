"""
Django Models
"""
from uuid import uuid4
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


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
    alignment = models.CharField(max_length=2,
                                 choices=(("LG", "Lawful Good"),
                                          ("NG", "Neutral Good"),
                                          ("CG", "Chaotic Good"),
                                          ("LN", "Lawful Neutral"),
                                          ("NN", "True Neutral"),
                                          ("CN", "Chaotic Neutral"),
                                          ("LE", "Lawful Evil"),
                                          ("NE", "Neutral Evil"),
                                          ("CE", "Chaotic Evil"),),
                                 default="NN")

    def get_absolute_url(self):
        """
        returns a string that points to the url to view this object.
        """
        return reverse('SE_character',
                       kwargs={'Char_uuid': self.Char_uuid})

    def __str__(self):
        return self.character_name
