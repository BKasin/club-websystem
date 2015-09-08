# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0007_remove_membership_signup_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='phone2',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
