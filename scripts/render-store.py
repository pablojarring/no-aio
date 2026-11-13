"""Genera los assets de la Chrome Web Store (capturas y promo tiles) en ES y EN.

Uso: python3 scripts/render-store.py   (requiere Google Chrome; CHROME=/ruta opcional)
Salida: store/assets/
"""
import os, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "store" / "src", ROOT / "store" / "assets"
CHROME = os.environ.get("CHROME", "google-chrome")
ICON = (ROOT / "branding" / "icon.svg").read_text().replace("<svg ", '<svg width="100%" height="100%" ')
POPUP_CSS = (ROOT / "src" / "popup.css").as_uri()

COPY = {
    "es": {
        "s1_h": "Google, sin el resumen de IA.",
        "s1_p": "Tus resultados de siempre, otra vez arriba de todo.",
        "s2_h": "Recupera la parte de arriba de la página.",
        "before": "Antes", "after": "Con No AIO",
        "s3_h": "Dos modos. Un clic.",
        "b1_t": "Ocultar", "b1_d": "Búsqueda normal: solo desaparece el bloque de IA y la pestaña Modo IA.",
        "b2_t": "Web (udm=14)", "b2_d": "Abre siempre el filtro Web de Google: el resumen ni siquiera se genera.",
        "b3_t": "Open source y sin rastreo", "b3_d": "Licencia MIT. No recolecta ni envía ningún dato.",
        "tag": "Google, sin el resumen de IA",
        "pop": {"state": "Activada · Ocultar", "mode": "Modo", "hide": "Ocultar", "hide_d": "Búsqueda normal, solo se esconde el bloque de IA.",
                "web": "Web (udm=14)", "web_d": "Abre siempre el filtro Web: solo enlaces, sin IA ni bloques de compras.",
                "aimode": "Ocultar la pestaña “Modo IA”", "foot": "Open source · Sin rastreo"},
    },
    "en": {
        "s1_h": "Google search, minus the AI summary.",
        "s1_p": "Your regular results, back at the top of the page.",
        "s2_h": "Take back the top of the page.",
        "before": "Before", "after": "With No AIO",
        "s3_h": "Two modes. One click.",
        "b1_t": "Hide", "b1_d": "Normal search: only the AI block and the AI Mode tab disappear.",
        "b2_t": "Web (udm=14)", "b2_d": "Always open Google's Web filter: the summary is never generated.",
        "b3_t": "Open source, no tracking", "b3_d": "MIT licensed. Collects and sends no data at all.",
        "tag": "Google search, minus the AI summary",
        "pop": {"state": "On · Hide", "mode": "Mode", "hide": "Hide", "hide_d": "Normal search, only the AI block is hidden.",
                "web": "Web (udm=14)", "web_d": "Always open the Web filter: plain links, no AI, no shopping blocks.",
                "aimode": "Hide the “AI Mode” tab", "foot": "Open source · No tracking"},
    },
}

BASE_CSS = """
*{box-sizing:border-box;margin:0}
body{font-family:Inter,system-ui,sans-serif;color:#f8fafc;background:#0f172a;overflow:hidden;
 background-image:radial-gradient(circle at 85% 10%,rgba(139,92,246,.35),transparent 45%),radial-gradient(circle at 0% 100%,rgba(244,63,94,.18),transparent 40%)}
.logo{display:flex;align-items:center;gap:12px;font-weight:700;font-size:22px}
.logo i{width:40px;height:40px;display:block}
h1{font-size:46px;line-height:1.1;letter-spacing:-1px;font-weight:800}
p.sub{font-size:21px;color:#cbd5e1;margin-top:10px}
.frame{border-radius:14px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.12);background:#fff}
.frame .bar{height:28px;background:#e2e8f0;display:flex;gap:7px;align-items:center;padding-left:12px}
.frame .bar b{width:11px;height:11px;border-radius:50%;background:#cbd5e1;display:block}
.frame img{display:block;width:100%}
"""

def logo():
    return f'<div class="logo"><i>{ICON}</i>No AIO</div>'

def frame(img, extra=""):
    return f'<div class="frame" {extra}><div class="bar"><b></b><b></b><b></b></div><img src="{(SRC/img).as_uri()}"></div>'

def popup(c):
    p = c["pop"]
    return f"""<div style="width:300px;border-radius:14px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.5);background:#fff;color:#0f172a;font:13px/1.4 Inter,system-ui,sans-serif">
<header><i style="width:32px;height:32px;display:block">{ICON}</i><div class="brand"><strong>No AIO</strong><span class="state">{p['state']}</span></div>
<label class="switch"><input type="checkbox" checked><span></span></label></header>
<fieldset><legend>{p['mode']}</legend>
<label class="opt"><input type="radio" name="m" checked><span><b>{p['hide']}</b><small>{p['hide_d']}</small></span></label>
<label class="opt"><input type="radio" name="m"><span><b>{p['web']}</b><small>{p['web_d']}</small></span></label></fieldset>
<label class="row"><span>{p['aimode']}</span><span class="switch small"><input type="checkbox" checked><span></span></span></label>
<footer><a>{p['foot']}</a><span>v1.0.0</span></footer></div>"""

def s1(c):
    return f"""<div style="padding:56px 90px 0">{logo()}<h1 style="margin-top:34px">{c['s1_h']}</h1><p class="sub">{c['s1_p']}</p>
<div style="margin-top:40px">{frame('after-wide.png')}</div></div>"""

def s2(c):
    lab = 'style="font-size:15px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;color:{}"'
    col = lambda t, img, color: f'<div style="flex:1"><div {lab.format(color)}>{t}</div>{frame(img)}</div>'
    return f"""<div style="padding:56px 90px 0">{logo()}<h1 style="margin-top:34px">{c['s2_h']}</h1>
<div style="display:flex;gap:44px;margin-top:40px">{col(c['before'],'before-col.png','#fda4af')}{col(c['after'],'after-col.png','#c4b5fd')}</div></div>"""

def s3(c):
    item = lambda t, d: f'<div style="margin-bottom:30px"><div style="font-size:24px;font-weight:700;color:#c4b5fd">{t}</div><div style="font-size:19px;color:#cbd5e1;margin-top:6px;line-height:1.4">{d}</div></div>'
    return f"""<div style="display:flex;height:800px;align-items:center;gap:80px;padding:0 110px">
<div style="flex:1">{logo()}<h1 style="margin:34px 0 40px">{c['s3_h']}</h1>{item(c['b1_t'],c['b1_d'])}{item(c['b2_t'],c['b2_d'])}{item(c['b3_t'],c['b3_d'])}</div>
<div style="transform:scale(1.35);transform-origin:center;margin-right:50px">{popup(c)}</div></div>"""

def small_tile(c):
    return f"""<div style="height:280px;display:flex;flex-direction:column;justify-content:center;padding:0 40px">
<i style="width:84px;height:84px;display:block">{ICON}</i><div style="font-size:40px;font-weight:800;margin-top:18px;letter-spacing:-1px">No AIO</div>
<div style="font-size:19px;color:#cbd5e1;margin-top:4px">{c['tag']}</div></div>"""

def marquee(c):
    return f"""<div style="display:flex;height:560px;align-items:center;padding-left:90px;gap:60px">
<div style="width:520px;flex:none"><i style="width:96px;height:96px;display:block">{ICON}</i><div style="font-size:64px;font-weight:800;margin-top:22px;letter-spacing:-2px">No AIO</div>
<div style="font-size:28px;color:#cbd5e1;margin-top:8px;line-height:1.25">{c['tag']}</div></div>
<div style="width:900px;flex:none;margin-top:120px">{frame('after-wide.png')}</div></div>"""

def render(name, body, w, h):
    html = SRC / f"{name}.html"
    html.write_text(f"<!doctype html><meta charset=utf-8><link rel=stylesheet href='{POPUP_CSS}'><style>{BASE_CSS}</style><body style='width:{w}px;height:{h}px'>{body}</body>")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", f"--screenshot={OUT / (name + '.png')}", html.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    html.unlink()

OUT.mkdir(parents=True, exist_ok=True)
for lang, c in COPY.items():
    render(f"screenshot-1-{lang}", s1(c), 1280, 800)
    render(f"screenshot-2-{lang}", s2(c), 1280, 800)
    render(f"screenshot-3-{lang}", s3(c), 1280, 800)
    render(f"promo-small-440x280-{lang}", small_tile(c), 440, 280)
    render(f"promo-marquee-1400x560-{lang}", marquee(c), 1400, 560)
print("assets generados en", OUT)
