"""Publica en Instagram los carruseles cuya hora ya ha llegado (API oficial de Instagram, Instagram Login).

Variables de entorno (secretos de GitHub):
  IG_ACCESS_TOKEN  token de acceso de la cuenta (permisos instagram_business_basic + instagram_business_content_publish)
  IG_USER_ID       ID de la cuenta de Instagram
  GITHUB_REPOSITORY / RAMA  para construir las URL públicas de las imágenes (raw.githubusercontent.com)
  DRY_RUN=1        solo muestra lo que haría, sin llamar a la API

Un post se publica si: tiene img/01.jpg, su hora "publicar" ya pasó, no tiene publicado.json
y no han pasado más de MAX_RETRASO_H horas (para no sacar posts atrasados sin querer).
"""
import datetime as dt, json, os, pathlib, sys, time
import requests

RAIZ = pathlib.Path(__file__).resolve().parents[1]
MAX_RETRASO_H = 6
REEL_PENDIENTE_H = 24  # Reels que faltan en posts publicados hace menos de esto se suben (uno por pasada)
# Si Instagram bloquea la acción (código 4 / subcódigo 2207051, «se ha bloqueado la acción»), insistir cada 15 min
# puede alargar el bloqueo: se apunta en posts/_bloqueo_instagram.json y no se reintenta hasta pasadas PAUSA_BLOQUEO_H horas.
PAUSA_BLOQUEO_H = 4
BLOQUEO = RAIZ / "posts" / "_bloqueo_instagram.json"
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")
USER = os.environ.get("IG_USER_ID", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "")
RAMA = os.environ.get("RAMA", "main")
DRY = os.environ.get("DRY_RUN") == "1"
# Los tokens de Instagram (inicio de sesión con Instagram/unificado) empiezan por "IG" y van contra graph.instagram.com;
# los de Facebook (empiezan por "EAA") van contra graph.facebook.com. IG_API_HOST permite forzarlo.
HOST = os.environ.get("IG_API_HOST") or ("graph.facebook.com" if TOKEN.startswith("EAA") else "graph.instagram.com")
API = f"https://{HOST}/v25.0"

def url_publica(ruta):
    rel = ruta.relative_to(RAIZ).as_posix()
    return f"https://raw.githubusercontent.com/{REPO}/{RAMA}/{rel}"

def api(metodo, ruta, **datos):
    if DRY:
        print("   (simulación)", metodo, ruta, {k: v for k, v in datos.items() if k != "caption"})
        return {"id": "SIMULADO", "status_code": "FINISHED"}
    datos["access_token"] = TOKEN
    r = requests.request(metodo, f"{API}/{ruta}", data=datos if metodo == "POST" else None,
                         params=datos if metodo == "GET" else None, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"{metodo} {ruta}: {r.status_code} {r.text[:500]}")
    return r.json()

def esperar(contenedor, intentos=30, pausa=5):
    for _ in range(intentos):
        r = api("GET", contenedor, fields="status_code,status")
        estado = r.get("status_code")
        if estado == "FINISHED":
            return
        if estado in ("ERROR", "EXPIRED"):  # "status" trae el motivo (p. ej. «Error: 2207026»)
            raise RuntimeError(f"contenedor {contenedor}: {estado} ({r.get('status', 'sin detalle')})")
        time.sleep(pausa)
    raise RuntimeError(f"contenedor {contenedor}: no terminó a tiempo")

def primera_linea(texto):
    return " ".join((texto or "").strip().splitlines()[0].split()).lower() if (texto or "").strip() else ""

def ya_publicado(post):
    """Busca en las últimas publicaciones de la cuenta un carrusel con la misma primera línea del pie.
    Instagram a veces publica el post aunque media_publish devuelva error (p. ej. 2207051): sin esta
    comprobación el post se volvía a publicar en el siguiente intento y salía repetido."""
    clave = primera_linea(post.get("pie", ""))
    if not clave or DRY:
        return None
    desde = dt.datetime.fromisoformat(post["publicar"]) - dt.timedelta(hours=2)
    datos = api("GET", f"{USER}/media", fields="id,caption,timestamp,media_type", limit=25).get("data", [])
    for m in datos:
        if m.get("media_type") != "CAROUSEL_ALBUM" or primera_linea(m.get("caption", "")) != clave:
            continue
        cuando = dt.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if cuando >= desde:
            return {"media_id": m["id"], "publicado_utc": cuando.astimezone(dt.timezone.utc).isoformat()}
    return None

def reel_publicado(post):
    """ID de un Reel ya publicado con la misma primera línea del pie (o None)."""
    clave = primera_linea(post.get("pie", ""))
    if not clave or DRY:
        return None
    desde = dt.datetime.fromisoformat(post["publicar"]) - dt.timedelta(hours=2)
    for m in api("GET", f"{USER}/media", fields="id,caption,timestamp,media_type,media_product_type", limit=25).get("data", []):
        es_reel = m.get("media_product_type") == "REELS" or m.get("media_type") == "VIDEO"
        if es_reel and primera_linea(m.get("caption", "")) == clave and \
           dt.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z") >= desde:
            return m["id"]
    return None

def publicar(carpeta, post):
    imgs = sorted(p for p in (carpeta / "img").glob("[0-9][0-9].jpg"))
    hijos = []
    for p in imgs:
        c = api("POST", f"{USER}/media", image_url=url_publica(p), is_carousel_item="true")["id"]
        try:
            esperar(c)
        except RuntimeError as e:
            raise RuntimeError(f"diapositiva {p.name}: {e}") from None
        hijos.append(c)
    car = api("POST", f"{USER}/media", media_type="CAROUSEL", children=",".join(hijos), caption=post.get("pie", ""))["id"]
    try:
        esperar(car)
    except RuntimeError as e:
        raise RuntimeError(f"carrusel (pie/hijos): {e}") from None
    pub = api("POST", f"{USER}/media_publish", creation_id=car)["id"]
    resultado = {"media_id": pub, "publicado_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    return extras(carpeta, post, resultado)

def extras(carpeta, post, resultado):
    """Reel y story tras el carrusel. Se llama también cuando Instagram devolvió error en el carrusel
    pero lo publicó (2207051): antes, en ese caso, el Reel no se subía nunca."""
    reel = carpeta / "img" / "reel.mp4"
    if post.get("reel", True) and reel.exists() and not resultado.get("reel_id"):  # Reel normal; los «de prueba» exigen un mínimo de seguidores
        try:
            time.sleep(20)  # respiro tras el carrusel para no disparar el límite de peticiones
            datos = {"media_type": "REELS", "video_url": url_publica(reel), "caption": post.get("pie", "")}
            portada = carpeta / "img" / "reel_portada.jpg"
            if portada.exists():
                datos["cover_url"] = url_publica(portada)
            if post.get("reel_prueba", False):
                datos["trial_params"] = json.dumps({"graduation_strategy": "SS_PERFORMANCE"})
            else:
                datos["share_to_feed"] = "true"
            r = api("POST", f"{USER}/media", **datos)["id"]
            esperar(r, intentos=40, pausa=15)  # los vídeos tardan más en procesarse
            try:
                resultado["reel_id"] = api("POST", f"{USER}/media_publish", creation_id=r)["id"]
            except RuntimeError as e:
                if "2207051" not in str(e):
                    raise
                time.sleep(30)  # igual que el carrusel: Instagram suele publicarlo pese al error
                resultado["reel_id"] = reel_publicado(post) or "desconocido"
                resultado["reel_nota"] = "media_publish devolvió 2207051; " + ("reel encontrado en la cuenta" if resultado["reel_id"] != "desconocido" else "no se encontró: revisar a mano")
            resultado["reel_prueba"] = bool(post.get("reel_prueba", False))
        except Exception as e:
            resultado["reel_error"] = str(e); print("   AVISO reel:", e)
    story = carpeta / "img" / "story.jpg"
    if post.get("story_auto") and story.exists():  # las stories por API solo funcionan en cuentas de empresa
        try:
            s = api("POST", f"{USER}/media", image_url=url_publica(story), media_type="STORIES")["id"]
            esperar(s); resultado["story_id"] = api("POST", f"{USER}/media_publish", creation_id=s)["id"]
        except Exception as e:
            resultado["story_error"] = str(e); print("   AVISO story:", e)
    return resultado

if __name__ == "__main__":
    ahora = dt.datetime.now(dt.timezone.utc); fallos = 0
    if BLOQUEO.exists() and not DRY:
        b = json.loads(BLOQUEO.read_text(encoding="utf-8"))
        hasta = dt.datetime.fromisoformat(b["hasta_utc"])
        if ahora < hasta:
            print(f"Instagram bloqueó la publicación ({b.get('error', '')[:200]}). En pausa hasta {hasta} UTC; borra {BLOQUEO.name} para reintentar antes.")
            sys.exit(0)
    for carpeta in sorted((RAIZ / "posts").iterdir()):  # Reels pendientes de posts ya publicados (máx. REEL_PENDIENTE_H)
        f, pj = carpeta / "post.json", carpeta / "publicado.json"
        if DRY or not (f.exists() and pj.exists() and (carpeta / "img" / "reel.mp4").exists() and TOKEN and USER and REPO):
            continue
        res = json.loads(pj.read_text(encoding="utf-8")); post = json.loads(f.read_text(encoding="utf-8"))
        if res.get("reel_id") or res.get("reel_error") or not post.get("reel", True):
            continue
        if ahora - dt.datetime.fromisoformat(res["publicado_utc"]) > dt.timedelta(hours=REEL_PENDIENTE_H):
            continue
        print(f"[{carpeta.name}] el carrusel está publicado pero falta el Reel: publicándolo…")
        try:
            existente = reel_publicado(post)
        except Exception as e:
            existente = None; print("   AVISO: no se pudo comprobar si el Reel ya estaba:", e)
        if existente:
            res["reel_id"] = existente
        else:
            res = extras(carpeta, {**post, "story_auto": False}, res)
        pj.write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"[{carpeta.name}] Reel: {res.get('reel_id') or res.get('reel_error')}")
        break  # uno por pasada, para no saturar la cuenta
    for carpeta in sorted((RAIZ / "posts").iterdir()):
        f = carpeta / "post.json"
        if not f.exists() or (carpeta / "publicado.json").exists() or not (carpeta / "img" / "01.jpg").exists():
            continue
        post = json.loads(f.read_text(encoding="utf-8"))
        if post.get("borrador"):
            print(f"[{carpeta.name}] borrador pendiente de aprobación: no se publica")
            continue
        cuando = dt.datetime.fromisoformat(post["publicar"])
        if cuando > ahora:
            continue
        if ahora - cuando > dt.timedelta(hours=MAX_RETRASO_H):
            print(f"[{carpeta.name}] OMITIDO: su hora ({cuando}) pasó hace más de {MAX_RETRASO_H} h. Cambia 'publicar' si quieres sacarlo.")
            continue
        if not DRY and not (TOKEN and USER and REPO):
            fallos += 1; print(f"[{carpeta.name}] ERROR: toca publicarlo, pero faltan los secretos IG_ACCESS_TOKEN / IG_USER_ID."); continue
        try:  # ¿ya está en Instagram? (evita publicarlo dos veces)
            previo = ya_publicado(post)
        except Exception as e:
            previo = None; print(f"[{carpeta.name}] AVISO: no se pudo comprobar si ya estaba publicado: {e}")
        if previo:
            previo["nota"] = "ya estaba publicado en Instagram (detectado antes de publicar); no se repite"
            previo = extras(carpeta, post, previo)
            (carpeta / "publicado.json").write_text(json.dumps(previo, indent=1), encoding="utf-8")
            print(f"[{carpeta.name}] ya estaba publicado: {previo}"); continue
        print(f"[{carpeta.name}] publicando ({post.get('audiencia', '')})…")
        try:
            res = publicar(carpeta, post)
            if not DRY:
                (carpeta / "publicado.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
            print(f"[{carpeta.name}] OK {res}")
        except Exception as e:
            if "media_publish" in str(e) and not DRY:  # Instagram puede haberlo publicado pese al error
                time.sleep(30)
                try:
                    previo = ya_publicado(post)
                except Exception:
                    previo = None
                if previo:
                    previo["nota"] = f"Instagram devolvió error pero el post se publicó: {str(e)[:300]}"
                    previo = extras(carpeta, post, previo)
                    (carpeta / "publicado.json").write_text(json.dumps(previo, indent=1), encoding="utf-8")
                    print(f"[{carpeta.name}] publicado pese al error de Instagram: {previo}"); continue
            fallos += 1; print(f"[{carpeta.name}] ERROR: {e}")
            if "2207051" in str(e) and not DRY:
                hasta = ahora + dt.timedelta(hours=PAUSA_BLOQUEO_H)
                BLOQUEO.write_text(json.dumps({"desde_utc": ahora.isoformat(), "hasta_utc": hasta.isoformat(),
                                               "post": carpeta.name, "error": str(e)}, indent=1), encoding="utf-8")
                print(f"   Bloqueo de Instagram: no se reintenta hasta {hasta} UTC.")
                break
    sys.exit(1 if fallos else 0)
