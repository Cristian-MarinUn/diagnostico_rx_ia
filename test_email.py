#!/usr/bin/env python
"""
Script para probar el envío de emails en Django
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostico_ia_project.settings')
django.setup()

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def test_email_sending():
    """Probar envío de email con template HTML"""
    try:
        # Crear contexto de prueba
        context = {
            'nombre': 'Juan Pérez García',
            'email': 'test@hospital.com',
            'password': 'TempPass123!',
            'rol': 'Técnico de Salud',
        }
        
        print("=" * 60)
        print("PRUEBA DE ENVÍO DE EMAIL")
        print("=" * 60)
        print(f"\nContexto del email:")
        print(f"  - Nombre: {context['nombre']}")
        print(f"  - Email: {context['email']}")
        print(f"  - Rol: {context['rol']}")
        print(f"  - Contraseña: {context['password']}")
        
        # Renderizar template
        print(f"\nRenderizando template 'emails/welcome_email.html'...")
        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = strip_tags(html_message)
        
        print(f"[OK] Template renderizado correctamente")
        print(f"  - Contenido HTML: {len(html_message)} caracteres")
        print(f"  - Contenido texto plano: {len(plain_message)} caracteres")
        
        # Enviar email
        print(f"\nEnviando email...")
        result = send_mail(
            subject='Bienvenido al Sistema de Diagnóstico IA',
            message=plain_message,
            from_email='noreply@diagnostico-ia.com',
            recipient_list=['test@hospital.com'],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"[OK] Email enviado exitosamente")
        print(f"  - Resultado: {result} mensaje(s) enviado(s)")
        
        print("\n" + "=" * 60)
        print("PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error al enviar email:")
        print(f"  {type(e).__name__}: {str(e)}")
        print("\n" + "=" * 60)
        return False

if __name__ == '__main__':
    success = test_email_sending()
    sys.exit(0 if success else 1)
