# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
import django.db.models.deletion
import django.core.validators
import contentblocks.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('contentblocks', '0003_auto_20151012_0146'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='block',
            managers=[
                ('objects', contentblocks.models.CustomBlockManager()),
            ],
        ),
        migrations.AddField(
            model_name='block',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sites.Site', help_text=b'Note: deleting a site will also delete any content associated with it. To avoid that, leave this field blank.', null=True, verbose_name=b'Site'),
        ),
        migrations.AlterField(
            model_name='block',
            name='uniquetitle',
            field=models.CharField(help_text=b'Use only letters, numbers, underscores or hyphens. This is used internally to lookup this piece of content, so use something short and logical, and use a prefix that can be filtered on later (competition_ccdc, project_securitysystem, etc.)', max_length=20, verbose_name=b'Unique title', validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')]),
        ),
        migrations.AlterUniqueTogether(
            name='block',
            unique_together=set([('site', 'uniquetitle')]),
        ),
        migrations.RemoveField(
            model_name='block',
            name='club',
        ),
    ]
