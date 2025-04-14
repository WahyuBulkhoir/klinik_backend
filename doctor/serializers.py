from rest_framework import serializers
from .models import JadwalDokter, MeetingRequest
from django.contrib.auth import get_user_model
from patient.serializers import AdmRekamMedisPasienSerializer
from patient.models import AdmRekamMedisPasien

User = get_user_model()

class JadwalDokterSerializer(serializers.ModelSerializer):
    class Meta:
        model = JadwalDokter
        fields = '__all__'
        read_only_fields = ['dokter']

class DoctorProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['skills', 'specialty', 'slogan']
        
class MeetingRequestSerializer(serializers.ModelSerializer):
    pasien_username = serializers.CharField(source='pasien.username', read_only=True)
    dokter_nama = serializers.CharField(source='dokter.nama', read_only=True)
    rekam_medis_detail = AdmRekamMedisPasienSerializer(source='rekam_medis', read_only=True)
    jadwal_detail = JadwalDokterSerializer(source='jadwal', read_only=True)

    class Meta:
        model = MeetingRequest
        fields = [
            'id',
            'pasien',
            'pasien_username',
            'dokter',
            'dokter_nama',
            'jadwal',  # foreign key ID
            'jadwal_detail',
            'rekam_medis',
            'rekam_medis_detail',
            'status',
            'created_at',
        ]
        read_only_fields = ['status', 'created_at']
        
class MeetingRequestDetailSerializer(serializers.ModelSerializer):
    rekam_medis_detail = serializers.SerializerMethodField()

    class Meta:
        model = MeetingRequest
        fields = [
            'id', 'pasien', 'dokter', 'jadwal', 'status', 'created_at', 'rekam_medis', 'rekam_medis_detail'
        ]

    def get_rekam_medis_detail(self, obj):
        try:
            rekam_medis = AdmRekamMedisPasien.objects.get(id=obj.rekam_medis.id)
            return AdmRekamMedisPasienSerializer(rekam_medis).data
        except AdmRekamMedisPasien.DoesNotExist:
            return None
