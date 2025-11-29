// ================================
// users/static/users/js/patient_create.js
// Funcionalidad para crear pacientes
// ================================

(function() {
    'use strict';

    // DOM Elements
    let patientForm;
    let formInputs = {};
    let alertContainer;

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        initializeElements();
        initializeEventListeners();
    });

    // ========== Initialization ==========
    function initializeElements() {
        patientForm = document.getElementById('patient-form');
        alertContainer = document.getElementById('alert-container');

        // Get all form inputs
        formInputs = {
            identification: document.getElementById('id_identification'),
            first_name: document.getElementById('id_first_name'),
            last_name: document.getElementById('id_last_name'),
            date_of_birth: document.getElementById('id_date_of_birth'),
            gender: document.getElementById('id_gender'),
            email: document.getElementById('id_email'),
            email_confirmation: document.getElementById('id_email_confirmation'),
            phone: document.getElementById('id_phone')
        };
    }

    function initializeEventListeners() {
        if (!patientForm) return;

        // Form submission
        patientForm.addEventListener('submit', handleSubmit);

        // Form reset
        const resetBtn = document.getElementById('reset-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', handleReset);
        }

        // Real-time validation and progress tracking
        Object.values(formInputs).forEach(input => {
            if (input) {
                input.addEventListener('blur', validateField);
                input.addEventListener('change', () => {
                    updateProgress();
                    validateField({ target: input });
                });
                input.addEventListener('input', updateProgress);
            }
        });

        // Age calculation on date change
        if (formInputs.date_of_birth) {
            formInputs.date_of_birth.addEventListener('change', calculateAge);
        }

        // Email confirmation validation
        if (formInputs.email && formInputs.email_confirmation) {
            formInputs.email_confirmation.addEventListener('blur', validateEmailMatch);
        }
    }

    // ========== Form Submission ==========
    function handleSubmit(e) {
        e.preventDefault();

        if (!validateForm()) {
            showAlert('Por favor, completa todos los campos obligatorios', 'warning');
            return;
        }

        submitForm();
    }

    function validateForm() {
        let isValid = true;

        // Required fields
        const requiredFields = ['identification', 'first_name', 'last_name', 'date_of_birth', 'gender'];

        requiredFields.forEach(fieldName => {
            const field = formInputs[fieldName];
            if (field && !field.value.trim()) {
                markFieldInvalid(field, 'Este campo es obligatorio');
                isValid = false;
            } else if (field) {
                clearFieldError(field);
            }
        });

        // Validate email match if present
        if (formInputs.email && formInputs.email.value.trim()) {
            if (formInputs.email_confirmation && formInputs.email.value !== formInputs.email_confirmation.value) {
                markFieldInvalid(formInputs.email_confirmation, 'Los emails no coinciden');
                isValid = false;
            }
        }

        return isValid;
    }

    function validateField(e) {
        const field = e.target;
        const fieldName = field.name.replace('id_', '');

        if (!field.value.trim()) {
            if (field.hasAttribute('required')) {
                markFieldInvalid(field, 'Este campo es obligatorio');
            }
            return false;
        }

        clearFieldError(field);

        // Type-specific validation
        if (fieldName === 'date_of_birth') {
            const dateValue = new Date(field.value);
            const today = new Date();

            if (dateValue > today) {
                markFieldInvalid(field, 'La fecha no puede ser futura');
                return false;
            }

            const maxDate = new Date();
            maxDate.setFullYear(maxDate.getFullYear() - 150);
            if (dateValue < maxDate) {
                markFieldInvalid(field, 'Fecha de nacimiento inválida (muy antigua)');
                return false;
            }
        }

        if (fieldName === 'email') {
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailRegex.test(field.value)) {
                markFieldInvalid(field, 'Formato de email inválido');
                return false;
            }
        }

        if (fieldName === 'phone' && field.value) {
            const phoneRegex = /^(\+?[0-9\s\-\(\)]{7,})?$/;
            if (!phoneRegex.test(field.value)) {
                markFieldInvalid(field, 'Formato de teléfono inválido');
                return false;
            }
        }

        return true;
    }

    function validateEmailMatch(e) {
        const emailField = formInputs.email;
        const confirmField = formInputs.email_confirmation;

        if (confirmField.value && emailField.value !== confirmField.value) {
            markFieldInvalid(confirmField, 'Los emails no coinciden');
        } else if (confirmField.value) {
            clearFieldError(confirmField);
        }
    }

    function markFieldInvalid(field, message) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');

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
        if (field.value.trim()) {
            field.classList.add('is-valid');
        }

        const feedback = field.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = '';
        }
    }

    // ========== Age Calculation ==========
    function calculateAge() {
        const dateValue = formInputs.date_of_birth.value;
        if (!dateValue) return;

        const birthDate = new Date(dateValue);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }

        const ageDisplay = document.getElementById('age-display');
        if (ageDisplay && age >= 0) {
            ageDisplay.textContent = `Edad: ${age} años`;
            ageDisplay.style.color = 'var(--text-secondary)';
        }
    }

    // ========== Progress Tracking ==========
    function updateProgress() {
        const requiredFields = ['identification', 'first_name', 'last_name', 'date_of_birth', 'gender'];
        let completedCount = 0;

        requiredFields.forEach(fieldName => {
            const field = formInputs[fieldName];
            const checklistItem = document.querySelector(`[data-field="${fieldName}"]`);

            if (field && field.value.trim()) {
                completedCount++;
                if (checklistItem) {
                    checklistItem.classList.add('completed');
                }
            } else if (checklistItem) {
                checklistItem.classList.remove('completed');
            }
        });

        const totalRequired = requiredFields.length;
        const percentage = Math.round((completedCount / totalRequired) * 100);

        const progressFill = document.getElementById('progress-fill');
        const progressPercent = document.getElementById('progress-percent');

        if (progressFill) progressFill.style.width = `${percentage}%`;
        if (progressPercent) progressPercent.textContent = percentage;
    }

    // ========== Form Submission ==========
    function submitForm() {
        const submitBtn = document.getElementById('submit-btn');
        const originalText = submitBtn.innerHTML;

        // Set loading state
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Registrando...';

        // Simulate form submission (actual submission handled by Django)
        setTimeout(() => {
            // If there are no JS errors, the form will submit normally
            patientForm.submit();
        }, 300);
    }

    function handleReset(e) {
        e.preventDefault();

        patientForm.reset();
        alertContainer.innerHTML = '';

        // Clear validation states
        Object.values(formInputs).forEach(input => {
            if (input) {
                input.classList.remove('is-invalid', 'is-valid');
                const feedback = input.parentElement.querySelector('.invalid-feedback');
                if (feedback) {
                    feedback.textContent = '';
                }
            }
        });

        // Reset progress
        updateProgress();
        const ageDisplay = document.getElementById('age-display');
        if (ageDisplay) {
            ageDisplay.textContent = '';
        }
    }

    // ========== Alerts ==========
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

        // Auto-close after 5 seconds
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                alert.remove();
            }
        }, 5000);
    }

})();
