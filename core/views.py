from django.shortcuts import render, redirect
from django.urls import reverse


def home(request):
	# Si el usuario está autenticado, redirigir al dashboard de usuarios
	if request.user.is_authenticated:
		# Si es administrador, enviarlo al admin dashboard
		if getattr(request.user, 'rol', None) == 'ADMINISTRADOR':
			return redirect(reverse('users:admin_dashboard'))
		return redirect(reverse('users:dashboard'))

	features = [
		{'icon': '🔬', 'title': 'Análisis de imágenes', 'description': 'Procesamiento y detección en radiografías.'},
		{'icon': '⚡', 'title': 'Resultados rápidos', 'description': 'Resultados preliminares en segundos.'},
		{'icon': '🔒', 'title': 'Privacidad', 'description': 'Manejo seguro de los datos del paciente.'},
	]
	context = {
		'title': 'Inicio',
		'features': features,
	}
	return render(request, 'core/home.html', context)
