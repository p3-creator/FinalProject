# Generated by Django 4.0.5 on 2022-09-07 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medservices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
