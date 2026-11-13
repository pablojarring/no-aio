# Contribuir a No AIO

¡Gracias por ayudar! *(English below.)*

## Lo que más ayuda

1. **Un idioma nuevo o un título que cambió.** Google pone un título distinto al bloque de IA en cada idioma. Si en el tuyo no se oculta:
   - Clic derecho sobre el título del bloque → *Inspeccionar*, y copia el texto exacto.
   - Agrégalo en minúsculas a `AIO_LABELS` en `src/detector.js`.
   - Agrega un caso en `test/detector.test.mjs`.
2. **Traducir el popup.** Copia `_locales/en/messages.json` a `_locales/<código>/messages.json` y traduce.
3. **Reportar cuando Google cambie el DOM**, con la plantilla "El resumen de IA sigue apareciendo".

## Desarrollo

```bash
npm install
npm test          # tests de detección con jsdom
npm run build     # regenera manifest.json desde domains.txt
npm run zip       # paquete para la tienda
```

Carga la carpeta en `chrome://extensions` → *Modo de desarrollador* → *Cargar descomprimida*. Después de cambiar algo, pulsa ↻ en la tarjeta de la extensión.

## Reglas del proyecto

- **Cero datos:** nada de analytics, peticiones de red ni código remoto. Un PR que agregue algo de eso no se acepta.
- **Permisos mínimos:** no agregues permisos nuevos sin abrir un issue primero.
- Detecta por **texto y estructura**, no por clases ofuscadas de Google (`.bzXtMb` cambia sin aviso).
- Nunca ocultes un contenedor que tenga `#rso`, `#center_col` o `#rhs`.

## Publicar una versión (mantenedores)

1. Sube la versión en `package.json` y agrega la entrada en `CHANGELOG.md`
2. `npm run build`, commit y `git tag vX.Y.Z && git push --tags`
3. El workflow **Release** crea el release de GitHub con `no-aio.zip`
4. Sube ese zip en el Developer Dashboard de la Chrome Web Store

---

## Contributing (English)

The most useful contributions are AI Overview titles in new languages (`AIO_LABELS` in `src/detector.js` plus a test), popup translations (`_locales/`), and reports when Google changes its markup. Run `npm install && npm test` before opening a PR. The extension must stay zero-data and minimal-permission.
