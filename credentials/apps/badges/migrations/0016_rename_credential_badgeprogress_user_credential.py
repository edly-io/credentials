# Generated by Django 3.2.20 on 2024-04-16 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0015_credlybadge_external_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='badgeprogress',
            old_name='credential',
            new_name='user_credential',
        ),
    ]