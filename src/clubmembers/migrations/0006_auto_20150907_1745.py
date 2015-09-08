# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0005_auto_20150907_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(max_length=1, null=True, choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
        migrations.AlterField(
            model_name='membership',
            name='badge_issue_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_until_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='receipt_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='shirt_received_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='signup_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
