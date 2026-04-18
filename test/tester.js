// ============================================================
//  OffGrid UI Tester
//  Crawls routes, clicks controls, submits forms, reports issues
// ============================================================

const { chromium } = require('playwright');
const Anthropic = require('@anthropic-ai/sdk');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://localhost:5000';
const REPORT_OUT = path.join(__dirname, 'report.html');
// const client = new Anthropic(); // reads ANTHROPIC_API_KEY from env

function log(msg, type = 'info') {
  const icons = { info: '->', ok: 'OK', warn: '!!', error: 'XX', ai: 'AI' };
  console.log(`${icons[type] || '..'} ${msg}`);
}

async function askClaude(prompt) {
  // Optional AI review hook is intentionally disabled for now.
  void prompt;
  return '';
}

async function crawlRoutes(page) {
  const visited = new Set();
  const queue = [BASE_URL, `${BASE_URL}/dashboard.html`, `${BASE_URL}/sponsor_dashboard.html`];
  const found = [];

  const normalizeUrl = (value) => {
    const url = new URL(value);
    url.hash = '';
    return url.toString();
  };

  while (queue.length) {
    const url = normalizeUrl(queue.shift());
    if (visited.has(url)) continue;
    visited.add(url);
    found.push(url);

    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 10000 });
      const links = await page.$$eval('a[href]', (els) =>
        els.map((a) => a.href).filter((h) => h && !h.startsWith('mailto') && !h.startsWith('tel'))
      );
      for (const link of links) {
        const normalized = normalizeUrl(link);
        if (normalized.startsWith(BASE_URL) && !visited.has(normalized)) queue.push(normalized);
      }
    } catch (_) {}
  }

  return [...new Set(found)];
}

async function findDemoCredentials(page) {
  try {
    await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 10000 });
    const bodyText = await page.evaluate(() => document.body.innerText.slice(0, 3000));
    const html = await page.content();

    const answer = await askClaude(
      `You are inspecting a web app. Here is the visible page text:\n\n${bodyText}\n\n` +
      `And here is a snippet of the HTML:\n\n${html.slice(0, 3000)}\n\n` +
      `Find any demo/test login credentials (email, username, password). ` +
      `Reply ONLY in JSON like: {"email":"...","password":"..."} or {"username":"...","password":"..."}. ` +
      `If none found, reply: {"email":"demo@example.com","password":"demo123"}`
    );

    const json = answer.match(/\{[\s\S]*?\}/);
    if (json) return JSON.parse(json[0]);
  } catch (_) {}

  return { email: 'demo@example.com', password: 'demo123' };
}

function buildRunCredentials(baseCreds) {
  const uniqueSuffix = Date.now();
  return {
    ...baseCreds,
    registerEmail: `qa+${uniqueSuffix}@example.com`,
    username: baseCreds.username || `qa_user_${uniqueSuffix}`,
  };
}

async function testPage(page, url, creds, issues) {
  log(`Testing: ${url}`);
  const pageIssues = [];

  try {
    const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });

    if (response && response.status() >= 400) {
      pageIssues.push({
        type: 'HTTP Error',
        severity: 'critical',
        detail: `Page returned HTTP ${response.status()}`,
        fix: `Check your server route handler for ${url}. Make sure the route is defined and the handler returns a proper response.`
      });
    }

    const consoleErrors = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const brokenImgs = await page.$$eval('img', (imgs) =>
      imgs.filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.src)
    );
    for (const src of brokenImgs) {
      pageIssues.push({
        type: 'Broken Image',
        severity: 'warning',
        detail: `Image failed to load: ${src}`,
        fix: `Check the image path "${src}". Make sure the file exists and the path is correct relative to your server's static folder.`
      });
    }

    const buttons = await page.$$('button, input[type="submit"], input[type="button"], a[role="button"]');
    log(`  Found ${buttons.length} buttons on ${url}`);

    for (let i = 0; i < buttons.length; i++) {
      try {
        const btn = buttons[i];
        const isInHiddenContainer = await btn.evaluate((el) => {
          let node = el;
          while (node) {
            if (node.hidden) return true;
            if (node.getAttribute && node.getAttribute('aria-hidden') === 'true') return true;
            const style = window.getComputedStyle(node);
            if (style.display === 'none' || style.visibility === 'hidden') return true;
            node = node.parentElement;
          }
          return false;
        });
        if (isInHiddenContainer) continue;

        const isFormSubmitButton = await btn.evaluate((el) => {
          const form = el.closest('form');
          if (!form) return false;
          if (el.tagName === 'INPUT') {
            return el.type === 'submit';
          }
          if (el.tagName === 'BUTTON') {
            return !el.type || el.type === 'submit';
          }
          return false;
        });
        if (isFormSubmitButton) continue;

        const label = await btn.evaluate((el, idx) =>
          el.textContent?.trim() || el.value || el.getAttribute('aria-label') || `Button #${idx + 1}`, i
        );
        if (/sign out|logout|log out/i.test(label)) continue;
        const isVisible = await btn.isVisible();
        const isEnabled = await btn.isEnabled();

        if (!isVisible) {
          pageIssues.push({
            type: 'Hidden Button',
            severity: 'warning',
            detail: `Button "${label}" is hidden (display:none or visibility:hidden)`,
            fix: `Review the CSS or JS controlling visibility of "${label}". If it should be visible, check conditional rendering logic.`
          });
          continue;
        }

        if (!isEnabled) {
          pageIssues.push({
            type: 'Disabled Button',
            severity: 'info',
            detail: `Button "${label}" is disabled`,
            fix: `Confirm that "${label}" is intentionally disabled. If not, check the disabled attribute or JS logic that controls it.`
          });
          continue;
        }

        const errorsBefore = [...consoleErrors];
        try {
          await btn.click({ timeout: 3000 });
          await page.waitForTimeout(800);
        } catch (clickErr) {
          pageIssues.push({
            type: 'Click Failed',
            severity: 'warning',
            detail: `Could not click button "${label}": ${clickErr.message}`,
            fix: `Check the click handler or DOM state for "${label}".`
          });
        }

        const newErrors = consoleErrors.filter((e) => !errorsBefore.includes(e));
        for (const err of newErrors) {
          pageIssues.push({
            type: 'JS Console Error',
            severity: 'error',
            detail: `Clicking "${label}" triggered: ${err}`,
            fix: `Fix the JavaScript error triggered by "${label}": ${err}`
          });
        }

        if (!page.url().startsWith(url.split('?')[0])) {
          await page.goBack({ waitUntil: 'networkidle', timeout: 5000 }).catch(() => page.goto(url));
        }
      } catch (_) {}
    }

    const forms = await page.$$('form');
    for (let fi = 0; fi < forms.length; fi++) {
      try {
        const isHiddenForm = await forms[fi].evaluate((form) => {
          if (form.hidden || form.getAttribute('aria-hidden') === 'true') return true;
          const style = window.getComputedStyle(form);
          return style.display === 'none' || style.visibility === 'hidden';
        });
        if (isHiddenForm) continue;

        const formKind = await forms[fi].evaluate((form) => {
          const id = (form.id || '').toLowerCase();
          const name = (form.getAttribute('name') || '').toLowerCase();
          const text = (form.innerText || '').toLowerCase();
          return { id, name, text };
        });
        const isRegisterForm =
          formKind.id.includes('register') ||
          formKind.name.includes('register') ||
          formKind.text.includes('create account') ||
          formKind.text.includes('join offgrid');

        const inputs = await forms[fi].$$('input:not([type="hidden"]):not([type="submit"])');
        for (const input of inputs) {
          const type = await input.getAttribute('type') || 'text';
          const name = (await input.getAttribute('name') || '').toLowerCase();
          const placeholder = (await input.getAttribute('placeholder') || '').toLowerCase();

          let value = 'test_value';
          if (type === 'email' || name.includes('email') || placeholder.includes('email')) value = isRegisterForm ? (creds.registerEmail || creds.email || 'demo@example.com') : (creds.email || 'demo@example.com');
          else if (type === 'password' || name.includes('pass')) value = creds.password || 'demo123';
          else if (name.includes('user') || name.includes('name')) value = creds.username || creds.email || 'demo_user';
          else if (type === 'number') value = '42';
          else if (type === 'tel') value = '9999999999';

          await input.fill(value).catch(() => {});
        }

        const submitBtn = await forms[fi].$('button[type="submit"], input[type="submit"]');
        if (submitBtn) {
          const errorsBefore = [...consoleErrors];
          await submitBtn.click({ timeout: 3000 }).catch(() => {});
          await page.waitForTimeout(1000);

          const newErrors = consoleErrors.filter((e) => !errorsBefore.includes(e));
          for (const err of newErrors) {
            pageIssues.push({
              type: 'Form Submit Error',
              severity: 'error',
              detail: `Form #${fi + 1} submission triggered JS error: ${err}`,
              fix: `Fix the error in the form submit handler: ${err}`
            });
          }

          const alerts = await page.$$eval('[class*="error"],[class*="alert"],[class*="invalid"]', (els) =>
            els.map((el) => el.textContent?.trim()).filter(Boolean)
          );
          for (const alert of alerts) {
            pageIssues.push({
              type: 'Form Validation',
              severity: 'info',
              detail: `Form showed message: "${alert}"`,
              fix: `Review validation logic for this message: "${alert}". Ensure it only appears when appropriate.`
            });
          }
        }

        if (!page.url().startsWith(url.split('?')[0])) {
          await page.goto(url, { waitUntil: 'networkidle', timeout: 10000 }).catch(() => {});
        }
      } catch (_) {}
    }

    const pageText = await page.evaluate(() => document.body.innerText.slice(0, 2000)).catch(() => '');
    if (pageText.length > 100) {
      const aiReview = await askClaude(
        `You are a web QA engineer reviewing a page at URL: ${url}\n\n` +
        `Visible page content:\n${pageText}\n\n` +
        `Issues already found: ${JSON.stringify(pageIssues.map((i) => i.detail))}\n\n` +
        `Identify any UX problems, missing content, broken flows, or accessibility issues NOT already listed. ` +
        `Reply as a JSON array of objects with keys: type, severity (critical/error/warning/info), detail, fix. ` +
        `Keep it to max 3 most important issues. If none found, reply: []`
      );
      try {
        const arr = JSON.parse(aiReview.match(/\[[\s\S]*\]/)?.[0] || '[]');
        for (const item of arr) pageIssues.push({ ...item, source: 'ai' });
      } catch (_) {}
    }

    if (pageIssues.length === 0) log('  No issues', 'ok');
    else log(`  ${pageIssues.length} issue(s) found`, 'warn');

    issues.push({ url, issues: pageIssues });
  } catch (err) {
    log(`  Failed to load: ${err.message}`, 'error');
    issues.push({
      url,
      issues: [{
        type: 'Page Load Failed',
        severity: 'critical',
        detail: err.message,
        fix: `The page at ${url} failed to load. Check your server is running and the route exists.`
      }]
    });
  }
}

function generateReport(allIssues, creds) {
  const severityColor = { critical: '#e74c3c', error: '#e67e22', warning: '#f1c40f', info: '#3498db' };
  const total = allIssues.reduce((s, p) => s + p.issues.length, 0);
  const pagesWithIssues = allIssues.filter((p) => p.issues.length > 0).length;

  const pageBlocks = allIssues.map((p) => {
    if (p.issues.length === 0) {
      return `<div class="page ok"><span class="url">${p.url}</span> <span class="badge ok-badge">Clean</span></div>`;
    }

    const rows = p.issues.map((i) => `
      <div class="issue">
        <div class="issue-header">
          <span class="badge" style="background:${severityColor[i.severity] || '#888'}">${i.severity.toUpperCase()}</span>
          <strong>${i.type}</strong>
          ${i.source === 'ai' ? '<span class="ai-tag">AI</span>' : ''}
        </div>
        <p class="detail">${i.detail}</p>
        <div class="fix"><strong>Fix:</strong> ${i.fix}</div>
      </div>`).join('');

    return `<div class="page"><span class="url">${p.url}</span><div class="issues">${rows}</div></div>`;
  }).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>OffGrid Test Report</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #0f1117; color: #e2e8f0; padding: 32px; }
  h1 { font-size: 28px; font-weight: 700; margin-bottom: 4px; color: #fff; }
  .subtitle { color: #718096; margin-bottom: 32px; font-size: 14px; }
  .stats { display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }
  .stat { background: #1a1d27; border: 1px solid #2d3148; border-radius: 10px; padding: 16px 24px; }
  .stat-num { font-size: 32px; font-weight: 700; color: #fff; }
  .stat-label { font-size: 12px; color: #718096; margin-top: 2px; }
  .page { background: #1a1d27; border: 1px solid #2d3148; border-radius: 10px; margin-bottom: 16px; padding: 20px; }
  .page.ok { display: flex; align-items: center; gap: 12px; padding: 14px 20px; }
  .url { font-family: monospace; font-size: 14px; color: #a0aec0; word-break: break-all; }
  .issues { margin-top: 16px; display: flex; flex-direction: column; gap: 12px; }
  .issue { background: #13151f; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #444; }
  .issue-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
  .badge { font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px; color: #000; }
  .ok-badge { background: #2ecc71; color: #000; }
  .ai-tag { font-size: 12px; color: #a78bfa; }
  .detail { font-size: 14px; color: #cbd5e0; margin-bottom: 8px; line-height: 1.5; }
  .fix { font-size: 13px; background: #1e2235; border: 1px solid #2d3755; border-radius: 6px; padding: 10px 12px; color: #90cdf4; line-height: 1.6; }
  .creds { background: #1a2035; border: 1px solid #2d4068; border-radius: 10px; padding: 16px 20px; margin-bottom: 28px; font-size: 14px; color: #90cdf4; }
  .creds strong { color: #fff; }
</style>
</head>
<body>
<h1>OffGrid Test Report</h1>
<p class="subtitle">Generated ${new Date().toLocaleString()}</p>

<div class="creds">
  <strong>Demo credentials used:</strong>
  ${Object.entries(creds).map(([k, v]) => `${k}: <code>${v}</code>`).join('  |  ')}
</div>

<div class="stats">
  <div class="stat"><div class="stat-num">${allIssues.length}</div><div class="stat-label">Pages tested</div></div>
  <div class="stat"><div class="stat-num">${pagesWithIssues}</div><div class="stat-label">Pages with issues</div></div>
  <div class="stat"><div class="stat-num">${total}</div><div class="stat-label">Total issues found</div></div>
  <div class="stat"><div class="stat-num">${allIssues.filter((p) => p.issues.length === 0).length}</div><div class="stat-label">Clean pages</div></div>
</div>

${pageBlocks}
</body>
</html>`;
}

(async () => {
  log('OffGrid UI Tester starting...');
  log(`Target: ${BASE_URL}`);

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();

  log('Looking for demo credentials...', 'ai');
  const creds = buildRunCredentials(await findDemoCredentials(page));
  log(`Using credentials: ${JSON.stringify(creds)}`, 'ok');

  log('Crawling all routes...');
  const routes = await crawlRoutes(page);
  log(`Found ${routes.length} routes: ${routes.join(', ')}`, 'ok');

  const allIssues = [];
  for (const route of routes) {
    await testPage(page, route, creds, allIssues);
    await page.waitForTimeout(500);
  }

  const html = generateReport(allIssues, creds);
  fs.writeFileSync(REPORT_OUT, html, 'utf8');
  log(`Report saved -> ${REPORT_OUT}`, 'ok');
  log('Open report.html in your browser to review the results.', 'ok');

  await browser.close();
})();
