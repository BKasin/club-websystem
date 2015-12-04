# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_changed_event_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringEvent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('starts_on', models.DateField(verbose_name=b'Starts on')),
                ('ends_on', models.DateField(verbose_name=b'Ends on')),
                ('rule_type', models.IntegerField(default=200, verbose_name=b'Recurring rule', choices=[(100, b'Every day'), (200, b'Specified days of the week'), (300, b'Specified days of the month')])),
                ('repeat_each', models.IntegerField(default=1, help_text=b'Repeat every X days/weeks/months.', verbose_name=b'Repeat each')),
                ('criteria', models.CharField(max_length=200, verbose_name=b'Criteria')),
            ],
            options={
                'verbose_name': 'Recurring Event',
                'verbose_name_plural': 'Recurring Events',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='recurring',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Belongs to recurring group', blank=True, to='events.RecurringEvent', null=True),
        ),
    ]
