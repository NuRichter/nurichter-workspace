/* NuRichter Workspace — interaksi situs (tanpa dependensi) */
(() => {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  root.classList.add("js");

  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (_) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (_) {} },
  };

  /* ---------------------------------------------------------- tema */
  const themeBtn = $(".theme-toggle");
  const isDark = () => root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  themeBtn?.addEventListener("click", () => {
    const next = isDark() ? "light" : "dark";
    root.dataset.theme = next;
    store.set("nr-theme", next);
    window.dispatchEvent(new CustomEvent("nr-theme"));
  });

  /* ---------------------------------------------------------- menu ponsel */
  const menuBtn = $(".menu-btn");
  const mnav = $("#mnav");
  const setMenu = (open) => {
    menuBtn.setAttribute("aria-expanded", String(open));
    mnav.hidden = !open;
    if (open) mnav.querySelector("a")?.focus();
  };
  menuBtn?.addEventListener("click", () => setMenu(menuBtn.getAttribute("aria-expanded") !== "true"));
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && menuBtn?.getAttribute("aria-expanded") === "true") { setMenu(false); menuBtn.focus(); }
  });

  /* ---------------------------------------------------------- command palette */
  const dlg = $(".cmd");
  const q = $(".cmd-q");
  const list = $(".cmd-list");
  let results = [];
  let sel = 0;

  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const norm = (s) => String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  const hl = (text, term) => {
    if (!term) return esc(text);
    const i = norm(text).indexOf(term);
    if (i < 0) return esc(text);
    return esc(text.slice(0, i)) + "<mark>" + esc(text.slice(i, i + term.length)) + "</mark>" + esc(text.slice(i + term.length));
  };

  const tt = (k, d) => (window.NR_TT ? window.NR_TT(k, d) : d);
  const KIND = { page: "Halaman", work: "Karya", brand: "Sub-brand", project: "Proyek", article: "Tulisan", profile: "Profil" };
  const label = (it) => (it.tk ? tt(it.tk, it.t) : it.t).replace(/<[^>]+>/g, "");
  const desc = (it) => (it.dk ? tt(it.dk, it.d) : it.d || "").replace(/<[^>]+>/g, "");
  function score(item, term) {
    if (!term) return item.k === "page" ? 3 : item.k === "work" ? 2 : 0;
    const t = norm(label(item));
    if (t.startsWith(term)) return 10;
    if (t.includes(term)) return 6;
    if (norm(desc(item)).includes(term) || norm(item.t).includes(term)) return 3;
    // cocok per huruf berurutan
    let j = 0;
    for (const ch of t) if (ch === term[j]) j++;
    return j === term.length ? 1 : 0;
  }

  function render() {
    const term = norm(q.value.trim());
    results = (window.NR_INDEX || [])
      .map((it) => ({ it, s: score(it, term) }))
      .filter((r) => r.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 12)
      .map((r) => r.it);
    sel = 0;
    list.innerHTML = results.length
      ? results.map((it, i) => {
          const ext = it.u.startsWith("http");
          return `<li><a role="option" href="${esc(it.u)}"${ext ? ' target="_blank" rel="noopener"' : ""} aria-selected="${i === sel}" data-i="${i}">
            <span>${hl(label(it), term)}</span>${it.d ? `<small>${esc(desc(it))}</small>` : ""}<em>${esc(tt("js.kind." + it.k, KIND[it.k]))}</em></a></li>`;
        }).join("")
      : `<li class="empty" style="padding:16px">${esc(tt("js.noresults", "Tidak ada hasil untuk"))} “${esc(q.value)}”.</li>`;
  }

  function move(d) {
    if (!results.length) return;
    sel = (sel + d + results.length) % results.length;
    $$("a", list).forEach((a, i) => a.setAttribute("aria-selected", String(i === sel)));
    $$("a", list)[sel]?.scrollIntoView({ block: "nearest" });
  }

  function openCmd() {
    if (!dlg || dlg.open) return;
    q.value = "";
    render();
    dlg.showModal();
    q.focus();
  }

  $$(".cmd-open").forEach((b) => b.addEventListener("click", openCmd));
  q?.addEventListener("input", render);
  q?.addEventListener("keydown", (ev) => {
    if (ev.key === "ArrowDown") { ev.preventDefault(); move(1); }
    else if (ev.key === "ArrowUp") { ev.preventDefault(); move(-1); }
    else if (ev.key === "Enter") { ev.preventDefault(); $$("a", list)[sel]?.click(); dlg.close(); }
  });
  list?.addEventListener("mousemove", (ev) => {
    const a = ev.target.closest("a[data-i]");
    if (a && +a.dataset.i !== sel) { sel = +a.dataset.i; move(0); }
  });
  list?.addEventListener("click", (ev) => { if (ev.target.closest("a")) dlg.close(); });
  dlg?.addEventListener("click", (ev) => { if (ev.target === dlg) dlg.close(); });
  document.addEventListener("keydown", (ev) => {
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName);
    if ((ev.key === "k" || ev.key === "K") && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); openCmd(); }
    else if (ev.key === "/" && !typing) { ev.preventDefault(); openCmd(); }
  });
  if (/Mac|iPhone|iPad/.test(navigator.platform)) $$(".cmd-open kbd").forEach((k) => (k.textContent = "⌘K"));

  /* ---------------------------------------------------------- reveal saat terlihat */
  const revealables = $$(".sec > *:not(.sh):not(.wi-preview), .cs-body > *, .brand-row, .svc, .tl-i, .stats > div, .dom");
  if ("IntersectionObserver" in window && !reduced) {
    revealables.forEach((el) => el.classList.add("rv"));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    revealables.forEach((el) => io.observe(el));
  }

  // grafik batang tumbuh saat terlihat
  const bars = $$(".bars");
  if ("IntersectionObserver" in window) {
    const bo = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in"); bo.unobserve(en.target); } });
    }, { threshold: .4 });
    bars.forEach((b) => bo.observe(b));
  } else bars.forEach((b) => b.classList.add("in"));

  /* ---------------------------------------------------------- indeks karya: pratinjau mengikuti kursor */
  const prev = $(".wi-preview");
  if (prev && matchMedia("(hover: hover)").matches) {
    let x = 0, y = 0, tx = 0, ty = 0, raf = 0;
    const loop = () => {
      x += (tx - x) * .18; y += (ty - y) * .18;
      prev.style.transform = `translate3d(${x + 24}px, ${y - 110}px, 0)`;
      raf = Math.abs(tx - x) + Math.abs(ty - y) > .5 ? requestAnimationFrame(loop) : 0;
    };
    $$(".wi").forEach((a) => {
      a.addEventListener("mouseenter", () => {
        const src = a.dataset.preview;
        if (!src) { prev.classList.remove("on"); return; }
        if (!prev.src.endsWith(src)) prev.src = src;
        prev.classList.add("on");
      });
      a.addEventListener("mouseleave", () => prev.classList.remove("on"));
      a.addEventListener("mousemove", (ev) => {
        tx = ev.clientX; ty = ev.clientY;
        if (!prev.classList.contains("on")) { x = tx; y = ty; }
        if (!raf) raf = requestAnimationFrame(loop);
      });
    });
  }

  /* ---------------------------------------------------------- karya: filter bidang + scrollspy */
  const works = $$(".cs");
  if (works.length) {
    const chips = $$(".chips .chip");
    const tocLinks = $$(".toc a");
    const empty = $(".works .empty");
    const apply = (f) => {
      chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.f === f)));
      let shown = 0;
      works.forEach((w) => {
        const on = f === "all" || w.dataset.disc.split(" ").includes(f);
        w.hidden = !on;
        if (on) shown++;
        const li = tocLinks.find((a) => a.hash === "#" + w.id)?.parentElement;
        li?.classList.toggle("off", !on);
        if (on) w.querySelectorAll(".rv").forEach((el) => el.classList.add("in"));
      });
      empty.hidden = shown > 0;
    };
    chips.forEach((c) => c.addEventListener("click", () => apply(c.dataset.f)));

    if ("IntersectionObserver" in window) {
      const spy = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) tocLinks.forEach((a) => a.classList.toggle("on", a.hash === "#" + en.target.id));
        });
      }, { rootMargin: "-40% 0px -55% 0px" });
      works.forEach((w) => spy.observe(w));
    }
  }

  /* ---------------------------------------------------------- arsip: status + pencarian */
  const arch = $(".arch");
  if (arch) {
    const rows = $$("tbody tr", arch);
    const chips = $$(".arch-tools .chip");
    const input = $(".arch-q");
    const empty = $(".arch-empty");
    let f = "all";
    const apply = () => {
      const term = norm(input.value.trim());
      let n = 0;
      rows.forEach((r) => {
        const on = (f === "all" || r.dataset.s === f) && (!term || norm(r.textContent).includes(term));
        r.hidden = !on;
        if (on) n++;
      });
      empty.hidden = n > 0;
    };
    chips.forEach((c) => c.addEventListener("click", () => {
      f = c.dataset.f;
      chips.forEach((x) => x.setAttribute("aria-pressed", String(x === c)));
      apply();
    }));
    input.addEventListener("input", apply);

    // urutkan kolom: No., Tahun, Proyek, Status
    const tbody = arch.tBodies[0];
    const ORDER = { active: 0, future: 1, temporal: 2, finished: 3, abandoned: 4 };
    const keyOf = (r, col) => {
      if (col === 0) return parseInt(r.cells[0].textContent.replace(/\D/g, ""), 10);
      if (col === 1) { const y = parseInt(r.cells[1].textContent, 10); return isNaN(y) ? 9999 : y; }
      if (col === 4) return ORDER[r.dataset.s] ?? 9;
      return norm(r.cells[col].textContent);
    };
    $$("thead th", arch).forEach((th, col) => {
      if (col === 3) return;
      const b = document.createElement("button");
      b.type = "button";
      b.append(...th.childNodes);
      th.append(b);
      th.setAttribute("aria-sort", col === 0 ? "ascending" : "none");
      b.addEventListener("click", () => {
        const dir = th.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        $$("thead th", arch).forEach((x) => x.hasAttribute("aria-sort") && x.setAttribute("aria-sort", "none"));
        th.setAttribute("aria-sort", dir);
        const sorted = rows.slice().sort((r1, r2) => {
          const a = keyOf(r1, col), z = keyOf(r2, col);
          return (a > z ? 1 : a < z ? -1 : 0) * (dir === "ascending" ? 1 : -1);
        });
        tbody.append(...sorted);
      });
    });
  }

  /* ---------------------------------------------------------- salin warna (halaman brand) */
  $$("[data-copy]").forEach((btn) => btn.addEventListener("click", async () => {
    const val = btn.dataset.copy;
    try { await navigator.clipboard.writeText(val); } catch (_) {
      const ta = document.createElement("textarea"); ta.value = val; document.body.append(ta); ta.select();
      try { document.execCommand("copy"); } catch (__) {} ta.remove();
    }
    btn.dataset.done = `${(window.NR_TT ? window.NR_TT("js.copied", "Disalin") : "Disalin")} ${val}`;
    btn.classList.add("done");
    setTimeout(() => btn.classList.remove("done"), 1600);
  }));

  /* ---------------------------------------------------------- formulir kontak → WhatsApp */
  const form = $(".cform");
  if (form) {
    const need = new URLSearchParams(location.search).get("need");
    const sel = form.elements.need;
    if (need) {
      if (![...sel.options].some((o) => o.value === need)) sel.add(new Option(need, need));
      sel.value = need;
    }
    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      let ok = true;
      ["name", "email", "msg"].forEach((n) => {
        const el = form.elements[n];
        const bad = !el.value.trim() || (n === "email" && !/^\S+@\S+\.\S+$/.test(el.value));
        el.setAttribute("aria-invalid", String(bad));
        if (bad && ok) { el.focus(); ok = false; }
      });
      const note = $(".cform-note");
      const tt = (k, d) => (window.NR_TT ? window.NR_TT(k, d) : d);
      if (!ok) { note.textContent = tt("js.form.err", "Lengkapi nama, email yang valid, dan pesan."); return; }
      const v = (n) => form.elements[n].value.trim();
      const needText = sel.options[sel.selectedIndex]?.textContent || v("need");
      const text = `${tt("js.form.hello", "Halo NuRichter Workspace,")}\n\n${tt("js.form.name", "Nama")}: ${v("name")}\nEmail: ${v("email")}` +
        (v("org") ? `\n${tt("js.form.org", "Instansi")}: ${v("org")}` : "") + `\n${tt("js.form.need", "Kebutuhan")}: ${needText}\n\n${v("msg")}`;
      window.open(`https://wa.me/6281280717345?text=${encodeURIComponent(text)}`, "_blank", "noopener");
      note.textContent = tt("js.form.ok", "WhatsApp dibuka di tab baru.");
    });
  }
})();
