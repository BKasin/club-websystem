# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0006_remove_member_photoppoi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='texting_ok',
            field=models.BooleanField(default=False),
        ),
    ]
