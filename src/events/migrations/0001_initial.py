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
                ('title', models.CharField(max_length=200, verbose_name=b'Title', blank=True)),
                ('start', models.DateTimeField(verbose_name=b'Start')),
                ('end', models.DateTimeField(verbose_name=b'End')),
                ('allDay', models.BooleanField(default=False, verbose_name=b'All day')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]
