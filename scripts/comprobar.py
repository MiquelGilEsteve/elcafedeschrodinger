"""Comprueba la conexión con Instagram SIN publicar nada: nombre de la cuenta y cupo de publicaciones."""
import os, sys
import requests

TOKEN = os.environ.get("IG_ACCESS_TOKEN", ""); USER = os.environ.get("IG_USER_ID", "")
if not TOKEN or not USER:
    sys.exit("FALTA algún secreto: IG_ACCESS_TOKEN y/o IG_USER_ID.")
HOST = os.environ.get("IG_API_HOST") or ("graph.facebook.com" if TOKEN.startswith("EAA") else "graph.instagram.com")
base = f"https://{HOST}/v25.0"
r = requests.get(f"{base}/{USER}", params={"fields": "username,name,media_count", "access_token": TOKEN}, timeout=30)
print("Cuenta:", r.status_code, r.text[:300])
r2 = requests.get(f"{base}/{USER}/content_publishing_limit", params={"fields": "quota_usage,config", "access_token": TOKEN}, timeout=30)
print("Cupo:", r2.status_code, r2.text[:300])
ok = r.ok and r.json().get("username") == "elcafedeschrodinger" and r2.ok
print("RESULTADO:", "OK, conexión correcta" if ok else "ERROR")
sys.exit(0 if ok else 1)
