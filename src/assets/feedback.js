/**
 * Web feedback form — opens mail client with structured subject:
 * Web - Bug - Short summary
 */
(function () {
  "use strict";

  var SUPPORT_EMAIL = "support@orangejuiceapplications.com";
  var SOURCE = "Web";
  var ALLOWED_CATEGORIES = {
    Feedback: true,
    Bug: true,
    Issue: true,
    "Feature Request": true
  };
  var MAX_SUMMARY = 120;
  var MAX_DETAIL = 4000;

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function sanitizeText(value, maxLength) {
    if (!value) return "";
    return String(value)
      .replace(/[\u0000-\u001F\u007F]/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, maxLength);
  }

  function sanitizeMultiline(value, maxLength) {
    if (!value) return "";
    return String(value)
      .replace(/[\u0000-\u0008\u000B-\u000C\u000E-\u001F\u007F]/g, "")
      .replace(/\r\n/g, "\n")
      .trim()
      .slice(0, maxLength);
  }

  function encodeMailto(value) {
    return encodeURIComponent(value);
  }

  function buildSubject(category, summary) {
    var short = sanitizeText(summary, 80) || "Feedback";
    return SOURCE + " - " + category + " - " + short;
  }

  function buildBody(category, summary, detail) {
    var page = sanitizeText(window.location.href, 500);
    var browser = sanitizeText(navigator.userAgent, 500);

    return [
      "Source: " + SOURCE,
      "Category: " + category,
      "Summary: " + sanitizeText(summary, MAX_SUMMARY),
      "",
      "Description:",
      sanitizeMultiline(detail, MAX_DETAIL),
      "",
      "---",
      "Page: " + page,
      "Browser: " + browser
    ].join("\n");
  }

  function showError(form, message) {
    var box = form.querySelector(".feedback-error");
    if (!box) return;
    box.textContent = message;
    box.hidden = false;
  }

  function clearError(form) {
    var box = form.querySelector(".feedback-error");
    if (!box) return;
    box.hidden = true;
    box.textContent = "";
  }

  function showSuccess(form, message) {
    var box = form.querySelector(".feedback-success");
    if (!box) return;
    box.textContent = message;
    box.hidden = false;
  }

  onReady(function () {
    var form = document.getElementById("feedback-form");
    if (!form) return;

    var categoryField = form.querySelector("#feedback-category");
    var summaryField = form.querySelector("#feedback-summary");
    var detailField = form.querySelector("#feedback-detail");
    var previewField = form.querySelector("#feedback-subject-preview");

    function refreshPreview() {
      if (!previewField || !categoryField || !summaryField) return;
      var category = ALLOWED_CATEGORIES[categoryField.value]
        ? categoryField.value
        : "Feedback";
      previewField.textContent = buildSubject(
        category,
        summaryField.value || "…"
      );
    }

    categoryField.addEventListener("change", refreshPreview);
    summaryField.addEventListener("input", refreshPreview);
    refreshPreview();

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      clearError(form);

      var category = ALLOWED_CATEGORIES[categoryField.value]
        ? categoryField.value
        : "Feedback";
      var summary = sanitizeText(summaryField.value, MAX_SUMMARY);
      var detail = sanitizeMultiline(detailField.value, MAX_DETAIL);

      if (!summary) {
        showError(form, "Add a short summary so we can identify your feedback.");
        summaryField.focus();
        return;
      }

      if (!detail) {
        showError(form, "Add a description of the bug, issue, or feedback.");
        detailField.focus();
        return;
      }

      var subject = buildSubject(category, summary);
      var body = buildBody(category, summary, detail);
      var mailto =
        "mailto:" +
        SUPPORT_EMAIL +
        "?subject=" +
        encodeMailto(subject) +
        "&body=" +
        encodeMailto(body);

      showSuccess(
        form,
        "Opening your email app… Send the message to complete your feedback."
      );

      window.location.href = mailto;
    });
  });
})();
