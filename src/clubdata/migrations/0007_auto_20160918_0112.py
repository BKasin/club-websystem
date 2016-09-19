# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import system.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clubdata', '0006_auto_20151012_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='site',
            field=system.fields.OneToOneFieldWithFlag(to='sites.Site', flag_name=b'has_club'),
        ),
    ]
