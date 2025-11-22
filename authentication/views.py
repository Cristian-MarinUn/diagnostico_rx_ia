from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.views import View
from django.utils import timezone
from datetime import timedelta
from .forms import LoginForm
from .models import User, Session, Log
import secrets

def get_client_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class LoginView(View):
    """Vista de inicio de sesión - CU-001"""
    
    template_name = 'authentication/login.html'
    form_class = LoginForm
    
    def get(self, request):
        """Muestra el formulario de login"""
        # Si el usuario ya está autenticado, redirigir al dashboard
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url(request.user))
        
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """Procesa el formulario de login"""
        form = self.form_class(request.POST)
        
        # Paso 8: Validar campos
        if not form.is_valid():
            messages.error(request, 'Complete los campos correctamente')
            return render(request, self.template_name, {'form': form})
        
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        remember_me = form.cleaned_data.get('remember_me', False)
        
        # Paso 10: Buscar usuario por email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Flujo Alternativo A1: Usuario no existe
            self.log_failed_attempt(request, email, 'Usuario no encontrado')
            messages.error(request, 'Usuario o contraseña incorrectos. Inténtelo nuevamente.')
            return render(request, self.template_name, {'form': form})
        
        # Paso 12: Verificar contraseña
        if not user.check_password(password):
            # Flujo Alternativo A1: Contraseña incorrecta
            self.log_failed_attempt(request, email, 'Contraseña incorrecta')
            messages.error(request, 'Usuario o contraseña incorrectos. Inténtelo nuevamente.')
            return render(request, self.template_name, {'form': form})
        
        # Verificar que el usuario esté activo
        if not user.estado or not user.is_active:
            messages.error(request, 'Tu cuenta ha sido desactivada. Contacta al administrador.')
            return render(request, self.template_name, {'form': form})
        
        # Paso 13-14: Crear sesión y generar token
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=24 if remember_me else 8)
        
        # Paso 15: Guardar sesión en BD
        session = Session.objects.create(
            user=user,
            token=token,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            expires_at=expires_at
        )
        
        # Actualizar último acceso
        user.ultimo_acceso = timezone.now()
        user.save(update_fields=['ultimo_acceso'])
        
        # Paso 18: Registrar login exitoso en logs
        Log.objects.create(
            user=user,
            accion='LOGIN_SUCCESS',
            nivel='INFO',
            descripcion=f'Login exitoso desde {get_client_ip(request)}',
            ip_address=get_client_ip(request)
        )
        
        # Autenticar usuario en Django
        django_login(request, user)
        
        # Configurar duración de sesión
        if not remember_me:
            request.session.set_expiry(0)  # Expira al cerrar navegador
        else:
            request.session.set_expiry(86400)  # 24 horas
        
        # Paso 21-23: Redirigir al dashboard según rol
        messages.success(request, f'Bienvenido, {user.get_full_name()} ({user.get_rol_display()})')
        return redirect(self.get_redirect_url(user))
    
    def get_redirect_url(self, user):
        """Determina la URL de redirección según el rol"""
        if user.rol == 'ADMINISTRADOR':
            return '/admin-dashboard/'
        elif user.rol == 'MEDICO_RADIOLOGO':
            return '/medico-dashboard/'
        elif user.rol == 'TECNICO_SALUD':
            return '/tecnico-dashboard/'
        return '/'
    
    def log_failed_attempt(self, request, email, razon):
        """Registra un intento fallido de login"""
        Log.objects.create(
            accion='LOGIN_FAILED',
            nivel='WARNING',
            descripcion=f'Intento fallido de login para {email}: {razon}',
            ip_address=get_client_ip(request),
            datos_adicionales={'email': email, 'razon': razon}
            )