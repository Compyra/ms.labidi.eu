/* Network-first shell, cache-fallback offline. Version pairs with ?v= in index.html. */
"use strict";
var CACHE = "mshub-v14";
var ASSETS = [
  "./",
  "404.html",
  "style.css?v=14",
  "search.js?v=14",
  "app.js?v=14",
  "manifest.webmanifest",
  "icons/icon.svg",
  "data/data-commands-entra.js?v=14",
  "data/data-commands-intune.js?v=14",
  "data/data-commands-defender.js?v=14",
  "data/data-commands-sentinel.js?v=14",
  "data/data-commands-azure.js?v=14",
  "data/data-commands-m365.js?v=14",
  "data/data-commands-purview.js?v=14",
  "data/data-commands-power.js?v=14",
  "data/data-commands-windows.js?v=14",
  "data/data-commands-automation.js?v=14",
  "data/data-commands-licensing.js?v=14",
  "data/data-commands-msp.js?v=14",
  "data/data-commands-toolbox.js?v=14",
  "data/data-commands-mypages.js?v=14",
  "data/data-synonyms.js?v=14",
  "data/data-registry.js?v=14",
  "data/data-kql.js?v=14",
  "data/data-ps.js?v=14",
  "data/data-runbooks.js?v=14",
  "data/data-licensing.js?v=14",
  "data/data-meta.js?v=14"
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
