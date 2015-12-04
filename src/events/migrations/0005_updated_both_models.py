# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_created_recurring_event_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.DurationField(verbose_name=b'Duration'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name=b'Start date/time'),
        ),
        migrations.AlterField(
            model_name='recurringevent',
            name='criteria',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Criteria', blank=True),
        ),
        migrations.AlterField(
            model_name='recurringevent',
            name='repeat_each',
            field=models.IntegerField(default=1, verbose_name=b'Repeat each', validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='recurringevent',
            name='rule_type',
            field=models.IntegerField(default=200, verbose_name=b'Recurring rule', choices=[(100, b'Daily'), (200, b'Weekly'), (300, b'Monthly')]),
        ),
    ]
