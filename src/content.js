// Content script: oculta el AI Overview y (opcional) la pestaña "Modo IA".
(function () {
  "use strict";
  const { HIDDEN_CLASS, findAioBlocks, findAiModeEntries } = globalThis.NoAIO;

  const DEFAULTS = { enabled: true, hideAiMode: true, mode: "hide" };
  let settings = { ...DEFAULTS };
  let scheduled = false;

  // Estilo inyectado lo antes posible (document_start).
  const style = document.createElement("style");
  style.textContent = `.${HIDDEN_CLASS}{display:none !important}`;
  (document.head || document.documentElement).appendChild(style);

  function scan() {
    scheduled = false;
    if (!settings.enabled) return;
    for (const el of findAioBlocks(document)) el.classList.add(HIDDEN_CLASS);
    if (settings.hideAiMode) {
      for (const el of findAiModeEntries(document)) el.classList.add(HIDDEN_CLASS);
    }
  }

  function unhideAll() {
    for (const el of document.querySelectorAll("." + HIDDEN_CLASS)) {
      el.classList.remove(HIDDEN_CLASS);
    }
  }

  function schedule() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(scan);
  }

  // Google carga el AIO de forma asíncrona (streaming), así que observamos el DOM.
  new MutationObserver(schedule).observe(document.documentElement, {
    childList: true,
    subtree: true,
  });

  chrome.storage.sync.get(DEFAULTS, (s) => {
    settings = s;
    schedule();
  });

  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== "sync") return;
    for (const [k, { newValue }] of Object.entries(changes)) settings[k] = newValue;
    unhideAll();
    schedule();
  });
})();
