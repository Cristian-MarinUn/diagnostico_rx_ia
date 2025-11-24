/* ================================ */
/* ARCHIVO: authentication/static/authentication/js/login.js */
/* ================================ */

// Toggle para mostrar/ocultar contraseña
function togglePassword() {
    const passwordInput = document.querySelector('input[type="password"], input[type="text"][name*="password"]');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (!passwordInput) return;
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.textContent = '🙈'; // Icono de ocultar
    } else {
        passwordInput.type = 'password';
        toggleIcon.textContent = '👁️'; // Icono de mostrar
    }
}

// Animación del botón de login al enviar el formulario
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginButton = document.querySelector('.btn-login');
    
    if (loginForm && loginButton) {
        loginForm.addEventListener('submit', function(e) {
            // Añadir clase de loading al botón
            loginButton.classList.add('loading');
            loginButton.disabled = true;
            
            // Cambiar texto del botón
            const originalText = loginButton.textContent;
            loginButton.textContent = 'Iniciando sesión...';
            
            // Si el formulario falla la validación, restaurar el botón
            setTimeout(function() {
                if (!loginForm.checkValidity()) {
                    loginButton.classList.remove('loading');
                    loginButton.disabled = false;
                    loginButton.textContent = originalText;
                }
            }, 100);
        });
    }
    
    // Validación en tiempo real
    const emailInput = document.querySelector('input[type="email"]');
    const passwordInput = document.querySelector('input[type="password"], input[type="text"][name*="password"]');
    
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            validateEmail(this);
        });
        
        emailInput.addEventListener('input', function() {
            if (this.classList.contains('invalid')) {
                validateEmail(this);
            }
        });
    }
    
    if (passwordInput) {
        passwordInput.addEventListener('blur', function() {
            validatePassword(this);
        });
        
        passwordInput.addEventListener('input', function() {
            if (this.classList.contains('invalid')) {
                validatePassword(this);
            }
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
    
    // Animación de entrada para los campos del formulario
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach(function(group, index) {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        setTimeout(function() {
            group.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, 100 * index);
    });
});

// Validar email
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

// Validar contraseña
function validatePassword(input) {
    const value = input.value;
    
    if (!value) {
        showFieldError(input, 'La contraseña es requerida');
        return false;
    }
    
    if (value.length < 6) {
        showFieldError(input, 'La contraseña debe tener al menos 6 caracteres');
        return false;
    }
    
    clearFieldError(input);
    return true;
}

// Mostrar error en campo
function showFieldError(input, message) {
    input.classList.add('invalid');
    
    // Remover mensaje de error existente
    const existingError = input.parentElement.querySelector('.error-message');
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
    
    // Si hay toggle de contraseña, insertar antes del toggle
    const passwordToggle = input.parentElement.querySelector('.password-toggle-btn');
    if (passwordToggle) {
        input.parentElement.parentElement.appendChild(errorDiv);
    } else {
        input.parentElement.appendChild(errorDiv);
    }
}

// Limpiar error del campo
function clearFieldError(input) {
    input.classList.remove('invalid');
    const errorMessage = input.parentElement.querySelector('.error-message') || 
                        input.parentElement.parentElement.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.style.opacity = '0';
        errorMessage.style.transform = 'translateY(-10px)';
        setTimeout(function() {
            errorMessage.remove();
        }, 300);
    }
}

// Efecto de partículas en el fondo (opcional)
function createParticles() {
    const container = document.querySelector('.login-container');
    if (!container) return;
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: rgba(102, 126, 234, ${Math.random() * 0.5 + 0.2});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: float ${Math.random() * 10 + 10}s ease-in-out infinite;
            animation-delay: ${Math.random() * 5}s;
            pointer-events: none;
            z-index: 0;
        `;
        container.appendChild(particle);
    }
}

// Activar partículas (comentado por defecto)
// createParticles();

// Efecto de tecla Enter en campos
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const loginForm = document.getElementById('loginForm');
        const activeElement = document.activeElement;
        
        if (activeElement.tagName === 'INPUT' && loginForm.contains(activeElement)) {
            const inputs = Array.from(loginForm.querySelectorAll('input:not([type="checkbox"])'));
            const currentIndex = inputs.indexOf(activeElement);
            
            if (currentIndex < inputs.length - 1) {
                e.preventDefault();
                inputs[currentIndex + 1].focus();
            }
        }
    }
});

// Prevenir doble envío del formulario
let formSubmitted = false;
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            if (formSubmitted) {
                e.preventDefault();
                return false;
            }
            formSubmitted = true;
        });
    }
});

// Detectar si el navegador tiene autocompletar activado
window.addEventListener('load', function() {
    const inputs = document.querySelectorAll('input[type="email"], input[type="password"]');
    
    inputs.forEach(function(input) {
        if (input.value) {
            input.parentElement.classList.add('has-value');
        }
        
        input.addEventListener('change', function() {
            if (this.value) {
                this.parentElement.classList.add('has-value');
            } else {
                this.parentElement.classList.remove('has-value');
            }
        });
    });
});