from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from patient.models import AdmRekamMedisPasien

User = get_user_model()

class JadwalDokter(models.Model):
    dokter = models.ForeignKey(User, on_delete=models.CASCADE)
    hari = models.CharField(max_length=20)
    tanggal = models.DateField()
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    time_range_label = models.CharField(max_length=50, blank=True)  
    
    def __str__(self):
        return f"{self.dokter} - {self.hari} - {self.jam_mulai}"
    
class MeetingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    pasien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meeting_requests'
    )
    dokter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_for_doctor')
    jadwal = models.ForeignKey(JadwalDokter, on_delete=models.CASCADE, related_name='meeting_requests_patient')
    rekam_medis = models.ForeignKey(AdmRekamMedisPasien, on_delete=models.CASCADE, related_name='meeting_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dokter.get_full_name() or self.dokter.username} → ({self.jadwal.hari}, {self.jadwal.tanggal} {self.jadwal.jam_mulai})"

