// ===== THEME SELECTOR LOGIC (SEASONS) =====
let currentTheme = localStorage.getItem('theme') || 'winter'; // default to winter

function applyTheme(themeName) {
    document.documentElement.setAttribute('data-theme', themeName);
}

function updateThemeBadges() {
    document.querySelectorAll('.theme-badge').forEach(badge => {
        badge.textContent = '';
        badge.classList.remove('current');
    });
    const currentBadge = document.getElementById(`badge-${currentTheme}`);
    if (currentBadge) {
        currentBadge.textContent = 'Current';
        currentBadge.classList.add('current');
    }
    document.querySelectorAll('.theme-option').forEach(option => {
        option.classList.remove('active');
    });
    const activeOption = document.querySelector(`[data-theme="${currentTheme}"]`);
    if (activeOption) activeOption.classList.add('active');
}

// Optionally, expose setTheme globally for inline onclick handlers in the template
window.setTheme = setTheme;

function setTheme(themeName) {
    currentTheme = themeName;
    applyTheme(themeName);
    localStorage.setItem('theme', themeName);
    updateThemeBadges();

    const option = document.querySelector(`[data-theme="${themeName}"]`);
    if (option) {
        option.style.transform = 'scale(0.95)';
        setTimeout(() => { option.style.transform = 'scale(1)'; }, 150);
    }

    // Auto-close theme panel after selection
    setTimeout(() => {
        const panel = document.getElementById('theme-panel');
        const toggleBtn = document.querySelector('.theme-toggle-btn');
        if (panel && toggleBtn) {
            panel.style.display = 'none';
            toggleBtn.classList.remove('active');
        }
    }, 500);
}

function toggleThemeSelector() {
    const panel = document.getElementById('theme-panel');
    const toggleBtn = document.querySelector('.theme-toggle-btn');
    if (panel && toggleBtn) {
        if (panel.style.display === 'none' || panel.style.display === '') {
            panel.style.display = 'block';
            toggleBtn.classList.add('active');
        } else {
            panel.style.display = 'none';
            toggleBtn.classList.remove('active');
        }
    }
}

// Apply theme and update badges on page load
document.addEventListener('DOMContentLoaded', () => {
    applyTheme(currentTheme);
    updateThemeBadges();
});
