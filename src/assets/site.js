/**
 * Shared client-side helpers for orangejuiceapplications.com
 */
(function () {
  "use strict";

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  onReady(function () {
    // Warn if the main stylesheet failed to load (CDN/host misconfiguration).
    var stylesheet = document.querySelector('link[rel="stylesheet"][href*="style.css"]');
    if (!stylesheet) return;

    var cssOk = false;
    for (var i = 0; i < document.styleSheets.length; i++) {
      var sheet = document.styleSheets[i];
      try {
        if (sheet.href && sheet.href.indexOf("style.css") !== -1 && sheet.cssRules && sheet.cssRules.length > 0) {
          cssOk = true;
          break;
        }
      } catch (e) {
        cssOk = true;
        break;
      }
    }

    if (!cssOk) {
      var banner = document.createElement("div");
      banner.className = "site-banner site-banner-warning";
      banner.setAttribute("role", "alert");
      banner.textContent = "Some page styles could not be loaded. Try refreshing, or clear your browser cache.";
      document.body.insertBefore(banner, document.body.firstChild);
    }

    // Broken image fallback for app icon references.
    document.querySelectorAll("img.app-icon-img").forEach(function (img) {
      img.addEventListener("error", function () {
        img.style.display = "none";
        var fallback = document.createElement("div");
        fallback.className = "app-icon";
        fallback.setAttribute("aria-hidden", "true");
        fallback.textContent = "FM";
        img.parentNode.insertBefore(fallback, img);
      });
    });

    // External links open safely in a new tab when marked.
    document.querySelectorAll('a[rel~="noopener"]').forEach(function (link) {
      if (!link.target) link.target = "_blank";
    });
  });

  window.addEventListener("error", function (event) {
    if (window.location.pathname.indexOf("/facematch/oauth/") !== -1) return;
    console.warn("[FaceMatch site]", event.message || "Unhandled page error");
  });
})();
