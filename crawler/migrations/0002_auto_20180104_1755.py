# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-04 08:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site_name',
            old_name='title',
            new_name='titles',
        ),
    ]
