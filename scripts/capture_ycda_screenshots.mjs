import { chromium } from "playwright";
import { mkdir, copyFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const brandDir = path.join(root, "Brand", "ycda", "screenshots");
const assetsDir = path.join(root, "src", "assets", "ycda-screenshots");

/** Desktop viewport — matches capture size for the OJA preview frame. */
const VIEWPORT = { width: 1440, height: 900 };

/**
 * Live YCDA site is a single-page app with hash sections (verified 2026-06).
 * /classes/, /book-a-taster/, /member-portal/ return 404.
 */
const shots = [
  ["https://youcandanceacademy.co.uk/", "home.png", null],
  ["https://youcandanceacademy.co.uk/#classes", "classes.png", "#classes"],
  ["https://youcandanceacademy.co.uk/#signup", "tasters.png", "#signup"],
  ["https://youcandanceacademy.co.uk/portal/login", "portal.png", null],
];

const ACCEPT_SELECTORS = [
  "#onetrust-accept-btn-handler",
  "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
  "#CybotCookiebotDialogBodyButtonAccept",
  "button[data-cookie-accept]",
  "[data-cookie] button",
  ".cookie-notice button",
  ".cookie-banner button",
  "#cookie-notice button",
  "#cookie-consent button",
  ".cc-btn.cc-dismiss",
  ".cc-accept",
  "[class*='cookie'] button[class*='accept']",
  "[id*='cookie'] button",
  "button:has-text('Accept all')",
  "button:has-text('Accept All')",
  "button:has-text('Accept cookies')",
  "button:has-text('Accept Cookies')",
  "button:has-text('Allow all')",
  "button:has-text('Allow All')",
  "button:has-text('I agree')",
  "button:has-text('Agree')",
  "button:has-text('OK')",
  "button:has-text('Got it')",
  "a:has-text('Accept')",
];

const HIDE_COOKIE_CSS = `
  #onetrust-banner-sdk, #onetrust-consent-sdk, .onetrust-pc-dark-filter,
  #CybotCookiebotDialog, #CybotCookiebotDialogBodyUnderlay,
  [id*='cookie' i], [class*='cookie' i], [class*='consent' i],
  [data-cookie], .cookie-notice, .cookie-banner, #cookie-notice,
  .cc-window, .cc-banner, [aria-label*='cookie' i] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
  }
  body { overflow: auto !important; }
`;

async function dismissCookieBanner(page) {
  await page.waitForTimeout(1200);

  for (const selector of ACCEPT_SELECTORS) {
    try {
      const el = page.locator(selector).first();
      if (await el.isVisible({ timeout: 600 })) {
        await el.click({ timeout: 3000 });
        await page.waitForTimeout(800);
        return true;
      }
    } catch {
      /* try next */
    }
  }

  try {
    const clicked = await page.evaluate(() => {
      const labels = [
        "accept all",
        "accept cookies",
        "allow all",
        "i agree",
        "agree",
        "got it",
        "ok",
      ];
      const nodes = document.querySelectorAll("button, a, [role='button']");
      for (const node of nodes) {
        const text = (node.textContent || "").trim().toLowerCase();
        if (labels.some((l) => text === l || text.startsWith(l + " "))) {
          node.click();
          return true;
        }
      }
      return false;
    });
    if (clicked) {
      await page.waitForTimeout(800);
      return true;
    }
  } catch {
    /* fall through */
  }

  await page.addStyleTag({ content: HIDE_COOKIE_CSS });
  await page.waitForTimeout(400);
  return false;
}

async function waitForPageReady(page, hashSelector) {
  await page.waitForLoadState("networkidle", { timeout: 45000 }).catch(() => {});
  await page.waitForTimeout(2500);

  if (hashSelector) {
    try {
      await page.locator(hashSelector).first().waitFor({ state: "visible", timeout: 15000 });
      await page.locator(hashSelector).first().scrollIntoViewIfNeeded();
    } catch {
      await page.evaluate((sel) => {
        const el = document.querySelector(sel);
        if (el) el.scrollIntoView({ behavior: "instant", block: "start" });
      }, hashSelector);
    }
    await page.waitForTimeout(2000);
  } else {
    await page.waitForTimeout(1000);
  }
}

await mkdir(brandDir, { recursive: true });
await mkdir(assetsDir, { recursive: true });

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: VIEWPORT,
  locale: "en-GB",
  deviceScaleFactor: 1,
});
const page = await context.newPage();
let ok = 0;

console.log(`Viewport: ${VIEWPORT.width}×${VIEWPORT.height}`);

for (const [url, name, hashSelector] of shots) {
  const out = path.join(brandDir, name);
  try {
    await page.goto(url, { waitUntil: "load", timeout: 60000 });
    const dismissed = await dismissCookieBanner(page);
    await waitForPageReady(page, hashSelector);
    await page.screenshot({ path: out, fullPage: false });
    await copyFile(out, path.join(assetsDir, name));
    console.log("OK", name, url, dismissed ? "(cookies dismissed)" : "(cookies hidden)");
    ok += 1;
  } catch (err) {
    console.error("FAIL", url, err.message);
  }
}

await browser.close();
if (!ok) process.exit(1);
console.log(`Captured ${ok} desktop screenshots`);
