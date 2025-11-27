# ================================
# Tarea programada para cierre automático por inactividad
# ARCHIVO: authentication/tasks.py (NUEVO)
# ================================

from django.utils import timezone
from datetime import timedelta
from .models import Session, Log

class InactivityMonitor:
    """Monitor de inactividad - Flujo Alternativo A3"""
    
    @staticmethod
    def check_inactive_sessions():
        """
        Verifica y cierra sesiones inactivas
        Esta función debe ejecutarse periódicamente (cada 5-10 minutos)
        usando Celery, cron, o similar en producción
        """
        
        # Tiempo de inactividad permitido (30 minutos)
        inactivity_threshold = timezone.now() - timedelta(minutes=30)
        
        # Buscar sesiones activas pero inactivas
        inactive_sessions = Session.objects.filter(
            is_active=True,
            login_time__lt=inactivity_threshold
        )
        
        for session in inactive_sessions:
            # Invalidar sesión
            session.is_active = False
            session.save()
            
            # Registrar cierre automático
            Log.objects.create(
                user=session.user,
                accion='LOGOUT',
                nivel='INFO',
                descripcion='Sesión cerrada por inactividad (30 minutos)',
                datos_adicionales={
                    'login_time': str(session.login_time),
                    'auto_closed': True
                }
            )
        
        return inactive_sessions.count()
