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
            name='acad_concentration',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_grad_qtr',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_major',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_minor',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='membership',
            name='badge_type',
            field=models.CharField(max_length=20),
        ),
    ]
