from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from authentication.models import User

@login_required
@user_passes_test(lambda u: u.rol == 'ADMINISTRADOR')
@require_POST
def deactivate_user(request):
    user_id = request.POST.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'ID de usuario no proporcionado.'}, status=400)
    try:
        user = User.objects.get(id=user_id)
        user.estado = False
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado.'}, status=404)
