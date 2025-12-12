from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import User
from django.contrib import messages
from django import forms


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'rol', 'identificacion', 'telefono', 'estado']
        labels = {
            'estado': 'Estado',
        }
        widgets = {
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }


def admin_user_edit_view(request, user_id):
    if not request.user.is_authenticated or request.user.rol != 'ADMINISTRADOR':
        return render(request, '403.html', status=403)

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('users:user_profile', user_id=user.id)
    else:
        form = AdminUserEditForm(instance=user)

    context = {
        'form': form,
        'user_obj': user,
    }
    return render(request, 'users/admin_user_edit.html', context)
