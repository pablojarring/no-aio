// Genera manifest.json a partir de domains.txt (lista oficial de dominios de
// Google: https://www.google.com/supported_domains).
// Uso: node scripts/build-manifest.mjs
import { readFileSync, writeFileSync } from "node:fs";

const domains = readFileSync(new URL("../domains.txt", import.meta.url), "utf8")
  .split(/\s+/)
  .filter(Boolean);

const hosts = domains.map((d) => `https://www.${d}/*`);
const searchPages = domains.map((d) => `https://www.${d}/search*`);

const manifest = {
  manifest_version: 3,
  name: "No AIO – Oculta el AI Overview de Google",
  short_name: "No AIO",
  version: "1.0.0",
  description: "Oculta el AI Overview (y la pestaña Modo IA) de las búsquedas de Google, o fuerza el filtro Web (udm=14).",
  icons: { 16: "icons/16.png", 32: "icons/32.png", 48: "icons/48.png", 128: "icons/128.png" },
  action: { default_popup: "src/popup.html", default_title: "No AIO" },
  background: { service_worker: "src/background.js" },
  permissions: ["storage", "declarativeNetRequest"],
  host_permissions: hosts,
  declarative_net_request: {
    rule_resources: [{ id: "udm14", enabled: false, path: "rules/udm14.json" }],
  },
  content_scripts: [
    {
      matches: searchPages,
      js: ["src/detector.js", "src/content.js"],
      run_at: "document_start",
    },
  ],
};

writeFileSync(new URL("../manifest.json", import.meta.url), JSON.stringify(manifest, null, 2) + "\n");
console.log(`manifest.json generado con ${domains.length} dominios`);
