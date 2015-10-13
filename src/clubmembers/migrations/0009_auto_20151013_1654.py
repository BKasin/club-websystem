# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import clubmembers.models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0008_auto_20151012_1907'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='membership',
            managers=[
                ('objects', clubmembers.models.CustomMembershipManager()),
            ],
        ),
    ]
