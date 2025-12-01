// Auto-submit del filtro
document.addEventListener('DOMContentLoaded', function() {
    const filterSelect = document.querySelector('.filter-select');
    if (filterSelect) {
        filterSelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
});
