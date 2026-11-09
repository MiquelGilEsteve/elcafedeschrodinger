# Instrucciones para Claude — repositorio del publicador de @elcafedeschrodinger

Este repositorio publica **automáticamente** en Instagram (sin revisión de Miquel: lo decidió el 2026-11-09). Lo que se suba a `main` en `posts/` sale publicado a su hora. Máximo cuidado con datos, ortografía y licencias de las fotos.

Las reglas de contenido (estilo IMPACTO, rigor, titulares, horarios, registro) están en la guía del proyecto de claude.ai «Cuenta Instagram tecnología»: `claude/guia.md` y `claude/fuentes.md`.

## Estilo pedido por Miquel (2026-11-09) — manda sobre la guía
- **Todos los posts sensacionalistas, pero verdaderos.** Ya no «1 de cada 3»: SIEMPRE titular de máximo impacto en la portada.
  Técnicas: la cifra más llamativa primero (62 %, 481 m, 4.100 millones de años), «por primera vez», récords, contrastes, consecuencias concretas.
  Ejemplo: mejor «Los expertos dan un *62 %* de probabilidad a un desastre causado por la IA antes de 2050» que «Dicen que la IA podría acabar con la humanidad. Esto es lo que dicen los datos».
  Límites que no cambian: cada cifra verificada en la fuente original; si un dato tiene letra pequeña (definiciones, condiciones), se cuenta en la diapositiva 2 o 3; nada falso ni engañoso; en salud, nada alarmista (Meta lo penaliza).
- **Portada SIEMPRE con foto real** si existe alguna con licencia libre que muestre el tema o algo directamente relacionado (lugar, objeto, nave, animal, máquina). Para temas abstractos (IA, matemáticas…), una foto real relacionada (p. ej. un superordenador de la NASA). Nunca fotos de personas famosas, de películas o de medios.
- Truco Wikimedia: `https://commons.wikimedia.org/wiki/Special:FilePath/<Nombre_del_archivo.jpg>` redirige al archivo original (GitHub sigue la redirección). Comprobar antes la licencia en la página del archivo.

## Añadir una publicación
0. **La carpeta `posts/` es también el registro de lo ya publicado** (los que tienen `publicado.json`): no repitas tema ni categoría del día anterior mirando ahí y en el registro de la guía. Primera publicación real: 2026-11-09, «La IA y el fin de la humanidad: los datos» (categoría IA).
   **Antes de nada, mira la cola** (`posts/*/post.json` sin `publicado.json`): si ya hay un post para la franja de hoy (España o LATAM), no prepares otro para esa franja; prepara solo la que falte. Ejemplo: el martes 2026-11-10 la franja de España (14:00) ya la ocupa la Voyager, así que ese día solo se prepara el post de LATAM.
1. Carpeta `posts/AAAA-MM-DD_<es|latam>_<tema>/` con un `post.json` (formato en README.md). Campos clave:
   - `publicar`: fecha y hora ISO **con desfase**. España: `+01:00` en horario de invierno, `+02:00` en verano. LATAM: 20:00 de Ciudad de México = `T20:00:00-06:00`.
   - `audiencia`: `ES` o `LATAM`.
   - `diapositivas` (5) con `texto`, y `svg` en todas (ilustración de reserva). Donde haya foto real: `foto_url`, `credito` y, si hace falta, `foto_pos` (p. ej. `"center 8%"`).
   - `story` y `pie` (≤ 2200 caracteres, ≤ 30 hashtags, siempre `#elcafedeschrodinger`).
   - La story usa sola la foto de la portada (con su `foto_pos`); se puede cambiar con `foto_url`/`foto_pos` propios dentro de `story`. Si falta `img/story.jpg`, GitHub rehace solo la story.
   - `story_auto`: `false` mientras la cuenta sea de creador (la API solo publica stories en cuentas de empresa).
2. **Fotos reales (`foto_url`)**: desde la sesión de Claude no se pueden descargar, pero GitHub Actions sí. Hay que dar la URL directa del archivo:
   - NASA Photojournal: abrir con WebFetch `https://science.nasa.gov/photojournal/<titulo>/` y usar el JPG de resolución completa: `https://assets.science.nasa.gov/content/dam/science/psd/photojournal/pia/piaNN/piaNNNNN/PIANNNNN.jpg`. (La antigua `photojournal.jpl.nasa.gov/jpeg/...` ya no funciona.)
   - Wikimedia Commons: la URL `https://upload.wikimedia.org/...` del archivo original, comprobando la licencia en la página del archivo (dominio público, CC BY o CC BY-SA; nunca NC).
   - Si la descarga falla, GitHub usa el `svg` y no muestra el crédito.
3. Probar el render en local antes de subir (con `svg`): `python scripts/preparar.py` y revisar `posts/*/img/*.jpg`; después **borrar** `img/` y `pie.txt` para que GitHub lo renderice con las fotos.
4. `git add`, commit y `git push origin main`. El workflow arranca solo.
5. Comprobar que el run terminó bien: `curl -s https://api.github.com/repos/MiquelGilEsteve/elcafedeschrodinger/actions/runs?per_page=1`; luego `git pull` y revisar visualmente `posts/<id>/img/01.jpg` (¿salió la foto?, ¿encuadre?, ¿texto legible?). Si algo está mal: corregir, borrar `img/` y volver a subir.

## Borradores
- Un `post.json` con `"borrador": true` se renderiza (con fotos) pero NO se publica. Sirve para enseñarle la imagen a Miquel antes. Al aprobarlo: quitar `borrador` y ajustar `publicar`. Cuenta como franja ocupada.

## Rehacer o anular un post
- Rehacer imágenes: borrar `posts/<id>/img/` y subir.
- Anular: borrar la carpeta del post antes de su hora.
- Un post ya publicado tiene `publicado.json`: no tocarlo.
- Si la hora de un post pasó hace más de 6 h, no se publica solo (cambiar `publicar`).

## Commits
Autor: Miquel Albert <MiquelGilEsteve@users.noreply.github.com>. Terminar el mensaje con las líneas de atribución de Claude que indique la sesión.
