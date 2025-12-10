from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# Exportar PDF (CU-019)
@login_required
def export_diagnosis_pdf(request, diagnosis_id):
    diagnosis = get_object_or_404(AIDiagnosis, id=diagnosis_id)
    # Permisos: solo quien solicitó, validó, admin o superuser
    if not (request.user == diagnosis.requested_by or 
            request.user == diagnosis.validated_by or 
            request.user.is_superuser or
            request.user.rol == 'ADMINISTRADOR'):
        return HttpResponse('No tienes acceso a este diagnóstico.', status=403)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    # Encabezado
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, y, f"Diagnóstico IA #{diagnosis.id}")
    y -= 30
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Paciente: {diagnosis.patient.get_full_name()} ({diagnosis.patient.identification})")
    y -= 20
    p.drawString(50, y, f"Solicitado por: {diagnosis.requested_by.get_full_name()}")
    y -= 20
    p.drawString(50, y, f"Fecha: {diagnosis.created_at.strftime('%d/%m/%Y %H:%M')}")
    y -= 30

    # Resultado
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Resultado del Diagnóstico:")
    y -= 20
    p.setFont("Helvetica", 12)
    text = diagnosis.diagnosis_result or "Sin resultado"
    for line in text.splitlines():
        p.drawString(60, y, line)
        y -= 15
    y -= 20

    # Observaciones IA
    if diagnosis.ai_observations:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Observaciones de la IA:")
        y -= 20
        p.setFont("Helvetica", 12)
        for obs in diagnosis.ai_observations:
            p.drawString(60, y, f"- {obs}")
            y -= 15
        y -= 10

    # Confianza
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Nivel de confianza: {diagnosis.confidence_level or '-'}%")
    y -= 20

    # Comentarios del médico
    if diagnosis.doctor_comments:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Comentarios del Médico:")
        y -= 20
        p.setFont("Helvetica", 12)
        for line in diagnosis.doctor_comments.splitlines():
            p.drawString(60, y, line)
            y -= 15
        y -= 10

    # Pie de página
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 40, "Generado automáticamente por Diagnóstico IA - CU-019")

    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=diagnostico_{diagnosis.id}.pdf'
    return response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from django.db import models
from datetime import timedelta
import json

from .models import AIDiagnosis, DiagnosisLog
from users.models import Patient
from medical_images.models import MedicalImage


@login_required
def request_diagnosis_select(request):
    """Vista para seleccionar un paciente y solicitar diagnóstico"""
    
    # Verificar permiso: solo médicos y técnicos pueden solicitar
    if request.user.rol not in ['MEDICO_RADIOLOGO', 'TECNICO_SALUD']:
        messages.error(request, 'No tienes permiso para solicitar diagnósticos.')
        return redirect('users:user_dashboard')
    
    # Obtener lista de pacientes activos con imágenes
    patients = Patient.objects.filter(is_active=True).prefetch_related('medical_images').annotate(
        image_count=models.Count('medical_images', filter=models.Q(medical_images__is_active=True))
    ).filter(image_count__gt=0).order_by('-created_at')
    
    # Búsqueda
    search = request.GET.get('search', '')
    if search:
        patients = patients.filter(
            models.Q(identification__icontains=search) |
            models.Q(first_name__icontains=search) |
            models.Q(last_name__icontains=search) |
            models.Q(email__icontains=search)
        )
    
    context = {
        'title': 'Seleccionar Paciente - Solicitar Diagnóstico',
        'patients': patients,
        'search': search,
        'page': 'request_diagnosis_select'
    }
    
    return render(request, 'diagnostico/request_diagnosis_select.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def request_diagnosis(request, patient_id):
    """Vista para solicitar un diagnóstico de IA para un paciente"""
    
    patient = get_object_or_404(Patient, id=patient_id, is_active=True)
    
    # Verificar permiso: solo médicos y técnicos pueden solicitar
    if request.user.rol not in ['MEDICO_RADIOLOGO', 'TECNICO_SALUD']:
        messages.error(request, 'No tienes permiso para solicitar diagnósticos.')
    if request.method == "POST":
        selected_images = request.POST.getlist('selected_images')
        diagnosis = AIDiagnosis.objects.create(
            patient=patient,
            requested_by=request.user,
            status='PENDING',
            model_version='1.0.0'  # Versión de ejemplo
        )
        # Agregar imágenes
        images = MedicalImage.objects.filter(id__in=selected_images, patient=patient)
        diagnosis.images.set(images)
        # Crear log de auditoría
        DiagnosisLog.objects.create(
            diagnosis=diagnosis,
            action='CREATED',
            performed_by=request.user,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        messages.success(request, 'Diagnóstico solicitado exitosamente. Se está procesando...')
        return redirect('diagnostico:diagnosis_detail', diagnosis_id=diagnosis.id)
    
    # GET: Mostrar formulario
    images = MedicalImage.objects.filter(patient=patient, is_active=True).order_by('-study_date')
    
    context = {
        'title': f'Solicitar Diagnóstico - {patient.get_full_name()}',
        'patient': patient,
        'images': images,
        'page': 'request_diagnosis'
    }
    
    return render(request, 'diagnostico/request_diagnosis.html', context)


@login_required
def diagnosis_detail(request, diagnosis_id):
    """Vista para ver el detalle de un diagnóstico"""
    
    diagnosis = get_object_or_404(AIDiagnosis, id=diagnosis_id)
    
    # Verificar acceso: solo quien solicitó, quien validó o superusuarios
    if not (request.user == diagnosis.requested_by or 
            request.user == diagnosis.validated_by or 
            request.user.is_superuser or
            request.user.rol == 'ADMINISTRADOR'):
        messages.error(request, 'No tienes acceso a este diagnóstico.')
        return redirect('users:user_dashboard')
    
    images = diagnosis.images.all()
    logs = diagnosis.logs.all()
    
    # Simular procesamiento para diagnósticos en cola
    if diagnosis.status == 'PENDING':
        # En producción, aquí iría la lógica de procesamiento real con Celery/background tasks
        # Por ahora, simulamos que después de cierto tiempo se completa
        time_elapsed = (timezone.now() - diagnosis.created_at).total_seconds()
        if time_elapsed > 10:  # Después de 10 segundos, marca como completado
            diagnosis.status = 'COMPLETED'
            diagnosis.completed_at = timezone.now()
            diagnosis.processing_time = time_elapsed
            diagnosis.confidence_level = 85.5
            diagnosis.diagnosis_result = "Se detectan cambios mínimos en la estructura ósea. No se observan anomalías significativas. Se recomienda seguimiento rutinario."
            diagnosis.ai_observations = [
                "Alineación vertebral normal",
                "Espacios intervertebrales preservados",
                "No se identifican lesiones óseas agudas",
                "Estructuras de partes blandas dentro de los límites normales"
            ]
            diagnosis.save()
            
            DiagnosisLog.objects.create(
                diagnosis=diagnosis,
                action='COMPLETED',
                performed_by=request.user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
    
    context = {
        'title': f'Diagnóstico #{diagnosis.id}',
        'diagnosis': diagnosis,
        'images': images,
        'logs': logs,
        'page': 'diagnosis_detail'
    }
    
    return render(request, 'diagnostico/diagnosis_detail.html', context)


@login_required
@require_http_methods(["POST"])
def validate_diagnosis(request, diagnosis_id):
    """Endpoint para validar un diagnóstico completado"""
    
    diagnosis = get_object_or_404(AIDiagnosis, id=diagnosis_id)
    
    # Verificar permiso: solo médicos pueden validar
    if request.user.rol != 'MEDICO_RADIOLOGO':
        return JsonResponse({'success': False, 'error': 'Solo médicos pueden validar diagnósticos.'}, status=403)
    
    if diagnosis.status != 'COMPLETED':
        return JsonResponse({'success': False, 'error': 'Solo se pueden validar diagnósticos completados.'}, status=400)
    
    # Actualizar diagnóstico
    diagnosis.status = 'VALIDATED'
    diagnosis.validated_by = request.user
    diagnosis.validated_at = timezone.now()
    
    # Obtener comentarios si existen
    doctor_comments = request.POST.get('doctor_comments', '')
    if doctor_comments:
        diagnosis.doctor_comments = doctor_comments
    
    diagnosis.save()
    
    # Crear log
    DiagnosisLog.objects.create(
        diagnosis=diagnosis,
        action='VALIDATED',
        performed_by=request.user,
        details={'comments': doctor_comments},
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    messages.success(request, 'Diagnóstico validado exitosamente.')
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["POST"])
def discard_diagnosis(request, diagnosis_id):
    """Endpoint para descartar un diagnóstico"""
    
    diagnosis = get_object_or_404(AIDiagnosis, id=diagnosis_id)
    
    # Verificar permiso: solo médicos y administradores
    if request.user.rol not in ['MEDICO_RADIOLOGO', 'ADMINISTRADOR']:
        return JsonResponse({'success': False, 'error': 'Permiso denegado.'}, status=403)
    
    diagnosis.status = 'DISCARDED'
    diagnosis.save()
    
    # Crear log
    DiagnosisLog.objects.create(
        diagnosis=diagnosis,
        action='DISCARDED',
        performed_by=request.user,
        details={'reason': request.POST.get('reason', 'Sin especificar')},
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    messages.warning(request, 'Diagnóstico descartado.')
    return JsonResponse({'success': True})


@login_required
def check_status(request, diagnosis_id):
    """AJAX endpoint para verificar el estado de un diagnóstico"""
    
    diagnosis = get_object_or_404(AIDiagnosis, id=diagnosis_id)
    
    return JsonResponse({
        'status': diagnosis.status,
        'confidence_level': diagnosis.confidence_level,
        'processing_time': diagnosis.processing_time
    })


@login_required
def diagnosis_list(request):
    """Vista para listar diagnósticos del usuario"""
    
    # Filtrar según rol
    if request.user.rol == 'MEDICO_RADIOLOGO':
        diagnoses = AIDiagnosis.objects.filter(requested_by=request.user) | AIDiagnosis.objects.filter(validated_by=request.user)
    elif request.user.rol == 'TECNICO_SALUD':
        diagnoses = AIDiagnosis.objects.filter(requested_by=request.user)
    else:
        diagnoses = AIDiagnosis.objects.all()
    
    # Filtros opcionales
    status_filter = request.GET.get('status')
    if status_filter:
        diagnoses = diagnoses.filter(status=status_filter)
    
    diagnoses = diagnoses.distinct().order_by('-created_at')
    
    context = {
        'title': 'Diagnósticos',
        'diagnoses': diagnoses,
        'page': 'diagnosis_list'
    }
    
    return render(request, 'diagnostico/diagnosis_list.html', context)


@login_required
@require_http_methods(["GET"])
def autocomplete_patients(request):
    """API endpoint para autocompletado de pacientes"""
    
    # Verificar permiso
    if request.user.rol not in ['MEDICO_RADIOLOGO', 'TECNICO_SALUD']:
        return JsonResponse({'patients': []})
    
    # Obtener término de búsqueda
    query = request.GET.get('q', '').strip()
    
    if len(query) < 1:
        return JsonResponse({'patients': []})
    
    # Buscar pacientes activos (no filtramos por imágenes para permitir upload inicial)
    patients = Patient.objects.filter(
        is_active=True
    ).filter(
        models.Q(identification__icontains=query) |
        models.Q(first_name__icontains=query) |
        models.Q(last_name__icontains=query) |
        models.Q(email__icontains=query)
    ).order_by('last_name', 'first_name')[:10]
    
    # Construir respuesta
    results = []
    for patient in patients:
        # Obtener tipos de imágenes
        image_types = set()
        image_count = patient.medical_images.filter(is_active=True).count()
        for img in patient.medical_images.filter(is_active=True)[:5]:
            if img.study_type == 'RX':
                image_types.add('🩻 RX')
            elif img.study_type == 'TAC':
                image_types.add('🔬 TAC')
            elif img.study_type == 'RMN':
                image_types.add('🧲 RMN')
            elif img.study_type == 'ECO':
                image_types.add('📡 ECO')
            elif img.study_type == 'MAM':
                image_types.add('🎗️ MAM')
            else:
                image_types.add(f'📋 {img.study_type}')
        
        results.append({
            'id': patient.id,
            'name': patient.get_full_name(),
            'identification': patient.identification,
            'age': patient.get_age(),
            'gender': patient.get_gender_display_spanish(),
            'email': patient.email,
            'phone': patient.phone,
            'image_count': image_count,
            'image_types': ', '.join(sorted(list(image_types))[:3]) if image_types else 'Sin imágenes',
            'url': f'/diagnostico/request/{patient.id}/'
        })
    
    return JsonResponse({'patients': results})




@require_http_methods(["GET"])
@login_required
def get_patient_by_id(request, patient_id):
    """API endpoint para obtener un paciente específico por ID"""
    
    # Verificar permiso
    if request.user.rol not in ['MEDICO_RADIOLOGO', 'TECNICO_SALUD']:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    try:
        # Buscar por ID (que puede ser patient.id o patient.identification)
        try:
            patient = Patient.objects.get(id=patient_id, is_active=True)
        except Patient.DoesNotExist:
            patient = Patient.objects.get(identification=patient_id, is_active=True)
        
        # Obtener tipos de imágenes
        image_types = set()
        image_count = patient.medical_images.filter(is_active=True).count()
        for img in patient.medical_images.filter(is_active=True)[:5]:
            if img.study_type == 'RX':
                image_types.add('🩻 RX')
            elif img.study_type == 'TAC':
                image_types.add('🔬 TAC')
            elif img.study_type == 'RMN':
                image_types.add('🧲 RMN')
            elif img.study_type == 'ECO':
                image_types.add('📡 ECO')
            elif img.study_type == 'MAM':
                image_types.add('🎗️ MAM')
            else:
                image_types.add(f'📋 {img.study_type}')
        
        return JsonResponse({
            'patient': {
                'id': patient.id,
                'name': patient.get_full_name(),
                'identification': patient.identification,
                'age': patient.get_age(),
                'gender': patient.get_gender_display_spanish(),
                'email': patient.email,
                'phone': patient.phone,
                'image_count': image_count,
                'image_types': ', '.join(sorted(list(image_types))[:3]) if image_types else 'Sin imágenes',
            }
        })
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Paciente no encontrado'}, status=404)


def get_client_ip(request):
    """Obtiene la dirección IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
