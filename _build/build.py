#!/usr/bin/env python3
"""Generator statis NuRichter Workspace.

    python3 _build/build.py

Membaca _build/data.py, menulis semua halaman .html ke root repo.
Semua teks diberi kunci terjemahan (data-t). Sumber bahasa Indonesia
diekspor ke i18n/id.json; terjemahan lain ada di _build/i18n/<kode>.json
dan disalin ke i18n/ saat build. Tidak butuh dependensi.
"""
import json
import os
import shutil
import sys
from datetime import date
from html import escape as e

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from data import (ARTICLES, BRANDS, DISCIPLINES, LAB_CAPS, LAB_PROJECTS, MACHINES, PARTNERS, PROCESS,  # noqa: E402
                  PROJECTS, SERVICES, SITE, SOCIAL, STATUS, TEAM, TIMELINE, WORKS)
from figures import FIGS, seismo  # noqa: E402
from langs import LANGS  # noqa: E402

CREDITS = {c["file"].split("/")[-1].rsplit(".", 1)[0]: c for c in json.load(open(os.path.join(HERE, "credits.json"), encoding="utf-8"))}
SHOTS = {"wellsense-dashboard": (1600, 1000), "wellsense-regime": (1600, 1000)}

WORK_MEDIA = {
    "wellsense": {"cover": "wellsense-dashboard", "gallery": ["wellsense-regime", "wellsense-rig"]},
    "bst-avl": {"svg": "bstavl"},
    "gif-pdf": {"svg": "gifpdf"},
    "agrihex": {"cover": "agrihex-drone", "gallery": ["hexacopter"]},
    "sperm-quant": {"cover": "microscope", "svg2": "casa"},
    "ragnarok-trainer": {"cover": "electrical-panel", "gallery": ["plc-cabinet"]},
    "armx": {"cover": "robot-arm-diy", "gallery": ["robot-arm-acrylic"]},
    "mulya-jaya": {"cover": "cnc-acrylic", "gallery": ["trophy"]},
    "seratus-ilmu": {"svg": "web"},
    "catalyst": {"svg": "books"},
    "audio": {"cover": "dj-mixer"},
}
BRAND_PHOTO = {"mulya-jaya": "trophy", "rigroom": "robot-arm-acrylic", "ragnarok": "plc-cabinet"}

# ------------------------------------------------------------------ i18n

K = {}  # kunci -> teks Indonesia (sumber)


def T(key, text):
    """Teks yang bisa diterjemahkan, dibungkus span dengan kunci."""
    prev = K.get(key)
    if prev is not None and prev != text:
        raise ValueError(f"kunci {key} dipakai untuk dua teks berbeda")
    K[key] = text
    return f'<span data-t="{key}">{text}</span>'


def R(key, text):
    """Daftarkan kunci tanpa membungkus (untuk atribut dan string JS)."""
    K[key] = text
    return text


NAV = [
    ("works.html", "nav.works", "Karya"),
    ("projects.html", "nav.archive", "Arsip"),
    ("products.html", "nav.brands", "Sub-brand"),
    ("services.html", "nav.services", "Layanan"),
    ("lab.html", "nav.labs", "Labs"),
    ("about.html", "nav.about", "Tentang"),
    ("contact.html", "nav.contact", "Kontak"),
]
EXTRA_NAV = [("index.html", "nav.home", "Beranda"), ("history.html", "nav.history", "Sejarah"), ("credits.html", "nav.credits", "Kredit foto")]

SHEETS = {}

BOLT = '<svg class="bolt" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2L5 13h6l-3 9 11-13h-6l3-7z" fill="currentColor"/></svg>'
ARROW = '<svg class="ar" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
EXT = '<svg class="ar" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 11L11 5M6 5h5v5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'

DISC = dict(DISCIPLINES)


# ------------------------------------------------------------------ komponen

def link(href, key, label):
    ext = href.startswith("http")
    attrs = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="lnk" href="{e(href)}"{attrs}>{T(key, e(label))}{EXT if ext else ARROW}</a>'


def raw_link(href, label):
    """Tautan dengan label yang tidak diterjemahkan (nama diri)."""
    ext = href.startswith("http")
    attrs = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="lnk" href="{e(href)}"{attrs}>{e(label)}{EXT if ext else ARROW}</a>'


def status(s):
    return f'<span class="st st-{s}"><i></i>{T("status." + s, STATUS[s])}</span>'


def photo(name, alt_key, alt, cls="", sizes="(max-width: 800px) 100vw, 50vw", eager=False, caption=True):
    if name in SHOTS:
        w, h = SHOTS[name]
        cap = T("ui.shot", "Tangkapan layar dari wellsense-sim.vercel.app")
    else:
        c = CREDITS[name]
        w, h = c["w"], c["h"]
        lic = f'CC {c["license"].upper()} {c["license_version"]}' if c["license"] not in ("cc0", "pdm") else ("CC0" if c["license"] == "cc0" else "Public domain")
        cap = f'{T("ui.photo", "Foto")}: <a href="{e(c["source"])}" target="_blank" rel="noopener">{e(c["creator"] or "Flickr")}</a> · <a href="{e(c["license_url"])}" target="_blank" rel="noopener">{lic}</a>'
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    fc = f"<figcaption>{cap}</figcaption>" if caption else ""
    R(alt_key, alt)
    return f'<figure class="ph {cls}"><img src="img/{name}.webp" alt="{e(alt)}" data-ta="alt:{alt_key}" width="{w}" height="{h}" {load} sizes="{sizes}">{fc}</figure>'


def frame(name, alt_key, alt):
    w, h = SHOTS[name]
    R(alt_key, alt)
    return (f'<figure class="browser"><div class="browser-bar"><i></i><i></i><i></i><span>wellsense-sim.vercel.app</span></div>'
            f'<img src="img/{name}.webp" alt="{e(alt)}" data-ta="alt:{alt_key}" width="{w}" height="{h}" loading="lazy" decoding="async"></figure>')


def sec_head(num, title_html, aside=""):
    a = f'<div class="sh-aside">{aside}</div>' if aside else ""
    return f'<header class="sh"><span class="sh-num">{num}</span><h2>{title_html}</h2>{a}</header>'


def page_head(pid, code, title, lede, extra=""):
    return f'''
<section class="ph-head wrap">
  <div class="ph-meta"><span>{T("sheet." + pid, code)}</span><span>NuRichter Workspace</span><span>Rev {SITE["rev"]}</span></div>
  <h1 class="display">{T("page." + pid + ".title", title)}</h1>
  <p class="lede">{T("page." + pid + ".lede", lede)}</p>
  {extra}
</section>'''


def lang_menu():
    items = "".join(
        f'<li><button type="button" data-lang="{c}" lang="{c}"><b>{n}</b><span>{en}</span></button></li>'
        for c, n, en, _d, _f in LANGS)
    return f'''
<dialog class="langs" aria-labelledby="langs-h">
  <div class="langs-in">
    <header><h2 id="langs-h">{T("ui.lang.title", "Bahasa")}</h2><button type="button" class="tool-btn langs-x" data-ta="aria-label:ui.close" aria-label="{R("ui.close", "Tutup")}">✕</button></header>
    <ul>{items}</ul>
    <p class="langs-note">{T("ui.lang.note", "Bahasa Indonesia dan Inggris diterjemahkan penuh. Bahasa lain menerjemahkan antarmuka dan ringkasan; paragraf panjang memakai bahasa Inggris, atau diterjemahkan di perangkat bila browser Anda mendukungnya.")}</p>
  </div>
</dialog>'''


def nav_html(current):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=page" if h == current else ""}>{T(k, l)}</a></li>' for h, k, l in NAV)
    return f'''
<a class="skip" href="#main">{T("ui.skip", "Langsung ke konten")}</a>
<header class="topbar" id="top">
  <div class="wrap topbar-in">
    <a class="brand" href="index.html" aria-label="NuRichter Workspace">{BOLT}<span>NuRichter</span><em>Workspace</em></a>
    <nav class="nav" data-ta="aria-label:ui.nav.main" aria-label="{R("ui.nav.main", "Utama")}"><ul>{items}</ul></nav>
    <div class="tools">
      <button class="tool-btn cmd-open" type="button" data-ta="aria-label:ui.search" aria-label="{R("ui.search", "Cari halaman dan karya")}"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10.5 10.5L14 14" stroke="currentColor" stroke-width="1.5"/></svg><kbd>Ctrl K</kbd></button>
      <button class="tool-btn lang-open" type="button" data-ta="aria-label:ui.lang.title" aria-label="Bahasa"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M2 8h12M8 2c-2.2 2.4-2.2 9.6 0 12M8 2c2.2 2.4 2.2 9.6 0 12" fill="none" stroke="currentColor" stroke-width="1.3"/></svg><span class="lang-code">ID</span></button>
      <button class="tool-btn theme-toggle" type="button" data-ta="aria-label:ui.theme" aria-label="{R("ui.theme", "Ganti tema terang/gelap")}"><svg class="i-sun" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3 3l1.4 1.4M11.6 11.6L13 13M3 13l1.4-1.4M11.6 4.4L13 3" stroke="currentColor" stroke-width="1.5"/></svg><svg class="i-moon" viewBox="0 0 16 16" aria-hidden="true"><path d="M13.5 9.5A5.5 5.5 0 0 1 6.5 2.5a5.5 5.5 0 1 0 7 7z" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button>
      <button class="tool-btn menu-btn" type="button" data-ta="aria-label:ui.menu" aria-label="{R("ui.menu", "Buka menu")}" aria-expanded="false" aria-controls="mnav"><span></span><span></span></button>
    </div>
  </div>
  <nav class="mnav" id="mnav" aria-label="Menu" hidden>
    <ul><li><a href="index.html">{T("nav.home", "Beranda")}</a></li>{items}<li><a href="history.html">{T("nav.history", "Sejarah")}</a></li></ul>
  </nav>
</header>'''


def footer_html(current):
    sheet = SHEETS.get(current, ("00", ""))[0]
    total = len(SHEETS)
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}<span>{h}</span></a></li>' for n, u, h in SOCIAL)
    pages = "".join(f'<li><a href="{h}">{T(k, l)}</a></li>' for h, k, l in [EXTRA_NAV[0]] + NAV + EXTRA_NAV[1:])
    return f'''
<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <p class="foot-say display">{T("foot.say", "Punya masalah teknis<br>yang perlu dibangun?")}</p>
      <div class="foot-cta">
        <a class="btn btn-solid" href="https://wa.me/{SITE["wa"]}" target="_blank" rel="noopener">WhatsApp {SITE["wa_display"]}</a>
        <a class="btn" href="mailto:{SITE["email"]}">{SITE["email"]}</a>
      </div>
    </div>
    <div class="foot-grid">
      <div><h3>{T("foot.pages", "Halaman")}</h3><ul class="foot-list">{pages}</ul></div>
      <div><h3>{T("foot.profiles", "Profil")}</h3><ul class="foot-list soc">{soc}</ul></div>
      <div><h3>{T("nav.about", "Tentang")}</h3><p class="mute">{T("foot.about", "Workspace engineering dan kreatif yang dibangun Ibnu Khoirul Anwar sejak 2020, diresmikan 2025. Berbasis di Rorotan, Jakarta Utara.")}</p></div>
    </div>
    <div class="tblock">
      <div><span>{T("tb.project", "Proyek")}</span>NuRichter Workspace</div>
      <div><span>{T("tb.sheet", "Lembar")}</span>{sheet} / {total:02d}</div>
      <div><span>{T("tb.rev", "Revisi")}</span>{SITE["rev"]}</div>
      <div><span>{T("tb.loc", "Lokasi")}</span>Jakarta, ID</div>
      <div><span>{T("tb.motto", "Moto")}</span>{SITE["tagline"]} ∞</div>
      <div><span>©</span>{date.today().year} NuRichter</div>
    </div>
  </div>
</footer>
<dialog class="cmd" aria-label="Search">
  <div class="cmd-in">
    <input class="cmd-q" type="search" data-ta="placeholder:cmd.ph" placeholder="{R("cmd.ph", "Cari karya, proyek, halaman…")}" autocomplete="off">
    <ul class="cmd-list" role="listbox"></ul>
    <p class="cmd-foot"><kbd>↑</kbd><kbd>↓</kbd> {T("cmd.pick", "pilih")} · <kbd>Enter</kbd> {T("cmd.open", "buka")} · <kbd>Esc</kbd> {T("cmd.close", "tutup")}</p>
  </div>
</dialog>
{lang_menu()}'''


def layout(fname, pid, title, desc, body, extra_head="", scripts=""):
    canon = SITE["url"] + "/" + ("" if fname == "index.html" else fname.replace(".html", ""))
    full_title = f"{title} — NuRichter Workspace" if fname != "index.html" else "NuRichter Workspace — Richterize The Infinity"
    R(f"meta.{pid}.title", full_title)
    R(f"meta.{pid}.desc", desc)
    hreflang = "".join(f'\n<link rel="alternate" hreflang="{c}" href="{canon}?lang={c}">' for c, *_ in LANGS)
    return f'''<!doctype html>
<html lang="id" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-t-title="meta.{pid}.title">{e(full_title)}</title>
<meta name="description" content="{e(desc)}" data-ta="content:meta.{pid}.desc">
<meta name="author" content="{SITE["founder"]}">
<meta name="google-site-verification" content="67CBEEY7FYGuQq-JT2VrVPUojU3lCzyV5SvF-bA6Los">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="x-default" href="{canon}">{hreflang}
<meta property="og:type" content="website">
<meta property="og:site_name" content="NuRichter Workspace">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE["url"]}/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f1efe9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0f0f0e" media="(prefers-color-scheme: dark)">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<script>(function(){{var d=document.documentElement;try{{var t=localStorage.getItem("nr-theme");if(t)d.dataset.theme=t}}catch(_){{}}var L="{" ".join(c for c, *_ in LANGS)}".split(" "),l=null;try{{l=new URLSearchParams(location.search).get("lang")||localStorage.getItem("nr-lang")}}catch(_){{}}if(!l){{var n=(navigator.languages||[navigator.language||""]);for(var i=0;i<n.length;i++){{var c=String(n[i]).toLowerCase().split("-")[0];if(L.indexOf(c)>-1){{l=c;break}}}}}}if(l&&l!=="id"&&L.indexOf(l)>-1){{d.lang=l;d.classList.add("i18n-wait");if(/^(ar|ur|fa)$/.test(l))d.dir="rtl";setTimeout(function(){{d.classList.remove("i18n-wait")}},2500)}}}})()</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..900&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="css/style.css">
{extra_head}
</head>
<body data-page="{fname}">
{nav_html(fname)}
<main id="main">
{body}
</main>
{footer_html(fname)}
<script src="js/search-index.js" defer></script>
<script src="js/langs.js" defer></script>
<script src="js/i18n.js" defer></script>
<script src="js/main.js" defer></script>
{scripts}
</body>
</html>
'''


# ------------------------------------------------------------------ halaman

def work_by(id_):
    return next(w for w in WORKS if w["id"] == id_)


def wk(w, field):
    """Teks karya yang bisa diterjemahkan."""
    return T(f'w.{w["id"]}.{field}', w[field])


def work_visual(w, eager=False, size="(max-width: 800px) 100vw, 60vw"):
    m = WORK_MEDIA[w["id"]]
    if "cover" in m:
        if m["cover"] in SHOTS:
            return frame(m["cover"], "alt.ws.dash", "Dashboard Wellsense: aliran sensor, status zona, dan output LSTM")
        return photo(m["cover"], f'alt.{w["id"]}.cover', f'{w["title"]}: foto ilustrasi', sizes=size, eager=eager)
    return f'<figure class="drawing"><div class="drawing-in">{FIGS[m["svg"]]()}</div><figcaption>Fig. {w["code"]} · {T("ui.schematic", "gambar skematis")}</figcaption></figure>'


def metrics_html(w):
    return '<dl class="kpis">' + "".join(
        f'<div><dt>{T(f"w.{w["id"]}.m{i}.v", v)}</dt><dd>{T(f"w.{w["id"]}.m{i}.l", l)}</dd></div>'
        for i, (v, l) in enumerate(w["metrics"])) + "</dl>"


def page_index():
    feat = work_by("wellsense")
    rows = []
    for w in WORKS:
        prev = WORK_MEDIA[w["id"]].get("cover") or ""
        rows.append(f'''
      <li><a class="wi" href="works.html#{w["id"]}" data-preview="{f"img/{prev}.webp" if prev else ""}">
        <span class="wi-code">{w["code"]}</span>
        <span class="wi-title">{wk(w, "title")}</span>
        <span class="wi-kick">{wk(w, "kicker")}</span>
        <span class="wi-year">{w["year"]}</span>
        {ARROW}
      </a></li>''')
    arts = "".join(f'''
      <li><a class="art" href="{a["url"]}" target="_blank" rel="noopener">
        <time datetime="{a["date"]}">{a["date"][8:10]}.{a["date"][5:7]}.{a["date"][:4]}</time>
        <span class="art-lang">{a["lang"]}</span>
        <span class="art-t">{e(a["title"])}</span>
        <span class="art-d">{T(f"art.{i}.dek", e(a["dek"]))}</span>
      </a></li>''' for i, a in enumerate(ARTICLES))
    domains = "".join(f'''
      <li class="dom"><span class="dom-n">{i+1:02d}</span><h3>{T(f"svc.{i}.t", s[0])}</h3><p>{T(f"svc.{i}.d", s[2])}</p><span class="dom-by">{s[4]}</span></li>''' for i, s in enumerate(SERVICES))
    n_part = sum(len(v) for v in PARTNERS.values())
    n_active = sum(1 for p in PROJECTS if p[4] == "active")
    feat_links = "".join(link(u, f"wl.wellsense.{i}", l) for i, (l, u) in enumerate(feat["links"]))
    body = f'''
<section class="hero">
  <canvas class="quake" aria-hidden="true"></canvas>
  <div class="wrap hero-in">
    <p class="hero-meta"><span>Est. 2020</span><span>Rorotan, Jakarta</span><span class="live"><i></i>{n_active} {T("hero.active", "proyek berjalan")}</span></p>
    <h1 class="display hero-h">Richterize<br>the Infinity.</h1>
    <p class="hero-p">{T("hero.p", "Workspace engineering dari Jakarta. Kami merancang sistem IoT, panel PLC, model AI, dan produk CNC, lalu menuliskan apa yang kami pelajari.")}</p>
    <div class="hero-cta">
      <a class="btn btn-solid" href="works.html">{T("hero.cta1", "Lihat karya")}</a>
      <a class="btn" href="contact.html">{T("hero.cta2", "Mulai proyek")}</a>
    </div>
  </div>
  <div class="hero-readout wrap" aria-hidden="true">
    <span>{T("hero.hint", "Klik bidang di atas untuk memicu gelombang")}</span>
    <span class="ro"><b class="ro-m">M 0.0</b> · <b class="ro-xy">x 0.00 · y 0.00</b></span>
  </div>
</section>

<section class="wrap stats">
  <div><b>2020</b><span>{T("stat.year", "tahun berdiri")}</span></div>
  <div><b>14</b><span>{T("stat.people", "kontributor aktif")}</span></div>
  <div><b>{len(PROJECTS)}</b><span>{T("stat.projects", "proyek tercatat")}</span></div>
  <div><b>{n_part}</b><span>{T("stat.partners", "mitra sekolah, kampus, perusahaan, instansi")}</span></div>
</section>

<section class="wrap sec">
  {sec_head("01", T("home.s1", "Karya unggulan"), link("works.html", "home.s1.more", "Semua studi kasus"))}
  <article class="feature">
    <div class="feature-media">{frame("wellsense-dashboard", "alt.ws.dash", "Dashboard Wellsense: aliran sensor, status zona, dan output LSTM")}</div>
    <div class="feature-body">
      <p class="eyebrow">{feat["code"]} · {wk(feat, "kicker")}</p>
      <h3 class="feature-h">{feat["title"]}</h3>
      <p>{wk(feat, "lede")}</p>
      <dl class="kpis">{"".join(f'<div><dt>{T(f"w.wellsense.m{i}.v", v)}</dt><dd>{T(f"w.wellsense.m{i}.l", l)}</dd></div>' for i, (v, l) in enumerate(feat["metrics"][:2]))}</dl>
      <div class="links">{feat_links}</div>
    </div>
  </article>
</section>

<section class="wrap sec">
  {sec_head("02", T("home.s2", "Indeks karya"), f'<span class="mute">{len(WORKS)} · {T("home.s2.hint", "arahkan kursor untuk pratinjau")}</span>')}
  <ul class="windex">{"".join(rows)}</ul>
  <img class="wi-preview" alt="" aria-hidden="true">
</section>

<section class="wrap sec">
  {sec_head("03", T("home.s3", "Domain kerja"), link("services.html", "home.s3.more", "Detail layanan"))}
  <ol class="doms">{domains}</ol>
</section>

<section class="wrap sec">
  {sec_head("04", T("home.s4", "Tulisan terbaru"), raw_link("https://medium.com/@ibnurorotan", "Medium"))}
  <ul class="arts">{arts}</ul>
</section>

<section class="wrap sec">
  {sec_head("05", T("home.s5", "Mitra"), link("about.html#mitra", "home.s5.more", "Daftar lengkap"))}
  <div class="partners-sum">
    {"".join(f'<div><b>{len(v)}</b><span>{T(f"pg.{i}", k)}</span></div>' for i, (k, v) in enumerate(PARTNERS.items()))}
  </div>
  <p class="partners-line">{" · ".join(e(x) for x in PARTNERS["Perusahaan"])}</p>
</section>
'''
    return layout("index.html", "home", "Beranda",
                  "NuRichter Workspace: IoT, elektrikal industri, AI/ML, manufaktur CNC, dan konten kreatif dari Jakarta. Lihat karya seperti Wellsense dan riset BST vs AVL.",
                  body, extra_head='<link rel="modulepreload" href="js/quake.js">',
                  scripts='<script type="module" src="js/quake.js"></script>')


def chart_html(w):
    out = [f'<figure class="bars"><figcaption>{T("chart.cap", "Waktu (ms), 5.000 pemain, input terurut. Batang lebih pendek lebih baik.")}</figcaption>']
    for i, (label, a, b, unit) in enumerate(w["chart"]):
        mx = max(a, b)
        fa = f"{a:g}"
        fb = f"{b:g}"
        out.append(f'''<div class="bar-g"><p>{T(f"chart.{i}", label)}</p>
<div class="bar"><span class="bar-k">BST</span><span class="bar-t"><i class="acc" style="--w:{a/mx*100:.2f}%"></i></span><span class="bar-v">{fa} {unit}</span></div>
<div class="bar"><span class="bar-k">AVL</span><span class="bar-t"><i style="--w:{max(b/mx*100, .6):.2f}%"></i></span><span class="bar-v">{fb} {unit}</span></div></div>''')
    out.append("</figure>")
    return "".join(out)


def work_links(w, col=False):
    return "".join(link(u, f'wl.{w["id"]}.{i}', l) for i, (l, u) in enumerate(w["links"]))


def page_works():
    chips = f'<button class="chip" aria-pressed="true" data-f="all">{T("ui.all", "Semua")}</button>' + "".join(
        f'<button class="chip" aria-pressed="false" data-f="{k}">{T("disc." + k, l)}</button>' for k, l in DISCIPLINES if any(k in w["disc"] for w in WORKS))
    arts = []
    for w in WORKS:
        m = WORK_MEDIA[w["id"]]
        gallery = ""
        if m.get("gallery"):
            items = []
            for j, g in enumerate(m["gallery"]):
                if g in SHOTS:
                    items.append(frame(g, "alt.ws.regime", "Wellsense: pengelompokan rezim operasi dengan K-Means"))
                else:
                    items.append(photo(g, f'alt.{w["id"]}.g{j}', f'{w["title"]}: foto pendukung', sizes="(max-width: 800px) 100vw, 30vw"))
            gallery = f'<div class="gal">{"".join(items)}</div>'
        if m.get("svg2"):
            gallery = f'<div class="gal"><figure class="drawing"><div class="drawing-in">{FIGS[m["svg2"]]()}</div><figcaption>Fig. {w["code"]}b · {T("ui.tracking", "prinsip pelacakan")}</figcaption></figure></div>'
        prob = f'<div class="cs-p"><h4>{T("cs.problem", "Masalah")}</h4><p>{wk(w, "problem")}</p></div>' if w["problem"] else ""
        appr = f'<div class="cs-p"><h4>{T("cs.approach", "Pendekatan")}</h4><p>{wk(w, "approach")}</p></div>' if w["approach"] else ""
        chart = chart_html(w) if w.get("chart") else ""
        links = work_links(w)
        arts.append(f'''
<article class="cs" id="{w["id"]}" data-disc="{" ".join(w["disc"])}">
  <aside class="cs-meta">
    <p class="cs-code">{w["code"]}</p>
    <dl>
      <div><dt>{T("cs.year", "Tahun")}</dt><dd>{w["year"]}</dd></div>
      <div><dt>{T("cs.status", "Status")}</dt><dd>{status(w["status"])}</dd></div>
      <div><dt>{T("cs.field", "Bidang")}</dt><dd>{", ".join(T("disc." + d, DISC[d]) for d in w["disc"])}</dd></div>
      <div><dt>{T("cs.tools", "Alat")}</dt><dd class="tags">{"".join(f"<span>{e(s)}</span>" for s in w["stack"])}</dd></div>
    </dl>
    {f'<div class="links col">{links}</div>' if links else ""}
  </aside>
  <div class="cs-body">
    <p class="eyebrow">{wk(w, "kicker")}</p>
    <h2 class="cs-h">{wk(w, "title")}</h2>
    <p class="cs-lede">{wk(w, "lede")}</p>
    {work_visual(w)}
    <div class="cs-cols">{prob}{appr}</div>
    {chart}
    {metrics_html(w)}
    {gallery}
  </div>
</article>''')
    toc = "".join(f'<li><a href="#{w["id"]}"><span>{w["code"]}</span>{wk(w, "title")}</a></li>' for w in WORKS)
    body = page_head("works", "Lembar W", "Karya", "Studi kasus dari NuRichter Workspace dan sub-brand-nya: riset AI untuk migas, publikasi struktur data, drone pertanian, trainer PLC, sampai produksi CNC. Angka yang ditampilkan berasal dari laporan dan tulisan masing-masing proyek.",
                     f'<div class="chips" role="group">{chips}</div>')
    body += f'''
<div class="wrap works-layout">
  <nav class="toc"><p class="toc-h">{T("ui.toc", "Isi")}</p><ol>{toc}</ol></nav>
  <div class="works">{"".join(arts)}<p class="empty" hidden>{T("ui.none", "Tidak ada karya di bidang ini.")}</p></div>
</div>'''
    return layout("works.html", "works", "Karya", "Portofolio NuRichter Workspace: Wellsense, BST vs AVL, AgriHex-SkyCure, Ragnarok PLC trainer, ArmX, Mulya Jaya, dan lainnya.", body)


def page_projects():
    counts = {k: sum(1 for p in PROJECTS if p[4] == k) for k in STATUS}
    chips = f'<button class="chip" aria-pressed="true" data-f="all">{T("ui.all", "Semua")} <span>{len(PROJECTS)}</span></button>' + "".join(
        f'<button class="chip" aria-pressed="false" data-f="{k}">{T("status." + k, v)} <span>{counts[k]}</span></button>' for k, v in STATUS.items())
    rows = []
    for i, (yr, title, field, desc, st, href) in enumerate(PROJECTS, 1):
        tt = T(f"p.{i}.t", e(title))
        t = f'<a href="{href}">{tt}</a>' if href else tt
        rows.append(f'<tr data-s="{st}"><td class="mono">P-{i:02d}</td><td class="mono">{T(f"p.{i}.y", yr) if not yr[0].isdigit() else yr}</td><td><b>{t}</b><span class="tdesc">{T(f"p.{i}.d", e(desc))}</span></td><td class="mute">{T(f"p.{i}.f", e(field))}</td><td>{status(st)}</td></tr>')
    body = page_head("archive", "Lembar A", "Arsip proyek", "Semua yang pernah dimulai, termasuk yang ditunda dan dihentikan. Proyek yang dihentikan tetap dicatat karena idenya sering diwariskan ke proyek berikutnya.",
                     f'''<div class="arch-tools"><div class="chips" role="group">{chips}</div>
<label class="search"><span class="sr">{T("ui.find", "Cari proyek")}</span><input type="search" class="arch-q" data-ta="placeholder:ui.find.ph" placeholder="{R("ui.find.ph", "Cari judul atau bidang…")}"></label></div>''')
    body += f'''
<div class="wrap">
  <div class="tbl-wrap"><table class="tbl arch">
    <thead><tr><th scope="col">{T("th.no", "No.")}</th><th scope="col">{T("cs.year", "Tahun")}</th><th scope="col">{T("th.project", "Proyek")}</th><th scope="col">{T("cs.field", "Bidang")}</th><th scope="col">{T("cs.status", "Status")}</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table></div>
  <p class="empty arch-empty" hidden>{T("ui.none2", "Tidak ada proyek yang cocok.")}</p>
</div>'''
    return layout("projects.html", "archive", "Arsip proyek", "Arsip lengkap proyek NuRichter Workspace: berjalan, selesai, ditunda, dihentikan, dan rencana.", body)


def brand_meta(b):
    return (f'{T("b.since", "Sejak")} {b["since"]} · {b["staff"]} {T("b.staff", "staf")} · '
            f'{T("b.head", "Kepala")}: {b["head"]}')


def page_products():
    cards = []
    for b in BRANDS:
        cards.append(f'''
<article class="brand-row">
  <a class="brand-media" href="{b["page"]}">{photo(BRAND_PHOTO[b["id"]], f'alt.b.{b["id"]}', b["name"], caption=False, sizes="(max-width:800px) 100vw, 40vw")}</a>
  <div class="brand-body">
    <p class="eyebrow">{brand_meta(b)}</p>
    <h2 class="cs-h"><span class="mark">{b["mark"]}</span>{b["name"]}</h2>
    <p class="mute">{T(f'b.{b["id"]}.role', b["role"])}</p>
    <p>{T(f'b.{b["id"]}.body', b["body"])}</p>
    <div class="links">{link(b["page"], "b.profile", "Profil")}{link("works.html#" + b["work"], "b.case", "Studi kasus")}</div>
  </div>
</article>''')
    body = page_head("brands", "Lembar B", "Sub-brand", "Tiga unit dengan keahlian berbeda, satu workspace. Mulya Jaya membuat barang fisik, RigRoom membuat sistem IoT, Ragnarok menangani kelistrikan industri.")
    body += f'<div class="wrap brands">{"".join(cards)}</div>'
    body += f'''
<section class="wrap sec">
  {sec_head("—", T("eco.h", "Bagaimana mereka terhubung"))}
  <div class="eco">
    <div class="eco-core">NuRichter<br>Workspace</div>
    <div class="eco-n"><b>Mulya Jaya</b><span>{T("eco.mj", "membuat casing, bracket, dan unit fisik")}</span></div>
    <div class="eco-n"><b>RigRoom</b><span>{T("eco.rr", "mengisi unit dengan sensor dan firmware")}</span></div>
    <div class="eco-n"><b>Ragnarok</b><span>{T("eco.rg", "menghubungkannya ke panel dan PLC industri")}</span></div>
    <div class="eco-n"><b>Labs</b><span>{T("eco.lb", "tempat semuanya dirakit dan diuji")}</span></div>
  </div>
</section>'''
    return layout("products.html", "brands", "Sub-brand", "Sub-brand NuRichter: Mulya Jaya (CNC), RigRoom (IoT), Ragnarok (elektrikal industri).", body)


def page_brand(b):
    bid = b["id"]
    log = "".join(f'<li><time>{T(f"b.{bid}.log{i}.d", d) if not d[0].isdigit() else d}</time><span>{T(f"b.{bid}.log{i}", t)}</span></li>' for i, (d, t) in enumerate(b["log"]))
    offer = "".join(f'<li>{T(f"b.{bid}.o{i}", o)}</li>' for i, o in enumerate(b["offer"]))
    w = work_by(b["work"])
    body = f'''
<section class="ph-head wrap">
  <div class="ph-meta"><span>{T("sheet.brand", "Lembar")} {b["mark"]}</span><span>NuRichter Workspace</span><span>Rev {SITE["rev"]}</span></div>
  <h1 class="display">{b["name"]}</h1>
  <p class="lede">{T(f"b.{bid}.body", b["body"])}</p>
  <p class="ph-sub mono">{T(f"b.{bid}.role", b["role"])} · {brand_meta(b)}</p>
</section>
<div class="wrap brand-detail">
  <div>{photo(BRAND_PHOTO[bid], f"alt.b.{bid}", b["name"], sizes="(max-width:800px) 100vw, 55vw")}</div>
  <div>
    <h2 class="h-sm">{T("b.journey", "Perjalanan")}</h2>
    <ol class="log">{log}</ol>
    <h2 class="h-sm">{T("b.offer", "Yang kami kerjakan")}</h2>
    <ul class="ticks">{offer}</ul>
    <div class="links"><a class="btn btn-solid" href="contact.html?need={e(b["cta"])}">{T(f"b.{bid}.cta", b["cta"])}</a></div>
  </div>
</div>
<section class="wrap sec">
  {sec_head("→", T("b.related", "Studi kasus terkait"))}
  <a class="rel" href="works.html#{w["id"]}">
    <span class="wi-code">{w["code"]}</span><span class="rel-t">{wk(w, "title")}</span><span class="mute">{wk(w, "lede")}</span>{ARROW}
  </a>
</section>'''
    return layout(b["page"], f"brand.{bid}", b["name"], f'{b["name"]}, sub-brand NuRichter Workspace: {b["role"]}.', body)


def page_archer():
    body = page_head("archer", "Lembar NRM-1", "NRM-1 “Archer”", "Platform peluncur bergerak berbasis remote control dengan telemetri IoT. Proyek ini masih dalam tahap rancangan di NuRichter Labs.",
                     f'<p class="ph-sub">{status("future")}</p>')
    body += f'''
<div class="wrap brand-detail">
  <figure class="drawing big"><div class="drawing-in">{FIGS["archer"]()}</div><figcaption>Fig. NRM-1 · {T("archer.fig", "sketsa konsep, bukan gambar produksi")}</figcaption></figure>
  <div>
    <h2 class="h-sm">{T("archer.scope", "Lingkup rancangan")}</h2>
    <ul class="ticks">
      <li>{T("archer.s0", "Sasis beroda atau rantai dengan kendali RC")}</li>
      <li>{T("archer.s1", "Telemetri IoT: posisi, kemiringan, status baterai")}</li>
      <li>{T("archer.s2", "Perakitan mekanik di NuRichter Labs")}</li>
      <li>{T("archer.s3", "Kendali embedded untuk sudut elevasi peluncur")}</li>
    </ul>
    <h2 class="h-sm">{T("archer.sib", "Proyek saudara")}</h2>
    <p>{T("archer.sib.p", "NFF-X “Axel”, pesawat RC fixed-wing dengan sasis hibrida darat, dirancang paralel dan berbagi sistem telemetri yang sama.")}</p>
    <div class="links">{link("lab.html", "archer.more", "Lihat proyek Labs lainnya")}</div>
  </div>
</div>'''
    return layout("nurichter-nrmarcher.html", "archer", "NRM-1 Archer", "NRM-1 Archer: platform peluncur RC dengan telemetri IoT dari NuRichter Labs.", body)


def page_services():
    items = []
    for i, (t, sub, desc, tags, by) in enumerate(SERVICES):
        items.append(f'''
<article class="svc">
  <span class="svc-n">{i+1:02d}</span>
  <div class="svc-h"><h2>{T(f"svc.{i}.t", t)}</h2><p class="mute">{T(f"svc.{i}.s", sub)}</p></div>
  <p class="svc-d">{T(f"svc.{i}.d", desc)}</p>
  <div class="svc-t"><span class="tags">{"".join(f'<span>{T(f"svc.{i}.tag{j}", x)}</span>' for j, x in enumerate(tags))}</span><span class="mono mute">{T("svc.by", "oleh")} {by}</span></div>
</article>''')
    proc = "".join(f'<li><span class="mono">{i+1:02d}</span><h3>{T(f"proc.{i}.t", t)}</h3><p>{T(f"proc.{i}.d", d)}</p></li>' for i, (t, d) in enumerate(PROCESS))
    body = page_head("services", "Lembar S", "Layanan", "Enam bidang yang kami kerjakan sendiri, dari sensor sampai produk jadi. Untuk pekerjaan fisik, produksi dilakukan bersama Workshop Mekatronika SMK Negeri 4 Jakarta.")
    body += f'<div class="wrap svcs">{"".join(items)}</div>'
    body += f'''
<section class="wrap sec">
  {sec_head("→", T("proc.h", "Cara kerja"))}
  <ol class="proc">{proc}</ol>
  <div class="links"><a class="btn btn-solid" href="contact.html">{T("proc.cta", "Ceritakan kebutuhan Anda")}</a></div>
</section>'''
    return layout("services.html", "services", "Layanan", "Layanan NuRichter Workspace: IoT, elektrikal industri, mekatronika, CNC & 3D print, AI/ML, dan konten kreatif.", body)


def page_lab():
    total = sum(m[0] for m in MACHINES)
    mrows = "".join(f'<tr><td class="mono qty">{q}×</td><td><b>{T(f"mc.{i}.n", n) if i == 5 else n}</b><span class="tdesc">{T(f"mc.{i}.d", d)}</span></td><td class="mute">{T(f"mc.{i}.c", c)}</td></tr>' for i, (q, n, d, c) in enumerate(MACHINES))
    caps = "".join(f'<li><h3>{T(f"cap.{i}.t", t)}</h3><p>{T(f"cap.{i}.d", d)}</p></li>' for i, (t, d) in enumerate(LAB_CAPS))
    lp = "".join(f'<li>{status(s)}<h3>{t}</h3><p class="mono mute">{f}</p><p>{T(f"lp.{i}", d)}</p></li>' for i, (s, t, f, d) in enumerate(LAB_PROJECTS))
    body = page_head("labs", "Lembar L", "NuRichter Labs", "Lab produksi kreatif kami berada di Workshop Mekatronika SMK Negeri 4 Jakarta. Kami juga menjadi mitra utama fasilitator Lembaga Sertifikasi Profesi (LSP) sekolah tersebut.")
    body += f'''
<div class="wrap lab-photos">
  {photo("cnc-router", "alt.lab.0", "Mesin CNC router meja", sizes="(max-width:800px) 100vw, 33vw")}
  {photo("printer-nozzle", "alt.lab.1", "Nozzle printer 3D saat mencetak", sizes="(max-width:800px) 100vw, 33vw")}
  {photo("soldering", "alt.lab.2", "Menyolder komponen elektronik", sizes="(max-width:800px) 100vw, 33vw")}
</div>
<section class="wrap sec">
  {sec_head("01", T("lab.s1", "Mesin"), f'<span class="mute">{total} {T("lab.units", "unit")}</span>')}
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">{T("th.qty", "Jml")}</th><th scope="col">{T("th.machine", "Mesin")}</th><th scope="col">{T("th.class", "Kelas")}</th></tr></thead><tbody>{mrows}</tbody></table></div>
</section>
<section class="wrap sec">
  {sec_head("02", T("lab.s2", "Kapabilitas"))}
  <ul class="grid4">{caps}</ul>
</section>
<section class="wrap sec">
  {sec_head("03", T("lab.s3", "Proyek di Labs"))}
  <ul class="grid4 lp">{lp}</ul>
</section>'''
    return layout("lab.html", "labs", "Labs", "NuRichter Labs di Workshop Mekatronika SMK Negeri 4 Jakarta: CNC 5-axis, 3D print, elektronika, dan lengan robot.", body)


def page_about():
    team = "".join(f'<li><span class="ini">{"".join(p[0] for p in n.split()[:2])}</span><b>{n}</b><span>{r}</span><span class="mute">{u}</span></li>' for n, r, u in TEAM)
    partners = "".join(f'<div class="pgroup"><h3>{T(f"pg.{i}", k)} <span>{len(v)}</span></h3><ul>{"".join(f"<li>{e(x)}</li>" for x in v)}</ul></div>' for i, (k, v) in enumerate(PARTNERS.items()))
    body = page_head("about", "Lembar T", "Tentang", "NuRichter dimulai sebagai kanal YouTube pada 2017, menjadi brand personal Ibnu Khoirul Anwar pada 2020, dan diresmikan sebagai workspace pada 2025. Hari ini ada 14 kontributor dan tiga sub-brand.")
    body += f'''
<div class="wrap about-top">
  {photo("jakarta", "alt.jakarta", "Langit sore Jakarta", sizes="(max-width:800px) 100vw, 50vw")}
  <div class="about-text">
    <p>{T("about.p1", "Kami menggabungkan pekerjaan yang biasanya terpisah: rekayasa elektrikal, IoT, AI, manufaktur, dan konten. Alasannya sederhana: proyek nyata jarang berhenti di satu disiplin. Drone pertanian butuh mekanik, firmware, dan model visi komputer sekaligus.")}</p>
    <p>{T("about.p2", "Sebagian besar kerja kami juga kembali ke pendidikan. Trainer PLC Ragnarok dipakai di SMK, Labs berada di SMK Negeri 4 Jakarta, dan buku Robotics Catalyst ditulis untuk siswa vokasi.")}</p>
    <div class="links">{link("history.html", "about.history", "Sejarah lengkap")}{link("https://www.linkedin.com/in/nurichter", "about.li", "LinkedIn pendiri")}</div>
  </div>
</div>
<section class="wrap sec">
  {sec_head("01", T("about.team", "Tim inti"), f'<span class="mute">14 · Labs 6 · Mulya Jaya 3 · RigRoom 3 · Ragnarok 2</span>')}
  <ul class="team">{team}</ul>
</section>
<section class="wrap sec" id="mitra">
  {sec_head("02", T("home.s5", "Mitra"), f'<span class="mute">{sum(len(v) for v in PARTNERS.values())}</span>')}
  <div class="partners">{partners}</div>
</section>'''
    return layout("about.html", "about", "Tentang", "Tentang NuRichter Workspace: tim, sejarah singkat, dan mitra di Jakarta dan Bekasi.", body)


def page_history():
    items = "".join(f'''
<li class="tl-i{" tl-future" if i == len(TIMELINE) - 1 else ""}">
  <time>{T(f"tl.{i}.d", d)}</time>
  <div class="tl-b"><p class="mono mute">{T(f"tl.{i}.c", c)}</p><h2>{T(f"tl.{i}.t", t)}</h2><p>{T(f"tl.{i}.x", x)}</p></div>
  {seismo(i * 1.7)}
</li>''' for i, (d, t, c, x) in enumerate(TIMELINE))
    body = page_head("history", "Lembar H", "Sejarah", "Dari kanal YouTube pada 2017 sampai riset AI pada 2026. Setiap baris di bawah adalah satu lonjakan di seismogram NuRichter.")
    body += f'<div class="wrap"><ol class="tl">{items}</ol></div>'
    return layout("history.html", "history", "Sejarah", "Sejarah NuRichter Workspace dari 2017 sampai sekarang.", body)


def page_contact():
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener"><b>{n}</b><span>{h}</span>{EXT}</a></li>' for n, u, h in SOCIAL)
    needs = ["Kolaborasi proyek", "Workshop & pelatihan", "Sistem IoT", "Konsultasi elektrikal", "Pesan produksi", "Konsultasi IoT", "Riset / AI", "Lainnya"]
    opts = "".join(f'<option value="{n}" data-t="need.{i}">{R(f"need.{i}", n)}</option>' for i, n in enumerate(needs))
    body = page_head("contact", "Lembar K", "Kontak", "Ceritakan masalahnya, bukan hanya solusinya. Pesan dari formulir di bawah dikirim lewat WhatsApp, jadi balasan biasanya datang di hari yang sama.")
    body += f'''
<div class="wrap contact">
  <form class="cform" novalidate>
    <div class="f"><label for="c-name">{T("f.name", "Nama")}</label><input id="c-name" name="name" required autocomplete="name"></div>
    <div class="f"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
    <div class="f"><label for="c-org">{T("f.org", "Instansi")} <span class="mute">{T("f.opt", "(opsional)")}</span></label><input id="c-org" name="org" autocomplete="organization"></div>
    <div class="f"><label for="c-need">{T("f.need", "Kebutuhan")}</label><select id="c-need" name="need">{opts}</select></div>
    <div class="f f-wide"><label for="c-msg">{T("f.msg", "Pesan")}</label><textarea id="c-msg" name="msg" rows="6" required data-ta="placeholder:f.msg.ph" placeholder="{R("f.msg.ph", "Apa yang ingin dibangun, kapan dibutuhkan, dan di mana lokasinya?")}"></textarea></div>
    <div class="f-wide cform-end"><button class="btn btn-solid" type="submit">{T("f.send", "Kirim lewat WhatsApp")}</button><p class="cform-note mute" role="status" aria-live="polite"></p></div>
  </form>
  <aside class="contact-side">
    <dl class="cinfo">
      <div><dt>WhatsApp</dt><dd><a href="https://wa.me/{SITE["wa"]}" target="_blank" rel="noopener">{SITE["wa_display"]}</a></dd></div>
      <div><dt>Email</dt><dd><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></dd></div>
      <div><dt>{T("c.emailpro", "Email profesional")}</dt><dd><a href="mailto:{SITE["email_pro"]}">{SITE["email_pro"]}</a></dd></div>
      <div><dt>{T("c.base", "Basis")}</dt><dd>Rorotan, Jakarta Utara</dd></div>
      <div><dt>Labs</dt><dd>Workshop Mekatronika SMK Negeri 4 Jakarta</dd></div>
    </dl>
    <ul class="soc-list">{soc}</ul>
  </aside>
</div>'''
    return layout("contact.html", "contact", "Kontak", "Hubungi NuRichter Workspace lewat WhatsApp atau email.", body)


def page_credits():
    rows = []
    for name, c in CREDITS.items():
        lic = "CC0" if c["license"] == "cc0" else f'CC {c["license"].upper()} {c["license_version"]}'
        rows.append(f'<tr><td><img src="{c["file"]}" alt="" width="96" height="64" loading="lazy" class="thumb"></td><td><b>{e(c["title"] or name)}</b><span class="tdesc"><a href="{e(c["source"])}" target="_blank" rel="noopener">{T("cr.src", "Sumber")}</a></span></td><td>{e(c["creator"] or "—")}</td><td><a href="{e(c["license_url"])}" target="_blank" rel="noopener">{lic}</a></td></tr>')
    body = page_head("credits", "Lembar C", "Kredit foto", "Foto ilustrasi di situs ini berlisensi Creative Commons dan diambil lewat Openverse dari Flickr. Foto dipakai tanpa perubahan selain ukuran dan format. Tangkapan layar Wellsense diambil dari demo publiknya.")
    body += f'<div class="wrap"><div class="tbl-wrap"><table class="tbl credits"><thead><tr><th scope="col">{T("ui.photo", "Foto")}</th><th scope="col">{T("cr.title", "Judul")}</th><th scope="col">{T("cr.by", "Pembuat")}</th><th scope="col">{T("cr.lic", "Lisensi")}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></div>'
    return layout("credits.html", "credits", "Kredit foto", "Atribusi foto Creative Commons yang dipakai di situs NuRichter Workspace.", body)


def page_catalog():
    body = page_head("catalog", "Lembar ∞", "Katalog", "Katalog sudah dipecah menjadi dua halaman: karya untuk studi kasus, arsip untuk semua proyek.",
                     f'<div class="links">{link("works.html", "nav.works", "Karya")}{link("projects.html", "nav.archive", "Arsip")}{link("products.html", "nav.brands", "Sub-brand")}</div>')
    return layout("catalog.html", "catalog", "Katalog", "Katalog NuRichter Workspace.", body)


def page_404():
    body = page_head("404", "Lembar 404", "Halaman tidak ditemukan", "Mungkin tautannya sudah pindah. Coba pencarian dengan Ctrl K, atau kembali ke beranda.",
                     f'<div class="links">{link("index.html", "nav.home", "Beranda")}{link("works.html", "nav.works", "Karya")}</div>')
    return layout("404.html", "404", "404", "Halaman tidak ditemukan.", body)


# ------------------------------------------------------------------ indeks, sitemap, i18n

def search_index():
    idx = [{"t": "Beranda", "tk": "nav.home", "u": "index.html", "k": "page"}]
    idx += [{"t": l, "tk": k, "u": h, "k": "page"} for h, k, l in NAV]
    idx += [{"t": l, "tk": k, "u": h, "k": "page"} for h, k, l in EXTRA_NAV[1:]]
    idx += [{"t": w["title"], "tk": f'w.{w["id"]}.title', "u": f'works.html#{w["id"]}', "k": "work", "d": w["kicker"], "dk": f'w.{w["id"]}.kicker'} for w in WORKS]
    idx += [{"t": b["name"], "u": b["page"], "k": "brand", "d": b["role"], "dk": f'b.{b["id"]}.role'} for b in BRANDS]
    idx += [{"t": p[1], "tk": f"p.{i}.t", "u": p[5] or "projects.html", "k": "project", "d": p[2], "dk": f"p.{i}.f"} for i, p in enumerate(PROJECTS, 1)]
    idx += [{"t": a["title"], "u": a["url"], "k": "article", "d": a["date"]} for a in ARTICLES]
    idx += [{"t": n, "u": u, "k": "profile", "d": h} for n, u, h in SOCIAL]
    return "window.NR_INDEX=" + json.dumps(idx, ensure_ascii=False) + ";\n"


JS_STRINGS = {
    "js.kind.page": "Halaman", "js.kind.work": "Karya", "js.kind.brand": "Sub-brand", "js.kind.project": "Proyek",
    "js.kind.article": "Tulisan", "js.kind.profile": "Profil",
    "js.noresults": "Tidak ada hasil untuk",
    "js.form.err": "Lengkapi nama, email yang valid, dan pesan.",
    "js.form.ok": "WhatsApp dibuka di tab baru. Kalau tidak muncul, cek pemblokir pop-up.",
    "js.form.hello": "Halo NuRichter Workspace,", "js.form.name": "Nama", "js.form.org": "Instansi", "js.form.need": "Kebutuhan",
    "js.translating": "Menerjemahkan di perangkat…",
}


def sitemap(pages):
    today = date.today().isoformat()
    urls = "".join(
        f'  <url><loc>{SITE["url"]}/{"" if p == "index.html" else p.replace(".html", "")}</loc><lastmod>{today}</lastmod></url>\n'
        for p in pages if p not in ("404.html", "catalog.html"))
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'


def write_i18n():
    out = os.path.join(ROOT, "i18n")
    os.makedirs(out, exist_ok=True)
    K.update(JS_STRINGS)
    with open(os.path.join(out, "id.json"), "w", encoding="utf-8") as f:
        json.dump(K, f, ensure_ascii=False, indent=0, sort_keys=True)
    src = os.path.join(HERE, "i18n")
    report = []
    for code, *_ in LANGS:
        if code == "id":
            continue
        p = os.path.join(src, f"{code}.json")
        if not os.path.exists(p):
            report.append(f"{code}: BELUM ADA")
            continue
        d = json.load(open(p, encoding="utf-8"))
        unknown = [k for k in d if k not in K]
        d = {k: v for k, v in d.items() if k in K}
        with open(os.path.join(out, f"{code}.json"), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
        report.append(f"{code}: {len(d)}/{len(K)}" + (f" (kunci tak dikenal: {len(unknown)} {unknown[:3]})" if unknown else ""))
    print("Kunci sumber:", len(K))
    print("  ".join(report))


def main():
    pages = {
        "index.html": page_index,
        "works.html": page_works,
        "projects.html": page_projects,
        "products.html": page_products,
        **{b["page"]: (lambda b=b: page_brand(b)) for b in BRANDS},
        "nurichter-nrmarcher.html": page_archer,
        "services.html": page_services,
        "lab.html": page_lab,
        "about.html": page_about,
        "history.html": page_history,
        "contact.html": page_contact,
        "credits.html": page_credits,
        "catalog.html": page_catalog,
        "404.html": page_404,
    }
    for i, p in enumerate(pages, 1):
        SHEETS[p] = (f"{i:02d}", p)
    for p, fn in pages.items():
        with open(os.path.join(ROOT, p), "w", encoding="utf-8") as f:
            f.write(fn())
    with open(os.path.join(ROOT, "js", "search-index.js"), "w", encoding="utf-8") as f:
        f.write(search_index())
    with open(os.path.join(ROOT, "js", "langs.js"), "w", encoding="utf-8") as f:
        f.write("window.NR_LANGS=" + json.dumps([{"c": c, "n": n, "en": en, "dir": d, "font": fo} for c, n, en, d, fo in LANGS], ensure_ascii=False) + ";\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap(pages))
    write_i18n()
    print(f"{len(pages)} halaman ditulis.")


if __name__ == "__main__":
    main()
