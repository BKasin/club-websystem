# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0008_member_phone2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='phone2',
        ),
    ]
