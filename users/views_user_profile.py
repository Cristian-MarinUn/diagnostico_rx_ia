from django.shortcuts import render, get_object_or_404
from authentication.models import User

def user_profile_view(request, user_id):
    """
    Vista para visualizar el perfil de un usuario específico (solo para administradores)
    """
    if not request.user.is_authenticated or request.user.rol != 'ADMINISTRADOR':
        # Solo administradores pueden ver perfiles de otros usuarios
        return render(request, '403.html', status=403)

    user = get_object_or_404(User, id=user_id)
    user_data = {
        'nombre_completo': user.get_full_name(),
        'rol': user.get_rol_display(),
        'email': user.email,
        'identificacion': getattr(user, 'identificacion', ''),
        'telefono': getattr(user, 'telefono', ''),
        'fecha_registro': user.fecha_registro if hasattr(user, 'fecha_registro') else None,
    }
    context = {
        'user': user,
        'user_data': user_data,
    }
    return render(request, 'users/profile.html', context)
