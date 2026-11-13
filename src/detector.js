// Lógica de detección del AI Overview (AIO). Sin dependencias del navegador
// más allá del DOM estándar, para poder testearla con jsdom.
(function (root) {
  "use strict";

  // Títulos visibles del bloque AIO según el idioma de la interfaz de Google.
  // Verificados en google.com (nov 2026): en, es ("visión general creada por ia"),
  // de, ja, ru, hi. El resto viene de traducciones conocidas.
  // Si en tu idioma no se oculta, agrega aquí el texto exacto del título.
  const AIO_LABELS = [
    "ai overview",
    "ai overviews",
    "visión general creada por ia",
    "vista creada con ia",
    "resumen creado con ia",
    "resumen de ia",
    "visão geral criada por ia",
    "visão geral de ia",
    "aperçu ia",
    "aperçu généré par l'ia",
    "übersicht mit ki",
    "ki-übersicht",
    "panoramica ai",
    "panoramica creata con l'ai",
    "ai による概要",
    "ai जवाब",
    "ai 摘要",
    "ai 개요",
    "обзор от ии",
  ];

  // Zonas que NO se deben ocultar nunca: resultados orgánicos y panel lateral.
  // Desde el título del AIO subimos hasta el ancestro más alto que no las
  // contenga. (Google envuelve todo en divs con display:contents, así que
  // "subir hasta el hijo de #rcnt" taparía la página entera.)
  const PROTECTED = "#rso, #center_col, #rhs, #search";

  const HIDDEN_CLASS = "noaio-hidden";

  function normalize(text) {
    return (text || "").replace(/\s+/g, " ").trim().toLowerCase();
  }

  function isAioLabel(text) {
    return AIO_LABELS.includes(normalize(text));
  }

  function containsProtected(el) {
    return el.matches(PROTECTED) || !!el.querySelector(PROTECTED);
  }

  function topBlock(el) {
    let node = el;
    while (
      node.parentElement &&
      node.parentElement !== el.ownerDocument.body &&
      !containsProtected(node.parentElement)
    ) {
      node = node.parentElement;
    }
    return node;
  }

  function findAioBlocks(doc) {
    const blocks = new Set();
    const headings = doc.querySelectorAll('h1, h2, h3, [role="heading"]');
    for (const h of headings) {
      if (!isAioLabel(h.textContent)) continue;
      if (containsProtected(h)) continue;
      blocks.add(topBlock(h));
    }
    return [...blocks];
  }

  // Pestaña / botón "Modo IA" (udm=50).
  function findAiModeEntries(doc) {
    const out = new Set();
    for (const a of doc.querySelectorAll('a[href*="udm=50"]')) {
      out.add(a.closest('[role="listitem"]') || a);
    }
    return [...out];
  }

  root.NoAIO = { AIO_LABELS, HIDDEN_CLASS, isAioLabel, findAioBlocks, findAiModeEntries };
})(typeof globalThis !== "undefined" ? globalThis : this);
