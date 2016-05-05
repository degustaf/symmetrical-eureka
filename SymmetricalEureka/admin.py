"""
Module to allow admin to access WordMadness Data.
"""
from django.contrib import admin

from .models import Character

admin.site.register(Character)
