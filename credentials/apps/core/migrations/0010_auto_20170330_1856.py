# Generated by Django 1.9.12 on 2017-03-30 18:56
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_siteconfiguration_segment_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfiguration',
            name='catalog_api_url',
            field=models.URLField(help_text='Root URL of the Catalog API (e.g. https://api.edx.org/catalog/v1/)', verbose_name='Catalog API URL'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='lms_url_root',
            field=models.URLField(help_text="Root URL of this site's LMS (e.g. https://courses.stage.edx.org)", verbose_name='LMS base url for custom site'),
        ),
    ]
