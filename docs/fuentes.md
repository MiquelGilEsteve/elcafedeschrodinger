# El Café de Schrödinger — webs de donde se saca la información

Lista de fuentes para buscar temas y verificar datos. Se lee junto con `claude/guia.md`. Para añadir o quitar webs, editar solo este archivo.

**Regla de oro:** las webs de divulgación (Muy Interesante, Xataka, National Geographic, ScienceAlert…) sirven para **encontrar** el tema. Las cifras se comprueban en el estudio original o en la nota de prensa de la universidad/agencia, y se cita esa fuente original. Comprobar siempre la fecha del estudio original.

**Herramienta clave (2026-11-11):** si la sesión tiene el conector **Firecrawl** (`mcp__Firecrawl__firecrawl_scrape`, con `formats: ["query"]` o `["markdown"]`), lee muchas webs que WebFetch no puede: nature.com (artículo completo y licencia), doi.org → sciencedirect.com (resumen y fecha), commons.wikimedia.org (páginas File: y Category:, con licencia, autor y URL directa de upload.wikimedia.org) y URL muy largas (p. ej. notas de la Junta de Andalucía). Las imágenes en sí no las describe.

## 1. Para encontrar temas

### En español (pedidas por Miquel el 2026-11-09)
| Web | Cómo leerla desde la sesión | Notas |
|---|---|---|
| **Muy Interesante** (muyinteresante.okdiario.com) | WebFetch sí lee las secciones: /ciencia/, /historia/, /naturaleza/, /tecnologia/, /salud/ y /temas/… (universo, fisica, genetica, neurociencia, medicina) | Los listados **no muestran la fecha**: abrir el artículo o buscar el estudio original para comprobar que es reciente. Sus titulares tienden a exagerar («reescribe la historia», «revolución»): no copiarlos; aplicar las reglas de titulares de la guía. |
| **Xataka** (xataka.com) | WebFetch sí lee xataka.com/tag/ciencia (con fecha en cada artículo); también /tag/ciencia-y-tecnologia y las secciones espacio, investigacion, medicina-y-salud | Buena para tecnología e IA. El listado de /tag/ciencia no se actualiza a diario (el 11-nov su último artículo era del 22-oct): complementar con WebSearch («xataka» + tema). |
| **National Geographic España** (nationalgeographic.com.es) | La portada de /ciencia no se lee bien con WebFetch (solo sale un test). **Usar WebSearch con allowed_domains=["nationalgeographic.com.es"]**: los resultados traen el texto de los artículos. | Buena para naturaleza, animales, arqueología e historia. Su sección semanal «Las buenas noticias de la semana» reúne varios temas. |
| **Agencia SINC** (agenciasinc.es) | WebFetch sí la lee (la portada no muestra fechas) | Ciencia española (CSIC, universidades): ideal para el post de España. |
| **WebSearch «investigadores españoles descubren … [mes año]»** (modo extended) | — | 2026-11-11: así salió la mula de Lebrija (eldiario.es → nota de la UPO y de la Junta). Buenas notas oficiales: upo.es/diario, juntadeandalucia.es/presidencia/portavoz (esta última con Firecrawl: la URL es demasiado larga para WebFetch). |
| **Merca2.0** (merca20.com, México) | WebFetch sí la lee (2026-11-10) | Útil para ver qué temas de ciencia son virales en México; verificar siempre en la fuente original. |

### En inglés
- **sciencedaily.com/news** y **sci.news**: índices de titulares recientes con fecha (ojo: ScienceDaily a veces repone comunicados antiguos con fecha nueva). sci.news trae a menudo fósiles de Latinoamérica (2026-11-11: cachalote de Perú).
- **sciencealert.com**, **livescience.com**, **popsci.com**, **iflscience.com**, **earthsky.org** (astronomía).
- **miragenews.com**: reposta notas de prensa de universidades.

## 2. Para verificar los datos (fuente original)
- Revistas: **science.org**, **frontiersin.org** (artículo completo en /full), **arxiv.org** (abs y html, para preprints), **nature.com** (con Firecrawl; WebFetch falla). *PNAS no se lee* (buscar la nota de prensa de la universidad).
- Notas de prensa de universidades y centros (p. ej. curtin.edu.au, bath.ac.uk, Universidad de Berna, CSIC, news.uzh.ch de la Universidad de Zúrich, upo.es).
- **un.org** (ONU: World Population Prospects y otras cifras oficiales) se lee con WebFetch.
- **science.nasa.gov/?p=…** (misiones y créditos de fotos del Photojournal) y blogs de misiones de la NASA.
- **Associated Press** repostada en webs de televisiones locales de EE. UU. (ksat.com, clickondetroit.com, ny1.com): útil para la opinión de expertos que no participaron en el estudio.

## 3. Fotos con licencia libre
- **svs.gsfc.nasa.gov** (NASA Scientific Visualization Studio): WebFetch lee las páginas y da las URL directas de los archivos (JPG/PNG de alta resolución). Ejemplo: Black Marble 2016, la Tierra de noche (svs.gsfc.nasa.gov/30876). Galería de la Tierra de noche: svs.gsfc.nasa.gov/gallery/earthat-night-imagery/.
- **Wikimedia Commons con Firecrawl**: abrir la categoría (p. ej. Category:Mules_in_Andalusia, Category:Pisco_Formation) para ver los archivos y luego la página File: para la licencia y la URL directa.
- Artículos open access con licencia CC BY 4.0 (p. ej. Communications Biology): sus figuras se pueden reutilizar citando; las URL son media.springernature.com/full/… Ojo: suelen ser láminas con varios paneles y fondo blanco, poco aptas para portada.
- **NOIRLab** (noirlab.edu/public/images/…): fotos de Gemini, Rubin, Kitt Peak, Cerro Tololo con licencia **CC BY 4.0** (página /public/copyright/); muchas están también en Commons (Category:Gemini_North_Observatory), mejor usar Commons con `Special:FilePath/…?width=2000` porque los originales de NOIRLab pesan cientos de MB (2026-11-12).
- **PLOS ONE**: todo CC BY 4.0; figura directa en `journals.plos.org/plosone/article/figure/image?size=large&id=<doi>.g00N` (2026-11-12).
- **NOIRLab directo** (2026-11-14): las páginas noirlab.edu/public/images/<id>/ dan la URL `storage.noirlab.edu/media/archives/images/large/<id>.jpg` (≈1 MB, mejor que el original TIFF). Licencia CC BY 4.0. Las notas de prensa en español de NOIRLab se leen en newswise.com.
- earthobservatory.nasa.gov ahora redirige a science.nasa.gov/earth/earth-observatory/.

## 4. Lo que no funciona en la sesión (proxy)
- **2026-11-14: render local.** Tampoco venía el paquete `playwright` de Python: `python -m pip install playwright==1.63.0` (misma versión que el de Node) y lanzar con `executable_path="/opt/pw-browsers/chromium"` (un envoltorio que parchee `BrowserType.launch`, sin tocar el repositorio).
- **2026-11-13: render local.** El entorno no traía `requests` y el Pillow del sistema estaba roto: `python -m pip install requests` y `python -m pip install --ignore-installed pillow`. No instalar `playwright` con pip (cambia la versión y no encuentra el Chromium preinstalado); si pasa, lanzar con `executable_path="/opt/pw-browsers/chromium"`.
- **2026-11-12: WebFetch no resolvía ningún dominio** (ENOTFOUND en sciencedaily.com, sci.news y agenciasinc.es). Todo se leyó con **Firecrawl** (`firecrawl_scrape` con `formats: ["query"]`, y `firecrawl_search` con `sources: ["news"]` para noticias recientes de Latinoamérica). Los enlaces de la portada de SINC daban 404 vía Firecrawl: buscar el tema con `firecrawl_search`.
- WebFetch falla en: phys.org, scitechdaily.com, pnas.org, doi.org, nature.com, commons.wikimedia.org/wiki/File:… (url_not_found), krdo.com (robots), URL demasiado largas (juntadeandalucia.es). Varias se leen con Firecrawl (ver arriba).
- Los enlaces de Google (google.com/url?…) no se pueden abrir: usar la URL directa de la web.
- Para fotos: wikimedia, NASA Images, ESA, NOAA, NPS, USGS, svs.gsfc.nasa.gov, media.springernature.com… bloqueados para descargar desde la sesión (las descarga GitHub Actions).

## 5. Ideas para el post de LATAM
- **infobae.com/america/ciencia-america** (2026-11-13): buen índice de ciencia con foco latinoamericano, se lee con Firecrawl y enlaza el estudio original (así salieron los monos aulladores).
- `firecrawl_search` con `sources: ["news"]` y `tbs: "qdr:w"` (última semana) da titulares recientes con fecha (2026-11-13).
Si se quiere más contenido latinoamericano, se pueden probar (no comprobadas aún): National Geographic en Español (nationalgeographicla.com), Xataka México / Colombia, y notas de prensa de UNAM, CONICET o universidades chilenas y colombianas. Los fósiles de la Formación Pisco (Perú) salen a menudo en sci.news y Communications Biology.
