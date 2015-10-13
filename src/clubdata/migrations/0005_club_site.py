# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('clubdata', '0004_auto_20151006_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='site',
            field=models.OneToOneField(null=True, to='sites.Site'),
        ),
    ]
