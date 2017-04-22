# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 09:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def add_default_username(apps, schema_editor):
    userprofile = apps.get_model('SymmetricalEureka', 'userprofile')
    for user_prof in userprofile.objects.exclude(user_name__isnull=False).iterator():
        user_prof.user_name = user_prof.user.username
        user_prof.save()

class Migration(migrations.Migration):

    dependencies = [
        ('SymmetricalEureka', '0005_auto_20170418_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_name',
            field=models.CharField(db_index=True, max_length=256, null=True),
        ),
        migrations.RunPython(add_default_username),
        migrations.AlterField(
            model_name='userprofile',
            name='user_name',
            field=models.CharField(db_index=True, max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
