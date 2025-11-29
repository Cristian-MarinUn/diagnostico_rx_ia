"""
================================
ARCHIVO: diagnostico_ia/forms.py (agregar)
================================
Formularios para registro de pacientes
CU-025: Registrar Nuevo Paciente
"""

from django import forms
from .models import Patient
from django.core.exceptions import ValidationError
import re


class PatientRegistrationForm(forms.ModelForm):
    """Formulario para registrar un nuevo paciente"""
    
    # Campo de confirmación de email
    email_confirmation = forms.EmailField(
        required=False,
        label="Confirmar Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme el correo electrónico'
        })
    )
    
    class Meta:
        model = Patient
        fields = [
            'identification',
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'email',
            'phone'
        ]
        
        widgets = {
            'identification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de documento',
                'maxlength': '50',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres del paciente',
                'maxlength': '100',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos del paciente',
                'maxlength': '100',
                'required': True
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
                'max': '9999-12-31'  # Evita errores de fecha
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+57 300 123 4567',
                'maxlength': '20'
            })
        }
        
        labels = {
            'identification': 'Identificación *',
            'first_name': 'Nombres *',
            'last_name': 'Apellidos *',
            'date_of_birth': 'Fecha de Nacimiento *',
            'gender': 'Género *',
            'email': 'Correo Electrónico',
            'phone': 'Teléfono'
        }
        
        help_texts = {
            'identification': 'Documento de identidad único (CC, TI, CE, etc.)',
            'date_of_birth': 'Formato: DD/MM/AAAA',
            'phone': 'Incluir código de país si aplica'
        }
        
        error_messages = {
            'identification': {
                'unique': 'Ya existe un paciente registrado con este documento.',
                'required': 'El número de identificación es obligatorio.',
            },
            'first_name': {
                'required': 'Los nombres son obligatorios.',
            },
            'last_name': {
                'required': 'Los apellidos son obligatorios.',
            },
            'date_of_birth': {
                'required': 'La fecha de nacimiento es obligatoria.',
                'invalid': 'Formato de fecha inválido.',
            },
            'gender': {
                'required': 'Debe seleccionar un género.',
            }
        }
    
    def clean_identification(self):
        """Validación personalizada para identificación"""
        identification = self.cleaned_data.get('identification')
        
        if not identification:
            raise ValidationError('El número de identificación es obligatorio')
        
        # Eliminar espacios
        identification = identification.strip()
        
        # Validar que no esté vacío después de eliminar espacios
        if not identification:
            raise ValidationError('El número de identificación no puede estar vacío')
        
        # Validar longitud mínima
        if len(identification) < 5:
            raise ValidationError('El número de identificación debe tener al menos 5 caracteres')
        
        # Validar caracteres permitidos (letras, números, guiones)
        if not re.match(r'^[a-zA-Z0-9-]+$', identification):
            raise ValidationError('El número de identificación solo puede contener letras, números y guiones')
        
        # Verificar si ya existe (para creación)
        if not self.instance.pk:  # Solo al crear, no al editar
            if Patient.objects.filter(identification=identification).exists():
                raise ValidationError('Ya existe un paciente registrado con este documento')
        
        return identification.upper()  # Convertir a mayúsculas
    
    def clean_first_name(self):
        """Validación para nombres"""
        first_name = self.cleaned_data.get('first_name')
        
        if not first_name:
            raise ValidationError('Los nombres son obligatorios')
        
        first_name = first_name.strip()
        
        if len(first_name) < 2:
            raise ValidationError('Los nombres deben tener al menos 2 caracteres')
        
        # Validar que solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', first_name):
            raise ValidationError('Los nombres solo pueden contener letras y espacios')
        
        return first_name.title()  # Capitalizar cada palabra
    
    def clean_last_name(self):
        """Validación para apellidos"""
        last_name = self.cleaned_data.get('last_name')
        
        if not last_name:
            raise ValidationError('Los apellidos son obligatorios')
        
        last_name = last_name.strip()
        
        if len(last_name) < 2:
            raise ValidationError('Los apellidos deben tener al menos 2 caracteres')
        
        # Validar que solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            raise ValidationError('Los apellidos solo pueden contener letras y espacios')
        
        return last_name.title()  # Capitalizar cada palabra
    
    def clean_date_of_birth(self):
        """Validación para fecha de nacimiento"""
        from datetime import date, timedelta
        
        date_of_birth = self.cleaned_data.get('date_of_birth')
        
        if not date_of_birth:
            raise ValidationError('La fecha de nacimiento es obligatoria')
        
        # Validar que no sea fecha futura
        if date_of_birth > date.today():
            raise ValidationError('La fecha de nacimiento no puede ser en el futuro')
        
        # Validar edad mínima (recién nacido = 0 días)
        # No hay edad mínima, pero validar que no sea hoy mismo (podría ajustarse según políticas)
        
        # Validar edad máxima razonable (150 años)
        max_age_date = date.today() - timedelta(days=150*365)
        if date_of_birth < max_age_date:
            raise ValidationError('La fecha de nacimiento no puede ser mayor a 150 años atrás')
        
        return date_of_birth
    
    def clean_phone(self):
        """Validación para teléfono"""
        phone = self.cleaned_data.get('phone')
        
        if phone:
            phone = phone.strip()
            
            # Eliminar espacios y guiones para validación
            phone_digits = re.sub(r'[\s\-\(\)]', '', phone)
            
            # Validar formato básico (+ opcional, números)
            if not re.match(r'^\+?[0-9]+$', phone_digits):
                raise ValidationError('El teléfono solo puede contener números, espacios, guiones y el símbolo +')
            
            # Validar longitud (entre 7 y 15 dígitos)
            digits_only = re.sub(r'\D', '', phone_digits)
            if len(digits_only) < 7 or len(digits_only) > 15:
                raise ValidationError('El teléfono debe tener entre 7 y 15 dígitos')
            
            return phone
        
        return phone
    
    def clean_email(self):
        """Validación para email"""
        email = self.cleaned_data.get('email')
        
        if email:
            email = email.strip().lower()
            
            # Validar formato de email
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValidationError('Formato de correo electrónico inválido')
            
            return email
        
        return email
    
    def clean(self):
        """Validación cruzada de campos"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_confirmation = cleaned_data.get('email_confirmation')
        
        # Si se proporciona email, debe coincidir con la confirmación
        if email and email_confirmation:
            if email.lower() != email_confirmation.lower():
                raise ValidationError({
                    'email_confirmation': 'Los correos electrónicos no coinciden'
                })
        
        # Si se proporciona confirmación, debe haber email
        if email_confirmation and not email:
            raise ValidationError({
                'email': 'Debe ingresar el correo electrónico'
            })
        
        return cleaned_data


class PatientSearchForm(forms.Form):
    """Formulario para buscar pacientes"""
    
    search_query = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, apellido o identificación...',
            'autofocus': True
        }),
        label=''
    )
    
    search_type = forms.ChoiceField(
        required=False,
        choices=[
            ('all', 'Todos los campos'),
            ('identification', 'Identificación'),
            ('name', 'Nombre completo'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Buscar en',
        initial='all'
    )
    
    def clean_search_query(self):
        """Limpiar query de búsqueda"""
        query = self.cleaned_data.get('search_query')
        if query:
            return query.strip()
        return query


class PatientUpdateForm(forms.ModelForm):
    """Formulario para actualizar datos del paciente"""
    
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'email',
            'phone'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres del paciente'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos del paciente'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+57 300 123 4567'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # La identificación no se puede editar
        if self.instance.pk:
            self.fields['identification'] = forms.CharField(
                disabled=True,
                initial=self.instance.identification,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'
                }),
                label='Identificación'
            )