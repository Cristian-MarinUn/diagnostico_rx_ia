from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import Session, Log

class SessionExpirationMiddleware(MiddlewareMixin):
    """Middleware para manejar expiración de sesiones - Flujo A2"""
    
    def process_request(self, request):
        if request.user.is_authenticated:
            # Verificar si existe una sesión activa
            try:
                session = Session.objects.filter(
                    user=request.user,
                    is_active=True
                ).first()
                
                if session:
                    # Verificar si la sesión ha expirado
                    if session.is_expired():
                        # Invalidar sesión
                        session.is_active = False
                        session.save()
                        
                        # Registrar expiración
                        Log.objects.create(
                            user=request.user,
                            accion='LOGOUT',
                            nivel='INFO',
                            descripcion='Sesión expirada automáticamente',
                            ip_address=self.get_client_ip(request)
                        )
                        
                        # Cerrar sesión
                        logout(request)
                        
                        # Redirigir al login
                        messages.warning(request, 'Tu sesión ha expirado.')
                        return redirect('authentication:login')
            
            except Exception as e:
                # Si hay error, continuar normalmente
                pass
        
        return None
    
    def get_client_ip(self, request):
        """Obtiene la IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip