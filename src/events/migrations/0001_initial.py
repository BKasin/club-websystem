# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(help_text=b'This will show directly on the calendar.', max_length=200, verbose_name=b'Title', blank=True)),
                ('start', models.DateTimeField(verbose_name=b'Start date/time')),
                ('end', models.DateTimeField(verbose_name=b'End date/time')),
                ('allDay', models.BooleanField(default=False, verbose_name=b'All day event?')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]
