# Generated by Django 1.11.3 on 2017-10-18 21:05


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0010_auto_20170420_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='programcertificate',
            name='include_hours_of_effort',
            field=models.BooleanField(default=False, help_text="Display the estimated total number of hours needed to complete all courses in the program. This feature will only be displayed in the certificate if the attribute 'Total hours of effort' has been set for the program in Discovery."),
        ),
    ]
