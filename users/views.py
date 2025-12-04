# ================================
# ARCHIVO: users/views.py
# ================================

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from datetime import timedelta, date
from authentication.models import User, Session, Log
from django.utils.crypto import get_random_string
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.middleware.csrf import get_token
from .models import Patient
from .forms import PatientRegistrationForm


# ================================
# CU-013: MÓDULO DE DIAGNÓSTICO ASISTIDO POR IA (SIMULACIÓN)
# ================================


@login_required
def request_diagnosis_ia_view(request):
    """
    Módulo simplificado para 'Solicitar Análisis IA' según CU-013.
    - Solo accesible para médicos radiólogos
    - Permite seleccionar un paciente y simular la visualización de un
      diagnóstico preliminar (imagen se muestra como espacio vacío para
      futuras integraciones).
    """
    user = request.user
    if user.rol != 'MEDICO_RADIOLOGO':
        messages.error(request, 'No tienes permisos para acceder a este módulo.')
        return redirect('users:user_dashboard')

    patients = Patient.objects.filter(is_active=True).order_by('last_name', 'first_name')

    # Si no existen pacientes en la base de datos, crear algunos de prueba
    # Esto facilita la simulación del flujo cuando la instalación es limpia
    if not patients.exists():
        try:
            sample_data = [
                ('100001', 'Juan', 'Pérez', date(1980, 5, 12), 'M'),
                ('100002', 'María', 'García', date(1975, 8, 3), 'F'),
                ('100003', 'Carlos', 'Rodríguez', date(1990, 2, 20), 'M'),
                ('100004', 'Laura', 'Pineda', date(1985, 11, 30), 'F'),
                ('100005', 'Andrés', 'Ramírez', date(1978, 7, 14), 'M'),
            ]
            created = []
            for ident, fn, ln, dob, gender in sample_data:
                p = Patient.objects.create(
                    identification=ident,
                    first_name=fn,
                    last_name=ln,
                    date_of_birth=dob,
                    gender=gender,
                    email=f'{fn.lower()}.{ln.lower()}@example.com',
                    phone='0000000000',
                    created_by=request.user,
                    is_active=True,
                )
                created.append(p)
            patients = Patient.objects.filter(is_active=True).order_by('last_name', 'first_name')
            messages.info(request, f'Se han creado {len(created)} pacientes de prueba para la simulación.')
        except Exception:
            # No bloquear el flujo si la creación falla
            patients = Patient.objects.filter(is_active=True).order_by('last_name', 'first_name')
    selected_patient = None
    simulated_diag = None

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        action = request.POST.get('action')
        try:
            selected_patient = Patient.objects.get(id=patient_id)
        except Exception:
            selected_patient = None

        # Simular la obtención de un diagnóstico preliminar
        if action == 'simulate' and selected_patient:
            # Búsqueda simulada de diagnósticos del paciente
            # En producción, esto consultaría AIDiagnosis.objects.filter(patient=selected_patient)
            simulated_diag = {
                'id': 1,
                'patient_id': selected_patient.id,
                'patient_name': selected_patient.get_full_name(),
                'patient_id_doc': selected_patient.identification,
                'title': f'Diagnóstico preliminar para {selected_patient.get_full_name()}',
                'result': 'Posible consolidación pulmonar en lóbulo inferior derecho',
                'confidence': 87.4,
                'observations': [
                    'Opacidad localizada en proyección posterior',
                    'Correlacionar clínicamente y considerar seguimiento',
                    'Sugerir radiografía lateral para mejor evaluación'
                ],
                'image_available': False,
            }

        # Manejo de comentarios (CU-014)
        if action == 'save_comment' and selected_patient:
            comment_text = request.POST.get('comment_text', '').strip()
            if not comment_text:
                messages.error(request, 'Debe ingresar al menos una observación')
            else:
                # Registrar comentario en logs como auditoría (simulación de guardado en BD de diagnóstico)
                try:
                    # Incluimos un marcador con patient_id para identificar comentarios específicos del paciente
                    diag_marker = f"[DIAG_SIM:patient_{selected_patient.id}]"
                    descripcion = f"{diag_marker} Comentario agregado por {request.user.get_full_name()}: {comment_text}"
                    Log.objects.create(
                        user=request.user,
                        accion='USER_UPDATED',
                        nivel='INFO',
                        descripcion=descripcion,
                        ip_address=get_client_ip(request)
                    )
                    messages.success(request, 'Comentarios guardados exitosamente')
                except Exception as e:
                    messages.error(request, 'No fue posible guardar los comentarios. Intente nuevamente')

    context = {
        'patients': patients,
        'selected_patient': selected_patient,
        'simulated_diag': simulated_diag,
    }

    # Cargar comentarios previamente registrados para el paciente específico
    diag_comments = []
    try:
        if selected_patient:
            # Usamos un marcador con patient_id en la descripción para filtrar comentarios específicos
            diag_marker = f"[DIAG_SIM:patient_{selected_patient.id}]"
            diag_comments = Log.objects.filter(descripcion__contains=diag_marker).order_by('-timestamp')
    except Exception:
        diag_comments = []

    context['diag_comments'] = diag_comments

    return render(request, 'users/request_diagnosis_ia.html', context)

# ================================
# PERFIL DE USUARIO
# ================================

@login_required
def profile_view(request):
    """
    Vista para visualizar el perfil del usuario autenticado
    """
    user = request.user
    
    try:
        # Obtener información adicional del usuario
        active_sessions = Session.objects.filter(
            user=user,
            is_active=True
        ).order_by('-login_time')
        
        total_logins = Log.objects.filter(
            user=user,
            accion='LOGIN_SUCCESS'
        ).count()
        
        recent_logs = Log.objects.filter(
            user=user
        ).order_by('-timestamp')[:5]
        
        context = {
            'user_data': {
                'nombre_completo': user.get_full_name(),
                'email': user.email,
                'identificacion': user.identificacion or 'No especificado',
                'rol': user.get_rol_display(),
                'telefono': user.telefono or 'No especificado',
                'estado': 'Activo' if user.estado else 'Inactivo',
                'fecha_registro': user.fecha_registro,
                'ultimo_acceso': user.ultimo_acceso,
            },
            'active_sessions': active_sessions,
            'recent_logs': recent_logs,
            'statistics': {
                'total_logins': total_logins,
                'active_sessions_count': active_sessions.count(),
            }
        }
        
        return render(request, 'users/profile.html', context)
        
    except Exception as e:
        messages.error(request, 'No fue posible cargar tu perfil. Intenta nuevamente más tarde.')
        return redirect('users:dashboard')

@login_required
def profile_edit_view(request):
    """
    Vista para editar el perfil del usuario autenticado
    """
    user = request.user
    
    if request.method == 'GET':
        context = {
            'user_data': {
                'nombre_completo': user.get_full_name(),
                'email': user.email,
                'identificacion': user.identificacion,
                'rol': user.get_rol_display(),
                'telefono': user.telefono or '',
                'fecha_registro': user.fecha_registro,
                'ultimo_acceso': user.ultimo_acceso,
            }
        }
        return render(request, 'users/profile_edit.html', context)
    
    elif request.method == 'POST':
        try:
            # Actualizar información del perfil
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            user.telefono = request.POST.get('telefono', '').strip()
            
            # Validar nombre completo
            if not user.first_name or not user.last_name:
                messages.error(request, 'El nombre y apellido son requeridos.')
                return redirect('users:profile_edit')
            
            user.save()
            
            # Registrar cambios
            Log.objects.create(
                user=user,
                accion='PROFILE_UPDATE',
                descripcion=f'Usuario actualizó su perfil',
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('users:profile')
            
        except Exception as e:
            messages.error(request, 'Error al actualizar tu perfil. Intenta nuevamente.')
            return redirect('users:profile_edit')

def get_client_ip(request):
    """Obtiene la IP del cliente desde la solicitud"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# ================================
# DASHBOARD GENERAL
# ================================

@login_required
def dashboard_view(request):
    """
    Vista principal del dashboard que redirige según el rol del usuario
    """
    user = request.user
    
    # Redirigir según el rol
    if user.rol == 'ADMINISTRADOR':
        return redirect('users:admin_dashboard')
    elif user.rol == 'MEDICO_RADIOLOGO':
        return redirect('users:user_dashboard')
    elif user.rol == 'TECNICO_SALUD':
        return redirect('users:user_dashboard')
    else:
        messages.error(request, 'No tienes un rol asignado válido.')
        return redirect('core:home')

# ================================
# DASHBOARD DE USUARIO (MÉDICO/TÉCNICO)
# ================================

@login_required
def user_dashboard_view(request):
    """
    Dashboard para médicos radiólogos y técnicos de salud
    """
    user = request.user
    
    # Verificar que el usuario tenga un rol apropiado
    if user.rol not in ['MEDICO_RADIOLOGO', 'TECNICO_SALUD']:
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('core:home')
    
    # Datos base
    context = {
        'user': user,
    }
    
    # Estadísticas según el rol
    if user.rol == 'MEDICO_RADIOLOGO':
        context.update(get_medico_stats(user))
        context['recent_activities'] = get_recent_activities_medico(user)
    elif user.rol == 'TECNICO_SALUD':
        context.update(get_tecnico_stats(user))
        context['recent_activities'] = get_recent_activities_tecnico(user)
    
    return render(request, 'users/user_dashboard.html', context)

def get_medico_stats(user):
    """
    Obtiene estadísticas para médicos radiólogos
    """
    # TODO: Implementar con modelos reales cuando estén disponibles
    stats = {
        'total_estudios': 0,  # Conteo de estudios asignados
        'total_diagnosticos': 0,  # Diagnósticos completados
        'pendientes': 0,  # Diagnósticos pendientes
        'precision_ia': '94.2',  # Precisión promedio de la IA
    }
    
    # Ejemplo de cómo obtenerlo cuando tengas los modelos:
    # from diagnosis.models import Diagnosis
    # stats['total_diagnosticos'] = Diagnosis.objects.filter(
    #     medico=user,
    #     estado='FINALIZADO'
    # ).count()
    
    return stats

def get_tecnico_stats(user):
    """
    Obtiene estadísticas para técnicos de salud
    """
    # TODO: Implementar con modelos reales cuando estén disponibles
    stats = {
        'total_estudios': 0,
        'imagenes_cargadas': 0,  # Total de imágenes cargadas
        'en_proceso': 0,  # Imágenes siendo procesadas
        'completados': 0,  # Estudios completados hoy
    }
    
    # Ejemplo de cómo obtenerlo cuando tengas los modelos:
    # from images.models import MedicalImage
    # stats['imagenes_cargadas'] = MedicalImage.objects.filter(
    #     tecnico_carga=user
    # ).count()
    
    return stats

def get_recent_activities_medico(user):
    """
    Obtiene actividades recientes del médico
    """
    # Datos de ejemplo - reemplazar con consultas reales
    activities = [
        {
            'icon': '🔍',
            'type': 'primary',
            'title': 'Diagnóstico completado',
            'description': 'Análisis de radiografía de tórax - Paciente: Juan Pérez',
            'time': 'Hace 2 horas',
            'status': 'success',
            'status_text': 'Completado'
        },
        {
            'icon': '📊',
            'type': 'info',
            'title': 'Análisis IA solicitado',
            'description': 'Solicitud de análisis para estudio #1234',
            'time': 'Hace 4 horas',
            'status': 'warning',
            'status_text': 'En proceso'
        },
        {
            'icon': '✅',
            'type': 'success',
            'title': 'Reporte generado',
            'description': 'Reporte mensual de diagnósticos exportado',
            'time': 'Ayer',
            'status': 'success',
            'status_text': 'Completado'
        }
    ]
    
    return activities

def get_recent_activities_tecnico(user):
    """
    Obtiene actividades recientes del técnico
    """
    # Datos de ejemplo - reemplazar con consultas reales
    activities = [
        {
            'icon': '📤',
            'type': 'success',
            'title': 'Imágenes cargadas',
            'description': '5 imágenes radiológicas subidas al sistema',
            'time': 'Hace 1 hora',
            'status': 'success',
            'status_text': 'Completado'
        },
        {
            'icon': '⚙️',
            'type': 'warning',
            'title': 'Procesamiento en curso',
            'description': '3 imágenes siendo analizadas por IA',
            'time': 'Hace 2 horas',
            'status': 'warning',
            'status_text': 'Procesando'
        },
        {
            'icon': '✅',
            'type': 'info',
            'title': 'Carga completada',
            'description': 'Estudio #5678 completado y notificado',
            'time': 'Hace 3 horas',
            'status': 'success',
            'status_text': 'Notificado'
        }
    ]
    
    return activities


# ================================
# 2FA - Simple Verify Page (frontend bypass)
# ================================


@method_decorator(login_required, name='dispatch')
class Verify2FAView(View):
    """
    Simple 2FA verification view for frontend testing.
    GET: render a page asking for the 2FA code (or allow bypass).
    POST: if 'bypass' provided, set a session flag and redirect to dashboard.
    NOTE: This is a temporary frontend-only bypass; backend verification should be
    implemented later.
    """
    template_name = 'users/2fa_verify.html'

    def get(self, request, *args, **kwargs):
        # Ensure CSRF token is available in template
        get_token(request)
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        # Temporary bypass button: sets session flag and redirects
        if request.POST.get('bypass'):
            request.session['2fa_verified'] = True
            messages.success(request, 'Verificación 2FA marcada como completada (temporal).')
            return redirect('users:dashboard')

        # Otherwise, you can implement real verification here later
        messages.error(request, 'Código inválido o verificación no implementada aún.')
        return redirect('users:2fa-verify')

# ================================
# DASHBOARD DE ADMINISTRADOR
# ================================

@login_required
def admin_dashboard_view(request):
    """
    Dashboard para administradores del sistema
    """
    user = request.user
    
    # Verificar que el usuario sea administrador
    if user.rol != 'ADMINISTRADOR':
        messages.error(request, 'No tienes permisos de administrador.')
        return redirect('users:user_dashboard')
    
    # Estadísticas generales del sistema
    stats = get_admin_stats()
    
    # Usuarios recientes
    recent_users = get_recent_users()
    
    # Actividad del sistema
    system_activities = get_system_activities()
    
    context = {
        'user': user,
        'total_usuarios': stats['total_usuarios'],
        'total_medicos': stats['total_medicos'],
        'total_tecnicos': stats['total_tecnicos'],
        'total_diagnosticos': stats['total_diagnosticos'],
        'total_imagenes': stats['total_imagenes'],
        'precision_sistema': stats['precision_sistema'],
        'recent_users': recent_users,
        'system_activities': system_activities,
    }
    
    return render(request, 'users/admin_dashboard.html', context)


@login_required
def user_list_view(request):
    """
    Lista con todos los usuarios (vista para administradores).
    Soporta paginación básica.
    """
    # Verificar permisos de administrador
    if request.user.rol != 'ADMINISTRADOR':
        messages.error(request, 'No tienes permisos de administrador.')
        return redirect('users:user_dashboard')

    users_qs = User.objects.all().order_by('-fecha_registro')
    paginator = Paginator(users_qs, 25)  # 25 usuarios por página
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    context = {
        'users_list': users_page,
    }
    return render(request, 'users/user_list.html', context)


@login_required
def patient_create_view(request):
    """
    Vista para crear un nuevo paciente.
    Acceso: Médicos radiólogos y técnicos de salud
    """
    # Solo médicos y técnicos pueden crear pacientes
    if request.user.rol not in ['MEDICO_RADIOLOGO', 'TECNICO_SALUD']:
        messages.error(request, 'No tienes permisos para crear pacientes.')
        return redirect('users:user_dashboard')
    
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                # Crear paciente
                patient = form.save(commit=False)
                patient.created_by = request.user
                patient.save()
                
                # Registrar log
                Log.objects.create(
                    user=request.user,
                    accion='USER_CREATED',
                    nivel='INFO',
                    descripcion=f'Paciente {patient.get_full_name()} creado por {request.user.get_full_name()}',
                )
                
                messages.success(
                    request,
                    f'Paciente {patient.get_full_name()} registrado correctamente.'
                )
                return redirect('users:user_dashboard')
            
            except Exception as e:
                messages.error(request, f'Error al crear paciente: {str(e)}')
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PatientRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Crear Nuevo Paciente',
    }
    return render(request, 'users/patient_create.html', context)


@login_required
def user_create_view(request):
    """
    Vista para crear un usuario desde el panel de administración.
    """
    # Solo administradores pueden crear usuarios
    if request.user.rol != 'ADMINISTRADOR':
        messages.error(request, 'No tienes permisos para crear usuarios.')
        return redirect('users:admin_dashboard')

    roles = User.ROLES

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        identificacion = request.POST.get('identificacion', '').strip() or None
        email = request.POST.get('email', '').strip()
        rol = request.POST.get('rol') or 'TECNICO_SALUD'
        estado = True if request.POST.get('estado') in ['on', 'true', 'True', '1'] else False

        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'identificacion': identificacion,
            'email': email,
            'rol': rol,
            'estado': estado,
        }

        # Validaciones básicas
        if not (first_name and last_name and email and rol):
            messages.error(request, 'Por favor completa los campos requeridos.')
            return render(request, 'users/user_create.html', {
                'form_data': form_data,
                'roles': roles,
            })

        # Usar la identificación como contraseña temporal si está disponible
        if identificacion:
            temp_password = identificacion
            must_change = True
        else:
            temp_password = get_random_string(10)
            must_change = False

        try:
            user = User.objects.create_user(
                email=email,
                password=temp_password,
                first_name=first_name,
                last_name=last_name,
                identificacion=identificacion,
                rol=rol,
                estado=estado,
                must_change_password=must_change,
            )

            # Enviar email con contraseña temporal
            try:
                subject = 'Bienvenido al Sistema de Diagnóstico IA'
                context = {
                    'nombre': user.get_full_name(),
                    'email': user.email,
                    'password': temp_password,
                    'rol': user.get_rol_display(),
                }
                html_message = render_to_string('emails/welcome_email.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email='noreply@diagnostico-ia.com',
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                email_enviado = True
            except Exception as email_error:
                email_enviado = False
                print(f"Error al enviar email: {email_error}")

            # Registrar log
            Log.objects.create(
                user=request.user,
                accion='USER_CREATED',
                nivel='INFO',
                descripcion=f'Usuario {user.get_full_name()} creado por {request.user.get_full_name()}',
            )

            if email_enviado:
                messages.success(request, f'Usuario creado correctamente. Se envió un email con las credenciales a {user.email}')
            else:
                messages.warning(request, f'Usuario creado pero no se pudo enviar el email. Contraseña temporal: {temp_password}')
            
            return redirect('users:admin_dashboard')

        except Exception as e:
            messages.error(request, f'Error al crear usuario: {e}')
            return render(request, 'users/user_create.html', {
                'form_data': form_data,
                'roles': roles,
            })

    # GET
    context = {
        'form_data': {},
        'roles': roles,
    }
    return render(request, 'users/user_create.html', context)


@login_required
def change_password_view(request):
    """
    Vista para que los usuarios cambien su contraseña.
    """
    if request.method == 'POST':
        # Si el usuario está forzado a cambiar contraseña, no pedimos la actual
        if getattr(request.user, 'must_change_password', False):
            new_password = request.POST.get('new_password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()

            if not new_password:
                messages.error(request, 'Debes ingresar una nueva contraseña.')
                return render(request, 'users/change_password.html')

            if new_password != confirm_password:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'users/change_password.html')

            if len(new_password) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                return render(request, 'users/change_password.html')

            try:
                request.user.set_password(new_password)
                # Desactivar la bandera de cambio obligatorio
                request.user.must_change_password = False
                request.user.save()

                Log.objects.create(
                    user=request.user,
                    accion='PASSWORD_CHANGE',
                    nivel='INFO',
                    descripcion=f'Cambio de contraseña forzado por primera vez',
                )

                messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
                return redirect('users:profile')

            except Exception as e:
                messages.error(request, f'Error al cambiar contraseña: {str(e)}')
                return render(request, 'users/change_password.html')

        # Flujo normal: pedimos la contraseña actual
        current_password = request.POST.get('current_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Validaciones
        if not current_password:
            messages.error(request, 'Debes ingresar tu contraseña actual.')
            return render(request, 'users/change_password.html')

        if not new_password:
            messages.error(request, 'Debes ingresar una nueva contraseña.')
            return render(request, 'users/change_password.html')

        if new_password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'users/change_password.html')

        # Verificar contraseña actual
        if not request.user.check_password(current_password):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return render(request, 'users/change_password.html')

        # Validar que la nueva contraseña sea diferente
        if request.user.check_password(new_password):
            messages.error(request, 'La nueva contraseña debe ser diferente a la actual.')
            return render(request, 'users/change_password.html')

        # Validar longitud mínima
        if len(new_password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'users/change_password.html')

        try:
            # Cambiar contraseña
            request.user.set_password(new_password)
            request.user.save()

            # Registrar cambio en logs
            Log.objects.create(
                user=request.user,
                accion='PASSWORD_CHANGE',
                nivel='INFO',
                descripcion=f'Cambio de contraseña realizado por el usuario',
            )

            messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
            return redirect('users:profile')

        except Exception as e:
            messages.error(request, f'Error al cambiar contraseña: {str(e)}')
            return render(request, 'users/change_password.html')

    # GET
    return render(request, 'users/change_password.html')

def get_admin_stats():
    """
    Obtiene estadísticas generales del sistema para el admin
    """
    stats = {
        'total_usuarios': User.objects.filter(is_active=True).count(),
        'total_medicos': User.objects.filter(rol='MEDICO_RADIOLOGO', is_active=True).count(),
        'total_tecnicos': User.objects.filter(rol='TECNICO_SALUD', is_active=True).count(),
        'total_diagnosticos': 0,  # TODO: Implementar cuando exista el modelo
        'total_imagenes': 0,  # TODO: Implementar cuando exista el modelo
        'precision_sistema': '96.8',  # Puede venir de un modelo de configuración
    }
    
    return stats

def get_recent_users(limit=5):
    """
    Obtiene los usuarios más recientes del sistema
    """
    return User.objects.filter(
        is_active=True
    ).order_by('-fecha_registro')[:limit]

def get_system_activities():
    """
    Obtiene las actividades recientes del sistema
    """
    # Datos de ejemplo - implementar con un modelo de logs real
    activities = [
        {
            'icon': '👤',
            'type': 'primary',
            'title': 'Nuevo usuario registrado',
            'description': 'Dr. María González - Médico Radiólogo',
            'time': 'Hace 30 minutos',
            'level': 'info',
            'level_text': 'Info'
        },
        {
            'icon': '📊',
            'type': 'success',
            'title': 'Sistema actualizado',
            'description': 'Modelo de IA actualizado a versión 2.1',
            'time': 'Hace 2 horas',
            'level': 'success',
            'level_text': 'Éxito'
        },
        {
            'icon': '⚠️',
            'type': 'warning',
            'title': 'Mantenimiento programado',
            'description': 'El sistema se actualizará el 25 de noviembre',
            'time': 'Hace 1 día',
            'level': 'warning',
            'level_text': 'Advertencia'
        },
        {
            'icon': '✅',
            'type': 'info',
            'title': 'Backup completado',
            'description': 'Backup diario realizado exitosamente',
            'time': 'Hace 1 día',
            'level': 'success',
            'level_text': 'Éxito'
        }
    ]
    
    return activities
