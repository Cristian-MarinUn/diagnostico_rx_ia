/* ================================ */
/* ARCHIVO: users/static/users/js/dashboard.js */
/* ================================ */

// Inicialización del dashboard
document.addEventListener('DOMContentLoaded', function() {
    initAnimations();
    initStatCards();
    initActionCards();
    initActivityItems();
    updateTimeStamps();
    
    // Actualizar timestamps cada minuto
    setInterval(updateTimeStamps, 60000);
});

// Animaciones de entrada
function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    // Observar elementos para animación
    const animatedElements = document.querySelectorAll(
        '.stat-card, .action-card, .activity-item'
    );
    
    animatedElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = `all 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.05}s`;
        observer.observe(el);
    });
}

// Interacción con las tarjetas de estadísticas
function initStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Animar el icono
            const icon = this.querySelector('.stat-icon');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(-5deg)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.stat-icon');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });

        // Efecto de click
        card.addEventListener('click', function(e) {
            if (!e.target.closest('a')) {
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            }
        });
    });

    // Animar valores de estadísticas
    animateStatValues();
}

// Animar números de estadísticas
function animateStatValues() {
    const statValues = document.querySelectorAll('.stat-value');
    
    statValues.forEach(element => {
        const target = parseFloat(element.textContent.replace(/[^0-9.]/g, ''));
        
        if (!isNaN(target) && target > 0) {
            let current = 0;
            const increment = target / 50; // 50 pasos
            const duration = 1000; // 1 segundo
            const stepTime = duration / 50;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                
                // Formatear el número
                let displayValue = Math.floor(current);
                if (element.textContent.includes('%')) {
                    displayValue = current.toFixed(1) + '%';
                } else {
                    displayValue = displayValue.toLocaleString();
                }
                
                element.textContent = displayValue;
            }, stepTime);
        }
    });
}

// Interacción con action cards
function initActionCards() {
    const actionCards = document.querySelectorAll('.action-card');
    
    actionCards.forEach(card => {
        // Efecto de partículas en hover (opcional)
        card.addEventListener('mouseenter', function() {
            createParticleEffect(this);
        });

        // Efecto ripple en click
        card.addEventListener('click', function(e) {
            createRippleEffect(e, this);
        });
    });
}

// Crear efecto de partículas
function createParticleEffect(element) {
    const rect = element.getBoundingClientRect();
    
    for (let i = 0; i < 5; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(102, 126, 234, 0.6);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            left: ${rect.left + rect.width / 2}px;
            top: ${rect.top + rect.height / 2}px;
        `;
        
        document.body.appendChild(particle);
        
        const angle = (Math.PI * 2 * i) / 5;
        const velocity = 2;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;
        
        let x = 0;
        let y = 0;
        let opacity = 1;
        
        const animate = () => {
            x += vx;
            y += vy;
            opacity -= 0.02;
            
            particle.style.transform = `translate(${x}px, ${y}px)`;
            particle.style.opacity = opacity;
            
            if (opacity > 0) {
                requestAnimationFrame(animate);
            } else {
                particle.remove();
            }
        };
        
        requestAnimationFrame(animate);
    }
}

// Crear efecto ripple
function createRippleEffect(e, element) {
    const ripple = document.createElement('div');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        left: ${x}px;
        top: ${y}px;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
}

// Añadir estilos para la animación ripple
if (!document.getElementById('ripple-styles')) {
    const style = document.createElement('style');
    style.id = 'ripple-styles';
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// Interacción con items de actividad
function initActivityItems() {
    const activityItems = document.querySelectorAll('.activity-item');
    
    activityItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.activity-icon');
            if (icon) {
                icon.style.transform = 'scale(1.15) rotate(5deg)';
            }
        });
        
        item.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.activity-icon');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });
}

// Actualizar timestamps relativos
function updateTimeStamps() {
    const timeElements = document.querySelectorAll('[data-timestamp]');
    
    timeElements.forEach(element => {
        const timestamp = parseInt(element.dataset.timestamp);
        if (!isNaN(timestamp)) {
            element.textContent = getRelativeTime(timestamp);
        }
    });
}

// Obtener tiempo relativo
function getRelativeTime(timestamp) {
    const now = Date.now();
    const diff = now - timestamp;
    
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (seconds < 60) return 'Hace un momento';
    if (minutes < 60) return `Hace ${minutes} min`;
    if (hours < 24) return `Hace ${hours}h`;
    if (days < 7) return `Hace ${days} días`;
    if (days < 30) return `Hace ${Math.floor(days / 7)} semanas`;
    if (days < 365) return `Hace ${Math.floor(days / 30)} meses`;
    return `Hace ${Math.floor(days / 365)} años`;
}

// Actualizar estadísticas en tiempo real (simulado)
function updateStatsRealTime() {
    // Esta función se puede conectar a WebSockets para datos en tiempo real
    setInterval(() => {
        const statChanges = document.querySelectorAll('.stat-change');
        statChanges.forEach(change => {
            // Añadir pulso visual cuando hay cambios
            change.style.animation = 'pulse 0.5s ease-in-out';
            setTimeout(() => {
                change.style.animation = '';
            }, 500);
        });
    }, 30000); // Cada 30 segundos
}

// Filtros para la tabla de usuarios (si existe)
function initTableFilters() {
    const searchInput = document.querySelector('.table-search');
    const roleFilter = document.querySelector('.role-filter');
    const statusFilter = document.querySelector('.status-filter');
    
    if (searchInput) {
        searchInput.addEventListener('input', filterTable);
    }
    
    if (roleFilter) {
        roleFilter.addEventListener('change', filterTable);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterTable);
    }
}

function filterTable() {
    const searchTerm = document.querySelector('.table-search')?.value.toLowerCase() || '';
    const roleFilter = document.querySelector('.role-filter')?.value || 'all';
    const statusFilter = document.querySelector('.status-filter')?.value || 'all';
    
    const rows = document.querySelectorAll('.users-table tbody tr');
    
    rows.forEach(row => {
        const name = row.querySelector('.user-name')?.textContent.toLowerCase() || '';
        const email = row.querySelector('.user-email')?.textContent.toLowerCase() || '';
        const role = row.querySelector('.badge')?.textContent.toLowerCase() || '';
        const status = row.querySelector('.badge-success, .badge-danger')?.textContent.toLowerCase() || '';
        
        const matchesSearch = name.includes(searchTerm) || email.includes(searchTerm);
        const matchesRole = roleFilter === 'all' || role.includes(roleFilter.toLowerCase());
        const matchesStatus = statusFilter === 'all' || status.includes(statusFilter.toLowerCase());
        
        if (matchesSearch && matchesRole && matchesStatus) {
            row.style.display = '';
            row.style.animation = 'fadeIn 0.3s ease-out';
        } else {
            row.style.display = 'none';
        }
    });
}

// Confirmación para acciones destructivas
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Manejar clicks en botones de tabla
document.addEventListener('click', function(e) {
    // Botón de eliminar/desactivar
    if (e.target.closest('.btn-danger')) {
        const btn = e.target.closest('.btn-danger');
        if (btn.title?.includes('Desactivar') || btn.title?.includes('Eliminar')) {
            e.preventDefault();
            confirmAction(
                '¿Estás seguro de que deseas realizar esta acción?',
                () => {
                    // Aquí iría la lógica de desactivación/eliminación
                    console.log('Acción confirmada');
                }
            );
        }
    }
});

// Notificaciones toast
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: calc(var(--navbar-height) + 1rem);
        right: 1rem;
        padding: 1rem 1.5rem;
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 0.875rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 9999;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Añadir estilos para las animaciones de toast
if (!document.getElementById('toast-styles')) {
    const style = document.createElement('style');
    style.id = 'toast-styles';
    style.textContent = `
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100%);
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
                transform: translateX(100%);
            }
        }
    `;
    document.head.appendChild(style);
}

// Exportar funciones útiles
window.dashboardUtils = {
    showToast,
    confirmAction,
    updateStatsRealTime,
    getRelativeTime
};