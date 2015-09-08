# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0006_auto_20150907_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='signup_date',
        ),
    ]
