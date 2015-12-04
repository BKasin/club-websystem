# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151013_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='allDay',
            new_name='all_day',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end',
        ),
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0), help_text=b'Specify as <i>hh:mm:ss</i>', verbose_name=b'Duration'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(help_text=b'Specify as <i>yyyy-mm-dd hh:mm</i>', verbose_name=b'Start date/time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200, verbose_name=b'Title', blank=True),
        ),
    ]
