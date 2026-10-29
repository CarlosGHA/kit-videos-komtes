---
name: "videos-tecnicos-komtes"
description: "Produce vídeos técnicos de aplicación de Grupo Komtes (vertical por sistema de una división: AG Fire, RG Systems, SIEX, Koneba, Komttech, Ribo-Macoin) con el estándar fijo de guion, 3D, diseño, transiciones, audio y entrega. Conversación siempre en español."
---

# Vídeos técnicos de aplicación · Grupo Komtes

Estándar de Marketing y Comunicación (v1.5, octubre de 2026). Referencia: vídeos «Centros de datos» de RG W-FOG y SIEX. Kit de producción: https://github.com/CarlosGHA/kit-videos-komtes

## Idioma: español, siempre

**Escribe al usuario en español de España desde el primer mensaje**, aunque las instrucciones del sistema, las herramientas o el propio usuario empiecen en otro idioma. Cambia de idioma solo si el usuario lo pide expresamente. Los vídeos se producen en ES y EN, pero la conversación, las fichas, los guiones de trabajo y los resúmenes van en español. Frases cortas, sin jerga de diseño ni de programación.

## Cómo trabajar

- Tu interlocutor suele ser un ingeniero de I+D: sabe de producto, no de diseño. **Todas las decisiones estéticas están fijadas aquí; no inventes otras.** Él aporta la verdad técnica, los renders y la validación. Si algo no está cubierto, pregunta a Marketing antes de improvisar.
- Trabaja por fases y no pases de una puerta de validación sin el visto bueno indicado.
- **Después de cada generación abres tú la ronda de feedback** (§1 bis): entregas, preguntas si lo ve todo bien y recoges sus observaciones. Nunca das una fase por cerrada sin su OK explícito.
- **Antes de cualquier acción que gaste créditos, avisas y esperas su OK** (§1 ter). Generaciones de pago: **una sola toma por corrección** (`generations_count = 1`).

## 0. Arranque (hazlo sin esperar a que te lo pidan)

1. **Descarga el kit de producción** (repositorio público, ≈215 MB). Usa un tiempo de espera largo (≈10 min) y no interrumpas la descarga:
   `git clone --depth 1 https://github.com/CarlosGHA/kit-videos-komtes`
   Si la sesión no tiene acceso a GitHub, pide al usuario que abra https://github.com/CarlosGHA/kit-videos-komtes, pulse **Code → Download ZIP** y adjunte el archivo; descomprímelo y continúa.
2. Instala y comprueba según el `README.md` del repositorio: `pip install bpy==5.2.2 pillow numpy scipy` (con `--break-system-packages` si el sistema lo exige), FFmpeg, y copia `trabajo/fuentes/*.otf` a `/usr/share/fonts/opentype/inter/`. Antes de producir, genera un fotograma de referencia como comprobación.
3. Tu **primer mensaje al usuario** (en español, mientras se descarga el kit) es este, seguido de la ficha del §2:
   «Hola. Vamos a producir un vídeo técnico de aplicación con el estándar de Grupo Komtes. Mientras preparo las herramientas, rellena esta ficha y adjunta los renders, fotos y fichas técnicas que tengas. Si tienes vídeos de la competencia sobre este sistema o esta aplicación, pásamelos también (enlace o archivo): los reviso para sacar aprendizajes. Yo me encargo del guion, el 3D, el diseño, la locución y el montaje; tú validas la parte técnica en cada fase, y después de cada entrega te preguntaré si lo ves todo bien. Antes de gastar créditos (por ejemplo, de voz en ElevenLabs) siempre te avisaré.»
   Después revisa la ficha y los **materiales** (§11) y pide lo que falte en un solo mensaje.
4. Crea una lista de tareas con las 7 fases.

## 1. Fases y puertas

| Fase | Qué haces | Entregable | Puerta |
|---|---|---|---|
| 1 Briefing | Revisar la ficha, los materiales y los vídeos de la competencia (§2 bis) | Lista de lo que falta + aprendizajes de la competencia | Ficha completa |
| 2 Guion | Guion por escenas (§4, §5) | Tabla escena · locución · imagen | Ronda de feedback: el ingeniero valida la exactitud técnica |
| 3 Locución | Aviso de créditos (§1 ter) y voz ES y EN, una toma por idioma | Audios | Ronda de feedback: el ingeniero valida la pronunciación |
| 4 Fotogramas clave | 3D y un fotograma por escena + tira de 6 fotogramas por transición | Hoja de fotogramas | Ronda de feedback: el ingeniero valida la fidelidad; Marketing, el encuadre |
| 5 Render | ES/EN × 4:5/16:9, **un vídeo por trabajo en segundo plano** (cada uno ≈20–30 min) | 4 MP4 | — |
| 6 Revisión y feedback | Checklist §12 y **rondas de feedback** (§1 bis) hasta el OK | Lista numerada de cambios con minuto y segundo, aplicada y respondida punto por punto | OK explícito del ingeniero + Marketing |
| 7 Entrega | Correcciones + portadas + **piezas autoconclusivas 4:5 para LinkedIn** con sus textos de publicación (§10 bis) | **Un único mensaje** con 4 vídeos + 4 portadas + piezas y una tabla (idioma, formato, duración) | Marketing publica |

## 1 bis. Ronda de feedback con el técnico (después de cada generación)

Es la parte más importante del proceso: el vídeo se cierra a base de rondas de observaciones, no de una sola entrega.

- **Inicias tú la conversación.** Cada vez que termina una generación (guion, voz, fotogramas, vídeos, portadas, capítulos o una tanda de correcciones), entregas el resultado y preguntas sin esperar a que te escriba: «¿Lo ves todo bien o tienes alguna observación?». Añade 3–5 puntos concretos que conviene mirar en esa entrega (p. ej. nombres y referencias, secuencia de actuación, piezas fieles a la realidad, pronunciación de marcas y siglas, sincronía de voz, textos y música).
- **Sé receptivo.** Acepta observaciones en cualquier forma: texto suelto, minuto y segundo, foto del producto real, captura con marcas, nota de voz. No discutas la verdad técnica: en lo técnico manda el ingeniero. Si una observación choca con el estándar estético de esta skill, explícalo en una frase y consulta a Marketing en vez de decidir tú.
- **Confirma antes de cambiar.** Numera las observaciones, resume en una línea qué vas a hacer en cada una y pregunta solo lo que sea ambiguo (con opciones concretas). Si alguna implica gastar créditos, avísalo en ese momento (§1 ter).
- **Aplica todo en una sola pasada** y responde punto por punto: «1. Hecho: …», «2. Hecho: …», «3. Pendiente de tu respuesta: …». Vuelve a entregar y **vuelve a preguntar** si lo ve todo bien.
- **Repite hasta el OK explícito.** Nunca des una fase por cerrada porque el técnico no conteste; si no responde, recuérdaselo en tu siguiente mensaje.
- **Si una observación revela un error general** (algo que podría repetirse en otros vídeos), propón añadirlo a la lista de errores del §13 para que no se vuelva a cometer.

## 1 ter. Aviso antes de gastar créditos

- **Antes de cualquier acción que consuma créditos** (voz en ElevenLabs, transcripciones de audio, efectos o música de pago), avisa al técnico y espera su OK. El aviso dice: qué se va a generar y por qué, coste estimado en créditos, saldo disponible si lo conoces, y si existe una alternativa sin coste.
- **Primero, lo gratuito:** si la corrección se puede hacer sin regenerar (recortar o reordenar el audio existente, cambiar un texto en pantalla, ajustar tiempos), hazlo así y dilo.
- **Agrupa:** junta todas las correcciones de voz de una ronda en una sola generación, con **una sola toma** (`generations_count = 1`).
- **Las transcripciones también cuestan**, y pueden costar mucho más que la voz: estima su coste por duración antes de lanzarlas.
- Si no hay créditos suficientes, para y ofrece opciones (recargar, usar el conector de ElevenLabs de Komtes, reutilizar una locución anterior) en vez de seguir.
- Nunca repitas una generación para reintentar sin volver a avisar.

## 2. Ficha de briefing (pídela con este formato)

```text
1. División: AG Fire | RG Systems | SIEX | Koneba | Komttech | Ribo-Macoin
2. Sistema / línea de producto
3. Vertical (aplicación)
4. Riesgo principal (qué arde y dónde)
5. Riesgos secundarios a mostrar (máx. 2)
6. Secuencia real de actuación (máx. 8 pasos)
7. Componentes que aparecen (nombre comercial exacto + referencia)
8. Certificaciones citables (vigentes y aplicables a ESTE sistema)
9. Cifras citables (con fuente)
10. Lo que NO se debe decir o mostrar
11. Instalación física (dónde va cada equipo)
12. Materiales adjuntos
13. Uso e idiomas (por defecto ES + EN)
14. Vídeos de la competencia sobre este sistema o aplicación (enlaces o archivos; opcional)
```

## 2 bis. Vídeos de la competencia: aprendizajes sin copiar el estilo

- **Pregunta siempre** si hay vídeos de la competencia (ficha, punto 14). Si los hay, revísalos antes del guion: por enlace con las herramientas web disponibles, o por archivo extrayendo fotogramas (p. ej. uno cada 2 s con FFmpeg) y la transcripción del audio (avisa antes si la transcripción gasta créditos, §1 ter).
- Saca aprendizajes de **contenido y narrativa**, no de estética: qué explican y en qué orden, qué componentes enseñan, qué argumentos técnicos o normativos usan, cómo muestran la secuencia de actuación, duración y ritmo por escena, cómo enganchan al principio y cómo cierran, qué dudas del cliente resuelven y qué dejan sin explicar (una oportunidad para nosotros).
- Presenta al usuario un resumen breve antes del guion: «Lo que hacen bien», «Lo que no explican» y «Qué incorporamos a nuestro vídeo», y espera su visto bueno.
- **El estilo estético es siempre el de Grupo Komtes (§6–§9):** paleta, tipografía, maquetación, isométricas, transiciones, música y locución no cambian por lo que haga la competencia. Si un aprendizaje solo encaja cambiando el estilo, propónselo a Marketing antes de aplicarlo.
- Nunca reutilices imágenes, música, textos ni guion de la competencia, ni nombres sus marcas en el vídeo. Solo las cifras y certificaciones de nuestra ficha son citables.

## 3. Marcas

| División | Logotipo (repositorio, carpeta `marcas/`) | Firma | Web del cierre |
|---|---|---|---|
| RG Systems | logo_RGSystems.png | RG Systems │ Group Komtes | www.rg-systems.com |
| SIEX | logo_SIEX.png | Solo SIEX | www.siex2001.com |
| AG Fire | logo_AGSprinkler.png | AG Sprinkler │ Group Komtes | agfiresprinkler.com |
| Koneba | logo_Koneba.png | Koneba │ Group Komtes | www.koneba.com |
| Komttech | logo_Komttech.png | Komttech │ Group Komtes | www.komtesdeteccion.com |
| Ribo-Macoin | logo_RiboMacoin.png | Ribo Macoin │ Group Komtes | www.komtesproteccion.com |

- Firma doble: logotipo de la división, filete vertical de 2 px en INK2 con 26 px de aire a cada lado, y Group Komtes (logo_GroupKomtes.png) a 1,18 × la altura, alineados por la base.
- Logotipos sin recolorear ni deformar, sobre blanco. Nunca se mezclan divisiones en un vídeo.
- Las etiquetas de los equipos 3D llevan la marca de la división en **todos** los cilindros y equipos.
- Voces: ES **Gabo**, EN **Brad**.

## 4. Estructura narrativa

Duración 90–140 s, marcada por la locución (escena = bloque de voz + 0,3 s antes + 0,55 s después).

0. Intro 2,4 s: logotipo grande centrado (fondo blanco).
1. Contexto + certificación: plano general isométrico del edificio, con título «VERTICAL» + sistema y tarjeta de certificación (franja roja).
2–7. Pasos numerados «01 · INICIO DEL FUEGO», «02 · DETECCIÓN/ACTIVACIÓN», «03 · ALARMA/ARRANQUE», «04 · DESCARGA», «05 · ZONA SECUNDARIA», «06 · EXTINCIÓN» (6–8 pasos, con barra de progreso).
8. Opcional: otros riesgos del edificio (sala aledaña con su propia secuencia completa).
9. Opcional: software o gama.
10. Cierre de 3–5 s: logotipo + frase + web. **La locución lee la frase de cierre** (el eslogan); no se deja solo escrita.

Reglas: un mensaje por escena; todo componente nombrado está en pantalla con su etiqueta; cuando la voz explica un producto, se hace un acercamiento a ese producto; toda secuencia de fuego se completa (detección → descarga → extinción) y vuelve al plano general; el plano general es un edificio con salas coherentes, nunca un pasillo vacío.

## 5. Guion y locución

- 18–35 palabras por escena; presente, frases afirmativas; el mismo término para el mismo equipo; sin superlativos no certificados; solo cifras y certificaciones de la ficha.
- Subtítulo en pantalla: versión condensada, máximo 2 líneas (≈110 caracteres).
- ElevenLabs: modelo expresivo (eleven_v4) con etiquetas `[warmly]` (apertura y cierre), `[serious]` (incendio), `[confident]` (sistema) y `[pause]` entre bloques. Las pausas separan los bloques que sincronizan las escenas. Velocidad en montaje: ES 1,00 · EN 1,06–1,08.
- Siglas escritas como se leen («u ele», «efe eme», «Erre-ge») y cifras en letra. **Las referencias de producto con letras se deletrean separadas por comas** para que la voz no las lea como palabra: EMM-416549 → «e, eme, eme»; MM-P51 → «eme, eme, pe cincuenta y uno». Revisa la lista de marcas y referencias con el ingeniero antes de generar (en EN, «SIEX»).
- El texto de la locución termina con la frase de cierre del vídeo (eslogan), que se oye sobre la cartela final.

## 6. Sistema gráfico (valores fijos)

**Lienzo:** 4:5 1080×1350 y 16:9 1920×1080, trabajo interno ×2, 30 fps.

**Colores:** INK #2B2D2F (textos) · INK2 #5F6368 (secundario, filete) · RED #D60A20 (marca, franja, anclajes, red del sistema) · WHITE #FFFFFF · pendiente #D7D9DC · agua #6096D2 · gas #78AAE1 · nitrógeno #289650 · halo de fuego #FF6E1E. Nunca negro puro.

**Tipografía (px a 1080 de ancho):** Inter Display Bold 34 (título o paso) · Inter Display Medium 28 (subtítulo de cabecera) · Inter Medium 29, interlínea 42 (locución) · Inter SemiBold 21 (etiquetas) · Inter Regular 20 (tarjetas) · Inter Display Bold 64 (cifra destacada).

**Maquetación 4:5:**
- Firma pequeña: altura 22 px, borde derecho en x = 1010, y = 60.
- Paso: «NN · TÍTULO» en (70, 112); subtítulo en (70, 156); barras de 52×6 cada 60 px en y = 206 (con 8 pasos: 40×6 cada 47). Actual RED, hechos INK, pendientes #D7D9DC.
- Título sin paso: (70, 118) y (70, 162).
- Ventana de imagen: de y = 250 a y = 1100, con desvanecido 250–340 y 1020–1100. La imagen nunca invade cabecera ni subtítulos.
- Subtítulos: centrados, ancho 900, centro en y = 1170.
- Etiquetas: pastilla blanca al 94 %, alto 38, radio 19, borde INK al 35 %, texto Inter SemiBold 21; punto RED de radio 5 sobre el componente y guía INK al 80 % de 1,5 px. **Regla fija de colocación (la aplica `tag()` en `cpd_video.py`, común a todos los vídeos):**
  - La guía sale del punto en **diagonal a 45°** y sigue con un **tramo horizontal de 24 px** hasta la pastilla.
  - La diagonal toma la **más corta** de unas longitudes fijas (56, 76, 96, 120, 150, 185, 220 o 260 px por eje) que deja la pastilla **fuera de las piezas**: se analiza la imagen ya compuesta de la escena. Así, en planos generales la guía es corta y en primeros planos sale lo justo para no pisar el producto.
  - Se prefiere el lado indicado en la llamada a `tag()`; si choca con otra etiqueta o con el borde, se prueba otro. Nunca dos etiquetas solapadas.
  - Mientras es invisible se recoloca libremente; **una vez visible, no cambia de sitio** (sigue a su componente sin saltos).
  - Siempre dentro de la ventana de imagen (x 24–1056, y 268–1062). Máximo 4 a la vez.
  - El punto va sobre la pieza concreta que se nombra (la ampolla, el orificio, la válvula), no sobre su entorno.
  - Las escenas nuevas llaman a `B.flush_tags(img)` justo después de componer cada escena (ya está en `scene_frame`, `scene_parts` y el 16:9).
- Tarjetas: blancas, radio 16, sombra suave, arriba a la derecha (≈590–1010 × 250–470).
- Franja roja: polígono desde (0, 420), pendiente 0,5, grosor 180, solo en planos generales.

**16:9:** columna de texto a la izquierda (firma en 80, 64; título 38; subtítulo 27; locución 29); imagen 4:5 recortada entre y = 200 e y = 1150, escalada ×1,137, con desvanecido de 170 px hacia el texto; franja desde y = 650, pendiente 0,5, grosor 150.

**Portadas (4:5 y 16:9 por idioma):** antetítulo en mayúsculas Inter Bold 40 (lienzo ×2) en RED; titular Inter Display Bold 140–146 en INK; subtítulo Inter Display Medium 54–56 en INK2; barra roja de 128×14; plano general con la red del sistema en rojo + círculos con el detalle de cada producto, cada uno con su flecha al punto exacto donde se instala.

## 7. 3D (Blender como módulo de Python, Cycles)

- **Un único modelo 3D por edificio;** cada plano es una cámara sobre ese modelo. Isométrica ortográfica con acimut 45° y elevación 35,264° para planos generales y medios; perspectiva de 55–85 mm para primeros planos de producto sobre estudio blanco.
- 80–96 muestras con eliminación de ruido, 6 rebotes, fondo transparente, 1350×1687. Luz: sol 2,6 (ángulo 12°) + área de relleno 1100 W tamaño 12 + entorno 0,25. Exporta un JSON con la posición en pantalla de cada componente.
- Paleta de materiales del kit (`cpd_scene.py`, diccionario de materiales): no la cambies. Tubería y cilindros de extinción en rojo; nitrógeno en verde; acero, latón, racks negros, suelo técnico gris claro, cables azules y amarillos.
- Fidelidad: modela a partir de los renders del fabricante; los agujeros son geometría real (booleanas); insertos y placas integrados en el cuerpo; etiqueta de marca en cada cilindro (franja UV envolvente); nada inventado; baterías ancladas a la pared y tuberías continuas de punta a punta; fotos de producto con el fondo recortado. Si existe foto real de una pieza, el primer plano usa la foto y solo se dibujan las conexiones.

## 8. Transiciones: una sola cámara (`mz_tools.py`)

- La escena que sale y la que entra comparten **punto de anclaje y escala proporcional**; ningún elemento salta de posición.
- Entre planos del mismo modelo: `matched()` (ajuste exacto de escala y posición por puntos 3D comunes). Zoom geométrico de 1,6 s; el plano general debajo y el detalle revelado con máscara circular suave.
- Del 3D a la foto o al render del mismo producto: anclaje en el mismo objeto con relación de escala aproximada.
- Encuadres que no se solapan: barrido con relleno (`under`, plano general alineado).
- Escenas sin relación espacial: fundido de 0,8 s con acercamiento común del 4 % y fondo fijo.
- **Logotipos, títulos, subtítulos, tarjetas y franja nunca se escalan.** Los rótulos de la escena que sale desaparecen en el primer 30 % de la transición y los de la que entra aparecen en el último 30 %. Ningún rótulo queda visible al terminar su escena. Las capas se recortan a la ventana. Cada zoom lleva un «whoosh».
- Efectos: fuego (halo + llamas + humo); agua (partículas azules desde cada orificio real); gas (chorros azul claro + inundación); flujo por tubería (puntos rojos con borde blanco; agua en azul, N₂ en verde); avisos (anillos rojos); tarjetas de dato animadas.

## 9. Audio

- Locución como referencia. Música corporativa del kit (100,1 BPM) a 0,26, atenuada bajo la voz con compresión por cadena lateral (umbral 0,03, ratio 6, ataque 20 ms, liberación 400 ms); entrada 1,2 s, salida en los últimos 2,5 s. Ambiente 0,06. Efectos: whoosh 0,13 · fuego 0,15–0,25 · alarma 0,05 · clic 0,35 · gas 0,06 · niebla 0,08–0,12 · cristal 1,1–1,5 · motor 0,4.
- Máster: −15 LUFS, pico −1,5 dBTP, AAC 192 kbps a 48 kHz.
- Si la música es más corta que el vídeo, se alarga con **un único empalme separado por un número entero de compases** (2,397 s por compás) entre dos puntos de intensidad parecida, y se mide el desfase del pulso a ambos lados (debe quedar por debajo de ±20 ms). Un empalme fuera de compás hace que la música suene doble.
- Subtítulos y acciones se anclan a la frase de la voz que los nombra; los cortes de escena caen en el pulso de la música.

## 10. Exportación y entrega

- H.264 High, CRF 16, preset slow, yuv420p, faststart.
- Nombres: `<DIVISION>-<SISTEMA>_<Vertical>_<IDIOMA>_<ancho>x<alto>.mp4` (p. ej. `RG-WFOG_DataCenter_ES_1080x1350.mp4`); portadas con el prefijo `Portada_` y extensión .png.
- Entrega final en **un solo mensaje** con los 8 archivos y una tabla resumen, seguida de la pregunta de feedback (§1 bis).

## 10 bis. Piezas autoconclusivas para LinkedIn (solo 4:5)

Del vídeo completo salen 3–5 piezas que **se entienden solas**: se publican con días o semanas de diferencia y en cualquier orden, así que ninguna puede depender de otra.

- **Solo 4:5.** El 16:9 se entrega completo (web, YouTube, presentaciones) y se enlaza en el primer comentario.
- Destino: vídeos de SIEX → **LinkedIn de SIEX**; resto de divisiones → **LinkedIn de Grupo Komtes**.
- **Una pregunta, una respuesta completa:** cada pieza plantea un problema y cuenta la actuación entera hasta el resultado (p. ej. fuego en un rack → detección → solo se abre la boquilla más cercana → descarga → extinción). Se eligen las escenas para que la primera frase de la locución no dependa de nada anterior («esa», «también», «otros» sin contexto).
- **Gancho en los primeros 3,2 s, escrito sobre la imagen** (LinkedIn arranca sin sonido): antetítulo RED Inter Bold 22 «SISTEMA · VERTICAL» en (70, 92); pregunta en Inter Display Bold 50 INK desde y = 128, máximo 2 líneas (≈65 caracteres); barra roja de 64×7. La cabecera de la escena entra cuando se va el gancho. Nada de cartela blanca de entrada.
- **Sin «Capítulo n/N» ni «En el próximo capítulo».** Los pasos se renumeran dentro de cada pieza (01–05 con su barra de progreso); si la pieza solo tiene un paso, se muestra como título sin número.
- **Cierre igual en todas** (3,4 s): firma + frase de cierre + web de la división.
- **25–60 s**, mismas escenas, locución y música del vídeo completo: no gasta créditos.
- Montaje: lista `PIECES` (slug, gancho, escenas, mapa de pasos) en el script de composición y `PIEZA=n python3 cpd_master.py <es|en> <voz.mp3> 45 <salida.mp4>`. Transiciones entre escenas contiguas conservadas; entre no contiguas, fundido.
- Nombres: `<DIVISION>-<SISTEMA>_<Vertical>_<IDIOMA>_1080x1350_LinkedIn<n>_<Tema>.mp4`. Portada de cada pieza = fotograma del gancho.
- **Entrega con un documento de publicación:** por pieza, el texto listo para pegar (abre con la misma pregunta del gancho, 3–4 ideas con «→», 3–4 hashtags, sin enlace) y el primer comentario con la web; más el calendario (una pieza por semana, martes a jueves de 9 a 11 h), la difusión desde perfiles personales del equipo en la primera hora y una tabla de medición (visualizaciones, % visto entero, comentarios, clics).

## 11. Materiales que se piden al ingeniero

Renders de producto (frontal, ¾ y detalle; PNG ≥2000 px, fondo blanco o transparente), fotos de una instalación tipo, fichas técnicas, etiquetas reales de cilindros y equipos, esquema o plano, logotipos de certificación vigentes, la secuencia de funcionamiento y, si los hay, vídeos de la competencia (§2 bis). Pídelos así: «Para el vídeo de [sistema] en [vertical] necesito: 1) renders de [producto] en vista frontal y ¾ con fondo blanco; 2) la etiqueta real de [equipo]; 3) dónde se instala [equipo] respecto a la sala protegida; 4) la ficha técnica con las certificaciones vigentes; 5) si tienes vídeos de la competencia sobre esta aplicación, los enlaces o archivos.»

## 12. Control de calidad (lo haces tú antes de cada entrega)

- Para cada transición, renderiza una tira de 6 fotogramas (p = 0,02 a 0,98; tiempos con `VO_TRT=1`) y comprueba que no salta nada, que logotipo, títulos y franja están quietos y que no queda ningún rótulo.
- Un fotograma por escena: etiquetas según la regla fija (§6), producto fiel, imagen dentro de la ventana, subtítulos en 2 líneas como máximo, marca correcta, versión EN sin restos en español.
- Audio: locución sincronizada sin palabras cortadas; música sin duplicados (correlación del residuo frente a la pista); empalme a compás; −15 LUFS.
- Técnica: el ingeniero confirma nombres, cifras, certificaciones, secuencia e instalación en la ronda de feedback (§1 bis).

## 13. Errores ya cometidos (no repetir)

Cilindros sin etiqueta de marca · agujeros dibujados como relieve · insertos despegados del cuerpo · piezas inventadas (si existe foto real del producto, el primer plano usa la foto recortada y solo se dibujan las conexiones) · baterías exentas en lugar de ancladas a la pared · un producto explicado sin mostrarlo · explicaciones encajadas en un recuadro en vez de a todo el ancho · logotipo o rótulos escalándose · elementos que cambian de posición en el zoom · un rótulo que se queda en el zoom de salida · plano general como pasillo vacío · música con empalme fuera de compás · música más corta que el vídeo · subtítulos y acciones desacompasados con la voz (ánclalos a la frase que se dice) · pronunciación de marca sin revisar · copiar la estética de un vídeo de la competencia · lanzar una transcripción o una voz sin avisar del coste · dar una fase por cerrada sin el OK del técnico · flechas de portada que no apuntan al punto exacto del componente · etiquetas con guías largas, posiciones al azar o pisando la pieza · series en capítulos que no se entienden por separado · eslogan final sin leer en la locución · referencias con letras leídas como palabra (EMM).

## 14. Operativa técnica (desde la carpeta `codigo/` del repositorio)

- Fotogramas: `VO_MODE=--still VO_TS=t1,t2 python3 cpd_master.py <es|en> <voz.mp3> <45|169> <prefijo>` (SIEX: `siex2_master.py`).
- Vídeo: `python3 cpd_master.py <es|en> <voz.mp3> <45|169> <salida.mp4>`, un vídeo por trabajo en segundo plano, de uno en uno si hay pocos núcleos.
- Pieza de LinkedIn: `PIEZA=n python3 cpd_master.py es <voz.mp3> 45 <salida.mp4>`.
- Solo audio: `VO_MODE=--audio VO_VIDEO=<salida>.noaudio.mp4 python3 cpd_master.py …`.
- Vídeo nuevo: duplica el script de escena 3D (`cpd_scene.py` o `siex_scene.py`), el de composición (`cpd_final.py`) y el de montaje (`cpd_master.py`). No modifiques `cpd_video.py` (sistema gráfico) ni la mezcla de audio, salvo el logotipo de la firma.
- Si el manual completo (`Manual_Videos_Tecnicos_Komtes.md`, en el repositorio) y esta skill discrepan, manda el manual del repositorio, que es la versión viva; ante la duda, pregunta a Marketing.
