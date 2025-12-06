let deferredPrompt;
let isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;

function showInstallUI() {
    const installBtn = document.getElementById('pwa-install-button');
    const hintBtn = document.getElementById('pwa-install-hint');

    if (!isStandalone) {
        // Show navbar button on desktop
        if (installBtn) installBtn.style.display = 'inline-block';

        // Show floating hint on small screens
        if (hintBtn && window.innerWidth < 768) hintBtn.style.display = 'block';
    }
}

// Handle beforeinstallprompt
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallUI();

    const installBtn = document.getElementById('pwa-install-button');
    const hintBtn = document.getElementById('pwa-install-hint');

    [installBtn, hintBtn].forEach(btn => {
        if (btn) {
            btn.addEventListener('click', () => {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(choiceResult => {
                    if (choiceResult.outcome === 'accepted') console.log('User accepted the install');
                    deferredPrompt = null;
                    if (installBtn) installBtn.style.display = 'none';
                    if (hintBtn) hintBtn.style.display = 'none';
                });
            });
        }
    });
});

// Hide buttons if already installed
window.addEventListener('appinstalled', () => {
    const installBtn = document.getElementById('pwa-install-button');
    const hintBtn = document.getElementById('pwa-install-hint');
    if (installBtn) installBtn.style.display = 'none';
    if (hintBtn) hintBtn.style.display = 'none';
    isStandalone = true;
});

// Fallback for browsers without beforeinstallprompt
window.addEventListener('load', () => {
    setTimeout(() => {
        if (!deferredPrompt && !isStandalone) {
            const installBtn = document.getElementById('pwa-install-button');
            const hintBtn = document.getElementById('pwa-install-hint');
            const instructions = `
                📱 Install Diary App<br>
                <small style="font-weight:normal; font-size:10px; line-height:1.3;">
                    Chrome/Edge: Click ⊕ icon in address bar<br>
                    Firefox: Bookmark this page<br>
                    Safari (iOS): Share → Add to Home Screen<br>
                    Opera: Menu → Install App
                </small>
            `;
            if (installBtn) { installBtn.innerHTML = instructions; installBtn.style.display='inline-block'; }
            if (hintBtn && window.innerWidth < 768) { hintBtn.innerHTML = instructions; hintBtn.style.display='block'; }
        }
    }, 2000);
});
