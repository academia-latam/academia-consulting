// AcademIA — progressive enhancement only. Fully readable without JS.
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Scroll reveals (gated by html.anim so content is visible without JS / in headless / for crawlers)
  var els = document.querySelectorAll("[data-reveal]");
  if (reduce || !("IntersectionObserver" in window)) {
    els.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.06 });
    els.forEach(function (el) { io.observe(el); });
  }

  // Remember language choice for the root redirect
  document.querySelectorAll("[data-lang-set]").forEach(function (a) {
    a.addEventListener("click", function () {
      try { localStorage.setItem("academia_lang", a.getAttribute("data-lang-set")); } catch (e) {}
    });
  });

  // CTA service selector -> mailto body (progressive: link already works without JS)
  var dcta = document.querySelector(".cta .btn-primary");
  if (dcta) {
    dcta.addEventListener("click", function () {
      var picked = [].slice.call(document.querySelectorAll(".selector input:checked")).map(function (i) { return i.value; });
      var href = dcta.getAttribute("href").split("&body=")[0];
      var es = (document.documentElement.lang || "en").slice(0, 2) === "es";
      var lead = es ? "Interes en: " : "Interested in: ";
      if (picked.length) href += "&body=" + encodeURIComponent(lead + picked.join(", "));
      dcta.setAttribute("href", href);
    });
  }

  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();
