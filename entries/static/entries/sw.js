// Service Worker for offline functionality
const CACHE_NAME = 'diary-app-v1';
const STATIC_CACHE = 'diary-static-v1';
const DYNAMIC_CACHE = 'diary-dynamic-v1';

// Files to cache for offline use
const STATIC_FILES = [
  '/',
  '/static/entries/css/diary.css',
  '/accounts/login/',
  '/entries/',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap'
];

// Install event - cache static files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('Caching static files');
        return cache.addAll(STATIC_FILES);
      })
      .catch(err => console.log('Cache install failed:', err))
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', event => {
  const { request } = event;
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Handle static files
  if (request.url.includes('/static/') || STATIC_FILES.includes(request.url)) {
    event.respondWith(
      caches.match(request)
        .then(response => {
          return response || fetch(request);
        })
    );
    return;
  }

  // Handle dynamic content (entries, pages)
  event.respondWith(
    caches.match(request)
      .then(response => {
        if (response) {
          return response;
        }
        
        return fetch(request)
          .then(fetchResponse => {
            // Don't cache if not a success response
            if (!fetchResponse || fetchResponse.status !== 200 || fetchResponse.type !== 'basic') {
              return fetchResponse;
            }

            // Clone the response
            const responseToCache = fetchResponse.clone();

            caches.open(DYNAMIC_CACHE)
              .then(cache => {
                cache.put(request, responseToCache);
              });

            return fetchResponse;
          })
          .catch(() => {
            // If offline, show offline page for HTML requests
            if (request.headers.get('accept').includes('text/html')) {
              return caches.match('/');
            }
          });
      })
  );
});

// Background sync for offline entry creation
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync-diary-entry') {
    event.waitUntil(syncOfflineEntries());
  }
});

// Sync offline entries when back online
function syncOfflineEntries() {
  return new Promise((resolve, reject) => {
    // Get offline entries from IndexedDB and sync them
    // This would integrate with your form submission logic
    console.log('Syncing offline diary entries...');
    resolve();
  });
}

// Push notifications for writing reminders
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'Time to write in your diary!',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      url: '/',
      timestamp: Date.now()
    },
    actions: [
      {
        action: 'write',
        title: 'Write Entry',
        icon: '/static/icons/write-icon.png'
      },
      {
        action: 'dismiss',
        title: 'Later',
        icon: '/static/icons/dismiss-icon.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Diary Reminder', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'write') {
    event.waitUntil(
      clients.openWindow('/entries/new/')
    );
  } else if (event.action === 'dismiss') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});
