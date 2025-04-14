from rest_framework import serializers
from .models import AdmRekamMedisPasien

class AdmRekamMedisPasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmRekamMedisPasien
        fields = '__all__'
        read_only_fields = ['user']