const CACHE_NAME = 'rural-learning-games-v2';
const PRECACHE = [
  '/',
  '/courses/',
  '/courses/games/',
  '/static/css/style.css',
  '/static/js/main.js',
];

// Install Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE)));
  self.skipWaiting();
});

// Activate Service Worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) => Promise.all(names.map((n) => n !== CACHE_NAME && caches.delete(n))))
  );
  self.clients.claim();
});

// Fetch event handler
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  const isGamesAsset = url.pathname.startsWith('/static/games/');
  const isStatic = url.pathname.startsWith('/static/');
  const isHtml = event.request.destination === 'document';

  // Cache-first for games and static assets
  if (isGamesAsset || isStatic) {
    event.respondWith(
      caches.match(event.request).then((cached) => cached || fetch(event.request).then((res) => {
        const copy = res.clone();
        caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));
        return res;
      }))
    );
    return;
  }

  // Network-first for HTML pages with offline fallback
  if (isHtml) {
    event.respondWith(
      fetch(event.request).then((res) => {
        const copy = res.clone();
        caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));
        return res;
      }).catch(() => caches.match(event.request) || caches.match('/courses/games/'))
    );
    return;
  }
});
// No background sync for now; focus on full offline play for games
