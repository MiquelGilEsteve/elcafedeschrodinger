"""Prepara las publicaciones pendientes: descarga las fotos reales, renderiza y deja los JPG listos.

Para cada carpeta posts/<id>/ con post.json y sin img/01.jpg:
  1. Descarga cada "foto_url" (diapositivas y story) a posts/<id>/fotos/ y la usa como "foto".
     Si la descarga falla y hay "svg", se usa la ilustración y se avisa (no se bloquea la publicación).
  2. Renderiza con render/render_impacto.py.
  3. Convierte a JPEG (Instagram publica JPEG) en posts/<id>/img/01.jpg ... y story.jpg.
  4. Comprueba límites de Instagram (máx. 10 diapositivas, pie ≤ 2200 caracteres, ≤ 30 hashtags).
Uso: python scripts/preparar.py
"""
import asyncio, json, pathlib, re, shutil, sys, tempfile
import requests
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "render"))
import render_impacto as R  # noqa: E402

UA = {"User-Agent": "elcafedeschrodinger-bot/1.0 (publicador de Instagram)"}

def descargar(url, destino):
    r = requests.get(url, headers=UA, timeout=60)
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

def preparar(carpeta, solo_story=False):
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
        for png in sorted((tmp / "png").glob("*.png")):
            if solo_story and not png.stem.endswith("_story"):
                continue
            nombre = "story.jpg" if png.stem.endswith("_story") else png.stem.rsplit("_", 1)[-1] + ".jpg"
            Image.open(png).convert("RGB").save(img / nombre, "JPEG", quality=92, optimize=True)
        if not solo_story and (tmp / "png" / f"{post['id']}_texto.txt").exists():
            shutil.copy(tmp / "png" / f"{post['id']}_texto.txt", carpeta / "pie.txt")
    print(f"[{carpeta.name}] listo: {len(list((carpeta / 'img').glob('*.jpg')))} imágenes")
    return True

if __name__ == "__main__":
    ok = True
    for carpeta in sorted((RAIZ / "posts").iterdir()):
        if not (carpeta / "post.json").exists():
            continue
        if not (carpeta / "img" / "01.jpg").exists():
            ok = preparar(carpeta) and ok
        elif not (carpeta / "img" / "story.jpg").exists():  # rehacer solo la story
            ok = preparar(carpeta, solo_story=True) and ok
    sys.exit(0 if ok else 1)
