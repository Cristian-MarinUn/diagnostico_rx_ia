#!/usr/bin/env python
"""
Script para crear pacientes de prueba en la base de datos.
Ejecutar: python manage.py shell < create_test_patients.py
o: python create_test_patients.py
"""

import os
import django
from datetime import datetime, timedelta
from random import choice, randint

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostico_ia_project.settings')
django.setup()

from users.models import Patient
from authentication.models import User

# Obtener un usuario creador (el primer médico o técnico disponible)
creator = User.objects.filter(rol__in=['MEDICO_RADIOLOGO', 'TECNICO_SALUD']).first()

if not creator:
    print("❌ No hay usuarios médicos o técnicos en el sistema. Por favor, crea uno primero.")
    exit(1)

print(f"✓ Usando usuario creador: {creator.get_full_name()} ({creator.rol})")

# Datos de prueba
FIRST_NAMES = [
    'Juan', 'María', 'Carlos', 'Ana', 'Pedro', 'Isabel',
    'Diego', 'Rosa', 'Miguel', 'Laura', 'Andrés', 'Carmen'
]

LAST_NAMES = [
    'García', 'Rodríguez', 'Martínez', 'López', 'Hernández', 'González',
    'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Morales'
]

GENDERS = ['M', 'F', 'O']

EMAILS_DOMAINS = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']

# Función para generar datos aleatorios
def generate_identification():
    """Genera un número de identificación único."""
    return str(randint(1000000000, 9999999999))

def generate_phone():
    """Genera un número de teléfono válido (7-15 dígitos)."""
    length = randint(7, 15)
    return ''.join([str(randint(0, 9)) for _ in range(length)])

def generate_email(first_name, last_name):
    """Genera un email único."""
    domain = choice(EMAILS_DOMAINS)
    base = f"{first_name.lower()}.{last_name.lower()}"
    random_num = randint(100, 999)
    return f"{base}{random_num}@{domain}"

def generate_date_of_birth():
    """Genera una fecha de nacimiento razonable (18-80 años)."""
    age = randint(18, 80)
    days_ago = age * 365 + randint(0, 365)
    return datetime.now().date() - timedelta(days=days_ago)

# Crear pacientes
print("\n📝 Creando 10 pacientes de prueba...\n")

patients_created = []

for i in range(1, 11):
    first_name = choice(FIRST_NAMES)
    last_name = choice(LAST_NAMES)
    gender = choice(GENDERS)
    
    # Asegurar identificación única
    identification = generate_identification()
    while Patient.objects.filter(identification=identification).exists():
        identification = generate_identification()
    
    patient = Patient(
        identification=identification,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=generate_date_of_birth(),
        gender=gender,
        email=generate_email(first_name, last_name),
        phone=generate_phone(),
        created_by=creator,
        is_active=True
    )
    patient.save()
    patients_created.append(patient)
    
    age = patient.get_age()
    gender_display = patient.get_gender_display_spanish()
    
    print(f"{i}. ✅ {patient.get_full_name()}")
    print(f"   - Identificación: {patient.identification}")
    print(f"   - Edad: {age} años | Género: {gender_display}")
    print(f"   - Email: {patient.email}")
    print(f"   - Teléfono: {patient.phone}")
    print(f"   - Creado por: {creator.get_full_name()}\n")

print(f"\n✅ {len(patients_created)} pacientes creados exitosamente.")
print(f"\n📊 Resumen:")
print(f"   - Total de pacientes en el sistema: {Patient.objects.count()}")
print(f"   - Pacientes activos: {Patient.objects.filter(is_active=True).count()}")
print(f"   - Edad promedio de nuevos pacientes: {sum(p.get_age() for p in patients_created) / len(patients_created):.1f} años")
