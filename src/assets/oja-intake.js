/**
 * Start a project — multi-step lead intake (mailto, no server storage).
 */
(function () {
  "use strict";

  var EMAIL = "support@orangejuiceapplications.com";
  var form = null;
  var steps = [];
  var progressFill = null;
  var current = 0;

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function sanitize(value, max) {
    return String(value || "")
      .replace(/[\u0000-\u001F\u007F]/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, max || 500);
  }

  function sanitizeMultiline(value, max) {
    return String(value || "")
      .replace(/[\u0000-\u0008\u000B-\u000C\u000E-\u001F\u007F]/g, "")
      .trim()
      .slice(0, max || 4000);
  }

  function selectedValues(name) {
    if (!form) return [];
    var nodes = form.querySelectorAll('[name="' + name + '"]:checked');
    return Array.prototype.map.call(nodes, function (n) {
      return n.value;
    });
  }

  function fieldValue(name) {
    if (!form) return "";
    var el = form.elements[name];
    if (!el) return "";
    if (el.type === "radio") {
      var picked = form.querySelector('[name="' + name + '"]:checked');
      return picked ? picked.value : "";
    }
    return el.value || "";
  }

  function updateProgress() {
    if (!progressFill || !steps.length) return;
    var pct = ((current + 1) / steps.length) * 100;
    progressFill.style.width = pct + "%";
    var label = qs("[data-intake-step-label]");
    if (label) {
      label.textContent = "Step " + (current + 1) + " of " + steps.length;
    }
  }

  function showStep(index) {
    current = Math.max(0, Math.min(index, steps.length - 1));
    steps.forEach(function (step, i) {
      step.classList.toggle("is-active", i === current);
      step.hidden = i !== current;
    });
    var back = qs("[data-intake-back]");
    var next = qs("[data-intake-next]");
    var submit = qs("[data-intake-submit]");
    if (back) back.hidden = current === 0;
    if (next) next.hidden = current === steps.length - 1;
    if (submit) submit.hidden = current !== steps.length - 1;
    updateProgress();
  }

  function validateStep() {
    var step = steps[current];
    if (!step) return true;
    if (step.hasAttribute("data-validate-platforms") && !selectedValues("platforms").length) {
      showError("Select at least one platform.");
      return false;
    }
    var required = step.querySelectorAll("[data-required]");
    for (var i = 0; i < required.length; i++) {
      var el = required[i];
      if (el.type === "radio") {
        var group = form.querySelector('[name="' + el.name + '"]:checked');
        if (!group) {
          showError("Please choose an option to continue.");
          return false;
        }
      } else if (el.tagName === "SELECT" && !sanitize(el.value, 10)) {
        showError("Please choose an option.");
        el.focus();
        return false;
      } else if (el.tagName !== "SELECT" && el.type !== "checkbox" && !sanitize(el.value, 10)) {
        showError("Please fill in the required field.");
        el.focus();
        return false;
      }
    }
    clearError();
    return true;
  }

  function showError(msg) {
    var box = qs("[data-intake-error]");
    if (box) {
      box.textContent = msg;
      box.hidden = false;
    }
  }

  function clearError() {
    var box = qs("[data-intake-error]");
    if (box) box.hidden = true;
  }

  function buildMailto() {
    var projectType = fieldValue("project_type");
    var technical = fieldValue("technical_level");
    var name = sanitize(fieldValue("contact_name"), 80);
    var company = sanitize(fieldValue("contact_company"), 120);
    var email = sanitize(fieldValue("contact_email"), 120);
    var phone = sanitize(fieldValue("contact_phone"), 40);
    var github = sanitize(fieldValue("github_url"), 200);
    var languages = selectedValues("languages").join(", ") || "Not specified";
    var platforms = selectedValues("platforms").join(", ") || "Not specified";
    var timeline = fieldValue("timeline");
    var budget = fieldValue("budget");
    var summary = sanitizeMultiline(fieldValue("project_summary"), 2000);

    var subject =
      "Project inquiry - " +
      (projectType || "General") +
      (name ? " - " + name : "");

    var body = [
      "Orange Juice Applications — project intake",
      "",
      "Project type: " + projectType,
      "Technical level: " + technical,
      "",
      "GitHub / repo: " + (github || "None provided"),
      "Languages / stack: " + languages,
      "Platforms: " + platforms,
      "Timeline: " + timeline,
      "Budget band: " + budget,
      "",
      "Summary:",
      summary || "(none)",
      "",
      "---",
      "Contact: " + name,
      "Company: " + (company || "—"),
      "Email: " + email,
      "Phone: " + (phone || "—"),
      "Page: " + window.location.href,
    ].join("\n");

    return (
      "mailto:" +
      EMAIL +
      "?subject=" +
      encodeURIComponent(subject) +
      "&body=" +
      encodeURIComponent(body)
    );
  }

  function toggleTechnicalFields() {
    var level = fieldValue("technical_level");
    var repoBlock = qs("[data-intake-repo-fields]");
    var langBlock = qs("[data-intake-lang-fields]");
    if (!repoBlock) return;
    var showTech = level === "existing_repo" || level === "existing_team";
    repoBlock.hidden = !showTech;
    if (langBlock) langBlock.hidden = level === "non_technical";
  }

  function init() {
    form = qs("[data-intake-form]");
    if (!form) return;

    steps = Array.prototype.slice.call(form.querySelectorAll("[data-intake-step]"));
    progressFill = qs("[data-intake-progress-fill]");
    if (!steps.length) return;

    form.querySelectorAll('[name="technical_level"]').forEach(function (radio) {
      radio.addEventListener("change", toggleTechnicalFields);
    });
    toggleTechnicalFields();

    var nextBtn = qs("[data-intake-next]");
    var backBtn = qs("[data-intake-back]");
    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        if (!validateStep()) return;
        showStep(current + 1);
      });
    }
    if (backBtn) {
      backBtn.addEventListener("click", function () {
        clearError();
        showStep(current - 1);
      });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validateStep()) return;
      var email = sanitize(fieldValue("contact_email"), 120);
      if (!email || email.indexOf("@") === -1) {
        showError("Please enter a valid email address.");
        return;
      }
      window.location.href = buildMailto();
    });

    showStep(0);
  }

  onReady(init);
})();
