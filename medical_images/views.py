from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator


class UploadImageView(LoginRequiredMixin, TemplateView):
    """
    Vista para cargar imágenes médicas.
    Accesible solo para médicos radiólogos y técnicos de salud.
    """
    template_name = 'medical_images/upload.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = __import__('datetime').date.today().isoformat()
        return context


class ListImagesView(LoginRequiredMixin, TemplateView):
    """
    Vista para listar imágenes médicas.
    """
    template_name = 'medical_images/list.html'
    login_url = 'login'
