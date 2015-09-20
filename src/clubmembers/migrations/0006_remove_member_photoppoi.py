# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0005_auto_20150916_0119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='photoppoi',
        ),
    ]
