// Validar al menos una imagen seleccionada
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const selectedImages = document.querySelectorAll('input[name="images"]:checked').length;
            if (selectedImages === 0) {
                e.preventDefault();
                alert('Debes seleccionar al menos una imagen para solicitar un diagnóstico.');
            }
        });
    }
});

// Habilitar/deshabilitar botón según selección
function updateSubmitButton() {
    const selectedImages = document.querySelectorAll('input[name="images"]:checked').length;
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = selectedImages === 0;
    }
}

// Escuchar cambios en checkboxes
document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('input[name="images"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSubmitButton);
    });
    updateSubmitButton();
});
