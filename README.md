# El Café de Schrödinger — publicador automático

Publica en Instagram (@elcafedeschrodinger) los carruseles que prepara Claude cada mañana.

## Cómo funciona
1. **Claude** (tarea programada, cada mañana) investiga, escribe los textos y elige fotos reales con licencia libre. Deja cada publicación en `posts/<fecha>_<tema>/post.json`, con la hora a la que debe salir (`publicar`).
2. **GitHub Actions** (`.github/workflows/publicar.yml`, cada 15 min):
   - descarga las fotos reales (`foto_url`) y renderiza las diapositivas con `render/render_impacto.py`;
   - guarda los JPG en `posts/<id>/img/` (tienen que estar en una URL pública para que Instagram los descargue);
   - cuando llega la hora, publica el carrusel con la **API oficial de Instagram** y guarda `publicado.json`.
3. Si un post lleva más de 6 h de retraso no se publica solo (para evitar sorpresas): cambia su `publicar` y se publicará en la siguiente pasada.

## post.json
```json
{
  "id": "2026-11-10_voyager_dia_luz",
  "publicar": "2026-11-10T14:00:00+01:00",
  "audiencia": "ES",
  "story_auto": false,
  "diapositivas": [
    {"texto": "Titular con *resaltado*", "foto_url": "https://…jpg", "credito": "Foto: NASA · Dominio público",
     "foto_pos": "center", "svg": "<svg>…</svg> (ilustración de reserva si la foto no se puede descargar)"},
    {"texto": "…", "svg": "…", "fuente": "Fuentes de la última diapositiva"}
  ],
  "story": {"texto": "…", "svg": "…", "llamada": "NUEVO POST ↓"},
  "pie": "Texto del pie con #hashtags"
}
```
Límites de Instagram: máx. 10 diapositivas por carrusel, pie ≤ 2200 caracteres, ≤ 30 hashtags. Las stories por API solo funcionan en cuentas de **empresa** (`story_auto: true`).

## Configuración (una sola vez)
Secretos del repositorio (Settings → Secrets and variables → Actions):
- `IG_ACCESS_TOKEN`: token de larga duración de la cuenta (app de Meta con «Instagram API with Instagram login», permisos `instagram_business_basic` e `instagram_business_content_publish`).
- `IG_USER_ID`: ID de la cuenta de Instagram.
- `GH_PAT` (opcional): token de GitHub con permiso para escribir secretos de este repositorio; lo usa `renovar_token.yml` para renovar el token de Instagram cada semana (caduca a los 60 días).

Prueba sin publicar nada: Actions → «Preparar y publicar en Instagram» → Run workflow → marcar «Simulación».

## Créditos
- Fuente Anton (`render/Anton.woff2`): SIL Open Font License 1.1.
- Fotos: cada imagen lleva su crédito y licencia en la propia diapositiva.
