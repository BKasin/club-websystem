# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import versatileimagefield.fields


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
                ('phone', models.CharField(max_length=10, blank=True)),
                ('texting_ok', models.BooleanField()),
                ('photo', versatileimagefield.fields.VersatileImageField(default=b'', upload_to=b'memberphotos', width_field=b'photowidth', height_field=b'photoheight', blank=True)),
                ('photowidth', models.PositiveIntegerField(null=True, editable=False)),
                ('photoheight', models.PositiveIntegerField(null=True, editable=False)),
                ('photoppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', max_length=20, editable=False, blank=True)),
                ('pin_hash', models.CharField(max_length=120, blank=True)),
                ('shirt_size', models.CharField(max_length=2, blank=True)),
                ('acad_major', models.CharField(max_length=50, blank=True)),
                ('acad_minor', models.CharField(max_length=50, blank=True)),
                ('acad_concentration', models.CharField(max_length=50, blank=True)),
                ('acad_grad_qtr', models.CharField(max_length=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('paid_date', models.DateField(null=True)),
                ('paid_until_date', models.DateField(null=True)),
                ('paid_amount', models.DecimalField(null=True, max_digits=6, decimal_places=2)),
                ('receipt_date', models.DateField(null=True)),
                ('badge_type', models.CharField(max_length=20, null=True)),
                ('badge_issue_date', models.DateField(null=True)),
                ('shirt_received_date', models.DateField(null=True)),
                ('club', models.ForeignKey(to='clubmembers.Club')),
                ('member', models.ForeignKey(to='clubmembers.Member')),
            ],
        ),
    ]
