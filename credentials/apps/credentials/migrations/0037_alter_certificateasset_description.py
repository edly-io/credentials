from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0036_programcertificatetemplate_unique_active_template_per_program_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificateasset',
            name='description',
            field=models.CharField(
                max_length=255,
                help_text="Human-readable description of this asset (e.g. 'FBR Pakistan org logo – PNG 200×200').",
            ),
        ),
    ]
