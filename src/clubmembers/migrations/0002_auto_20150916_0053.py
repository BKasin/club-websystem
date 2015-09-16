# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='email',
            field=models.CharField(max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='name_first',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='name_last',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
