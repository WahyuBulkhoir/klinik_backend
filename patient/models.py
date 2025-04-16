from django.db import models
from django.conf import settings

class AdmRekamMedisPasien(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rekam_medis'
    )
    nama_lengkap = models.CharField(max_length=100)
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10, choices=[('laki-laki', 'Laki-laki'), ('perempuan', 'Perempuan')])
    golongan_darah = models.CharField(max_length=2, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], blank=True, null=True)
    no_hp = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    jenis_kepesertaan = models.CharField(
        max_length=30,
        choices=[
            ('kis', 'Kartu Indonesia Sehat (KIS)'),
            ('jamkesda', 'Jaminan Kesehatan Daerah (Jamkesda)'),
            ('jknbpjs', 'JKN - BPJS Kesehatan'),
            ('bpjsket', 'BPJS Ketenagakerjaan'),
        ],
        blank=True,
        null=True
    )
    nomor_kartu = models.CharField(max_length=50, blank=True, null=True)
    nama_kontak_darurat = models.CharField(max_length=100, blank=True, null=True)
    hubungan_kontak = models.CharField(
        max_length=20,
        choices=[
            ('suami', 'Suami'),
            ('istri', 'Istri'),
            ('ayah', 'Ayah'),
            ('ibu', 'Ibu'),
            ('etc', 'Lainnya')
        ],
        blank=True,
        null=True
    )
    no_hp_kontak = models.CharField(max_length=20, blank=True, null=True)
    riwayat_penyakit = models.TextField(blank=True, null=True)
    alergi_obat_makanan = models.TextField(blank=True, null=True)
    riwayat_operasi = models.TextField(blank=True, null=True)
    riwayat_pengobatan = models.TextField(blank=True, null=True)
    merokok = models.CharField(max_length=10, choices=[("Iya", "Iya"), ("Tidak", "Tidak")])
    konsumsi_alkohol = models.CharField(max_length=10, choices=[("Iya", "Iya"), ("Tidak", "Tidak")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama_lengkap} - {self.tanggal_lahir}"