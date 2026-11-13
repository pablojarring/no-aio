// Tests de la detección con un DOM simulado de la página de resultados.
// Uso: npm test
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";
import { JSDOM } from "jsdom";

function load(html) {
  const dom = new JSDOM(html, { runScripts: "outside-only" });
  const ctx = dom.getInternalVMContext();
  vm.runInContext(readFileSync(new URL("../src/detector.js", import.meta.url), "utf8"), ctx);
  return { doc: dom.window.document, NoAIO: dom.window.NoAIO };
}

const PAGE = (aio) => `
<body><div id="main"><div id="rcnt"><div id="center_col">
  ${aio}
  <div id="rso">
    <div class="g" id="r1"><h3>Resultado orgánico 1</h3></div>
    <div class="g" id="r2"><h3>Resultado orgánico 2</h3></div>
  </div>
</div></div></div>
<div role="list"><div role="listitem" id="aimode"><a href="/search?q=x&udm=50">Modo IA</a></div></div>
</body>`;

test("oculta el AIO en español fuera de #rso", () => {
  const { doc, NoAIO } = load(PAGE(`<div id="aio"><div><h1>Vista creada con IA</h1><p>bla</p></div></div>`));
  const blocks = NoAIO.findAioBlocks(doc);
  assert.deepEqual(Array.from(blocks, (b) => b.id), ["aio"]);
});

test("oculta el AIO en inglés dentro de #rso sin tocar resultados", () => {
  const html = PAGE("").replace('<div id="rso">', '<div id="rso"><div id="aio"><div role="heading">AI Overview</div></div>');
  const { doc, NoAIO } = load(html);
  assert.deepEqual(Array.from(NoAIO.findAioBlocks(doc), (x) => x.id), ["aio"]);
});

test("no oculta nada si no hay AIO", () => {
  const { doc, NoAIO } = load(PAGE(""));
  assert.equal(NoAIO.findAioBlocks(doc).length, 0);
});

test("no confunde un resultado que menciona 'AI Overview' en su título largo", () => {
  const { doc, NoAIO } = load(PAGE(`<div id="x"><h3>How to turn off AI Overview in Google</h3></div>`));
  assert.equal(NoAIO.findAioBlocks(doc).length, 0);
});

test("detecta la pestaña Modo IA (udm=50)", () => {
  const { doc, NoAIO } = load(PAGE(""));
  assert.deepEqual(Array.from(NoAIO.findAiModeEntries(doc), (x) => x.id), ["aimode"]);
});

test("estructura real (nov 2026): wrapper display:contents con AIO y resultados juntos", () => {
  const html = `<body><div id="main"><div id="cnt"><div id="rcnt">
    <div style="display:contents">
      <div class="bzXtMb M8OgIe" id="aio"><div><section><div role="heading">Visión general creada por IA</div><p>...</p></section></div></div>
      <div><div id="center_col"><div id="rso"><div id="r1"><h3>Fotosíntesis - Wikipedia</h3></div></div></div></div>
    </div>
    <div id="rhs"><h2>Panel</h2></div>
  </div></div></div></body>`;
  const { doc, NoAIO } = load(html);
  assert.deepEqual(Array.from(NoAIO.findAioBlocks(doc), (b) => b.id), ["aio"]);
});

test("detecta los títulos verificados en vivo (en, es, de, ru, ja, hi)", () => {
  const { NoAIO } = load("<body></body>");
  for (const t of ["AI Overview", "Visión general creada por IA", "Übersicht mit KI", "Обзор от ИИ", "AI による概要", "AI जवाब"]) {
    assert.ok(NoAIO.isAioLabel(t), t);
  }
});
