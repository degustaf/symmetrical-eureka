"""
Module to allow admin to access WordMadness Data.
"""
# from django.conf import settings
from django.contrib import admin

from .models import Character, SpellListing, UserProfile

admin.site.register(Character)
admin.site.register(SpellListing)
admin.site.register(UserProfile)
