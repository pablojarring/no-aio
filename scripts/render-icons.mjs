// Renderiza branding/icon.svg a PNG con Chrome headless.
// Uso: CHROME=/ruta/a/chrome node scripts/render-icons.mjs
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const chrome = process.env.CHROME || "google-chrome";
const svg = readFileSync(new URL("../branding/icon.svg", import.meta.url), "utf8");
const dir = mkdtempSync(join(tmpdir(), "noaio-"));

function render(size, padding, out) {
  const inner = size - padding * 2;
  const html = `<html><body style="margin:0;background:transparent">
    <div style="width:${size}px;height:${size}px;display:grid;place-items:center">
      <div style="width:${inner}px;height:${inner}px">${svg.replace("<svg ", '<svg width="100%" height="100%" ')}</div>
    </div></body></html>`;
  const file = join(dir, `i${size}.html`);
  writeFileSync(file, html);
  execFileSync(chrome, [
    "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
    "--default-background-color=00000000", `--window-size=${size},${size}`,
    `--screenshot=${new URL(out, import.meta.url).pathname}`, `file://${file}`,
  ], { stdio: "ignore" });
}

for (const s of [16, 32, 48, 128]) render(s, 0, `../icons/${s}.png`);
// Ícono de la tienda: 128x128 con 16 px de margen transparente (96x96 de arte).
render(128, 16, "../store/assets/store-icon-128.png");
console.log("íconos generados");
