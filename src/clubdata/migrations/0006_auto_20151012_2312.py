# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

# This is a special migration. After applying migration 'clubdata.0005_club_site', you must
# manually modify each club to point to a site. Then run this migration.

class Migration(migrations.Migration):

    dependencies = [
        ('clubdata', '0005_club_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='site',
            field=models.OneToOneField(to='sites.Site'),
        ),
    ]
