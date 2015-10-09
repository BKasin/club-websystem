# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0004_auto_20151005_2344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='date_created',
            new_name='date_joined',
        ),
        migrations.AlterField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name=b'Account activated?'),
        ),
    ]
