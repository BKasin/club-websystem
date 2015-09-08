# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0003_auto_20150907_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='member',
            name='email',
        ),
    ]
