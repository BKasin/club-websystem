# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentblocks', '0002_auto_20151004_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='datatype',
            field=models.CharField(default=b'md', help_text=b'This tells the website how to process and render the content for the user.', max_length=3, verbose_name=b'Type of content', choices=[(b'md', b'CommonMark'), (b'htm', b'HTML'), (b'txt', b'Raw Text'), (b'jsn', b'JSON')]),
        ),
        migrations.AlterField(
            model_name='block',
            name='published',
            field=models.BooleanField(default=False, help_text=b'If true, this content will be visible to regular users of the site. False will hide the content without needing to delete it.', verbose_name=b'Published?'),
        ),
    ]
