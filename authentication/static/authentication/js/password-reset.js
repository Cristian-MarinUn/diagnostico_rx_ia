/* ================================ */
/* ARCHIVO: authentication/static/authentication/js/password-reset.js */
/* ================================ */

document.addEventListener('DOMContentLoaded', function() {
    const resetForm = document.getElementById('resetForm');
    const newPasswordInput = document.querySelector('input[name="new_password"]');
    const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');
    const submitButton = document.getElementById('submitBtn');
    
    // Validación en tiempo real
    if (newPasswordInput) {
        newPasswordInput.addEventListener('input', function() {
            validatePasswordStrength(this.value);
            checkPasswordsMatch();
        });
    }
    
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', function() {
            checkPasswordsMatch();
        });
    }
    
    // Validación al enviar
    if (resetForm) {
        resetForm.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                return false;
            }
            
            // Estado de loading
            submitButton.disabled = true;
            submitButton.innerHTML = `
                <span class="btn-text">Guardando...</span>
                <span class="btn-icon">⏳</span>
            `;
        });
    }
    
    // Animación de entrada
    animateEntrance();
});

// Toggle para mostrar/ocultar contraseña
function togglePassword(fieldName) {
    const input = document.querySelector(`input[name="${fieldName}"]`);
    const icon = document.getElementById(fieldName === 'new_password' ? 'toggleIcon1' : 'toggleIcon2');
    
    if (!input) return;
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.textContent = '🙈';
    } else {
        input.type = 'password';
        icon.textContent = '👁️';
    }
}

// Validar fortaleza de contraseña
function validatePasswordStrength(password) {
    const requirements = {
        length: password.length >= 8,
        upper: /[A-Z]/.test(password),
        lower: /[a-z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };
    
    // Actualizar indicadores visuales
    updateRequirement('req-length', requirements.length);
    updateRequirement('req-upper', requirements.upper);
    updateRequirement('req-lower', requirements.lower);
    updateRequirement('req-number', requirements.number);
    updateRequirement('req-special', requirements.special);
    
    // Calcular fortaleza
    const metCount = Object.values(requirements).filter(Boolean).length;
    const strength = metCount <= 2 ? 'weak' : metCount <= 4 ? 'medium' : 'strong';
    
    // Actualizar barra de fortaleza
    const strengthFill = document.getElementById('strengthFill');
    const strengthText = document.getElementById('strengthText');
    
    if (strengthFill && strengthText) {
        strengthFill.className = 'strength-fill ' + strength;
        strengthText.className = 'strength-text ' + strength;
        
        const strengthMessages = {
            weak: 'Contraseña débil',
            medium: 'Contraseña moderada',
            strong: 'Contraseña fuerte'
        };
        
        strengthText.textContent = password ? strengthMessages[strength] : 'Ingresa una contraseña';
    }
    
    // Habilitar/deshabilitar botón
    const allRequirementsMet = Object.values(requirements).every(Boolean);
    updateSubmitButton(allRequirementsMet);
    
    return allRequirementsMet;
}

function updateRequirement(reqId, isMet) {
    const requirement = document.getElementById(reqId);
    if (!requirement) return;
    
    if (isMet) {
        requirement.classList.add('met');
        const icon = requirement.querySelector('.req-icon');
        if (icon) icon.textContent = '✓';
    } else {
        requirement.classList.remove('met');
        const icon = requirement.querySelector('.req-icon');
        if (icon) icon.textContent = '○';
    }
}

function checkPasswordsMatch() {
    const newPassword = document.querySelector('input[name="new_password"]').value;
    const confirmPassword = document.querySelector('input[name="confirm_password"]').value;
    const confirmInput = document.querySelector('input[name="confirm_password"]');
    
    if (!confirmPassword) {
        clearFieldError(confirmInput);
        return true;
    }
    
    if (newPassword !== confirmPassword) {
        showFieldError(confirmInput, 'Las contraseñas no coinciden');
        updateSubmitButton(false);
        return false;
    } else {
        clearFieldError(confirmInput);
        // Verificar si todos los requisitos están cumplidos
        const allRequirementsMet = validatePasswordStrength(newPassword);
        updateSubmitButton(allRequirementsMet);
        return true;
    }
}

function updateSubmitButton(isValid) {
    const submitButton = document.getElementById('submitBtn');
    if (!submitButton) return;
    
    const newPassword = document.querySelector('input[name="new_password"]').value;
    const confirmPassword = document.querySelector('input[name="confirm_password"]').value;
    
    const canSubmit = isValid && newPassword && confirmPassword && newPassword === confirmPassword;
    
    submitButton.disabled = !canSubmit;
    
    if (canSubmit) {
        submitButton.style.opacity = '1';
        submitButton.style.cursor = 'pointer';
    } else {
        submitButton.style.opacity = '0.5';
        submitButton.style.cursor = 'not-allowed';
    }
}

function validateForm() {
    const newPassword = document.querySelector('input[name="new_password"]').value;
    const confirmPassword = document.querySelector('input[name="confirm_password"]').value;
    
    // Validar fortaleza
    if (!validatePasswordStrength(newPassword)) {
        alert('Por favor, asegúrate de que la contraseña cumpla todos los requisitos.');
        return false;
    }
    
    // Validar coincidencia
    if (newPassword !== confirmPassword) {
        alert('Las contraseñas no coinciden.');
        return false;
    }
    
    return true;
}

function showFieldError(input, message) {
    input.classList.add('invalid');
    
    const existingError = input.parentElement.parentElement.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <span>⚠️</span>
        <span>${message}</span>
    `;
    
    input.parentElement.parentElement.appendChild(errorDiv);
}

function clearFieldError(input) {
    input.classList.remove('invalid');
    const errorMessage = input.parentElement.parentElement.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.style.opacity = '0';
        errorMessage.style.transform = 'translateY(-10px)';
        setTimeout(function() {
            errorMessage.remove();
        }, 300);
    }
}

function animateEntrance() {
    const elements = [
        '.recovery-header',
        '.alert',
        '.form-group',
        '.password-strength',
        '.password-requirements',
        '.btn-recovery',
        '.recovery-footer'
    ];
    
    elements.forEach((selector, index) => {
        const items = document.querySelectorAll(selector);
        items.forEach((element, itemIndex) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            setTimeout(() => {
                element.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, (index * 100) + (itemIndex * 50));
        });
    });
}

// Auto-cerrar alertas
const alerts = document.querySelectorAll('.alert');
alerts.forEach(function(alert) {
    setTimeout(function() {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        setTimeout(function() {
            alert.remove();
        }, 300);
    }, 5000);
});