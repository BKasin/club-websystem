# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clubmembers', '0007_auto_20150920_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='name_long',
            field=models.CharField(max_length=120, verbose_name=b'Name (long version)'),
        ),
        migrations.AlterField(
            model_name='club',
            name='name_short',
            field=models.CharField(max_length=20, verbose_name=b'Name (short version)'),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_concentration',
            field=models.CharField(help_text=b'List your academic concentration, if any (Cybersecurity, etc.)', max_length=50, verbose_name=b'Concentration', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_grad_qtr',
            field=models.CharField(help_text=b'Specify your graduation quarter (Spring 2015, Fall 2016, etc.)', max_length=20, verbose_name=b'Graduation quarter', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_major',
            field=models.CharField(help_text=b'List your academic major (Business Administration, Computer Science, etc.)', max_length=50, verbose_name=b'Major', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='acad_minor',
            field=models.CharField(help_text=b'List your academic minor, if any (Business Administration, Computer Science, etc.)', max_length=50, verbose_name=b'Minor', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=254, verbose_name=b'Email address', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='name_first',
            field=models.CharField(max_length=30, verbose_name=b'First name'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name_last',
            field=models.CharField(max_length=30, verbose_name=b'Last name'),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=10, verbose_name=b'Phone number', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='photo',
            field=versatileimagefield.fields.VersatileImageField(height_field=b'photoheight', width_field=b'photowidth', upload_to=b'memberphotos', blank=True, help_text=b'Upload a photo of yourself (no more than 5MB).', null=True, verbose_name=b'Profile photo'),
        ),
        migrations.AlterField(
            model_name='member',
            name='pin_hash',
            field=models.CharField(help_text=b'This is optional, but will be used for less critical sign-in purposes, such as checking into a project meeting or confirming your lab hours.', max_length=120, verbose_name=b'PIN', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='shirt_size',
            field=models.CharField(help_text=b'Please use an abbreviation here (XS, S, M, L, XL, XXL, etc.).', max_length=5, verbose_name=b'Preferred shirt size', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='texting_ok',
            field=models.BooleanField(default=True, verbose_name=b'May the club send SMS messages to this number?'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, help_text=b"This provides a link to Django's built-in user model, which handles attributes such as username, password, permissions, staff status, etc.", verbose_name=b'Associated user'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='badge_issue_date',
            field=models.DateField(null=True, verbose_name=b'Badge issued on', blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='badge_type',
            field=models.CharField(max_length=20, verbose_name=b'Type of badge issued', blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='club',
            field=models.ForeignKey(verbose_name=b'is a member of', to='clubmembers.Club'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(verbose_name=b'Member', to='clubmembers.Member'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_amount',
            field=models.DecimalField(null=True, verbose_name=b'Paid amount', max_digits=6, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_date',
            field=models.DateField(null=True, verbose_name=b'Paid on', blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='paid_until_date',
            field=models.DateField(null=True, verbose_name=b'Payment is valid until', blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='receipt_date',
            field=models.DateField(null=True, verbose_name=b'Receipt sent to member on', blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='shirt_received_date',
            field=models.DateField(null=True, verbose_name=b'Shirt received on', blank=True),
        ),
    ]
