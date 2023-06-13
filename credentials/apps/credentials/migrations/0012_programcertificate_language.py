# Generated by Django 1.11.3 on 2017-10-24 19:28


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0011_programcertificate_include_hours_of_effort'),
    ]

    operations = [
        migrations.AddField(
            model_name='programcertificate',
            name='language',
            field=models.CharField(help_text='Language in which certificates for this program will be rendered', max_length=8, null=True),
        ),
    ]
