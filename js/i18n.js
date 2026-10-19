/* NuRichter Workspace — terjemahan 30 bahasa.
   HTML ditulis dalam bahasa Indonesia; setiap teks punya kunci (data-t).
   Urutan pencarian: bahasa pilihan → kunci lain dengan teks sumber sama →
   bahasa Inggris → teks Indonesia. Teks yang jatuh ke bahasa Inggris bisa
   diterjemahkan di perangkat lewat Translator API (Chrome) bila tersedia. */
(() => {
  "use strict";
  const root = document.documentElement;
  const LANGS = window.NR_LANGS || [];
  const byCode = Object.fromEntries(LANGS.map((l) => [l.c, l]));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (_) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (_) {} },
  };

  const param = new URLSearchParams(location.search).get("lang");
  const saved = store.get("nr-lang");
  let lang = (param && byCode[param] && param) || (saved && byCode[saved] && saved) || "id";
  if (!param && !saved) {
    // kunjungan pertama: ikuti bahasa browser bila didukung
    const pref = (navigator.languages || [navigator.language || ""]).map((x) => x.toLowerCase().split("-")[0]);
    const hit = pref.find((c) => byCode[c]);
    if (hit) lang = hit;
  }

  let dict = {};       // kunci -> teks terjemahan untuk bahasa aktif
  let fallback = {};   // kunci yang memakai bahasa Inggris
  let source = {};     // id.json

  window.NR_LANG = lang;
  window.NR_TT = (key, def) => dict[key] ?? def ?? key;

  const fetchJSON = (c) => fetch(`i18n/${c}.json`, { cache: "force-cache" }).then((r) => (r.ok ? r.json() : {})).catch(() => ({}));

  function setFont(l) {
    const info = byCode[l];
    if (!info || !info.font) return;
    const fam = info.font;
    const id = "nr-font-" + fam.replace(/\s+/g, "-");
    if (!document.getElementById(id)) {
      const link = document.createElement("link");
      link.id = id;
      link.rel = "stylesheet";
      link.href = `https://fonts.googleapis.com/css2?family=${encodeURIComponent(fam)}:wght@400;500;700&display=swap`;
      document.head.appendChild(link);
    }
    root.style.setProperty("--f-script", `"${fam}"`);
    root.classList.add("has-script");
  }

  async function build(l) {
    const [id, en, cur] = await Promise.all([fetchJSON("id"), l === "en" ? null : fetchJSON("en"), fetchJSON(l)]);
    source = id;
    const eng = en || cur;
    // teks sumber yang sama di kunci lain → pakai terjemahannya
    const byText = {};
    const byTextEn = {};
    for (const [k, v] of Object.entries(id)) {
      if (cur[k] != null) byText[v] ??= cur[k];
      if (eng[k] != null) byTextEn[v] ??= eng[k];
    }
    const sheetWord = cur["tb.sheet"] ?? eng["tb.sheet"];
    for (const [k, v] of Object.entries(id)) {
      let t = cur[k] ?? byText[v];
      if (t == null && k.startsWith("meta.") && k.endsWith(".title")) {
        const pid = k.slice(5, -6);
        const pt = cur[`page.${pid}.title`] ?? byText[id[`page.${pid}.title`]];
        if (pt) t = pid === "home" ? v : `${pt.replace(/<[^>]+>/g, "")} — NuRichter Workspace`;
      }
      if (t == null && k.startsWith("sheet.") && sheetWord) t = v.replace(/^Lembar/, sheetWord);
      if (t == null) { const en2 = eng[k] ?? byTextEn[v]; if (en2 != null) { t = en2; if (l !== "en") fallback[k] = true; } }
      dict[k] = t ?? v;
    }
  }

  function apply() {
    document.querySelectorAll("[data-t]").forEach((el) => {
      const v = dict[el.dataset.t];
      if (v == null) return;
      if (el.tagName === "OPTION") el.textContent = v;
      else el.innerHTML = v;
      if (fallback[el.dataset.t]) el.setAttribute("lang", "en");
    });
    document.querySelectorAll("[data-ta]").forEach((el) => {
      el.dataset.ta.split(";").forEach((pair) => {
        const [attr, key] = pair.split(":");
        if (dict[key] != null) el.setAttribute(attr, dict[key].replace(/<[^>]+>/g, " "));
      });
    });
    const tt = document.querySelector("title[data-t-title]");
    if (tt && dict[tt.dataset.tTitle]) document.title = dict[tt.dataset.tTitle];
  }

  /* terjemahan di perangkat untuk teks yang jatuh ke bahasa Inggris */
  async function onDevice(l, userGesture) {
    if (!("Translator" in self) || l === "en" || l === "id") return;
    const keys = Object.keys(fallback);
    if (!keys.length) return;
    let state;
    try { state = await self.Translator.availability({ sourceLanguage: "en", targetLanguage: l }); } catch (_) { return; }
    if (state === "unavailable") return;
    if (state !== "available" && !userGesture) { showOffer(l); return; }
    const note = toast(window.NR_TT("js.translating", "…"));
    try {
      const tr = await self.Translator.create({ sourceLanguage: "en", targetLanguage: l });
      const cacheKey = `nr-tr-${l}`;
      let cache = {};
      try { cache = JSON.parse(sessionStorage.getItem(cacheKey) || "{}"); } catch (_) {}
      for (const k of keys) {
        const src = dict[k];
        if (/<[^>]+>/.test(src)) continue;
        const out = cache[k] || (await tr.translate(src));
        cache[k] = out;
        dict[k] = out;
        document.querySelectorAll(`[data-t="${k}"]`).forEach((el) => { el.textContent = out; el.setAttribute("lang", l); });
      }
      try { sessionStorage.setItem(cacheKey, JSON.stringify(cache)); } catch (_) {}
    } catch (_) { /* biarkan bahasa Inggris */ }
    note?.remove();
  }

  function toast(text) {
    const n = document.createElement("div");
    n.className = "toast";
    n.setAttribute("role", "status");
    n.textContent = text;
    document.body.appendChild(n);
    return n;
  }

  function showOffer(l) {
    const n = toast("");
    const b = document.createElement("button");
    b.type = "button";
    b.className = "btn btn-solid";
    b.textContent = `${byCode[l].n}: ${window.NR_TT("js.translating", "").replace(/…$/, "")}?`;
    b.addEventListener("click", () => { n.remove(); onDevice(l, true); });
    const x = document.createElement("button");
    x.type = "button";
    x.className = "tool-btn";
    x.textContent = "✕";
    x.setAttribute("aria-label", window.NR_TT("ui.close", "Close"));
    x.addEventListener("click", () => n.remove());
    n.append(b, x);
  }

  /* pemilih bahasa */
  function setupPicker() {
    const dlg = document.querySelector(".langs");
    const code = document.querySelector(".lang-code");
    if (code) code.textContent = lang.toUpperCase();
    document.querySelectorAll(".lang-open").forEach((b) => b.addEventListener("click", () => dlg?.showModal()));
    dlg?.querySelector(".langs-x")?.addEventListener("click", () => dlg.close());
    dlg?.addEventListener("click", (ev) => { if (ev.target === dlg) dlg.close(); });
    dlg?.querySelectorAll("[data-lang]").forEach((b) => {
      if (b.dataset.lang === lang) b.setAttribute("aria-current", "true");
      b.addEventListener("click", () => {
        store.set("nr-lang", b.dataset.lang);
        const u = new URL(location.href);
        u.searchParams.delete("lang");
        location.replace(u.toString());
      });
    });
  }

  function reveal() { root.classList.remove("i18n-wait"); }

  async function run() {
    setupPicker();
    const info = byCode[lang];
    root.lang = lang;
    root.dir = info?.dir || "ltr";
    if (lang === "id") { reveal(); return; }
    setFont(lang);
    try {
      await build(lang);
      apply();
    } finally {
      reveal();
    }
    window.dispatchEvent(new CustomEvent("nr-i18n", { detail: lang }));
    onDevice(lang, false);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
