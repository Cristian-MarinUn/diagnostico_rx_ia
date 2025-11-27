import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostico_ia_project.settings')
django.setup()

from authentication.models import User

print('=' * 70)
print('ELIMINANDO TODOS LOS USUARIOS')
print('=' * 70)

count_deleted = User.objects.all().delete()[0]
print(f'Se eliminaron {count_deleted} usuarios')

print('=' * 70)
print('CREANDO NUEVOS USUARIOS CON DATOS COMPLETOS')
print('=' * 70)

nuevos_usuarios = [
    # Administrador
    {
        'email': 'admin@hospital.com',
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'identificacion': '1087654321',
        'telefono': '+573001234567',
        'rol': 'ADMINISTRADOR',
        'password': 'AdminPass123!',
        'estado': True,
    },
    {
        'email': 'cmarinm@unal.edu.co',
        'first_name': 'Cristian',
        'last_name': 'Marín',
        'identificacion': '1087210926',
        'telefono': '+573124567890',
        'rol': 'ADMINISTRADOR',
        'password': 'AdminPass123!',
        'estado': True,
    },













    # Médicos Radiólogos
    {
        'email': 'medico@hospital.com',
        'first_name': 'Marta',
        'last_name': 'García',
        'identificacion': '1098765432',
        'telefono': '+573102345678',
        'rol': 'MEDICO_RADIOLOGO',
        'password': 'MedicoPass123!',
        'estado': True,
    },
    {
        'email': 'medico1@hospital.com',
        'first_name': 'María',
        'last_name': 'García',
        'identificacion': '1055555001',
        'telefono': '+573103456789',
        'rol': 'MEDICO_RADIOLOGO',
        'password': 'MedicoPass123!',
        'estado': True,
    },
    {
        'email': 'medico2@hospital.com',
        'first_name': 'Andrés',
        'last_name': 'Ramírez',
        'identificacion': '1055555002',
        'telefono': '+573104567890',
        'rol': 'MEDICO_RADIOLOGO',
        'password': 'MedicoPass123!',
        'estado': True,
    },
    {
        'email': 'medico3@hospital.com',
        'first_name': 'Laura',
        'last_name': 'Pineda',
        'identificacion': '1055555003',
        'telefono': '+573105678901',
        'rol': 'MEDICO_RADIOLOGO',
        'password': 'MedicoPass123!',
        'estado': True,
    },
    {
        'email': 'medico4@hospital.com',
        'first_name': 'Julián',
        'last_name': 'Mendoza',
        'identificacion': '1055555004',
        'telefono': '+573106789012',
        'rol': 'MEDICO_RADIOLOGO',
        'password': 'MedicoPass123!',
        'estado': True,
    },
    {
        'email': 'medico5@hospital.com',
        'first_name': 'Sofía',
        'last_name': 'Cortés',
        'identificacion': '1055555005',
        'telefono': '+573107890123',
        'rol': 'MEDICO_RADIOLOGO',
        'password': 'MedicoPass123!',
        'estado': True,
    },

















    
    # Técnicos de Salud
    {
        'email': 'tecnico@hospital.com',
        'first_name': 'Carlos',
        'last_name': 'Rodríguez',
        'identificacion': '1066666001',
        'telefono': '+573108901234',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico1@hospital.com',
        'first_name': 'Carlos',
        'last_name': 'Rodríguez',
        'identificacion': '1066666002',
        'telefono': '+573109012345',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico2@hospital.com',
        'first_name': 'Daniel',
        'last_name': 'Ruiz',
        'identificacion': '1066666003',
        'telefono': '+573110123456',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico3@hospital.com',
        'first_name': 'Ana',
        'last_name': 'Quintero',
        'identificacion': '1066666004',
        'telefono': '+573111234567',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico4@hospital.com',
        'first_name': 'Felipe',
        'last_name': 'Villalba',
        'identificacion': '1066666005',
        'telefono': '+573112345678',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico5@hospital.com',
        'first_name': 'Paula',
        'last_name': 'Santos',
        'identificacion': '1066666006',
        'telefono': '+573113456789',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico6@hospital.com',
        'first_name': 'Diego',
        'last_name': 'Martínez',
        'identificacion': '1066666007',
        'telefono': '+573114567890',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico7@hospital.com',
        'first_name': 'Valentina',
        'last_name': 'Lagos',
        'identificacion': '1066666008',
        'telefono': '+573115678901',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico8@hospital.com',
        'first_name': 'Sebastián',
        'last_name': 'Cárdenas',
        'identificacion': '1066666009',
        'telefono': '+573116789012',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico9@hospital.com',
        'first_name': 'Natalia',
        'last_name': 'Bermúdez',
        'identificacion': '1066666010',
        'telefono': '+573117890123',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico10@hospital.com',
        'first_name': 'Ricardo',
        'last_name': 'Herrera',
        'identificacion': '1066666011',
        'telefono': '+573118901234',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico11@hospital.com',
        'first_name': 'Camila',
        'last_name': 'Torres',
        'identificacion': '1066666012',
        'telefono': '+573119012345',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico12@hospital.com',
        'first_name': 'Jorge',
        'last_name': 'Salazar',
        'identificacion': '1066666013',
        'telefono': '+573120123456',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico13@hospital.com',
        'first_name': 'Melissa',
        'last_name': 'Valencia',
        'identificacion': '1066666014',
        'telefono': '+573121234567',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico14@hospital.com',
        'first_name': 'Oscar',
        'last_name': 'Gallego',
        'identificacion': '1066666015',
        'telefono': '+573122345678',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
    {
        'email': 'tecnico15@hospital.com',
        'first_name': 'Andrea',
        'last_name': 'Murillo',
        'identificacion': '1066666016',
        'telefono': '+573123456789',
        'rol': 'TECNICO_SALUD',
        'password': 'TecnicoPass123!',
        'estado': True,
    },
]

count_created = 0
for datos in nuevos_usuarios:
    try:
        password = datos.pop('password')
        usuario = User.objects.create_user(**datos, password=password)
        print(f'✓ {usuario.email} ({usuario.get_full_name()})')
        count_created += 1
    except Exception as e:
        print(f'✗ Error al crear usuario: {e}')

print('=' * 70)
print(f'Usuarios creados: {count_created}')
print('=' * 70)
