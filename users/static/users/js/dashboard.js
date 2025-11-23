// ================================
// ARCHIVO: users/static/users/js/dashboard.js
// ================================

/**
 * Dashboard de Administración
 * Funcionalidades generales para el dashboard y formularios
 */

(function() {
    'use strict';
    
    /**
     * Inicialización
     */
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Admin Dashboard loaded');
        
        // Inicializar funcionalidades
        initFormValidation();
        initToggleSwitches();
        initAnimations();
        initTableSorting();
        
        // Auto-ocultar mensajes después de 5 segundos
        autoHideAlerts();
    });
    
    /**
     * Validación de formularios en tiempo real
     */
    function initFormValidation() {
        const forms = document.querySelectorAll('.user-form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input[required], select[required]');
            
            inputs.forEach(input => {
                // Validación al perder foco
                input.addEventListener('blur', function() {
                    validateField(this);
                });
                
                // Remover error al escribir
                input.addEventListener('input', function() {
                    if (this.classList.contains('invalid')) {
                        this.classList.remove('invalid');
                    }
                });
            });
            
            // Validación al enviar
            form.addEventListener('submit', function(e) {
                let isValid = true;
                
                inputs.forEach(input => {
                    if (!validateField(input)) {
                        isValid = false;
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    showNotification('Por favor, complete todos los campos correctamente', 'error');
                }
            });
        });
    }
    
    /**
     * Valida un campo individual
     */
    function validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        const pattern = field.pattern;
        let isValid = true;
        
        // Campo requerido vacío
        if (field.hasAttribute('required') && !value) {
            isValid = false;
        }
        
        // Email
        if (type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
            }
        }
        
        // Pattern personalizado
        if (pattern && value) {
            const regex = new RegExp(pattern);
            if (!regex.test(value)) {
                isValid = false;
            }
        }
        
        // Actualizar UI
        if (!isValid) {
            field.classList.add('invalid');
        } else {
            field.classList.remove('invalid');
        }
        
        return isValid;
    }
    
    /**
     * Inicializa los toggle switches
     */
    function initToggleSwitches() {
        const toggles = document.querySelectorAll('.toggle-switch input');
        
        toggles.forEach(toggle => {
            const textElement = document.getElementById(`${toggle.id}-text`);
            
            if (textElement) {
                // Estado inicial
                updateToggleText(toggle, textElement);
                
                // Cambio de estado
                toggle.addEventListener('change', function() {
                    updateToggleText(this, textElement);
                });
            }
        });
    }
    
    /**
     * Actualiza el texto del toggle
     */
    function updateToggleText(toggle, textElement) {
        textElement.textContent = toggle.checked ? 'Activo' : 'Inactivo';
    }
    
    /**
     * Inicializa animaciones de entrada
     */
    function initAnimations() {
        const cards = document.querySelectorAll('.stat-card, .dashboard-card, .role-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.animation = 'fadeInUp 0.5s ease-out forwards';
                        entry.target.style.opacity = '1';
                    }, index * 100);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        cards.forEach(card => {
            card.style.opacity = '0';
            observer.observe(card);
        });
        
        // Agregar keyframes
        if (!document.getElementById('dashboard-animations')) {
            const style = document.createElement('style');
            style.id = 'dashboard-animations';
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
            `;
            document.head.appendChild(style);
        }
    }
    
    /**
     * Ordenamiento de tablas
     */
    function initTableSorting() {
        const tables = document.querySelectorAll('.data-table');
        
        tables.forEach(table => {
            const headers = table.querySelectorAll('th');
            
            headers.forEach((header, index) => {
                header.style.cursor = 'pointer';
                header.addEventListener('click', function() {
                    sortTable(table, index);
                });
            });
        });
    }
    
    /**
     * Ordena una tabla por columna
     */
    function sortTable(table, columnIndex) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        const sortedRows = rows.sort((a, b) => {
            const aText = a.cells[columnIndex].textContent.trim();
            const bText = b.cells[columnIndex].textContent.trim();
            
            return aText.localeCompare(bText);
        });
        
        // Redibujar tabla
        tbody.innerHTML = '';
        sortedRows.forEach(row => tbody.appendChild(row));
    }
    
    /**
     * Auto-ocultar alertas después de 5 segundos
     */
    function autoHideAlerts() {
        const alerts = document.querySelectorAll('.alert');
        
        alerts.forEach(alert => {
            setTimeout(() => {
                alert.style.animation = 'slideUp 0.3s ease-out';
                setTimeout(() => alert.remove(), 300);
            }, 5000);
        });
        
        // Agregar animación
        if (!document.getElementById('alert-animations')) {
            const style = document.createElement('style');
            style.id = 'alert-animations';
            style.textContent = `
                @keyframes slideUp {
                    from {
                        opacity: 1;
                        transform: translateY(0);
                    }
                    to {
                        opacity: 0;
                        transform: translateY(-20px);
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    /**
     * Muestra una notificación tipo toast
     */
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = 'toast-notification';
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        const colors = {
            success: '#10B981',
            error: '#EF4444',
            warning: '#F59E0B',
            info: '#3B82F6'
        };
        
        notification.innerHTML = `
            <span style="font-size: 1.25rem;">${icons[type]}</span>
            <span>${message}</span>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${colors[type]};
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
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
        
        // Agregar animaciones
        if (!document.getElementById('toast-animations')) {
            const style = document.createElement('style');
            style.id = 'toast-animations';
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
    }
    
    /**
     * Confirmar acción
     */
    function confirmAction(message, callback) {
        if (confirm(message)) {
            callback();
        }
    }
    
    /**
     * Copiar al portapapeles
     */
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copiado al portapapeles', 'success');
        }).catch(() => {
            showNotification('Error al copiar', 'error');
        });
    }
    
    // Exponer funciones globalmente
    window.Dashboard = {
        showNotification,
        confirmAction,
        copyToClipboard
    };
    
})();