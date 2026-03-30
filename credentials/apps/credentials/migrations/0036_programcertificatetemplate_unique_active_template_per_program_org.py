from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0035_remove_programcertificatetemplate_program_type'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='programcertificatetemplate',
            constraint=models.UniqueConstraint(
                condition=models.Q(is_active=True),
                fields=['program_certificate', 'organization'],
                nulls_distinct=False,
                name='unique_active_template_per_program_org',
            ),
        ),
    ]
