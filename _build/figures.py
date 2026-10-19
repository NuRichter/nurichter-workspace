"""Gambar teknik inline SVG. Semua garis memakai currentColor; aksen memakai var(--accent)."""
import math


def _wrap(body, label, vb="0 0 400 260"):
    return (
        f'<svg class="fig" viewBox="{vb}" role="img" aria-label="{label}" '
        f'fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">'
        f"{body}</svg>"
    )


def _t(x, y, s, anchor="start", cls="lbl"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def bstavl():
    out = []
    # BST degenerasi: rantai diagonal
    for i in range(7):
        x, y = 30 + i * 22, 40 + i * 25
        if i:
            out.append(f'<line x1="{x-22+5}" y1="{y-25+5}" x2="{x-5}" y2="{y-5}"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="7" class="acc-s"/>')
        out.append('<line x1="18" y1="40" x2="18" y2="190" class="dim"/>')
    out.append('<path d="M14 40h8M14 190h8" class="dim"/>')
    out.append(_t(24, 232, "BST · sorted input"))
    out.append(_t(24, 246, "h = 4.999", cls="lbl acc"))
    # AVL seimbang
    nodes = {}
    def tree(x, y, dx, depth, key):
        nodes[key] = (x, y)
        if depth == 0:
            return
        for side, k in ((-1, "l"), (1, "r")):
            cx, cy = x + side * dx, y + 42
            out.append(f'<line x1="{x}" y1="{y+7}" x2="{cx}" y2="{cy-7}"/>')
            tree(cx, cy, dx / 2, depth - 1, key + k)
    tree(292, 50, 50, 3, "")
    for x, y in nodes.values():
        out.append(f'<circle cx="{x}" cy="{y}" r="6"/>')
    out.append(_t(228, 232, "AVL · same input"))
    out.append(_t(228, 246, "h = 12", cls="lbl"))
    return _wrap("".join(out), "Diagram pohon: BST menjadi rantai, AVL tetap seimbang")


def gifpdf():
    o = ['<rect x="40" y="24" width="150" height="200" rx="2"/>',
         '<path d="M160 24v30h30" opacity=".5"/>',
         _t(52, 46, "PDF")]
    for i in range(4):
        x = 56 + i * 30
        cls = ' class="acc-s"' if i == 2 else ""
        o.append(f'<rect x="{x}" y="90" width="24" height="60"{cls}/>')
        o.append(f'<circle cx="{x+12}" cy="{108 + (i%2)*20}" r="4"/>')
    o.append('<path d="M56 165h118" class="dim"/>')
    o.append(_t(56, 182, "frame 3/4")); o.append(_t(56, 196, "JS trigger", cls="lbl mute"))
    # bar ukuran
    o.append('<rect x="230" y="70" width="140" height="22"/>')
    o.append('<rect x="230" y="120" width="44" height="22" class="acc-f"/>')
    o.append(_t(230, 62, "before · 34 MB"))
    o.append(_t(230, 112, "after · 10.7 MB", cls="lbl acc"))
    o.append('<path d="M274 131h96" stroke-dasharray="3 4" opacity=".5"/>')
    o.append(_t(230, 176, "Chrome · Edge"))
    o.append(_t(230, 192, "Firefox 157 · PDF.js 6.3"))
    return _wrap("".join(o), "Halaman PDF berisi frame animasi; ukuran berkas turun dari 34 MB ke 10,7 MB")


def web():
    o = ['<rect x="24" y="30" width="250" height="180" rx="4"/>',
         '<path d="M24 50h250"/>',
         '<circle cx="36" cy="40" r="2.5"/><circle cx="46" cy="40" r="2.5"/><circle cx="56" cy="40" r="2.5"/>',
         '<rect x="40" y="66" width="110" height="12" class="acc-f"/>',
         '<path d="M40 92h180M40 102h150" opacity=".6"/>',
         '<rect x="40" y="120" width="68" height="70"/><rect x="118" y="120" width="68" height="70"/><rect x="196" y="120" width="62" height="70"/>',
         '<rect x="298" y="60" width="78" height="150" rx="10"/>',
         '<path d="M326 70h22" />',
         '<rect x="308" y="88" width="44" height="8" class="acc-f"/>',
         '<path d="M308 104h56M308 112h40" opacity=".6"/>',
         '<rect x="308" y="124" width="58" height="34"/><rect x="308" y="164" width="58" height="34"/>',
         _t(24, 236, "desktop · 1280"), _t(298, 236, "mobile · 375")]
    return _wrap("".join(o), "Wireframe situs di desktop dan ponsel")


def books():
    o = []
    specs = [("HUMAN CATALYST", 70, 34, False), ("ROBOTICS CATALYST · I", 120, 40, True), ("ROBOTICS CATALYST · II", 176, 40, False)]
    for title, x, w, acc in specs:
        dash = ' stroke-dasharray="4 4"' if title.endswith("II") else ""
        cls = ' class="acc-s"' if acc else ""
        o.append(f'<rect x="{x}" y="40" width="{w}" height="180"{cls}{dash}/>')
        o.append(f'<text class="lbl spine" transform="translate({x + w/2 + 4} 210) rotate(-90)">{title}</text>')
    o.append('<path d="M40 220h240"/>')
    o.append(_t(250, 70, "Part II"))
    o.append(_t(250, 84, "planned", cls="lbl mute"))
    return _wrap("".join(o), "Tiga punggung buku seri Catalyst")


def casa():
    o = ['<circle cx="200" cy="130" r="104"/>', '<circle cx="200" cy="130" r="98" opacity=".35"/>']
    tracks = [(130, 90, 1), (230, 70, 0), (170, 170, 0), (260, 150, 1), (150, 130, 0)]
    for i, (x, y, acc) in enumerate(tracks):
        pts = []
        for k in range(9):
            pts.append(f"{x + k*7 + 6*math.sin(k*1.3+i):.1f},{y + 5*math.cos(k*0.9+i*2) + k*1.5:.1f}")
        cls = ' class="acc-s"' if acc else ' opacity=".7"'
        o.append(f'<polyline points="{" ".join(pts)}"{cls}/>')
        ex, ey = pts[-1].split(",")
        o.append(f'<circle cx="{ex}" cy="{ey}" r="3.5"/>')
    o.append('<path d="M96 130h-24M304 130h24M200 26v-14M200 234v14" class="dim"/>')
    o.append(_t(318, 40, "track / frame"))
    o.append(_t(318, 54, "VCL · VSL · LIN", cls="lbl mute"))
    return _wrap("".join(o), "Lintasan sel sperma yang dilacak di bidang pandang mikroskop")


def archer():
    o = ['<rect x="70" y="150" width="220" height="44" rx="22"/>']
    for x in range(92, 290, 34):
        o.append(f'<circle cx="{x}" cy="172" r="12"/>')
    o.append('<rect x="100" y="120" width="150" height="30"/>')
    o.append('<g transform="rotate(-24 210 120)"><rect x="150" y="96" width="170" height="20" class="acc-s"/><path d="M320 96l18 10-18 10"/></g>')
    o.append('<circle cx="210" cy="120" r="5"/>')
    o.append('<path d="M250 120 A40 40 0 0 0 246 104" class="dim"/>')
    o.append(_t(258, 112, "24°"))
    o.append('<path d="M70 214h220M70 210v8M290 210v8" class="dim"/>')
    o.append(_t(180, 232, "wheeled / tracked chassis", "middle"))
    o.append('<path d="M120 120v-30M114 90h12" />')
    o.append(_t(108, 82, "IoT telemetry"))
    return _wrap("".join(o), "Sketsa NRM-1 Archer: sasis rantai dengan tabung peluncur")


def seismo(seed=0, w=400, h=60, n=200):
    pts = []
    for i in range(n + 1):
        x = i * w / n
        env = math.exp(-((i - n * 0.55) / (n * 0.09)) ** 2)
        y = h / 2 + (math.sin(i * 0.9 + seed) * 2 + math.sin(i * 2.3 + seed) * 1.2) + env * 22 * math.sin(i * 1.7 + seed)
        pts.append(f"{x:.1f},{y:.1f}")
    return f'<svg class="seis" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true"><polyline points="{" ".join(pts)}" fill="none" stroke="currentColor" stroke-width="1.2" vector-effect="non-scaling-stroke"/></svg>'


FIGS = {"bstavl": bstavl, "gifpdf": gifpdf, "web": web, "books": books, "casa": casa, "archer": archer}
