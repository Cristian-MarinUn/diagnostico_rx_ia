#!/usr/bin/env python
"""
Script para cargar pacientes de prueba consistentes en la base de datos.
Siempre carga los mismos pacientes con los mismos datos.

Ejecutar: python manage.py shell < seed_patients.py
o: python seed_patients.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostico_ia_project.settings')
django.setup()

from users.models import Patient
from authentication.models import User
from datetime import datetime, date

# Datos consistentes de pacientes de prueba
PATIENTS_DATA = [
    {
        'identification': '1001234567',
        'first_name': 'Roberto',
        'last_name': 'Sánchez',
        'date_of_birth': date(1965, 3, 15),
        'gender': 'M',
        'email': 'roberto.sanchez@email.com',
        'phone': '3001234567',
    },
    {
        'identification': '1002345678',
        'first_name': 'Isabel',
        'last_name': 'Flores',
        'date_of_birth': date(1972, 7, 22),
        'gender': 'F',
        'email': 'isabel.flores@email.com',
        'phone': '3012345678',
    },
    {
        'identification': '1003456789',
        'first_name': 'David',
        'last_name': 'Torres',
        'date_of_birth': date(1958, 11, 8),
        'gender': 'M',
        'email': 'david.torres@email.com',
        'phone': '3023456789',
    },
    {
        'identification': '1004567890',
        'first_name': 'Patricia',
        'last_name': 'Morales',
        'date_of_birth': date(1980, 5, 30),
        'gender': 'F',
        'email': 'patricia.morales@email.com',
        'phone': '3034567890',
    },
    {
        'identification': '1005678901',
        'first_name': 'Miguel',
        'last_name': 'Ramírez',
        'date_of_birth': date(1976, 2, 14),
        'gender': 'M',
        'email': 'miguel.ramirez@email.com',
        'phone': '3045678901',
    },
    {
        'identification': '1006789012',
        'first_name': 'Carmen',
        'last_name': 'González',
        'date_of_birth': date(1969, 9, 25),
        'gender': 'F',
        'email': 'carmen.gonzalez@email.com',
        'phone': '3056789012',
    },
    {
        'identification': '1007890123',
        'first_name': 'Fernando',
        'last_name': 'Hernández',
        'date_of_birth': date(1955, 12, 3),
        'gender': 'M',
        'email': 'fernando.hernandez@email.com',
        'phone': '3067890123',
    },
    {
        'identification': '1008901234',
        'first_name': 'Laura',
        'last_name': 'Díaz',
        'date_of_birth': date(1985, 4, 18),
        'gender': 'F',
        'email': 'laura.diaz@email.com',
        'phone': '3078901234',
    },
    {
        'identification': '1009012345',
        'first_name': 'Andrés',
        'last_name': 'Castillo',
        'date_of_birth': date(1970, 10, 7),
        'gender': 'M',
        'email': 'andres.castillo@email.com',
        'phone': '3089012345',
    },
    {
        'identification': '1010123456',
        'first_name': 'Silvia',
        'last_name': 'Martín',
        'date_of_birth': date(1962, 6, 19),
        'gender': 'F',
        'email': 'silvia.martin@email.com',
        'phone': '3090123456',
    },
]

def seed_patients():
    """Carga los pacientes de prueba si no existen"""
    
    # Obtener un usuario creador (médico o técnico)
    creator = User.objects.filter(rol__in=['MEDICO_RADIOLOGO', 'TECNICO_SALUD']).first()
    
    if not creator:
        print("❌ ERROR: No hay usuarios médicos o técnicos en el sistema.")
        print("   Por favor, ejecuta primero: python seed_users.py\n")
        return
    
    created_count = 0
    updated_count = 0
    existing_count = 0
    
    print("\n" + "="*70)
    print("CARGANDO PACIENTES DE PRUEBA CONSISTENTES")
    print("="*70 + "\n")
    
    for patient_data in PATIENTS_DATA:
        identification = patient_data['identification']
        
        try:
            # Buscar paciente existente
            patient = Patient.objects.get(identification=identification)
            
            # Actualizar datos
            patient.first_name = patient_data['first_name']
            patient.last_name = patient_data['last_name']
            patient.date_of_birth = patient_data['date_of_birth']
            patient.gender = patient_data['gender']
            patient.email = patient_data['email']
            patient.phone = patient_data['phone']
            patient.is_active = True
            patient.save()
            
            print(f"✏️  ACTUALIZADO: {patient.get_full_name()}")
            print(f"    Identificación: {identification}")
            print(f"    Edad: {patient.get_age()} años")
            print(f"    Email: {patient_data['email']}\n")
            updated_count += 1
            
        except Patient.DoesNotExist:
            # Crear nuevo paciente
            patient = Patient.objects.create(
                identification=identification,
                first_name=patient_data['first_name'],
                last_name=patient_data['last_name'],
                date_of_birth=patient_data['date_of_birth'],
                gender=patient_data['gender'],
                email=patient_data['email'],
                phone=patient_data['phone'],
                created_by=creator,
                is_active=True,
            )
            
            age = patient.get_age()
            print(f"✅ CREADO: {patient.get_full_name()}")
            print(f"    Identificación: {identification}")
            print(f"    Edad: {age} años")
            print(f"    Email: {patient_data['email']}")
            print(f"    Teléfono: {patient_data['phone']}\n")
            created_count += 1
    
    # Resumen final
    total_patients = Patient.objects.filter(is_active=True).count()
    
    print("="*70)
    print("RESUMEN")
    print("="*70)
    print(f"✅ Pacientes creados: {created_count}")
    print(f"✏️  Pacientes actualizados: {updated_count}")
    print(f"📊 Total de pacientes en sistema: {total_patients}")
    print("\n📋 PACIENTES CARGADOS:")
    print("-" * 70)
    
    for patient in Patient.objects.filter(is_active=True).order_by('last_name', 'first_name'):
        age = patient.get_age()
        gender = patient.get_gender_display_spanish()
        print(f"  • {patient.get_full_name():<30} ({age} años, {gender})")
        print(f"    ID: {patient.identification}")
        print(f"    Email: {patient.email}\n")
    
    print("="*70 + "\n")

if __name__ == '__main__':
    seed_patients()
