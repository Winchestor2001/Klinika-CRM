# Generated by Django 4.1.6 on 2023-02-15 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_patient_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='days',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
