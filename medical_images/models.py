from django.db import models
from users.models import Patient
from authentication.models import User


class MedicalImage(models.Model):
    """Modelo para almacenar imágenes médicas"""
    
    STUDY_TYPES = (
        ('RX', 'Radiografía'),
        ('TAC', 'Tomografía (TAC)'),
        ('RMN', 'Resonancia Magnética'),
        ('ECO', 'Ecografía'),
        ('MAM', 'Mamografía'),
        ('OTHER', 'Otro'),
    )
    
    MODALITY_CHOICES = (
        ('CR', 'Radiografía Digital (CR)'),
        ('DR', 'Radiografía Directa (DR)'),
        ('CT', 'Tomografía Computarizada (CT)'),
        ('MR', 'Resonancia Magnética (MR)'),
        ('US', 'Ultrasonido (US)'),
        ('XC', 'Radiografía Externa (XC)'),
        ('OTHER', 'Otra'),
    )
    
    # Relaciones
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_images')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_images')
    
    # Información del estudio
    study_type = models.CharField('Tipo de Estudio', max_length=10, choices=STUDY_TYPES, default='OTHER')
    study_date = models.DateField('Fecha del Estudio')
    study_description = models.TextField('Descripción del Estudio', blank=True, null=True)
    
    # Archivo
    file_path = models.FileField('Archivo', upload_to='medical_images/%Y/%m/%d/')
    file_hash = models.CharField('Hash del Archivo', max_length=256, unique=True, db_index=True)
    file_size = models.BigIntegerField('Tamaño del Archivo (bytes)', default=0)
    
    # Metadatos DICOM
    modality = models.CharField('Modalidad', max_length=10, choices=MODALITY_CHOICES, blank=True, null=True)
    institution = models.CharField('Institución', max_length=255, blank=True, null=True)
    
    # Control
    uploaded_at = models.DateTimeField('Fecha de Carga', auto_now_add=True)
    is_active = models.BooleanField('Activo', default=True)
    
    class Meta:
        ordering = ['-study_date']
        indexes = [
            models.Index(fields=['patient', '-study_date']),
            models.Index(fields=['study_type']),
            models.Index(fields=['uploaded_at']),
        ]
        verbose_name = 'Imagen Médica'
        verbose_name_plural = 'Imágenes Médicas'
    
    def __str__(self):
        return f"{self.get_study_type_display()} - {self.patient.get_full_name()} ({self.study_date})"
    
    def get_study_type_display(self):
        """Devuelve el nombre legible del tipo de estudio"""
        return dict(self.STUDY_TYPES).get(self.study_type, self.study_type)
