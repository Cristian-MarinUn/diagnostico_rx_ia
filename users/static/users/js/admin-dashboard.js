/* ================================ */
/* ARCHIVO: users/static/users/js/admin-dashboard.js */
/* ================================ */

// Funcionalidades específicas del dashboard de administrador
document.addEventListener('DOMContentLoaded', function() {
    initUserManagement();
    initCharts();
    initSystemMonitoring();
    initBulkActions();
});

// Gestión de usuarios
function initUserManagement() {
    const createUserBtn = document.querySelector('[href*="nuevo-usuario"]');
    const editButtons = document.querySelectorAll('[title*="Editar"]');
    const deleteButtons = document.querySelectorAll('[title*="Desactivar"]');
    
    // Botón crear usuario
    if (createUserBtn) {
        createUserBtn.addEventListener('click', function(e) {
            // Aquí puedes abrir un modal o redirigir
            console.log('Crear nuevo usuario');
        });
    }
    
    // Botones de editar
    editButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const row = this.closest('tr');
            const userName = row.querySelector('.user-name')?.textContent;
            
            if (confirm(`¿Deseas editar el usuario ${userName}?`)) {
                // Lógica para editar usuario
                console.log('Editar usuario:', userName);
            }
        });
    });
    
    // Botones de eliminar/desactivar
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const row = this.closest('tr');
            const userName = row.querySelector('.user-name')?.textContent;
            
            if (confirm(`¿Estás seguro de desactivar al usuario ${userName}?`)) {
                // Animación de eliminación
                row.style.transition = 'all 0.3s ease-out';
                row.style.opacity = '0';
                row.style.transform = 'translateX(-20px)';
                
                setTimeout(() => {
                    row.remove();
                    window.dashboardUtils.showToast(
                        `Usuario ${userName} desactivado correctamente`,
                        'success'
                    );
                }, 300);
            }
        });
    });
}

// Inicializar gráficos (usando Chart.js si está disponible)
function initCharts() {
    // Gráfico de usuarios por rol
    createRoleDistributionChart();
    
    // Gráfico de actividad por fecha
    createActivityTimelineChart();
    
    // Gráfico de precisión del sistema
    createAccuracyChart();
}

// Gráfico de distribución de roles
function createRoleDistributionChart() {
    const chartContainer = document.getElementById('role-distribution-chart');
    if (!chartContainer) return;
    
    // Ejemplo con datos simulados
    const data = {
        medicos: 15,
        tecnicos: 22,
        admin: 3
    };
    
    // Crear visualización simple con CSS
    const total = data.medicos + data.tecnicos + data.admin;
    
    const html = `
        <div class="chart-simple">
            <div class="chart-bar" style="width: ${(data.medicos/total)*100}%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <span class="chart-label">Médicos: ${data.medicos}</span>
            </div>
            <div class="chart-bar" style="width: ${(data.tecnicos/total)*100}%; background: linear-gradient(135deg, #10b981 0%, #34d399 100%);">
                <span class="chart-label">Técnicos: ${data.tecnicos}</span>
            </div>
            <div class="chart-bar" style="width: ${(data.admin/total)*100}%; background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);">
                <span class="chart-label">Admin: ${data.admin}</span>
            </div>
        </div>
    `;
    
    chartContainer.innerHTML = html;
}

// Gráfico de línea de tiempo de actividad
function createActivityTimelineChart() {
    const chartContainer = document.getElementById('activity-timeline-chart');
    if (!chartContainer) return;
    
    // Datos de ejemplo de los últimos 7 días
    const days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
    const values = [45, 52, 38, 65, 70, 55, 48];
    const maxValue = Math.max(...values);
    
    const html = `
        <div class="timeline-chart">
            ${days.map((day, index) => `
                <div class="timeline-bar-container">
                    <div class="timeline-bar" 
                         style="height: ${(values[index]/maxValue)*100}%; 
                                background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);"
                         data-value="${values[index]}">
                    </div>
                    <span class="timeline-label">${day}</span>
                </div>
            `).join('')}
        </div>
    `;
    
    chartContainer.innerHTML = html;
    
    // Añadir hover effects
    const bars = chartContainer.querySelectorAll('.timeline-bar');
    bars.forEach(bar => {
        bar.addEventListener('mouseenter', function() {
            const value = this.dataset.value;
            this.style.opacity = '0.8';
            
            // Mostrar tooltip
            const tooltip = document.createElement('div');
            tooltip.className = 'chart-tooltip';
            tooltip.textContent = `${value} diagnósticos`;
            tooltip.style.cssText = `
                position: absolute;
                top: -30px;
                left: 50%;
                transform: translateX(-50%);
                padding: 0.5rem 1rem;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                border-radius: 0.5rem;
                font-size: 0.875rem;
                white-space: nowrap;
                pointer-events: none;
            `;
            this.style.position = 'relative';
            this.appendChild(tooltip);
        });
        
        bar.addEventListener('mouseleave', function() {
            this.style.opacity = '1';
            const tooltip = this.querySelector('.chart-tooltip');
            if (tooltip) tooltip.remove();
        });
    });
}

// Gráfico de precisión del sistema
function createAccuracyChart() {
    const chartContainer = document.getElementById('accuracy-chart');
    if (!chartContainer) return;
    
    const accuracy = 96.8; // Porcentaje de precisión
    
    const html = `
        <div class="accuracy-gauge">
            <div class="gauge-background">
                <div class="gauge-fill" style="width: ${accuracy}%; background: linear-gradient(90deg, #10b981 0%, #34d399 100%);"></div>
            </div>
            <div class="gauge-value">
                <span class="gauge-percentage">${accuracy}%</span>
                <span class="gauge-label">Precisión del Sistema</span>
            </div>
        </div>
    `;
    
    chartContainer.innerHTML = html;
    
    // Animar el llenado
    const gaugeFill = chartContainer.querySelector('.gauge-fill');
    if (gaugeFill) {
        gaugeFill.style.width = '0%';
        setTimeout(() => {
            gaugeFill.style.transition = 'width 1.5s cubic-bezier(0.4, 0, 0.2, 1)';
            gaugeFill.style.width = `${accuracy}%`;
        }, 100);
    }
}

// Añadir estilos para los gráficos
if (!document.getElementById('chart-styles')) {
    const style = document.createElement('style');
    style.id = 'chart-styles';
    style.textContent = `
        .chart-simple {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            padding: 1rem;
        }
        
        .chart-bar {
            height: 40px;
            border-radius: 0.75rem;
            display: flex;
            align-items: center;
            padding: 0 1rem;
            color: white;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .chart-bar:hover {
            transform: translateX(8px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
        
        .timeline-chart {
            display: flex;
            justify-content: space-around;
            align-items: flex-end;
            height: 200px;
            padding: 1rem;
            gap: 0.75rem;
        }
        
        .timeline-bar-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }
        
        .timeline-bar {
            width: 100%;
            border-radius: 0.5rem 0.5rem 0 0;
            transition: all 0.3s;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            min-height: 20px;
        }
        
        .timeline-bar:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        
        .timeline-label {
            font-size: 0.8125rem;
            color: var(--text-secondary);
            font-weight: 600;
        }
        
        .accuracy-gauge {
            padding: 2rem;
        }
        
        .gauge-background {
            height: 40px;
            background: rgba(51, 65, 85, 0.4);
            border-radius: 9999px;
            overflow: hidden;
            margin-bottom: 1.5rem;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .gauge-fill {
            height: 100%;
            border-radius: 9999px;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
        }
        
        .gauge-value {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }
        
        .gauge-percentage {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .gauge-label {
            font-size: 1rem;
            color: var(--text-secondary);
            font-weight: 600;
        }
    `;
    document.head.appendChild(style);
}

// Monitoreo del sistema en tiempo real
function initSystemMonitoring() {
    // Simular actualizaciones en tiempo real
    setInterval(updateSystemMetrics, 5000);
}

function updateSystemMetrics() {
    // Actualizar métricas del sistema
    const metrics = {
        cpu: Math.random() * 100,
        memory: Math.random() * 100,
        disk: Math.random() * 100
    };
    
    // Aquí puedes actualizar indicadores visuales
    console.log('System metrics updated:', metrics);
}

// Acciones en lote
function initBulkActions() {
    const selectAllCheckbox = document.getElementById('select-all-users');
    const userCheckboxes = document.querySelectorAll('.user-checkbox');
    const bulkActionBtn = document.getElementById('bulk-action-btn');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            userCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActionButton();
        });
    }
    
    userCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateBulkActionButton);
    });
    
    if (bulkActionBtn) {
        bulkActionBtn.addEventListener('click', performBulkAction);
    }
}

function updateBulkActionButton() {
    const checkedBoxes = document.querySelectorAll('.user-checkbox:checked');
    const bulkActionBtn = document.getElementById('bulk-action-btn');
    
    if (bulkActionBtn) {
        bulkActionBtn.textContent = `Acciones (${checkedBoxes.length})`;
        bulkActionBtn.disabled = checkedBoxes.length === 0;
    }
}

function performBulkAction() {
    const checkedBoxes = document.querySelectorAll('.user-checkbox:checked');
    const selectedUsers = Array.from(checkedBoxes).map(cb => {
        return cb.closest('tr').querySelector('.user-name').textContent;
    });
    
    if (confirm(`¿Deseas realizar esta acción sobre ${selectedUsers.length} usuarios?`)) {
        window.dashboardUtils.showToast(
            `Acción aplicada a ${selectedUsers.length} usuarios`,
            'success'
        );
    }
}

// Exportar reportes
function exportReport(format = 'pdf') {
    window.dashboardUtils.showToast('Generando reporte...', 'info');
    
    // Simular generación de reporte
    setTimeout(() => {
        window.dashboardUtils.showToast(
            `Reporte ${format.toUpperCase()} generado exitosamente`,
            'success'
        );
    }, 2000);
}

// Buscar usuarios con debounce
let searchTimeout;
function searchUsers(query) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        // Realizar búsqueda
        console.log('Buscando:', query);
    }, 500);
}

// Añadir event listener para búsqueda si existe el input
const searchInput = document.getElementById('user-search');
if (searchInput) {
    searchInput.addEventListener('input', function(e) {
        searchUsers(e.target.value);
    });
}

// Exportar funciones
window.adminDashboard = {
    exportReport,
    searchUsers,
    updateSystemMetrics
};