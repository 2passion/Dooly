// service-worker.js
// King Assistant OS v1.0 PWA

const CACHE_NAME = 'king-assistant-v3';
const URLS_TO_CACHE = [
  '/Dooly/',
  '/Dooly/index.html',
  '/Dooly/02_Task_v1.html',
  '/Dooly/03_SOP_v1.html',
  '/Dooly/04_FAQ_v1.html',
  '/Dooly/05_Notice_v1.html',
  '/Dooly/06_Dooly_v1.html',
  '/Dooly/07_Settings_v1.html',
  '/Dooly/data.js',
  '/Dooly/manifest.json',
  '/Dooly/icons/icon-192.png',
  '/Dooly/icons/icon-512.png'
];

// 설치: 모든 파일 캐시에 저장
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(URLS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// 활성화: 이전 캐시 삭제
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(name) {
          return name !== CACHE_NAME;
        }).map(function(name) {
          return caches.delete(name);
        })
      );
    })
  );
  self.clients.claim();
});

// 요청: 캐시 우선, 없으면 네트워크
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
