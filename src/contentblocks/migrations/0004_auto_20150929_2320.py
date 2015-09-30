# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contentblocks', '0003_auto_20150916_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='blob',
            field=models.TextField(help_text=b'This is the actual block of content. Specify the format above.', verbose_name=b'Content block'),
        ),
        migrations.AlterField(
            model_name='block',
            name='club',
            field=models.ForeignKey(blank=True, to='clubmembers.Club', help_text=b'Note: deleting a club will also delete any content associated with it. To avoid that, leave this field blank.', null=True, verbose_name=b'Club which owns the content'),
        ),
        migrations.AlterField(
            model_name='block',
            name='created_by_user',
            field=models.ForeignKey(related_name='content_created', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='clubmembers.Member', help_text=b'Note: deleting a user will simply mark this field as Null on associated content, rather than deleting the content.', null=True, verbose_name=b'Created by'),
        ),
        migrations.AlterField(
            model_name='block',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name=b'Created on', blank=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='datatype',
            field=models.CharField(help_text=b'This tells the website how to process and render the content for the user.', max_length=3, verbose_name=b'Type of content', choices=[(b'md', b'CommonMark'), (b'htm', b'HTML'), (b'txt', b'Raw Text')]),
        ),
        migrations.AlterField(
            model_name='block',
            name='description',
            field=models.CharField(help_text=b'Longer description, if any.', max_length=100, verbose_name=b'Description', blank=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='edited_by_user',
            field=models.ForeignKey(related_name='content_edited', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='clubmembers.Member', help_text=b'Note: deleting a user will simply mark this field as Null on associated content, rather than deleting the content.', null=True, verbose_name=b'Last edited by'),
        ),
        migrations.AlterField(
            model_name='block',
            name='edited_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name=b'Last edited on', blank=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='published',
            field=models.BooleanField(help_text=b'If true, this content will be visible to regular users of the site. False will hide the content without needing to delete it.', verbose_name=b'Published?'),
        ),
        migrations.AlterField(
            model_name='block',
            name='uniquetitle',
            field=models.CharField(help_text=b'This is used internally to lookup this piece of content, so use something short and logical, and use a prefix that can be filtered on later (competition_ccdc, project_securitysystem, etc.)', unique=True, max_length=20, verbose_name=b'Unique title'),
        ),
    ]
