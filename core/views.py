from django.shortcuts import render


def home(request):
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
