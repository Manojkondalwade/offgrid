# OffGrid UI Tester

Automatically crawls the OffGrid app, clicks visible controls, fills forms with demo credentials, and generates an HTML bug report.

---

## Setup

```bash
# 1. Install Node dependencies
npm install

# 2. Install Playwright's Chromium browser
npx playwright install chromium

# 3. Start the OffGrid app on port 5000
cd Backend
python run.py
```

---

## Run

Make sure the OffGrid server is running on port 5000, then:

```bash
npm test
```

A browser window will open while the tester crawls and checks the site.

When done, open `report.html` in your browser to see:
- Every page tested
- Button and form interaction results
- Issues grouped by severity
- Suggested fixes for each issue

---

## What It Checks

| Check | Description |
|---|---|
| HTTP status | Detects 404, 500, and other failed responses |
| Broken images | Finds images that fail to load |
| Button clicks | Clicks visible buttons and captures JS errors |
| Form filling | Fills forms with demo values and submits them |
| Console errors | Captures JavaScript errors triggered by interactions |
| AI review stub | Present in `tester.js`, but currently disabled |

---

## Credentials

The tester tries to detect demo credentials from the app.
If none are found, it falls back to `demo@example.com` / `demo123`.
