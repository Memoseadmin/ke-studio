// v3 촬영기: HTML 카드 -> 1080x1350 PNG + 검수 측정(줄 수·넘침·안전 영역·실제 사용 서체).
// 사용: NODE_PATH=$(npm root -g) node shoot.cjs job.json   (render_v3.py 가 호출)
// 실제 사용 서체는 CDP CSS.getPlatformFontsForNode 로 받는다(폴백 서체가 끼면 render_v3.py 가 실패 처리).
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  const cdp = await page.context().newCDPSession(page);
  const results = [];
  for (const c of job.cards) {
    await page.goto('file://' + c.html, { waitUntil: 'load' });
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(i => (i.complete ? null : new Promise(r => { i.onload = i.onerror = r; }))));
    });
    const metrics = await page.evaluate(() => {
      const checks = [];
      for (const el of document.querySelectorAll('[data-check]')) {
        const cs = getComputedStyle(el);
        const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2;
        const range = document.createRange();
        range.selectNodeContents(el);
        const tops = [];
        for (const r of range.getClientRects()) {
          if (r.width < 0.5) continue;
          if (!tops.some(t => Math.abs(t - r.top) < lh * 0.5)) tops.push(r.top);
        }
        const b = el.getBoundingClientRect();
        checks.push({ check: el.dataset.check, max: +el.dataset.maxlines || 0, lines: tops.length,
          text: el.textContent, box: [b.left, b.top, b.right, b.bottom],
          overflow: el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + parseFloat(cs.fontSize) * 0.5 });
      }
      const imgs = [...document.images].map(i => { const b = i.getBoundingClientRect();
        return { src: i.getAttribute('src'), ok: i.complete && i.naturalWidth > 0, natural: [i.naturalWidth, i.naturalHeight], box: [b.left, b.top, b.right, b.bottom] }; });
      const card = document.querySelector('.card').getBoundingClientRect();
      const bottoms = [...document.querySelectorAll('.card > *:not(.mockup)')].map(e => e.getBoundingClientRect().bottom);
      return { checks, imgs, contentBottom: Math.max(...bottoms), cardBottom: card.bottom };
    });
    await cdp.send('DOM.enable');
    await cdp.send('CSS.enable');
    const { root } = await cdp.send('DOM.getDocument', { depth: -1 });
    const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: root.nodeId, selector: '[data-font]' });
    const fonts = {};
    for (const id of nodeIds) {
      const r = await cdp.send('CSS.getPlatformFontsForNode', { nodeId: id });
      for (const f of r.fonts) {
        const k = f.familyName + (f.isCustomFont ? '' : ' (system)');
        fonts[k] = (fonts[k] || 0) + f.glyphCount;
      }
    }
    await page.screenshot({ path: c.png, type: 'png' });
    results.push({ n: c.n, metrics, fonts });
  }
  await browser.close();
  process.stdout.write(JSON.stringify(results));
})().catch(e => { console.error(e); process.exit(1); });
