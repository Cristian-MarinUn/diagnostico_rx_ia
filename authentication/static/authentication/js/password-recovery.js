/* ================================ */
/* ARCHIVO: authentication/static/authentication/js/password-recovery.js */
/* ================================ */

document.addEventListener('DOMContentLoaded', function() {
    const recoveryForm = document.getElementById('recoveryForm');
    const emailInput = document.querySelector('input[type="email"]');
    const submitButton = document.querySelector('.btn-recovery');
    
    // Validación del formulario
    if (recoveryForm && emailInput) {
        emailInput.addEventListener('input', function() {
            validateEmail(this);
        });
        
        recoveryForm.addEventListener('submit', function(e) {
            if (!validateEmail(emailInput)) {
                e.preventDefault();
                return false;
            }
            
            // Añadir estado de carga
            submitButton.disabled = true;
            submitButton.innerHTML = `
                <span class="btn-text">Enviando...</span>
                <span class="btn-icon loading">⏳</span>
            `;
            
            // Añadir animación de loading
            submitButton.classList.add('loading');
        });
    }
    
    // Auto-cerrar alertas después de 5 segundos
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
    
    // Animación de entrada para los elementos
    animateEntrance();
});

function validateEmail(input) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const value = input.value.trim();
    
    if (!value) {
        showFieldError(input, 'El correo electrónico es requerido');
        return false;
    }
    
    if (!emailRegex.test(value)) {
        showFieldError(input, 'Ingresa un correo electrónico válido');
        return false;
    }
    
    clearFieldError(input);
    return true;
}

function showFieldError(input, message) {
    input.classList.add('invalid');
    
    // Remover mensaje de error existente
    const existingError = input.parentElement.parentElement.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Crear nuevo mensaje de error
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
        '.btn-recovery',
        '.recovery-footer',
        '.info-card'
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

// Añadir estilos para el estado de loading
const style = document.createElement('style');
style.textContent = `
    .btn-recovery.loading {
        pointer-events: none;
    }
    
    .btn-recovery .btn-icon.loading {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
`;
document.head.appendChild(style);