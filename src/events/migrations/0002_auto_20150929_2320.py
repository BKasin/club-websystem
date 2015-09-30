# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='allDay',
            field=models.BooleanField(default=False, verbose_name=b'All day event?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(verbose_name=b'End date/time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name=b'Start date/time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(help_text=b'This will show directly on the calendar.', max_length=200, verbose_name=b'Title', blank=True),
        ),
    ]
