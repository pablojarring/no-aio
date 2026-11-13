# Checklist de publicación

Todo lo que se puede preparar ya está en el repo. Aquí quedan solo los pasos que tienes que hacer tú, en orden.

## 1. GitHub (≈10 min)

- [ ] Crea el repo **público** `pablojarring/no-aio`. Si usas otro usuario, reemplaza `pablojarring` en todo el repo con buscar y reemplazar.
- [ ] `git remote add origin git@github.com:pablojarring/no-aio.git && git push -u origin main`
- [ ] **Settings → Pages** → Source: *Deploy from a branch* → `main` / `/docs`
- [ ] Revisa que la página abra: `https://pablojarring.github.io/no-aio/privacy/`
- [ ] **Settings → Security** → activa *Private vulnerability reporting*
- [ ] *About* (rueda dentada): descripción, website = la URL de Pages, topics: `chrome-extension`, `google-search`, `ai-overview`, `manifest-v3`, `privacy`
- [ ] Revisa que el workflow **CI** pase en verde

## 2. Cuenta de desarrollador de la Chrome Web Store (≈10 min)

- [ ] Entra a https://chrome.google.com/webstore/devconsole con la cuenta de Google con la que vas a publicar. Google sugiere usar un correo dedicado, porque **no se puede cambiar después**.
- [ ] Acepta el acuerdo y paga la cuota única de registro (**US$5**) con tarjeta habilitada para pagos internacionales.
- [ ] En *Account*: nombre público del publisher = **Oniria** y verifica el correo de contacto.
- [ ] Activa la verificación en 2 pasos en esa cuenta de Google. Es obligatoria para publicar.

## 3. Subir la extensión

- [ ] `npm ci && npm test && npm run zip` (o descarga el `no-aio.zip` del último workflow de CI)
- [ ] Dashboard → **New item** → sube `no-aio.zip`

## 4. Completar la ficha

Todo está en `store/`:

| Pestaña del dashboard | Archivo |
|---|---|
| Store listing (textos, categoría, URLs) | `store/LISTING.md` |
| Store listing (imágenes) | `store/assets/` |
| Privacy practices | `store/PRIVACY-TAB.md` |
| Distribution | Public, todas las regiones, gratis |

- [ ] Idioma por defecto **English**. Agrega **Español** y sube las capturas `-es`.
- [ ] Botón **Submit for review**. Desmarca "publish automatically" si quieres elegir el momento.

## 5. Después de que la aprueben

- [ ] Copia la URL de la ficha en `README.md` (*Install*) y en `docs/index.html` (botón *Add to Chrome*)
- [ ] Haz el tag `v1.0.0` y push, para que el workflow publique el release
- [ ] *(Opcional)* Publícala en Firefox Add-ons y Edge Add-ons; el mismo código MV3 sirve casi sin cambios

## Notas para la revisión

- Como pide acceso a 187 dominios, la revisión puede tardar más de lo normal. Las justificaciones de `PRIVACY-TAB.md` explican por qué cada permiso es necesario.
- Si la rechazan por el modo Web (redirección), la opción rápida es quitar `rules/` y `declarative_net_request` del manifest y volver a enviarla solo con el modo Ocultar.
- No uses el logo ni los colores de Google en ningún asset. La ficha ya dice "Not affiliated with Google".
