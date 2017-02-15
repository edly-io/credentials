# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-17 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0007_auto_20170118_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programcertificate',
            name='program_uuid',
            field=models.UUIDField(db_index=True, unique=True, verbose_name='Program UUID'),
        ),
    ]
