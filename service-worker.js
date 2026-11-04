// ============================================================
// IPTV Hero Pro TV - Service Worker
// Estratégia: cache-first para assets, network-first para API IPTV
// ============================================================
const CACHE_VERSION = 'v1';
const CACHE_STATIC = `iptv-hero-static-${CACHE_VERSION}`;
const CACHE_RUNTIME = `iptv-hero-runtime-${CACHE_VERSION}`;

const STATIC_ASSETS = [
    './',
    './index.html',
    './offline.html',
    './manifest.json',
    './vendor/hls.min.js',
    './icons/icon-192.png',
    './icons/icon-512.png',
    './icons/icon-512-maskable.png',
    './icons/favicon.png'
];

// ============ INSTALL ============
self.addEventListener('install', (event) => {
    console.log('[SW] Instalando...');
    event.waitUntil(
        caches.open(CACHE_STATIC)
            .then(cache => cache.addAll(STATIC_ASSETS))
            .then(() => self.skipWaiting())
            .catch(err => console.error('[SW] Falha ao cachear assets:', err))
    );
});

// ============ ACTIVATE ============
self.addEventListener('activate', (event) => {
    console.log('[SW] Ativando...');
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys
                .filter(k => k !== CACHE_STATIC && k !== CACHE_RUNTIME)
                .map(k => caches.delete(k))
            )
        ).then(() => self.clients.claim())
    );
});

// ============ FETCH ============
self.addEventListener('fetch', (event) => {
    const req = event.request;
    const url = new URL(req.url);

    // Ignora métodos não-GET
    if (req.method !== 'GET') return;

    // Ignora esquemas não HTTP(S)
    if (!url.protocol.startsWith('http')) return;

    // Requests para APIs IPTV (player_api, get.php, streams) → network-first sem cache
    if (
        url.pathname.includes('player_api.php') ||
        url.pathname.includes('get.php') ||
        url.pathname.endsWith('.m3u8') ||
        url.pathname.endsWith('.ts') ||
        url.pathname.endsWith('.mp4') ||
        url.pathname.endsWith('.mkv') ||
        url.hostname.includes('workers.dev')
    ) {
        event.respondWith(fetch(req).catch(() => new Response('', { status: 503 })));
        return;
    }

    // Navegação (HTML) → network-first com fallback offline
    if (req.mode === 'navigate') {
        event.respondWith(
            fetch(req)
                .then(resp => {
                    const copy = resp.clone();
                    caches.open(CACHE_RUNTIME).then(c => c.put(req, copy));
                    return resp;
                })
                .catch(() => caches.match(req).then(c => c || caches.match('./offline.html')))
        );
        return;
    }

    // Assets estáticos → cache-first
    event.respondWith(
        caches.match(req).then(cached => {
            if (cached) return cached;
            return fetch(req).then(resp => {
                if (resp && resp.status === 200 && resp.type === 'basic') {
                    const copy = resp.clone();
                    caches.open(CACHE_RUNTIME).then(c => c.put(req, copy));
                }
                return resp;
            }).catch(() => cached);
        })
    );
});