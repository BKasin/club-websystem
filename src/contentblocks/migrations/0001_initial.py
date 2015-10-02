# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubdata', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('uniquetitle', models.CharField(help_text=b'This is used internally to lookup this piece of content, so use something short and logical, and use a prefix that can be filtered on later (competition_ccdc, project_securitysystem, etc.)', unique=True, max_length=20, verbose_name=b'Unique title')),
                ('description', models.CharField(help_text=b'Longer description, if any.', max_length=100, verbose_name=b'Description', blank=True)),
                ('datatype', models.CharField(help_text=b'This tells the website how to process and render the content for the user.', max_length=3, verbose_name=b'Type of content', choices=[(b'md', b'CommonMark'), (b'htm', b'HTML'), (b'txt', b'Raw Text')])),
                ('blob', models.TextField(help_text=b'This is the actual block of content. Specify the format above.', verbose_name=b'Content block')),
                ('published', models.BooleanField(help_text=b'If true, this content will be visible to regular users of the site. False will hide the content without needing to delete it.', verbose_name=b'Published?')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name=b'Created on', blank=True)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name=b'Last edited on', blank=True)),
                ('club', models.ForeignKey(blank=True, to='clubdata.Club', help_text=b'Note: deleting a club will also delete any content associated with it. To avoid that, leave this field blank.', null=True, verbose_name=b'Club which owns the content')),
                ('created_by_user', models.ForeignKey(related_name='content_created', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, help_text=b'Note: deleting a user will simply mark this field as Null on associated content, rather than deleting the content.', null=True, verbose_name=b'Created by')),
                ('edited_by_user', models.ForeignKey(related_name='content_edited', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, help_text=b'Note: deleting a user will simply mark this field as Null on associated content, rather than deleting the content.', null=True, verbose_name=b'Last edited by')),
            ],
        ),
    ]
