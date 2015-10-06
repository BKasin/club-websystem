# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubdata', '0003_auto_20151006_1641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='logo',
            new_name='logo_small',
        ),
    ]
