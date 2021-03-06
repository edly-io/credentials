# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-11 18:09


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('credentials', '0013_auto_20180611_1809'),
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramCertRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credentials.ProgramCertificate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'A viewable record of a program certificate',
            },
        ),
        migrations.AlterUniqueTogether(
            name='programcertrecord',
            unique_together=set([('certificate', 'user')]),
        ),
    ]
