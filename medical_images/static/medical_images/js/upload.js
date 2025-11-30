// ================================
// ARCHIVO: apps/medical_images/static/medical_images/js/upload.js
// CU-010: JavaScript para Cargar Imagen Médica
// ================================

(function() {
    'use strict';

    // ========== Variables Globales (referencias serán inicializadas tras DOMContentLoaded) ==========
    let form, uploadZone, fileInput, filePreview, submitBtn, alertContainer;
    // Búsqueda de pacientes
    let patientSearch, patientResults, selectedPatientCard, patientIdInput;
    // Contador de caracteres
    let descriptionTextarea, charCount;
    // Modals (instancias de bootstrap)
    let successModal, duplicateModal;
    
    // API Endpoints
    const API_UPLOAD_URL = '/api/images/upload/';
    const API_PATIENTS_URL = '/api/images/patients/';
    
    // Variables de estado
    let selectedPatient = null;
    let selectedFile = null;
    let searchTimeout = null;
    let currentObjectURL = null;

    // ========== Inicialización ==========
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar referencias a elementos del DOM ahora que están disponibles
        form = document.getElementById('upload-form');
        uploadZone = document.getElementById('upload-zone');
        fileInput = document.getElementById('image_file');
        filePreview = document.getElementById('file-preview');
        submitBtn = document.getElementById('submit-btn');
        alertContainer = document.getElementById('alert-container');

        patientSearch = document.getElementById('patient_search');
        patientResults = document.getElementById('patient-results');
        selectedPatientCard = document.getElementById('selected-patient');
        patientIdInput = document.getElementById('patient_id');

        descriptionTextarea = document.getElementById('description');
        charCount = document.getElementById('char-count');

        // Inicializar modales de bootstrap si están disponibles; crear stubs si no
        try {
            const successModalEl = document.getElementById('successModal');
            const duplicateModalEl = document.getElementById('duplicateModal');

            if (window.bootstrap && typeof bootstrap.Modal === 'function') {
                if (successModalEl) successModal = new bootstrap.Modal(successModalEl);
                if (duplicateModalEl) duplicateModal = new bootstrap.Modal(duplicateModalEl);

                // Bind events to toggle the hidden class so modals remain hidden in DOM until shown
                try {
                    if (successModalEl) {
                        successModalEl.addEventListener('show.bs.modal', () => successModalEl.classList.remove('hidden-modal'));
                        successModalEl.addEventListener('hidden.bs.modal', () => successModalEl.classList.add('hidden-modal'));
                    }
                    if (duplicateModalEl) {
                        duplicateModalEl.addEventListener('show.bs.modal', () => duplicateModalEl.classList.remove('hidden-modal'));
                        duplicateModalEl.addEventListener('hidden.bs.modal', () => duplicateModalEl.classList.add('hidden-modal'));
                    }
                } catch (evErr) {
                    // non-fatal if events can't be attached
                    console.warn('No se pudieron añadir listeners de eventos de modal:', evErr);
                }
            }

            // Si alguno no se creó, usar stubs que usan showAlert como fallback
            if (!successModal) {
                successModal = {
                    show: () => showAlert('Imagen cargada correctamente', 'success'),
                    hide: () => {}
                };
            }

            if (!duplicateModal) {
                duplicateModal = {
                    show: () => showAlert('Esta imagen ya existe en el sistema', 'warning'),
                    hide: () => {}
                };
            }
        } catch (err) {
            // En caso de error, usar stubs
            successModal = { show: () => showAlert('Imagen cargada correctamente', 'success'), hide: () => {} };
            duplicateModal = { show: () => showAlert('Esta imagen ya existe en el sistema', 'warning'), hide: () => {} };
            console.warn('Bootstrap modals not available, using stubs:', err);
        }

        initializeEventListeners();
        setTodayDate();
    });

    // ========== Event Listeners ==========
    function initializeEventListeners() {
        // Formulario
        form.addEventListener('submit', handleSubmit);
        
        // Drag & Drop
        uploadZone.addEventListener('click', handleUploadZoneClick);
        uploadZone.addEventListener('dragover', handleDragOver);
        uploadZone.addEventListener('dragleave', handleDragLeave);
        uploadZone.addEventListener('drop', handleDrop);

        // Handle cancel button to avoid beforeunload prompt
        const cancelBtn = document.getElementById('cancel-btn');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', function(e) {
                // Capture href before preventing default
                const href = this.getAttribute('href');
                e.preventDefault();
                // Try to remove any beforeunload handlers created elsewhere
                try { window.onbeforeunload = null; } catch (err) {}
                // Navigate to target
                window.location.href = href;
            });
        }
        
        // Handle search patient button click
        const searchPatientBtn = document.getElementById('search-patient-btn');
        if (searchPatientBtn) {
            searchPatientBtn.addEventListener('click', function(e) {
                e.preventDefault();
                const query = patientSearch.value.trim();
                if (query.length >= 2) {
                    searchPatients(query);
                } else {
                    showAlert('Ingresa al menos 2 caracteres para buscar', 'warning');
                }
            });
        }
        
        // Selección de archivo
        fileInput.addEventListener('change', handleFileSelect);
        
        // Helper: avoid double dialog when clicking label inside uploadZone
        function handleUploadZoneClick(e) {
            // If the click originated from the label (which already opens the file dialog), do nothing
            if (e.target.closest && e.target.closest('label[for="image_file"]')) return;
            // If clicking on an input/link/button inside the zone, ignore
            if (e.target.closest && (e.target.closest('input') || e.target.closest('a') || e.target.closest('button'))) return;
            fileInput.click();
        }
        
        // Búsqueda de pacientes
        patientSearch.addEventListener('input', handlePatientSearch);
        document.addEventListener('click', closePatientResults);
        
        // Contador de caracteres
        descriptionTextarea.addEventListener('input', updateCharCount);
        
        // Validación en tiempo real
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => validateField(input));
            input.addEventListener('input', () => clearFieldError(input));
        });
    }

    // ========== Drag & Drop ==========
    function handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.add('dragover');
    }

    function handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('dragover');
    }

    function handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect();
        }
    }

    // ========== Selección de Archivo ==========
    function handleFileSelect() {
        const file = fileInput.files[0];
        
        if (!file) return;
        
        // Validar archivo
        const validation = validateFile(file);
        if (!validation.valid) {
            showAlert(validation.message, 'danger');
            fileInput.value = '';
            return;
        }
        
        selectedFile = file;
        displayFilePreview(file);
    }

    function validateFile(file) {
        // Validar tamaño (500 MB)
        const maxSize = 500 * 1024 * 1024;
        if (file.size > maxSize) {
            return {
                valid: false,
                message: `El archivo excede el tamaño máximo permitido (500 MB). Tamaño actual: ${formatFileSize(file.size)}`
            };
        }
        
        // Validar extensión
        const allowedExtensions = ['.dcm', '.jpg', '.jpeg', '.png', '.tiff', '.tif'];
        const fileName = file.name.toLowerCase();
        const hasValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
        
        if (!hasValidExtension) {
            return {
                valid: false,
                message: `Formato de archivo no soportado. Formatos permitidos: ${allowedExtensions.join(', ')}`
            };
        }
        
        return { valid: true };
    }

    function displayFilePreview(file) {
        uploadZone.classList.add('d-none');
        filePreview.classList.remove('d-none');
        document.getElementById('file-name').textContent = file.name;
        document.getElementById('file-info').textContent = `${formatFileSize(file.size)} • ${file.type || 'Archivo médico'}`;

        // Mostrar miniatura si es una imagen estándar (jpg/png/tiff)
        const thumb = document.getElementById('file-thumbnail');
        const icon = filePreview.querySelector('.file-preview-icon');
        const isImage = (file.type && file.type.startsWith('image/')) || /\.(jpe?g|png|tiff?|gif)$/i.test(file.name);

        // Limpiar URL anterior si existe
        if (currentObjectURL) {
            URL.revokeObjectURL(currentObjectURL);
            currentObjectURL = null;
        }

        const largeImg = document.getElementById('file-large');
        const previewImageWrapper = document.getElementById('file-preview-image');

        if (isImage) {
            currentObjectURL = URL.createObjectURL(file);
            if (largeImg) {
                largeImg.src = currentObjectURL;
                // show large centered image wrapper
                if (previewImageWrapper) previewImageWrapper.classList.remove('d-none');
            }
            if (thumb) {
                thumb.src = currentObjectURL;
                thumb.classList.remove('d-none');
            }
            if (icon) icon.classList.add('d-none');
        } else {
            // hide image elements
            if (largeImg) {
                largeImg.src = '';
                if (previewImageWrapper) previewImageWrapper.classList.add('d-none');
            }
            if (thumb) thumb.classList.add('d-none');
            if (icon) icon.classList.remove('d-none');
        }
    }

    window.clearFile = function() {
        fileInput.value = '';
        selectedFile = null;
        uploadZone.classList.remove('d-none');
        filePreview.classList.add('d-none');
        document.getElementById('upload-progress-bar').classList.add('d-none');
        document.getElementById('progress-bar').style.width = '0%';

        // Limpiar miniatura si corresponde
        if (currentObjectURL) {
            URL.revokeObjectURL(currentObjectURL);
            currentObjectURL = null;
        }
        const thumb = document.getElementById('file-thumbnail');
        if (thumb) {
            thumb.src = '';
            thumb.classList.add('d-none');
        }
        const largeImg = document.getElementById('file-large');
        const previewImageWrapper = document.getElementById('file-preview-image');
        if (largeImg) {
            largeImg.src = '';
        }
        if (previewImageWrapper) previewImageWrapper.classList.add('d-none');
        const icon = document.querySelector('#file-preview .file-preview-icon');
        if (icon) icon.classList.remove('d-none');
    };

    // ========== Búsqueda de Pacientes ==========
    function handlePatientSearch(e) {
        const query = e.target.value.trim();
        
        clearTimeout(searchTimeout);
        
        if (query.length < 2) {
            patientResults.classList.remove('show');
            return;
        }
        
        searchTimeout = setTimeout(() => {
            searchPatients(query);
        }, 300);
    }

    async function searchPatients(query) {
        try {
            const response = await fetch(`${API_PATIENTS_URL}?search=${encodeURIComponent(query)}`, {
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`
                }
            });
            
            if (!response.ok) throw new Error('Error al buscar pacientes');
            
            const data = await response.json();
            displayPatientResults(data.data);
            
        } catch (error) {
            console.error('Error:', error);
            showAlert('Error al buscar pacientes', 'danger');
        }
    }

    function displayPatientResults(patients) {
        patientResults.innerHTML = '';
        
        if (patients.length === 0) {
            patientResults.innerHTML = '<div class="no-results">No se encontraron pacientes</div>';
            patientResults.classList.add('show');
            return;
        }
        
        patients.forEach(patient => {
            const item = document.createElement('div');
            item.className = 'patient-result-item';
            item.innerHTML = `
                <h6>${patient.nombre_completo}</h6>
                <p>ID: ${patient.identificacion} • Edad: ${patient.edad} años</p>
            `;
            
            item.addEventListener('click', () => selectPatient(patient));
            patientResults.appendChild(item);
        });
        
        patientResults.classList.add('show');
    }

    function selectPatient(patient) {
        selectedPatient = patient;
        patientIdInput.value = patient.id;
        
        // Mostrar paciente seleccionado
        selectedPatientCard.classList.remove('d-none');
        document.getElementById('selected-patient-name').textContent = patient.nombre_completo;
        document.getElementById('selected-patient-id').textContent = `ID: ${patient.identificacion}`;
        document.getElementById('selected-patient-age').textContent = `Edad: ${patient.edad} años • ${patient.genero === 'M' ? 'Masculino' : patient.genero === 'F' ? 'Femenino' : 'Otro'}`;
        
        // Limpiar búsqueda
        patientSearch.value = patient.nombre_completo;
        patientResults.classList.remove('show');
        
        // Limpiar error si existe
        clearFieldError(patientSearch);
    }

    window.clearPatient = function() {
        selectedPatient = null;
        patientIdInput.value = '';
        selectedPatientCard.classList.add('d-none');
        patientSearch.value = '';
    };

    function closePatientResults(e) {
        const searchBtn = document.getElementById('search-patient-btn');
        // Don't close if clicking on search input, results, or search button
        if (!patientSearch.contains(e.target) && !patientResults.contains(e.target) && !(searchBtn && searchBtn.contains(e.target))) {
            patientResults.classList.remove('show');
        }
    }

    // ========== Contador de Caracteres ==========
    function updateCharCount() {
        const count = descriptionTextarea.value.length;
        charCount.textContent = count;
        
        if (count > 500) {
            charCount.style.color = 'var(--danger-color)';
        } else {
            charCount.style.color = '';
        }
    }

    // ========== Validación del Formulario ==========
    function validateForm() {
        let isValid = true;
        
        // Validar paciente
        if (!selectedPatient) {
            markFieldInvalid(patientSearch, 'Debe seleccionar un paciente');
            isValid = false;
        }
        
        // Validar archivo
        if (!selectedFile) {
            showAlert('Debe seleccionar una imagen médica', 'warning');
            isValid = false;
        }
        
        // Validar tipo de estudio
        const studyType = document.getElementById('study_type');
        if (!studyType.value) {
            markFieldInvalid(studyType, 'Debe seleccionar el tipo de estudio');
            isValid = false;
        }
        
        // Validar fecha
        const studyDate = document.getElementById('study_date');
        if (!studyDate.value) {
            markFieldInvalid(studyDate, 'Debe ingresar la fecha del estudio');
            isValid = false;
        } else if (new Date(studyDate.value) > new Date()) {
            markFieldInvalid(studyDate, 'La fecha no puede ser futura');
            isValid = false;
        }
        
        return isValid;
    }

    function validateField(field) {
        if (field.hasAttribute('required') && !field.value) {
            markFieldInvalid(field, 'Este campo es obligatorio');
            return false;
        }
        
        clearFieldError(field);
        return true;
    }

    function markFieldInvalid(field, message) {
        field.classList.add('is-invalid');
        const feedback = field.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = message;
        }
        
        // Shake animation
        field.classList.add('shake');
        setTimeout(() => field.classList.remove('shake'), 500);
    }

    function clearFieldError(field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        const feedback = field.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = '';
        }
    }

    // ========== Submit del Formulario ==========
    async function handleSubmit(e) {
        e.preventDefault();
        
        // Limpiar alertas previas
        alertContainer.innerHTML = '';
        
        // Validar formulario
        if (!validateForm()) {
            showAlert('Por favor, complete todos los campos obligatorios', 'warning');
            return;
        }
        
        // Preparar FormData
        const formData = new FormData();
        formData.append('image_file', selectedFile);
        formData.append('patient_id', patientIdInput.value);
        formData.append('study_type', document.getElementById('study_type').value);
        formData.append('study_date', document.getElementById('study_date').value);
        formData.append('body_part', document.getElementById('body_part').value);
        formData.append('institution', document.getElementById('institution').value);
        formData.append('description', descriptionTextarea.value);
        
        try {
            // Mostrar loading
            setLoadingState(true);
            showProgressBar();
            
            // Simular progreso
            simulateProgress();
            
            const response = await fetch(API_UPLOAD_URL, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`,
                    'X-CSRFToken': getCSRFToken()
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (response.status === 409) {
                // Imagen duplicada
                handleDuplicateImage(data);
            } else if (response.ok && data.status === 'success') {
                // Carga exitosa
                handleUploadSuccess(data);
            } else {
                // Error
                handleUploadError(data);
            }
            
        } catch (error) {
            console.error('Error:', error);
            showAlert('Error de conexión. No se pudo completar la carga', 'danger');
        } finally {
            setLoadingState(false);
            hideProgressBar();
        }
    }

    // ========== Manejo de Respuestas ==========
    function handleUploadSuccess(data) {
        // Mostrar modal de éxito. Si no hay mensaje en la respuesta, usar uno por defecto.
        const msg = data && data.message ? data.message : 'La imagen se cargó correctamente.';
        const successMessageEl = document.getElementById('success-message');
        if (successMessageEl) successMessageEl.textContent = msg;

        try {
            // Ensure modal element is visibleable by removing hidden flag before showing (fallback)
            const successModalEl = document.getElementById('successModal');
            if (successModalEl && successModalEl.classList.contains('hidden-modal')) successModalEl.classList.remove('hidden-modal');
            successModal.show();
        } catch (err) {
            // Fallback: mostrar alerta si el modal no está disponible
            showAlert(msg, 'success');
        }

        // Limpiar formulario
        resetForm();
    }

    function handleDuplicateImage(data) {
        // Mostrar información de la imagen duplicada con validaciones
        const existing = data && data.existing_image ? data.existing_image : null;

        if (existing) {
            const dupPatientEl = document.getElementById('dup-patient');
            const dupTypeEl = document.getElementById('dup-type');
            const dupDateEl = document.getElementById('dup-date');

            if (dupPatientEl) dupPatientEl.textContent = existing.patient?.nombre_completo || '—';
            if (dupTypeEl) dupTypeEl.textContent = existing.study_type_display || (existing.study_type || '—');
            if (dupDateEl) dupDateEl.textContent = existing.study_date ? formatDate(existing.study_date) : '—';

            try {
                // Ensure DOM-hidden class removed before showing
                const duplicateModalEl = document.getElementById('duplicateModal');
                if (duplicateModalEl && duplicateModalEl.classList.contains('hidden-modal')) duplicateModalEl.classList.remove('hidden-modal');
                duplicateModal.show();
            } catch (err) {
                // Fallback: mostrar alerta con resumen
                showAlert(`Imagen duplicada detectada para ${existing.patient?.nombre_completo || 'un paciente'}.`, 'warning');
            }
        } else {
            // Si la respuesta no incluye datos detallados, mostrar mensaje genérico
            const msg = (data && data.message) ? data.message : 'Esta imagen ya existe en el sistema.';
            showAlert(msg, 'warning');
        }
    }

    function handleUploadError(data) {
        if (data.errors) {
            // Mostrar errores específicos
            Object.keys(data.errors).forEach(fieldName => {
                const field = document.getElementById(fieldName);
                if (field) {
                    const errors = data.errors[fieldName];
                    const errorMessage = Array.isArray(errors) ? errors.join(', ') : errors;
                    markFieldInvalid(field, errorMessage);
                }
            });
        }
        
        showAlert(data.message || 'Error al cargar la imagen', 'danger');
    }

    // ========== Manejo de Duplicados ==========
    window.keepBoth = function() {
        // Conservar ambas: actualmente simulado en frontend.
        try { duplicateModal.hide(); } catch (err) {}
        // Si bootstrap no está disponible, asegurar que el modal vuelva a ocultarse
        const duplicateModalEl = document.getElementById('duplicateModal');
        if (duplicateModalEl && !duplicateModalEl.classList.contains('hidden-modal')) duplicateModalEl.classList.add('hidden-modal');
        showAlert('Se conservarán ambas imágenes (acción simulada).', 'success');
        // Limpiar formulario para permitir nueva carga
        resetForm();
    };

    window.replaceImage = function() {
        // Reemplazar: actualmente simulado en frontend. Idealmente esto debería enviar una petición al backend indicando "replace: true".
        try { duplicateModal.hide(); } catch (err) {}
        const duplicateModalEl = document.getElementById('duplicateModal');
        if (duplicateModalEl && !duplicateModalEl.classList.contains('hidden-modal')) duplicateModalEl.classList.add('hidden-modal');
        showAlert('La imagen existente será reemplazada (acción simulada).', 'success');
        // Limpiar formulario
        resetForm();
    };

    // ========== Modal de Éxito ==========
    window.uploadAnother = function() {
        try { successModal.hide(); } catch (err) {}
        const successModalEl = document.getElementById('successModal');
        if (successModalEl && !successModalEl.classList.contains('hidden-modal')) successModalEl.classList.add('hidden-modal');
        resetForm();
    };

    // ========== Progress Bar ==========
    function showProgressBar() {
        document.getElementById('upload-progress-bar').classList.remove('d-none');
    }

    function hideProgressBar() {
        setTimeout(() => {
            document.getElementById('upload-progress-bar').classList.add('d-none');
            document.getElementById('progress-bar').style.width = '0%';
        }, 500);
    }

    function simulateProgress() {
        let progress = 0;
        const progressBar = document.getElementById('progress-bar');
        
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 95) {
                progress = 95;
                clearInterval(interval);
            }
            progressBar.style.width = `${progress}%`;
        }, 200);
    }

    // ========== Loading State ==========
    function setLoadingState(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Cargando...';
        } else {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
            submitBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Cargar Imagen';
        }
    }

    // ========== Utilidades ==========
    function showAlert(message, type = 'info') {
        const icons = {
            'success': 'fa-check-circle',
            'danger': 'fa-exclamation-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        
        const alertHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas ${icons[type]} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        alertContainer.innerHTML = alertHTML;
        alertContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        // Auto-cerrar después de 5 segundos
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                try {
                    if (window.bootstrap && typeof bootstrap.Alert === 'function') {
                        const bsAlert = new bootstrap.Alert(alert);
                        bsAlert.close();
                    } else {
                        // Fallback: remover manualmente
                        alert.remove();
                    }
                } catch (err) {
                    // Fallback: remover manualmente en caso de error
                    alert.remove();
                }
            }
        }, 5000);
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    function setTodayDate() {
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('study_date').setAttribute('max', today);
    }

    window.resetForm = function() {
        form.reset();
        clearFile();
        clearPatient();
        alertContainer.innerHTML = '';
        
        // Limpiar validaciones
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.classList.remove('is-invalid', 'is-valid');
        });
        
        updateCharCount();
    };

    function getAuthToken() {
        return localStorage.getItem('access_token') || sessionStorage.getItem('access_token') || '';
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

})();
