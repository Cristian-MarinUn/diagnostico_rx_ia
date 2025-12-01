from django.db import models
from users.models import Patient
from authentication.models import User
from medical_images.models import MedicalImage
import json


class AIDiagnosis(models.Model):
    """Modelo para almacenar diagnósticos generados por la IA"""
    
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('PROCESSING', 'Procesando'),
        ('COMPLETED', 'Completado'),
        ('FAILED', 'Error'),
        ('VALIDATED', 'Validado'),
        ('DISCARDED', 'Descartado'),
    )
    
    # Relaciones
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnoses')
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_diagnoses')
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_diagnoses')
    images = models.ManyToManyField(MedicalImage, related_name='diagnoses')
    
    # Estado y Resultado
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    diagnosis_result = models.TextField('Resultado del Diagnóstico', blank=True, null=True)
    confidence_level = models.FloatField('Nivel de Confianza (%)', default=0.0, help_text='Porcentaje de confianza (0-100)')
    ai_observations = models.JSONField('Observaciones de la IA', default=list, blank=True)
    
    # Datos técnicos
    heatmap_data = models.JSONField('Datos del Mapa de Calor', default=dict, blank=True)
    model_version = models.CharField('Versión del Modelo', max_length=50, blank=True, null=True)
    processing_time = models.FloatField('Tiempo de Procesamiento (s)', default=0.0, blank=True)
    
    # Validación médica
    doctor_comments = models.TextField('Comentarios del Médico', blank=True, null=True)
    validated_at = models.DateTimeField('Fecha de Validación', null=True, blank=True)
    
    # Errores
    error_message = models.TextField('Mensaje de Error', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de Actualización', auto_now=True)
    completed_at = models.DateTimeField('Fecha de Completación', null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['requested_by', '-created_at']),
        ]
        verbose_name = 'Diagnóstico IA'
        verbose_name_plural = 'Diagnósticos IA'
    
    def __str__(self):
        return f"Diagnóstico #{self.id} - {self.patient.get_full_name()} ({self.get_status_display()})"
    
    def get_status_display(self):
        """Devuelve el nombre legible del estado"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    @property
    def is_processing(self):
        """Verifica si el diagnóstico está siendo procesado"""
        return self.status in ['PENDING', 'PROCESSING']
    
    @property
    def is_completed(self):
        """Verifica si el diagnóstico está completado"""
        return self.status in ['COMPLETED', 'VALIDATED', 'DISCARDED']


class DiagnosisLog(models.Model):
    """Modelo para auditoría y registro de cambios en diagnósticos"""
    
    ACTION_CHOICES = (
        ('CREATED', 'Creado'),
        ('PROCESSING', 'Procesando'),
        ('COMPLETED', 'Completado'),
        ('FAILED', 'Error'),
        ('VALIDATED', 'Validado'),
        ('DISCARDED', 'Descartado'),
        ('COMMENTED', 'Comentado'),
        ('UPDATED', 'Actualizado'),
    )
    
    diagnosis = models.ForeignKey(AIDiagnosis, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField('Acción', max_length=20, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='diagnosis_logs')
    details = models.JSONField('Detalles', default=dict, blank=True)
    ip_address = models.GenericIPAddressField('Dirección IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True, null=True)
    timestamp = models.DateTimeField('Fecha y Hora', auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['diagnosis', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
        verbose_name = 'Log de Diagnóstico'
        verbose_name_plural = 'Logs de Diagnóstico'
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.diagnosis.id} ({self.timestamp})"
    
    def get_action_display(self):
        """Devuelve el nombre legible de la acción"""
        return dict(self.ACTION_CHOICES).get(self.action, self.action)
