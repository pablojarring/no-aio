# No AIO: oculta el AI Overview de Google

Extensión de Chrome (Manifest V3) que quita de las búsquedas de Google el **AI Overview** ("Visión general creada por IA") y, si quieres, la pestaña **Modo IA**.

## ¿Por qué una extensión?

Google no tiene ninguna opción para desactivarlo. Su página de ayuda dice que AI Overviews es una función central de Search y que no se puede apagar. El toggle de Search Labs solo te saca de los experimentos, no quita el AIO. La única salida oficial es el filtro **Web** (`&udm=14`), y hay que elegirlo en cada búsqueda.

## Modos

| Modo | Qué hace | Pros / contras |
|---|---|---|
| **Ocultar** (por defecto) | Carga la búsqueda normal ("Todo") y esconde el bloque de IA en cuanto aparece | Conservas imágenes, videos, "Más preguntas" y el panel lateral. Si Google cambia el título del bloque, hay que actualizar la lista de textos. |
| **Web (udm=14)** | Redirige cada búsqueda al filtro Web, así Google ni genera el AIO | Más robusto y sin anuncios de shopping, pero solo muestra enlaces azules. La pestaña "Todo" te devuelve a Web. |

Las demás pestañas (Imágenes, Noticias, etc.) siguen funcionando en ambos modos.

## Instalación (modo desarrollador)

1. `npm install && npm run build` (genera `manifest.json`, que ya viene incluido)
2. Abre `chrome://extensions` y activa **Modo de desarrollador**
3. Haz clic en **Cargar descomprimida** y elige la carpeta del repo
4. Fija el ícono y elige el modo en el popup

## Cómo funciona

- **`src/detector.js`** busca los títulos (`h1–h3`, `role="heading"`) cuyo texto sea exactamente el del AIO en algún idioma (`AIO_LABELS`). Desde ahí sube hasta el ancestro más alto que **no** contenga los resultados (`#rso`, `#center_col`, `#rhs`) y oculta ese bloque. No depende de las clases ofuscadas de Google, que cambian seguido.
- **`src/content.js`** corre en `document_start` y usa un `MutationObserver`, porque Google carga el AIO por streaming después del HTML inicial.
- **`rules/udm14.json`** es un ruleset de `declarativeNetRequest`. La regla 1 deja pasar las URLs que ya tienen `udm`/`tbm` y la regla 2 agrega `udm=14` al resto. El service worker lo activa solo en el modo Web.
- **`domains.txt`** tiene los 187 dominios de [google.com/supported_domains](https://www.google.com/supported_domains). Los content scripts no aceptan comodines en el TLD, así que `scripts/build-manifest.mjs` genera los permisos a partir de esta lista.

## Si deja de funcionar

Google cambia el DOM con frecuencia. Si el AIO vuelve a aparecer:

1. Clic derecho sobre el título del bloque → Inspeccionar, y copia el texto exacto
2. Agrégalo en minúsculas a `AIO_LABELS` en `src/detector.js`
3. Agrega un caso en `test/detector.test.mjs` y corre `npm test`

Mientras tanto, el modo **Web** sigue funcionando porque no depende del DOM.

## Scripts

- `npm run build`: regenera `manifest.json`
- `npm test`: tests de detección con jsdom (incluye la estructura real de nov 2026)
- `npm run zip`: empaqueta para subir a la Chrome Web Store

## Privacidad

No recolecta ni envía datos. Solo guarda tus 3 preferencias en `chrome.storage.sync`.

## Licencia

MIT
