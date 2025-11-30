import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostico_ia_project.settings')
django.setup()

from authentication.models import User

usuarios = User.objects.all()
print('=' * 70)
print("USUARIOS EN EL SISTEMA")
print('=' * 70)

for u in usuarios:
    print(f"Email: {u.email}")
    print(f"  - Nombre: {u.first_name}")
    print(f"  - Apellido: {u.last_name}")
    print(f"  - Identificación: {u.identificacion if u.identificacion else 'VACÍO'}")
    print(f"  - Teléfono: {u.telefono if u.telefono else 'VACÍO'}")
    print(f"  - Rol: {u.rol}")
    print(f"  - Estado: {'Activo' if u.estado else 'Inactivo'}")
    print('-' * 70)
