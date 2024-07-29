# Generated by Django 4.2.13 on 2024-07-04 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('badges', '0001_initial'),
        ('credentials', '0030_alter_usercredential_credential_content_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenBadge',
            fields=[
                ('usercredential_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='credentials.usercredential')),
                ('expires_at', models.DateField(null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
            bases=('credentials.usercredential',),
        ),
        migrations.CreateModel(
            name='OpenBadgeTemplate',
            fields=[
                ('badgetemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='badges.badgetemplate')),
            ],
            options={
                'abstract': False,
            },
            bases=('badges.badgetemplate',),
        ),
    ]
