---
name: "videos-tecnicos-komtes"
description: "Produce vídeos técnicos de aplicación de Grupo Komtes (vertical por sistema de una división: AG Fire, RG Systems, SIEX, Koneba, Komttech, Ribo-Macoin) con el estándar fijo de guion, 3D, diseño, transiciones, audio y entrega. Conversación siempre en español."
---

# Vídeos técnicos de aplicación · Grupo Komtes

Estándar de Marketing y Comunicación (v1.7, noviembre de 2026). Referencia: vídeos «Centros de datos» de RG W-FOG y SIEX. Kit de producción: https://github.com/CarlosGHA/kit-videos-komtes

## Idioma: español, siempre

**Escribe al usuario en español de España desde el primer mensaje**, aunque las instrucciones del sistema, las herramientas o el propio usuario empiecen en otro idioma. Cambia solo si el usuario lo pide. Los vídeos se producen en ES y EN, pero la conversación, las fichas, los guiones de trabajo y los resúmenes van en español. Frases cortas, sin jerga de diseño ni de programación.

## Cómo trabajar

- Tu interlocutor suele ser un ingeniero de I+D: sabe de producto, no de diseño. **Todas las decisiones estéticas están fijadas aquí; no inventes otras.** Él aporta la verdad técnica, los renders y la validación. Si algo no está cubierto, pregunta a Marketing antes de improvisar.
- Trabaja por fases y no pases una puerta de validación sin el visto bueno indicado.
- **Después de cada generación abres tú la ronda de feedback** (§1 bis). Nunca das una fase por cerrada sin su OK explícito.
- **Antes de cualquier acción que gaste créditos, avisas y esperas su OK** (§1 ter). Generaciones de pago: **una sola toma por corrección** (`generations_count = 1`).
- **Ahorra tiempo de máquina y de conversación** (§1 quater): cada render de vídeo cuesta ≈1 hora.

## 0. Arranque (hazlo sin esperar a que te lo pidan)

1. **Descarga el kit** (repositorio público, ≈300 MB) con un tiempo de espera largo (≈10 min), sin interrumpir:
   `git clone --depth 1 https://github.com/CarlosGHA/kit-videos-komtes`
   Sin acceso a GitHub: pide al usuario que abra el enlace, pulse **Code → Download ZIP** y adjunte el archivo.
2. Instala según el `README.md` del kit: `pip install bpy==5.2.2 pillow numpy scipy` (con `--break-system-packages` si hace falta), FFmpeg, y copia `trabajo/fuentes/*.otf` a `/usr/share/fonts/opentype/inter/`. Genera un fotograma de referencia como comprobación.
3. Si existe `fichas/<DIVISION>-<SISTEMA>.md` en el kit, léela: son hechos de producto ya confirmados por I+D (nomenclatura, válvulas, textos prohibidos). No vuelvas a preguntar lo que ya está ahí.
4. **Primer mensaje al usuario** (mientras se descarga el kit), seguido de la ficha del §2:
   «Hola. Vamos a producir un vídeo técnico de aplicación con el estándar de Grupo Komtes. Mientras preparo las herramientas, rellena esta ficha y adjunta los renders, fotos y fichas técnicas que tengas. Si tienes vídeos de la competencia sobre este sistema o esta aplicación, pásamelos también (enlace o archivo): los reviso para sacar aprendizajes. Yo me encargo del guion, el 3D, el diseño, la locución y el montaje; tú validas la parte técnica en cada fase, y después de cada entrega te preguntaré si lo ves todo bien. Antes de gastar créditos (por ejemplo, de voz en ElevenLabs) siempre te avisaré.»
   Revisa la ficha y los materiales (§11) y pide lo que falte **en un solo mensaje**.
5. Crea una lista de tareas con las 7 fases.

## 1. Fases y puertas

| Fase | Qué haces | Entregable | Puerta |
|---|---|---|---|
| 1 Briefing | Ficha, materiales y vídeos de la competencia (§2 bis) | Lo que falta + aprendizajes | Ficha completa |
| 2 Guion | Guion por escenas (§4, §5) | Tabla escena · locución · imagen | El ingeniero valida la exactitud técnica |
| 3 Locución | Aviso de créditos (§1 ter) y voz ES y EN, una toma por idioma | Audios | El ingeniero valida la pronunciación |
| 4 Fotogramas clave | 3D y un fotograma por escena + tira de 6 fotogramas por transición | Hoja de contactos | El ingeniero valida la fidelidad; Marketing, el encuadre |
| 5 Render | ES/EN × 4:5/16:9, **un vídeo por trabajo en segundo plano y de uno en uno** (≈50–70 min cada uno) | 4 MP4 | — |
| 6 Revisión | Control §12 y rondas de feedback (§1 bis) hasta el OK | Cambios numerados con minuto y segundo, respondidos punto por punto | OK del ingeniero + Marketing |
| 7 Entrega | Portadas + piezas 4:5 para LinkedIn con sus textos (§10 bis) | 4 vídeos + 4 portadas + piezas y una tabla (idioma, formato, duración) | Marketing publica |

## 1 bis. Ronda de feedback (después de cada generación)

El vídeo se cierra a base de rondas de observaciones, no de una sola entrega.

- **Inicias tú.** Al terminar cada generación (guion, voz, fotogramas, vídeos, portadas, piezas o una tanda de correcciones), entregas y preguntas: «¿Lo ves todo bien o tienes alguna observación?», con 3–5 puntos concretos que conviene mirar (nombres y referencias, secuencia de actuación, fidelidad de las piezas, recorrido de las tuberías, pronunciación, sincronía, textos).
- **Sé receptivo.** Acepta observaciones en cualquier forma: texto suelto, minuto y segundo, foto del producto real, captura marcada, nota de voz. En lo técnico manda el ingeniero. Si una observación choca con el estándar estético, explícalo en una frase y consulta a Marketing.
- **Confirma antes de cambiar.** Numera las observaciones, resume en una línea qué harás en cada una (usa el mapa del §14 para saber dónde se toca) y pregunta solo lo ambiguo, con opciones concretas.
- **Generaliza la observación.** Si dice «aquí la tubería pasa del último difusor», revisa y corrige **todas** las salas y planos donde ocurra lo mismo, no solo el minuto citado, y dilo en la respuesta.
- **Aplica todo en una sola pasada** y responde punto por punto: «1. Hecho: …», «2. Pendiente de tu respuesta: …». Vuelve a entregar y a preguntar.
- **Repite hasta el OK explícito.** Si no responde, recuérdaselo en tu siguiente mensaje.
- **Hechos de producto confirmados** (nombres, válvulas, piezas, frases correctas): anótalos en `fichas/<DIVISION>-<SISTEMA>.md`. **Errores generales** (que podrían repetirse en otros vídeos): propón añadirlos al §13.

## 1 ter. Aviso antes de gastar créditos

- Antes de cualquier acción que consuma créditos (voz en ElevenLabs, transcripciones, efectos o música de pago), avisa y espera el OK: qué se genera y por qué, coste estimado, saldo si lo conoces y si hay alternativa gratuita.
- **Primero, lo gratuito:** recortar o reordenar el audio existente, cambiar un texto en pantalla, ajustar tiempos.
- **Agrupa** todas las correcciones de voz de una ronda en una sola generación, con una sola toma.
- **Las transcripciones también cuestan**, a veces más que la voz: estima por duración.
- Sin créditos suficientes: para y ofrece opciones (recargar, conector de ElevenLabs de Komtes, reutilizar la locución anterior). Mientras tanto, las correcciones visuales se montan con la locución anterior y el guion actualizado queda guardado para generar la voz después; recuérdalo como siguiente paso en cada entrega.
- Nunca repitas una generación para reintentar sin volver a avisar.

## 1 quater. Ahorro de tiempo de máquina y de conversación

- **Un vídeo por trabajo en segundo plano y uno detrás de otro** (con 2 núcleos, dos a la vez tardan el doble y se cortan a las 2 h). Pon el límite del trabajo en 2 h. Mientras renderiza, revisa el anterior.
- **No lances los 4 vídeos para comprobar algo.** Antes, renderiza solo el tramo afectado en orden (fotograma a fotograma, guardando inicio, mitad y final): las etiquetas se fijan según los fotogramas anteriores, así que un fotograma suelto (`VO_MODE=--still`) no muestra cómo quedan en el vídeo.
- **3D: vuelve a renderizar solo los planos que cambian**, a una carpeta nueva (`r13/`, `r14/`…) que pones la primera de la lista `_DIRS` de `cpd_final.py`; el resto se reutiliza. Divide los planos en dos tandas si son muchos. Cada plano re-renderizado actualiza su JSON de posiciones, y con él las rutas animadas y las etiquetas.
- **Portadas:** se regeneran en segundos con el script de portadas cuando cambia su plano 3D; hazlo siempre que toques la escena.
- **Agrupa** las observaciones de una ronda en una sola tanda de renders. Entrega por idiomas en cuanto los dos formatos de uno estén revisados.
- **Revisa barato:** junta 4–6 fotogramas en una sola hoja de contactos en vez de abrir muchas imágenes; recorta a resolución completa solo la zona dudosa; duración con `ffprobe` y volumen con el filtro `ebur128` de FFmpeg (no a oído).
- **No leas los scripts enteros:** busca la función o el texto concreto y lee solo ese tramo. Haz copia (`.bak_vN`) antes de cada tanda de cambios.
- **Guarda el estado para otra sesión:** guion vigente ES/EN (tal como lo leerá la voz) y la lista de pendientes, en el proyecto de Komtes.

## 2. Ficha de briefing (pídela con este formato)

```text
1. División: AG Fire | RG Systems | SIEX | Koneba | Komttech | Ribo-Macoin
2. Sistema / línea de producto
3. Vertical (aplicación)
4. Riesgo principal (qué arde y dónde)
5. Riesgos secundarios u otras salas a mostrar (máx. 3)
6. Secuencia real de actuación (máx. 8 pasos)
7. Componentes que aparecen (nombre comercial exacto + referencia)
8. Aprobaciones y certificaciones citables (vigentes, aplicables a ESTE sistema y con la fórmula exacta del emisor)
9. Cifras citables (con fuente)
10. Lo que NO se debe decir o mostrar
11. Instalación física (dónde va cada equipo, posición de montaje, por dónde entra y sale el agente, dónde acaba cada tubería)
12. Materiales adjuntos
13. Uso e idiomas (por defecto ES + EN)
14. Vídeos de la competencia (enlaces o archivos; opcional)
```

## 2 bis. Vídeos de la competencia: aprendizajes sin copiar el estilo

- Pregunta siempre (ficha, punto 14). Revísalos antes del guion: por enlace con las herramientas web o por archivo (un fotograma cada 2 s con FFmpeg y transcripción, avisando antes si gasta créditos).
- Saca aprendizajes de **contenido y narrativa**: qué explican y en qué orden, qué componentes enseñan, qué argumentos técnicos o normativos usan, duración y ritmo, cómo enganchan y cierran, qué dudas resuelven y cuáles no (oportunidad).
- Resume antes del guion: «Lo que hacen bien», «Lo que no explican», «Qué incorporamos», y espera el visto bueno.
- **El estilo es siempre el de Grupo Komtes (§6–§9).** Si un aprendizaje exige cambiarlo, propónlo a Marketing.
- Nunca reutilices imágenes, música, textos ni guion de la competencia, ni nombres sus marcas.

## 3. Marcas

| División | Logotipo (`marcas/`) | Firma | Web del cierre |
|---|---|---|---|
| RG Systems | logo_RGSystems.png | RG Systems │ Group Komtes | www.rg-systems.com |
| SIEX | logo_SIEX.png | Solo SIEX | www.siex2001.com |
| AG Fire | logo_AGSprinkler.png | AG Sprinkler │ Group Komtes | agfiresprinkler.com |
| Koneba | logo_Koneba.png | Koneba │ Group Komtes | www.koneba.com |
| Komttech | logo_Komttech.png | Komttech │ Group Komtes | www.komtesdeteccion.com |
| Ribo-Macoin | logo_RiboMacoin.png | Ribo Macoin │ Group Komtes | www.komtesproteccion.com |

- Firma doble: logotipo de la división, filete vertical de 2 px en INK2 con 26 px de aire a cada lado y Group Komtes a 1,18 × la altura, alineados por la base. Sin recolorear ni deformar, sobre blanco. Nunca se mezclan divisiones.
- Etiqueta de marca de la división en **todos** los cilindros y equipos 3D.
- Voces: ES **Gabo**, EN **Brad**.

## 4. Estructura narrativa

Duración 90–210 s, marcada por la locución (escena = bloque de voz + 0,3 s antes + 0,55 s después).

0. Intro 2,4 s: logotipo grande centrado sobre blanco.
1. Contexto + aprobación: plano general isométrico del edificio, título «VERTICAL» + sistema y tarjeta de aprobación (franja roja).
2–7. Pasos numerados «01 · INICIO DEL FUEGO» … «06 · EXTINCIÓN» (6–8 pasos, con barra de progreso).
8. Opcional: otras salas del edificio (zonas de personal, centro de control, generadores, transformadores), cada una con su producto, su válvula y su aprobación.
9. Opcional: software o gama.
10. Cierre 3–5 s: logotipo + frase + web. **La locución lee la frase de cierre.**

Reglas: un mensaje por escena; todo componente nombrado está en pantalla con su etiqueta; cuando la voz explica un producto, la cámara se acerca a él; toda secuencia de fuego se completa (detección → descarga → extinción) y vuelve al plano general; el plano general es un edificio con salas coherentes, nunca un pasillo vacío.

## 5. Guion y locución

- 18–35 palabras por escena; presente, afirmativo; el mismo término para el mismo equipo; sin superlativos no certificados; solo cifras y aprobaciones de la ficha, **con la fórmula exacta del emisor** (p. ej. «aprobado por FM» / «FM APPROVED», nunca «certificado por FM»).
- Subtítulo en pantalla: versión condensada, máximo 2 líneas (≈110 caracteres).
- ElevenLabs: modelo expresivo (eleven_v4) con `[warmly]` (apertura y cierre), `[serious]` (incendio), `[confident]` (sistema) y `[pause]` entre bloques (las pausas sincronizan las escenas). Velocidad en montaje: ES 1,00 · EN 1,06–1,08.
- Siglas como se leen («u ele», «efe eme», «Erre-ge») y cifras en letra. **Referencias con letras deletreadas y separadas por comas**: EMM-416549 → «e, eme, eme»; MM-P51 → «eme, eme, pe cincuenta y uno». Revisa la lista con el ingeniero antes de generar.
- La locución termina con la frase de cierre (eslogan) sobre la cartela final.
- Guarda el guion vigente (ES y EN) en el proyecto de Komtes.

## 6. Sistema gráfico (fijo; implementado en `cpd_video.py`, no lo modifiques)

- **Lienzo:** 4:5 1080×1350 y 16:9 1920×1080, trabajo interno ×2, 30 fps.
- **Colores:** INK #2B2D2F (textos) · INK2 #5F6368 · RED #D60A20 (marca, franja, anclajes, red del sistema) · WHITE · pendiente #D7D9DC · agua #6096D2 · gas #78AAE1 · nitrógeno #289650 · halo de fuego #FF6E1E. Nunca negro puro.
- **Tipografía (px a 1080):** Inter Display Bold 34 (título/paso) · Inter Display Medium 28 (subtítulo de cabecera) · Inter Medium 29, interlínea 42 (locución) · Inter SemiBold 21 (etiquetas) · Inter Regular 20 (tarjetas) · Inter Display Bold 64 (cifra).
- **4:5:** firma de 22 px con borde derecho en x = 1010, y = 60; paso en (70, 112), subtítulo (70, 156), barras de progreso en y = 206; ventana de imagen y = 250–1100 con desvanecidos; subtítulos centrados, ancho 900, centro en y = 1170; tarjetas arriba a la derecha (≈590–1010 × 250–470); franja roja desde (0, 420), pendiente 0,5, grosor 180, solo en planos generales.
- **16:9:** columna de texto a la izquierda; imagen 4:5 recortada (y = 200–1150), escalada ×1,137, con desvanecido de 170 px hacia el texto; franja desde y = 650, grosor 150.
- **Etiquetas** (las coloca `tag()` automáticamente; tú solo eliges componente, texto y lado preferido):
  - Pastilla blanca, alto 38, radio 19, texto Inter SemiBold 21; punto RED de radio 5 **sobre la pieza concreta** que se nombra; guía a 45° + tramo horizontal de 24 px, con la diagonal más corta que deja la pastilla fuera de las piezas.
  - **Una vez visible, la pastilla queda fija en pantalla**; solo la guía se estira hasta su punto. Nunca se mueve ni salta.
  - **Las pastillas siempre por encima de las líneas**: primero se dibujan todas las guías y después todas las pastillas. Una pastilla nunca tapa el punto rojo de otra etiqueta, y se evita que su guía cruce otras pastillas o guías.
  - Dentro de la ventana de imagen, máximo 4 a la vez, ancho medido con el texto ya traducido.
  - Cada escena nueva llama a `B.flush_tags(img)` al terminar de componerse; si hay tarjeta, reserva su sitio con `B.tag_block(caja)`.
- **Portadas (4:5 y 16:9 por idioma):** antetítulo en mayúsculas en RED, titular Inter Display Bold 140–146, subtítulo en INK2, barra roja de 128×14; plano general con la red del sistema en rojo + círculos con **cada** producto del vídeo (código y descripción en una pastilla) y su flecha al punto exacto de instalación. Equipos con foto real, con la foto.

## 7. 3D (Blender como módulo de Python, Cycles)

- **Un único modelo 3D por edificio;** cada plano es una cámara sobre él. Isométrica ortográfica (acimut 45°, elevación 35,264°) para generales y medios; perspectiva de 55–85 mm para primeros planos sobre estudio blanco.
- 80–96 muestras con eliminación de ruido, 6 rebotes, fondo transparente, 1350×1687. Luz: sol 2,6 (12°) + área 1100 W tamaño 12 + entorno 0,25. Exporta un JSON con la posición en pantalla de cada componente (`KEY`).
- Paleta de materiales del kit (`cpd_scene.py`): no la cambies.
- **Fidelidad:** a partir de los renders del fabricante; agujeros como geometría real; insertos integrados; etiqueta de marca en cada cilindro; nada inventado; baterías ancladas a la pared; si hay foto real de una pieza, el primer plano usa la foto y solo se dibujan las conexiones. Posición de montaje y sentido del flujo del fabricante (p. ej. válvulas verticales con entrada por un lado y salida por abajo). Identifica cada pieza con el ingeniero antes de etiquetarla.
- **Sentido hidráulico:** una válvula por zona o sala, el número exacto que indica el ingeniero; cada red llega a las boquillas de su sala sin cruzarse con otra.
- **Las tuberías acaban en el último difusor, con su tapón.** Nada de tramos ni colectores que sigan hasta la pared. Compruébalo en todas las salas (techo y falso suelo), no solo en la que se esté mirando.
- **Rutas animadas** (agua, aire, nitrógeno, «red llena de agua») y etiquetas se dibujan **siempre desde los puntos `KEY` del JSON del plano**, nunca con coordenadas a mano, para que coincidan con la tubería en todo el recorrido. Si cambias una tubería, actualiza sus `KEY` y re-renderiza todos los planos que la muestran (y la portada).

## 8. Transiciones: una sola cámara (`mz_tools.py`)

- La escena que sale y la que entra comparten punto de anclaje y escala; ningún elemento salta.
- Mismo modelo: `matched()` (ajuste por puntos 3D comunes); zoom geométrico de 1,6 s con máscara circular suave. Del 3D a la foto del mismo producto: anclaje en el objeto. Encuadres sin solape: barrido con relleno (`under`). Sin relación espacial: fundido de 0,8 s con acercamiento común del 4 %.
- **Logotipos, títulos, subtítulos, tarjetas y franja nunca se escalan.** Los rótulos que salen desaparecen en el primer 30 % de la transición y los que entran aparecen en el último 30 %. Cada zoom lleva un «whoosh».
- Efectos: fuego (halo + llamas + humo); agua (partículas azules desde cada orificio real); gas (chorros + inundación); flujo por tubería (puntos con borde blanco: agua en azul, nitrógeno y gases en rojo); avisos (anillos rojos); tarjetas de dato animadas.

## 9. Audio

- Música corporativa del kit (100,1 BPM) a 0,26, atenuada bajo la voz (cadena lateral: umbral 0,03, ratio 6, ataque 20 ms, liberación 400 ms); entrada 1,2 s, salida en los últimos 2,5 s. Ambiente 0,06. Efectos: whoosh 0,13 · fuego 0,15–0,25 · alarma 0,05 · clic 0,35 · gas 0,06 · niebla 0,08–0,12 · cristal 1,1–1,5 · motor 0,4.
- Máster: −15 LUFS, pico −1,5 dBTP, AAC 192 kbps a 48 kHz.
- Música más corta que el vídeo: **un único empalme separado por un número entero de compases** (2,397 s) entre puntos de intensidad parecida, con desfase del pulso < ±20 ms.
- Subtítulos y acciones se anclan a la frase que los nombra; los cortes caen en el pulso.

## 10. Exportación y entrega

- H.264 High, CRF 16, preset slow, yuv420p, faststart.
- Nombres: `<DIVISION>-<SISTEMA>_<Vertical>_<IDIOMA>_<ancho>x<alto>.mp4`; portadas `Portada_….png`.
- Entrega final con los 8 archivos y una tabla resumen, seguida de la pregunta de feedback y del siguiente paso pendiente (p. ej. locución por generar).

## 10 bis. Piezas autoconclusivas para LinkedIn (solo 4:5)

Del vídeo completo salen 3–5 piezas que **se entienden solas** y se publican en cualquier orden.

- Solo 4:5; el 16:9 completo se enlaza en el primer comentario. SIEX → LinkedIn de SIEX; resto → LinkedIn de Grupo Komtes.
- **Una pregunta, una respuesta completa:** cada pieza cuenta la actuación entera hasta el resultado; la primera frase no depende de nada anterior.
- **Gancho en los primeros 3,2 s escrito sobre la imagen** (LinkedIn arranca sin sonido): antetítulo RED Inter Bold 22 «SISTEMA · VERTICAL» en (70, 92); pregunta Inter Display Bold 50 desde y = 128, máximo 2 líneas (≈65 caracteres); barra roja de 64×7.
- Sin «Capítulo n/N». Pasos renumerados dentro de cada pieza; con un solo paso, título sin número. Cierre igual en todas (3,4 s).
- 25–60 s con las mismas escenas, locución y música: no gasta créditos. Montaje: lista `PIECES` en `cpd_final.py` y `PIEZA=n python3 cpd_master.py <es|en> <voz.mp3> 45 <salida.mp4>`.
- Nombres: `…_1080x1350_LinkedIn<n>_<Tema>.mp4`; portada = fotograma del gancho.
- Documento de publicación: por pieza, texto listo para pegar (abre con la pregunta del gancho, 3–4 ideas con «→», 3–4 hashtags, sin enlace) y primer comentario con la web; calendario (una por semana, martes a jueves de 9 a 11 h), difusión del equipo en la primera hora y tabla de medición.

## 11. Materiales que se piden al ingeniero

«Para el vídeo de [sistema] en [vertical] necesito: 1) renders o fotos de [producto] en vista frontal y ¾ con fondo blanco, en su posición real de montaje; 2) la etiqueta real de [equipo]; 3) dónde se instala cada equipo, por dónde entra y sale el agua y hasta dónde llega cada tubería; 4) qué es cada pieza visible de las válvulas; 5) la ficha técnica con las aprobaciones vigentes; 6) si los tienes, vídeos de la competencia.»

## 12. Control de calidad (antes de cada entrega)

- **Transiciones:** tira de 6 fotogramas (p = 0,02–0,98; tiempos con `VO_TRT=1`): nada salta, logotipo, títulos y franja quietos, ningún rótulo residual.
- **Escenas:** hoja de contactos con un fotograma por escena en las cuatro versiones: producto fiel, imagen dentro de la ventana, subtítulos en 2 líneas, marca correcta, EN sin restos en español (`SIN TRADUCIR` vacío).
- **Etiquetas:** en un tramo renderizado en orden (§1 quater): fijas una vez visibles, por encima de las líneas, sin tapar puntos ajenos ni tarjetas. Todos los puntos rojos dentro de la ventana de imagen: con `TAG_WARN=1` el montaje avisa (`TAG_FUERA`) de los que caen en la cabecera o fuera del encuadre.
- **Tuberías:** en planos generales y de detalle, cada red acaba en su último difusor y las rutas animadas van encima de la tubería real.
- **Audio:** voz sin palabras cortadas, música sin duplicados, empalme a compás, −15 LUFS y duración esperada (`ffprobe`).
- **Técnica:** el ingeniero confirma nombres, cifras, aprobaciones, secuencia e instalación (§1 bis).

## 13. Errores ya cometidos (no repetir)

- **Producto y 3D:** cilindros sin etiqueta de marca · agujeros dibujados como relieve · insertos despegados · piezas inventadas · baterías exentas en vez de ancladas · válvulas en otra posición o con otra entrada/salida · más válvulas o colectores de los reales · **tuberías que siguen hasta la pared pasado el último difusor** · plano general como pasillo vacío.
- **Nombres y textos:** llamar «preacción» a una válvula de sección o de control · etiquetar una pieza con el nombre de otra (presostato frente a interruptor de confirmación) · «certificado» en lugar de la fórmula del emisor («aprobado por FM») · referencias con letras leídas como palabra · pronunciación de marca sin revisar · eslogan final sin leer · un producto explicado sin mostrarlo.
- **Etiquetas:** guías largas o posiciones al azar · pisando la pieza · tapando tarjetas · texto en inglés fuera de la pastilla · **pastillas que se mueven después de aparecer** · **guías de una etiqueta pasando por encima de otra pastilla** · **una pastilla tapando el punto rojo de otra** · validar etiquetas con fotogramas sueltos en vez de un tramo en orden · **punto rojo fuera de la ventana** (en la cabecera o fuera del encuadre: ánclalo al último tramo visible de la pieza).
- **Animación:** logotipo o rótulos escalándose · elementos que saltan en el zoom · rótulos que se quedan al salir · **ruta animada desplazada respecto a la tubería** (dibujada a mano en vez de desde los `KEY`) · ruta animada que invade la cabecera (recorta la capa a la ventana) · explicaciones en un recuadro en vez de a todo el ancho.
- **Audio y montaje:** empalme fuera de compás · música más corta que el vídeo · subtítulos y acciones desacompasados con la voz · series en capítulos que no se entienden por separado.
- **Proceso:** copiar la estética de la competencia · lanzar voz o transcripción sin avisar del coste · dar una fase por cerrada sin el OK del técnico · flechas de portada que no apuntan al punto exacto · corregir solo el minuto citado sin revisar los demás planos con el mismo problema · lanzar dos vídeos a la vez o encadenados en un mismo trabajo.

## 14. Operativa técnica (carpeta `codigo/` del kit)

**Comandos:**
- Plano 3D: `python3 cpd_scene.py <carpeta> <plano> [muestras] [escala] [led]` → PNG + JSON con los `KEY` (SIEX: `siex_scene.py`).
- Fotogramas sueltos: `VO_MODE=--still VO_TS=t1,t2 python3 cpd_master.py <es|en> <voz.mp3> <45|169> <prefijo>` (SIEX: `siex2_master.py`).
- Vídeo: `python3 cpd_master.py <es|en> <voz.mp3> <45|169> <salida.mp4>` — un vídeo por trabajo, de uno en uno.
- Solo audio: `VO_MODE=--audio VO_VIDEO=<salida>.noaudio.mp4 python3 cpd_master.py …`.
- Pieza de LinkedIn: `PIEZA=n python3 cpd_master.py es <voz.mp3> 45 <salida.mp4>`.
- Portadas: `python3 rg_covers.py` (SIEX: `siex_covers.py`).

**Mapa de observaciones → dónde se cambia:**

| Observación del ingeniero | Dónde | Qué hay que volver a generar |
|---|---|---|
| Texto en pantalla, subtítulo o etiqueta (ES) | Función de la escena en `cpd_final.py` | Vídeos |
| Traducción EN | Diccionario `EN` de `cpd_final.py` | Vídeos EN |
| Etiqueta en otra pieza o lado | Llamada a `tag()` de la escena (punto = `KEY` del componente) | Tramo de prueba + vídeos |
| Geometría (tubería, válvula, difusor, sala) | `cpd_scene.py` (y sus `KEY`) | Planos 3D afectados en carpeta nueva + portadas + vídeos |
| Ruta animada desplazada | `KEY` del plano en `cpd_scene.py` (nunca píxeles en `cpd_final.py`) | Planos afectados + vídeos |
| Duración u orden de escenas | `SCENES` y `SCENE_BLOCKS` de `cpd_final.py` | Vídeos |
| Locución | Guion + ElevenLabs (§1 ter) | Voz + vídeos |
| Portada | `rg_covers.py` | Portadas (segundos) |

- Escena nueva sin locución todavía: va en `SCENES` sin bloque en `SCENE_BLOCKS` y dura lo fijado; cuando llegue la voz se le asigna su bloque.
- Vídeo nuevo: duplica `cpd_scene.py`/`siex_scene.py`, `cpd_final.py` y `cpd_master.py`. No modifiques `cpd_video.py` ni la mezcla de audio, salvo el logotipo de la firma.
- Si el manual del kit (`Manual_Videos_Tecnicos_Komtes.md`) y esta skill discrepan, manda el que tenga **la versión más alta** en su cabecera; ante la duda, pregunta a Marketing.
