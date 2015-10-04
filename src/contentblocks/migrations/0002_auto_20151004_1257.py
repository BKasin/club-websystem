# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contentblocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='uniquetitle',
            field=models.CharField(help_text=b'Use only letters, numbers, underscores or hyphens. This is used internally to lookup this piece of content, so use something short and logical, and use a prefix that can be filtered on later (competition_ccdc, project_securitysystem, etc.)', unique=True, max_length=20, verbose_name=b'Unique title', validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')]),
        ),
    ]
