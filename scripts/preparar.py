"""Prepara las publicaciones pendientes: descarga las fotos reales, renderiza y deja los JPG listos.

Para cada carpeta posts/<id>/ con post.json y sin img/01.jpg:
  1. Descarga cada "foto_url" (diapositivas y story) a posts/<id>/fotos/ y la usa como "foto".
     Si la descarga falla y hay "svg", se usa la ilustración y se avisa (no se bloquea la publicación).
  2. Renderiza con render/render_impacto.py.
  3. Convierte a JPEG (Instagram publica JPEG) en posts/<id>/img/01.jpg ... y story.jpg.
  4. Comprueba límites de Instagram (máx. 10 diapositivas, pie ≤ 2200 caracteres, ≤ 30 hashtags).
Uso: python scripts/preparar.py
"""
import asyncio, json, pathlib, re, shutil, subprocess, sys, tempfile, time
import requests
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "render"))
import render_impacto as R  # noqa: E402

SEG_REEL, FUNDIDO = 4.5, 0.5  # segundos por frase y duración del fundido (5 frases ≈ 20 s)

UA = {"User-Agent": "elcafedeschrodinger-bot/1.0 (publicador de Instagram)"}

def descargar(url, destino):
    # Wikimedia devuelve «429 Too Many Requests» tras unas pocas descargas seguidas: esperar y reintentar.
    for intento in range(4):
        r = requests.get(url, headers=UA, timeout=60)
        if r.status_code != 429 or intento == 3:
            break
        try:
            espera = min(int(r.headers.get("retry-after", "")), 90)
        except ValueError:
            espera = 20 * (intento + 1)
        print(f"   429 en {url[:80]}…; reintento en {espera} s")
        time.sleep(max(espera, 5))
    r.raise_for_status()
    if not r.headers.get("content-type", "").startswith("image/"):
        raise ValueError(f"no es una imagen ({r.headers.get('content-type')})")
    destino.write_bytes(r.content)
    return destino

def comprobar(post, carpeta):
    errores = []
    if len(post["diapositivas"]) > 10:
        errores.append("más de 10 diapositivas (límite de Instagram)")
    pie = post.get("pie", "")
    if len(pie) > 2200:
        errores.append(f"pie de {len(pie)} caracteres (máx. 2200)")
    if len(re.findall(r"#\w+", pie)) > 30:
        errores.append("más de 30 hashtags")
    if "publicar" not in post:
        errores.append("falta la fecha 'publicar'")
    for e in errores:
        print(f"[{carpeta.name}] ERROR: {e}")
    return not errores

def montar_reel(pngs, destino):
    """Une los fotogramas con fundidos y añade una pista AAC en silencio (Instagram espera audio)."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in pngs:
        cmd += ["-loop", "1", "-t", str(SEG_REEL), "-framerate", "30", "-i", str(f)]
    total = len(pngs) * SEG_REEL - (len(pngs) - 1) * FUNDIDO
    cmd += ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    filtro, prev = [], "[0:v]"
    for i in range(1, len(pngs)):
        sal = f"[v{i}]"
        filtro.append(f"{prev}[{i}:v]xfade=transition=fade:duration={FUNDIDO}:offset={i * (SEG_REEL - FUNDIDO):.2f}{sal}")
        prev = sal
    filtro.append(f"{prev}format=yuv420p[v]")
    cmd += ["-filter_complex", ";".join(filtro), "-map", "[v]", "-map", f"{len(pngs)}:a",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "20", "-r", "30",
            "-c:a", "aac", "-b:a", "64k", "-ar", "44100", "-t", f"{total:.2f}", "-movflags", "+faststart", str(destino)]
    subprocess.run(cmd, check=True)

def preparar(carpeta, solo_story=False, solo_reel=False):
    post = json.loads((carpeta / "post.json").read_text(encoding="utf-8"))
    if not comprobar(post, carpeta):
        return False
    st, d1 = post.get("story"), post["diapositivas"][0]
    if st is not None and not st.get("foto_url") and not st.get("foto") and not st.get("sin_foto"):
        # la story usa la foto real de la portada si no tiene una propia
        for k in ("foto_url", "foto", "credito"):
            if d1.get(k): st[k] = d1[k]
        if "foto_pos" not in st and d1.get("foto_pos"): st["foto_pos"] = d1["foto_pos"]
    fotos = carpeta / "fotos"; fotos.mkdir(exist_ok=True)
    piezas = list(enumerate(post["diapositivas"], 1)) + ([("story", post["story"])] if post.get("story") else [])
    for n, d in piezas:
        if d.get("foto_url") and not d.get("foto"):
            ext = pathlib.Path(d["foto_url"].split("?")[0]).suffix or ".jpg"
            try:
                d["foto"] = str(descargar(d["foto_url"], fotos / f"{n}{ext}").resolve())
                print(f"[{carpeta.name}] foto {n} descargada: {d['foto_url']}")
            except Exception as e:  # sin foto: se usa la ilustración si existe
                print(f"[{carpeta.name}] AVISO: no se pudo descargar la foto {n} ({e}); se usa la ilustración.")
                if not d.get("svg"):
                    print(f"[{carpeta.name}] ERROR: la diapositiva {n} no tiene ilustración de reserva.")
                    return False
        elif d.get("foto"):
            d["foto"] = str((carpeta / d["foto"]).resolve())
    post["logo"] = str((RAIZ / "render" / "caricatura.jpg").resolve())
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "post.json").write_text(json.dumps(post, ensure_ascii=False), encoding="utf-8")
        asyncio.run(R.main(str(tmp / "post.json"), str(tmp / "png")))
        img = carpeta / "img"; img.mkdir(exist_ok=True)
        reel_pngs = sorted((tmp / "png").glob("*_reel[0-9][0-9].png"))
        if reel_pngs and not solo_story:
            montar_reel(reel_pngs, img / "reel.mp4")
            Image.open(reel_pngs[0]).convert("RGB").save(img / "reel_portada.jpg", "JPEG", quality=90)
            print(f"[{carpeta.name}] reel listo ({len(reel_pngs)} frases)")
        for png in sorted((tmp / "png").glob("*.png")):
            if png in reel_pngs or solo_reel:
                continue
            if solo_story and not png.stem.endswith("_story"):
                continue
            nombre = "story.jpg" if png.stem.endswith("_story") else png.stem.rsplit("_", 1)[-1] + ".jpg"
            Image.open(png).convert("RGB").save(img / nombre, "JPEG", quality=92, optimize=True)
        if not (solo_story or solo_reel) and (tmp / "png" / f"{post['id']}_texto.txt").exists():
            shutil.copy(tmp / "png" / f"{post['id']}_texto.txt", carpeta / "pie.txt")
    print(f"[{carpeta.name}] listo: {len(list((carpeta / 'img').glob('*.jpg')))} imágenes")
    return True

def falta_reel(carpeta):
    if (carpeta / "publicado.json").exists() or (carpeta / "img" / "reel.mp4").exists():
        return False
    post = json.loads((carpeta / "post.json").read_text(encoding="utf-8"))
    return post.get("reel", True) and not post.get("borrador")

if __name__ == "__main__":
    ok = True
    for carpeta in sorted((RAIZ / "posts").iterdir()):
        if not (carpeta / "post.json").exists():
            continue
        if not (carpeta / "img" / "01.jpg").exists():
            ok = preparar(carpeta) and ok
        elif not (carpeta / "img" / "story.jpg").exists():  # rehacer solo la story
            ok = preparar(carpeta, solo_story=True) and ok
        elif falta_reel(carpeta):  # posts pendientes sin Reel (preparados antes de existir los Reels)
            ok = preparar(carpeta, solo_reel=True) and ok
    sys.exit(0 if ok else 1)
