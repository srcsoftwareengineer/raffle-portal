self.addEventListener("install", (event) => {
  console.log("[StormPWA] Installed");
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  console.log("[StormPWA] Activated");
});

self.addEventListener("fetch", (event) => {
  event.respondWith(fetch(event.request));
});

