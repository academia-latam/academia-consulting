/* AcademIAS — MANIFESTO cinematic choreography.
   Progressive enhancement: if GSAP is missing or the user prefers
   reduced motion, we bail and the page stays fully visible/static.
   Vendored deps (assets/vendor): gsap, ScrollTrigger, lenis, SplitType. */
(function () {
  "use strict";
  var root = document.documentElement;
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var small = matchMedia("(max-width: 800px)").matches;

  if (reduce || !window.gsap || !window.ScrollTrigger) return; // stay static + visible

  var gsap = window.gsap;
  gsap.registerPlugin(window.ScrollTrigger);
  root.classList.add("mf-enhanced");

  // ---- Lenis smooth scroll (desktop only; native touch on mobile) ----
  if (!small && window.Lenis) {
    var lenis = new window.Lenis({ lerp: 0.1, wheelMultiplier: 1, smoothWheel: true });
    lenis.on("scroll", window.ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    window.__lenis = lenis;
  }

  function splitChars(el) {
    if (!el || !window.SplitType) return null;
    return new window.SplitType(el, { types: "words,chars", tagName: "span" });
  }

  // ---- ACT 0 · HERO: char assemble on load, warp + parallax on scroll ----
  var hero = document.querySelector(".mf-hero");
  if (hero) {
    var l1 = splitChars(hero.querySelector(".l1"));
    var l2 = splitChars(hero.querySelector(".l2"));
    var heroChars = [].concat(l1 ? l1.chars : [], l2 ? l2.chars : []);
    if (heroChars.length) {
      gsap.set(heroChars, { yPercent: 115, opacity: 0 });
      gsap.to(heroChars, { yPercent: 0, opacity: 1, duration: 0.9, ease: "expo.out", stagger: 0.018, delay: 0.15 });
    }
    var sub = hero.querySelector(".mf-hero__sub");
    var kick = hero.querySelector(".mf-kick");
    if (kick) gsap.from(kick, { opacity: 0, y: 14, duration: 0.7, ease: "power2.out", delay: 0.05 });
    if (sub) gsap.from(sub, { opacity: 0, y: 18, duration: 0.8, ease: "power2.out", delay: 0.55 });

    var heroBg = hero.querySelector(".mf-hero__bg");
    if (heroBg) {
      gsap.to(heroBg, { yPercent: 16, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
    }
    // warp the Faust etching as you leave the hero
    var warp = document.querySelector("#mf-warp feDisplacementMap");
    if (warp) {
      gsap.fromTo(warp, { attr: { scale: 0 } }, { attr: { scale: 34 }, ease: "none",
        scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
    }
    // title drifts up + fades as hero exits
    gsap.to(".mf-hero__in", { yPercent: -18, opacity: 0.15, ease: "none",
      scrollTrigger: { trigger: hero, start: "center top", end: "bottom top", scrub: true } });
  }

  // ---- ACTS 1..5: pin + scrub reveal ----
  gsap.utils.toArray(".act").forEach(function (act) {
    var splitMedia = act.querySelector(".act__media img");
    var fullBg = act.querySelector(".act__bg img");
    var h = act.querySelector(".act__h");
    var split = splitChars(h);
    var chars = split ? split.chars : [];
    var num = act.querySelector(".act__num");
    var rule = act.querySelector(".act__rule");
    var p = act.querySelector(".act__p");
    var eyebrow = act.querySelector(".act__eyebrow");

    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: act,
        start: "top top",
        end: "+=130%",
        pin: !small,
        scrub: 0.6,
        anticipatePin: 1
      }
    });

    // numeral stays visible (opacity from CSS) and anchors each scene; only scales
    if (num) tl.fromTo(num, { scale: 1.16, yPercent: (act.classList.contains("act--split") ? -4 : 4) },
                            { scale: 1, yPercent: 0, ease: "none" }, 0);
    // split acts: clip-wipe the bounded media column
    if (splitMedia) tl.fromTo(splitMedia, { clipPath: "inset(0% 100% 0% 0%)", scale: 1.14 },
                                          { clipPath: "inset(0% 0% 0% 0%)", scale: 1, ease: "none" }, 0);
    // full-bleed acts: keep the etching present (fade + settle), never an empty color field
    if (fullBg) tl.fromTo(fullBg, { scale: 1.16, opacity: 0.5 }, { scale: 1, opacity: 1, ease: "none" }, 0);
    var warpMap = act.querySelector("feDisplacementMap");
    if (warpMap) tl.fromTo(warpMap, { attr: { scale: 0 } }, { attr: { scale: 26 }, ease: "none" }, 0);
    if (eyebrow) tl.fromTo(eyebrow, { opacity: 0, y: 16 }, { opacity: 1, y: 0, ease: "none" }, 0.05);
    if (chars.length) {
      gsap.set(chars, { display: "inline-block" });
      tl.fromTo(chars, { yPercent: 120, opacity: 0 }, { yPercent: 0, opacity: 1, stagger: 0.012, ease: "none" }, 0.08);
    } else if (h) {
      tl.fromTo(h, { opacity: 0, y: 30 }, { opacity: 1, y: 0, ease: "none" }, 0.08);
    }
    if (rule) tl.fromTo(rule, { scaleX: 0 }, { scaleX: 1, ease: "none" }, 0.35);
    if (p) tl.fromTo(p, { opacity: 0, y: 22 }, { opacity: 1, y: 0, ease: "none" }, 0.4);
  });

  // ---- DATA BEAT: count up on enter ----
  gsap.utils.toArray(".mf-data__n").forEach(function (n) {
    var target = parseInt(n.getAttribute("data-count"), 10) || 0;
    var obj = { v: 0 };
    window.ScrollTrigger.create({
      trigger: n,
      start: "top 80%",
      once: true,
      onEnter: function () {
        gsap.to(obj, { v: target, duration: 1.4, ease: "power2.out",
          onUpdate: function () { n.textContent = Math.round(obj.v); } });
      }
    });
  });

  // reveal simple elements that use data-mf-reveal (close section)
  gsap.utils.toArray("[data-mf-reveal]").forEach(function (el) {
    gsap.from(el, { opacity: 0, y: 28, duration: 0.9, ease: "power3.out",
      scrollTrigger: { trigger: el, start: "top 85%", once: true } });
  });

  window.addEventListener("load", function () { window.ScrollTrigger.refresh(); });
})();
