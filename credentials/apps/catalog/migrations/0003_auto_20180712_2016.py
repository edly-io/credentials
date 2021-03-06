# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-12 20:16


from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('catalog', '0002_program_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditPathway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('org_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('programs', sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='pathways', to='catalog.Program')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='creditpathway',
            unique_together=set([('site', 'name')]),
        ),
    ]
