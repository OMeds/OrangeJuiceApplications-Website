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

  /* --- Ambient particle canvas --- */
  function initCanvas() {
    var canvas = qs("#oja-canvas");
    if (!canvas || prefersReducedMotion) return;

    var ctx = canvas.getContext("2d");
    var particles = [];
    var count = Math.min(48, Math.floor(window.innerWidth / 28));
    var mouse = { x: 0, y: 0, on: false };

    function resize() {
      canvas.width = window.innerWidth * devicePixelRatio;
      canvas.height = window.innerHeight * devicePixelRatio;
      canvas.style.width = window.innerWidth + "px";
      canvas.style.height = window.innerHeight + "px";
      ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
    }

    for (var i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
        r: 1 + Math.random() * 2,
      });
    }

    window.addEventListener(
      "pointermove",
      function (e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        mouse.on = true;
        document.documentElement.classList.add("has-pointer");
      },
      { passive: true }
    );

    function frame() {
      ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
      particles.forEach(function (p) {
        if (mouse.on) {
          var dx = mouse.x - p.x;
          var dy = mouse.y - p.y;
          var dist = Math.sqrt(dx * dx + dy * dy) || 1;
          if (dist < 140) {
            p.vx -= (dx / dist) * 0.02;
            p.vy -= (dy / dist) * 0.02;
          }
        }
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0 || p.x > window.innerWidth) p.vx *= -1;
        if (p.y < 0 || p.y > window.innerHeight) p.vy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(232, 93, 4, 0.35)";
        ctx.fill();
      });
      for (var i = 0; i < particles.length; i++) {
        for (var j = i + 1; j < particles.length; j++) {
          var a = particles[i];
          var b = particles[j];
          var d = Math.hypot(a.x - b.x, a.y - b.y);
          if (d < 120) {
            ctx.strokeStyle = "rgba(232, 93, 4, " + (0.12 * (1 - d / 120)) + ")";
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(frame);
    }

    resize();
    window.addEventListener("resize", resize, { passive: true });
    requestAnimationFrame(frame);
  }

  /* --- Cursor glow follows pointer --- */
  function initCursorGlow() {
    if (prefersReducedMotion || !document.documentElement.classList.contains("oja-site")) return;
    var glow = document.createElement("div");
    glow.className = "oja-cursor-glow";
    glow.setAttribute("aria-hidden", "true");
    document.body.appendChild(glow);
    window.addEventListener(
      "pointermove",
      function (e) {
        glow.style.left = e.clientX + "px";
        glow.style.top = e.clientY + "px";
      },
      { passive: true }
    );
  }

  /* --- Magnetic buttons --- */
  function initMagnetic() {
    if (prefersReducedMotion) return;
    qsa("[data-magnetic]").forEach(function (btn) {
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        var x = e.clientX - r.left - r.width / 2;
        var y = e.clientY - r.top - r.height / 2;
        btn.style.transform = "translate(" + x * 0.18 + "px," + y * 0.18 + "px)";
      });
      btn.addEventListener("pointerleave", function () {
        btn.style.transform = "";
      });
    });
  }

  /* --- Chip switcher (hub) --- */
  function initChips() {
    var root = qs("[data-chip-group]");
    if (!root) return;
    var chips = qsa("[data-chip]", root);
    var panels = qsa("[data-chip-panel]");
    function activate(id) {
      chips.forEach(function (c) {
        c.classList.toggle("is-active", c.getAttribute("data-chip") === id);
      });
      panels.forEach(function (p) {
        p.classList.toggle("is-active", p.getAttribute("data-chip-panel") === id);
      });
    }
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        activate(c.getAttribute("data-chip"));
      });
    });
    if (chips[0]) activate(chips[0].getAttribute("data-chip"));
  }

  function initNavScroll() {
    var nav = qs(".site-nav.is-enhanced");
    if (!nav) return;
    function onScroll() {
      nav.classList.toggle("is-scrolled", window.scrollY > 24);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  function revealFallback() {
    window.setTimeout(function () {
      qsa("[data-reveal]:not(.is-visible)").forEach(function (el) {
        el.classList.add("is-visible");
      });
    }, 1200);
  }

  onReady(function () {
    initNav();
    initScrollProgress();
    initReveal();
    revealFallback();
    initCounters();
    initTabs();
    initAccordion();
    initCarousel();
    initHeroGlow();
    initTilt();
    initDevProgress();
    initCanvas();
    initCursorGlow();
    initMagnetic();
    initChips();
    initNavScroll();
  });
})();
