# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0007_pendingemailchange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='coyote_id',
            field=models.CharField(blank=True, help_text=b'Provide the 9-digit CSUSB student identification number. Leave blank if you do not yet have (or no longer have) a student ID number.', max_length=9, verbose_name=b'Coyote ID #', validators=[django.core.validators.RegexValidator(b'^[\\d]{9}$')]),
        ),
    ]
