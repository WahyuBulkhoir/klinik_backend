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
        # Mengambil semua meeting requests yang terkait dengan pasien yang sedang login
        meeting_requests = MeetingRequest.objects.filter(pasien=user)

        # Periksa apakah ada query parameter id untuk memfilter data berdasarkan id
        meeting_id = request.query_params.get('id')
        if meeting_id:
            meeting_requests = meeting_requests.filter(id=meeting_id)

        # Serialisasi data untuk dikirimkan ke frontend
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
    # Periksa apakah user sudah memiliki rekam medis
    existing_rekam_medis = AdmRekamMedisPasien.objects.filter(user=request.user).first()
    if existing_rekam_medis:
        return Response({'detail': 'Anda sudah mengisi rekam medis.'}, status=400)

    serializer = AdmRekamMedisPasienSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'detail': 'Rekam medis berhasil disimpan.'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_rekam_medis_view(request):
    # Periksa apakah user sudah memiliki rekam medis
    has_rekam_medis = AdmRekamMedisPasien.objects.filter(user=request.user).exists()
    return Response({'has_rekam_medis': has_rekam_medis})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_meeting_requests_for_pasien_view(request):
    user = request.user

    if user.role != 'patient':
        return Response({'error': 'Unauthorized'}, status=403)

    meeting_requests = MeetingRequest.objects.filter(pasien=user).order_by('-created_at')
    serializer = MeetingRequestSerializer(meeting_requests, many=True)
    return Response({'success': True, 'data': serializer.data}, status=200)
