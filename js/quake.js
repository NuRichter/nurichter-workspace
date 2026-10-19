/* Hero beranda: bidang seismik Three.js.
   Garis-garis seismogram disusun dalam kedalaman. Klik memicu gempa
   di titik itu; magnitudonya tampil di readout. Tanpa interaksi,
   gempa kecil muncul sendiri setiap beberapa detik. */
import * as THREE from "./vendor/three.module.min.js";

const canvas = document.querySelector(".quake");
const hero = document.querySelector(".hero");
const roM = document.querySelector(".ro-m");
const roXY = document.querySelector(".ro-xy");

const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const ROWS = 54;
const COLS = 200;
const W = 16;   // lebar bidang
const D = 9;    // kedalaman bidang

function cssColor(name) {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return new THREE.Color(v || "#000");
}

function init() {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "low-power" });
  } catch (_) {
    return; // tanpa WebGL, hero tetap tampil tanpa animasi
  }
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  const target = new THREE.Vector3(1.2, 0, -1.2);

  let ink, accent, accent2, bg;
  const readTheme = () => {
    ink = cssColor("--ink"); accent = cssColor("--accent"); accent2 = cssColor("--accent-2"); bg = cssColor("--bg");
    if (logoMat) { logoMat.color.copy(accent); edgeMat.color.copy(ink); }
  };
  let logoMat = null, edgeMat = null;
  readTheme();

  // ---------------------------------------------------------------- logo 3D (episentrum)
  // path master logo NuRichter, kotak 700 x 781, simetris putar 180°
  const OUTER = [[415, 0], [0, 492], [48, 533.5], [306, 533.5], [285, 781], [700, 289], [652, 247.5], [394, 247.5]];
  const HOLES = [[[335, 191], [310, 493.5], [81, 493.5]], [[365, 590], [390, 287.5], [619, 287.5]]];
  const LOGO_H = 1.9;
  const S = LOGO_H / 781;
  const toV = ([x, y]) => new THREE.Vector2((x - 350) * S, (390.5 - y) * S);
  const shape = new THREE.Shape(OUTER.map(toV));
  HOLES.forEach((h) => shape.holes.push(new THREE.Path(h.map(toV))));
  const logoGeo = new THREE.ExtrudeGeometry(shape, { depth: 0.16, bevelEnabled: false });
  logoGeo.translate(0, 0, -0.08);
  logoMat = new THREE.MeshLambertMaterial({ color: accent });
  edgeMat = new THREE.LineBasicMaterial({ color: ink, transparent: true, opacity: 0.35 });
  const logo = new THREE.Group();
  const logoMesh = new THREE.Mesh(logoGeo, logoMat);
  logo.add(logoMesh, new THREE.LineSegments(new THREE.EdgesGeometry(logoGeo, 25), edgeMat));
  scene.add(logo);
  scene.add(new THREE.AmbientLight(0xffffff, 2.1));
  const sun = new THREE.DirectionalLight(0xffffff, 1.6);
  sun.position.set(-2, 4, 6);
  scene.add(sun);
  const LOGO = { x: 3.3, z: -1.0, s: 1 };
  let pulse = 0;
  let fromLogo = false;

  // satu THREE.Line per baris, posisi & warna diperbarui tiap frame
  const lines = [];
  const mat = new THREE.LineBasicMaterial({ vertexColors: true, transparent: true });
  for (let r = 0; r < ROWS; r++) {
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(COLS * 3);
    const col = new Float32Array(COLS * 3);
    const z = -D / 2 + (r / (ROWS - 1)) * D;
    for (let c = 0; c < COLS; c++) {
      pos[c * 3] = -W / 2 + (c / (COLS - 1)) * W;
      pos[c * 3 + 2] = z;
    }
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    geo.setAttribute("color", new THREE.BufferAttribute(col, 3));
    const line = new THREE.Line(geo, mat);
    line.frustumCulled = false;
    scene.add(line);
    lines.push({ geo, pos, col, z, depth: r / (ROWS - 1) });
  }

  // gempa aktif
  const quakes = [];
  let t = 0;
  let lastUser = -10;
  let nextAuto = 1.2;
  const pointer = { x: 99, z: 99, on: false };

  function addQuake(x, z, mag) {
    quakes.push({ x, z, t0: t, mag });
    if (quakes.length > 6) quakes.shift();
    if (roM) roM.textContent = "M " + mag.toFixed(1);
    if (roXY) roXY.textContent = `x ${x.toFixed(2)} · y ${z.toFixed(2)}`;
  }

  function height(x, z) {
    // getaran mikro latar
    let y = 0.035 * Math.sin(x * 1.3 + t * 0.7 + z * 0.8) + 0.025 * Math.sin(x * 2.9 - t * 1.1 + z * 2.1) + 0.015 * Math.sin(x * 7.1 + z * 5.3 + t * 2.3);
    // gempa: muka gelombang melingkar yang meluruh
    for (const q of quakes) {
      const dt = t - q.t0;
      const r = Math.hypot(x - q.x, z - q.z);
      const front = dt * 3.2;
      const amp = 0.12 * Math.pow(1.55, q.mag - 3) * Math.exp(-dt * 0.55) / (1 + r * 0.35);
      const env = Math.exp(-((r - front) ** 2) / 1.6);
      y += amp * env * Math.sin((r - front) * 4.2);
    }
    // getaran kecil di sekitar kursor
    if (pointer.on) {
      const r = Math.hypot(x - pointer.x, z - pointer.z);
      y += 0.09 * Math.exp(-r * r * 1.4) * Math.sin(t * 9 + r * 6);
    }
    return y;
  }

  const tmp = new THREE.Color();
  function update() {
    for (const L of lines) {
      // fade ke warna latar sesuai kedalaman (baris jauh lebih pudar)
      const base = tmp.copy(bg).lerp(ink, 0.12 + 0.5 * L.depth);
      for (let c = 0; c < COLS; c++) {
        const i = c * 3;
        const x = L.pos[i];
        const y = height(x, L.z);
        L.pos[i + 1] = y;
        // dua tahap: tinta → biru Richter → ungu Infinity di puncak gelombang
        const k = Math.min(1, Math.abs(y) * 5.5);
        let r, g, b;
        if (k < 0.55) {
          const u = k / 0.55;
          r = base.r + (accent.r - base.r) * u; g = base.g + (accent.g - base.g) * u; b = base.b + (accent.b - base.b) * u;
        } else {
          const u = (k - 0.55) / 0.45;
          r = accent.r + (accent2.r - accent.r) * u; g = accent.g + (accent2.g - accent.g) * u; b = accent.b + (accent2.b - accent.b) * u;
        }
        L.col[i] = r; L.col[i + 1] = g; L.col[i + 2] = b;
      }
      L.geo.attributes.position.needsUpdate = true;
      L.geo.attributes.color.needsUpdate = true;
    }
    // logo menunggang gelombang, berayun pelan, berdenyut saat memicu gempa
    pulse *= 0.94;
    const s = LOGO.s * (1 + pulse * 0.12);
    logo.position.set(LOGO.x, (LOGO_H / 2) * LOGO.s + 0.18 + height(LOGO.x, LOGO.z) * 1.4 + Math.sin(t * 0.8) * 0.05, LOGO.z);
    logo.rotation.set(Math.sin(t * 0.5) * 0.06, -0.35 + Math.sin(t * 0.35) * 0.45, Math.sin(t * 0.6) * 0.03);
    logo.scale.setScalar(s);
  }

  function resize() {
    const w = hero.clientWidth;
    const h = hero.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    // di layar sempit, kamera mundur supaya bidang tetap memenuhi hero
    const narrow = w < 700;
    // ponsel: logo pindah ke belakang tengah (area atas hero, di atas teks)
    if (narrow) { LOGO.x = 0.75; LOGO.z = -1.2; LOGO.s = 0.55; } else { LOGO.x = 3.3; LOGO.z = -1.0; LOGO.s = 1; }
    camera.position.set(narrow ? 0.4 : 0.6, narrow ? 6.4 : 4.4, narrow ? 6.6 : 6.4);
    camera.lookAt(narrow ? new THREE.Vector3(0, 0, 0.9) : target);
    camera.updateProjectionMatrix();
  }

  // raycast ke bidang y=0
  const ray = new THREE.Raycaster();
  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  const ndc = new THREE.Vector2();
  const hit = new THREE.Vector3();
  function toField(ev) {
    const b = canvas.getBoundingClientRect();
    ndc.set(((ev.clientX - b.left) / b.width) * 2 - 1, -((ev.clientY - b.top) / b.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    return ray.ray.intersectPlane(plane, hit) ? hit : null;
  }

  hero.addEventListener("pointermove", (ev) => {
    const p = toField(ev);
    if (p) { pointer.x = p.x; pointer.z = p.z; pointer.on = true; }
  });
  hero.addEventListener("pointerleave", () => { pointer.on = false; });
  canvas.addEventListener("pointerdown", (ev) => {
    // klik tepat di logo: gempa besar dari episentrum
    const b0 = canvas.getBoundingClientRect();
    ndc.set(((ev.clientX - b0.left) / b0.width) * 2 - 1, -((ev.clientY - b0.top) / b0.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    if (ray.intersectObject(logoMesh, false).length) {
      lastUser = t; pulse = 1;
      addQuake(LOGO.x, LOGO.z, 6 + Math.random() * 1.5);
      return;
    }
    const p = toField(ev);
    if (!p) return;
    lastUser = t;
    addQuake(p.x, p.z, 3.8 + Math.random() * 2.8);
    if (reduced) { update(); renderer.render(scene, camera); }
  });

  window.addEventListener("nr-theme", () => { readTheme(); if (reduced) { update(); renderer.render(scene, camera); } });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", readTheme);

  let visible = true;
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; }).observe(hero);

  resize();
  new ResizeObserver(resize).observe(hero);

  if (reduced) {
    addQuake(LOGO.x, LOGO.z, 5.2);
    t = 1.4;
    update();
    renderer.render(scene, camera);
    return;
  }

  const clock = new THREE.Clock();
  function frame() {
    requestAnimationFrame(frame);
    const dt = Math.min(clock.getDelta(), 0.05);
    if (!visible || document.hidden) return;
    t += dt;
    if (t > nextAuto && t - lastUser > 5) {
      // bergantian: dari logo (episentrum) dan dari titik acak
      fromLogo = !fromLogo;
      if (fromLogo) { pulse = 1; addQuake(LOGO.x, LOGO.z, 4.6 + Math.random() * 1.4); }
      else addQuake((Math.random() - 0.2) * W * 0.55, (Math.random() - 0.5) * D * 0.6, 3.2 + Math.random() * 2.2);
      nextAuto = t + 4.5 + Math.random() * 3;
    }
    update();
    renderer.render(scene, camera);
  }
  frame();
}

if (canvas && hero) init();
