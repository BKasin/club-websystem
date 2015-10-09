# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0004_auto_20151005_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='username',
            field=models.CharField(error_messages={b'unique': b'Another member with that username already exists.'}, max_length=50, validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$')], help_text=b'Letters, digits or the following symbols only: <span style="font-size:1.2em">@.+-_</span>', unique=True, verbose_name=b'User name'),
        ),
    ]
