# NuRichter Workspace

Situs resmi NuRichter Workspace — *Richterize The Infinity*.
Statis (HTML + CSS + JS tanpa framework), siap di-deploy ke Vercel tanpa build step.

## Struktur

```
index.html, works.html, ...   halaman hasil generate (jangan diedit langsung)
css/style.css                 seluruh gaya (tema terang/gelap, RTL)
js/main.js                    interaksi: tema, menu, palet Ctrl K, filter, formulir
js/i18n.js                    mesin terjemahan 30 bahasa
js/quake.js                   hero 3D (Three.js) — bidang seismik interaktif
js/vendor/three.module.min.js Three.js r170 (MIT), disimpan lokal
i18n/*.json                   kamus bahasa (id.json dibuat otomatis)
img/                          foto (WebP) + og.png
_build/                       generator (tidak ikut deploy, lihat .vercelignore)
```

## Mengubah konten

Semua teks ada di `_build/data.py` (karya, proyek, tim, sejarah, layanan, mitra).
Setelah mengedit, jalankan:

```bash
python3 _build/build.py
```

Butuh Python 3.9+ saja, tanpa paket tambahan. Script menulis ulang semua `.html`,
`sitemap.xml`, `js/search-index.js`, `js/langs.js`, dan `i18n/*.json`,
lalu melaporkan cakupan terjemahan tiap bahasa.

## Terjemahan

- Bahasa Indonesia (sumber) dan Inggris diterjemahkan penuh.
- 28 bahasa lain: antarmuka, judul, ringkasan halaman, dan ringkasan karya diterjemahkan
  manual di `_build/i18n/<kode>.json`. Paragraf panjang memakai bahasa Inggris, dan
  diterjemahkan di perangkat lewat Translator API bila browser mendukung (Chrome 138+).
- Teks baru di `data.py` otomatis mendapat kunci; tambahkan terjemahannya di file JSON
  bahasa terkait dengan kunci yang sama (lihat `i18n/id.json` untuk daftar kunci).
- Bahasa dipilih otomatis dari browser pada kunjungan pertama, atau lewat tombol 🌐 / `?lang=xx`.

## Foto

Foto ilustrasi berlisensi Creative Commons dari Flickr (via Openverse); atribusi lengkap
ada di halaman `credits.html` dan `_build/credits.json`. Ganti dengan foto asli NuRichter
kapan pun: simpan sebagai WebP di `img/` dengan nama yang sama.

## Jalankan lokal

```bash
python3 -m http.server 8000
# buka http://localhost:8000
```
