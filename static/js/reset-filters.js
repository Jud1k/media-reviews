document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('[data-reset-filters]')) {
            window.location.href = window.location.pathname;
        }
    });
});