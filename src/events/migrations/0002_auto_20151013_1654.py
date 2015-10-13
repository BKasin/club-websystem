# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('clubdata', '0006_auto_20151012_2312'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='event',
            managers=[
                ('objects', events.models.CustomEventManager()),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='clubdata.Club', help_text=b'Only the specified club will show the event on their calendar. If none, event will show on calendars of all clubs.', null=True, verbose_name=b'Specific to club'),
        ),
    ]
