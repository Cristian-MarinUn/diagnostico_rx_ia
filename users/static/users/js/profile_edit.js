// ================================
// ARCHIVO: apps/users/static/users/js/profile_edit.js
// CU-008: JavaScript para Actualizar Información de Perfil
// ================================

(function() {
    'use strict';

    // ========== Variables Globales ==========
    const form = document.getElementById('profile-update-form');
    const submitBtn = document.getElementById('submit-btn');
    const loadingSpinner = document.getElementById('loading-spinner');
    const alertContainer = document.getElementById('alert-container');
    const photoInput = document.getElementById('foto_perfil');
    const currentPhoto = document.getElementById('current-photo');
    const deletePhotoBtn = document.getElementById('delete-photo-btn');
    const deletePhotoModal = new bootstrap.Modal(document.getElementById('deletePhotoModal'));
    const confirmDeleteBtn = document.getElementById('confirm-delete-photo');

    // API Endpoint
    const API_URL = '/api/profile/update/';
    const IMAGE_API_URL = '/api/profile/image/';

    // ========== Inicialización ==========
    document.addEventListener('DOMContentLoaded', function() {
        initializeEventListeners();
        loadProfileData();
    });

    // ========== Event Listeners ==========
    function initializeEventListeners() {
        // Submit del formulario
        form.addEventListener('submit', handleFormSubmit);

        // Preview de imagen al seleccionar
        photoInput.addEventListener('change', handlePhotoSelect);

        // Eliminar foto
        if (deletePhotoBtn) {
            deletePhotoBtn.addEventListener('click', () => deletePhotoModal.show());
        }
        
        confirmDeleteBtn.addEventListener('click', handlePhotoDelete);

        // Validación en tiempo real
        const inputs = form.querySelectorAll('input:not([readonly]):not([disabled])');
        inputs.forEach(input => {
            input.addEventListener('blur', () => validateField(input));
            input.addEventListener('input', () => clearFieldError(input));
        });
    }

    // ========== Cargar Datos del Perfil ==========
    async function loadProfileData() {
        try {
            const response = await fetch(API_URL, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Error al cargar los datos del perfil');
            }

            const data = await response.json();
            
            if (data.status === 'success') {
                populateForm(data.data);
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('Error al cargar los datos del perfil', 'danger');
        }
    }

    // ========== Poblar Formulario ==========
    function populateForm(data) {
        document.getElementById('nombre_completo').value = data.nombre_completo || '';
        document.getElementById('telefono').value = data.telefono || '';
        
        if (data.foto_perfil) {
            currentPhoto.src = data.foto_perfil;
        }
    }

    // ========== Manejo de Envío del Formulario ==========
    async function handleFormSubmit(e) {
        e.preventDefault();

        // Validar todos los campos
        if (!validateForm()) {
            showAlert('Por favor, corrige los errores en el formulario', 'warning');
            return;
        }

        // Mostrar loading
        setLoadingState(true);

        try {
            // Preparar FormData
            const formData = new FormData();
            
            const nombreCompleto = document.getElementById('nombre_completo').value.trim();
            const telefono = document.getElementById('telefono').value.trim();
            
            if (nombreCompleto) {
                formData.append('nombre_completo', nombreCompleto);
            }
            
            if (telefono) {
                formData.append('telefono', telefono);
            }

            // Agregar foto si se seleccionó una nueva
            if (photoInput.files.length > 0) {
                formData.append('foto_perfil', photoInput.files[0]);
            }

            // Enviar petición
            const response = await fetch(API_URL, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`,
                    'X-CSRFToken': getCSRFToken()
                },
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                showAlert(data.message, 'success');
                
                // Mostrar advertencia si hay campos restringidos
                if (data.warning) {
                    setTimeout(() => {
                        showAlert(data.warning.message, 'warning');
                    }, 2000);
                }

                // Actualizar la vista
                updateProfileView(data.data);

                // Redirigir después de 2 segundos
                setTimeout(() => {
                    window.location.href = '/profile/';
                }, 2000);
            } else {
                handleFormErrors(data);
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('Error al actualizar el perfil. Intenta más tarde', 'danger');
        } finally {
            setLoadingState(false);
        }
    }

    // ========== Validación del Formulario ==========
    function validateForm() {
        let isValid = true;
        
        const nombreCompleto = document.getElementById('nombre_completo');
        const telefono = document.getElementById('telefono');

        // Validar nombre completo
        if (!validateField(nombreCompleto)) {
            isValid = false;
        }

        // Validar teléfono (opcional)
        if (telefono.value.trim() && !validateField(telefono)) {
            isValid = false;
        }

        return isValid;
    }

    // ========== Validar Campo Individual ==========
    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        switch(field.id) {
            case 'nombre_completo':
                if (!value) {
                    isValid = false;
                    errorMessage = 'El nombre completo es obligatorio';
                } else if (value.length < 3) {
                    isValid = false;
                    errorMessage = 'El nombre debe tener al menos 3 caracteres';
                } else if (value.length > 100) {
                    isValid = false;
                    errorMessage = 'El nombre no puede exceder 100 caracteres';
                } else if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(value)) {
                    isValid = false;
                    errorMessage = 'El nombre solo puede contener letras y espacios';
                }
                break;

            case 'telefono':
                if (value && !/^\+?1?\d{9,15}$/.test(value)) {
                    isValid = false;
                    errorMessage = 'Formato de teléfono inválido. Ejemplo: +57300123456';
                }
                break;
        }

        if (!isValid) {
            markFieldInvalid(field, errorMessage);
        } else {
            markFieldValid(field);
        }

        return isValid;
    }

    // ========== Marcar Campo como Inválido ==========
    function markFieldInvalid(field, message) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        
        const feedback = field.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = message;
        }
    }

    // ========== Marcar Campo como Válido ==========
    function markFieldValid(field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    }

    // ========== Limpiar Error del Campo ==========
    function clearFieldError(field) {
        field.classList.remove('is-invalid', 'is-valid');
    }

    // ========== Manejo de Errores del Formulario ==========
    function handleFormErrors(data) {
        if (data.errors) {
            // Mostrar errores específicos de campos
            Object.keys(data.errors).forEach(fieldName => {
                const field = document.getElementById(fieldName);
                if (field) {
                    const errors = data.errors[fieldName];
                    const errorMessage = Array.isArray(errors) ? errors.join(', ') : errors;
                    markFieldInvalid(field, errorMessage);
                }
            });

            // Mostrar mensaje general
            showAlert(data.message || 'Error de validación en los campos', 'danger');
        } else {
            showAlert(data.message || 'Error al actualizar el perfil', 'danger');
        }
    }

    // ========== Manejo de Selección de Foto ==========
    function handlePhotoSelect(e) {
        const file = e.target.files[0];
        
        if (!file) return;

        // Validar tipo de archivo
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            showAlert('Formato de imagen no soportado. Use JPG, PNG o WEBP', 'danger');
            photoInput.value = '';
            return;
        }

        // Validar tamaño (5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
            showAlert('La imagen excede el tamaño máximo permitido (5MB)', 'danger');
            photoInput.value = '';
            return;
        }

        // Preview de la imagen
        const reader = new FileReader();
        reader.onload = function(e) {
            currentPhoto.src = e.target.result;
            showAlert('Imagen seleccionada. No olvides guardar los cambios', 'info');
        };
        reader.readAsDataURL(file);
    }

    // ========== Eliminar Foto de Perfil ==========
    async function handlePhotoDelete() {
        try {
            deletePhotoModal.hide();
            setLoadingState(true);

            const response = await fetch(IMAGE_API_URL, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`,
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                // Cambiar a imagen por defecto
                currentPhoto.src = '/static/images/default-avatar.png';
                
                // Ocultar botón de eliminar
                if (deletePhotoBtn) {
                    deletePhotoBtn.style.display = 'none';
                }

                showAlert(data.message, 'success');
            } else {
                showAlert(data.message || 'Error al eliminar la foto', 'danger');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('Error al eliminar la foto de perfil', 'danger');
        } finally {
            setLoadingState(false);
        }
    }

    // ========== Actualizar Vista del Perfil ==========
    function updateProfileView(data) {
        if (data.nombre_completo) {
            document.getElementById('nombre_completo').value = data.nombre_completo;
        }
        
        if (data.telefono) {
            document.getElementById('telefono').value = data.telefono;
        }
        
        if (data.foto_perfil) {
            currentPhoto.src = data.foto_perfil;
        }
    }

    // ========== Mostrar Alerta ==========
    function showAlert(message, type = 'info') {
        const alertHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-${getAlertIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        alertContainer.innerHTML = alertHTML;
        
        // Scroll hacia la alerta
        alertContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Auto-cerrar después de 5 segundos
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }

    // ========== Obtener Icono de Alerta ==========
    function getAlertIcon(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // ========== Estado de Carga ==========
    function setLoadingState(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            loadingSpinner.classList.remove('d-none');
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Guardando...';
        } else {
            submitBtn.disabled = false;
            loadingSpinner.classList.add('d-none');
            submitBtn.innerHTML = '<i class="fas fa-save me-2"></i>Guardar Cambios';
        }
    }

    // ========== Obtener Token de Autenticación ==========
    function getAuthToken() {
        // Obtener token del localStorage o sessionStorage
        return localStorage.getItem('access_token') || sessionStorage.getItem('access_token') || '';
    }

    // ========== Obtener CSRF Token ==========
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    // ========== Confirmar antes de salir si hay cambios ==========
    let formChanged = false;
    
    form.addEventListener('change', () => {
        formChanged = true;
    });

    window.addEventListener('beforeunload', (e) => {
        if (formChanged) {
            e.preventDefault();
            e.returnValue = '';
            return '';
        }
    });

    // Resetear flag al enviar
    form.addEventListener('submit', () => {
        formChanged = false;
    });

})();