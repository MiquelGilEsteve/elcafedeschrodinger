"""Renderizador estilo IMPACTO - "El Café de Schrödinger".

Formato inspirado en cuentas de curiosidades virales: imagen a sangre arriba que se
funde con negro, titular enorme en mayúsculas (Anton) con 1-2 palabras resaltadas,
insignia redonda con el logo arriba a la izquierda y el usuario pequeño abajo.

Uso:  python3 render_impacto.py post.json carpeta_salida/
Necesita Anton.woff2 junto al script (npm i @fontsource/anton ->
node_modules/@fontsource/anton/files/anton-latin-400-normal.woff2).

JSON:
{ "id": "...", "diapositivas": [ {"texto": "...", "svg": "<...>" | "foto": "x.jpg", "credito": "...",
   "fuente": "..." (opcional, línea pequeña de fuentes), "max": 520 (alto máx. del texto, opcional)} ],
  "story": {"texto": "...", "svg"/"foto", "llamada": "NUEVO POST"}, "pie": "...",
  "logo": "caricatura.png" (opcional; si no, busca logo.png junto al script) }
La insignia es la caricatura de Miquel (logo actual de la cuenta) recortada en círculo.
En textos: *así* -> amarillo, _así_ -> azul claro. Lienzo SVG: 1080x900 (post) y 1080x1300 (story).
"""
import asyncio, base64, json, mimetypes, pathlib, re, sys, html as H
from playwright.async_api import async_playwright

AQUI = pathlib.Path(__file__).resolve().parent
HANDLE = "@elcafedeschrodinger"
Y, BLUE_L, NAVY = "#FFD84D", "#7FA0FF", "#0B1A3A"
BASE = pathlib.Path(".")

def fmt(t):
    t = H.escape(t)
    t = re.sub(r"\*(.+?)\*", r'<span class="y">\1</span>', t)
    t = re.sub(r"_(.+?)_", r'<span class="b">\1</span>', t)
    return t

def b64(p):
    p = pathlib.Path(p); p = p if p.is_absolute() else BASE / p
    return f"data:{mimetypes.guess_type(str(p))[0] or 'image/jpeg'};base64," + base64.b64encode(p.read_bytes()).decode()

LOGO = None  # ruta a la caricatura de Miquel (logo actual). Campo "logo" del JSON o logo.png/.jpg junto al script.

# Recorte de la cara en la caricatura original de Miquel (1024x1536), comprobado a ojo el 2026-11-09.
# Es el mismo recorte que la foto de perfil (1080x1080).
RECORTE_CARICATURA = (160, 130, 800, 770)  # mismo encuadre que la foto de perfil (cara + taza), pedido por Miquel

def logo_uri():
    from PIL import Image
    import io
    p = pathlib.Path(LOGO); p = p if p.is_absolute() else BASE / p
    im = Image.open(p).convert("RGB")
    if im.size == (1024, 1536):
        im = im.crop(RECORTE_CARICATURA)
    elif im.width != im.height:  # otra imagen no cuadrada: cuadrado centrado arriba (donde suele estar la cara)
        s = min(im.size); x0 = (im.width - s) // 2
        im = im.crop((x0, 0, x0 + s, s))
    buf = io.BytesIO(); im.resize((300, 300)).save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def insignia():
    if LOGO:
        return (f'<div style="width:118px;height:118px;border-radius:50%;border:4px solid {Y};'
                f'background:#fff url({logo_uri()}) center/cover no-repeat"></div>')
    # Si no hay caricatura: logo antiguo (taza con gato cuántico), igual que logo.py
    def gato(cx, cy, k, col):
        L = f"M{cx},{cy+36*k} C{cx-30*k},{cy+36*k} {cx-50*k},{cy+18*k} {cx-50*k},{cy-10*k} L{cx-50*k},{cy-50*k} L{cx-28*k},{cy-30*k} C{cx-18*k},{cy-35*k} {cx-9*k},{cy-36*k} {cx},{cy-36*k}"
        R = f"M{cx},{cy+36*k} C{cx+30*k},{cy+36*k} {cx+50*k},{cy+18*k} {cx+50*k},{cy-10*k} L{cx+50*k},{cy-50*k} L{cx+28*k},{cy-30*k} C{cx+18*k},{cy-35*k} {cx+9*k},{cy-36*k} {cx},{cy-36*k}"
        return (f'<path d="{L}" fill="none" stroke="{col}" stroke-width="{10*k:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="{R}" fill="none" stroke="{col}" stroke-width="{10*k:.1f}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{13*k:.1f} {14*k:.1f}"/>'
                f'<circle cx="{cx-18*k}" cy="{cy-2*k}" r="{6.5*k}" fill="{col}"/>'
                f'<circle cx="{cx+18*k}" cy="{cy-2*k}" r="{6.5*k}" fill="none" stroke="{col}" stroke-width="{3.6*k:.1f}"/>')
    vapor = "".join(f'<path d="M{x},188 C{x-16},168 {x+16},150 {x},130 C{x-16},110 {x+16},96 {x},80" fill="none" stroke="{Y}" stroke-width="10" stroke-linecap="round"/>' for x in (160, 200, 240))
    s = (f'<path d="M120,208 L280,208 L268,318 C266,334 254,344 238,344 L162,344 C146,344 134,334 132,318 Z" fill="#fff"/>'
         f'<path d="M278,232 C318,232 322,296 270,300" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round"/>'
         f'<ellipse cx="200" cy="208" rx="80" ry="12" fill="{Y}"/>{gato(200, 282, 0.95, "#2A4BFF")}'
         f'<line x1="104" y1="364" x2="296" y2="364" stroke="#fff" stroke-width="10" stroke-linecap="round"/>')
    return (f'<svg viewBox="0 0 400 400" width="118" height="118"><circle cx="200" cy="200" r="196" fill="{NAVY}" stroke="{Y}" stroke-width="8"/>'
            f'<g transform="translate(190 200) scale(1.05) translate(-200 -278)">{s}</g></svg>')

def fuente_anton():
    f = AQUI / "Anton.woff2"
    if not f.exists():  # npm sí tiene salida en las sesiones en la nube
        import subprocess, shutil
        subprocess.run(["npm", "i", "--prefix", str(AQUI), "@fontsource/anton"], check=True, capture_output=True)
        shutil.copy(AQUI / "node_modules/@fontsource/anton/files/anton-latin-400-normal.woff2", f)
    return f.read_bytes()

def css(h):
    font = base64.b64encode(fuente_anton()).decode()
    return f"""
@font-face{{font-family:'Anton';src:url(data:font/woff2;base64,{font}) format('woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:{h}px;overflow:hidden;background:#000;color:#fff;position:relative;font-family:'Inter'}}
.img{{position:absolute;left:0;right:0;top:0}}
.img svg,.img .ph{{display:block;width:100%;height:100%}}
.ph{{background-size:cover;background-position:center}}
.fade{{position:absolute;left:0;right:0;background:linear-gradient(rgba(0,0,0,0),#000)}}
.badge{{position:absolute;top:34px;left:34px;filter:drop-shadow(0 4px 10px rgba(0,0,0,.5))}}
.cred{{position:absolute;right:26px;font-size:17px;color:#fff;opacity:.75}}
.txt{{position:absolute;left:44px;right:44px;text-align:center;font-family:'Anton';text-transform:uppercase;line-height:1.04;letter-spacing:.005em}}
.y{{color:{Y}}} .b{{color:{BLUE_L}}}
.src{{position:absolute;left:60px;right:60px;text-align:center;font-size:21px;color:#9AA3B5;font-weight:500}}
.hand{{position:absolute;left:0;right:0;bottom:30px;display:flex;align-items:center;justify-content:center;gap:16px;font-size:19px;font-weight:700;letter-spacing:.12em;color:#fff;opacity:.85;text-transform:uppercase}}
.hand i{{display:block;width:120px;height:2px;background:#fff;opacity:.6}}
.call{{position:absolute;left:50%;transform:translateX(-50%);background:{Y};color:#000;font-family:'Anton';font-size:52px;letter-spacing:.03em;padding:18px 48px;border-radius:60px}}
"""

def imagen(d, h_img):
    if d.get("foto"):
        pos = d.get("foto_pos", "center")  # encuadre de la foto, p. ej. "center 30%"
        ph = f'<div class="ph" style="background-image:url({b64(d["foto"])});background-position:{pos}"></div>'
    else:
        ph = d.get("svg", "")
    cred = f'<div class="cred" style="top:{h_img-300}px">{H.escape(d["credito"])}</div>' if d.get("credito") else ""
    return f'<div class="img" style="height:{h_img}px">{ph}</div><div class="fade" style="top:{h_img-360}px;height:360px"></div>{cred}'

# El texto se ajusta solo: empieza grande y baja de tamaño hasta caber en el alto máximo.
AJUSTE = """<script>
window.ajustado=false;
document.fonts.ready.then(()=>{const t=document.querySelector('.txt'); let f=+t.dataset.f; t.style.fontSize=f+'px';
while(t.offsetHeight>+t.dataset.max && f>40){f-=2;t.style.fontSize=f+'px';} window.ajustado=true;});
</script>"""

def slide(d):
    H_ = 1350; fuente = d.get("fuente")
    bottom = 128 if fuente else 82
    src = f'<div class="src" style="bottom:72px">Fuentes: {H.escape(fuente)}</div>' if fuente else ""
    body = (imagen(d, 920) + f'<div class="badge">{insignia()}</div>'
            f'<div class="txt" data-f="{d.get("tam", 104)}" data-max="{d.get("max", 470)}" style="bottom:{bottom}px">{fmt(d["texto"])}</div>'
            f'{src}<div class="hand"><i></i>{HANDLE[1:]}<i></i></div>')
    return f'<html><head><meta charset="utf-8"><style>{css(H_)}</style></head><body>{body}{AJUSTE}</body></html>'

def story(d):
    body = (imagen(d, 1300) + f'<div class="badge">{insignia()}</div>'
            f'<div class="txt" data-f="{d.get("tam", 120)}" data-max="{d.get("max", 430)}" style="bottom:330px">{fmt(d["texto"])}</div>'
            f'<div class="call" style="bottom:170px">{H.escape(d.get("llamada", "NUEVO POST"))}</div>'
            f'<div class="hand" style="bottom:90px"><i></i>{HANDLE[1:]}<i></i></div>')
    return f'<html><head><meta charset="utf-8"><style>{css(1920)}</style></head><body>{body}{AJUSTE}</body></html>'

async def main(src, out):
    global BASE, LOGO; BASE = pathlib.Path(src).resolve().parent
    post = json.loads(pathlib.Path(src).read_text(encoding="utf-8"))
    LOGO = post.get("logo") or next((str(AQUI / n) for n in ("logo.png", "logo.jpg", "logo.jpeg", "logo.webp") if (AQUI / n).exists()), None)
    if not LOGO: print("Aviso: no hay caricatura (logo.png); se usa el logo antiguo de la taza.")
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i, d in enumerate(post["diapositivas"], 1):
            await pg.set_content(slide(d)); await pg.wait_for_function("window.ajustado"); await pg.wait_for_timeout(100)
            await pg.screenshot(path=str(out / f"{post['id']}_{i:02d}.png"))
        if post.get("story"):
            await pg.set_viewport_size({"width": 1080, "height": 1920})
            await pg.set_content(story(post["story"])); await pg.wait_for_function("window.ajustado"); await pg.wait_for_timeout(100)
            await pg.screenshot(path=str(out / f"{post['id']}_story.png"))
        await b.close()
    if post.get("pie"):
        (out / f"{post['id']}_texto.txt").write_text(post["pie"], encoding="utf-8")

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
