# No AIO: guía de marca

## Nombre

**No AIO**: siempre con esa capitalización y un espacio. "AIO" es la sigla de *AI Overview*. Es corto, se lee igual en cualquier idioma y dice exactamente lo que hace.

- Tagline (EN): **Google search, minus the AI summary.**
- Tagline (ES): **Google, sin el resumen de IA.**
- Firma: *Made by Oniria · Hecho por Oniria*

## Ícono

`branding/icon.svg` es la fuente única. Los PNG se generan con `npm run icons`.

Una lupa (búsqueda) con el destello de IA adentro, tachado. Usa la paleta propia y **nunca** los colores ni el logo de Google, para no dar a entender que es un producto oficial.

## Paleta

| Rol | Hex | Uso |
|---|---|---|
| Ink | `#0F172A` | Fondo de marca, encabezado del popup |
| Paper | `#F8FAFC` | Texto sobre Ink, lupa |
| Violet | `#8B5CF6` / `#A78BFA` | Acento, destello de IA, toggles |
| Rose | `#F43F5E` | Tachado (solo en el ícono) |
| Muted | `#64748B` | Texto secundario |

## Tipografía

Inter (o la fuente del sistema). Titulares en 800 con tracking negativo y texto en 400.

## Voz

Directa, breve y sin tono anti-Google. Decimos qué hace la extensión, no por qué la IA es mala. Siempre "No afiliado a Google".

## Assets de la tienda

`python3 scripts/render-store.py` regenera todas las capturas y los promo tiles en `store/assets/`, con los textos de `COPY` en ese script.
