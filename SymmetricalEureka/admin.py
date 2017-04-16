"""
Module to allow admin to access WordMadness Data.
"""
from django.contrib import admin

from .models import Character, SpellListing

admin.site.register(Character)
admin.site.register(SpellListing)
