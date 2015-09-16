# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0002_auto_20150916_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='photoheight',
            field=models.PositiveIntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='photowidth',
            field=models.PositiveIntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='badge_issue_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='badge_type',
            field=models.CharField(default='', max_length=20, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_amount',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_until_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='receipt_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='shirt_received_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
