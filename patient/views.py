import stat
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from doctor.models import MeetingRequest 
from doctor.serializers import MeetingRequestSerializer
from .models import AdmRekamMedisPasien
from .serializers import AdmRekamMedisPasienSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_meeting_requests_for_patient_view(request):
    user = request.user

    if user.role != 'patient':
        return Response({'error': 'You are not authorized to access this data.'}, status=403)

    try:
        meeting_requests = MeetingRequest.objects.filter(pasien=user)
        meeting_id = request.query_params.get('id')
        
        if meeting_id:
            meeting_requests = meeting_requests.filter(id=meeting_id)
        serializer = MeetingRequestSerializer(meeting_requests, many=True)

        return Response({'success': True, 'data': serializer.data}, status=200)

    except Exception as e:
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching meeting request for patient: {str(e)}")
        traceback.print_exc()

        return Response({'success': False, 'error': 'Terjadi kesalahan internal'}, status=500)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rekam_medis_view(request):
    user = request.user
    existing_rekam_medis = AdmRekamMedisPasien.objects.filter(user=user).first()

    if existing_rekam_medis:
        all_requests = MeetingRequest.objects.filter(pasien=user)
        if all_requests.exists():
            all_rejected = all_requests.exclude(status='rejected').count() == 0
            if all_rejected:
                existing_rekam_medis.delete()
            else:
                return Response({'detail': 'Anda sudah mengisi rekam medis dan masih memiliki permintaan yang aktif.'}, status=400)
        else:
            return Response({'detail': 'Anda sudah mengisi rekam medis.'}, status=400)

    serializer = AdmRekamMedisPasienSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response({'detail': 'Rekam medis berhasil disimpan.'}, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_rekam_medis_view(request):
    user = request.user

    if user.role != 'patient':
        
        return Response({'detail': 'User bukan pasien.'}, status=stat.HTTP_403_FORBIDDEN)

    try:
        print("Cek apakah pasien memiliki rekam medis...")
        has_rekam_medis = AdmRekamMedisPasien.objects.filter(user=user).exists()
        print("has_rekam_medis:", has_rekam_medis)
        requests = MeetingRequest.objects.filter(pasien=user)
        print("Jumlah request:", requests.count())
        all_rejected = requests.exists() and all(req.status == 'rejected' for req in requests)
        print("Semua request ditolak:", all_rejected)

        if has_rekam_medis and all_rejected:
            has_rekam_medis = False

        return Response({'has_rekam_medis': has_rekam_medis})
    
    except Exception as e:
        print("Terjadi error saat check_rekam_medis_view:", str(e))
        return Response({'has_rekam_medis': False, 'error': str(e)}, status=500)