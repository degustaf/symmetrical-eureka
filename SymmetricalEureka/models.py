"""
Django Models
"""
# import pickle
# import base64

# from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

# from oauth2client.contrib.django_orm import FlowField
from oauth2client.contrib.django_orm import CredentialsField


class CredentialsModel(models.Model):
    """
    Model for Credentials
    """
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()


# class CredentialsAdmin(admin.ModelAdmin):
#     """
#     Model for Credentials in Admin Panel.
#     """
#     pass


# admin.site.register(CredentialsModel, CredentialsAdmin)
