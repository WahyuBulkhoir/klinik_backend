# Generated by Django 5.1.7 on 2025-04-03 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('doctor', 'Doctor'), ('patient', 'Patient')], default='patient', max_length=10),
        ),
    ]
