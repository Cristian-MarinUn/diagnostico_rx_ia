// Autocompletado de pacientes
(function() {
    'use strict';
    
    const searchInput = document.getElementById('searchInput');
    const dropdown = document.getElementById('autocompleteDropdown');
    const autocompleteList = document.getElementById('autocompleteList');
    let debounceTimer;
    
    // Mostrar autocompletado al escribir
    searchInput.addEventListener('input', function(e) {
        const query = this.value.trim();
        
        clearTimeout(debounceTimer);
        
        if (query.length < 1) {
            dropdown.style.display = 'none';
            return;
        }
        
        debounceTimer = setTimeout(() => {
            fetchAutoComplete(query);
        }, 300);
    });
    
    // Cerrar dropdown al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-input-wrapper')) {
            dropdown.style.display = 'none';
        }
    });
    
    // Permitir navegación con teclado
    searchInput.addEventListener('keydown', function(e) {
        const items = dropdown.querySelectorAll('.autocomplete-item');
        const activeItem = dropdown.querySelector('.autocomplete-item.active');
        let nextItem;
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            nextItem = activeItem ? activeItem.nextElementSibling : items[0];
            if (nextItem) setActive(nextItem);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            nextItem = activeItem ? activeItem.previousElementSibling : items[items.length - 1];
            if (nextItem) setActive(nextItem);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (activeItem) {
                const link = activeItem.querySelector('a');
                if (link) window.location.href = link.href;
            }
        }
    });
    
    function setActive(item) {
        document.querySelectorAll('.autocomplete-item').forEach(el => {
            el.classList.remove('active');
        });
        item.classList.add('active');
    }
    
    function fetchAutoComplete(query) {
        fetch(`/diagnostico/api/autocomplete-patients/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                renderAutoComplete(data.patients);
            })
            .catch(error => {
                console.error('Error en autocompletado:', error);
            });
    }
    
    function renderAutoComplete(patients) {
        autocompleteList.innerHTML = '';
        
        if (patients.length === 0) {
            autocompleteList.innerHTML = '<div class="autocomplete-empty">No se encontraron pacientes</div>';
            dropdown.style.display = 'block';
            return;
        }
        
        patients.forEach(patient => {
            const li = document.createElement('li');
            li.className = 'autocomplete-item';
            
            // Obtener iniciales para avatar
            const initials = (patient.name.split(' ')[0][0] + patient.name.split(' ').pop()[0]).toUpperCase();
            
            li.innerHTML = `
                <a href="${patient.url}">
                    <div class="autocomplete-avatar">${initials}</div>
                    <div class="autocomplete-content">
                        <div class="autocomplete-name">${patient.name}</div>
                        <div class="autocomplete-details">
                            <span>ID: ${patient.identification}</span>
                            <span>•</span>
                            <span>${patient.age} años</span>
                            <span>•</span>
                            <span>${patient.gender}</span>
                        </div>
                        <div class="autocomplete-images">🖼️ ${patient.image_types} (+${patient.image_count} imágenes)</div>
                    </div>
                </a>
            `;
            
            li.addEventListener('click', function() {
                const link = this.querySelector('a');
                if (link) {
                    // Guardar datos del paciente en sessionStorage
                    sessionStorage.setItem('selected_patient_id', patient.id);
                    sessionStorage.setItem('selected_patient_name', patient.name);
                    sessionStorage.setItem('selected_patient_identification', patient.identification);
                    sessionStorage.setItem('selected_patient_age', patient.age);
                    sessionStorage.setItem('selected_patient_gender', patient.gender);
                    sessionStorage.setItem('selected_patient_phone', patient.phone || '');
                    sessionStorage.setItem('selected_patient_email', patient.email || '');
                    
                    console.log('Paciente guardado en sessionStorage:', {
                        id: patient.id,
                        name: patient.name,
                        identification: patient.identification
                    });
                    
                    window.location.href = link.href;
                }
            });
            
            autocompleteList.appendChild(li);
        });
        
        dropdown.style.display = 'block';
    }
})();

// Guardar paciente en sessionStorage cuando se hace click en botones de acción
document.addEventListener('DOMContentLoaded', function() {
    const patientActionButtons = document.querySelectorAll('.patient-action-btn');
    
    patientActionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Obtener los datos del paciente de la tarjeta
            const card = this.closest('.patient-card');
            if (card) {
                const nameEl = card.querySelector('.patient-name');
                const idEl = card.querySelector('.patient-id');
                
                if (nameEl && idEl) {
                    const name = nameEl.textContent.trim();
                    const id = idEl.textContent.replace('ID: ', '').trim();
                    
                    // Guardar en sessionStorage
                    sessionStorage.setItem('selected_patient_id', id);
                    sessionStorage.setItem('selected_patient_name', name);
                    
                    console.log('Paciente guardado desde tarjeta:', { id, name });
                }
            }
        });
    });
});
