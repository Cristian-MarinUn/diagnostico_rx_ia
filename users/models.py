from django.db import models
from django.utils import timezone
import re


class Patient(models.Model):
    """Modelo para pacientes del sistema"""
    
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    # Información personal
    identification = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Identificación',
        help_text='Documento de identidad único'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Nombres'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Apellidos'
    )
    date_of_birth = models.DateField(
        verbose_name='Fecha de Nacimiento'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Género'
    )
    
    # Información de contacto
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Correo Electrónico'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    
    # Metadatos
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='patients_created',
        verbose_name='Creado por'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['identification']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.identification})"
    
    def get_full_name(self):
        """Obtener nombre completo del paciente"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_age(self):
        """Calcular edad del paciente"""
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age
    
    def get_gender_display_spanish(self):
        """Obtener género en español"""
        return dict(self.GENDER_CHOICES).get(self.gender, 'Otro')
