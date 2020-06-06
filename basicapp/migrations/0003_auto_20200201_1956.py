# Generated by Django 2.2.9 on 2020-02-02 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicapp', '0002_patient_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='DICOM_FILE',
        ),
        migrations.AddField(
            model_name='patient',
            name='MASK_DICOM',
            field=models.FileField(default='', upload_to='DICOM/'),
        ),
        migrations.AddField(
            model_name='patient',
            name='PATIENT_DICOM',
            field=models.FileField(default='', upload_to='DICOM/'),
        ),
    ]