// Funciones para validar diagnóstico
function validateDiagnosis(diagnosisId) {
    if (confirm('¿Deseas validar este diagnóstico?')) {
        fetch(`/diagnostico/validate/${diagnosisId}/`, {
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
