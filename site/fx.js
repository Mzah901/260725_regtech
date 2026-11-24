// Shared motion for every page (styles in fx.css). Loaded with `defer`, so the page is already parsed when this runs.
(() => {
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 1. Click ring: a red circle spreads from wherever you click or tap.
  if (!still) addEventListener("pointerdown", (ev) => {
    const ring = document.createElement("span");
    ring.className = "fx-ring"; ring.style.left = ev.clientX + "px"; ring.style.top = ev.clientY + "px";
    ring.addEventListener("animationend", () => ring.remove());
    document.body.append(ring);
  }, { passive: true });

  // 2. Reading bar: how far down the page you are.
  const bar = document.createElement("div"); bar.className = "fx-bar"; bar.setAttribute("aria-hidden", "true"); document.body.append(bar);
  let queued = false;
  const paint = () => {
    queued = false;
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${max > 40 ? Math.min(1, scrollY / max) : 0})`;
  };
  addEventListener("scroll", () => { if (!queued) { queued = true; requestAnimationFrame(paint); } }, { passive: true });
  addEventListener("resize", paint); paint();

  // 3. Scroll reveal: blocks fade up as they come into view; ones arriving together follow each other a beat apart.
  // A page can name its own blocks with data-reveal; otherwise these common ones are used.
  const picks = document.querySelectorAll("[data-reveal], main section, main article > *:not(.rank), main .connections, main figure, main .index > li, .chapters > li, footer");
  if (!still && "IntersectionObserver" in window) {
    const seen = new IntersectionObserver((entries) => {
      let n = 0;
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        e.target.style.setProperty("--fx-d", Math.min(n++ * 0.07, 0.35) + "s");
        e.target.classList.add("fx-in"); seen.unobserve(e.target);
        // Once it has risen, hand the element back to its own styles (its own hover transitions, for one).
        e.target.addEventListener("transitionend", function done(t) {
          if (t.target !== e.target || t.propertyName !== "translate") return;
          e.target.classList.remove("fx-r", "fx-in"); e.target.style.removeProperty("--fx-d"); e.target.removeEventListener("transitionend", done);
        });
      }
    }, { rootMargin: "0px 0px -8% 0px" });
    for (const el of picks) { el.classList.add("fx-r"); seen.observe(el); }
  }

  // 4. Faster page changes: Chrome and Edge fetch a same-site page in the background as soon as you hover its link.
  if (HTMLScriptElement.supports && HTMLScriptElement.supports("speculationrules")) {
    const rules = document.createElement("script"); rules.type = "speculationrules";
    rules.textContent = JSON.stringify({ prefetch: [{ source: "document", where: { href_matches: "/*" }, eagerness: "moderate" }] });
    document.head.append(rules);
  }

  // 5. Browsers without view transitions: fade the page out before following a same-site link.
  if (!still && !("onpagereveal" in window)) {
    addEventListener("click", (ev) => {
      const a = ev.target.closest && ev.target.closest("a[href]");
      if (!a || ev.defaultPrevented || ev.button || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey || a.target || a.hasAttribute("download")) return;
      const url = new URL(a.href, location.href);
      if (url.origin !== location.origin || (url.pathname === location.pathname && url.hash)) return;
      ev.preventDefault();
      document.documentElement.classList.add("fx-leave");
      setTimeout(() => (location.href = url.href), 180);
    });
  }
  // Coming back with the Back button can restore a faded page from memory: show it again.
  addEventListener("pageshow", () => document.documentElement.classList.remove("fx-leave"));
})();
