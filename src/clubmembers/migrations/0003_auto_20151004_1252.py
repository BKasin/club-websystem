# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0002_auto_20151004_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='coyote_id',
            field=models.CharField(blank=True, help_text=b'Provide the 9-digit CSUSB student identification number. Leave blank if member is not yet or no longer a student.', max_length=9, verbose_name=b'Coyote ID #', validators=[django.core.validators.RegexValidator(b'^[\\d]+$')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='email_pending',
            field=models.EmailField(help_text=b'This field is only to be used for an email that has not yet been verified by the user. Once verified, the <i>email</i> field is updated and this one is cleared.', max_length=254, verbose_name=b'Pending email address', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(help_text=b'Please enter your phone number in the following format: 000-000-0000', max_length=100, verbose_name=b'Phone number', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='username',
            field=models.CharField(error_messages={b'unique': b'Another InfoSec Club member with that username already exists.'}, max_length=50, validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$')], help_text=b'Letters, digits or the following symbols only: <span style="font-size:1.2em">@.+-_</span>', unique=True, verbose_name=b'User name'),
        ),
    ]
