/**
 * Sync YCDA CTA links from meta[name="oja-ycda-app-url"] — no auto-redirect.
 */
(function () {
  "use strict";

  var meta = document.querySelector('meta[name="oja-ycda-app-url"]');
  var url = meta && meta.getAttribute("content");
  if (!url || !/^https:\/\//i.test(url)) {
    return;
  }

  document.querySelectorAll("#ycda-open, a[data-ycda-live]").forEach(function (link) {
    link.href = url;
  });

  var display = document.getElementById("ycda-url-display");
  if (display) {
    display.textContent = "Live site: " + url;
    display.hidden = false;
  }
})();
