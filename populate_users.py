import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostico_ia_project.settings')
django.setup()

from authentication.models import User

datos_usuarios = {
    'admin@hospital.com': ('1087654321', '+573001234567'),
    'medico@hospital.com': ('1098765432', '+573102345678'),
    'medico1@hospital.com': ('1055555001', '+573103456789'),
    'medico2@hospital.com': ('1055555002', '+573104567890'),
    'medico3@hospital.com': ('1055555003', '+573105678901'),
    'medico4@hospital.com': ('1055555004', '+573106789012'),
    'medico5@hospital.com': ('1055555005', '+573107890123'),
    'tecnico@hospital.com': ('1066666001', '+573108901234'),
    'tecnico1@hospital.com': ('1066666002', '+573109012345'),
    'tecnico2@hospital.com': ('1066666003', '+573110123456'),
    'tecnico3@hospital.com': ('1066666004', '+573111234567'),
    'tecnico4@hospital.com': ('1066666005', '+573112345678'),
    'tecnico5@hospital.com': ('1066666006', '+573113456789'),
    'tecnico6@hospital.com': ('1066666007', '+573114567890'),
    'tecnico7@hospital.com': ('1066666008', '+573115678901'),
    'tecnico8@hospital.com': ('1066666009', '+573116789012'),
    'tecnico9@hospital.com': ('1066666010', '+573117890123'),
    'tecnico10@hospital.com': ('1066666011', '+573118901234'),
    'tecnico11@hospital.com': ('1066666012', '+573119012345'),
    'tecnico12@hospital.com': ('1066666013', '+573120123456'),
    'tecnico13@hospital.com': ('1066666014', '+573121234567'),
    'tecnico14@hospital.com': ('1066666015', '+573122345678'),
    'tecnico15@hospital.com': ('1066666016', '+573123456789'),
    'cmarinm@unal.edu.co': ('1087210926', '+573124567890'),
}

print('=' * 70)
print('ACTUALIZANDO DATOS DE USUARIOS')
print('=' * 70)

count = 0
for email, (id_num, tel) in datos_usuarios.items():
    try:
        usuario = User.objects.get(email=email)
        usuario.identificacion = id_num
        usuario.telefono = tel
        usuario.save()
        print('OK: ' + email)
        count += 1
    except User.DoesNotExist:
        print('NO ENCONTRADO: ' + email)

print('=' * 70)
print('Actualizacion completada! ' + str(count) + ' usuarios actualizados.')
print('=' * 70)
