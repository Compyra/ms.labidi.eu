/* Network-first shell, cache-fallback offline. Version pairs with ?v= in index.html. */
"use strict";
var CACHE = "__CACHE__";
var ASSETS = [
__ASSETS__
];

self.addEventListener("install", function (ev) {
  ev.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(ASSETS); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (ev) {
  ev.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) {
        return k.indexOf("mshub-") === 0 && k !== CACHE;
      }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (ev) {
  var req = ev.request;
  var url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== self.location.origin) { return; }
  if (req.mode === "navigate") {
    ev.respondWith(
      fetch(req).then(function (res) {
        if (res.ok && (url.pathname === "/" || url.pathname === "/index.html")) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put("./", copy); });
        }
        return res;
      }).catch(function () {
        return caches.match("./").then(function (hit) {
          return hit || caches.match("404.html");
        });
      })
    );
    return;
  }
  ev.respondWith(
    caches.match(req, { ignoreSearch: false }).then(function (hit) {
      if (hit) { return hit; }
      return fetch(req).then(function (res) {
        if (res.ok && url.search.indexOf("v=") >= 0) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
        }
        return res;
      });
    })
  );
});
