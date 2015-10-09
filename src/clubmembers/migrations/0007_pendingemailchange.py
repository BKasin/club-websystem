# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0006_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingEmailChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('confirmation_key', models.CharField(max_length=40, verbose_name=b'Confirmation key')),
                ('date_initiated', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date of email change request')),
                ('member', models.ForeignKey(verbose_name=b'Member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
