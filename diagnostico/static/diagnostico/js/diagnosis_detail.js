console.log('diagnosis_detail.js cargado');
// Exportar PDF (CU-019)
function exportDiagnosisPDF(diagnosisId) {
    window.open(`/diagnostico/export-pdf/${diagnosisId}/`, '_blank');
}
window.exportDiagnosisPDF = exportDiagnosisPDF;
// Funciones para validar diagnóstico
function validateDiagnosis(diagnosisId) {
    // Mostrar modal personalizado en vez de confirm
    showValidationModal();
    fetch(`/diagnostico/validate/${diagnosisId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        // No recargar, solo mostrar modal
        if (!data.success) {
            alert('Error: ' + data.error);
        }
    });
}

function showValidationModal() {
    let modal = document.getElementById('validation-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'validation-modal';
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100vw';
        modal.style.height = '100vh';
        modal.style.background = 'rgba(15,23,42,0.6)';
        modal.style.display = 'flex';
        modal.style.alignItems = 'center';
        modal.style.justifyContent = 'center';
        modal.style.zIndex = '9999';
        modal.innerHTML = `
            <div style="background:#1e293b; border-radius:10px; padding:2rem; min-width:320px; box-shadow:0 8px 32px rgba(0,0,0,0.25); position:relative; text-align:center;">
                <button id="close-validation-modal" style="position:absolute; top:1rem; right:1rem; background:none; border:none; color:#94a3b8; font-size:1.5rem; cursor:pointer;">&times;</button>
                <h2 style="color:#e2e8f0; margin-bottom:1rem;">Diagnóstico validado</h2>
                <div style="margin-top:1.5rem;">
                    <button id="close-validation-btn" class="btn-simulate" style="width:100px;">Cerrar</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        document.getElementById('close-validation-modal').onclick = closeValidationModal;
        document.getElementById('close-validation-btn').onclick = closeValidationModal;
    } else {
        modal.style.display = 'flex';
    }
}

function closeValidationModal() {
    let modal = document.getElementById('validation-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Función para descartar diagnóstico
function discardDiagnosis(diagnosisId) {
    if (confirm('¿Deseas descartar este diagnóstico?')) {
        fetch(`/diagnostico/discard/${diagnosisId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + data.error);
            }
        });
    }
}

// Obtener cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Auto-refresh para estados en procesamiento
document.addEventListener('DOMContentLoaded', function() {
    const statusElement = document.querySelector('.status-badge-large');
    if (statusElement && (statusElement.textContent.includes('Pendiente') || statusElement.textContent.includes('Procesando'))) {
        setInterval(checkDiagnosisStatus, 5000);
    }
});

// Verificar estado del diagnóstico
function checkDiagnosisStatus() {
    const diagnosisId = document.querySelector('[data-diagnosis-id]')?.dataset.diagnosisId;
    if (!diagnosisId) return;
    
    fetch(`/diagnostico/check-status/${diagnosisId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'COMPLETED' || data.status === 'FAILED') {
                location.reload();
            }
        });
}
