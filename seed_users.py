#!/usr/bin/env python
"""
Script para cargar usuarios de prueba consistentes en la base de datos.
Siempre carga los mismos usuarios con los mismos datos.

Ejecutar: python manage.py shell < seed_users.py
o: python seed_users.py
"""

import os
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostico_ia_project.settings')
django.setup()

from authentication.models import User

# Datos consistentes de usuarios de prueba
USERS_DATA = [
    {
        'email': 'medico1@hospital.com',
        'first_name': 'Carlos',
        'last_name': 'García',
        'identificacion': '1000000001',
        'telefono': '3001000001',
        'rol': 'MEDICO_RADIOLOGO',
        'is_active': True,
    },
    {
        'email': 'medico2@hospital.com',
        'first_name': 'María',
        'last_name': 'Rodríguez',
        'identificacion': '1000000002',
        'telefono': '3001000002',
        'rol': 'MEDICO_RADIOLOGO',
        'is_active': True,
    },
    {
        'email': 'tecnico1@hospital.com',
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'identificacion': '1000000003',
        'telefono': '3001000003',
        'rol': 'TECNICO_SALUD',
        'is_active': True,
    },
    {
        'email': 'tecnico2@hospital.com',
        'first_name': 'Ana',
        'last_name': 'López',
        'identificacion': '1000000004',
        'telefono': '3001000004',
        'rol': 'TECNICO_SALUD',
        'is_active': True,
    },
    {
        'email': 'admin@hospital.com',
        'first_name': 'Pedro',
        'last_name': 'Martínez',
        'identificacion': '1000000005',
        'telefono': '3001000005',
        'rol': 'ADMINISTRADOR',
        'is_active': True,
    },
]

PASSWORD = 'Test1234!'

def create_users():
    """Crea los usuarios de prueba si no existen"""
    created_count = 0
    updated_count = 0
    
    print("\n" + "="*70)
    print("CARGANDO USUARIOS DE PRUEBA CONSISTENTES")
    print("="*70 + "\n")
    
    for user_data in USERS_DATA:
        email = user_data['email']
        identificacion = user_data['identificacion']
        
        try:
            # Buscar usuario existente
            user = User.objects.get(email=email)
            
            # Actualizar datos si es necesario
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.identificacion = user_data['identificacion']
            user.telefono = user_data['telefono']
            user.rol = user_data['rol']
            user.estado = user_data['is_active']
            user.save()
            
            print(f"✏️  ACTUALIZADO: {user.get_full_name()}")
            print(f"    Email: {email}")
            print(f"    Identificación: {identificacion}")
            print(f"    Rol: {user_data['rol']}")
            print(f"    Estado: {'Activo ✓' if user.estado else 'Inactivo ✗'}\n")
            updated_count += 1
            
        except User.DoesNotExist:
            # Crear nuevo usuario
            user = User.objects.create_user(
                email=email,
                password=PASSWORD,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                identificacion=user_data['identificacion'],
                telefono=user_data['telefono'],
                rol=user_data['rol'],
                estado=user_data['is_active'],
            )
            
            print(f"✅ CREADO: {user.get_full_name()}")
            print(f"    Email: {email}")
            print(f"    Identificación: {identificacion}")
            print(f"    Rol: {user_data['rol']}")
            print(f"    Contraseña: {PASSWORD}")
            print(f"    Estado: {'Activo ✓' if user.estado else 'Inactivo ✗'}\n")
            created_count += 1
    
    # Resumen final
    print("="*70)
    print("RESUMEN")
    print("="*70)
    print(f"✅ Usuarios creados: {created_count}")
    print(f"✏️  Usuarios actualizados: {updated_count}")
    print(f"📊 Total de usuarios en sistema: {User.objects.filter(estado=True).count()}")
    print("\n📋 USUARIOS DISPONIBLES:")
    print("-" * 70)
    
    for user in User.objects.filter(estado=True).order_by('rol', 'email'):
        rol_display = dict(User.ROLES).get(user.rol, user.rol)
        print(f"  • {user.get_full_name():<30} ({rol_display})")
        print(f"    Email: {user.email}")
        print(f"    Identificación: {user.identificacion}\n")
    
    print("="*70)
    print(f"\n🔐 Contraseña de todos los usuarios: {PASSWORD}\n")
    print("="*70 + "\n")

if __name__ == '__main__':
    create_users()
