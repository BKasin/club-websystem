# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0004_auto_20150907_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='priv_level',
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_concentration',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_grad_qtr',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_major',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_minor',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='pin_hash',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='shirt_size',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='badge_issue_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='badge_type',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_amount',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_until_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='receipt_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='shirt_received_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
