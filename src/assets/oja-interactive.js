/**
 * Orange Juice Applications — interactive hub, YCDA showcase, FaceMatch preview
 */
(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

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

  function qsa(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  /* --- Mobile nav --- */
  function initNav() {
    var toggle = qs("[data-nav-toggle]");
    var panel = qs("[data-nav-panel]");
    if (!toggle || !panel) return;

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      panel.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
    }

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    qsa("a", panel).forEach(function (link) {
      link.addEventListener("click", function () {
        setOpen(false);
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
  }

  /* --- Scroll progress --- */
  function initScrollProgress() {
    var bar = qs("[data-scroll-progress]");
    if (!bar) return;

    function update() {
      var doc = document.documentElement;
      var scrollTop = doc.scrollTop || document.body.scrollTop;
      var height = doc.scrollHeight - doc.clientHeight;
      var pct = height > 0 ? (scrollTop / height) * 100 : 0;
      bar.style.width = pct + "%";
    }

    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  /* --- Reveal on scroll --- */
  function initReveal() {
    var items = qsa("[data-reveal]");
    if (!items.length) return;

    if (prefersReducedMotion) {
      items.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );

    items.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* --- Animated counters --- */
  function initCounters() {
    var counters = qsa("[data-count-to]");
    if (!counters.length) return;

    function animateCounter(el) {
      var target = parseInt(el.getAttribute("data-count-to"), 10);
      if (isNaN(target)) return;
      var suffix = el.getAttribute("data-count-suffix") || "";
      var duration = prefersReducedMotion ? 0 : 1400;
      var start = performance.now();

      function tick(now) {
        var t = duration === 0 ? 1 : Math.min(1, (now - start) / duration);
        var eased = 1 - Math.pow(1 - t, 3);
        el.textContent = Math.round(target * eased) + suffix;
        if (t < 1) requestAnimationFrame(tick);
      }

      requestAnimationFrame(tick);
    }

    var obs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );

    counters.forEach(function (c) {
      obs.observe(c);
    });
  }

  /* --- Tabs (classes, paths) --- */
  function initTabs() {
    qsa("[data-tabs]").forEach(function (root) {
      var buttons = qsa("[data-tab]", root);
      var panels = qsa("[data-tab-panel]", root);
      if (!buttons.length || !panels.length) return;

      function activate(id) {
        buttons.forEach(function (btn) {
          var on = btn.getAttribute("data-tab") === id;
          btn.classList.toggle("is-active", on);
          btn.setAttribute("aria-selected", on ? "true" : "false");
        });
        panels.forEach(function (panel) {
          var on = panel.getAttribute("data-tab-panel") === id;
          panel.classList.toggle("is-active", on);
          panel.hidden = !on;
        });
      }

      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          activate(btn.getAttribute("data-tab"));
        });
      });

      var initial = buttons.find(function (b) {
        return b.classList.contains("is-active");
      });
      activate((initial || buttons[0]).getAttribute("data-tab"));
    });
  }

  /* --- FAQ accordion --- */
  function initAccordion() {
    qsa("[data-accordion]").forEach(function (item) {
      var trigger = qs("[data-accordion-trigger]", item);
      var panel = qs("[data-accordion-panel]", item);
      if (!trigger || !panel) return;

      trigger.addEventListener("click", function () {
        var open = item.classList.toggle("is-open");
        trigger.setAttribute("aria-expanded", open ? "true" : "false");
        panel.hidden = !open;
      });
    });
  }

  /* --- Testimonial carousel --- */
  function initCarousel() {
    var root = qs("[data-carousel]");
    if (!root) return;

    var track = qs("[data-carousel-track]", root);
    var slides = qsa("[data-carousel-slide]", root);
    var prev = qs("[data-carousel-prev]", root);
    var next = qs("[data-carousel-next]", root);
    var dots = qsa("[data-carousel-dot]", root);
    if (!track || !slides.length) return;

    var index = 0;

    function goTo(i) {
      index = (i + slides.length) % slides.length;
      track.style.transform = "translateX(-" + index * 100 + "%)";
      dots.forEach(function (dot, d) {
        dot.classList.toggle("is-active", d === index);
        dot.setAttribute("aria-selected", d === index ? "true" : "false");
      });
      slides.forEach(function (slide, s) {
        slide.setAttribute("aria-hidden", s !== index ? "true" : "false");
      });
    }

    if (prev) {
      prev.addEventListener("click", function () {
        goTo(index - 1);
      });
    }
    if (next) {
      next.addEventListener("click", function () {
        goTo(index + 1);
      });
    }
    dots.forEach(function (dot, d) {
      dot.addEventListener("click", function () {
        goTo(d);
      });
    });

    root.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") goTo(index - 1);
      if (e.key === "ArrowRight") goTo(index + 1);
    });

    if (!prefersReducedMotion) {
      var autoplay = window.setInterval(function () {
        if (document.hidden) return;
        goTo(index + 1);
      }, 7000);
      root.addEventListener("mouseenter", function () {
        window.clearInterval(autoplay);
      });
    }

    goTo(0);
  }

  /* --- Hero pointer glow --- */
  function initHeroGlow() {
    var hero = qs("[data-hero-glow]");
    if (!hero || prefersReducedMotion) return;

    hero.addEventListener(
      "pointermove",
      function (e) {
        var rect = hero.getBoundingClientRect();
        var x = ((e.clientX - rect.left) / rect.width) * 100;
        var y = ((e.clientY - rect.top) / rect.height) * 100;
        hero.style.setProperty("--glow-x", x + "%");
        hero.style.setProperty("--glow-y", y + "%");
      },
      { passive: true }
    );
  }

  /* --- Tilt cards --- */
  function initTilt() {
    if (prefersReducedMotion || window.matchMedia("(max-width: 768px)").matches) return;

    qsa("[data-tilt]").forEach(function (card) {
      card.addEventListener(
        "pointermove",
        function (e) {
          var r = card.getBoundingClientRect();
          var px = (e.clientX - r.left) / r.width - 0.5;
          var py = (e.clientY - r.top) / r.height - 0.5;
          card.style.transform =
            "perspective(800px) rotateY(" + px * 6 + "deg) rotateX(" + -py * 6 + "deg) translateY(-4px)";
        },
        { passive: true }
      );
      card.addEventListener("pointerleave", function () {
        card.style.transform = "";
      });
    });
  }

  /* --- FaceMatch dev progress (decorative) --- */
  function initDevProgress() {
    var bar = qs("[data-dev-progress]");
    if (!bar || prefersReducedMotion) return;

    var obs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            bar.style.width = bar.getAttribute("data-dev-progress") || "72%";
            obs.unobserve(bar);
          }
        });
      },
      { threshold: 0.4 }
    );
    obs.observe(bar.parentElement || bar);
  }

  onReady(function () {
    initNav();
    initScrollProgress();
    initReveal();
    initCounters();
    initTabs();
    initAccordion();
    initCarousel();
    initHeroGlow();
    initTilt();
    initDevProgress();
  });
})();
