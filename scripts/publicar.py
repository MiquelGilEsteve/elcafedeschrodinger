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
API = "https://graph.instagram.com/v25.0"
MAX_RETRASO_H = 6
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")
USER = os.environ.get("IG_USER_ID", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "")
RAMA = os.environ.get("RAMA", "main")
DRY = os.environ.get("DRY_RUN") == "1"

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

def esperar(contenedor, intentos=30):
    for _ in range(intentos):
        estado = api("GET", contenedor, fields="status_code").get("status_code")
        if estado == "FINISHED":
            return
        if estado in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"contenedor {contenedor}: {estado}")
        time.sleep(5)
    raise RuntimeError(f"contenedor {contenedor}: no terminó a tiempo")

def publicar(carpeta, post):
    imgs = sorted(p for p in (carpeta / "img").glob("[0-9][0-9].jpg"))
    hijos = []
    for p in imgs:
        c = api("POST", f"{USER}/media", image_url=url_publica(p), is_carousel_item="true")["id"]
        esperar(c); hijos.append(c)
    car = api("POST", f"{USER}/media", media_type="CAROUSEL", children=",".join(hijos), caption=post.get("pie", ""))["id"]
    esperar(car)
    pub = api("POST", f"{USER}/media_publish", creation_id=car)["id"]
    resultado = {"media_id": pub, "publicado_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
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
    for carpeta in sorted((RAIZ / "posts").iterdir()):
        f = carpeta / "post.json"
        if not f.exists() or (carpeta / "publicado.json").exists() or not (carpeta / "img" / "01.jpg").exists():
            continue
        post = json.loads(f.read_text(encoding="utf-8"))
        cuando = dt.datetime.fromisoformat(post["publicar"])
        if cuando > ahora:
            continue
        if ahora - cuando > dt.timedelta(hours=MAX_RETRASO_H):
            print(f"[{carpeta.name}] OMITIDO: su hora ({cuando}) pasó hace más de {MAX_RETRASO_H} h. Cambia 'publicar' si quieres sacarlo.")
            continue
        if not DRY and not (TOKEN and USER and REPO):
            fallos += 1; print(f"[{carpeta.name}] ERROR: toca publicarlo, pero faltan los secretos IG_ACCESS_TOKEN / IG_USER_ID."); continue
        print(f"[{carpeta.name}] publicando ({post.get('audiencia', '')})…")
        try:
            res = publicar(carpeta, post)
            if not DRY:
                (carpeta / "publicado.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
            print(f"[{carpeta.name}] OK {res}")
        except Exception as e:
            fallos += 1; print(f"[{carpeta.name}] ERROR: {e}")
    sys.exit(1 if fallos else 0)
