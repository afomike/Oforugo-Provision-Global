document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(el) {
            el.style.opacity = '0';
            el.style.transition = 'opacity 0.5s';
            setTimeout(function() { el.remove(); }, 500);
        });
    }, 5000);

    // Quantity buttons on cart page
    document.querySelectorAll('.qty-btn-minus').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var input = this.parentElement.querySelector('input[type="number"]');
            if (input && parseInt(input.value) > 1) input.value = parseInt(input.value) - 1;
        });
    });
    document.querySelectorAll('.qty-btn-plus').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var input = this.parentElement.querySelector('input[type="number"]');
            var max = parseInt(input.max || 999);
            if (input && parseInt(input.value) < max) input.value = parseInt(input.value) + 1;
        });
    });

    // Sort dropdown auto-submit
    var sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            var url = new URL(window.location.href);
            url.searchParams.set('sort', this.value);
            window.location.href = url.toString();
        });
    }

    // Highlight active nav
    var path = window.location.pathname;
    document.querySelectorAll('.nav-inner a').forEach(function(a) {
        if (a.getAttribute('href') === path) a.style.color = 'var(--green)';
    });
    document.querySelectorAll('.admin-nav a').forEach(function(a) {
        if (window.location.pathname.startsWith(a.getAttribute('href'))) a.classList.add('active');
    });
});
