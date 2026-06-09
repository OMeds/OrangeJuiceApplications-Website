/**
 * Start a project — multi-step lead intake (Formspree when configured, else mailto).
 */
(function () {
  "use strict";

  var form = null;
  var steps = [];
  var progressFill = null;
  var current = 0;
  var STORAGE_KEY = "oja-intake-draft-v1";

  function config() {
    return window.OJA_SITE_CONFIG || {};
  }

  function supportEmail() {
    return config().supportEmail || "support@orangejuiceapplications.com";
  }

  function formspreeEndpoint() {
    var id = (config().formspreeIntakeId || "").trim();
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

  function getAttachmentNames() {
    var input = qs("#intake_files");
    if (!input || !input.files || !input.files.length) return [];
    return Array.prototype.map.call(input.files, function (f) {
      return sanitize(f.name, 120);
    });
  }

  function attachmentNote() {
    var names = getAttachmentNames();
    if (!names.length) return "None";
    return names.join(", ");
  }

  function serializeForm() {
    var data = { step: current, fields: {}, checks: {} };
    if (!form) return data;
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.type === "file" || el.type === "submit" || el.type === "button") return;
      if (el.type === "checkbox") {
        if (!data.checks[el.name]) data.checks[el.name] = [];
        if (el.checked) data.checks[el.name].push(el.value);
      } else if (el.type === "radio") {
        if (el.checked) data.fields[el.name] = el.value;
      } else {
        data.fields[el.name] = el.value;
      }
    });
    data.attachmentNames = getAttachmentNames();
    return data;
  }

  function saveDraft() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(serializeForm()));
    } catch (e) {
      /* storage full or private mode */
    }
  }

  function clearDraft() {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (e) {
      /* ignore */
    }
  }

  function applyDraft(data) {
    if (!form || !data) return;
    Object.keys(data.fields || {}).forEach(function (name) {
      var val = data.fields[name];
      var el = form.elements[name];
      if (el && el.type !== "radio" && el.type !== "checkbox") {
        el.value = val;
        return;
      }
      form.querySelectorAll('[name="' + name + '"]').forEach(function (node) {
        if (node.type === "radio") node.checked = node.value === val;
      });
    });
    Object.keys(data.checks || {}).forEach(function (name) {
      var vals = data.checks[name];
      form.querySelectorAll('[name="' + name + '"]').forEach(function (el) {
        el.checked = vals.indexOf(el.value) !== -1;
      });
    });
    toggleTechnicalFields();
    if (typeof data.step === "number") showStep(data.step);
  }

  function initRestoreBanner() {
    var raw;
    try {
      raw = localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return;
    }
    if (!raw) return;
    var data;
    try {
      data = JSON.parse(raw);
    } catch (e) {
      return;
    }
    if (!data || (!data.fields && !data.checks)) return;
    var banner = document.createElement("div");
    banner.className = "oja-intake-restore card";
    banner.setAttribute("role", "status");
    banner.innerHTML =
      "<p><strong>Saved progress found.</strong> Restore your answers from this device?</p>" +
      '<div class="oja-intake-restore-actions">' +
      '<button type="button" class="btn btn-primary" data-intake-restore-yes>Restore</button> ' +
      '<button type="button" class="btn btn-secondary" data-intake-restore-no>Start fresh</button>' +
      "</div>";
    var panel = qs(".intake-panel");
    if (!panel || !panel.parentNode) return;
    panel.parentNode.insertBefore(banner, panel);
    banner.querySelector("[data-intake-restore-yes]").addEventListener("click", function () {
      applyDraft(data);
      banner.remove();
    });
    banner.querySelector("[data-intake-restore-no]").addEventListener("click", function () {
      clearDraft();
      banner.remove();
    });
  }

  function applyPrefill(data) {
    if (!form || !data) return;
    var checks = data._checks || {};
    delete data._checks;
    var goal = data.project_goal;
    delete data.project_goal;
    applyDraft({ fields: data, checks: checks, step: 0 });
    if (goal) {
      var goalEl = form.elements.project_goal;
      if (goalEl) goalEl.value = goal;
    }
    saveDraft();
    showStep(2);
    clearError();
    var formEl = qs("#intake-form");
    if (formEl && formEl.scrollIntoView) formEl.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function initPrefills() {
    qsa("[data-intake-prefill]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        try {
          applyPrefill(JSON.parse(btn.getAttribute("data-intake-prefill")));
        } catch (e) {
          /* invalid prefill */
        }
      });
    });
  }

  function qsa(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function initGlossary() {
    qsa(".oja-glossary-btn").forEach(function (btn) {
      var tipId = btn.getAttribute("aria-controls");
      var tip = tipId ? document.getElementById(tipId) : null;
      if (!tip) return;
      function closeAll() {
        tip.hidden = true;
        btn.setAttribute("aria-expanded", "false");
      }
      function open() {
        tip.hidden = false;
        btn.setAttribute("aria-expanded", "true");
      }
      btn.addEventListener("click", function () {
        if (tip.hidden) open();
        else closeAll();
      });
      btn.addEventListener("blur", function () {
        setTimeout(closeAll, 150);
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeAll();
      });
    });
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
    saveDraft();
  }

  function validateStep() {
    var step = steps[current];
    if (!step) return true;
    var checkboxGroup = step.getAttribute("data-validate-checkboxes");
    if (checkboxGroup && !selectedValues(checkboxGroup).length) {
      showError('Select at least one option, or choose "Help me decide".');
      return false;
    }
    if (step.hasAttribute("data-validate-platforms") && !selectedValues("platforms").length) {
      showError('Select at least one option, or choose "Not sure yet".');
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

  function buildPayload() {
    var goal = sanitizeMultiline(fieldValue("project_goal"), 2000);
    var extra = sanitizeMultiline(fieldValue("project_extra"), 1500);
    return {
      customer_type: fieldValue("customer_type"),
      request_types: selectedValues("request_types").join(", ") || "Not specified",
      project_goal: goal,
      project_extra: extra,
      platforms: selectedValues("platforms").join(", ") || "Not specified",
      technical_level: fieldValue("technical_level"),
      github_url: sanitize(fieldValue("github_url"), 200),
      languages: selectedValues("languages").join(", ") || "Not specified",
      timeline: fieldValue("timeline"),
      budget: fieldValue("budget"),
      project_summary: [goal, extra].filter(Boolean).join("\n\n") || "(none)",
      contact_name: sanitize(fieldValue("contact_name"), 80),
      contact_company: sanitize(fieldValue("contact_company"), 120),
      contact_email: sanitize(fieldValue("contact_email"), 120),
      contact_phone: sanitize(fieldValue("contact_phone"), 40),
      attachment_note: attachmentNote(),
      page: window.location.href,
      _subject:
        "Project inquiry - " +
        (fieldValue("customer_type") || "General") +
        (sanitize(fieldValue("contact_name"), 80)
          ? " - " + sanitize(fieldValue("contact_name"), 80)
          : ""),
    };
  }

  function buildMailto() {
    var p = buildPayload();
    var body = [
      "Orange Juice Applications — project intake",
      "",
      "Who they are: " + p.customer_type,
      "What they need help with: " + p.request_types,
      "",
      "Goal (in their words):",
      p.project_goal || "(none)",
      "",
      "Kind of solution: " + p.platforms,
      "Starting point: " + p.technical_level,
      "",
      "GitHub / repo: " + (p.github_url || "None provided"),
      "Languages / stack (if known): " + p.languages,
      "",
      "Timeline: " + p.timeline,
      "Budget band: " + p.budget,
      "",
      "Anything else:",
      p.project_extra || "(none)",
      "",
      "Files selected (attach manually in email if using mailto):",
      p.attachment_note,
      "",
      "---",
      "Contact: " + p.contact_name,
      "Organisation: " + (p.contact_company || "—"),
      "Email: " + p.contact_email,
      "Phone: " + (p.contact_phone || "—"),
      "Page: " + p.page,
    ].join("\n");

    return (
      "mailto:" +
      supportEmail() +
      "?subject=" +
      encodeURIComponent(p._subject) +
      "&body=" +
      encodeURIComponent(body)
    );
  }

  function showSuccess() {
    clearDraft();
    var panel = qs(".intake-panel");
    if (!panel) return;
    panel.innerHTML =
      '<div class="intake-success card" role="status">' +
      "<h2>Thank you</h2>" +
      "<p>Your inquiry was sent. We typically reply within <strong>two business days</strong>.</p>" +
      '<p><a class="btn btn-secondary" href="/contact/">Contact page</a> ' +
      '<a class="btn btn-primary" href="/">Home</a></p>' +
      "</div>";
  }

  function submitFormspree() {
    var endpoint = formspreeEndpoint();
    var submitBtn = qs("[data-intake-submit]");
    var fileInput = qs("#intake_files");
    var hasFiles = fileInput && fileInput.files && fileInput.files.length;
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending…";
    }
    var req;
    if (hasFiles) {
      var fd = new FormData(form);
      var payload = buildPayload();
      Object.keys(payload).forEach(function (k) {
        if (k !== "_subject") fd.append(k, payload[k]);
      });
      fd.append("_subject", payload._subject);
      req = fetch(endpoint, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: fd,
      });
    } else {
      req = fetch(endpoint, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(buildPayload()),
      });
    }
    return req
      .then(function (res) {
        if (!res.ok) throw new Error("Form submission failed");
        showSuccess();
      })
      .catch(function () {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = "Send inquiry";
        }
        showError(
          "Could not send online. We opened your mail app as a fallback — please send the message."
        );
        window.location.href = buildMailto();
      });
  }

  function toggleTechnicalFields() {
    var picked = form.querySelector('[name="technical_level"]:checked');
    var repoBlock = qs("[data-intake-repo-fields]");
    var langBlock = qs("[data-intake-lang-fields]");
    if (!repoBlock) return;
    var showRepo = picked && picked.hasAttribute("data-shows-repo");
    var showLang = picked && picked.hasAttribute("data-shows-lang");
    repoBlock.hidden = !showRepo;
    if (langBlock) langBlock.hidden = !showLang;
  }

  function updateSubmitLabel() {
    var submit = qs("[data-intake-submit]");
    var footnote = qs("[data-intake-footnote]");
    var online = !!formspreeEndpoint();
    if (submit) {
      submit.textContent = online ? "Send inquiry" : "Send inquiry via email";
    }
    if (footnote) {
      footnote.innerHTML = online
        ? "Submitting sends your answers securely to our inbox. We never sell your details. See our <a href=\"/company/privacy/\">website privacy policy</a>."
        : "Submitting opens your email app with your project details ready to send to <strong>" +
          supportEmail() +
          "</strong>. Send the message to start the conversation.";
    }
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
    updateSubmitLabel();
    initRestoreBanner();
    initPrefills();
    initGlossary();

    form.addEventListener("change", saveDraft);
    form.addEventListener("input", saveDraft);

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
      if (formspreeEndpoint()) {
        submitFormspree();
      } else {
        window.location.href = buildMailto();
      }
    });

    showStep(0);
  }

  onReady(init);
})();
