# Generated by Django 4.1.1 on 2022-09-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medservices', '0006_appointment_timseslots_booked_appointments_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality', models.CharField(max_length=100)),
                ('doctor', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('payment_completed', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
    ]
