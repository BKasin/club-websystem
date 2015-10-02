# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name_short', models.CharField(max_length=20, verbose_name=b'Name (short version)')),
                ('name_long', models.CharField(max_length=120, verbose_name=b'Name (long version)')),
            ],
        ),
    ]
