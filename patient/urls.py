from django.urls import path
from . import views

urlpatterns = [
    path('rekam-medis/', views.rekam_medis_view, name='rekam_medis'),
    path('check-rekam-medis/', views.check_rekam_medis_view, name='check_rekam_medis'),
    path('request/patient/', views.list_meeting_requests_for_patient_view, name='meeting_request_patient_list'),
]