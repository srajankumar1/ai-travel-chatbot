// Basic service worker to allow home-screen installation
self.addEventListener('fetch', function(event) {
    // Just forwards requests to Render directly
    event.respondWith(fetch(event.request));
});
