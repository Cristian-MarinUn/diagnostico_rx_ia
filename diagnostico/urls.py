from django.urls import path
from . import views

app_name = 'diagnostico'

urlpatterns = [
    # Autocompletado de pacientes (API)
    path('api/autocomplete-patients/', views.autocomplete_patients, name='autocomplete_patients'),
    
    # Obtener paciente por ID (API)
    path('api/patient/<int:patient_id>/', views.get_patient_by_id, name='get_patient_by_id'),
    
    # Seleccionar paciente
    path('request/', views.request_diagnosis_select, name='request_diagnosis_select'),
    
    # Solicitar diagnóstico
    path('request/<int:patient_id>/', views.request_diagnosis, name='request_diagnosis'),
    
    # Ver detalle de diagnóstico
    path('detail/<int:diagnosis_id>/', views.diagnosis_detail, name='diagnosis_detail'),
    
    # Validar diagnóstico
    path('validate/<int:diagnosis_id>/', views.validate_diagnosis, name='validate_diagnosis'),
    
    # Descartar diagnóstico
    path('discard/<int:diagnosis_id>/', views.discard_diagnosis, name='discard_diagnosis'),
    
    # Exportar PDF (CU-019)
    path('export-pdf/<int:diagnosis_id>/', views.export_diagnosis_pdf, name='export_diagnosis_pdf'),
    # Verificar estado
    path('check-status/<int:diagnosis_id>/', views.check_status, name='check_status'),

    # Listar diagnósticos
    path('list/', views.diagnosis_list, name='diagnosis_list'),
]
