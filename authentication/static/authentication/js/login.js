/* JS extracted from login.html, uses name selectors so it works without template ids */

function togglePassword() {
    const passwordInput = document.querySelector('input[name="password"]');
    const toggleIcon = document.getElementById('toggleIcon');

    if (!passwordInput || !toggleIcon) return;

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.textContent = '🙈';
    } else {
        passwordInput.type = 'password';
        toggleIcon.textContent = '👁️';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInput = document.querySelector('input[name="password"]');

    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.value)) {
                this.classList.add('error');
            } else {
                this.classList.remove('error');
            }
        });

        // Auto-focus if present
        emailInput.focus();
    }

    if (passwordInput) {
        passwordInput.addEventListener('blur', function() {
            if (this.value.length < 8) {
                this.classList.add('error');
            } else {
                this.classList.remove('error');
            }
        });
    }

    // Optional: handle form submit validations here if needed
    if (form) {
        form.addEventListener('submit', function(e) {
            // Simple client-side validation example: prevent submit if invalid
            if (emailInput && passwordInput) {
                const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value);
                const passwordValid = passwordInput.value.length >= 8;
                if (!emailValid || !passwordValid) {
                    e.preventDefault();
                    if (!emailValid) emailInput.classList.add('error');
                    if (!passwordValid) passwordInput.classList.add('error');
                }
            }
        });
    }
});
