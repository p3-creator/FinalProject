# Generated by Django 4.0.5 on 2022-09-10 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medservices', '0003_appointment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Appointment',
        ),
        migrations.RenameField(
            model_name='doctor',
            old_name='speciality',
            new_name='specialities',
        ),
    ]
