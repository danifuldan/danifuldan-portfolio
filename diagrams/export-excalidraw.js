// Open excalidraw.com in headless Chrome, paste a .excalidraw file's elements
// via a synthetic clipboard event, zoom to fit, and screenshot the canvas.
// Usage: node render-excalidraw.js <file.excalidraw> <out.png>
const { chromium } = require("playwright");
const fs = require("fs");

(async () => {
  const [file, out] = process.argv.slice(2);
  const data = JSON.parse(fs.readFileSync(file, "utf8"));
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  page.on("pageerror", (e) => console.log("pageerror:", e.message));
  // Excalidraw prefers the File System Access API in Chrome, which Playwright
  // can't intercept; removing it forces the classic <input type=file> path.
  await page.addInitScript(() => {
    delete window.showOpenFilePicker;
    delete window.showSaveFilePicker;
  });
  await page.goto("https://excalidraw.com/", { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForSelector("canvas", { timeout: 30000 });
  // Close any welcome/modal overlay with Escape, then click the canvas to focus.
  await page.keyboard.press("Escape");
  await page.mouse.click(800, 500);

  // Load through the real "Open" file dialog, the same path the user takes.
  const [chooser] = await Promise.all([
    page.waitForEvent("filechooser", { timeout: 15000 }),
    page.getByText("Open", { exact: true }).first().click(),
  ]);
  await chooser.setFiles(file);
  await page.waitForTimeout(1500);
  // Deselect, then zoom to fit (Shift+1).
  await page.keyboard.press("Escape");
  await page.keyboard.press("Shift+1");
  await page.waitForTimeout(800);

  // Count elements Excalidraw now holds, via its exposed API if present.
  const count = await page.evaluate(() => {
    try {
      const api = window.__EXCALIDRAW_API__ || null;
      return api ? api.getSceneElements().length : -1;
    } catch (e) { return -2; }
  });
  console.log("pasted elements expected:", data.elements.length, "scene count (if api exposed):", count);

  await page.screenshot({ path: out });
  console.log("wrote", out);

  // Optional third arg: export a PNG through Excalidraw's own export dialog.
  const pngOut = process.argv[4];
  if (pngOut) {
    await page.keyboard.press("Escape");
    await page.keyboard.press("Meta+Shift+E"); // Export image dialog
    const dialog = page.locator(".Modal, [role=dialog]").first();
    await dialog.waitFor({ timeout: 10000 });
    // Scale 2x, background on (default). Buttons are labelled by their text.
    const twoX = dialog.getByText(/^\s*2\s*[x×]\s*$/).first();
    console.log("2x control found:", await twoX.count());
    if (await twoX.count()) await twoX.click();
    const [download] = await Promise.all([
      page.waitForEvent("download", { timeout: 20000 }),
      dialog.getByRole("button", { name: /PNG/i }).first().click(),
    ]);
    await download.saveAs(pngOut);
    console.log("exported", pngOut);
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
