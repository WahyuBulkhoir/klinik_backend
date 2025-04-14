from django.urls import path
from .views import doctor_schedule_view, doctor_schedule_by_id_view, list_doctors, doctor_detail, doctor_profile_setting, create_meeting_request_view, list_meeting_requests_for_dokter_view, meeting_request_detail_view, update_status_meeting_satus_view


urlpatterns = [
    path('doctor-schedule/', doctor_schedule_view, name='doctor_schedule'),
    path('doctor-schedule/<int:doctor_id>/', doctor_schedule_by_id_view, name='doctor_schedule_by_id'),
    path('doctors/', list_doctors, name='list_doctors'),
    path('doctors/<int:doctor_id>/', doctor_detail, name='doctor_detail'),
    path('doctor/settings/', doctor_profile_setting, name='doctor-settings'),
    path('meeting-request/', create_meeting_request_view, name='create-meeting-request'),
    path('meeting-request/list-dokter/', list_meeting_requests_for_dokter_view, name='list-meeting-request-for-dokter'),
    path('meeting-request/list-dokter/<int:pk>/', meeting_request_detail_view, name='meeting-request-detail'),
    path('meeting-request/update-status/', update_status_meeting_satus_view, name='update_meeting_status'),
]
