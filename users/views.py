# ================================
# ARCHIVO: users/views.py
# ================================

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from authentication.models import User, Session, Log

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from authentication.models import User, Log
import secrets
import string


def get_client_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ProfileView(LoginRequiredMixin, View):
    """Vista para visualizar perfil de usuario - CU-007"""

    login_url = '/auth/login/'
    template_name = 'users/profile.html'

    def get(self, request):
        """Muestra el perfil del usuario autenticado"""
        user = request.user

        try:
            # Obtener información adicional del usuario
            # Sesiones activas
            active_sessions = Session.objects.filter(
                user=user,
                is_active=True
            ).order_by('-login_time')

            # Última sesión
            last_session = Session.objects.filter(
                user=user
            ).order_by('-login_time').first()

            # Logs recientes del usuario
            recent_logs = Log.objects.filter(
                user=user
            ).order_by('-timestamp')[:5]

            # Estadísticas básicas
            total_logins = Log.objects.filter(
                user=user,
                accion='LOGIN_SUCCESS'
            ).count()

            context = {
                'user_data': {
                    'nombre_completo': user.get_full_name(),
                    'email': user.email,
                    'identificacion': user.identificacion,
                    'rol': user.get_rol_display(),
                    'telefono': user.telefono or 'No especificado',
                    'estado': 'Activo' if user.estado else 'Inactivo',
                    'fecha_registro': user.fecha_registro,
                    'ultimo_acceso': user.ultimo_acceso,
                },
                'active_sessions': active_sessions,
                'last_session': last_session,
                'recent_logs': recent_logs,
                'statistics': {
                    'total_logins': total_logins,
                    'active_sessions_count': active_sessions.count(),
                }
            }

            return render(request, self.template_name, context)

        except Exception as e:
            # Flujo Alternativo A1: Error al recuperar datos
            Log.objects.create(
                user=user,
                accion='USER_UPDATED',
                nivel='ERROR',
                descripcion=f'Error al cargar perfil: {str(e)}',
                ip_address=get_client_ip(request)
            )

            messages.error(request, 'No fue posible cargar tu perfil. Intenta nuevamente más tarde.')
            return redirect('core:home')


class DashboardView(LoginRequiredMixin, View):
    """Vista del dashboard de usuario - muestra layout principal para usuarios autenticados"""

    login_url = '/auth/login/'
    template_name = 'users/dashboard.html'

    def get(self, request):
        user = request.user

        # Datos resumidos para el dashboard
        active_sessions = Session.objects.filter(user=user, is_active=True).order_by('-login_time')
        total_logins = Log.objects.filter(user=user, accion='LOGIN_SUCCESS').count()

        context = {
            'user': user,
            'statistics': {
                'total_logins': total_logins,
                'active_sessions_count': active_sessions.count(),
            },
        }

        return render(request, self.template_name, context)


class AdminDashboardView(LoginRequiredMixin, View):
    """Dashboard exclusivo para administradores."""

    login_url = '/auth/login/'
    template_name = 'users/admin_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario sea administrador
        user = request.user
        if not getattr(user, 'rol', None) == 'ADMINISTRADOR':
            # No es admin: redirigir al dashboard general
            return redirect('users:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = request.user
        # Datos y métricas que podrían interesar al administrador
        total_users = User.objects.count()
        total_sessions = Session.objects.count()
        total_logs = Log.objects.count()

        # Proveer también un dict `statistics` para mantener compatibilidad
        # con la plantilla que puede esperar `statistics.total_logins` y
        # `statistics.active_sessions_count`.
        statistics = {
            'total_logins': total_logs,
            'active_sessions_count': total_sessions,
        }

        context = {
            'user': user,
            'metrics': {
                'total_users': total_users,
                'total_sessions': total_sessions,
                'total_logs': total_logs,
            },
            'statistics': statistics,
        }

        return render(request, self.template_name, context)
# ================================
#crear usuarios
def get_client_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Vista del dashboard de administrador"""
    
    login_url = '/auth/login/'
    template_name = 'users/admin_dashboard.html'
    
    def test_func(self):
        """Solo administradores pueden acceder"""
        return self.request.user.rol == 'ADMINISTRADOR'
    
    def handle_no_permission(self):
        """Manejo de acceso denegado"""
        messages.error(self.request, 'No tienes permisos para acceder a esta sección.')
        return redirect('core:home')
    
    def get(self, request):
        """Muestra el dashboard del administrador"""
        # Estadísticas generales
        total_users = User.objects.all().count()
        active_users = User.objects.filter(estado=True).count()
        inactive_users = User.objects.filter(estado=False).count()
        
        # Usuarios por rol
        admins = User.objects.filter(rol='ADMINISTRADOR').count()
        medicos = User.objects.filter(rol='MEDICO_RADIOLOGO').count()
        tecnicos = User.objects.filter(rol='TECNICO_SALUD').count()
        
        # Usuarios recientes
        recent_users = User.objects.all().order_by('-fecha_registro')[:5]
        
        # Actividad reciente
        recent_activity = Log.objects.all().order_by('-timestamp')[:10]
        
        context = {
            'statistics': {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': inactive_users,
                'admins': admins,
                'medicos': medicos,
                'tecnicos': tecnicos,
            },
            'recent_users': recent_users,
            'recent_activity': recent_activity,
        }
        
        return render(request, self.template_name, context)


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Vista para crear nuevo usuario - CU-004"""
    
    login_url = '/auth/login/'
    template_name = 'users/user_create.html'
    
    def test_func(self):
        """Solo administradores pueden crear usuarios"""
        return self.request.user.rol == 'ADMINISTRADOR'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para crear usuarios.')
        return redirect('users:admin_dashboard')
    
    def get(self, request):
        """Muestra el formulario de registro"""
        context = {
            'roles': User.ROLES,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Procesa el registro de nuevo usuario"""
        
        # Paso 4-5: Obtener datos del formulario
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        identificacion = request.POST.get('identificacion', '').strip()
        rol = request.POST.get('rol', '').strip()
        estado = request.POST.get('estado', 'on') == 'on'
        
        # Paso 6: Validar campos requeridos
        if not all([first_name, last_name, email, identificacion, rol]):
            messages.error(request, 'Complete los campos obligatorios.')
            return render(request, self.template_name, {
                'roles': User.ROLES,
                'form_data': request.POST
            })
        
        # Validar formato de email
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messages.error(request, 'Formato de correo electrónico inválido.')
            return render(request, self.template_name, {
                'roles': User.ROLES,
                'form_data': request.POST
            })
        
        # Paso 6: Verificar si el email ya existe (Flujo A1)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ingresado ya se encuentra registrado. Verifique la información.')
            return render(request, self.template_name, {
                'roles': User.ROLES,
                'form_data': request.POST
            })
        
        # Verificar si la identificación ya existe
        if User.objects.filter(identificacion=identificacion).exists():
            messages.error(request, 'La identificación ingresada ya se encuentra registrada.')
            return render(request, self.template_name, {
                'roles': User.ROLES,
                'form_data': request.POST
            })
        
        # Paso 7.2: Generar contraseña temporal
        password_temporal = self.generate_temp_password()
        
        try:
            # Paso 7.1: Crear usuario en la base de datos
            user = User.objects.create_user(
                email=email,
                password=password_temporal,
                first_name=first_name,
                last_name=last_name,
                identificacion=identificacion,
                rol=rol,
                estado=estado
            )
            
            # Paso 7.4: Enviar credenciales por correo
            email_sent = self.send_credentials_email(
                user=user,
                password=password_temporal,
                admin=request.user
            )
            
            # Paso 8: Registrar evento en logs
            Log.objects.create(
                user=request.user,
                accion='USER_CREATED',
                nivel='INFO',
                descripcion=f'Usuario creado: {user.email} con rol {user.get_rol_display()}',
                ip_address=get_client_ip(request),
                datos_adicionales={
                    'new_user_id': user.id,
                    'new_user_email': user.email,
                    'new_user_rol': user.rol,
                    'email_sent': email_sent
                }
            )
            
            # Paso 9: Mostrar mensaje de éxito
            if email_sent:
                messages.success(
                    request, 
                    f'Usuario {user.get_full_name()} registrado exitosamente. '
                    f'Se han enviado las credenciales al correo {user.email}.'
                )
            else:
                # Flujo Alternativo A3: Error en envío de correo
                messages.warning(
                    request,
                    f'Usuario registrado, pero no se pudo enviar el correo con las credenciales. '
                    f'Credenciales temporales: Email: {user.email} | Contraseña: {password_temporal}'
                )
            
            # Redirigir a la lista de usuarios o dashboard
            return redirect('users:admin_dashboard')
            
        except Exception as e:
            # Error general
            messages.error(request, f'Error al crear el usuario: {str(e)}')
            
            # Registrar error en logs
            Log.objects.create(
                user=request.user,
                accion='USER_CREATED',
                nivel='ERROR',
                descripcion=f'Error al crear usuario: {str(e)}',
                ip_address=get_client_ip(request)
            )
            
            return render(request, self.template_name, {
                'roles': User.ROLES,
                'form_data': request.POST
            })
    
    def generate_temp_password(self, length=12):
        """Genera una contraseña temporal segura"""
        # Incluir mayúsculas, minúsculas, números y símbolos
        characters = string.ascii_letters + string.digits + "!@#$%&*"
        
        # Asegurar al menos uno de cada tipo
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%&*")
        ]
        
        # Completar el resto
        password.extend(secrets.choice(characters) for _ in range(length - 4))
        
        # Mezclar
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        
        return ''.join(password_list)
    
    def send_credentials_email(self, user, password, admin):
        """Envía las credenciales por correo electrónico"""
        try:
            subject = 'Bienvenido al Sistema de Diagnóstico IA'
            message = f"""
Hola {user.get_full_name()},

Has sido registrado en el Sistema de Diagnóstico Asistido por IA.

Tus credenciales de acceso son:

Email: {user.email}
Contraseña temporal: {password}

Por seguridad, te recomendamos cambiar tu contraseña en el primer inicio de sesión.

Puedes acceder al sistema en: {settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost:8000'}

Rol asignado: {user.get_rol_display()}

Si tienes alguna pregunta, contacta al administrador.

---
Este correo fue enviado por: {admin.get_full_name()}
Sistema de Diagnóstico IA - Universidad Nacional de Colombia
            """
            
            # Enviar correo
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            return True
            
        except Exception as e:
            # Registrar error pero no fallar la creación del usuario
            Log.objects.create(
                accion='USER_CREATED',
                nivel='ERROR',
                descripcion=f'Error al enviar correo de credenciales: {str(e)}',
                ip_address=get_client_ip(self.request),
                datos_adicionales={
                    'user_email': user.email,
                    'error': str(e)
                }
            )
            return False