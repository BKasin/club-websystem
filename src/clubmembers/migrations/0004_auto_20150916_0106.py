# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0003_auto_20150916_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='name_first',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='member',
            name='name_last',
            field=models.CharField(max_length=30),
        ),
    ]
