// Uji asap: semua halaman × beberapa bahasa.
// - error konsol / pelanggaran CSP / respons 4xx-5xx
// - overflow horizontal di layar 390 px
// - audit aksesibilitas axe-core (WCAG 2.1 A/AA, dampak serius & kritis)
//
//   python3 tools/serve.py 8765 &   lalu   node tests/smoke.mjs
// Butuh paket npm: playwright, axe-core (lihat .github/workflows/ci.yml)
import { createRequire } from 'node:module';
import { readdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const AXE = readFileSync(process.env.AXE_PATH || require.resolve('axe-core/axe.min.js'), 'utf8');
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const BASE = process.env.BASE_URL || 'http://localhost:8765';
const LANGS = (process.env.LANGS || 'id,en,ar,ja').split(',');
const pages = readdirSync(ROOT).filter((f) => f.endsWith('.html')).sort();

const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
let failures = 0;
const report = [];
for (const lang of LANGS) {
  for (const vp of [{ width: 1280, height: 860 }, { width: 390, height: 844 }]) {
    const ctx = await browser.newContext({ viewport: vp, locale: 'id-ID' });
    for (const pg of pages) {
      const p = await ctx.newPage();
      const errs = [];
      p.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
      p.on('console', (m) => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
      p.on('response', (r) => { if (r.status() >= 400 && !r.url().endsWith('/404.html') && !(pg === '404.html' && r.url().includes('404'))) errs.push(`${r.status()} ${r.url()}`); });
      await p.goto(`${BASE}/${pg}?lang=${lang}`, { waitUntil: 'networkidle' });
      await p.waitForTimeout(250);
      const st = await p.evaluate(() => ({
        hidden: document.documentElement.classList.contains('i18n-wait'),
        overflow: document.documentElement.scrollWidth > innerWidth + 1,
      }));
      if (st.hidden) errs.push('halaman masih tersembunyi (i18n-wait)');
      if (st.overflow) errs.push(`overflow horizontal di ${vp.width}px`);
      if (vp.width === 1280 && (lang === 'id' || lang === 'ar')) {
        await p.evaluate(AXE); // lewat DevTools: tidak diblok CSP
        const res = await p.evaluate(async () => {
          const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] } });
          return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact)).map((v) => `${v.id} (${v.nodes.length}): ${v.nodes.slice(0, 2).map((n) => n.target.join(' ')).join(' | ')}`);
        });
        res.forEach((r) => errs.push('axe: ' + r));
      }
      if (errs.length) { failures++; report.push(`✗ ${lang} ${vp.width} ${pg}\n   ${errs.slice(0, 6).join('\n   ')}`); }
      await p.close();
    }
    await ctx.close();
  }
}
await browser.close();
console.log(report.join('\n') || '');
console.log(`${pages.length} halaman × ${LANGS.length} bahasa × 2 layar — ${failures} bermasalah`);
process.exit(failures ? 1 : 0);
