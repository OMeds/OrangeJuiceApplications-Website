/**
 * Web feedback form — Formspree when configured, else mailto.
 */
(function () {
  "use strict";

  var SOURCE = "Web";
  var ALLOWED_CATEGORIES = {
    Feedback: true,
    Bug: true,
    Issue: true,
    "Feature Request": true
  };
  var MAX_SUMMARY = 120;
  var MAX_DETAIL = 4000;

  function config() {
    return window.OJA_SITE_CONFIG || {};
  }

  function supportEmail() {
    return config().supportEmail || "support@orangejuiceapplications.com";
  }

  function formspreeEndpoint() {
    var id = (config().formspreeFeedbackId || "").trim();
    if (!id) return "";
    return "https://formspree.io/f/" + encodeURIComponent(id);
  }

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

  function buildSubject(category, summary) {
    var short = sanitizeText(summary, 80) || "Feedback";
    return SOURCE + " - " + category + " - " + short;
  }

  function buildPayload(category, summary, detail, email) {
    return {
      _subject: buildSubject(category, summary),
      category: category,
      summary: sanitizeText(summary, MAX_SUMMARY),
      detail: sanitizeMultiline(detail, MAX_DETAIL),
      contact_email: sanitizeText(email, 120),
      page: sanitizeText(window.location.href, 500),
      browser: sanitizeText(navigator.userAgent, 500),
      source: SOURCE
    };
  }

  function buildMailto(category, summary, detail) {
    var body = [
      "Source: " + SOURCE,
      "Category: " + category,
      "Summary: " + sanitizeText(summary, MAX_SUMMARY),
      "",
      "Description:",
      sanitizeMultiline(detail, MAX_DETAIL),
      "",
      "---",
      "Page: " + sanitizeText(window.location.href, 500),
      "Browser: " + sanitizeText(navigator.userAgent, 500)
    ].join("\n");
    return (
      "mailto:" +
      supportEmail() +
      "?subject=" +
      encodeURIComponent(buildSubject(category, summary)) +
      "&body=" +
      encodeURIComponent(body)
    );
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
    var emailField = form.querySelector("#feedback-email");
    var previewField = form.querySelector("#feedback-subject-preview");
    var submitBtn = form.querySelector("[type=submit]");

    if (submitBtn && formspreeEndpoint()) {
      submitBtn.textContent = "Send feedback";
    }

    function refreshPreview() {
      if (!previewField || !categoryField || !summaryField) return;
      var category = ALLOWED_CATEGORIES[categoryField.value]
        ? categoryField.value
        : "Feedback";
      previewField.textContent = buildSubject(category, summaryField.value || "…");
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
      var email = emailField ? sanitizeText(emailField.value, 120) : "";

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

      if (formspreeEndpoint()) {
        if (!email || email.indexOf("@") === -1) {
          showError(form, "Enter your email so we can reply.");
          if (emailField) emailField.focus();
          return;
        }
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = "Sending…";
        }
        fetch(formspreeEndpoint(), {
          method: "POST",
          headers: { Accept: "application/json", "Content-Type": "application/json" },
          body: JSON.stringify(buildPayload(category, summary, detail, email))
        })
          .then(function (res) {
            if (!res.ok) throw new Error("failed");
            form.reset();
            refreshPreview();
            showSuccess(form, "Thank you — your feedback was sent. We typically reply within two business days.");
          })
          .catch(function () {
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.textContent = "Send feedback";
            }
            showError(form, "Could not send online. Opening your email app instead.");
            window.location.href = buildMailto(category, summary, detail);
          });
        return;
      }

      showSuccess(form, "Opening your email app… Send the message to complete your feedback.");
      window.location.href = buildMailto(category, summary, detail);
    });
  });
})();
