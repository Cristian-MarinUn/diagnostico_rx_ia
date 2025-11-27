# ================================
# ARCHIVO: authentication/forms.py (agregar estos formularios)
# ================================

from django import forms
from django.core.exceptions import ValidationError
import re


class LoginForm(forms.Form):
    """Formulario de inicio de sesión con email, password y remember_me"""
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'correo@ejemplo.com',
            'autocomplete': 'email',
            'id': 'id_email'
        }),
        error_messages={
            'required': 'El correo electrónico es requerido.',
            'invalid': 'Ingresa un correo electrónico válido.'
        }
    )

    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password',
            'id': 'id_password'
        }),
        error_messages={
            'required': 'La contraseña es requerida.'
        }
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'id': 'id_remember_me'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if not email:
            raise ValidationError('El correo electrónico es requerido.')
        return email


class PasswordRecoveryForm(forms.Form):
    """
    Formulario para solicitar recuperación de contraseña
    """
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'correo@ejemplo.com',
            'autocomplete': 'email',
            'id': 'id_email'
        }),
        error_messages={
            'required': 'El correo electrónico es requerido.',
            'invalid': 'Ingresa un correo electrónico válido.'
        }
    )
    
    def clean_email(self):
        """
        Validación adicional del email
        """
        email = self.cleaned_data.get('email', '').lower().strip()
        
        if not email:
            raise ValidationError('El correo electrónico es requerido.')
        
        # Validar formato de email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError('Ingresa un correo electrónico válido.')
        
        return email


class PasswordResetForm(forms.Form):
    """
    Formulario para establecer nueva contraseña
    """
    new_password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Mínimo 8 caracteres',
            'autocomplete': 'new-password',
            'id': 'id_new_password',
            'name': 'new_password'
        }),
        error_messages={
            'required': 'La nueva contraseña es requerida.'
        }
    )
    
    confirm_password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirma tu contraseña',
            'autocomplete': 'new-password',
            'id': 'id_confirm_password',
            'name': 'confirm_password'
        }),
        error_messages={
            'required': 'Debes confirmar tu contraseña.'
        }
    )
    
    def clean_new_password(self):
        """
        Validar que la contraseña cumpla con las políticas de seguridad
        """
        password = self.cleaned_data.get('new_password')
        
        if not password:
            raise ValidationError('La contraseña es requerida.')
        
        # Longitud mínima
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        # Verificar que contiene mayúscula
        if not re.search(r'[A-Z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
        
        # Verificar que contiene minúscula
        if not re.search(r'[a-z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
        
        # Verificar que contiene número
        if not re.search(r'[0-9]', password):
            raise ValidationError('La contraseña debe contener al menos un número.')
        
        # Verificar que contiene carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('La contraseña debe contener al menos un carácter especial (!@#$%^&*).')
        
        return password
    
    def clean(self):
        """
        Validar que las contraseñas coincidan
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError({
                    'confirm_password': 'Las contraseñas no coinciden.'
                })
        
        return cleaned_data