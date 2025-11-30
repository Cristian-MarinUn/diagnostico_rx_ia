from django.contrib import admin
from .models import Patient

# ===== Patient Admin =====
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Admin para el modelo Patient"""
    
    list_display = [
        'identification',
        'get_full_name',
        'get_age',
        'get_gender_display',
        'email',
        'phone',
        'created_by',
        'created_at',
        'is_active'
    ]
    
    list_filter = [
        'gender',
        'is_active',
        'created_at',
        'updated_at'
    ]
    
    search_fields = [
        'identification',
        'first_name',
        'last_name',
        'email',
        'phone'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'created_by',
        'get_age'
    ]
    
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'identification',
                'first_name',
                'last_name',
                'date_of_birth',
                'get_age',
                'gender'
            )
        }),
        ('Información de Contacto', {
            'fields': (
                'email',
                'phone'
            )
        }),
        ('Metadatos', {
            'fields': (
                'created_by',
                'created_at',
                'updated_at',
                'is_active'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_age(self, obj):
        """Mostrar edad en admin"""
        return obj.get_age()
    get_age.short_description = 'Edad'
    
    def get_full_name(self, obj):
        """Mostrar nombre completo en admin"""
        return obj.get_full_name()
    get_full_name.short_description = 'Nombre Completo'
    
    def get_gender_display(self, obj):
        """Mostrar género en admin"""
        return obj.get_gender_display_spanish()
    get_gender_display.short_description = 'Género'
    
    def save_model(self, request, obj, form, change):
        """Guardar modelo y asignar creador si es nuevo"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# NOTE: 2FA models (TwoFactorAuth, TwoFactorCode, LoginAttempt) will be added to users/models.py later
# For now, this admin file is kept minimal to avoid import errors.

# TODO: Implement 2FA admin classes once models are defined in users/models.py

