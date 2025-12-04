// Service Worker for My Personal Diary PWA
const STATIC_CACHE = 'diary-static-v2';
const DYNAMIC_CACHE = 'diary-dynamic-v2';
const OFFLINE_PAGE = '/offline/';

// Files to cache for offline use
const STATIC_FILES = [
    '/',
    '/entries/',
    '/accounts/login/',
    '/static/entries/css/diary.css',
    '/static/entries/css/components.css',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap',
    '/static/entries/icons/icon-192x192.png',
    '/static/entries/icons/icon-512x512.png'
];

// Install Event - Cache static files
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(STATIC_CACHE).then(cache => {
            console.log('[SW] Caching static files');
            return cache.addAll(STATIC_FILES);
        })
    );
});

// Activate Event - Clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.filter(key => ![STATIC_CACHE, DYNAMIC_CACHE].includes(key))
                    .map(key => caches.delete(key))
            );
        })
    );
});

// Fetch Event - Serve from cache when offline
self.addEventListener('fetch', event => {
    const request = event.request;

    if (request.method !== 'GET') return;

    // Try static cache first
    if (STATIC_FILES.includes(request.url) || request.url.includes('/static/')) {
        event.respondWith(
            caches.match(request).then(resp => resp || fetch(request))
        );
        return;
    }

    // Dynamic content caching
    event.respondWith(
        fetch(request).then(fetchResp => {
            if (!fetchResp || fetchResp.status !== 200 || fetchResp.type !== 'basic') return fetchResp;
            const clone = fetchResp.clone();
            caches.open(DYNAMIC_CACHE).then(cache => cache.put(request, clone));
            return fetchResp;
        }).catch(() => {
            return caches.match(request).then(resp => resp || caches.match(OFFLINE_PAGE));
        })
    );
});

// Background sync placeholder for offline entries
self.addEventListener('sync', event => {
    if (event.tag === 'sync-diary-entry') {
        event.waitUntil(syncOfflineEntries());
    }
});
function syncOfflineEntries() {
    console.log('[SW] Syncing offline diary entries...');
    return Promise.resolve();
}

// Push Notifications
self.addEventListener('push', event => {
    const options = {
        body: event.data ? event.data.text() : 'Time to write in your diary!',
        icon: '/static/entries/icons/icon-192x192.png',
        badge: '/static/entries/icons/icon-192x192.png',
        vibrate: [200, 100, 200],
        data: { url: '/', timestamp: Date.now() },
        actions: [
            { action: 'write', title: 'Write Entry', icon: '/static/entries/icons/icon-192x192.png' },
            { action: 'dismiss', title: 'Later', icon: '/static/entries/icons/icon-192x192.png' }
        ]
    };
    event.waitUntil(self.registration.showNotification('Diary Reminder', options));
});

// Notification Click
self.addEventListener('notificationclick', event => {
    event.notification.close();
    let url = '/';
    if (event.action === 'write') url = '/entries/new/';
    event.waitUntil(clients.openWindow(url));
});
