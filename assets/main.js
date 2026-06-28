// AcademIA — progressive enhancement only. Fully readable without JS.
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Scroll reveals (content is visible by default; this only enhances)
  var els = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    els.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });
    els.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i % 4, 3) * 70 + "ms";
      io.observe(el);
    });
  }

  // Subtle parallax on [data-parallax] (speed factor in the attribute)
  var px = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  if (!reduce && px.length && "requestAnimationFrame" in window) {
    var ticking = false;
    var apply = function () {
      var vh = window.innerHeight;
      px.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var mid = r.top + r.height / 2;
        var off = (mid - vh / 2) / vh;            // -0.5..0.5 across viewport
        var f = parseFloat(el.getAttribute("data-parallax")) || 0.06;
        el.style.transform = "translateY(" + (off * f * 100).toFixed(1) + "px)";
      });
      ticking = false;
    };
    var onScroll = function () { if (!ticking) { ticking = true; requestAnimationFrame(apply); } };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    apply();
  }

  // Scrollytelling: activate step + matching stage image + progress
  var steps = document.querySelectorAll(".step");
  var imgs = document.querySelectorAll(".stage-img");
  var dots = document.querySelectorAll(".stage-progress span");
  if (steps.length && imgs.length) {
    var setActive = function (i) {
      imgs.forEach(function (im, k) { im.classList.toggle("is-active", k === i); });
      dots.forEach(function (d, k) { d.classList.toggle("on", k <= i); });
      steps.forEach(function (s, k) { s.classList.toggle("active", k === i); });
    };
    if ("IntersectionObserver" in window) {
      var so = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) setActive(+e.target.getAttribute("data-step")); });
      }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
      steps.forEach(function (s) { so.observe(s); });
    }
    setActive(0);
  }

  document.querySelectorAll("[data-lang-set]").forEach(function (a) {
    a.addEventListener("click", function () {
      try { localStorage.setItem("academia_lang", a.getAttribute("data-lang-set")); } catch (e) {}
    });
  });
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();
