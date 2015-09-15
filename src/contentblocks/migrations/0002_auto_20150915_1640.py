# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0001_initial'),
        ('contentblocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('uniquetitle', models.CharField(unique=True, max_length=20)),
                ('description', models.CharField(max_length=100, null=True)),
                ('blob', models.TextField()),
                ('published', models.BooleanField()),
                ('datatype', models.CharField(max_length=3, choices=[(b'md', b'CommonMark'), (b'htm', b'HTML'), (b'txt', b'Raw Text')])),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('club', models.ForeignKey(to='clubmembers.Club')),
                ('created_by_user', models.ForeignKey(related_name='content_created', to='clubmembers.Member', null=True)),
                ('edited_by_user', models.ForeignKey(related_name='content_edited', to='clubmembers.Member', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='content',
            name='club',
        ),
        migrations.RemoveField(
            model_name='content',
            name='created_by_user',
        ),
        migrations.RemoveField(
            model_name='content',
            name='edited_by_user',
        ),
        migrations.DeleteModel(
            name='Content',
        ),
    ]
