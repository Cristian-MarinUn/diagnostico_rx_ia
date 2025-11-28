from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import secrets

from .forms import LoginForm, PasswordRecoveryForm, PasswordResetForm
from .models import User, Session, Log, PasswordResetToken

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
            messages.error(
                request,
                'Usuario o contraseña incorrectos. Inténtelo nuevamente.')
            return render(request, self.template_name, {'form': form})

        # Paso 12: Verificar contraseña
        if not user.check_password(password):
            # Flujo Alternativo A1: Contraseña incorrecta
            self.log_failed_attempt(request, email, 'Contraseña incorrecta')
            messages.error(
                request,
                'Usuario o contraseña incorrectos. Inténtelo nuevamente.')
            return render(request, self.template_name, {'form': form})

        # Verificar que el usuario esté activo
        if not user.estado or not user.is_active:
            messages.error(
                request,
                'Tu cuenta ha sido desactivada. Contacta al administrador.')
            return render(request, self.template_name, {'form': form})

        # Paso 13-14: Crear sesión y generar token
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=24 if remember_me else 8)

        # Paso 15: Guardar sesión en BD
        session = Session.objects.create(user=user,
                                         token=token,
                                         ip_address=get_client_ip(request),
                                         user_agent=request.META.get(
                                             'HTTP_USER_AGENT', ''),
                                         expires_at=expires_at)

        # Actualizar último acceso
        user.ultimo_acceso = timezone.now()
        user.save(update_fields=['ultimo_acceso'])

        # Paso 18: Registrar login exitoso en logs
        Log.objects.create(
            user=user,
            accion='LOGIN_SUCCESS',
            nivel='INFO',
            descripcion=f'Login exitoso desde {get_client_ip(request)}',
            ip_address=get_client_ip(request))

        # Autenticar usuario en Django
        django_login(request, user)

        # Configurar duración de sesión
        if not remember_me:
            request.session.set_expiry(0)  # Expira al cerrar navegador
        else:
            request.session.set_expiry(86400)  # 24 horas

        # Redirigir a verificación 2FA (temporal frontend bypass)
        # TODO: Implementar verificación real 2FA en backend
        messages.info(request, 'Por favor verifica tu identidad.')
        return redirect(reverse('users:2fa-verify'))

        # Si el usuario debe cambiar la contraseña en el primer acceso,
        # redirigirlo a la vista de cambio de contraseña antes del dashboard.
        # if getattr(user, 'must_change_password', False):
        #     messages.info(request, 'Debes cambiar tu contraseña en el primer acceso.')
        #     return redirect(reverse('users:change_password'))

        # Paso 21-23: Redirigir al dashboard según rol
        # messages.success(
        #     request,
        #     f'Bienvenido, {user.get_full_name()} ({user.get_rol_display()})')
        # return redirect(self.get_redirect_url(user))

    def get_redirect_url(self, user):
        """Determina la URL de redirección según el rol."""
        # Si es administrador, enviar al admin dashboard; si no, al dashboard general.
        if getattr(user, 'rol', None) == 'ADMINISTRADOR':
            return reverse('users:admin_dashboard')
        return reverse('users:dashboard')

    def log_failed_attempt(self, request, email, razon):
        """Registra un intento fallido de login"""
        Log.objects.create(
            accion='LOGIN_FAILED',
            nivel='WARNING',
            descripcion=f'Intento fallido de login para {email}: {razon}',
            ip_address=get_client_ip(request),
            datos_adicionales={
                'email': email,
                'razon': razon
            })


#Cerrar sesión
class LogoutView(LoginRequiredMixin, View):
    """Vista de cierre de sesión - CU-003"""
    
    login_url = '/auth/login/'
    
    def get(self, request):
        """Muestra confirmación de cierre de sesión"""
        return render(request, 'authentication/logout_confirm.html')
    
    def post(self, request):
        """Procesa el cierre de sesión"""
        user = request.user
        
        # Paso 6-7: Invalidar token y eliminar sesión
        try:
            # Buscar sesiones activas del usuario
            active_sessions = Session.objects.filter(
                user=user,
                is_active=True
            )
            
            # Invalidar todas las sesiones activas
            for session in active_sessions:
                session.is_active = False
                session.save()
            
            # Paso 11: Registrar cierre de sesión en logs
            Log.objects.create(
                user=user,
                accion='LOGOUT',
                nivel='INFO',
                descripcion=f'Cierre de sesión manual desde {get_client_ip(request)}',
                ip_address=get_client_ip(request)
            )
            
        except Exception as e:
            # Si hay error, registrarlo pero continuar con el logout
            Log.objects.create(
                user=user,
                accion='LOGOUT',
                nivel='ERROR',
                descripcion=f'Error al invalidar sesión: {str(e)}',
                ip_address=get_client_ip(request)
            )
        
        # Paso 5: Borrar datos de sesión del navegador
        # Django se encarga de limpiar cookies, storage, etc.
        django_logout(request)
        
        # Paso 6: Redirigir al login con mensaje
        messages.success(request, 'Has cerrado sesión correctamente.')
        return redirect('authentication:login')


class LogoutCancelView(LoginRequiredMixin, View):
    """Cancela el cierre de sesión - Flujo Alternativo A1"""
    
    login_url = '/auth/login/'
    
    def post(self, request):
        """Usuario cancela el cierre de sesión"""
        # Redirigir al dashboard según el rol del usuario
        if request.user.rol == 'admin':
            return redirect('users:admin_dashboard')
        else:
            return redirect('users:dashboard')



# ================================
# CU-002: RECUPERAR CONTRASEÑA
# ================================

def password_recovery_view(request):
    """
    Vista para solicitar recuperación de contraseña.
    Fase 1-3 del CU-002: Solicitud y generación de token
    """
    if request.method == 'POST':
        form = PasswordRecoveryForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                # A1: Verificar si el usuario existe
                user = User.objects.get(email=email, is_active=True)
                
                # Generar token único y temporal (válido por 15 minutos)
                token = secrets.token_urlsafe(32)
                expires_at = timezone.now() + timedelta(minutes=15)
                
                # Guardar o actualizar token en la base de datos
                PasswordResetToken.objects.update_or_create(
                    user=user,
                    defaults={
                        'token': token,
                        'expires_at': expires_at,
                        'is_used': False
                    }
                )
                
                # Construir enlace de restablecimiento
                reset_link = request.build_absolute_uri(
                    f'/authentication/password-reset/{token}/'
                )
                
                # Enviar correo con el enlace
                try:
                    send_password_reset_email(user.email, user.get_full_name(), reset_link)
                    
                    # Mensaje genérico por seguridad (no revela si el email existe)
                    messages.success(
                        request,
                        'Si el correo está registrado, recibirás un enlace para restablecer tu contraseña.'
                    )
                    
                except Exception as e:
                    # Error al enviar correo
                    messages.error(
                        request,
                        'No se pudo enviar el correo. Intenta nuevamente más tarde.'
                    )
                    print(f"Error enviando correo: {e}")
                
            except User.DoesNotExist:
                # A1: Usuario no encontrado
                # Mensaje genérico por seguridad (no revela que el email no existe)
                messages.success(
                    request,
                    'Si el correo está registrado, recibirás un enlace para restablecer tu contraseña.'
                )
            
            return redirect('authentication:password_recovery')
    else:
        form = PasswordRecoveryForm()
    
    return render(request, 'authentication/password_recovery.html', {
        'form': form
    })


def password_reset_view(request, token):
    """
    Vista para restablecer la contraseña con el token.
    Fase 4-8 del CU-002: Validación de token y actualización de contraseña
    """
    # Validar el token
    try:
        reset_token = PasswordResetToken.objects.get(
            token=token,
            is_used=False,
            expires_at__gt=timezone.now()
        )
        user = reset_token.user
        
    except PasswordResetToken.DoesNotExist:
        # A2: Token expirado o inválido
        messages.error(
            request,
            'El enlace de restablecimiento ha expirado o no es válido. Solicita uno nuevo.'
        )
        return redirect('authentication:password_recovery')
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            # A3: Verificar que las contraseñas coincidan
            if new_password != confirm_password:
                messages.error(
                    request,
                    'Las contraseñas no coinciden. Vuelve a intentarlo.'
                )
                return render(request, 'authentication/password_reset.html', {
                    'form': form,
                    'token': token
                })
            
            # Actualizar la contraseña
            user.password = make_password(new_password)
            user.save()
            
            # Invalidar el token
            reset_token.is_used = True
            reset_token.used_at = timezone.now()
            reset_token.save()
            
            # Invalidar todos los tokens anteriores del usuario
            PasswordResetToken.objects.filter(
                user=user,
                is_used=False
            ).update(is_used=True)
            
            messages.success(
                request,
                'Tu contraseña ha sido actualizada exitosamente. Inicia sesión con tus nuevas credenciales.'
            )
            return redirect('authentication:login')
    else:
        form = PasswordResetForm()
    
    return render(request, 'authentication/password_reset.html', {
        'form': form,
        'token': token
    })


def send_password_reset_email(recipient_email, recipient_name, reset_link):
    """
    Función auxiliar para enviar el correo de recuperación de contraseña
    """
    subject = 'Recuperación de Contraseña - Diagnóstico IA'
    
    message = f"""
    Hola {recipient_name},

    Has solicitado restablecer tu contraseña para el sistema de Diagnóstico Asistido por IA.

    Para crear una nueva contraseña, haz clic en el siguiente enlace:
    {reset_link}

    Este enlace expirará en 15 minutos por seguridad.

    Si no solicitaste este cambio, ignora este mensaje y tu contraseña permanecerá sin cambios.

    Saludos,
    Equipo de Diagnóstico IA
    Universidad Nacional de Colombia
    """
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f8f9fa;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .button {{
                display: inline-block;
                padding: 15px 30px;
                background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔑 Recuperación de Contraseña</h1>
        </div>
        <div class="content">
            <p>Hola <strong>{recipient_name}</strong>,</p>
            
            <p>Has solicitado restablecer tu contraseña para el sistema de <strong>Diagnóstico Asistido por IA</strong>.</p>
            
            <p>Para crear una nueva contraseña, haz clic en el siguiente botón:</p>
            
            <center>
                <a href="{reset_link}" class="button">Restablecer Contraseña</a>
            </center>
            
            <p><small>O copia y pega este enlace en tu navegador:<br>
            <a href="{reset_link}">{reset_link}</a></small></p>
            
            <p><strong>⏱️ Este enlace expirará en 15 minutos por seguridad.</strong></p>
            
            <p>Si no solicitaste este cambio, ignora este mensaje y tu contraseña permanecerá sin cambios.</p>
            
            <p>Saludos,<br>
            <strong>Equipo de Diagnóstico IA</strong><br>
            Universidad Nacional de Colombia</p>
        </div>
        <div class="footer">
            <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
        </div>
    </body>
    </html>
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        html_message=html_message,
        fail_silently=False,
    )










