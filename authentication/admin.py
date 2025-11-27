

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Session, Log

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para el modelo User"""
    
    list_display = ('email', 'get_full_name', 'rol', 'estado', 'ultimo_acceso', 'fecha_registro')
    list_filter = ('rol', 'estado', 'is_staff', 'fecha_registro')
    search_fields = ('email', 'first_name', 'last_name', 'identificacion')
    ordering = ('-fecha_registro',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'identificacion', 'telefono', 'foto_perfil')}),
        ('Permisos', {'fields': ('rol', 'estado', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('ultimo_acceso', 'fecha_registro', 'last_login')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'rol', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('fecha_registro', 'ultimo_acceso', 'last_login')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Admin para el modelo Session"""
    
    list_display = ('user', 'login_time', 'ip_address', 'is_active', 'expires_at')
    list_filter = ('is_active', 'login_time')
    search_fields = ('user__email', 'ip_address')
    ordering = ('-login_time',)
    readonly_fields = ('login_time', 'token')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """Admin para el modelo Log"""
    
    list_display = ('accion', 'user', 'nivel', 'timestamp', 'ip_address')
    list_filter = ('accion', 'nivel', 'timestamp')
    search_fields = ('user__email', 'descripcion', 'ip_address')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    
    def has_add_permission(self, request):
        return False  # No permitir agregar logs manualmente
    
    def has_change_permission(self, request, obj=None):
        return False  # No permitir editar logs