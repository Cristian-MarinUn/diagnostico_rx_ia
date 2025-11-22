from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    """Manager personalizado para el modelo de usuario"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario regular"""
        if not email:
            raise ValueError('El email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'ADMINISTRADOR')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Modelo de usuario personalizado"""
    
    ROLES = (
        ('ADMINISTRADOR', 'Administrador'),
        ('MEDICO_RADIOLOGO', 'Médico Radiólogo'),
        ('TECNICO_SALUD', 'Técnico de Salud'),
    )
    
    username = None  # Removemos username, usaremos email
    email = models.EmailField('Correo electrónico', unique=True)
    identificacion = models.CharField('Identificación', max_length=20, unique=True, null=True, blank=True)
    rol = models.CharField('Rol', max_length=20, choices=ROLES, default='TECNICO_SALUD')
    telefono = models.CharField('Teléfono', max_length=15, blank=True, null=True)
    foto_perfil = models.ImageField('Foto de perfil', upload_to='perfiles/', blank=True, null=True)
    fecha_registro = models.DateTimeField('Fecha de registro', auto_now_add=True)
    ultimo_acceso = models.DateTimeField('Último acceso', null=True, blank=True)
    estado = models.BooleanField('Activo', default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"
    
    def get_dashboard_url(self):
        """Retorna la URL del dashboard según el rol"""
        dashboard_urls = {
            'ADMINISTRADOR': '/admin/dashboard/',
            'MEDICO_RADIOLOGO': '/medico/dashboard/',
            'TECNICO_SALUD': '/tecnico/dashboard/',
        }
        return dashboard_urls.get(self.rol, '/')


class Session(models.Model):
    """Modelo para gestionar sesiones de usuario"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sessions')
    token = models.CharField('Token', max_length=500, unique=True)
    login_time = models.DateTimeField('Hora de inicio', auto_now_add=True)
    ip_address = models.GenericIPAddressField('Dirección IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    is_active = models.BooleanField('Activa', default=True)
    expires_at = models.DateTimeField('Expira en')
    
    class Meta:
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
        ordering = ['-login_time']
    
    def __str__(self):
        return f"Sesión de {self.user.email} - {self.login_time}"
    
    def is_expired(self):
        """Verifica si la sesión ha expirado"""
        return timezone.now() > self.expires_at


class Log(models.Model):
    """Modelo para registrar eventos del sistema"""
    
    NIVELES = (
        ('INFO', 'Información'),
        ('WARNING', 'Advertencia'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Crítico'),
    )
    
    ACCIONES = (
        ('LOGIN_SUCCESS', 'Login exitoso'),
        ('LOGIN_FAILED', 'Login fallido'),
        ('LOGOUT', 'Cierre de sesión'),
        ('PASSWORD_CHANGE', 'Cambio de contraseña'),
        ('PASSWORD_RESET', 'Recuperación de contraseña'),
        ('USER_CREATED', 'Usuario creado'),
        ('USER_UPDATED', 'Usuario actualizado'),
        ('USER_DELETED', 'Usuario eliminado'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField('Acción', max_length=50, choices=ACCIONES)
    nivel = models.CharField('Nivel', max_length=10, choices=NIVELES, default='INFO')
    descripcion = models.TextField('Descripción')
    ip_address = models.GenericIPAddressField('Dirección IP', null=True, blank=True)
    timestamp = models.DateTimeField('Fecha y hora', auto_now_add=True)
    datos_adicionales = models.JSONField('Datos adicionales', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_accion_display()} - {self.timestamp}"