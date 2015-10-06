# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubdata', '0002_club_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='logo',
            field=models.CharField(help_text=b'Relative path to the small logo, to used on the users profile. Should not begin with a slash. Ex: img/clublogo-club1-sm.png', max_length=100, verbose_name=b'Logo of the club', blank=True),
        ),
    ]
