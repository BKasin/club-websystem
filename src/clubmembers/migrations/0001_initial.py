# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name_short', models.CharField(max_length=20)),
                ('name_long', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('pin_hash', models.CharField(max_length=120)),
                ('name_first', models.CharField(max_length=120)),
                ('name_last', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=10)),
                ('texting_ok', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.CharField(max_length=1)),
                ('shirt_size', models.CharField(max_length=2)),
                ('acad_major', models.CharField(max_length=20)),
                ('acad_minor', models.CharField(max_length=20)),
                ('acad_concentration', models.CharField(max_length=20)),
                ('acad_grad_qtr', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('priv_level', models.SmallIntegerField()),
                ('signup_date', models.DateField(auto_now_add=True)),
                ('paid_date', models.DateField(auto_now_add=True)),
                ('paid_amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('paid_until_date', models.DateField(auto_now_add=True)),
                ('receipt_date', models.DateField(auto_now_add=True)),
                ('badge_type', models.CharField(max_length=5)),
                ('badge_issue_date', models.DateField(auto_now_add=True)),
                ('shirt_received_date', models.DateField(auto_now_add=True)),
                ('club', models.ForeignKey(to='clubmembers.Club')),
                ('member', models.ForeignKey(to='clubmembers.Member')),
            ],
        ),
    ]
