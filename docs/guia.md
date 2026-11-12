# El Café de Schrödinger — guía de la cuenta de Instagram

Nombre de la cuenta: **El Café de Schrödinger** · usuario **@elcafedeschrodinger** · hashtag propio #elcafedeschrodinger (antes «Dato Cuántico», @datocuantico; cambiado el 2026-10-20).

Cuenta de Miquel sobre novedades y curiosidades de ciencia y tecnología. Claude prepara el contenido y Miquel lo publica a mano (puede programarlo en Meta Business Suite).

**Cambio (2026-11-11):** la tarea diaria pasa a ser una tarea programada de Claude Code, «El Café de Schrödinger – posts diarios (Code)», con el repositorio MiquelGilEsteve/elcafedeschrodinger. La guía y las fuentes que valen a partir de ahora son `docs/guia.md` y `docs/fuentes.md` **del repositorio**; esta copia del Project queda como referencia y puede quedarse atrás. La tarea antigua («Chat», dentro de este Project) se desactiva.

**Estado (2026-11-09):** la cuenta se creó el 2026-11-09. Hasta esa fecha no se había publicado nada: los posts del registro anteriores a la Voyager (2026-11-10) son **reserva sin publicar**; se pueden rehacer en estilo IMPACTO (volviendo a verificar los datos) para días flojos. Primera publicación: Voyager 1 a un día luz.

**Pendiente (2026-11-10):** los cambios de Reels, palabras clave y hashtags del repositorio están en `claude/parche_reels_2026-11-10.patch` (no se pudieron subir: push con 403). Si en el repositorio `scripts/preparar.py` todavía no tiene `montar_reel`, aplicar el parche (`git apply`) antes de preparar posts, comprobarlo con `python scripts/preparar.py` y subirlo. (2026-11-11: sigue sin aplicar en el repositorio.)

**Pendiente (2026-11-11):** los posts del 11-nov (mula de Lebrija, ES; cachalote de Perú, LATAM) están en `claude/posts_2026-11-11.patch` (`git am`) porque el push dio 403. El post LATAM del 10-nov (Doomsday 1960) tampoco llegó al repositorio.

## Logo actual
**El logo de la cuenta es la caricatura de Miquel** (ilustración con la taza de café, 1024×1536) que él pasó en un chat (confirmado 2026-11-09). Sustituye al logo anterior de la taza con el gato cuántico (`claude/logo.py`), que queda solo como reserva. Si la imagen no está en los archivos del proyecto ni en la sesión, pedírsela a Miquel. `render_impacto.py` la recorta solo (mismo encuadre que la foto de perfil: cara + taza).

## Perfil (aplicado 2026-11-09)
- Foto de perfil: caricatura recortada (160,130,800,770) a 1080×1080 (cara, corbata y taza). Miquel la sube a mano.
- Nombre: «Ciencia y tecnología en 1 café» (cuenta para la búsqueda; Instagram solo deja cambiarlo 2 veces cada 14 días).
- Bio: «☕ Ciencia y tecnología para tomar con café / 🔬 Lo nuevo y lo más curioso, explicado claro / 📚 Siempre con fuentes / 👇 Dos posts nuevos cada día».
- Cuenta de creador, categoría «Ciencia, tecnología e ingeniería» (visible en el perfil). Cuenta pública.
- Historias destacadas: Espacio, IA y tecno, Cuerpo, Animales, Historia, Física, Fuentes (portadas generadas con `claude/destacadas.py`: fondo azul marino con icono de trazo blanco y amarillo). Cada story de un post se añade a su destacada.

## Qué se entrega en cada ejecución (desde 2026-11-09: DOS publicaciones al día)
Petición de Miquel (2026-11-09): **dos publicaciones diarias, una para España y otra para LATAM, cada una a su mejor hora** (ver «Horarios»). Para cada una:
1. **Un carrusel de 5 diapositivas** (1080×1350) sobre una noticia o curiosidad llamativa y verificable de los últimos días.
2. **Una story** (1080×1920) que anuncia ese carrusel.
3. **El pie de foto**, con las palabras clave del tema en la primera línea, fuentes y **3-5 hashtags descriptivos** (ver «Crecer»).
4. **La hora a la que publicarla** (en hora de Madrid; para LATAM también en hora local de CDMX, Bogotá/Lima y Buenos Aires, calculada para esa fecha).
5. **Un Reel** (desde 2026-11-10): lo genera y publica solo el repositorio a partir de las 5 diapositivas (ver «Crecer»). No hay que escribir nada aparte; revisar un fotograma.

- Los dos temas deben ser distintos y de categorías distintas.
- Post LATAM: español neutro (sin «vosotros» ni expresiones solo de España: «computadora» mejor que «ordenador», «celular» o «teléfono» mejor que «móvil»). Si hay una buena noticia relacionada con Latinoamérica, darle prioridad.
- Post España: puede usar español de España; si hay una buena noticia relacionada con España (CSIC, universidades españolas), darle prioridad.

Se alternan temas: espacio, tecnología/IA, misterio, cuerpo humano y salud, animales y naturaleza, física y química, historia y arqueología. No repetir la categoría del día anterior (comprobar el registro de abajo).

**Ideas de arranque aprobadas por Miquel (2026-11-09)**, por orden: Voyager 1 a un día luz (hecha) · seta *Lanmaoa asiatica* que hace ver «gente diminuta» sin psicodélicos conocidos (Univ. de Utah, Mycologia 5-jun-2026; decir que es tóxica) · la constante G sigue sin cuadrar (NIST, Metrologia 16-abr-2026, 0,0235 % de diferencia, el sobre sellado) · chatbot que reduce el rendimiento (post del 28-oct) · ordenador de ADN de Maynooth (Nature, sept. 2026) · Leónidas, máximo 17-nov 23:45 UTC, ~15/h (publicar el 16 o 17).

## Crecer: Reels, envíos y palabras clave (decidido por Miquel el 2026-11-10)
Según Adam Mosseri (Instagram, recogido por Buffer en 2026), las señales que más cuentan son el tiempo de visualización, los «me gusta» y los **envíos** por mensaje privado (estos pesan algo más para llegar a no seguidores). Los hashtags no dan alcance; las palabras clave sí ayudan en el buscador. Buffer (más de 4 millones de posts): los Reels alcanzan un 36 % más que los carruseles y los carruseles consiguen un 12 % más de interacción.
1. **Reels:** cada post genera también un Reel vertical de ~20 s (una frase cada 4,5 s con fundidos), que se publica automáticamente justo después del carrusel como **Reel de prueba** (primero solo a no seguidores; Instagram lo pasa a los seguidores si funciona). **Sin música**: la API no puede usar la biblioteca de Instagram y Miquel eligió automático sin música. Detalles técnicos en el CLAUDE.md del repositorio.
2. **Envíos:** la portada tiene que entenderse sola, sin leer el pie (qué pasó + la cifra o el dato sorprendente). Pensar «¿se lo mandaría alguien a un amigo?».
3. **Palabras clave mejor que hashtags:** la primera línea del pie dice claramente de qué va el post con las palabras que buscaría la gente (p. ej. «Fin del mundo el 13 de noviembre de 2026: la predicción de Science de 1960 y por qué falló»). Los nombres propios del tema también en el texto de las diapositivas. **Solo 3-5 hashtags descriptivos**, siempre #elcafedeschrodinger; nada de genéricos (#curiosidades, #datoscuriosos).

## Horarios (decididos 2026-11-09)
No hay un estudio sólido por país: los rankings de herramientas (Buffer, SocialPilot, Metricool, SchedPilot) se contradicen y algunos no citan datos. Son un punto de partida; **revisar en Instagram Insights (Estadísticas > Público > Horas más activas, y países/ciudades de los seguidores) tras 2-3 semanas** y ajustar.

**España** (hora peninsular). Ventana fuerte por la noche (21:00-22:30) y segunda a mediodía (13:30-15:30), según SchedPilot; Buffer (9,6 millones de posts, enero 2026) también sitúa las mejores horas de varios días por la noche.
| Día | Hora recomendada |
|---|---|
| Lunes | 21:00 |
| Martes | 14:00 |
| Miércoles | 21:00 |
| Jueves | 20:45 |
| Viernes | 14:00 |
| Sábado | 12:00 |
| Domingo | 19:00 |
Ventaja: a las 21:00 de Madrid son las 14:00 en Ciudad de México en invierno (13:00 en verano español), hora de comida allí, así que el post de España también capta algo de México.

**LATAM**: una sola hora que encaja con la noche de varios países: **20:00 en Ciudad de México** = 21:00 Bogotá y Lima = 23:00 Buenos Aires = 23:00 Santiago (verano chileno; 22:00 en su invierno).
- En hora de Madrid: **03:00** con el horario de invierno español (hasta el 28-mar-2027) y **04:00** con el horario de verano (México ya no cambia la hora). Miquel tiene que **programarlo** en Meta Business Suite.
- Ventanas de noche locales (SchedPilot): CDMX 20:00-22:00 · Bogotá 19:00-21:00 · Lima 19:30-21:30 · Buenos Aires 21:30-23:30 · Santiago 20:30-22:30. México es el mercado más grande, por eso se ancla en CDMX.
- Si Insights muestra que la mayoría de seguidores de LATAM está en Argentina, mover a 21:00-21:30 CDMX.

## Estilo IMPACTO (desde 2026-11-09)
Miquel pidió el formato de la cuenta @increibleshechos (183 mil seguidores, curiosidades virales). Pendiente de que confirme si sustituye al estilo claro o se alternan; mientras tanto, usar IMPACTO (es lo último que pidió).
- Renderizador: `claude/render_impacto.py`. Uso: `python3 render_impacto.py post.json salida/`. Ejemplo: `claude/ejemplo_impacto_tunnug.py`.
- Cómo es: imagen a sangre arriba (920 px de alto) que se funde con negro; abajo, titular enorme en mayúsculas con la fuente **Anton** (letra estrecha), centrado, blanco, con 1-2 palabras resaltadas (`*así*` amarillo #FFD84D, `_así_` azul claro #7FA0FF); insignia redonda arriba a la izquierda con la **caricatura de Miquel** recortada en círculo y borde amarillo (si no está disponible, sale el logo antiguo de la taza y el script avisa); «— ELCAFEDESCHRODINGER —» pequeño abajo.
- Todas las diapositivas tienen el mismo esquema: una imagen y una frase. El texto se ajusta solo de tamaño (empieza a 104 px y baja hasta caber en 470 px de alto). Cada diapositiva cuenta un paso de la historia; la última lleva la línea de fuentes (campo `fuente`).
- **Composición de la imagen:** el degradado a negro empieza hacia y≈560 y el texto puede subir hasta y≈870; dejar lo importante de la ilustración por encima de y≈620 y no poner etiquetas cerca del borde derecho (se cortan). La insignia ocupa la esquina superior izquierda (x<160, y<160): no poner etiquetas ahí.
- Story: imagen de 1300 px, titular y botón amarillo «NUEVO POST ↓».
- Reel (1080×1920): mismo esquema por frase; la ilustración SVG va a 920 px de alto sin recortar y la foto a 1050 px; el texto queda en la zona segura (Instagram tapa ~380 px abajo y una columna a la derecha).
- La fuente Anton se descarga sola con npm (`@fontsource/anton`) si no está junto al script.
- Ilustraciones SVG de esta plantilla: lienzo 1080×920 (post) y 1080×1300 (story), fondo de cielo azul marino que oscurece hacia abajo, trazos blancos, acento amarillo. Mejor con foto real (`foto` + `credito`, mismas reglas de licencia de abajo).
- Lo que NO se copia de @increibleshechos: sus titulares exagerados («los científicos no tienen idea…») y sus imágenes generadas con IA. Se mantienen las reglas de titulares verdaderos y de rigor de esta guía. Si Miquel decide usar recreaciones con IA, irán siempre etiquetadas «Recreación artística (IA)» y nunca para inventar la prueba de un hallazgo.

## Plantilla
- Renderizador: `claude/render.py` (Python + Playwright). Uso: `python3 render.py post.json salida/`.
- Ejemplo completo: `claude/ejemplo_taurides.py` (genera el JSON con ilustración SVG).
- Tipos de diapositiva: `portada`, `dato`, `tarjetas` (4), `lista` (3-4 puntos), `cierre`, y `story`.
- En textos: `*así*` → resaltado amarillo; `_así_` → azul. Máximo 1-2 resaltados por diapositiva.
- Estructura habitual: portada → dato clave → contexto (tarjetas o lista) → detalle/por qué importa → cierre.
- **Imágenes: foto real** en portada, cierre y story (petición de Miquel, 2026-10-20). Campos `foto` (ruta al archivo, relativa al JSON) y `credito` (obligatorio, p. ej. «Foto: NASA/JPL · Dominio público» o «Foto: Autor · CC BY-SA 4.0 · Wikimedia Commons»).
  - Solo fotos con licencia que permita reutilizarlas: dominio público (NASA, NOAA, USGS, NPS y otras agencias federales de EE. UU.), CC BY / CC BY-SA (Wikimedia Commons, ESA, artículos open access con CC BY). Comprobar la licencia en la página del archivo. **Nunca** fotos de medios (Live Science, Gizmodo…), de agencias de prensa ni de webs sin licencia libre, ni con CC BY-NC si la cuenta puede monetizarse.
  - La foto debe mostrar lo real del tema (el lugar, el objeto, el animal, la nave), no un recurso genérico.
  - Si no se puede descargar una foto con licencia válida (por ejemplo, porque el dominio está bloqueado en la sesión), usar la ilustración SVG (`svg`, lienzo 952×600, 952×420 y 952×820; un objeto central simétrico, trazos blancos, acento #FFD84D) y avisar a Miquel en el resumen.
  - Nota 2026-10-21: en la sesión programada en la nube, el proxy bloqueó (403) usgs.gov, assets.science.nasa.gov, images-assets.nasa.gov, eoimages.gsfc.nasa.gov, upload.wikimedia.org y commons.wikimedia.org. Se usó SVG y se pasaron a Miquel los enlaces de las fotos válidas.
  - Nota 2026-10-22: siguen bloqueados (403) también www.nasa.gov, science.nasa.gov, jpl.nasa.gov, mars.nasa.gov, photojournal.jpl.nasa.gov, images.nasa.gov y www.esa.int. Para tener fotos reales en las ejecuciones programadas, Miquel tendría que permitir esos dominios en Ajustes > Capacidades de claude.ai.
  - Nota 2026-10-23: también bloqueados (403, «policy denial») www.noaa.gov, www.nps.gov, www.fws.gov, eurekalert.org, zenodo.org, inaturalist.org (y su S3), subtbiol.pensoft.net y doi.org. Desde el shell solo hay salida a registros de paquetes (pypi, npm). Comprobar rápido con `curl -s -o /dev/null -w '%{http_code}' URL` antes de buscar fotos.
  - Nota 2026-10-26: sigue igual (curl a upload/commons.wikimedia.org, images-assets.nasa.gov, www.esa.int y www.nasa.gov sin conexión; WebFetch a commons.wikimedia.org también falla). Se usó SVG.
  - Nota 2026-10-28: sigue igual (curl a esos mismos hosts sin conexión; pypi.org sí responde). Se usó SVG (reloj de arena). Playwright y la fuente Inter ya vienen instalados en el entorno.
  - Nota 2026-11-02: sigue igual (curl a assets.science.nasa.gov también sin conexión). WebFetch sí lee las páginas science.nasa.gov/?p=… del Photojournal (útil para sacar créditos y URL de las fotos y pasárselas a Miquel), pero el archivo no se puede descargar. Se usó SVG (meteorito).
  - Nota 2026-11-03: sigue igual (curl a wikimedia, images-assets.nasa.gov y esa.int sin conexión). Además, WebFetch falló en pnas.org, phys.org y scitechdaily.com; sciencealert.com, iflscience.com, miragenews.com (reposta notas de prensa de universidades) y agenciasinc.es sí se leen. Se usó SVG (araña dormida).
  - Nota 2026-11-04: sigue igual (curl a wikimedia, images-assets.nasa.gov, esa.int y nasa.gov sin conexión; pypi sí). WebFetch sí lee sciencedaily.com/news, sci.news (buenos índices de titulares recientes con fecha), earthsky.org y science.nasa.gov/?p=…. Se usó SVG (sonda Voyager).
  - Nota 2026-11-05: sigue igual (curl a wikimedia, images-assets.nasa.gov, esa.int y nasa.gov sin conexión). WebFetch sí lee curtin.edu.au, livescience.com y sciencealert.com. Se usó SVG (hueso con lupa).
  - Nota 2026-11-06: sigue igual (curl a wikimedia, images-assets.nasa.gov, esa.int y nasa.gov sin conexión; pypi sí). WebFetch sí lee frontiersin.org (artículo completo /full). Se usó SVG (dos hemisferios con vías cruzadas en X).
  - Nota 2026-11-09: sigue igual (curl a wikimedia, images-assets.nasa.gov, esa.int y nasa.gov sin conexión; pypi sí). WebFetch sí lee popsci.com, news-medical.net y las notas de AP repostadas en webs de TV locales (ksat.com, clickondetroit.com), útiles para opiniones de expertos independientes. Se usó SVG (túmulo funerario en corte).
  - Nota 2026-11-10: desde 2026-11-09 las fotos las descarga GitHub Actions (`foto_url`, ver CLAUDE.md del repositorio). WebFetch sí lee svs.gsfc.nasa.gov (NASA Scientific Visualization Studio: páginas con la lista de archivos y URL directas, p. ej. Black Marble 2016 en svs.gsfc.nasa.gov/30876); curl desde la sesión no llega. WebFetch a commons.wikimedia.org/wiki/File:… sigue fallando (no se puede comprobar la licencia de Commons desde la sesión). **En la ejecución programada del 10-nov no había forma de añadir el repositorio a la sesión y el push dio 403**: hay que autorizar el repositorio en la tarea programada.
  - Nota 2026-11-11: **Firecrawl (`mcp__Firecrawl__firecrawl_scrape`) sí lee commons.wikimedia.org/wiki/File:… y las categorías** (licencia, autor, URL directa de upload.wikimedia.org), además de nature.com (artículo completo, licencia CC BY de las figuras), doi.org y sciencedirect.com (resumen). curl a upload.wikimedia.org y media.springernature.com sigue bloqueado: las fotos se ven solo cuando las renderiza GitHub. **El push volvió a dar 403** (el repositorio no está autorizado en la tarea programada); se guardó el parche en `claude/posts_2026-11-11.patch` y se envió un zip a Miquel.

## Por qué este diseño (lo que dicen los datos)
- Curalate (2013, 8 millones de fotos de Instagram): tonos azules +24 % de "me gusta" frente a rojos; imágenes claras +24 % frente a oscuras; poca saturación +18 %; un color dominante +17 %.
- Int. Journal of Research in Marketing (≈150.000 posts de marcas): mejor pocos colores y algo apagados, luminosidad media, 1-2 objetos y composiciones simétricas.
- Paleta: fondo claro azulado #EEF2F8, texto azul marino #0B1A3A, acento azul #2A4BFF, resaltado amarillo #FFD84D.
- Tipografía: Inter Display Black para titulares (grande, legible en móvil), Inter para el texto. No hay estudios sólidos sobre tipografías concretas en Instagram; se prioriza legibilidad en pantalla pequeña.
- Nota: el estilo IMPACTO (fondo negro) va en contra del dato de Curalate sobre imágenes claras, pero es el formato que usan cuentas de curiosidades con mucho alcance. Conviene comparar las métricas de ambos estilos.

## Titulares "de impacto" (sensacionalistas pero verdaderos)
Aproximadamente **1 de cada 3 posts** con titular de máximo impacto (el CLAUDE.md del repositorio manda: desde 2026-11-09, siempre). Reglas:
- Gancho fuerte con **dato verdadero y concreto**: cifras, récords, "por primera vez", contraste sorprendente.
- Superlativos solo si la fuente los respalda. Nada de "los científicos alucinan", "esto lo cambia todo" si no es así.
- **Evitar titulares en forma de pregunta** en la portada: en un estudio con KQED restaron credibilidad a noticias científicas.
- El clickbait vacío no consigue más clics de forma fiable (estudios de Penn State).
- **No pedir interacción explícita** ("comenta SÍ", "etiqueta a…", "comparte si…"): Instagram dejó de recomendar este tipo de posts a no seguidores. Preguntas abiertas al final del pie sí están bien.
- Salud: nada de afirmaciones sensacionalistas o exageradas (Meta las penaliza) ni consejos médicos.
- Temas de drogas (aunque sean históricos): evitarlos en los primeros posts de la cuenta y no usar hashtags como #cannabis.

## Rigor
- Fuentes: ver `claude/fuentes.md` (manda sobre esta lista). Preferidas: NASA, ESA, Agencia SINC, Nature, Science, New Scientist, Live Science, MIT Technology Review, Xataka, comunicados de universidades/CSIC.
- Cada cifra debe estar en una fuente consultada en esa ejecución. Si un dato no se puede verificar, se quita.
- Si dos fuentes dan cifras u horas distintas, manda la fuente oficial (p. ej. la NASA). Ejemplo: EarthSky daba para la Voyager 12:16 CST (06:16 UTC) y la NASA da 5:16:07 a. m. EST = **10:16 UTC**; la buena es la de la NASA.
- Citar fuentes en la última diapositiva con contenido y en el pie. No copiar frases de los artículos: redactar con palabras propias.
- Fechas: comprobar que el evento no ha pasado y que la noticia es reciente (idealmente últimos 7 días).
- Ojo: ScienceDaily a veces repone comunicados antiguos con fecha nueva (p. ej. el caracol de cueva *Erhaia dijiang*, comunicado de abril de 2026; el cráter Silverpit, artículo de 2025; el simio fósil *Masripithecus* de Egipto, julio de 2026, repuesto el 1-nov-2026; el pez killi *Laimosemion laranja* de Amapá, Brasil, nota de Pensoft del 22-sep-2026, repuesto el 8-nov-2026). Comprobar la fecha de publicación del artículo original.
- Truco: arxiv.org (abs y html) sí se puede leer con WebFetch; útil para sacar las cifras exactas de un preprint.
- La fuente Anton no tiene comillas latinas («»): en el texto de las diapositivas salen como «<<» y «>>». No usarlas en diapositivas (sí en el pie).
- En los textos, usar espacio de no separación antes de «%» ( ) para que «65 %» no se parta entre líneas. También sirve para mantener juntas expresiones resaltadas en la portada (p. ej. «un día luz»).
- Titulares de portada: caben unas 2-3 líneas a 92 px; con 4 líneas el titular choca con la línea de «Fuente». Mejor antetítulo con contexto + titular corto.
- Si el artículo es una hipótesis o revisión (no un experimento), decirlo claramente en el cierre y en el pie.
- Si la foto de portada no es el objeto exacto del estudio (p. ej. otro fósil del mismo yacimiento, otra mula), decirlo en el crédito y en el pie («no es el ejemplar del estudio»).

## Registro de publicaciones preparadas
(Hasta el 2026-11-09 la cuenta no existía: lo anterior a la Voyager del 10-nov está sin publicar.)
- 2026-10-19 · Espacio · Táuridas del Sur, pico de bolas de fuego 4-5 nov (ejemplo inicial; ya pasado)
- 2026-10-20 · Historia/Arqueología · Campamento de 13.800 años en Alaska (Shég' Xdaltth'i'): posible vivienda más antigua de América y agujas con ojo más antiguas (titular de impacto)
- 2026-10-21 · Tierra/Naturaleza · Megatsunami de Tracy Arm (Alaska, 10-ago-2025): ola que subió 481 m, el segundo tsunami más alto medido (ilustración SVG: hosts de fotos bloqueados)
- 2026-10-22 · Espacio · Perseverance bate el récord de distancia fuera de la Tierra: 45,22 km (supera a Opportunity, 45,16 km) (titular de impacto; ilustración SVG de huellas de rueda: hosts de fotos bloqueados)
- 2026-10-23 · Animales/Naturaleza · Corales blanqueados que se recuperan en 7 semanas al tocar a un gemelo sano (Stanford, Science Advances 14-oct-2026) (ilustración SVG de dos corales: hosts de fotos bloqueados)
- 2026-10-26 · Historia/Física · Al reactor nuclear nazi B8 de Heisenberg (Haigerloch, 1945) le faltaba la mitad del uranio y más de la mitad del agua pesada (Park et al., PNAS Nexus 29-sep-2026) (titular de impacto; ilustración SVG de cubos colgando: hosts de fotos bloqueados)
- 2026-10-28 · Tecnología/IA · Sesiones de 13-15 min con un chatbot (GPT-5) reducen el rendimiento y la persistencia al quitarlo: 57 % vs 74 % resueltos, 20 % vs 11 % abandonos (Liu et al., arXiv:2604.04721, COLM 2026; 1.222 participantes) (titular de impacto; ilustración SVG de reloj de arena: hosts de fotos bloqueados)
- 2026-11-02 · Espacio · Meteorito marciano Teghaza 001 (Sáhara, Malí): al menos 4.100 millones de años, 8 fragmentos, 798,5 g (Liu et al., Science 29-oct-2026) (ilustración SVG de meteorito: hosts de fotos bloqueados)
- 2026-11-03 · Animales · La araña saltadora *Portia fimbriata* duerme en dos fases, una tipo REM; tras una noche sin dormir, casi un 80 % más de sueño tipo REM (Geiger et al., PNAS 26-oct-2026, Univ. de Bonn) (ilustración SVG de araña dormida: hosts de fotos bloqueados)
- 2026-11-04 · Espacio · Voyager 1 llegará a un día luz de la Tierra el 18-nov-2026 (**corregido 2026-11-09: 10:16:07 UTC según la NASA, no 06:16**; 25.902 millones de km, señal de 24 h); primera vez para un objeto humano (NASA, blog Voyager 29-oct-2026) (titular de impacto; ilustración SVG de la sonda: hosts de fotos bloqueados)
- 2026-11-05 · Paleontología · Hemo y posibles glóbulos rojos mineralizados en un hueso de *Aratasaurus museunacionali* de 115 millones de años (Brasil) (Grice et al., PNAS 2-nov-2026, Curtin Univ.; con la crítica de M. Schweitzer) (ilustración SVG de hueso con lupa: hosts de fotos bloqueados)
- 2026-11-06 · Cuerpo humano · Por qué cada hemisferio controla el lado contrario del cuerpo: hipótesis de que el cruce viene de la vista de peces del Cámbrico (>500 millones de años) y se mantuvo por «coste de cableado» (Wessendorf y Wang, Frontiers in Neuroanatomy 27-oct-2026, Univ. de Minnesota) (titular de impacto; ilustración SVG de hemisferios con vías cruzadas: hosts de fotos bloqueados)
- 2026-11-09 · Historia/Arqueología · Cannabis psicoactivo hace 2.800 años: unas 1.000 semillas (s. VIII a. C.) y CBN en pelo humano en la tumba escita de Tunnug 1 (Tuva, Siberia); con la crítica de V. Auwärter (Caspari et al., Science 5-nov-2026, Univ. de Berna) (ilustración SVG de túmulo: hosts de fotos bloqueados; sin hashtag #cannabis para no arriesgar alcance). Rehecho el mismo día en estilo IMPACTO (primer post con esa plantilla). No usar como primeros posts de la cuenta.
- 2026-11-10 · ES + LATAM · Espacio · **PRIMERA PUBLICACIÓN DE LA CUENTA.** Voyager 1 a un día luz el miércoles 18-nov a las 10:16 UTC (11:16 España, 04:16 CDMX, 05:16 Bogotá/Lima, 07:16 Buenos Aires/Santiago); 25.900 millones de km; 49 años, 2 meses y 11 días desde el despegue (5-sep-1977); pierde unos 4 W al año (NASA Science y blog Voyager 29-oct-2026). Estilo IMPACTO, ilustración SVG (sonda, regla de 24 h, relojes de ida y vuelta, trayectoria 1977-2026, batería). Repetir story el día 18.
- (Nota: según el repositorio, el 2026-11-09 se publicaron en realidad «La IA y el fin de la humanidad» (IA), los Illuminati (Historia), el coste del iPhone 18 Pro Max (Tecnología) y la encuesta sobre vida extraterrestre (Espacio). La carpeta `posts/` del repositorio es el registro fiable de lo publicado.)
- 2026-11-10 · ES · Espacio · Voyager 1 a un día luz (ya estaba en la cola del repositorio; martes 14:00 Madrid). No se preparó otro post para España.
- 2026-11-10 · LATAM · Ciencia/Matemáticas (demografía) · El artículo de Science de 1960 «Doomsday: Friday, 13 November, A.D. 2026» (von Foerster, Mora y Amiot, Univ. de Illinois; 2026,87 ± 5,5 años; 24 estimaciones de población) y por qué falló (desvío hacia 1993; ONU WPP 2024: 8.200 millones en 2024, máximo de ~10.300 millones a mediados de los 2080) · 20:00 CDMX = 03:00 Madrid (11-nov) · Portada: NASA Goddard/SVS, Black Marble 2016. **No se pudo subir a GitHub** (push con 403); se envió el post.json a Miquel para que lo suba a mano. Primer post con Reel, palabras clave y 5 hashtags.
- 2026-11-11 · ES · Misterio/Física · La teoría del «campo de conciencia» (al morir la mente se «reintegraría» en un campo universal) de Maria Strømme (Univ. de Uppsala), publicada en AIP Advances 15, 115319 (13-nov-2025) y **retirada el 7-may-2026** porque su operador central no es medible y la teoría no es falsable · miércoles 21:00 Madrid · tema elegido por Miquel (test de Muy Interesante, 19-mar-2026, anterior a la retirada) · Portada: recreación artística con IA aportada por Miquel (`portada.jpg` en la carpeta del post, crédito «Recreación artística (IA)»). Sustituye a la mula de Lebrija y a la pastilla Foundayo, que quedan en reserva (`claude/reserva_mula_lebrija_post.json`, `claude/reserva_pastilla_glp1_post.json`; antes de usar Foundayo, comprobar si la Comisión Europea ya lo autorizó).
- 2026-11-11 · LATAM · Animales/Paleontología · *Scaphokogia huachafo*, cachalote pigmeo fósil de Sacaco (Arequipa, Perú), 6,3-5,6 Ma, ~2,7 m, hocico 31° hacia abajo; cara más asimétrica conocida en cetáceos (31 especies comparadas), quizá en mamíferos (Benites-Palomino et al., Commun. Biol. 9-nov-2026) · 20:00 CDMX = 03:00 Madrid (12-nov) · Portada: fósil de ballena en Sacaco, Walt paz, CC BY-SA 4.0. **No subido a GitHub** (push 403).
- 2026-11-12 · ES · Historia/Arqueología · Cuero de cabra de 7.000 años (7.246-7.008 cal BP) de la Cueva de los Murciélagos (Albuñol, Granada): cabra doméstica hembra, 4 perforaciones, raza actual más afín la bermeya (Asturias), sin ascendencia africana, ADN humano y de cánido; primer ADN nuclear de cabra doméstica ibérica (Erven et al., PLOS ONE 4-nov-2026) · jueves 20:45 Madrid · Portada: entrada de la cueva, Loscast, CC BY-SA 4.0 (Commons); diapositiva 2: foto del cuero, figura 2 del artículo, CC BY 4.0. Ojo: Xataka lo llamó «el cuero más antiguo del mundo», el artículo no lo dice.
- 2026-11-12 · LATAM · Espacio · Nāpōwawāʻenakaulua (J1602+4228AB): pareja compacta de cuásares más antigua (z≈6,08, 900 Ma tras el Big Bang), 18.100 años luz de separación, 1.500 y 400 millones de masas solares; exceso de 100-1.000 veces sobre lo esperado; el artículo la llama «candidata» (Onorato et al., ApJL 1011, L59, 10-nov-2026; NOIRLab; Gemini Norte + JWST; coautora de la Univ. Diego Portales, Chile) · 20:00 CDMX = 03:00 Madrid (13-nov) · Portada: Gemini Norte y su láser, J. Chu/NOIRLab, CC BY 4.0 (Commons).

## Cambios del renderizador
- 2026-10-20: en `dato`, las cifras de más de 4 caracteres (p. ej. "13.800") se reducen a 250 px y sin interletraje negativo, porque a 300 px los dígitos se solapaban.
- 2026-10-20: soporte de `foto` + `credito` en los paneles (la foto se incrusta en base64).
- 2026-10-20: se probó una paleta sepia/dorada (estilo explorador). Miquel decidió mantener la paleta azul original.
- 2026-10-22: en `tarjetas`, el interletraje de la cifra grande pasa de -.03em a -.015em, porque en cifras como "45,16 km" los dígitos quedaban demasiado pegados.
- 2026-10-26: el resaltado amarillo (`*así*`) usa siempre texto azul marino (#0B1A3A). Antes heredaba el color del texto y, en la tarjeta oscura de `tarjetas`, quedaba texto claro sobre amarillo, ilegible.
- 2026-11-05: en `dato`, el interletraje de las cifras cortas (≤4 caracteres) pasa de -.05em a -.03em, porque en "115" los dos unos se tocaban.
- 2026-11-09: nuevo `render_impacto.py`. El script de autoajuste del texto va dentro de `document.fonts.ready` y en un bloque propio: con `const` a nivel global fallaba a partir de la 2.ª diapositiva (Playwright reutiliza la ventana) y el texto salía diminuto.
- 2026-11-09: `render_impacto.py` usa la caricatura de Miquel como insignia (campo `logo` o `logo.png` junto al script), recortada en círculo con borde amarillo y con el mismo encuadre que la foto de perfil (cara + taza), a petición de Miquel.
- 2026-11-10: Reels. `render_impacto.py` genera un fotograma vertical por diapositiva (`reel()`), `preparar.py` los une con ffmpeg en `img/reel.mp4` (4,5 s por frase, fundidos de 0,5 s, audio en silencio) y `publicar.py` lo publica tras el carrusel como Reel de prueba. En el Reel, la ilustración SVG va a 920 px de alto porque a 1150 px se recortaban los lados.
