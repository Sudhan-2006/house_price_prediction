// Initialize Bootstrap tooltips, popovers, etc. (optional)
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (el) {
        return new bootstrap.Tooltip(el);
    });
});