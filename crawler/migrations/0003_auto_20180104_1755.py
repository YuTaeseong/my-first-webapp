# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-04 08:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20180104_1755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site_name',
            old_name='titles',
            new_name='title',
        ),
    ]
