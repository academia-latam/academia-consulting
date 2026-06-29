// AcademIA — progressive enhancement only. Fully readable without JS.
(function () {
  "use strict";
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // main.js is running, so cancel the inline head-script failsafe that would
  // otherwise un-hide everything (that failsafe only matters if this never runs).
  if (window.__revealFS) { clearTimeout(window.__revealFS); window.__revealFS = null; }

  // Scroll reveals (gated by html.anim so content is visible without JS / in headless / for crawlers).
  var els = document.querySelectorAll("[data-reveal]");
  function show(el) { el.classList.add("in"); }

  if (reduce || !("IntersectionObserver" in window)) {
    els.forEach(show);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.04 });
    els.forEach(function (el) { io.observe(el); });

    // Fallback: some browsers (Android in-app/WebView, bfcache restores) never
    // fire the observer. Reveal whatever is in view on paint / scroll / load so
    // content is never stranded behind opacity:0.
    var showInView = function () {
      var vh = window.innerHeight || root.clientHeight;
      els.forEach(function (el) {
        if (el.classList.contains("in")) return;
        var r = el.getBoundingClientRect();
        if (r.top < vh * 0.97 && r.bottom > 0) show(el);
      });
    };
    requestAnimationFrame(function () { requestAnimationFrame(showInView); });
    window.addEventListener("load", showInView, { passive: true });
    window.addEventListener("scroll", showInView, { passive: true });
    window.addEventListener("resize", showInView, { passive: true });
  }

  // Scroll-spy: mark the current section in the nav
  var navLinks = [].slice.call(document.querySelectorAll('.nav-menu a[href^="#"]'));
  if (navLinks.length && "IntersectionObserver" in window) {
    var spyMap = {};
    navLinks.forEach(function (a) {
      var sec = document.getElementById(a.getAttribute("href").slice(1));
      if (sec) spyMap[sec.id] = a;
    });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        navLinks.forEach(function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
        var link = spyMap[e.target.id];
        if (link) { link.classList.add("is-active"); link.setAttribute("aria-current", "true"); }
      });
    }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
    Object.keys(spyMap).forEach(function (id) { spy.observe(document.getElementById(id)); });
  }

  // Remember language choice for the root redirect
  document.querySelectorAll("[data-lang-set]").forEach(function (a) {
    a.addEventListener("click", function () {
      try { localStorage.setItem("academia_lang", a.getAttribute("data-lang-set")); } catch (e) {}
    });
  });

  // CTA service selector -> email body on the "email us" link (the primary CTA
  // now opens Calendly). Progressive: the mailto link already works without JS.
  var dcta = document.querySelector('.cta a[href^="mailto"]');
  if (dcta) {
    dcta.addEventListener("click", function () {
      var picked = [].slice.call(document.querySelectorAll(".selector input:checked")).map(function (i) { return i.value; });
      var base = dcta.getAttribute("href").split(/[?&]body=/)[0];
      var es = (document.documentElement.lang || "en").slice(0, 2) === "es";
      var lead = es ? "Interes en: " : "Interested in: ";
      if (picked.length) {
        var sep = base.indexOf("?") === -1 ? "?" : "&";
        dcta.setAttribute("href", base + sep + "body=" + encodeURIComponent(lead + picked.join(", ")));
      }
    });
  }

  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();
