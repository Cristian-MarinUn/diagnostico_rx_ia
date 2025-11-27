import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostico_ia_project.settings')
django.setup()

from authentication.models import User

# Datos a actualizar para cada usuario
datos_usuarios = {
    'admin@hospital.com': {
        'identificacion': '1087654321',
        'telefono': '+573001234567'
    },
    'medico@hospital.com': {
        'identificacion': '1098765432',
        'telefono': '+573102345678'
    },
    'medico1@hospital.com': {
        'identificacion': '1055555001',
        'telefono': '+573103456789'
    },
    'medico2@hospital.com': {
        'identificacion': '1055555002',
        'telefono': '+573104567890'
    },
    'medico3@hospital.com': {
        'identificacion': '1055555003',
        'telefono': '+573105678901'
    },
    'medico4@hospital.com': {
        'identificacion': '1055555004',
        'telefono': '+573106789012'
    },
    'medico5@hospital.com': {
        'identificacion': '1055555005',
        'telefono': '+573107890123'
    },
    'tecnico@hospital.com': {
        'identificacion': '1066666001',
        'telefono': '+573108901234'
    },
    'tecnico1@hospital.com': {
        'identificacion': '1066666002',
        'telefono': '+573109012345'
    },
    'tecnico2@hospital.com': {
        'identificacion': '1066666003',
        'telefono': '+573110123456'
    },
    'tecnico3@hospital.com': {
        'identificacion': '1066666004',
        'telefono': '+573111234567'
    },
    'tecnico4@hospital.com': {
        'identificacion': '1066666005',
        'telefono': '+573112345678'
    },
    'tecnico5@hospital.com': {
        'identificacion': '1066666006',
        'telefono': '+573113456789'
    },
    'tecnico6@hospital.com': {
        'identificacion': '1066666007',
        'telefono': '+573114567890'
    },
    'tecnico7@hospital.com': {
        'identificacion': '1066666008',
        'telefono': '+573115678901'
    },
    'tecnico8@hospital.com': {
        'identificacion': '1066666009',
        'telefono': '+573116789012'
    },
    'tecnico9@hospital.com': {
        'identificacion': '1066666010',
        'telefono': '+573117890123'
    },
    'tecnico10@hospital.com': {
        'identificacion': '1066666011',
        'telefono': '+573118901234'
    },
    'tecnico11@hospital.com': {
        'identificacion': '1066666012',
        'telefono': '+573119012345'
    },
    'tecnico12@hospital.com': {
        'identificacion': '1066666013',
        'telefono': '+573120123456'
    },
    'tecnico13@hospital.com': {
        'identificacion': '1066666014',
        'telefono': '+573121234567'
    },
    'tecnico14@hospital.com': {
        'identificacion': '1066666015',
        'telefono': '+573122345678'
    },
    'tecnico15@hospital.com': {
        'identificacion': '1066666016',
        'telefono': '+573123456789'
    },
    'cmarinm@unal.edu.co': {
        'identificacion': '1087210926',
        'telefono': '+573124567890'
    },
}

print('=' * 70)
print("ACTUALIZANDO DATOS DE USUARIOS")
print('=' * 70)

for email, datos in datos_usuarios.items():
    try:
        usuario = User.objects.get(email=email)
        usuario.identificacion = datos['identificacion']
        usuario.telefono = datos['telefono']
        usuario.save()
        print(f"✓ {email}")
        print(f"  - ID: {datos['identificacion']}")
        print(f"  - Tel: {datos['telefono']}")
    except User.DoesNotExist:
        print(f"✗ {email} - NO ENCONTRADO")

print('=' * 70)
print("¡Actualización completada!")
print('=' * 70)
