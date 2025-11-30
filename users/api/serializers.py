from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
import re

User = get_user_model()

class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar información del perfil del usuario.
    Permite modificar solo campos permitidos.
    """
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    
    telefono = serializers.CharField(
        validators=[phone_regex],
        max_length=17,
        required=False,
        allow_blank=True,
        help_text="Número de teléfono de contacto"
    )
    
    foto_perfil = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text="Imagen de perfil (JPG, PNG, WEBP)"
    )
    
    class Meta:
        model = User
        fields = ['nombre_completo', 'telefono', 'foto_perfil']
        
    def validate_nombre_completo(self, value):
        """Valida que el nombre completo tenga formato válido"""
        if value:
            value = value.strip()
            if len(value) < 3:
                raise serializers.ValidationError(
                    "El nombre debe tener al menos 3 caracteres"
                )
            if len(value) > 100:
                raise serializers.ValidationError(
                    "El nombre no puede exceder 100 caracteres"
                )
            # Validar que contenga solo letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
                raise serializers.ValidationError(
                    "El nombre solo puede contener letras y espacios"
                )
        return value
    
    def validate_foto_perfil(self, value):
        """Valida el archivo de imagen de perfil"""
        if value:
            # Validar tamaño máximo (5MB)
            max_size = 5 * 1024 * 1024  # 5MB en bytes
            if value.size > max_size:
                raise serializers.ValidationError(
                    "El archivo excede el tamaño máximo permitido (5MB)"
                )
            
            # Validar tipo de archivo
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            ext = value.name.lower().split('.')[-1]
            if f'.{ext}' not in valid_extensions:
                raise serializers.ValidationError(
                    "Formato de imagen no soportado. Use JPG, PNG o WEBP"
                )
            
            # Validar tipo MIME
            valid_mime_types = [
                'image/jpeg',
                'image/jpg', 
                'image/png',
                'image/webp'
            ]
            if value.content_type not in valid_mime_types:
                raise serializers.ValidationError(
                    "Tipo de archivo no válido"
                )
        
        return value
    
    def validate(self, attrs):
        """Validación a nivel de objeto"""
        # Verificar que se está enviando al menos un campo para actualizar
        if not any(attrs.values()):
            raise serializers.ValidationError(
                "Debe proporcionar al menos un campo para actualizar"
            )
        
        return attrs
    
    def update(self, instance, validated_data):
        """
        Actualiza solo los campos permitidos.
        Los campos protegidos (email, rol, estado) son ignorados.
        """
        # Lista de campos permitidos para actualización por el usuario
        allowed_fields = ['nombre_completo', 'telefono', 'foto_perfil']
        
        # Actualizar solo campos permitidos
        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        
        instance.save()
        return instance


class ProfileResponseSerializer(serializers.ModelSerializer):
    """
    Serializer para la respuesta después de actualizar el perfil.
    """
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'nombre_completo',
            'telefono',
            'foto_perfil',
            'rol',
            'rol_display',
            'estado',
            'estado_display',
            'fecha_registro',
            'ultimo_acceso'
        ]
        read_only_fields = fields


class RestrictedFieldsSerializer(serializers.Serializer):
    """
    Serializer para advertir sobre campos restringidos intentados.
    """
    restricted_fields = serializers.ListField(
        child=serializers.CharField(),
        help_text="Campos que no pueden ser modificados por el usuario"
    )
    message = serializers.CharField(
        help_text="Mensaje de advertencia"
    )


