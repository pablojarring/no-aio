"""Genera los assets de la Chrome Web Store en 6 idiomas (en, es, de, ru, ja, hi).

Sistema visual "Sources first":
  - Grilla fija con márgenes de 80 px, eyebrow numerado (01–04) y pie con marca y contador.
  - Motivo: el tachado rosa del ícono cruza el título REAL del bloque de IA en cada idioma.
  - Color por slide: ink → paper → violet → ink.

Uso: python3 scripts/render-store.py   (requiere Google Chrome; CHROME=/ruta opcional)
Entrada: store/src/{before,after}-{wide,col}-<lang>.png (capturas reales), branding/icon.svg,
         _locales/<lang>/messages.json (textos del popup), store/fonts/
Salida: store/assets/
"""
import json, os, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT, FONTS = ROOT / "store" / "src", ROOT / "store" / "assets", ROOT / "store" / "fonts"
CHROME = os.environ.get("CHROME", "google-chrome")
ICON = (ROOT / "branding" / "icon.svg").read_text().replace("<svg ", '<svg width="100%" height="100%" ')
POPUP_CSS = (ROOT / "src" / "popup.css").as_uri()
REPO = "github.com/pablojarring/no-aio"

INK, PAPER, VIOLET, VIOLET_D, VIOLET_L, ROSE, SLATE = "#0F172A", "#F8FAFC", "#7C3AED", "#5B21B6", "#C4B5FD", "#F43F5E", "#64748B"

# Fuentes por sistema de escritura
FONT = {
    "latin": ("Brico, 'Inter Display', Inter, sans-serif", "Inter, sans-serif", 800),
    "cyr":   ("'Inter Display', Inter, sans-serif", "Inter, sans-serif", 800),
    "ja":    ("'Noto Sans CJK JP', sans-serif", "'Noto Sans CJK JP', sans-serif", 900),
    "hi":    ("Deva, sans-serif", "Deva, Inter, sans-serif", 800),
}

# label = título real del bloque de IA en Google (verificado en google.com, nov 2026)
COPY = {
    "en": dict(script="latin", label="AI Overview", hscale=1.0,
        e1="Chrome extension for Google Search", h1="Sources first.",
        p1="AI shouldn't be the first answer you read. No AIO hides Google's AI Overview so real results lead again.",
        chip1="hidden on every search",
        e2="Before / after", h2="Same search.<br>Straight to the sources.", before="Before", after="With No AIO",
        e3="Two modes", h3="Your search,<br>your rules.",
        m1t="Hide", m1d="Keep the full results page: images, videos, People also ask. Only the AI block goes.",
        m2t="Web mode", m2d="Every search opens in Google's Web filter. The AI summary is never generated.",
        n3="Plus: hide the AI Mode tab.",
        e4="Open source", h4="Zero data.<br>Fully open.",
        items=["No analytics or tracking", "No ads, no remote code", "Runs only on Google Search", "MIT license, on GitHub"],
        tag="Sources first."),
    "es": dict(script="latin", label="Visión general creada por IA", hscale=0.92,
        e1="Extensión de Chrome para Google", h1="Primero, las fuentes.",
        p1="La IA no debería ser lo primero que lees. No AIO oculta el resumen de IA de Google para que los resultados reales vuelvan a estar arriba.",
        chip1="oculto en cada búsqueda",
        e2="Antes / después", h2="La misma búsqueda.<br>Directo a las fuentes.", before="Antes", after="Con No AIO",
        e3="Dos modos", h3="Tu búsqueda,<br>tus reglas.",
        m1t="Ocultar", m1d="Conserva toda la página: imágenes, videos, “Más preguntas”. Solo se va el bloque de IA.",
        m2t="Modo Web", m2d="Cada búsqueda se abre en el filtro Web de Google. El resumen de IA nunca se genera.",
        n3="Además: oculta la pestaña Modo IA.",
        e4="Open source", h4="Cero datos.<br>Totalmente abierto.",
        items=["Sin analytics ni rastreo", "Sin anuncios ni código remoto", "Solo actúa en Google Search", "Licencia MIT, en GitHub"],
        tag="Primero, las fuentes."),
    "de": dict(script="latin", label="Übersicht mit KI", hscale=0.92,
        e1="Chrome-Erweiterung für die Google-Suche", h1="Quellen zuerst.",
        p1="KI sollte nicht das Erste sein, was du liest. No AIO blendet Googles KI-Übersicht aus, damit echte Ergebnisse wieder oben stehen.",
        chip1="bei jeder Suche ausgeblendet",
        e2="Vorher / nachher", h2="Gleiche Suche.<br>Direkt zu den Quellen.", before="Vorher", after="Mit No AIO",
        e3="Zwei Modi", h3="Deine Suche,<br>deine Regeln.",
        m1t="Ausblenden", m1d="Die ganze Ergebnisseite bleibt: Bilder, Videos, „Weitere Fragen“. Nur der KI-Block verschwindet.",
        m2t="Web-Modus", m2d="Jede Suche öffnet Googles Web-Filter. Die KI-Zusammenfassung wird gar nicht erst erzeugt.",
        n3="Außerdem: KI-Modus-Tab ausblenden.",
        e4="Open Source", h4="Keine Daten.<br>Komplett offen.",
        items=["Kein Tracking, keine Analytics", "Keine Werbung, kein Remote-Code", "Läuft nur auf der Google-Suche", "MIT-Lizenz, auf GitHub"],
        tag="Quellen zuerst."),
    "ru": dict(script="cyr", label="Обзор от ИИ", hscale=0.9,
        e1="Расширение Chrome для Google Поиска", h1="Сначала источники.",
        p1="ИИ не должен быть первым, что вы читаете. No AIO скрывает «Обзор от ИИ» в Google, и настоящие результаты снова наверху.",
        chip1="скрыт в каждом поиске",
        e2="До / после", h2="Тот же поиск.<br>Сразу к источникам.", before="До", after="С No AIO",
        e3="Два режима", h3="Ваш поиск —<br>ваши правила.",
        m1t="Скрыть", m1d="Вся страница результатов остаётся: картинки, видео, «Вопросы по теме». Пропадает только блок ИИ.",
        m2t="Режим «Веб»", m2d="Каждый поиск открывается в веб-фильтре Google. Сводка ИИ даже не создаётся.",
        n3="А ещё: скрыть вкладку «Режим ИИ».",
        e4="Открытый код", h4="Ноль данных.<br>Полностью открыт.",
        items=["Без аналитики и слежки", "Без рекламы и удалённого кода", "Работает только в Google Поиске", "Лицензия MIT, на GitHub"],
        tag="Сначала источники."),
    "ja": dict(script="ja", label="AI による概要", hscale=0.82,
        e1="Google 検索のための Chrome 拡張機能", h1="まずは、<br>情報源から。",
        p1="最初に読むのは AI の要約じゃなくていい。No AIO は Google の「AI による概要」を非表示にして、本来の検索結果をいちばん上に戻します。",
        chip1="すべての検索で非表示",
        e2="使用前 / 使用後", h2="同じ検索で、<br>すぐ情報源へ。", before="使用前", after="No AIO 使用後",
        e3="2 つのモード", h3="あなたの検索は、<br>あなたのルールで。",
        m1t="非表示", m1d="画像・動画・「関連する質問」はそのまま。AI のブロックだけを消します。",
        m2t="ウェブモード", m2d="すべての検索を Google のウェブフィルタで開きます。AI の要約は生成されません。",
        n3="AI モードのタブも非表示にできます。",
        e4="オープンソース", h4="データ収集ゼロ。<br>完全オープン。",
        items=["分析・トラッキングなし", "広告なし、リモートコードなし", "Google 検索でのみ動作", "MIT ライセンス、GitHub で公開"],
        tag="まずは、情報源から。"),
    "hi": dict(script="hi", label="AI जवाब", hscale=0.9,
        e1="Google सर्च के लिए Chrome एक्सटेंशन", h1="पहले स्रोत।",
        p1="AI पहली चीज़ नहीं होनी चाहिए जो आप पढ़ें। No AIO, Google का AI जवाब छिपा देता है, ताकि असली नतीजे फिर से सबसे ऊपर हों।",
        chip1="हर सर्च में छिपा हुआ",
        e2="पहले / बाद में", h2="वही सर्च।<br>सीधे स्रोतों तक।", before="पहले", after="No AIO के साथ",
        e3="दो मोड", h3="आपकी सर्च,<br>आपके नियम।",
        m1t="छिपाएं", m1d="पूरा नतीजों वाला पेज बना रहता है: इमेज, वीडियो, “लोग यह भी जानना चाहते हैं”। सिर्फ़ AI वाला हिस्सा हटता है।",
        m2t="वेब मोड", m2d="हर सर्च Google के वेब फ़िल्टर में खुलती है। AI सारांश बनता ही नहीं।",
        n3="साथ ही: AI मोड टैब भी छिपाएं।",
        e4="ओपन सोर्स", h4="ज़ीरो डेटा।<br>पूरी तरह ओपन।",
        items=["कोई एनालिटिक्स या ट्रैकिंग नहीं", "कोई विज्ञापन या रिमोट कोड नहीं", "सिर्फ़ Google सर्च पर चलता है", "MIT लाइसेंस, GitHub पर"],
        tag="पहले स्रोत।"),
}

def base_css(c):
    head, body, w = FONT[c["script"]]
    return f"""
@font-face{{font-family:Brico;src:url('{(FONTS/'bricolage-grotesque-var.woff2').as_uri()}') format('woff2');font-weight:200 800}}
@font-face{{font-family:Deva;src:url('{(FONTS/'noto-sans-devanagari-var.woff2').as_uri()}') format('woff2');font-weight:100 900}}
*{{box-sizing:border-box;margin:0}}
body{{font-family:{body};color:{INK};overflow:hidden;position:relative;margin:0}}
.abs{{position:absolute}}
.h{{font-family:{head};font-weight:{w};letter-spacing:-.025em;line-height:1.02}}
.eyebrow{{font-family:Inter,{body};font-size:15px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;display:flex;gap:14px;align-items:center}}
.eyebrow b{{font-weight:700;color:{VIOLET}}}
.eyebrow i{{display:block;width:36px;height:2px;background:currentColor;opacity:.35}}
.foot{{font-family:Inter,{body};font-size:14px;font-weight:600;display:flex;align-items:center;gap:10px}}
.foot i{{display:block;width:26px;height:26px}}
.frame{{border-radius:14px;overflow:hidden;background:#fff;box-shadow:0 24px 60px rgba(15,23,42,.28),0 0 0 1px rgba(15,23,42,.08)}}
.frame .bar{{height:28px;background:#E2E8F0;display:flex;gap:7px;align-items:center;padding-left:12px}}
.frame .bar b{{width:10px;height:10px;border-radius:50%;background:#94A3B8;display:block}}
.frame img{{display:block;width:100%}}
.strike{{display:inline-flex;align-items:center;gap:10px;position:relative;padding:10px 18px;border-radius:999px;font-weight:600;white-space:nowrap}}
.strike::after{{content:"";position:absolute;left:10px;right:10px;top:50%;height:4px;background:{ROSE};border-radius:4px;transform:rotate(-6deg)}}
.pill{{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;font-weight:700;font-size:15px;white-space:nowrap}}
"""

SPARK = f'<svg width="20" height="20" viewBox="0 0 20 20"><path d="M10 1 C11 7 13 9 19 10 C13 11 11 13 10 19 C9 13 7 11 1 10 C7 9 9 7 10 1Z" fill="{VIOLET_L}"/></svg>'

def frame(img):
    return f'<div class="frame"><div class="bar"><b></b><b></b><b></b></div><img src="{(SRC/img).as_uri()}"></div>'

def chrome(c, n, dark):
    fg = "#fff" if dark else INK
    sub = "rgba(255,255,255,.6)" if dark else SLATE
    return f"""<div class="abs eyebrow" style="left:80px;top:64px;color:{sub}"><b style="color:{VIOLET_L if dark else VIOLET}">0{n}</b><i></i><span>{c['e'+str(n)]}</span></div>
<div class="abs foot" style="left:80px;bottom:44px;color:{fg}"><i>{ICON}</i>No AIO</div>
<div class="abs foot" style="right:80px;bottom:44px;color:{sub};font-weight:500">{REPO}</div>"""

def strike_label(c, dark=True, size=22):
    bg = "rgba(255,255,255,.08)" if dark else "#fff"
    border = "rgba(255,255,255,.18)" if dark else "#E2E8F0"
    color = "#fff" if dark else INK
    return f'<span class="strike" style="background:{bg};border:1.5px solid {border};color:{color};font-size:{size}px">{SPARK}{c["label"]}</span>'

def check(color):
    return f'<svg width="30" height="30" viewBox="0 0 30 30" style="flex:none"><circle cx="15" cy="15" r="14" fill="{color}"/><path d="M9 15.5 L13.3 19.8 L21.5 11" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def popup(lang):
    m = {k: v["message"] for k, v in json.load(open(ROOT / "_locales" / lang / "messages.json")).items()}
    return f"""<div style="width:300px;border-radius:14px;overflow:hidden;background:#fff;color:#0f172a;font-size:13px;line-height:1.4">
<header><i style="width:32px;height:32px;display:block">{ICON}</i><div class="brand"><strong>No AIO</strong><span class="state">{m['on']} · {m['modeHide']}</span></div>
<label class="switch"><input type="checkbox" checked><span></span></label></header>
<fieldset><legend>{m['mode']}</legend>
<label class="opt"><input type="radio" name="m" checked><span><b>{m['modeHide']}</b><small>{m['modeHideDesc']}</small></span></label>
<label class="opt"><input type="radio" name="m"><span><b>{m['modeWeb']}</b><small>{m['modeWebDesc']}</small></span></label></fieldset>
<label class="row"><span>{m['hideAiMode']}</span><span class="switch small"><input type="checkbox" checked><span></span></span></label>
<footer><a>{m['footer']}</a><span>v1.0.0</span></footer></div>"""

hs = lambda c, px: f"{round(px * c['hscale'])}px"

# 01 · Hero (ink)
def s1(c, lang):
    return f"""<div class="abs" style="inset:0;background:{INK}"></div>
<div class="abs" style="inset:0;background:radial-gradient(900px 600px at 95% 0%,rgba(124,58,237,.45),transparent 60%)"></div>
{chrome(c, 1, True)}
<h1 class="abs h" style="left:80px;top:128px;width:520px;font-size:{hs(c,88)};color:#fff">{c['h1']}</h1>
<p class="abs" style="left:80px;top:{330 if c['h1'].count('<br>') or len(c['h1'])>14 else 300}px;width:470px;font-size:20px;line-height:1.5;color:#CBD5E1">{c['p1']}</p>
<div class="abs" style="left:80px;top:540px;display:flex;flex-direction:column;align-items:flex-start;gap:12px">{strike_label(c)}<span style="color:#94A3B8;font-size:16px;font-weight:500;padding-left:6px">{c['chip1']}</span></div>
<div class="abs" style="left:640px;top:128px;width:760px">{frame(f'after-wide-{lang}.png')}</div>"""

# 02 · Antes / después (paper)
def s2(c, lang):
    tag = lambda t, bg, fg: f'<div class="pill" style="background:{bg};color:{fg};margin-bottom:14px">{t}</div>'
    hatch = f"""<div class="abs" style="left:0;right:0;top:152px;bottom:0;background:repeating-linear-gradient(-45deg,rgba(244,63,94,.16) 0 10px,rgba(244,63,94,.05) 10px 20px);border-top:3px solid {ROSE}"></div>
<div class="abs" style="right:16px;bottom:16px;box-shadow:0 8px 24px rgba(15,23,42,.18);border-radius:999px">{strike_label(c, dark=False, size=17)}</div>"""
    return f"""<div class="abs" style="inset:0;background:{PAPER}"></div>
{chrome(c, 2, False)}
<h1 class="abs h" style="left:80px;top:112px;width:1120px;font-size:{hs(c,54)}">{c['h2']}</h1>
<div class="abs" style="left:80px;top:268px;width:540px">{tag(c['before'], '#FFE4E6', '#BE123C')}<div style="position:relative;height:380px;overflow:hidden;border-radius:14px">{frame(f'before-col-{lang}.png')}{hatch}</div></div>
<div class="abs" style="left:660px;top:268px;width:540px">{tag(c['after'], '#EDE9FE', VIOLET_D)}<div style="height:380px;overflow:hidden;border-radius:14px;box-shadow:0 0 0 3px {VIOLET}">{frame(f'after-col-{lang}.png')}</div></div>"""

# 03 · Modos (violet)
def s3(c, lang):
    card = lambda n, t, d, top: f"""<div class="abs" style="left:80px;top:{top}px;width:560px;display:flex;gap:20px;background:rgba(255,255,255,.1);border:1.5px solid rgba(255,255,255,.22);border-radius:18px;padding:24px 26px">
<div class="h" style="font-size:30px;color:{VIOLET_L};line-height:1">0{n}</div>
<div><div class="h" style="font-size:{hs(c,30)};color:#fff;margin-bottom:8px">{t}</div><div style="font-size:18px;line-height:1.5;color:#EDE9FE">{d}</div></div></div>"""
    return f"""<div class="abs" style="inset:0;background:linear-gradient(135deg,{VIOLET} 0%,{VIOLET_D} 100%)"></div>
{chrome(c, 3, True)}
<h1 class="abs h" style="left:80px;top:112px;width:620px;font-size:{hs(c,62)};color:#fff">{c['h3']}</h1>
{card(1, c['m1t'], c['m1d'], 300)}
{card(2, c['m2t'], c['m2d'], 470)}
<div class="abs" style="left:80px;top:650px;font-size:17px;font-weight:600;color:#fff;opacity:.85">{c['n3']}</div>
<div class="abs" style="left:770px;top:150px;transform:scale(1.3);transform-origin:top left;border-radius:14px;box-shadow:0 30px 70px rgba(15,23,42,.45)">{popup(lang)}</div>"""

# 04 · Open source (ink)
def s4(c, lang):
    items = "".join(f'<div style="display:flex;gap:14px;align-items:center;font-size:21px;font-weight:600;color:#fff">{check(VIOLET)}{t}</div>' for t in c["items"])
    code = f"""<div class="abs" style="left:700px;top:150px;width:500px;background:#020617;border:1.5px solid rgba(255,255,255,.12);border-radius:16px;overflow:hidden;font:16px/1.75 'DejaVu Sans Mono',monospace;color:#CBD5E1;box-shadow:0 30px 70px rgba(0,0,0,.4)">
<div style="padding:12px 18px;border-bottom:1px solid rgba(255,255,255,.08);color:#64748B;font-size:13px">src/detector.js</div>
<div style="padding:16px 20px">
<div><span style="color:{VIOLET_L}">const</span> AIO_LABELS = [</div>
<div>&nbsp;&nbsp;<span style="color:#86EFAC">"ai overview"</span>,</div>
<div>&nbsp;&nbsp;<span style="color:#86EFAC">"{c['label'].lower() if lang != 'en' else 'ai による概要'}"</span>, <span style="color:#475569">// …</span></div>
<div>];</div>
<div style="color:#475569;margin-top:8px">// no fetch(). no analytics. no remote code.</div>
</div></div>"""
    return f"""<div class="abs" style="inset:0;background:{INK}"></div>
<div class="abs" style="inset:0;background:radial-gradient(700px 500px at 0% 100%,rgba(124,58,237,.35),transparent 60%)"></div>
{chrome(c, 4, True)}
<h1 class="abs h" style="left:80px;top:128px;width:560px;font-size:{hs(c,76)};color:#fff">{c['h4']}</h1>
<div class="abs" style="left:80px;top:420px;display:grid;gap:22px">{items}</div>
{code}
<div class="abs" style="left:700px;top:430px;width:500px;display:flex;align-items:center;gap:14px;padding:20px 22px;border-radius:16px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.12)">
<svg width="32" height="32" viewBox="0 0 16 16" fill="#fff"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
<div style="color:#fff;font:600 19px Inter,sans-serif">{REPO}</div></div>"""

# Promo tiles: universales (sin texto de idioma salvo la marca).
LABELS = ["AI Overview", "Visión general creada por IA", "Übersicht mit KI", "Обзор от ИИ", "AI による概要", "AI जवाब"]
MULTI = "Inter, 'Noto Sans CJK JP', Deva, sans-serif"
UNI_CSS = f"""
.chip{{display:inline-flex;align-items:center;gap:8px;position:relative;padding:7px 14px;border-radius:999px;background:rgba(255,255,255,.07);
  border:1.5px solid rgba(255,255,255,.16);color:#E2E8F0;font:600 15px/1 {MULTI};white-space:nowrap}}
.chip::after{{content:"";position:absolute;left:8px;right:8px;top:50%;height:3px;background:{ROSE};border-radius:3px;transform:rotate(-5deg)}}
.glow{{background:radial-gradient(60% 90% at 100% 0%,rgba(124,58,237,.55),transparent 70%),radial-gradient(50% 70% at 0% 100%,rgba(124,58,237,.18),transparent 70%),{INK}}}
.grid{{background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:40px 40px}}
.word{{font-family:Brico,sans-serif;font-weight:800;letter-spacing:-.04em;color:#fff;line-height:.9}}
.sk{{background:#E2E8F0;border-radius:6px}}
"""
SPARK_SM = SPARK.replace('width="20" height="20"', 'width="14" height="14"')

def chips(labels, gap=10):
    return "".join(f'<span class="chip">{SPARK_SM}{t}</span>' for t in labels)

def serp(width):
    """Página de resultados abstracta: el bloque de IA colapsado y los resultados arriba."""
    result = lambda w1, w2: f"""<div style="display:flex;gap:12px;margin-bottom:20px">
<div style="width:22px;height:22px;border-radius:50%;background:#E2E8F0;flex:none"></div>
<div style="flex:1"><div class="sk" style="width:38%;height:8px;margin-bottom:8px"></div>
<div style="width:{w1}%;height:13px;border-radius:6px;background:{VIOLET};margin-bottom:9px"></div>
<div class="sk" style="width:96%;height:8px;margin-bottom:6px"></div><div class="sk" style="width:{w2}%;height:8px"></div></div></div>"""
    return f"""<div style="width:{width}px;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.45),0 0 0 1px rgba(255,255,255,.08)">
<div style="height:34px;background:#F1F5F9;display:flex;gap:8px;align-items:center;padding-left:16px">
<b style="width:11px;height:11px;border-radius:50%;background:#CBD5E1;display:block"></b><b style="width:11px;height:11px;border-radius:50%;background:#CBD5E1;display:block"></b><b style="width:11px;height:11px;border-radius:50%;background:#CBD5E1;display:block"></b></div>
<div style="padding:26px 32px 10px">
<div style="height:44px;border-radius:22px;border:1.5px solid #E2E8F0;display:flex;align-items:center;gap:12px;padding:0 18px;margin-bottom:20px;box-shadow:0 2px 8px rgba(15,23,42,.06)">
<svg width="18" height="18" viewBox="0 0 24 24"><circle cx="10" cy="10" r="7" fill="none" stroke="#94A3B8" stroke-width="2.6"/><line x1="15.5" y1="15.5" x2="21" y2="21" stroke="#94A3B8" stroke-width="2.6" stroke-linecap="round"/></svg>
<div class="sk" style="width:46%;height:9px"></div></div>
<div style="display:flex;gap:18px;margin-bottom:20px"><div style="width:34px;height:8px;border-radius:4px;background:{INK}"></div><div class="sk" style="width:42px;height:8px"></div><div class="sk" style="width:38px;height:8px"></div><div class="sk" style="width:46px;height:8px"></div></div>
<div style="position:relative;height:30px;border:2px dashed {ROSE};border-radius:12px;display:flex;align-items:center;gap:10px;padding:0 14px;margin-bottom:24px;background:rgba(244,63,94,.05)">
{SPARK_SM.replace(VIOLET_L, '#FDA4AF')}<div style="flex:1;height:3px;background:{ROSE};border-radius:3px;opacity:.7"></div></div>
{result(62, 70)}{result(54, 82)}{result(68, 60)}</div></div>"""

def serp_state(width, before):
    """Página de resultados abstracta en estado 'antes' (bloque de IA grande) o 'después'."""
    dots = "".join('<b style="width:10px;height:10px;border-radius:50%;background:#CBD5E1;display:block"></b>' for _ in range(3))
    result = lambda w1, w2: f"""<div style="display:flex;gap:12px;margin-bottom:18px">
<div style="width:20px;height:20px;border-radius:50%;background:#E2E8F0;flex:none"></div>
<div style="flex:1"><div class="sk" style="width:38%;height:7px;margin-bottom:7px"></div>
<div style="width:{w1}%;height:12px;border-radius:6px;background:{VIOLET};margin-bottom:8px"></div>
<div class="sk" style="width:96%;height:7px;margin-bottom:5px"></div><div class="sk" style="width:{w2}%;height:7px"></div></div></div>"""
    if before:
        lines = "".join(f'<div style="width:{w}%;height:8px;border-radius:4px;background:#DDD6FE;margin-bottom:9px"></div>' for w in (92, 86, 95, 70, 88, 93, 60))
        ai = f"""<div style="border-radius:14px;background:linear-gradient(180deg,#F5F3FF,#EDE9FE);padding:16px 18px;margin-bottom:22px">
<div style="display:flex;gap:8px;align-items:center;margin-bottom:14px">{SPARK_SM.replace(VIOLET_L, VIOLET)}<div style="width:90px;height:8px;border-radius:4px;background:#C4B5FD"></div></div>
<div style="display:flex;gap:8px;margin-bottom:14px">{''.join('<div style="flex:1;height:58px;border-radius:8px;background:#DDD6FE"></div>' for _ in range(4))}</div>
{lines}</div>"""
        results = result(60, 72)
    else:
        ai = f"""<div style="height:28px;border:2px dashed {ROSE};border-radius:12px;display:flex;align-items:center;gap:10px;padding:0 14px;margin-bottom:22px;background:rgba(244,63,94,.05)">
{SPARK_SM.replace(VIOLET_L, '#FDA4AF')}<div style="flex:1;height:3px;background:{ROSE};border-radius:3px;opacity:.7"></div></div>"""
        results = result(62, 70) + result(54, 82) + result(68, 60) + result(58, 76)
    return f"""<div style="width:{width}px;height:520px;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.45),0 0 0 1px rgba(255,255,255,.08)">
<div style="height:32px;background:#F1F5F9;display:flex;gap:8px;align-items:center;padding-left:16px">{dots}</div>
<div style="padding:22px 26px">
<div style="height:40px;border-radius:20px;border:1.5px solid #E2E8F0;display:flex;align-items:center;gap:12px;padding:0 16px;margin-bottom:16px">
<svg width="16" height="16" viewBox="0 0 24 24"><circle cx="10" cy="10" r="7" fill="none" stroke="#94A3B8" stroke-width="2.6"/><line x1="15.5" y1="15.5" x2="21" y2="21" stroke="#94A3B8" stroke-width="2.6" stroke-linecap="round"/></svg>
<div class="sk" style="width:46%;height:8px"></div></div>
<div style="display:flex;gap:16px;margin-bottom:20px"><div style="width:30px;height:7px;border-radius:4px;background:{INK}"></div><div class="sk" style="width:38px;height:7px"></div><div class="sk" style="width:34px;height:7px"></div><div class="sk" style="width:42px;height:7px"></div></div>
{ai}{results}</div></div>"""

def screenshot_uni():
    arrow = f"""<svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="31" fill="{VIOLET}"/>
<path d="M20 32 H42 M34 23 L43 32 L34 41" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
    return f"""<div class="abs glow grid" style="inset:0"></div>
<div class="abs" style="left:80px;top:52px;display:flex;align-items:center;gap:14px">
<div style="width:46px;height:46px">{ICON}</div><div class="word" style="font-size:40px">No AIO</div></div>
<div class="abs" style="left:80px;top:180px">{serp_state(500, True)}</div>
<div class="abs" style="left:608px;top:408px;filter:drop-shadow(0 10px 24px rgba(124,58,237,.5))">{arrow}</div>
<div class="abs" style="left:700px;top:180px;box-shadow:0 0 0 3px {VIOLET};border-radius:18px">{serp_state(500, False)}</div>
"""

import random

def noise(x0, x1, y0, y1, n_lines, n_sparks, seed, scale=1.0):
    """Ruido de IA: bloques de texto lavanda desenfocados y destellos dispersos."""
    rnd = random.Random(seed)
    out = []
    y = y0
    while y < y1 and n_lines:
        w = rnd.randint(int(120 * scale), int(420 * scale))
        x = rnd.randint(x0, max(x0, x1 - w))
        out.append(f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{int(9*scale)}px;border-radius:6px;'
                   f'background:rgba(196,181,253,{rnd.uniform(.10,.24):.2f});filter:blur({1.5*scale:.1f}px)"></div>')
        y += int(rnd.randint(18, 26) * scale); n_lines -= 1
    for _ in range(n_sparks):
        sz = rnd.randint(int(10 * scale), int(30 * scale))
        x, yy = rnd.randint(x0, x1), rnd.randint(y0, y1)
        out.append(f'<div class="abs" style="left:{x}px;top:{yy}px;width:{sz}px;height:{sz}px;opacity:{rnd.uniform(.25,.8):.2f}">'
                   f'{SPARK.replace("width=\"20\" height=\"20\"", "width=\"100%\" height=\"100%\"")}</div>')
    return "".join(out)

def lens(cx, cy, r, ring, handle_len, results, scale=1.0):
    """La lupa del logo como ventana: adentro, resultados limpios."""
    d = 2 * r
    res = "".join(f"""<div style="display:flex;gap:{int(12*scale)}px;margin-bottom:{int(16*scale)}px">
<div style="width:{int(20*scale)}px;height:{int(20*scale)}px;border-radius:50%;background:#E2E8F0;flex:none"></div>
<div style="flex:1"><div class="sk" style="width:36%;height:{int(7*scale)}px;margin-bottom:{int(6*scale)}px"></div>
<div style="width:{w}%;height:{int(12*scale)}px;border-radius:6px;background:{VIOLET};margin-bottom:{int(7*scale)}px"></div>
<div class="sk" style="width:94%;height:{int(7*scale)}px;margin-bottom:{int(5*scale)}px"></div><div class="sk" style="width:{w2}%;height:{int(7*scale)}px"></div></div></div>"""
                  for w, w2 in results)
    hx, hy = cx + r * 0.72, cy + r * 0.72
    return f"""<div class="abs" style="left:{hx - ring*0.9:.0f}px;top:{hy - ring*0.9:.0f}px;width:{handle_len}px;height:{ring*1.8:.0f}px;border-radius:{ring}px;
  background:#F8FAFC;transform-origin:{ring*0.9:.0f}px 50%;transform:rotate(45deg);box-shadow:0 20px 40px rgba(0,0,0,.35)"></div>
<div class="abs" style="left:{cx - r - ring}px;top:{cy - r - ring}px;width:{d + 2*ring}px;height:{d + 2*ring}px;border-radius:50%;background:#F8FAFC;
  box-shadow:0 30px 80px rgba(0,0,0,.45),0 0 0 1px rgba(255,255,255,.2),0 0 120px rgba(124,58,237,.35)"></div>
<div class="abs" style="left:{cx - r}px;top:{cy - r}px;width:{d}px;height:{d}px;border-radius:50%;overflow:hidden;background:#fff">
  <div style="position:absolute;left:{int(r*0.32)}px;right:{int(r*0.22)}px;top:{int(r*0.42)}px">{res}</div>
  <div style="position:absolute;inset:0;border-radius:50%;box-shadow:inset 0 0 {int(30*scale)}px rgba(15,23,42,.12)"></div>
</div>"""

def star_path(cx, cy, r):
    k1, k2 = 0.12, 0.28
    return (f"M{cx} {cy-r} C{cx+r*k1} {cy-r*k2} {cx+r*k2} {cy-r*k1} {cx+r} {cy} "
            f"C{cx+r*k2} {cy+r*k1} {cx+r*k1} {cy+r*k2} {cx} {cy+r} "
            f"C{cx-r*k1} {cy+r*k2} {cx-r*k2} {cy+r*k1} {cx-r} {cy} "
            f"C{cx-r*k2} {cy-r*k1} {cx-r*k1} {cy-r*k2} {cx} {cy-r}Z")

def ai_cluster(x, y, size, opacity=1.0, rot=0, uid="g"):
    """Símbolo genérico de IA: un destello grande y dos chicos, con degradado y brillo."""
    return f"""<svg class="abs" style="left:{x}px;top:{y}px;opacity:{opacity};transform:rotate({rot}deg);filter:drop-shadow(0 0 {size*0.18:.0f}px rgba(167,139,250,.75))"
 width="{size}" height="{size}" viewBox="0 0 100 100">
<defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#DDD6FE"/><stop offset=".55" stop-color="#A78BFA"/><stop offset="1" stop-color="#7C3AED"/></linearGradient></defs>
<path d="{star_path(42, 58, 38)}" fill="url(#{uid})"/>
<path d="{star_path(82, 18, 15)}" fill="url(#{uid})"/>
<path d="{star_path(84, 80, 9)}" fill="url(#{uid})"/></svg>"""

def small_tile_uni():
    return f"""<div class="abs glow" style="inset:0"></div>
{noise(170, 440, 10, 270, 12, 0, seed=7, scale=.7)}
{ai_cluster(196, 12, 62, .9, -8, "s1")}
{ai_cluster(392, 196, 40, .75, 10, "s2")}
{lens(326, 128, 86, 11, 92, [(64, 70), (52, 80), (60, 56)], scale=.62)}
<div class="abs" style="left:34px;top:40px;width:54px;height:54px;filter:drop-shadow(0 10px 24px rgba(124,58,237,.45))">{ICON}</div>
<div class="abs word" style="left:32px;top:150px;font-size:60px">No<br>AIO</div>"""

def marquee_uni():
    return f"""<div class="abs glow grid" style="inset:0"></div>
{noise(600, 1400, 20, 540, 22, 0, seed=11)}
{ai_cluster(690, 60, 120, .95, -10, "m1")}
{ai_cluster(1230, 40, 96, .8, 8, "m2")}
{ai_cluster(1240, 330, 70, .6, -6, "m3")}
{ai_cluster(700, 380, 64, .5, 12, "m4")}
{lens(1000, 262, 188, 22, 190, [(62, 72), (50, 84), (66, 58), (56, 76)])}
<div class="abs" style="left:100px;top:150px;width:96px;height:96px;filter:drop-shadow(0 16px 36px rgba(124,58,237,.5))">{ICON}</div>
<div class="abs word" style="left:94px;top:270px;font-size:150px">No AIO</div>"""

def render(name, body, w, h, c):
    html = SRC / f"{name}.html"
    html.write_text(f"<!doctype html><meta charset=utf-8><link rel=stylesheet href='{POPUP_CSS}'><style>{base_css(c)}{UNI_CSS}</style>"
                    f"<body style='width:{w}px;height:{h}px'>{body}</body>")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=2500",
                    f"--window-size={w},{h}", f"--screenshot={OUT / (name + '.png')}", html.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    html.unlink()
    # La tienda exige PNG de 24 bits sin canal alfa.
    from PIL import Image
    png = OUT / (name + ".png")
    Image.open(png).convert("RGB").save(png)

if __name__ == "__main__":
    import sys
    langs = sys.argv[1:] or list(COPY)
    OUT.mkdir(parents=True, exist_ok=True)
    for lang in langs:
        c = COPY[lang]
        for i, fn in enumerate([s1, s2, s3, s4], 1):
            render(f"screenshot-{i}-{lang}", fn(c, lang), 1280, 800, c)
        print("ok", lang)
    # Las imágenes promocionales son universales (una sola para todos los idiomas).
    render("screenshot-0-universal", screenshot_uni(), 1280, 800, COPY["en"])
    render("promo-small-440x280", small_tile_uni(), 440, 280, COPY["en"])
    render("promo-marquee-1400x560", marquee_uni(), 1400, 560, COPY["en"])
    print("ok promos")
