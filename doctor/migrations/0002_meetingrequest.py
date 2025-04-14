# Generated by Django 5.1.7 on 2025-04-10 07:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
        ('patient', '0004_admrekammedispasien_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dokter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_for_doctor', to=settings.AUTH_USER_MODEL)),
                ('pasien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting_requests', to=settings.AUTH_USER_MODEL)),
                ('rekam_medis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting_requests', to='patient.admrekammedispasien')),
            ],
        ),
    ]
