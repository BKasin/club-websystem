# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contentblocks', '0002_auto_20150915_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='created_by_user',
            field=models.ForeignKey(related_name='content_created', blank=True, to='clubmembers.Member', null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='description',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='block',
            name='edited_by_user',
            field=models.ForeignKey(related_name='content_edited', blank=True, to='clubmembers.Member', null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='edited_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True),
        ),
    ]
