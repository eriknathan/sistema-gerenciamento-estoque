document.addEventListener("DOMContentLoaded", function () {

    // ---- Theme Toggle ----
    const THEME_KEY = 'sge-theme';

    function getThemeIcon(theme) {
        return theme === 'light' ? 'bi-sun-fill' : 'bi-moon-stars-fill';
    }

    function applyTheme(theme) {
        if (theme === 'light') {
            document.body.classList.add('light-mode');
        } else {
            document.body.classList.remove('light-mode');
        }
        // Update all theme toggle icons
        document.querySelectorAll('#theme-toggle i, #sidebar-theme-toggle i').forEach(icon => {
            icon.className = `bi ${getThemeIcon(theme)}`;
        });
    }

    function toggleTheme(e) {
        if (e) e.preventDefault();
        const current = document.body.classList.contains('light-mode') ? 'light' : 'dark';
        const next = current === 'light' ? 'dark' : 'light';
        localStorage.setItem(THEME_KEY, next);
        applyTheme(next);
    }

    // Attach to both buttons
    document.querySelectorAll('#theme-toggle, #sidebar-theme-toggle').forEach(btn => {
        btn.addEventListener('click', toggleTheme);
    });

    // Restore saved theme
    applyTheme(localStorage.getItem(THEME_KEY) || 'dark');

    // ---- Sidebar Active State based on URL ----
    const currentPath = window.location.pathname;
    const pathRoot = currentPath.split('/').filter(Boolean)[0] || '';

    const sectionMap = {
        'products': 'products',
        'brands': 'brands',
        'categories': 'categories',
        'suppliers': 'suppliers',
        'inflows': 'inflows',
        'outflows': 'outflows',
    };

    const activeSection = sectionMap[pathRoot];
    if (activeSection) {
        document.querySelectorAll('.sidebar .nav-link[data-page]').forEach(link => {
            link.classList.remove('active');
        });
        const activeLink = document.querySelector(`.sidebar .nav-link[data-page="${activeSection}"]`);
        if (activeLink) activeLink.classList.add('active');
    }

    // ---- Bootstrap Toast auto-dismiss ----
    document.querySelectorAll('.toast.show').forEach(toastEl => {
        const toast = bootstrap.Toast.getOrCreateInstance(toastEl, {
            autohide: true,
            delay: 5000,
        });
        toast.show();
    });

});