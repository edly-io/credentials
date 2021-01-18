# Generated by Django 2.2.13 on 2021-01-18 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0015_auto_20180822_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercredential',
            name='credential_content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('coursecertificate', 'programcertificate')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
