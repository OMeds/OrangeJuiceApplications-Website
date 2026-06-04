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

  function config() {
    return window.OJA_SITE_CONFIG || {};
  }

  function loadPlausible() {
    var domain = (config().plausibleDomain || "").trim();
    if (!domain) return;
    var s = document.createElement("script");
    s.defer = true;
    s.setAttribute("data-domain", domain);
    s.src = "https://plausible.io/js/script.js";
    document.head.appendChild(s);
  }

  function initCalendly() {
    var url = (config().calendlyUrl || "").trim();
    var wrap = document.querySelector("[data-calendly-embed]");
    var frame = document.querySelector("[data-calendly-frame]");
    var fallback = document.querySelector("[data-calendly-fallback]");
    if (!url || !wrap || !frame) return;
    frame.src = url.replace(/\/$/, "") + "?hide_gdpr_banner=1";
    wrap.hidden = false;
    if (fallback) fallback.hidden = true;
  }

  function initTestFlight() {
    var url = (config().testFlightUrl || "").trim();
    document.querySelectorAll("[data-testflight-link]").forEach(function (link) {
      var soon = document.querySelector("[data-testflight-soon]");
      if (url) {
        link.href = url;
        link.hidden = false;
        link.classList.remove("is-hidden");
        if (soon) soon.hidden = true;
      }
    });
  }

  function initAppStoreBlocks() {
    var cfg = config();
    var map = {
      facematch: cfg.facematchAppStoreUrl,
      ycda: cfg.ycdaAppStoreUrl,
    };
    Object.keys(map).forEach(function (key) {
      var url = (map[key] || "").trim();
      document.querySelectorAll('[data-app-store="' + key + '"]').forEach(function (block) {
        var link = block.querySelector("[data-app-store-link]");
        var soon = block.querySelector("[data-app-store-soon]");
        if (url && link) {
          link.href = url;
          link.hidden = false;
          link.classList.remove("is-hidden");
          if (soon) soon.hidden = true;
        }
      });
    });
  }

  onReady(function () {
    loadPlausible();
    initCalendly();
    initTestFlight();
    initAppStoreBlocks();

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

    document.querySelectorAll('a[rel~="noopener"]').forEach(function (link) {
      if (!link.target) link.target = "_blank";
    });
  });

  window.addEventListener("error", function (event) {
    if (window.location.pathname.indexOf("/facematch/oauth/") !== -1) return;
    console.warn("[OJA site]", event.message || "Unhandled page error");
  });
})();
