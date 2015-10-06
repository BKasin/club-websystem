# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='logo',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'Logo of the club'),
        ),
    ]
