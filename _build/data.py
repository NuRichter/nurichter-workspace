"""Konten situs NuRichter Workspace. Edit di sini, lalu jalankan: python3 _build/build.py"""

SITE = {
    "url": "https://nurichter-workspace.vercel.app",
    "name": "NuRichter Workspace",
    "tagline": "Richterize The Infinity",
    "founder": "Ibnu Khoirul Anwar",
    "wa": "6281280717345",
    "wa_display": "0812 8071 7345",
    "email": "ibnurorotan@gmail.com",
    "email_pro": "ibnu@nurichterworkspace.com",
    "rev": "2026.10",
}

SOCIAL = [
    ("LinkedIn", "https://www.linkedin.com/in/nurichter", "in/nurichter"),
    ("GitHub", "https://github.com/NuRichter", "NuRichter"),
    ("Medium", "https://medium.com/@ibnurorotan", "@ibnurorotan"),
    ("YouTube", "https://www.youtube.com/@NuRichter", "@NuRichter"),
    ("Last Z", "https://www.youtube.com/@lastz3040", "@lastz3040"),
    ("Instagram", "https://www.instagram.com/ibnu_lpg/", "@ibnu_lpg"),
]

# ---------------------------------------------------------------- KARYA (case studies)
# fig = nama gambar teknik di figures.py ; disc = disiplin untuk filter
WORKS = [
    {
        "id": "wellsense",
        "code": "W-01",
        "title": "Wellsense",
        "kicker": "IOC Digital Hackathon AI/ML Hulu Migas 2026",
        "year": "2026",
        "disc": ["ai"],
        "status": "active",
        "fig": "wellsense",
        "lede": "Prototipe deteksi dini anomali sumur minyak lepas pantai. Dibangun lima mahasiswa untuk hackathon SKK Migas, lengkap dengan simulasi yang bisa dicoba langsung di browser.",
        "problem": "Data sensor sumur offshore berantakan: dalam satu kajian, 31,17% dari 15.872 variabel sensor di 21 sumur hilang atau rusak. Anomali yang telat terbaca berarti produksi yang hilang setiap jam.",
        "approach": "Arsitektur lima lapis. Sepuluh aliran sensor masuk, dibersihkan dan diseimbangkan dengan SMOTE adaptif, lalu dibaca dua jalur model: Isolation Forest dan LSTM dua lapis untuk peluang LPO per tick, K-Means untuk mengelompokkan rezim operasi harian. Setiap intervensi tetap harus disetujui manusia lewat RBAC tiga tingkat, dan tiket intervensi dicetak otomatis sebagai PDF untuk tanda tangan basah.",
        "metrics": [
            ("Rp73,5 jt", "potensi kerugian per jam pada sumur gas-lift 1.500 BOPD"),
            ("31,17%", "variabel sensor hilang/rusak dari 15.872"),
            ("±US$69 rb", "estimasi biaya software per implementasi"),
            ("5 lapis", "ingestion → ETL → dual-track ML → HITL → dashboard"),
        ],
        "stack": ["Isolation Forest", "LSTM", "K-Means++", "SMOTE", "Chart.js", "jsPDF", "ES Modules"],
        "links": [
            ("Coba simulasi", "https://wellsense-sim.vercel.app"),
            ("Kode sumber", "https://github.com/NuRichter/wellsense-sim"),
            ("Baca tulisan", "https://medium.com/@ibnurorotan/rp73-juta-hilang-setiap-jam-kita-terlambat-membaca-sumur-8f5eaed89e54"),
        ],
    },
    {
        "id": "bst-avl",
        "code": "W-02",
        "title": "BST vs AVL di bawah tekanan",
        "kicker": "Publikasi · Jurnal Teknologi dan Open Source, 2026",
        "year": "2026",
        "disc": ["research"],
        "status": "finished",
        "fig": "bstavl",
        "lede": "Uji stres leaderboard C++: Binary Search Tree biasa melawan AVL Tree. Dengan data acak BST menang. Dengan skor yang sudah terurut, BST runtuh jadi linked list.",
        "problem": "Leaderboard game sering menerima skor yang hampir terurut. Struktur data yang terlihat cepat di benchmark acak bisa berubah perilaku total di data nyata.",
        "approach": "Implementasi BST dan AVL di C++, diuji dengan ukuran 100 sampai 5.000 pemain, input acak dan terurut, diukur waktu build, tinggi pohon, dan 1.000 pencarian. Semua pengujian di satu laptop, dan batasan itu ditulis terang-terangan di paper.",
        "metrics": [
            ("32×", "lebih lambat: BST 1,1 s vs AVL 35 ms (5.000 pemain, input terurut)"),
            ("4.999 / 12", "tinggi pohon BST vs AVL"),
            ("234,56 / 8,92 ms", "1.000 pencarian, BST vs AVL"),
            ("30–45%", "BST lebih cepat membangun pohon pada data acak"),
        ],
        "chart": [
            ("Build, input terurut", 1100, 35, "ms"),
            ("1.000 pencarian", 234.56, 8.92, "ms"),
        ],
        "stack": ["C++", "AVL Tree", "Benchmarking", "Complexity analysis"],
        "links": [
            ("Baca tulisan", "https://medium.com/@ibnurorotan/we-fed-sorted-scores-to-a-binary-search-tree-it-got-32-slower-2c2dd502ea11"),
        ],
    },
    {
        "id": "gif-pdf",
        "code": "W-03",
        "title": "Animasi yang berjalan di dalam PDF",
        "kicker": "Eksperimen tooling · Claude Code",
        "year": "2026",
        "disc": ["research", "creative"],
        "status": "finished",
        "fig": "gifpdf",
        "lede": "Animasi automata langkah demi langkah yang benar-benar bergerak di dalam PDF, dan sebagai GIF di dokumen Word. Diuji di lab Windows, bukan diasumsikan.",
        "problem": "Materi kuliah automata lebih mudah dipahami kalau setiap transisi terlihat bergerak. Masalahnya, sebagian besar viewer PDF tidak memutar animasi, dan viewer bawaan Chrome adalah salah satunya.",
        "approach": "Riset dulu, baru build. Prediksinya Chrome akan gagal, dan uji di lab Windows membenarkannya. Pemicu JavaScript di level halaman memperbaiki Chrome; Firefox 157, PDF.js 6.3, dan Edge ikut memutar animasi. Font tertanam yang dobel dibuang tanpa mengubah satu piksel pun.",
        "metrics": [
            ("34 → 10,7 MB", "ukuran PDF setelah deduplikasi font, output identik piksel"),
            ("4 viewer", "Chrome, Edge, Firefox 157, PDF.js 6.3 lolos uji"),
            ("−69%", "pengurangan ukuran berkas"),
        ],
        "stack": ["PDF JavaScript", "GIF", "Word", "Claude Code", "Cross-viewer testing"],
        "links": [
            ("Baca tulisan", "https://medium.com/@ibnurorotan/i-asked-claude-to-make-a-gif-play-inside-a-pdf-first-it-predicted-chrome-would-fail-2b6600a9692e"),
        ],
    },
    {
        "id": "agrihex",
        "code": "W-04",
        "title": "AgriHex-SkyCure",
        "kicker": "PKM & PIMNAS 2026",
        "year": "2026",
        "disc": ["robotics", "ai", "iot"],
        "status": "active",
        "fig": "hexarotor",
        "lede": "Drone hexarotor untuk mendeteksi dan menyemprot penyakit tanaman bawang merah di Nganjuk, Jawa Timur.",
        "problem": "Penyakit bawang merah menyebar cepat dan biasanya baru terlihat saat sudah meluas. Penyemprotan merata membuang pestisida di area yang sehat.",
        "approach": "Kamera kedalaman Intel RealSense D435i dan komputer edge Jetson Orin/Nano membaca kondisi tanaman di udara. ArduPilot mengatur penerbangan, sementara data dikirim ke cloud Cyber-Physical System berbasis FastAPI. Konsepnya mewarisi proyek Mecha FlyBot milik RigRoom.",
        "metrics": [
            ("6 rotor", "hexarotor untuk redundansi dan muatan semprot"),
            ("Edge + cloud", "inferensi di Jetson, agregasi di CI-CPS"),
        ],
        "stack": ["Jetson Orin/Nano", "RealSense D435i", "ArduPilot", "FastAPI", "Computer Vision"],
        "links": [],
    },
    {
        "id": "sperm-quant",
        "code": "W-05",
        "title": "Sperm Quant",
        "kicker": "Computer-Assisted Sperm Analysis",
        "year": "2026",
        "disc": ["ai", "research"],
        "status": "active",
        "fig": "casa",
        "lede": "Sistem CASA berbasis image processing dan machine learning, kolaborasi riset dengan Dr. I Gede Susrama Mas Diyasa, ST., MT., IPU.",
        "problem": "Analisis motilitas sperma secara manual lambat dan hasilnya bergantung pada siapa yang menghitung.",
        "approach": "Melacak setiap sel di rekaman mikroskop, membangun lintasannya frame demi frame, lalu mengklasifikasikan pola gerak dengan model ML.",
        "metrics": [
            ("Riset aktif", "kolaborasi akademik"),
        ],
        "stack": ["Computer Vision", "Object tracking", "Python ML"],
        "links": [],
    },
    {
        "id": "ragnarok-trainer",
        "code": "W-06",
        "title": "Ragnarok Trainer Series",
        "kicker": "Trainer PLC untuk pendidikan vokasi",
        "year": "2023–2024",
        "disc": ["electrical"],
        "status": "finished",
        "fig": "plc",
        "lede": "Empat unit latih sistem kendali industri untuk SMK dan politeknik: tiga merek PLC dan satu rekonstruksi miniatur industri.",
        "problem": "Siswa vokasi butuh perangkat yang sama dengan yang mereka temui di pabrik, bukan simulasi di layar.",
        "approach": "Trainer Mitsubishi untuk pneumatik; Siemens S7-1200 dengan fitur diagnostik dan HMI sederhana; Schneider dengan sistem dua aktuator pneumatik dan hidrolik; serta rebuild unit Yalong YL-1B dengan wiring baru, umpan balik sensor, dan dokumentasi teknis ulang.",
        "metrics": [
            ("3 merek PLC", "Mitsubishi · Siemens S7-1200 · Schneider"),
            ("4 unit", "selesai dan dipakai untuk pelatihan"),
        ],
        "stack": ["Siemens S7-1200", "Mitsubishi PLC", "Schneider PLC", "HMI", "Pneumatics", "Hydraulics"],
        "links": [("Sub-brand Ragnarok", "nurichter-ragnarok.html")],
    },
    {
        "id": "armx",
        "code": "W-07",
        "title": "ArmX V1 & ArmX Pro V1",
        "kicker": "RigRoom · Robotika",
        "year": "2024",
        "disc": ["robotics", "iot"],
        "status": "finished",
        "fig": "arm",
        "lede": "Lengan robot rakitan sendiri berpenggerak servo. V1 membuktikan konsep, Pro V1 menaikkan muatan, presisi, dan menambah umpan balik sensor.",
        "problem": "Lengan robot industri terlalu mahal untuk dipakai belajar dan bereksperimen di skala lab kecil.",
        "approach": "Dua iterasi dalam satu tahun. Hasilnya dipakai bersama Smart Room Monitor & Control, sistem IoT RigRoom yang membaca sensor lingkungan dan mengendalikan relay lewat dashboard MQTT.",
        "metrics": [
            ("2 iterasi", "V1 → Pro V1 dalam 2024"),
            ("7 unit", "lengan robot di NuRichter Labs"),
        ],
        "stack": ["Servo", "Arduino / ESP32", "MQTT", "Sensor feedback"],
        "links": [("Sub-brand RigRoom", "nurichter-rigroom.html")],
    },
    {
        "id": "mulya-jaya",
        "code": "W-08",
        "title": "Plakat, medali & piala akrilik",
        "kicker": "Mulya Jaya · Manufaktur CNC",
        "year": "2022–2025",
        "disc": ["manufacturing"],
        "status": "finished",
        "fig": "cnc",
        "lede": "Lini produksi CNC dan 3D print untuk sekolah, perusahaan, dan acara resmi. Dimulai dari satu pesanan plakat pada 2022.",
        "problem": "Institusi butuh plakat dan piala custom dalam jumlah banyak, dengan tenggat dekat dan finishing yang rapi.",
        "approach": "CNC milling akrilik untuk bentuk dan gravir, lalu 3D print FDM masuk ke alur kerja pada 2024. Setiap tahun lini produk diperluas dengan toleransi yang lebih ketat dan pilihan material baru.",
        "metrics": [
            ("57", "desain baru 2023–2025 (10 + 26 + 21)"),
            ("50+", "varian produk aktif"),
        ],
        "stack": ["CNC milling", "Acrylic", "FDM 3D print", "CAD/CAM"],
        "links": [("Sub-brand Mulya Jaya", "nurichter-mulya-jaya.html")],
    },
    {
        "id": "seratus-ilmu",
        "code": "W-09",
        "title": "Seratus Ilmu",
        "kicker": "Website rebuild · PT Karya Nusatama Indonesia",
        "year": "2025",
        "disc": ["web"],
        "status": "finished",
        "fig": "web",
        "lede": "Pembangunan ulang situs platform pelatihan Seratus Ilmu, sekaligus kontribusi pada modul pelatihannya.",
        "problem": "Situs lama tidak nyaman dipakai di ponsel, padahal sebagian besar peserta pelatihan datang dari sana.",
        "approach": "UI/UX dimodernisasi dengan prioritas mobile. Proyek ini menjadi kemitraan strategis pertama NuRichter di dunia pelatihan profesional.",
        "metrics": [
            ("Mobile-first", "layout ulang seluruh halaman"),
        ],
        "stack": ["HTML/CSS", "JavaScript", "UI/UX"],
        "links": [],
    },
    {
        "id": "catalyst",
        "code": "W-10",
        "title": "Seri buku Catalyst",
        "kicker": "Penulisan teknis",
        "year": "2026",
        "disc": ["writing"],
        "status": "active",
        "fig": "books",
        "lede": "Human Catalyst tentang peran manusia dalam perubahan teknologi, dan Robotics Catalyst Part One sebagai buku referensi robotika untuk siswa SMK dan politeknik.",
        "problem": "Buku robotika berbahasa Indonesia yang berangkat dari dasar mekatronika sampai otomasi modern masih jarang.",
        "approach": "Part One membahas dasar mekatronik hingga otomasi. Part Two direncanakan untuk navigasi otonom, swarm robotics, dan industri 4.0.",
        "metrics": [
            ("2 judul", "sedang ditulis"),
            ("1 judul", "berikutnya: Robotics Catalyst Part Two"),
        ],
        "stack": ["Robotics", "Mechatronics", "Philosophy of technology"],
        "links": [],
    },
    {
        "id": "audio",
        "code": "W-11",
        "title": "Last Z & mixtape rawstyle",
        "kicker": "Musik hardstyle",
        "year": "2023–sekarang",
        "disc": ["creative"],
        "status": "active",
        "fig": "wave",
        "lede": "Kanal Last Z bersama Eurekanion untuk Hardstyle, Hardcore, dan Uptempo, setelah dua mixtape rawstyle: Death Impact 001 di YouTube dan Relentless di SoundCloud.",
        "problem": "",
        "approach": "",
        "metrics": [
            ("2", "mixtape rawstyle dirilis (2023)"),
        ],
        "stack": ["Mixing", "YouTube", "SoundCloud"],
        "links": [("Kanal Last Z", "https://www.youtube.com/@lastz3040")],
    },
]

DISCIPLINES = [
    ("ai", "AI / ML"),
    ("research", "Riset & publikasi"),
    ("robotics", "Robotika"),
    ("iot", "IoT"),
    ("electrical", "Elektrikal"),
    ("manufacturing", "Manufaktur"),
    ("web", "Web"),
    ("writing", "Penulisan"),
    ("creative", "Kreatif"),
]

# ---------------------------------------------------------------- TULISAN (Medium)
ARTICLES = [
    {
        "date": "2026-10-19",
        "title": "Rp73 Juta Hilang Setiap Jam Kita Terlambat Membaca Sumur",
        "dek": "Wellsense, prototipe AI deteksi dini anomali sumur minyak untuk IOC Digital Hackathon 2026.",
        "url": "https://medium.com/@ibnurorotan/rp73-juta-hilang-setiap-jam-kita-terlambat-membaca-sumur-8f5eaed89e54",
        "lang": "ID",
    },
    {
        "date": "2026-10-16",
        "title": "I Asked Claude to Make a GIF Play Inside a PDF. First, It Predicted Chrome Would Fail.",
        "dek": "Animasi automata di PDF, diuji di lab Windows. Ukuran berkas turun dari 34 MB ke 10,7 MB.",
        "url": "https://medium.com/@ibnurorotan/i-asked-claude-to-make-a-gif-play-inside-a-pdf-first-it-predicted-chrome-would-fail-2b6600a9692e",
        "lang": "EN",
    },
    {
        "date": "2026-10-15",
        "title": "We Fed Sorted Scores to a Binary Search Tree. It Got 32× Slower.",
        "dek": "Uji stres leaderboard C++ yang terbit di Jurnal Teknologi dan Open Source.",
        "url": "https://medium.com/@ibnurorotan/we-fed-sorted-scores-to-a-binary-search-tree-it-got-32-slower-2c2dd502ea11",
        "lang": "EN",
    },
]

# ---------------------------------------------------------------- ARSIP PROYEK
# status: active | finished | temporal | abandoned | future
PROJECTS = [
    ("2026", "PKM & PIMNAS 2026 — AgriHex-SkyCure", "Drone pertanian · IoT · CV", "Hexarotor deteksi & penyemprotan penyakit bawang merah di Nganjuk. Jetson Orin/Nano, RealSense D435i, ArduPilot, CI-CPS + FastAPI.", "active", "works.html#agrihex"),
    ("2026", "Hackathon IOC SKK Migas — Wellsense", "AI/ML · Migas", "Monitoring produksi offshore. Sensor ingestion → ETL/SMOTE → dual-track ML → HITL → dashboard.", "active", "works.html#wellsense"),
    ("2026", "Sperm Quant — CASA", "Biomedis · CV", "Computer-Assisted Sperm Analysis bersama Dr. I Gede Susrama Mas Diyasa.", "active", "works.html#sperm-quant"),
    ("2026", "Paper — BST vs AVL Leaderboard", "Riset · Struktur data", "Terbit di Jurnal Teknologi dan Open Source. BST 32× lebih lambat pada input terurut.", "finished", "works.html#bst-avl"),
    ("2026", "Animasi automata di PDF", "Tooling · Dokumen", "Animasi bergerak di PDF lintas viewer; 34 MB → 10,7 MB.", "finished", "works.html#gif-pdf"),
    ("2026", "Buku — Human Catalyst", "Penulisan · Filsafat teknologi", "Manusia sebagai katalis perubahan teknologi dan sosial.", "active", "works.html#catalyst"),
    ("2026", "Buku — Robotics Catalyst Part One", "Penulisan · Robotika", "Dasar mekatronik hingga otomasi modern untuk SMK/politeknik.", "active", "works.html#catalyst"),
    ("2025–", "Last Z Hardstyle Mix", "Musik · YouTube", "Bersama Eurekanion. Hardstyle, Hardcore, Uptempo.", "active", "works.html#audio"),
    ("2025–", "NuRichter YouTube Channel", "Konten · Teknik & gaming", "Gameplay, walkthrough, dan konten teknis.", "active", ""),
    ("2025–", "Scaramouche Genshin Impact Fanpage", "Facebook · Visual storytelling", "Visual novel berbasis gambar. Alter: Richter Scara.", "active", ""),
    ("2025", "Seratus Ilmu — Website Rebuild", "Web · Platform pelatihan", "Modernisasi UI/UX dan optimasi mobile untuk PT Karya Nusatama Indonesia.", "finished", "works.html#seratus-ilmu"),
    ("2025", "Mulya Jaya — Edisi 2025", "CNC · 3D print", "21 desain baru, finishing dan toleransi lebih ketat.", "finished", "works.html#mulya-jaya"),
    ("2024", "Mulya Jaya — Edisi 2024 + 3D Print", "CNC · 3D print", "26 desain baru dan lini 3D print pertama.", "finished", "works.html#mulya-jaya"),
    ("2024", "Ragnarok — Yalong Rebuild", "Otomasi industri · Edukasi", "Rewiring, sensor feedback, dokumentasi ulang unit Yalong YL-1B.", "finished", "works.html#ragnarok-trainer"),
    ("2024", "RigRoom — ArmX V1", "Robotika · Lengan robot", "Lengan robot servo rakitan sendiri, proof-of-concept.", "finished", "works.html#armx"),
    ("2024", "RigRoom — ArmX Pro V1", "Robotika · Lengan industri", "Muatan dan presisi naik, sensor feedback terintegrasi.", "finished", "works.html#armx"),
    ("2023–24", "Ragnarok — Mitsubishi PLC Trainer", "Elektrikal · Edukasi", "Trainer pneumatik, produk pertama lini Ragnarok.", "finished", "works.html#ragnarok-trainer"),
    ("2023–24", "Ragnarok — Siemens PLC Trainer", "Elektrikal · Edukasi", "S7-1200 pneumatik dengan diagnostik dan HMI.", "finished", "works.html#ragnarok-trainer"),
    ("2023–24", "Ragnarok — Schneider PLC Trainer", "Elektrikal · Edukasi", "Pneumatik & hidrolik, demonstrasi dua aktuator.", "finished", "works.html#ragnarok-trainer"),
    ("2023–24", "RigRoom — Smart Room Monitor & Control", "IoT · Smart building", "Sensor lingkungan, relay otomatis, dashboard MQTT.", "finished", "works.html#armx"),
    ("2023", "Mulya Jaya — Akrilik 2023", "CNC · Produksi kreatif", "10 desain baru plakat, medali, dan piala.", "finished", "works.html#mulya-jaya"),
    ("2023", "Death Impact Rawstyle Mixtape 001", "Musik · YouTube", "Mixtape rawstyle perdana NuRichter.", "finished", "works.html#audio"),
    ("2023", "Relentless Rawstyle Mixtape", "Musik · SoundCloud", "Mixtape rawstyle kedua.", "finished", "works.html#audio"),
    ("2022", "Mulya Jaya — Pesanan Plakat", "CNC", "Pesanan pertama; awal kapabilitas CNC NuRichter.", "finished", "works.html#mulya-jaya"),
    ("—", "Genshin Impact Mabar with Ray", "Komunitas gaming", "Ditunda; fokus ke proyek teknis.", "temporal", ""),
    ("—", "Earth Sky Space — Euphoric Hardstyle", "Musik", "Ditunda untuk Last Z.", "temporal", ""),
    ("—", "DDD — Dual Damage December", "Musik", "Ditinggalkan; arah kreatif pindah ke Last Z.", "abandoned", ""),
    ("—", "NNN — Noisecontrollers Nustyle November", "Musik", "Ditinggalkan menyusul DDD.", "abandoned", ""),
    ("—", "RigRoom — Mecha FlyBot", "IoT · Drone", "Quadcopter modular; konsepnya diwariskan ke AgriHex-SkyCure.", "abandoned", ""),
    ("Segera", "NRM-1 “Archer”", "IoT · RC · Robotika", "Peluncur bergerak RC dengan telemetri IoT.", "future", "nurichter-nrmarcher.html"),
    ("Segera", "NFF-X “Axel”", "IoT · RC · Desain mekanik", "Pesawat RC fixed-wing dengan sasis hibrida darat.", "future", ""),
    ("Segera", "Buku — Robotics Catalyst Part Two", "Penulisan · Robotika lanjut", "Navigasi otonom, swarm robotics, industri 4.0.", "future", "works.html#catalyst"),
    ("Segera", "Catalyst Series — Brand", "Publikasi", "Identitas resmi seri buku Catalyst.", "future", ""),
    ("Segera", "XUpscaler", "AI/ML · Desktop", "Upscaler gambar AI yang berjalan sepenuhnya offline.", "future", ""),
    ("Segera", "NuRichter's Academics Library", "Platform akademik", "Repositori paper, dataset, dan modul belajar.", "future", ""),
    ("Segera", "Ekspansi ke Surabaya", "Pengembangan bisnis", "Kemitraan baru dengan institusi Jawa Timur.", "future", ""),
]

STATUS = {
    "active": "Berjalan",
    "finished": "Selesai",
    "temporal": "Ditunda",
    "abandoned": "Dihentikan",
    "future": "Rencana",
}

# ---------------------------------------------------------------- TIM
TEAM = [
    ("Ibnu Khoirul Anwar", "Founder & CEO", "NuRichter Workspace"),
    ("Rahmat Hidayat", "Director of Strategy", "Workspace"),
    ("Jocellyn Fleudlys", "Finance Strategist", "Workspace"),
    ("Mochammad Aldi Mauludin", "Head of NuRichter Labs", "Labs · 6 orang"),
    ("Mulyadi Nur", "Head of Operations", "Mulya Jaya · 3 orang"),
    ("Pandu Muhammad Fazri", "Head of Operations", "Ragnarok · 2 orang"),
    ("Arya Saputra", "Head of Operations", "RigRoom · 3 orang"),
]

# ---------------------------------------------------------------- SEJARAH
TIMELINE = [
    ("Okt 2017", "Kanal YouTube “NuRichter”", "Konten", "Dimulai sebagai Ibnu Khoirul LPG, lalu Ibnu Khoirul MLOPG, sebelum menetap di nama NuRichter. Gameplay, walkthrough, dan identitas digital pertama."),
    ("2020", "Brand NuRichter berdiri", "Brand", "NuRichter resmi menjadi brand personal Ibnu Khoirul Anwar, wadah untuk minat teknik dan kreatif sekaligus."),
    ("Sep 2022", "Mulya Jaya", "Manufaktur CNC", "Awalnya proyek kompetisi nasional, lalu dijadikan layanan CNC milling dan 3D print skala UMKM Jakarta. Pesanan plakat pertama membuktikan NuRichter bisa membuat barang fisik."),
    ("Mei 2023", "RigRoom", "Layanan IoT", "Juga lahir dari kompetisi nasional. Layanan IoT berbasis Arduino, PLC Siemens & Mitsubishi, dan Raspberry Pi. “Your imagination can come true with RigRoom.”"),
    ("Mei 2023", "Typography Quickies", "Tipografi", "Infografis dengan karakter sendiri; setiap karya punya tanda tangan visualnya."),
    ("Jul 2023", "Ragnarok", "Elektrikal", "Layanan desain kelistrikan industri: pneumatik, hidrolik, SCADA tiga-fase. Melahirkan seri trainer PLC untuk pendidikan vokasi."),
    ("Sep 2025", "Kemitraan Seratus Ilmu", "Pelatihan", "Kolaborasi resmi dengan PT Karya Nusatama Indonesia: rebuild situs dan kontribusi modul pelatihan."),
    ("Sep 2025", "Fanpage Scaramouche & kanal Last Z", "Kreatif", "Visual storytelling di Facebook, dan kanal hardstyle bersama Eurekanion."),
    ("2025", "NuRichter Workspace diresmikan", "Workspace", "Semua sub-brand dan proyek disatukan di bawah satu workspace. “Richterize The Infinity” menjadi arah."),
    ("2026", "Babak riset", "R&D", "AgriHex-SkyCure, Wellsense, Sperm Quant, publikasi BST vs AVL di Jurnal Teknologi dan Open Source, dan dua buku Catalyst."),
    ("Berikutnya", "Belum ditulis", "Rencana", "Robotics Catalyst Part Two, NRM-1 Archer, NFF-X Axel, XUpscaler, dan ekspansi ke Surabaya."),
]

# ---------------------------------------------------------------- MITRA
PARTNERS = {
    "Perusahaan": [
        "PT Karya Nusatama Indonesia (Seratus Ilmu)", "PT Mesindo Tekniknesia", "PT Royal Teknik Gemilang",
        "PT Komatsu Indonesia", "BNI KCP Babek TNI",
    ],
    "Universitas": [
        "Universitas Esa Unggul Bekasi", "Universitas YARSI", "Universitas Negeri Jakarta",
        "Universitas BSI Kampus Pemuda", "Sekolah Tinggi Ilmu Pelayaran Jakarta",
    ],
    "Sekolah — Jakarta": [
        "SMK Negeri 4 Jakarta", "SMK Negeri 7 Jakarta", "SMK Negeri 10 Jakarta", "SMK Negeri 13 Jakarta",
        "SMK Negeri 17 Jakarta", "SMK Negeri 26 Jakarta", "SMK Negeri 35 Jakarta", "SMK Negeri 36 Jakarta",
        "SMK Negeri 41 Jakarta", "SMK Negeri 42 Jakarta", "SMK Negeri 46 Jakarta", "SMK Negeri 48 Jakarta",
        "SMK Negeri 49 Jakarta", "SMK Negeri 51 Jakarta", "SMK Negeri 53 Jakarta", "SMK Negeri 58 Jakarta",
        "SMK PGRI 11 Jakarta", "SMA Negeri 89 Jakarta", "SMA Negeri 102 Jakarta", "SMA Negeri 115 Jakarta",
        "SMP Negeri 200 Rorotan", "SMK Perguruan Cikini", "SMK Tarakanita 2", "SMK Muhammadiyah 4 Jakarta",
        "SMK Telkom Jakarta", "SMK Bunda Mulia", "SMK Satria", "SMK Bethel", "SMK Teladan Jakarta Timur",
        "SMK Global Mulia", "SMK Budi Perkasa", "SMK Bina Taruna", "SMK Mahanaim",
        "SMK Global Persada Mandiri", "SMK Taruna Budi Bangsa",
    ],
    "Sekolah — Bekasi & Cikarang": [
        "SMK Negeri 1 Kota Bekasi", "SMK Negeri 2 Kota Bekasi", "SMK Negeri 3 Kota Bekasi",
        "SMK Negeri 5 Kota Bekasi", "SMK Negeri 10 Kota Bekasi", "SMK Negeri 1 Cikarang Barat",
        "SMK Telekomunikasi Bekasi", "Sekolah Ananda Bekasi", "SMK Kesehatan Prima Indonesia",
        "SMK Mandiri Bekasi", "SMK Al-Azhar Bekasi",
    ],
    "Instansi": [
        "Kelurahan Rorotan", "Kecamatan Cilincing", "Kecamatan Cakung", "Walikota Jakarta Utara",
        "Walikota Jakarta Timur", "Walikota Jakarta Barat", "Pemprov DKI Jakarta", "Pemerintah Kota Bekasi",
        "Pemerintah Kabupaten Bekasi", "DJP Jakarta Sunter", "Sudin Pendidikan Wil. I & II Jakarta Utara",
        "Badan Kepegawaian Negara (BKN)",
    ],
}

# ---------------------------------------------------------------- LAYANAN
SERVICES = [
    ("IoT & IoE", "Dari sensor sampai cloud", "Prototipe hardware dengan Arduino, ESP32, dan Raspberry Pi; komunikasi MQTT/HTTP; dashboard pemantauan realtime; edge computing.", ["Hardware prototyping", "MQTT", "Dashboard cloud", "Edge computing"], "RigRoom"),
    ("Elektrikal industri", "Panel, PLC, SCADA", "Desain dan implementasi sistem kelistrikan industri dan komersial dengan PLC Siemens, Mitsubishi, dan Schneider; pneumatik, hidrolik, SCADA tiga-fase.", ["PLC programming", "Desain panel", "SCADA", "Pneumatik & hidrolik"], "Ragnarok"),
    ("Mekatronika", "Mekanik + elektronik + software", "Robotika, miniatur otomasi industri, sistem embedded, dan arsitektur cyber-physical.", ["Robotika", "Otomasi industri", "Arsitektur CPS", "Embedded"], "Labs"),
    ("CNC & 3D print", "Produksi fisik", "CNC milling, 3D print FDM, dan prototipe cepat skala UMKM, bersama Workshop Mekatronika SMK Negeri 4 Jakarta.", ["CNC milling", "FDM", "Rapid prototyping", "Pesanan massal"], "Mulya Jaya"),
    ("AI / ML", "LSTM & Transformer", "Prediksi deret waktu dengan LSTM, Transformer untuk NLP dan computer vision, penyeimbangan data dengan SMOTE, keputusan human-in-the-loop. Teruji di Wellsense dan AgriHex.", ["LSTM", "Transformer", "SMOTE", "Human-in-the-loop"], "Labs"),
    ("Konten kreatif", "Tipografi, video, identitas", "Infografis, video editing, konten YouTube, dan identitas brand dengan gaya Typography Quickies.", ["Tipografi", "Infografis", "Video", "Brand identity"], "Studio"),
]

PROCESS = [
    ("Konsultasi", "Kami dengarkan masalahnya, lihat lokasinya, dan sepakati apa yang dianggap berhasil."),
    ("Perancangan", "Gambar, skema, dan daftar komponen. Anda tahu biaya dan jadwalnya sebelum ada yang dibeli."),
    ("Implementasi", "Dibangun dan diuji di Labs, dengan laporan progres berkala."),
    ("Serah terima", "Unit, dokumentasi, dan pelatihan untuk tim yang akan memakainya."),
]

# ---------------------------------------------------------------- LAB
MACHINES = [
    (2, "CNC 5-Axis Twinhorn VTH-1055F", "Pemesinan 5 sumbu simultan, pelumas Castrol Magna BD 68", "CNC · 5 sumbu"),
    (1, "CNC SYIL X7/X5 Vertical", "Machining center vertikal untuk komponen mekanik skala menengah", "CNC · vertikal"),
    (2, "CNC Router 3040", "3 sumbu, 300 × 400 mm. Gravir, akrilik, PCB milling", "CNC · 3 sumbu"),
    (1, "Bambu Lab X1 Carbon", "CoreXY multi-material dengan AMS, presisi tinggi", "3D print · premium"),
    (3, "Creality Ender 3", "FDM 220 × 220 × 250 mm untuk prototipe cepat dan produksi UMKM", "3D print · FDM"),
    (7, "Lengan robot rakitan", "Konfigurasi Yalong YL-1B, platform demo robotika industri", "Robotika"),
]

LAB_CAPS = [
    ("CNC milling", "Aluminium, akrilik, kayu, komposit. Toleransi ±0,05 mm."),
    ("3D printing", "PLA, ABS, PETG, TPU. Volume cetak sampai 300 × 300 × 400 mm."),
    ("Elektronika", "Solder station, osiloskop, multimeter, prototipe PCB, embedded dan IoT."),
    ("Studio digital", "CAD/CAM, desain grafis, video, pengembangan ML. Fusion 360, SolidWorks, Python."),
]

LAB_PROJECTS = [
    ("active", "NuRichter Labs 2.0", "IoT · Computer vision", "Menambah computer vision ke kapabilitas IoT, menuju lab skala industri menengah."),
    ("active", "Miniatur Otomasi Industri 5.0", "Human-centric · Cobot", "Miniatur pabrik yang menggabungkan operator manusia dan cobot."),
    ("future", "NRM-1 “Archer”", "IoT · RC · Mekanik", "Platform peluncur RC beroda/rantai dengan telemetri IoT."),
    ("future", "NFF-X “Axel”", "IoT · RC · Mekanik", "Pesawat RC fixed-wing dengan sasis hibrida darat."),
]

# ---------------------------------------------------------------- SUB-BRAND
BRANDS = [
    {
        "id": "mulya-jaya", "page": "nurichter-mulya-jaya.html", "mark": "MJ",
        "name": "Mulya Jaya", "role": "Manufaktur CNC & 3D print", "since": "Sep 2022",
        "head": "Mulyadi Nur", "staff": 3, "fig": "cnc", "work": "mulya-jaya",
        "body": "Unit manufaktur NuRichter. Memproduksi akrilik presisi, plakat custom, medali, dan piala untuk sekolah, perusahaan, dan acara resmi. Lahir dari kompetisi nasional, kini melayani UMKM di Jakarta dan sekitarnya.",
        "log": [("Sep 2022", "Berdiri, CNC milling pertama"), ("2023", "10 desain baru plakat, medali, piala"), ("2024", "+26 desain, mulai 3D print"), ("2025", "+21 desain, lebih dari 50 varian")],
        "offer": ["CNC milling akrilik", "3D print FDM", "Desain piala & medali custom", "Pesanan massal institusi", "Rapid prototyping"],
        "cta": "Pesan produksi",
    },
    {
        "id": "rigroom", "page": "nurichter-rigroom.html", "mark": "RR",
        "name": "RigRoom", "role": "Layanan IoT · Arduino · PLC · Raspberry Pi", "since": "Mei 2023",
        "head": "Arya Saputra", "staff": 3, "fig": "arm", "work": "armx",
        "body": "Lini layanan IoT NuRichter. Menangani siklus penuh: hardware, firmware, sampai dashboard pemantauan, dari prototipe sensor sederhana hingga kendali berbasis PLC.",
        "log": [("Mei 2023", "Berdiri dari kompetisi nasional"), ("2023–24", "Smart Room Monitor & Control"), ("2024", "ArmX V1"), ("2024", "ArmX Pro V1"), ("2025–", "Proyek integrasi IoT di Labs")],
        "offer": ["Prototipe hardware (Arduino, ESP32, RPi)", "Pemrograman PLC (Siemens, Mitsubishi)", "Komunikasi MQTT / HTTP", "Otomasi ruangan & gedung", "Pengembangan lengan robot", "Dashboard realtime"],
        "cta": "Konsultasi IoT",
    },
    {
        "id": "ragnarok", "page": "nurichter-ragnarok.html", "mark": "RG",
        "name": "Ragnarok", "role": "Elektrikal · Pneumatik · Hidrolik", "since": "Jul 2023",
        "head": "Pandu Muhammad Fazri", "staff": 2, "fig": "plc", "work": "ragnarok-trainer",
        "body": "Layanan desain dan implementasi sistem kelistrikan skala industri. Berpengalaman dengan PLC Siemens, Mitsubishi, dan Schneider untuk pneumatik, hidrolik, dan SCADA, baik untuk industri maupun pendidikan vokasi.",
        "log": [("Jul 2023", "Berdiri"), ("2023–24", "Ragnarok Trainer Series"), ("2024", "Rebuild miniatur industri Yalong"), ("2025–", "Konsultasi & pelatihan industri")],
        "offer": ["Pemrograman PLC (Siemens, Mitsubishi, Schneider)", "Desain & wiring panel", "Sistem SCADA", "Desain pneumatik & hidrolik", "Unit trainer edukasi"],
        "cta": "Konsultasi elektrikal",
    },
]
