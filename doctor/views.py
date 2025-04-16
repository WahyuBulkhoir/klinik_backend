from datetime import datetime
import logging
logger = logging.getLogger(__name__)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import JadwalDokter, MeetingRequest
from .serializers import JadwalDokterSerializer, DoctorProfileUpdateSerializer, MeetingRequestSerializer, MeetingRequestDetailSerializer
from patient.models import AdmRekamMedisPasien
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core import serializers

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meeting_request_detail_view(request, pk):
    try:
        meeting_request = MeetingRequest.objects.get(pk=pk)
        print("USER YANG AKSES:", request.user.id)
        print("DOKTER DARI REQUEST:", meeting_request.dokter.id)

        if request.user != meeting_request.dokter:
            return Response({'detail': 'Unauthorized'}, status=403)

        serializer = MeetingRequestDetailSerializer(meeting_request)
        return Response(serializer.data, status=200)

    except MeetingRequest.DoesNotExist:
        return Response({'detail': 'MeetingRequest not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_meeting_requests_for_dokter_view(request):
    user = request.user

    if user.role != 'doctor':
        return Response({'error': 'You are not authorized to access this data.'}, status=403)

    try:
        doctor = user
        meeting_requests = MeetingRequest.objects.filter(dokter=doctor)
        meeting_id = request.query_params.get('id')
        if meeting_id:
            meeting_requests = meeting_requests.filter(id=meeting_id)

        serializer = MeetingRequestSerializer(meeting_requests, many=True)
        return Response({'success': True, 'data': serializer.data}, status=200)

    except Exception as e:
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching meeting request: {str(e)}")
        traceback.print_exc()

        return Response({'success': False, 'error': 'Terjadi kesalahan internal'}, status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_status_meeting_satus_view(request):
    user = request.user
    if user.role != 'doctor':
        return Response({'error': 'Unauthorized'}, status=403)
    meeting_id = request.data.get('meeting_id')
    status = request.data.get('status')

    if status not in ['approved', 'rejected']:
        return Response({'error': 'Invalid status'}, status=400)

    try:
        meeting = MeetingRequest.objects.get(id=meeting_id)
        meeting.status = status
        meeting.save()

        return Response({'message': 'Status updated successfully'})

    except MeetingRequest.DoesNotExist:
        return Response({'error': 'Meeting request not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_meeting_request_view(request):
    user = request.user
    data = request.data
    required_fields = ['dokter', 'jadwal']
    for field in required_fields:
        if field not in data:
            return Response(
                {'success': False, 'error': f'Field {field} harus diisi'},
                status=status.HTTP_400_BAD_REQUEST
            )

    try:
        try:
            rekam_medis = AdmRekamMedisPasien.objects.get(user=user)
        except AdmRekamMedisPasien.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Rekam medis belum diisi'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            dokter = User.objects.get(id=data['dokter'], role='doctor')
        except User.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Dokter tidak ditemukan'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            jadwal = JadwalDokter.objects.get(id=data['jadwal'], dokter=dokter)
        except JadwalDokter.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Jadwal tidak valid'},
                status=status.HTTP_404_NOT_FOUND
            )

        if MeetingRequest.objects.filter(jadwal=jadwal, dokter=dokter).exists():
            return Response(
                {'success': False, 'error': 'Jadwal sudah digunakan'},
                status=status.HTTP_409_CONFLICT
            )

        meeting_request = MeetingRequest.objects.create(
            pasien=user,
            dokter=dokter,
            jadwal=jadwal,
            rekam_medis=rekam_medis,
            status='pending'
        )

        serializer = MeetingRequestSerializer(meeting_request)
        return Response(
            {
                'success': True,
                'message': 'Permintaan pertemuan berhasil dibuat',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        import traceback
        logger.error(f"Error creating meeting request: {str(e)}")
        traceback.print_exc()

    return Response(
        {'success': False, 'error': 'Terjadi kesalahan internal'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def doctor_profile_setting(request):
    user = request.user

    if user.role != 'doctor':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = DoctorProfileUpdateSerializer(user)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DoctorProfileUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profil dokter berhasil diperbarui'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)@api_view(['GET', 'POST'])

@api_view(['GET'])
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(User, id=doctor_id, role='doctor')
    data = {
        "id": doctor.id,
        "name": doctor.get_full_name() or doctor.username,
        "email": doctor.email,
        "skills": doctor.skills or [],
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_doctors(request):
    doctors = User.objects.filter(role='doctor')
    data = [
        {
            "id": doctor.id,
            "name": doctor.get_full_name() or doctor.username,
            "email": doctor.email,
            "slogan": doctor.slogan,
            "specialty": doctor.specialty,
        }
        for doctor in doctors
    ]
    return Response(data)

@api_view(['GET'])
def doctor_schedule_by_id_view(request, doctor_id):
    doctor = get_object_or_404(User, id=doctor_id)
    jadwal = JadwalDokter.objects.filter(dokter=doctor)
    serializer = JadwalDokterSerializer(jadwal, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def doctor_schedule_view(request):
    if request.method == 'GET':
        jadwal = JadwalDokter.objects.filter(dokter=request.user)
        serializer = JadwalDokterSerializer(jadwal, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        schedules = request.data.get("schedules", {})
        if not schedules:
            return Response({"error": "Schedules data is required"}, status=status.HTTP_400_BAD_REQUEST)

        JadwalDokter.objects.filter(dokter=request.user).delete()

        created = []
        for hari, detail in schedules.items():
            tanggal_str = detail.get("date")
            time_range = detail.get("timeRange", "")
            times = detail.get("times", [])

            if not tanggal_str:
                continue

            try:
                tanggal = datetime.strptime(tanggal_str, "%Y-%m-%d").date()
            except ValueError:
                continue

            for jam in times:
                serializer = JadwalDokterSerializer(data={
                    "hari": hari,
                    "tanggal": tanggal,
                    "jam_mulai": jam,
                    "jam_selesai": jam,
                    "time_range_label": time_range
                })

                if serializer.is_valid():
                    serializer.save(dokter=request.user)
                    created.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True, "created": created}, status=status.HTTP_201_CREATED)