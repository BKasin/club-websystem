# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentblocks', '0004_auto_20151013_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='auth_required',
            field=models.BooleanField(default=False, help_text=b'If true, user must be logged in to view this block.', verbose_name=b'Login required?'),
        ),
    ]
