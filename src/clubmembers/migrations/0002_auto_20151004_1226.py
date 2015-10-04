# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(help_text=b'Please enter your phone number in the following format: 000-000-0000', max_length=20, verbose_name=b'Phone number', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='pin_hash',
            field=models.CharField(help_text=b'This is optional, but will be used for less critical sign-in purposes, such as checking into a project meeting or confirming your lab hours.', max_length=128, verbose_name=b'PIN', blank=True),
        ),
    ]
