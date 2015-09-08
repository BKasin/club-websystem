# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0002_auto_20150907_0637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='name_first',
        ),
        migrations.RemoveField(
            model_name='member',
            name='name_last',
        ),
    ]
