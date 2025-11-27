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