# Generated by Django 1.11.15 on 2019-05-03 12:41


from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0010_auto_20180828_1336'),
        ('records', '0016_auto_20180822_1655'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='programcertrecord',
            unique_together={('program', 'user')},
        ),
    ]