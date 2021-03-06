# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-10 20:07


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('catalog', '0003_auto_20180712_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditpathway',
            name='uuid',
            field=models.UUIDField(null=True, verbose_name='UUID'),
        ),
        migrations.AlterUniqueTogether(
            name='creditpathway',
            unique_together=set([('site', 'name', 'uuid')]),
        ),
    ]
