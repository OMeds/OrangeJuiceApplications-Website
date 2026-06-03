/**
 * OAuth HTTPS bridge — validates callback params and opens FaceMatch safely.
 */
(function () {
  "use strict";

  var ALLOWED_PLATFORMS = {
    linkedin: true
  };

  function sanitizeDisplayText(value) {
    if (!value) return "";
    return String(value)
      .replace(/[\u0000-\u001F\u007F]/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 240);
  }

  function showPanel(name) {
    ["loading", "error", "fallback"].forEach(function (id) {
      var panel = document.getElementById("panel-" + id);
      if (!panel) return;
      panel.classList.toggle("is-visible", id === name);
    });
  }

  function readPlatform() {
    var body = document.body;
    var platform = body && body.getAttribute("data-oauth-platform");
    if (platform && ALLOWED_PLATFORMS[platform]) return platform;

    var parts = window.location.pathname.split("/").filter(Boolean);
    var candidate = parts[parts.length - 1] || "";
    return ALLOWED_PLATFORMS[candidate] ? candidate : null;
  }

  function buildTarget(platform, query) {
    return "facematch://oauth/" + platform + (query || "");
  }

  function openApp(target) {
    try {
      window.location.replace(target);
    } catch (e) {}
    try {
      window.location.href = target;
    } catch (e2) {}
  }

  document.addEventListener("DOMContentLoaded", function () {
    var platform = readPlatform();
    var params = new URLSearchParams(window.location.search || "");
    var error = params.get("error");
    var errorDescription = params.get("error_description");
    var code = params.get("code");
    var query = window.location.search || "";

    var errorTitle = document.getElementById("error-title");
    var errorDetail = document.getElementById("error-detail");
    var openAppLink = document.getElementById("open-app-link");
    var retryLink = document.getElementById("retry-link");

    if (!platform) {
      if (errorTitle) errorTitle.textContent = "Invalid redirect";
      if (errorDetail) {
        errorDetail.textContent = "This sign-in link is not recognized.";
      }
      showPanel("error");
      return;
    }

    var target = buildTarget(platform, query);
    if (openAppLink) openAppLink.href = target;
    if (retryLink) retryLink.href = target;

    if (error) {
      if (errorTitle) {
        errorTitle.textContent =
          error === "access_denied"
            ? "Sign-in was cancelled or denied"
            : "Sign-in could not be completed";
      }
      if (errorDetail) errorDetail.textContent = sanitizeDisplayText(errorDescription || error);
      showPanel("error");
      return;
    }

    if (!code) {
      if (errorTitle) errorTitle.textContent = "Sign-in incomplete";
      if (errorDetail) {
        errorDetail.textContent = "No authorization code was returned. Open FaceMatch and tap Sign In again.";
      }
      showPanel("error");
      return;
    }

    openApp(target);
    window.setTimeout(function () {
      if (!document.hidden) showPanel("fallback");
    }, 2800);

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) showPanel("loading");
    });
  });
})();
