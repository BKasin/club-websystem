# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0003_auto_20151004_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='paid_date',
            field=models.DateField(default=datetime.datetime(2015, 1, 1, 0, 0), verbose_name=b'Paid on'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_until_date',
            field=models.DateField(default=datetime.datetime(2015, 1, 2, 0, 0), verbose_name=b'Payment is valid until'),
            preserve_default=False,
        ),
    ]
