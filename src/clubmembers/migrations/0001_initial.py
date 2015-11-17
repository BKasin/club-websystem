# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import versatileimagefield.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('clubdata', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'Account activated?')),
                ('is_staff', models.BooleanField(default=False, verbose_name=b'May login to /admin?')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date created', editable=False)),
                ('username', models.CharField(error_messages={b'unique': b'Another InfoSec Club member with that username already exists.'}, max_length=50, validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$', b'Enter a valid username.', b'invalid')], help_text=b'Letters, digits or the following symbols only: <span style="font-size:1.2em">@.+-_</span>', unique=True, verbose_name=b'User name')),
                ('coyote_id', models.CharField(help_text=b'Provide the 9-digit CSUSB student identification number. Leave blank if member is not yet or no longer a student.', max_length=9, verbose_name=b'Coyote ID #', blank=True)),
                ('name_first', models.CharField(max_length=30, verbose_name=b'First name')),
                ('name_last', models.CharField(max_length=30, verbose_name=b'Last name')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name=b'Email address')),
                ('email_pending', models.EmailField(max_length=254, verbose_name=b'New email address (pending verification)', blank=True)),
                ('phone', models.CharField(max_length=20, verbose_name=b'Phone number', blank=True)),
                ('texting_ok', models.BooleanField(default=True, help_text=b'May the club send SMS messages to this number? Your usual SMS charges will still apply.', verbose_name=b'SMS Okay?')),
                ('photo', versatileimagefield.fields.VersatileImageField(height_field=b'photoheight', width_field=b'photowidth', upload_to=b'memberphotos', blank=True, help_text=b'Upload a photo of yourself (no more than 5MB).', null=True, verbose_name=b'Profile photo')),
                ('photowidth', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('photoheight', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('pin_hash', models.CharField(help_text=b'This is optional, but will be used for less critical sign-in purposes, such as checking into a project meeting or confirming your lab hours.', max_length=120, verbose_name=b'PIN', blank=True)),
                ('shirt_size', models.CharField(help_text=b'Please use an abbreviation here (XS, S, M, L, XL, XXL, etc.).', max_length=5, verbose_name=b'Preferred shirt size', blank=True)),
                ('acad_major', models.CharField(help_text=b'List your academic major (Business Administration, Computer Science, etc.)', max_length=50, verbose_name=b'Major', blank=True)),
                ('acad_minor', models.CharField(help_text=b'List your academic minor, if any (Business Administration, Computer Science, etc.)', max_length=50, verbose_name=b'Minor', blank=True)),
                ('acad_concentration', models.CharField(help_text=b'List your academic concentration, if any (Cybersecurity, etc.)', max_length=50, verbose_name=b'Concentration', blank=True)),
                ('acad_grad_qtr', models.CharField(help_text=b'Specify your graduation quarter (Spring 2015, Fall 2016, etc.)', max_length=20, verbose_name=b'Graduation quarter', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('paid_date', models.DateField(null=True, verbose_name=b'Paid on', blank=True)),
                ('paid_until_date', models.DateField(null=True, verbose_name=b'Payment is valid until', blank=True)),
                ('paid_amount', models.DecimalField(null=True, verbose_name=b'Paid amount', max_digits=6, decimal_places=2, blank=True)),
                ('receipt_date', models.DateField(null=True, verbose_name=b'Receipt sent to member on', blank=True)),
                ('badge_issue_date', models.DateField(null=True, verbose_name=b'Badge issued on', blank=True)),
                ('badge_type', models.CharField(max_length=20, verbose_name=b'Type of badge issued', blank=True)),
                ('shirt_received_date', models.DateField(null=True, verbose_name=b'Shirt received on', blank=True)),
                ('club', models.ForeignKey(verbose_name=b'Is a member of', to='clubdata.Club')),
                ('member', models.ForeignKey(verbose_name=b'Member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
