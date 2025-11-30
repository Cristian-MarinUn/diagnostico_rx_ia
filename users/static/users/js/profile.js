// ================================
// ARCHIVO: authentication/static/authentication/js/profile.js
// ================================

/**
 * Script para la página de perfil de usuario
 * CU-007: Visualizar Perfil de Usuario
 */

(function() {
    'use strict';
    
    // Variables globales
    let currentSessionId = null;
    const modal = document.getElementById('closeSessionModal');
    
    /**
     * Inicialización cuando el DOM está listo
     */
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Profile page loaded');
        
        // Inicializar funcionalidades
        initCloseSessionButtons();
        initModalHandlers();
        initAnimations();
        initTooltips();
        
        // Actualizar tiempo relativo cada minuto
        setInterval(updateRelativeTimes, 60000);
    });
    
    /**
     * Inicializa los botones de cerrar sesión
     */
    function initCloseSessionButtons() {
        const closeButtons = document.querySelectorAll('.btn-close-session');
        
        closeButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                currentSessionId = this.getAttribute('data-session-id');
                showModal();
            });
        });
    }
    
    /**
     * Inicializa los handlers del modal
     */
    function initModalHandlers() {
        const cancelBtn = document.getElementById('cancelCloseSession');
        const confirmBtn = document.getElementById('confirmCloseSession');
        
        // Cancelar
        if (cancelBtn) {
            cancelBtn.addEventListener('click', function() {
                hideModal();
                currentSessionId = null;
            });
        }
        
        // Confirmar cierre
        if (confirmBtn) {
            confirmBtn.addEventListener('click', function() {
                if (currentSessionId) {
                    closeSession(currentSessionId);
                }
            });
        }
        
        // Cerrar al hacer click fuera del modal
        if (modal) {
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    hideModal();
                    currentSessionId = null;
                }
            });
        }
        
        // Cerrar con ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && modal.classList.contains('show')) {
                hideModal();
                currentSessionId = null;
            }
        });
    }
    
    /**
     * Muestra el modal
     */
    function showModal() {
        if (modal) {
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    }
    
    /**
     * Oculta el modal
     */
    function hideModal() {
        if (modal) {
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }
    }
    
    /**
     * Cierra una sesión específica
     */
    function closeSession(sessionId) {
        const confirmBtn = document.getElementById('confirmCloseSession');
        
        // Mostrar loading
        if (confirmBtn) {
            confirmBtn.disabled = true;
            confirmBtn.innerHTML = '<span class="spinner"></span> Cerrando...';
        }
        
        // Aquí iría la llamada AJAX para cerrar la sesión
        // Por ahora, simulamos el cierre
        setTimeout(() => {
            // Simular éxito
            showNotification('Sesión cerrada exitosamente', 'success');
            
            // Remover el item de sesión del DOM
            const sessionItem = document.querySelector(`[data-session-id="${sessionId}"]`).closest('.session-item');
            if (sessionItem) {
                sessionItem.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => {
                    sessionItem.remove();
                    updateSessionCount();
                }, 300);
            }
            
            // Cerrar modal
            hideModal();
            currentSessionId = null;
            
            // Restaurar botón
            if (confirmBtn) {
                confirmBtn.disabled = false;
                confirmBtn.textContent = 'Cerrar Sesión';
            }
        }, 1000);
    }
    
    /**
     * Actualiza el contador de sesiones activas
     */
    function updateSessionCount() {
        const sessionsList = document.querySelectorAll('.session-item');
        const badge = document.querySelector('.card-header .badge');
        
        if (badge) {
            badge.textContent = sessionsList.length;
        }
        
        // Si no quedan sesiones, mostrar mensaje vacío
        if (sessionsList.length === 0) {
            const container = document.querySelector('.sessions-list');
            if (container) {
                container.innerHTML = `
                    <div class="empty-state">
                        <span class="empty-icon">💤</span>
                        <p>No hay sesiones activas adicionales</p>
                    </div>
                `;
            }
        }
    }
    
    /**
     * Inicializa animaciones de entrada
     */
    function initAnimations() {
        // Observador de intersección para animaciones
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        // Observar todas las tarjetas
        const cards = document.querySelectorAll('.profile-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.animationDelay = `${index * 0.1}s`;
            observer.observe(card);
        });
        
        // Agregar animación CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideOut {
                from {
                    opacity: 1;
                    transform: translateX(0);
                }
                to {
                    opacity: 0;
                    transform: translateX(100px);
                }
            }
            
            .spinner {
                display: inline-block;
                width: 16px;
                height: 16px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-top-color: white;
                border-radius: 50%;
                animation: spin 0.6s linear infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }
    
    /**
     * Actualiza los tiempos relativos (ej: "hace 5 minutos")
     */
    function updateRelativeTimes() {
        const timeElements = document.querySelectorAll('[data-timestamp]');
        
        timeElements.forEach(element => {
            const timestamp = parseInt(element.getAttribute('data-timestamp'));
            const relativeTime = getRelativeTime(timestamp);
            element.textContent = relativeTime;
        });
    }
    
    /**
     * Calcula tiempo relativo
     */
    function getRelativeTime(timestamp) {
        const now = Date.now();
        const diff = now - timestamp;
        
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (days > 0) return `Hace ${days} día${days > 1 ? 's' : ''}`;
        if (hours > 0) return `Hace ${hours} hora${hours > 1 ? 's' : ''}`;
        if (minutes > 0) return `Hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
        return 'Hace unos momentos';
    }
    
    /**
     * Inicializa tooltips personalizados
     */
    function initTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                const tooltip = createTooltip(this.getAttribute('data-tooltip'));
                document.body.appendChild(tooltip);
                positionTooltip(tooltip, this);
            });
            
            element.addEventListener('mouseleave', function() {
                const tooltip = document.querySelector('.custom-tooltip');
                if (tooltip) {
                    tooltip.remove();
                }
            });
        });
    }
    
    /**
     * Crea un elemento tooltip
     */
    function createTooltip(text) {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            font-size: 0.875rem;
            z-index: 10000;
            pointer-events: none;
            white-space: nowrap;
        `;
        return tooltip;
    }
    
    /**
     * Posiciona el tooltip
     */
    function positionTooltip(tooltip, targetElement) {
        const rect = targetElement.getBoundingClientRect();
        tooltip.style.top = `${rect.top - tooltip.offsetHeight - 8}px`;
        tooltip.style.left = `${rect.left + (rect.width - tooltip.offsetWidth) / 2}px`;
    }
    
    /**
     * Muestra una notificación tipo toast
     */
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
        
        notification.innerHTML = `
            <span class="notification-icon">${icon}</span>
            <span class="notification-message">${message}</span>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10B981' : type === 'error' ? '#EF4444' : '#5B8DEE'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            gap: 0.75rem;
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
            font-weight: 500;
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remover después de 3 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
        
        // Agregar animaciones
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes slideOutRight {
                from {
                    opacity: 1;
                    transform: translateX(0);
                }
                to {
                    opacity: 0;
                    transform: translateX(100px);
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    /**
     * Copia texto al portapapeles
     */
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copiado al portapapeles', 'success');
        }).catch(() => {
            showNotification('Error al copiar', 'error');
        });
    }
    
    // Exponer funciones globalmente si es necesario
    window.ProfilePage = {
        showNotification,
        copyToClipboard
    };
    
})();














// ================================
// ARCHIVO: apps/users/static/users/js/profile_view.js
// CU-006 y CU-007: JavaScript para Perfil y 2FA
// ================================

(function() {
    'use strict';

    // ========== Variables Globales ==========
    const API_PROFILE_URL = '/api/users/profile/';
    const API_2FA_STATUS_URL = '/api/users/2fa/status/';
    const API_2FA_ENABLE_URL = '/api/users/2fa/enable/';
    const API_2FA_DISABLE_URL = '/api/users/2fa/disable/';
    const API_SECURITY_URL = '/api/users/profile/security/';

    // ========== Inicialización ==========
    document.addEventListener('DOMContentLoaded', function() {
        load2FAStatus();
        loadSecurityInfo();
    });

    // ========== Cargar Estado 2FA ==========
    async function load2FAStatus() {
        try {
            const response = await fetch(API_2FA_STATUS_URL, {
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) throw new Error('Error al cargar estado 2FA');

            const data = await response.json();
            render2FAStatus(data.data);
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('2fa-status-container').innerHTML = `
                <div class="alert alert-danger mb-0">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Error al cargar la información de 2FA
                </div>
            `;
        }
    }

    // ========== Renderizar Estado 2FA ==========
    function render2FAStatus(status) {
        const container = document.getElementById('2fa-status-container');
        
        if (status.is_enabled) {
            container.innerHTML = `
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <div class="d-flex align-items-center mb-2">
                            <span class="badge bg-success me-2">
                                <i class="fas fa-check-circle"></i> Habilitado
                            </span>
                        </div>
                        <p class="text-muted small mb-0">
                            Método: ${get2FAMethodName(status.method)}
                        </p>
                        <p class="text-muted small mb-0">
                            Configurado: ${formatDate(status.created_at)}
                        </p>
                    </div>
                    <button 
                        class="btn btn-sm btn-outline-danger" 
                        onclick="disable2FA()"
                    >
                        <i class="fas fa-times-circle me-1"></i>
                        Deshabilitar
                    </button>
                </div>
                <div class="alert alert-success mb-0">
                    <i class="fas fa-shield-alt me-2"></i>
                    Tu cuenta está protegida con 2FA
                </div>
            `;
        } else {
            container.innerHTML = `
                <div class="text-center mb-3">
                    <i class="fas fa-shield-alt fa-3x text-muted mb-3"></i>
                    <p class="text-muted mb-3">
                        La autenticación de dos factores agrega una capa adicional de seguridad a tu cuenta.
                    </p>
                    <button 
                        class="btn btn-success btn-sm" 
                        onclick="showEnable2FAModal()"
                    >
                        <i class="fas fa-plus-circle me-1"></i>
                        Habilitar 2FA
                    </button>
                </div>
            `;
        }
    }

    // ========== Cargar Información de Seguridad ==========
    async function loadSecurityInfo() {
        try {
            const response = await fetch(API_SECURITY_URL, {
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) throw new Error('Error al cargar información de seguridad');

            const data = await response.json();
            renderSecurityInfo(data.data);
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('security-info-container').innerHTML = `
                <div class="alert alert-danger mb-0">
                    Error al cargar información de seguridad
                </div>
            `;
        }
    }

    // ========== Renderizar Información de Seguridad ==========
    function renderSecurityInfo(info) {
        const container = document.getElementById('security-info-container');
        
        container.innerHTML = `
            <div class="row">
                <div class="col-md-6 mb-3">
                    <div class="security-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">Autenticación de Dos Factores</h6>
                                <p class="text-muted small mb-0">
                                    ${info.two_factor_enabled ? 'Habilitada' : 'Deshabilitada'}
                                </p>
                            </div>
                            <div>
                                ${info.two_factor_enabled ? 
                                    '<i class="fas fa-check-circle fa-2x text-success"></i>' :
                                    '<i class="fas fa-times-circle fa-2x text-danger"></i>'
                                }
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6 mb-3">
                    <div class="security-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">Sesiones Activas</h6>
                                <p class="text-muted small mb-0">
                                    ${info.active_sessions} sesión(es) activa(s)
                                </p>
                            </div>
                            <div>
                                <i class="fas fa-desktop fa-2x text-primary"></i>
                            </div>
                        </div>
                    </div>
                </div>

                ${info.last_login_ip ? `
                <div class="col-md-6 mb-3">
                    <div class="security-item">
                        <h6 class="mb-1">
                            <i class="fas fa-map-marker-alt text-primary me-2"></i>
                            Último Acceso desde IP
                        </h6>
                        <p class="mb-0 font-monospace">${info.last_login_ip}</p>
                    </div>
                </div>
                ` : ''}

                <div class="col-12">
                    <div class="alert alert-info mb-0">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>Recomendaciones de seguridad:</strong>
                        <ul class="mb-0 mt-2">
                            <li>Cambia tu contraseña regularmente</li>
                            <li>Habilita la autenticación de dos factores</li>
                            <li>No compartas tu contraseña con nadie</li>
                            <li>Cierra sesión en dispositivos públicos</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    // ========== Mostrar Modal para Habilitar 2FA ==========
    window.showEnable2FAModal = async function() {
        const modal = new bootstrap.Modal(document.getElementById('setup2FAModal'));
        const content = document.getElementById('setup2FAContent');
        
        content.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Configurando 2FA...</p>
            </div>
        `;
        
        modal.show();

        // Solicitar contraseña
        content.innerHTML = `
            <div class="mb-4">
                <p>Para habilitar la autenticación de dos factores, primero confirma tu contraseña actual:</p>
                <form id="confirm-password-form">
                    <div class="mb-3">
                        <label for="current-password" class="form-label">Contraseña Actual</label>
                        <input 
                            type="password" 
                            class="form-control" 
                            id="current-password" 
                            required
                        >
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-check me-2"></i>
                        Continuar
                    </button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancelar
                    </button>
                </form>
            </div>
        `;

        document.getElementById('confirm-password-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            await enable2FA();
        });
    };

    // ========== Habilitar 2FA ==========
    async function enable2FA() {
        const password = document.getElementById('current-password').value;
        const content = document.getElementById('setup2FAContent');

        try {
            content.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Habilitando 2FA...</p>
                </div>
            `;

            const response = await fetch(API_2FA_ENABLE_URL, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`,
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ password })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Error al habilitar 2FA');
            }

            // Mostrar QR y códigos de respaldo
            content.innerHTML = `
                <div class="text-center mb-4">
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle me-2"></i>
                        ${data.message}
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6 mb-4">
                        <h6 class="mb-3">1. Escanea el código QR</h6>
                        <p class="text-muted small">
                            Usa Google Authenticator, Authy o cualquier aplicación compatible con TOTP
                        </p>
                        <div class="text-center">
                            <img 
                                src="${data.data.qr_code}" 
                                alt="QR Code" 
                                class="img-fluid border rounded p-2"
                                style="max-width: 250px;"
                            >
                        </div>
                        <div class="mt-3">
                            <p class="text-muted small mb-1">O ingresa manualmente:</p>
                            <div class="input-group">
                                <input 
                                    type="text" 
                                    class="form-control font-monospace" 
                                    value="${data.data.secret}" 
                                    readonly
                                    id="secret-key"
                                >
                                <button 
                                    class="btn btn-outline-secondary" 
                                    onclick="copyToClipboard('secret-key')"
                                >
                                    <i class="fas fa-copy"></i>
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-6 mb-4">
                        <h6 class="mb-3">2. Guarda los códigos de respaldo</h6>
                        <div class="alert alert-warning">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            <strong>Importante:</strong> Guarda estos códigos en un lugar seguro. 
                            Los necesitarás si pierdes acceso a tu autenticador.
                        </div>
                        <div class="backup-codes-container p-3 bg-light rounded">
                            ${data.data.backup_codes.map(code => `
                                <code class="d-block mb-2">${code}</code>
                            `).join('')}
                        </div>
                        <button 
                            class="btn btn-sm btn-outline-primary mt-2 w-100" 
                            onclick="downloadBackupCodes(${JSON.stringify(data.data.backup_codes)})"
                        >
                            <i class="fas fa-download me-2"></i>
                            Descargar Códigos
                        </button>
                    </div>
                </div>

                <div class="text-center mt-4">
                    <button 
                        class="btn btn-success" 
                        onclick="complete2FASetup()"
                    >
                        <i class="fas fa-check me-2"></i>
                        Completar Configuración
                    </button>
                </div>
            `;

        } catch (error) {
            content.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    ${error.message}
                </div>
                <button class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
            `;
        }
    }

    // ========== Completar Setup 2FA ==========
    window.complete2FASetup = function() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('setup2FAModal'));
        modal.hide();
        
        // Recargar estado
        load2FAStatus();
        
        // Mostrar notificación
        showNotification('2FA habilitado correctamente', 'success');
    };

    // ========== Deshabilitar 2FA ==========
    window.disable2FA = async function() {
        if (!confirm('¿Estás seguro de que deseas deshabilitar 2FA? Esto reducirá la seguridad de tu cuenta.')) {
            return;
        }

        const password = prompt('Ingresa tu contraseña para confirmar:');
        if (!password) return;

        try {
            const response = await fetch(API_2FA_DISABLE_URL, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`,
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ password })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Error al deshabilitar 2FA');
            }

            showNotification(data.message, 'success');
            load2FAStatus();

        } catch (error) {
            showNotification(error.message, 'danger');
        }
    };

    // ========== Utilidades ==========

    function get2FAMethodName(method) {
        const methods = {
            'totp': 'Aplicación Autenticadora',
            'email': 'Código por Email',
            'sms': 'Código por SMS'
        };
        return methods[method] || method;
    }

    function formatDate(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    window.copyToClipboard = function(elementId) {
        const element = document.getElementById(elementId);
        element.select();
        document.execCommand('copy');
        showNotification('Copiado al portapapeles', 'success');
    };

    window.downloadBackupCodes = function(codes) {
        const content = 'Códigos de Respaldo 2FA\n' +
                       'Sistema de Diagnóstico IA\n\n' +
                       codes.join('\n');
        
        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = '2fa-backup-codes.txt';
        a.click();
        window.URL.revokeObjectURL(url);
    };

    function showNotification(message, type = 'info') {
        // Implementar según tu sistema de notificaciones
        alert(message);
    }

    function getAuthToken() {
        return localStorage.getItem('access_token') || sessionStorage.getItem('access_token') || '';
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

})();