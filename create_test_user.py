#!/usr/bin/env python
"""
Script para crear un usuario de prueba y verificar que el email se envía
"""
import os
import django
import sys
import secrets
import string

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostico_ia_project.settings')
django.setup()

from authentication.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def generate_temp_password(length=10):
    """Generar contraseña temporal segura"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

def create_test_user():
    """Crear usuario de prueba con email"""
    try:
        print("=" * 60)
        print("CREAR USUARIO DE PRUEBA CON EMAIL")
        print("=" * 60)
        
        # Generar datos
        email = f"testing.user.{secrets.randbelow(10000)}@hospital.com"
        temp_password = generate_temp_password()
        identificacion = f"109{secrets.randbelow(100000000):08d}"  # Generar ID único
        
        print(f"\nCreando usuario con:")
        print(f"  - Email: {email}")
        print(f"  - Identificación: {identificacion}")
        print(f"  - Rol: TECNICO_SALUD (3)")
        print(f"  - Contraseña temporal: {temp_password}")
        
        # Crear usuario
        user = User.objects.create_user(
            email=email,
            password=temp_password,
            first_name='Usuario',
            last_name='Prueba',
            rol=3,  # TECNICO_SALUD
            identificacion=identificacion,
            telefono='+573001234567',
            estado=True
        )
        
        print(f"\n[OK] Usuario creado exitosamente")
        print(f"  - ID: {user.id}")
        print(f"  - Nombre: {user.get_full_name()}")
        
        # Enviar email
        print(f"\nEnviando email de bienvenida...")
        try:
            context = {
                'nombre': user.get_full_name(),
                'email': user.email,
                'password': temp_password,
                'rol': user.get_rol_display(),
            }
            html_message = render_to_string('emails/welcome_email.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject='Bienvenido al Sistema de Diagnóstico IA',
                message=plain_message,
                from_email='noreply@diagnostico-ia.com',
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"[OK] Email enviado exitosamente")
            
        except Exception as email_error:
            print(f"[ERROR] Error al enviar email: {email_error}")
            return False
        
        print("\n" + "=" * 60)
        print("USUARIO CREADO Y EMAIL ENVIADO EXITOSAMENTE")
        print("=" * 60)
        print(f"\nCredenciales de prueba:")
        print(f"  Email: {email}")
        print(f"  Contraseña: {temp_password}")
        print(f"  URL: http://localhost:8000/auth/login/")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error al crear usuario:")
        print(f"  {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = create_test_user()
    sys.exit(0 if success else 1)
