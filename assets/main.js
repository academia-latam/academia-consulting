// AcademIA — progressive enhancement only. Site is fully readable without JS.
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Scroll reveals (enhances an already-visible default; if no JS, content shows)
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

  // Remember language choice for the root redirect
  document.querySelectorAll("[data-lang-set]").forEach(function (a) {
    a.addEventListener("click", function () {
      try { localStorage.setItem("academia_lang", a.getAttribute("data-lang-set")); } catch (e) {}
    });
  });

  // Year in footer
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();
