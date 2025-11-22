from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
import re

class LoginForm(forms.Form):
    """Formulario de inicio de sesión - CU-001"""
    
    email = forms.EmailField(
        label='Correo electrónico o Usuario',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'autofocus': True,
        })
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
        })
    )
    
    remember_me = forms.BooleanField(
        label='Recordarme',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    
    def clean_email(self):
        """Valida que el email no esté vacío y tenga formato correcto"""
        email = self.cleaned_data.get('email')
        
        if not email:
            raise ValidationError('El correo electrónico es obligatorio')
        
        # Validar formato de email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError('Formato de correo electrónico inválido')
        
        return email.lower()
    
    def clean_password(self):
        """Valida que la contraseña no esté vacía y tenga longitud mínima"""
        password = self.cleaned_data.get('password')
        
        if not password:
            raise ValidationError('La contraseña es obligatoria')
        
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres')
        
        return password