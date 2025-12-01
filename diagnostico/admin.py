"""
================================
ARCHIVO: admin.py
================================
Configuración del panel de administración Django
"""

from django.contrib import admin
from .models import AIDiagnosis, DiagnosisLog


@admin.register(AIDiagnosis)
class AIDiagnosisAdmin(admin.ModelAdmin):
    """Administración de Diagnósticos IA"""
    
    list_display = [
        'id',
        'patient',
        'status',
        'confidence_level',
        'requested_by',
        'created_at',
        'completed_at'
    ]
    
    list_filter = [
        'status',
        'created_at',
        'completed_at',
        'model_version'
    ]
    
    search_fields = [
        'patient__identification',
        'patient__first_name',
        'patient__last_name',
        'diagnosis_result'
    ]
    
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'completed_at',
        'processing_time',
        'model_version'
    ]
    
    fieldsets = (
        ('Paciente y Médico', {
            'fields': ('patient', 'requested_by', 'images')
        }),
        ('Resultado del Diagnóstico', {
            'fields': (
                'status',
                'diagnosis_result',
                'confidence_level',
                'ai_observations'
            )
        }),
        ('Datos Técnicos', {
            'fields': (
                'heatmap_data',
                'model_version',
                'processing_time'
            ),
            'classes': ('collapse',)
        }),
        ('Validación Médica', {
            'fields': (
                'doctor_comments',
                'validated_by',
                'validated_at'
            )
        }),
        ('Metadatos', {
            'fields': (
                'id',
                'created_at',
                'updated_at',
                'completed_at',
                'error_message'
            ),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['images']
    
    date_hierarchy = 'created_at'
    
    def has_delete_permission(self, request, obj=None):
        """Solo administradores pueden eliminar diagnósticos"""
        return request.user.is_superuser


@admin.register(DiagnosisLog)
class DiagnosisLogAdmin(admin.ModelAdmin):
    """Administración de Logs de Auditoría"""
    
    list_display = [
        'id',
        'diagnosis',
        'action',
        'performed_by',
        'timestamp'
    ]
    
    list_filter = [
        'action',
        'timestamp'
    ]
    
    search_fields = [
        'diagnosis__id',
        'performed_by__username'
    ]
    
    readonly_fields = [
        'id',
        'diagnosis',
        'action',
        'performed_by',
        'details',
        'ip_address',
        'user_agent',
        'timestamp'
    ]
    
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        """No permitir crear logs manualmente"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Solo superusuarios pueden eliminar logs"""
        return request.user.is_superuser
