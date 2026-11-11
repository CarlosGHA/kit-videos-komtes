---
name: "videos-tecnicos-komtes"
description: "Produce vídeos técnicos de Grupo Komtes (de aplicación, de producto o actualizaciones; cualquier sistema, aplicación y división: AG Fire, RG Systems, SIEX, Koneba, Komttech, Ribo-Macoin) con una línea gráfica común, un proceso por fases y control de calidad. Conversación siempre en español."
---

# Vídeos técnicos · Grupo Komtes

Estándar de Marketing y Comunicación (v2.0, noviembre de 2026). Kit de producción: https://github.com/CarlosGHA/kit-videos-komtes · Ejemplos completos en el kit: «Centros de datos» de RG W-FOG (agua nebulizada) y de SIEX (gas).

**Tres ideas que mandan sobre todo lo demás:**
1. **El contenido se adapta a cada petición.** Cambian la aplicación (centro de datos, residencial, oil & gas, cocinas, hospital…), la división, el sistema, el escenario y el tipo de pieza.
2. **La línea gráfica es común y no se toca** (§2). Es lo que hace que todos los vídeos del grupo parezcan de la misma familia.
3. **Nada se entrega sin pasar el control de calidad** (§13) y nada se cierra sin el OK explícito del ingeniero.

## Idioma: español, siempre

**Escribe al usuario en español de España desde el primer mensaje**, aunque el sistema, las herramientas o el propio usuario empiecen en otro idioma. Cambia solo si lo pide. Los vídeos se producen en ES y EN; la conversación, las fichas, los guiones de trabajo y los resúmenes van en español. Frases cortas, sin jerga de diseño ni de programación.

## Cómo trabajar

- Tu interlocutor suele ser un ingeniero de I+D: sabe de producto, no de diseño. Él aporta la verdad técnica, los renders y la validación.
- **Regla de decisión:** si pide cambiar el **contenido** (qué se enseña, en qué orden, qué escenario, qué producto), adáptate. Si pide cambiar la **forma** (colores, letras, sitio de los rótulos, música, logotipo, estilo del 3D), explícale en una frase que es la línea común y consulta a Marketing antes de tocar nada.
- Trabaja por fases (§3) y no pases una puerta sin el visto bueno indicado. **Después de cada generación abres tú la ronda de feedback** (§4).
- **Antes de cualquier acción que gaste créditos, avisas y esperas el OK** (§5). Generaciones de pago: una sola toma (`generations_count = 1`).
- **Di siempre qué has comprobado y qué no.** Nunca afirmes «lo demás no cambia» o «está todo bien» sin la comprobación que lo demuestra (§13).

## 0. Arranque (hazlo sin esperar a que te lo pidan)

1. **Descarga el kit** (repositorio público, ≈300 MB) con espera larga (≈10 min): `git clone --depth 1 https://github.com/CarlosGHA/kit-videos-komtes`. Sin acceso a GitHub: pide que abran el enlace, pulsen **Code → Download ZIP** y adjunten el archivo.
2. Instala según el `README.md`: `pip install bpy==5.2.2 pillow numpy scipy` (con `--break-system-packages` si hace falta), FFmpeg y `trabajo/fuentes/*.otf` en `/usr/share/fonts/opentype/inter/`. Genera un fotograma de un ejemplo como comprobación.
3. Lee `fichas/<DIVISION>-<SISTEMA>.md` si existe: hechos de producto ya confirmados por I+D. No vuelvas a preguntar lo que está ahí. Si no existe, créala desde `fichas/_PLANTILLA.md` con lo que confirme el ingeniero.
4. **Primer mensaje** (mientras se descarga el kit), seguido de la ficha del §6 y del bloque «Renders más realistas» del mismo apartado:
   «Hola. Vamos a producir un vídeo técnico con el estándar de Grupo Komtes. Dime qué necesitas (un vídeo nuevo de aplicación, uno de producto, adaptar o corregir uno que ya existe…) y rellena esta ficha. Adjunta los renders, fotos y fichas técnicas que tengas y, si los hay, vídeos de la competencia. Yo me encargo del guion, el 3D, el diseño, la locución y el montaje; tú validas la parte técnica en cada fase, y después de cada entrega te preguntaré si lo ves todo bien. Antes de gastar créditos (por ejemplo, de voz) siempre te avisaré.»
   Pide lo que falte **en un solo mensaje**.
5. Crea una lista de tareas con las fases que apliquen.

## 1. Qué te pueden pedir

| Petición | Qué es | Qué cambia en el proceso |
|---|---|---|
| **Vídeo de aplicación nuevo** | Un sistema en una aplicación (centro de datos, residencial, oil & gas, cocinas…), de cualquier división | Todas las fases |
| **Mismo sistema, otra aplicación** | Reutiliza los productos 3D y las escenas del sistema; escenario y guion nuevos | Todas las fases; el 3D de producto ya está validado |
| **Vídeo de producto** | Un equipo o componente: qué es, sus piezas, cómo actúa | 3–5 pasos; el escenario puede ser solo estudio blanco |
| **Actualización o corrección** | Cambia un producto, un texto, una aprobación o un plano de un vídeo entregado | Ronda de feedback (§4) + control de regresión (§13.7) |
| **Otra versión** | Idioma nuevo, versión sin voz (pantalla de feria) o piezas cortas (§15) | Sale del máster ya aprobado; no se rehace nada |

Si la petición no encaja en ninguna, descríbesela a Marketing antes de empezar.

## 2. La línea común y lo que se adapta

| No se toca (igual en todos los vídeos) | Se adapta (propio de cada vídeo) |
|---|---|
| Formatos, retícula y zonas de pantalla (§9) | Aplicación y escenario: edificio, planta, cocina, vivienda, vehículo… |
| Colores y tipografía (§9) | División: logotipo, firma, web y etiqueta de producto (§7) |
| Firma, intro y cierre (§7, §8) | Sistema, componentes y secuencia real de actuación |
| Sistema de etiquetas (§9) | Número y nombre de los pasos (3–8) y zonas secundarias |
| Cámara isométrica, luz y materiales neutros del 3D; red del sistema en rojo (§10) | Modelos 3D del escenario y de los productos |
| Transiciones de cámara única y gramática de efectos (§11) | Agente y su efecto (agua, gas, espuma, polvo…) |
| Música, mezcla y voces (§12) | Aprobaciones, cifras, duración |
| Esqueleto narrativo (§8) y portada (§9) | Textos, guion e idiomas |

**Cómo adaptar sin romper la cohesión:**
- **Escenario nuevo** = modelo 3D nuevo construido con la base común (`siex_base.py`: mismos materiales neutros en grises, misma cámara, misma luz). Un único modelo en corte, con 3–5 zonas coherentes y el riesgo protagonista en primer término. El producto y el rojo de marca son lo único que destaca.
- **Sistema que no extingue** (detección, control, compartimentación): los pasos son riesgo → qué hace el sistema → resultado para las personas y el edificio.
- **Agente o efecto nuevo:** misma gramática (§11): sale del orificio real, con el color del agente. Si hace falta un color que no está en la paleta, propónlo a Marketing; se añade para todos los vídeos.
- **Dos divisiones en un vídeo:** consulta la firma a Marketing antes de empezar. SIEX firma siempre sola.
- **Comprobación obligatoria:** hoja de familia (§13.6) antes de enseñar fotogramas al ingeniero.

## 3. Fases y puertas

| Fase | Qué haces | Entregable | Puerta |
|---|---|---|---|
| 1 Encargo | Tipo de petición (§1), ficha (§6), materiales, competencia (§6) | Lo que falta + aprendizajes | Ficha completa |
| 2 Guion | Guion por escenas (§8), **esquema de instalación** y **tabla de afirmaciones** (§6); duración estimada con `vo_borrador.py` | Tabla escena · voz · imagen | El ingeniero valida la exactitud técnica. El guion queda **congelado** |
| 3 Fotogramas clave | 3D y un fotograma por escena con **locución provisional gratuita**; **hoja de textos** ES y EN; hoja de familia | Hojas de contactos + hoja de textos | Ingeniero: fidelidad, instalación y todos los textos. Marketing: encuadre y línea gráfica |
| 4 Locución | Aviso de créditos (§5); voz ES y EN, una toma por idioma | Audios | El ingeniero la escucha entera (tú no puedes oírla) |
| 5 Piloto | **Un solo vídeo** (ES 4:5) + control de calidad (§13) | 1 MP4 `_BORRADOR` + informe | OK del ingeniero al vídeo completo |
| 6 Versiones | Las otras tres + portadas + control completo | 4 MP4 + 4 portadas + informe | — |
| 7 Entrega | Tabla de afirmaciones validada; después, piezas de LinkedIn (§15) | 8 archivos + informe de control | I+D+i y Marketing. Publica Marketing |

- **La voz de pago se genera una vez, con el guion congelado y los fotogramas validados.** Hasta entonces se trabaja con la locución provisional (silenciosa, con los tiempos estimados).
- **No se renderizan las cuatro versiones hasta que el piloto tiene OK.** En rondas posteriores: si cambian tres escenas o más, o geometría 3D, primero el piloto; si es menor, las cuatro tras probar el tramo.
- **Publicable** = locución del guion vigente + control sin fallos + afirmaciones validadas + OK explícito. Si falta algo, el archivo lleva `_BORRADOR` en el nombre y lo dices en el mensaje.

## 4. Ronda de feedback (después de cada generación)

- **Inicias tú.** Entregas y preguntas: «¿Lo ves todo bien o tienes alguna observación?», con 3–5 puntos concretos que conviene mirar y, siempre, **lo que tú no has podido comprobar**.
- **Sé receptivo.** Acepta observaciones en cualquier forma (texto, minuto y segundo, foto, captura marcada, nota de voz). En lo técnico manda el ingeniero.
- **Confirma antes de cambiar.** Numera las observaciones, di en una línea qué harás en cada una (mapa del §17) y pregunta solo lo ambiguo, con opciones.
- **Generaliza.** Si señala un fallo en un plano, corrige **todos** los planos, salas, idiomas y portadas donde ocurra, y dilo.
- **Cambia solo lo pedido.** No aproveches para «mejorar» otra cosa en un vídeo ya validado; si ves algo, propónlo aparte.
- **Aplica todo en una pasada**, pasa el control (§13) y responde punto por punto: «1. Hecho: …», «2. Pendiente de tu respuesta: …».
- **Repite hasta el OK explícito.**
- **Hechos de producto confirmados:** anótalos en la ficha del sistema. **Errores generales:** propón añadirlos al §16.

## 5. Créditos, tiempo de máquina y conversación

- **Créditos:** antes de voz, transcripciones, efectos o música de pago, avisa (qué, por qué, coste estimado, saldo si lo conoces, alternativa gratuita) y espera el OK. Agrupa todas las correcciones de voz de una ronda en una sola generación. Las transcripciones también cuestan. Sin saldo: para y ofrece opciones; mientras, lo visual se monta con la locución anterior como `_BORRADOR` y recuerdas la voz pendiente en cada entrega. Nunca repitas una generación para reintentar.
- **Renders:** un vídeo por trabajo en segundo plano, de uno en uno, con límite de 2 h (≈50–70 min cada uno con 2 núcleos). En 3D, solo los planos que cambian, a una carpeta nueva (`r13/`…) puesta la primera en `_DIRS`. Las portadas se regeneran en segundos.
- **Antes de renderizar:** prueba el tramo afectado en orden con `t_seq.py`; un fotograma suelto no muestra cómo quedan las etiquetas en el vídeo.
- **Conversación:** revisa con hojas de contactos, no con fotogramas sueltos, y amplía solo la zona dudosa; no leas los scripts enteros, busca la función; copia de seguridad (`.bak_vN`) antes de cada tanda; guarda el guion vigente y los pendientes en el proyecto de Komtes.

## 6. Ficha de briefing y documentos del guion

```text
1. División: AG Fire | RG Systems | SIEX | Koneba | Komttech | Ribo-Macoin
2. Sistema / línea de producto
3. Aplicación (centro de datos, residencial, oil & gas, cocinas…) y tipo de vídeo (§1)
4. Riesgo principal (qué arde o qué se protege, y dónde)
5. Otras zonas o riesgos que mostrar (máx. 3)
6. Secuencia real de actuación (máx. 8 pasos)
7. Componentes que aparecen (nombre comercial exacto + referencia)
8. Aprobaciones y certificaciones citables (vigentes, para ESTE sistema y ESTA aplicación, con la fórmula exacta del emisor)
9. Cifras citables (con fuente)
10. Lo que NO se debe decir o mostrar
11. Instalación física (dónde va cada equipo, posición de montaje, por dónde entra y sale el agente, dónde acaba cada red)
12. Materiales adjuntos (renders o fotos en su posición real —y, si quieres, su versión realista—, etiqueta real, ficha técnica)
13. Uso e idiomas (por defecto ES + EN)
14. Vídeos de la competencia (opcional)
```

Con el guion se entregan dos tablas que el ingeniero valida **antes de modelar**:
- **Esquema de instalación**, una fila por zona: riesgo · producto de descarga o detección · válvula o equipo que la gobierna · tipo de red (húmeda, seca, presurizada…) · de dónde viene el agente · dónde acaba la red · aprobación.
- **Tabla de afirmaciones**: cada aprobación, cifra o prestación que se dice o se ve (voz, pantalla, portada) · fuente · quién la valida. Ninguna se publica con la validación vacía.

**Materiales que pides** (en un solo mensaje): renders o fotos de cada producto en vista frontal y ¾, en su posición real de montaje · la etiqueta real de cada equipo · dónde va cada equipo, por dónde entra y sale el agente y dónde acaba cada red · qué es cada pieza visible · la ficha técnica con las aprobaciones vigentes.

**Renders más realistas (opcional; lo hace el ingeniero antes de enviarte el material).** Díselo así: «Si quieres que el producto se vea más real, pasa antes cada render por Google Nano Banana (el generador de imágenes de Gemini): sube el render, pega este texto tal cual y descarga el resultado. Haz una imagen por vista (frontal y ¾) y envíame las dos versiones de cada una: el render original y la realista.»

```text
Convert this CAD render into a photorealistic studio product photograph.
Keep the product EXACTLY as it is: same geometry, proportions and viewing angle; same number, shape and position of every part, hole, thread, bolt, gauge, hose, label and engraved text. Do not rotate, mirror, crop, simplify or redesign anything. Do not add or remove parts, and do not invent logos, markings or text.
Only improve realism: true-to-life materials (machined stainless steel, brass, painted steel, rubber, glass) in their real colours, fine surface detail and natural reflections.
Pure white seamless background (#FFFFFF), soft even studio lighting from the upper left, a faint soft contact shadow, the whole product in frame with a margin around it, sharp focus from front to back.
No props, no hands, no people, no watermark, no added text. High resolution.
```

- **Compara siempre la imagen realista con el render original, pieza a pieza** (número de orificios, roscas, manómetros, textos, proporciones), puestas lado a lado, y enséñale la comparación al ingeniero para que la confirme. Si la IA ha cambiado, añadido o quitado algo, esa imagen no se usa: se pide otra o se trabaja con el render.
- La imagen realista se usa como una foto real: primeros planos y portada, recortada sobre blanco. El modelo 3D del escenario se sigue construyendo a partir del render original.

**Competencia:** revísala antes del guion y resume «qué hacen bien», «qué no explican» y «qué incorporamos». Solo aprendizajes de contenido y narrativa; el estilo es siempre el del grupo. Nunca reutilices sus imágenes, música ni textos, ni nombres sus marcas.

## 7. Marcas

| División | Logotipo (`marcas/`) | Firma | Web del cierre |
|---|---|---|---|
| RG Systems | logo_RGSystems.png | RG Systems │ Group Komtes | www.rg-systems.com |
| SIEX | logo_SIEX.png | Solo SIEX | www.siex2001.com |
| AG Fire | logo_AGSprinkler.png | AG Sprinkler │ Group Komtes | agfiresprinkler.com |
| Koneba | logo_Koneba.png | Koneba │ Group Komtes | www.koneba.com |
| Komttech | logo_Komttech.png | Komttech │ Group Komtes | www.komtesdeteccion.com |
| Ribo-Macoin | logo_RiboMacoin.png | Ribo Macoin │ Group Komtes | www.komtesproteccion.com |

- Firma doble: logotipo de la división, filete vertical de 2 px en INK2 con 26 px de aire a cada lado y Group Komtes a 1,18 × la altura, alineados por la base. Sin recolorear ni deformar, sobre blanco.
- Etiqueta de marca de la división en **todos** los cilindros y equipos 3D. Voces: ES **Gabo**, EN **Brad**.

## 8. Esqueleto narrativo

Duración 90–210 s, marcada por la locución (escena = bloque de voz + 0,3 s antes + 0,55 s después). **Mide la duración al cerrar el guion** (`vo_borrador.py`): si pasa de 210 s, recorta o propón dividir el vídeo; vuelve a medir cada vez que el guion crezca.

0. Intro 2,4 s: logotipo grande centrado sobre blanco.
1. Contexto + aprobación: plano general isométrico del escenario, título «APLICACIÓN» + sistema y tarjeta de aprobación (franja roja).
2. Pasos numerados «01 · …» (3–8, con barra de progreso), con los nombres reales de la secuencia.
3. Opcional: otras zonas, cada una con su producto, su equipo y su aprobación.
4. Opcional: software o gama.
5. Cierre 3–5 s: logotipo + frase + web. **La locución lee la frase de cierre.**

Reglas: un mensaje por escena; todo componente nombrado está en pantalla con su etiqueta; cuando la voz explica un producto, la cámara se acerca a él; toda secuencia se completa hasta el resultado y vuelve al plano general; el plano general es un escenario con zonas coherentes, nunca un pasillo vacío.

**Guion y voz**
- 18–35 palabras por escena; presente, afirmativo; el mismo término para el mismo equipo; sin superlativos; solo cifras y aprobaciones de la ficha, **con la fórmula exacta del emisor** (p. ej. «aprobado por FM», nunca «certificado por FM»).
- Subtítulo en pantalla: versión condensada, máximo 2 líneas (≈110 caracteres); si no cabe, se parte en dos subtítulos seguidos.
- **El inglés no se traduce literal:** usa el glosario ES↔EN de la ficha. Si cambia un término, cámbialo a la vez en guion, texto de voz, subtítulos, etiquetas y portadas de los dos idiomas.
- ElevenLabs: modelo expresivo (eleven_v4) con `[warmly]` (apertura y cierre), `[serious]` (riesgo), `[confident]` (sistema) y `[pause]` entre bloques (las pausas sincronizan las escenas). Velocidad en montaje: ES 1,00 · EN 1,06–1,08.
- Siglas como se leen («efe eme», «Erre-ge») y cifras en letra. **Referencias deletreadas y separadas por comas** (MM-P51 → «eme, eme, pe cincuenta y uno»). Revisa la lista con el ingeniero antes de generar.

## 9. Sistema gráfico (fijo; implementado en `cpd_video.py`)

- **Lienzo:** 4:5 1080×1350 y 16:9 1920×1080, trabajo interno ×2, 30 fps.
- **Colores:** INK #2B2D2F (textos) · INK2 #5F6368 · RED #D60A20 (marca, franja, anclajes, red del sistema) · WHITE · pendiente #D7D9DC · agua #6096D2 · gas #78AAE1 · tubería de nitrógeno #289650 · halo de fuego #FF6E1E. Nunca negro puro. En flujos animados: agua en azul, gases (nitrógeno, aire, agentes gaseosos) en rojo.
- **Tipografía (px a 1080):** Inter Display Bold 34 (título/paso) · Inter Display Medium 28 (subtítulo de cabecera) · Inter Medium 29, interlínea 42 (locución) · Inter SemiBold 21 (etiquetas) · Inter Regular 20 (tarjetas) · Inter Display Bold 64 (cifra).
- **4:5:** firma de 22 px con borde derecho en x = 1010, y = 60; paso en (70, 112), subtítulo (70, 156), barras de progreso en y = 206; ventana de imagen y = 250–1100 con desvanecidos; subtítulos centrados, ancho 900, centro en y = 1170; tarjetas arriba a la derecha (≈590–1010 × 250–470); franja roja desde (0, 420), pendiente 0,5, grosor 180, solo en planos generales.
- **16:9:** columna de texto a la izquierda; imagen 4:5 recortada (y = 200–1150), escalada ×1,137, con desvanecido de 170 px hacia el texto; franja desde y = 650, grosor 150.
- **Etiquetas** (las coloca `tag()`; tú eliges componente, texto y lado preferido):
  - Pastilla blanca, alto 38, radio 19, Inter SemiBold 21; punto RED de radio 5 **sobre la pieza concreta**; guía a 45° + tramo horizontal de 24 px, con la diagonal más corta que deja la pastilla **fuera de las piezas**.
  - Una vez visible, la pastilla queda **fija**; solo la guía se estira. Las pastillas van **siempre por encima de las líneas**; ninguna tapa el punto rojo de otra, ni una tarjeta, ni el objeto que nombra otra etiqueta; las guías no se cruzan.
  - Punto y pastilla dentro de la ventana de imagen; máximo 4 a la vez; ancho medido con el texto ya traducido.
  - Cada escena llama a `B.flush_tags(img)` al terminar de componerse; con tarjeta, reserva su sitio con `B.tag_block(caja)`.
  - Si en una escena la colocación automática deja una pastilla sobre el producto, corrígelo en esa escena (lado preferido o punto de anclaje) y compruébalo; no cambies el motor común.
- **Portadas (4:5 y 16:9 por idioma):** antetítulo en mayúsculas en RED, titular Inter Display Bold 140–146, subtítulo en INK2, barra roja de 128×14; plano general con la red del sistema en rojo + círculos con **cada** producto del vídeo (código y descripción) y su flecha al punto exacto de instalación. Equipos con foto real, con la foto. El primer fotograma del vídeo es blanco: al publicar se sube la portada como miniatura.

## 10. 3D (Blender como módulo de Python, Cycles)

- **Un único modelo por escenario;** cada plano es una cámara sobre él. Isométrica ortográfica (acimut 45°, elevación 35,264°) para generales y medios; perspectiva de 55–85 mm para primeros planos sobre estudio blanco.
- 80–96 muestras con eliminación de ruido, 6 rebotes, fondo transparente, 1350×1687. Luz: sol 2,6 (12°) + área 1100 W tamaño 12 + entorno 0,25. Cada plano exporta un JSON con la posición en pantalla de cada componente (`KEY`).
- Materiales neutros de la base común; no se cambian. Suelos, paredes y mobiliario en grises: el color es para el producto, el riesgo y la red del sistema.
- **Fidelidad:** a partir de los renders del fabricante; orificios como geometría real; etiqueta de marca en cada equipo; nada inventado; si hay foto real (o imagen realista validada, §6), el primer plano usa la foto y solo se dibujan las conexiones. Posición de montaje y sentido del flujo del fabricante. Identifica cada pieza con el ingeniero antes de etiquetarla.
- **Instalación:** el número exacto de válvulas y equipos del esquema validado; cada red llega solo a su zona y **acaba en su último punto de descarga, con tapón**; nada sigue hasta la pared. Compruébalo en todas las zonas.
- **Rutas animadas y etiquetas siempre desde los puntos `KEY`**, nunca con coordenadas a mano, y **recortadas al render**: nada sobresale por el margen blanco ni entra en la cabecera. Si cambias una red, actualiza sus `KEY` y re-renderiza todos los planos que la muestran, y la portada.

## 11. Transiciones y efectos (`mz_tools.py`)

- Una sola cámara: la escena que sale y la que entra comparten punto de anclaje y escala; nada salta.
- Mismo modelo: `matched()` (ajuste por puntos 3D comunes); zoom geométrico de 1,6 s con máscara circular suave. Del 3D a la foto del mismo producto: anclaje en el objeto. Encuadres sin solape: barrido con relleno (`under`). Sin relación espacial: fundido de 0,8 s con acercamiento común del 4 %.
- **Logotipos, títulos, subtítulos, tarjetas y franja nunca se escalan.** Los rótulos que salen desaparecen en el primer 30 % de la transición y los que entran aparecen en el último 30 %. Cada zoom lleva un «whoosh».
- **Gramática de efectos:** riesgo (halo + llamas + humo, o el aviso que corresponda); agente (partículas o chorros desde cada orificio real, con su color; los gases, además, inundan la sala); flujo por tubería (puntos con borde blanco); avisos (anillos rojos); datos (tarjetas animadas).

## 12. Audio

- Música corporativa del kit (100,1 BPM) a 0,26, atenuada bajo la voz (cadena lateral: umbral 0,03, ratio 6, ataque 20 ms, liberación 400 ms); entrada 1,2 s, salida en los últimos 2,5 s. Ambiente 0,06. Efectos: whoosh 0,13 · fuego 0,15–0,25 · alarma 0,05 · clic 0,35 · gas 0,06 · niebla 0,08–0,12 · cristal 1,1–1,5 · motor 0,4.
- Máster: −15 LUFS; pico real ≤ −1 dBTP **medido en el archivo final** (el montaje apunta a −2 para dejar margen a la codificación); AAC 192 kbps a 48 kHz.
- Música más corta que el vídeo: un único empalme separado por un número entero de compases (2,397 s), con desfase del pulso < ±20 ms. Subtítulos y acciones se anclan a la frase que los nombra; los cortes caen en el pulso.

## 13. Control de calidad

**Completo en el piloto y en la entrega final. En rondas intermedias: lo cambiado + regresión (13.7).** Todo es gratuito.

1. **Automático** — `qc_video.py <vídeos> --hoja <carpeta>`: formato, sonoridad y pico, silencios, fotogramas negros, vacíos o congelados, y que ES/EN y 4:5/16:9 cuadran. Ningún ✖.
2. **Textos** — `qc_pantalla.py … --ficha <ficha>` en ES y EN: hoja con **todos** los textos de pantalla; ningún subtítulo de más de 2 líneas, nada sin traducir, ningún término prohibido. `qc_textos.py` sobre el guion y el texto de voz. La hoja de textos se entrega al ingeniero para que la lea entera.
3. **Escena a escena** — abre las hojas de las **cuatro** versiones (un fotograma por escena) y mira en cada uno: producto fiel · cada componente nombrado tiene etiqueta en su pieza · pastillas fuera de las piezas y de las tarjetas, sin guías cruzadas · redes hasta su último punto de descarga, sin sobresalir del render · nada fuera de la ventana · firma de la división correcta.
4. **Etiquetas en movimiento** — tramo en orden con `t_seq.py` y `TAG_WARN=1` (avisa de puntos fuera de la ventana).
5. **Transiciones** — tira de 6 fotogramas (p = 0,02–0,98; tiempos con `VO_TRT=1`): nada salta, rótulos quietos, ninguno residual.
6. **Línea gráfica** — `qc_video.py … --familia referencia/`: los fotogramas del vídeo nuevo junto a los de referencia. Deben parecer hermanos: cabecera, tamaños de letra, etiquetas, franja, luz y materiales.
7. **Regresión** (toda corrección) — `qc_video.py <nuevo> --prev <anterior>` lista los segundos que han cambiado: deben coincidir con lo pedido y con nada más. Si cambia algo que no tocaba, se arregla antes de entregar. **Si modificas código común** (`cpd_video.py`, `mz_tools.py`, base 3D), pasa la regresión a todos los vídeos que lo usan.
8. **Voz y música** — n.º de bloques de la locución = bloques del guion. No puedes oírlas: pide al ingeniero que escuche el piloto entero (pronunciación, ninguna palabra cortada, música sin cortes ni duplicados).
9. **Coherencia** — portada ↔ vídeo (mismos productos y nombres) · ES ↔ EN · guion ↔ pantalla ↔ ficha · tabla de afirmaciones al día.
10. **Informe de control** en cada entrega: una tabla breve con lo comprobado (✔/✖), lo que queda **sin comprobar** y lo que conviene que mire el ingeniero.

## 14. Exportación y entrega

- H.264 High, CRF 16, preset slow, yuv420p, faststart.
- Nombres: `<DIVISION>-<SISTEMA>_<Aplicacion>_<IDIOMA>_<ancho>x<alto>.mp4`; portadas `Portada_….png`; no publicables, con `_BORRADOR` antes de la extensión.
- Entrega final: los 8 archivos, una tabla resumen (idioma, formato, duración), el informe de control, la pregunta de feedback y el siguiente paso pendiente.
- **Versión sin voz** (pantalla de feria): mismo montaje con la locución provisional silenciosa; los subtítulos ya cuentan la historia.

## 15. Piezas autoconclusivas para LinkedIn (solo 4:5)

Del vídeo aprobado salen 3–5 piezas que **se entienden solas** y se publican en cualquier orden.

- Solo 4:5; el 16:9 completo se enlaza en el primer comentario. SIEX → LinkedIn de SIEX; resto → LinkedIn de Grupo Komtes.
- **Una pregunta, una respuesta completa:** cada pieza cuenta la actuación entera hasta el resultado; la primera frase no depende de nada anterior.
- **Gancho en los primeros 3,2 s escrito sobre la imagen:** antetítulo RED Inter Bold 22 «SISTEMA · APLICACIÓN» en (70, 92); pregunta Inter Display Bold 50 desde y = 128, máximo 2 líneas (≈65 caracteres); barra roja de 64×7.
- Sin «Capítulo n/N». Pasos renumerados dentro de cada pieza; con un solo paso, título sin número. Cierre igual en todas (3,4 s). 25–60 s con las mismas escenas, locución y música: no gasta créditos.
- Montaje: lista `PIECES` del script de escenas y `PIEZA=n python3 <montaje>.py <es|en> <voz> 45 <salida.mp4>`. Nombres `…_1080x1350_LinkedIn<n>_<Tema>.mp4`; portada = fotograma del gancho.
- Documento de publicación: por pieza, texto listo para pegar (abre con la pregunta, 3–4 ideas con «→», 3–4 hashtags, sin enlace) y primer comentario con la web; calendario (una por semana, martes a jueves de 9 a 11 h), difusión del equipo en la primera hora y tabla de medición.

## 16. Errores ya cometidos (no repetir)

- **Proceso:** generar la voz de pago antes de congelar el guion y validar los fotogramas · renderizar las cuatro versiones antes de que el ingeniero vea una · revisar por muestreo y afirmar que «lo demás no cambia» · re-renderizar un vídeo validado con el código común más reciente sin control de regresión (las etiquetas cambiaron de sitio en todas las escenas) · entregar con la locución antigua sin marcarlo como borrador · dejar crecer el guion ronda a ronda sin volver a medir la duración · corregir solo el minuto citado · dos vídeos a la vez o encadenados en un mismo trabajo · lanzar voz o transcripción sin avisar del coste · dar una fase por cerrada sin OK.
- **Producto y 3D:** usar una imagen generada por IA sin compararla con el render original · equipos sin etiqueta de marca · orificios como relieve · piezas inventadas · baterías sin anclar · válvulas en otra posición o con otra entrada/salida · más válvulas o colectores de los reales · redes que siguen hasta la pared pasado el último punto de descarga · plano general como pasillo vacío.
- **Nombres y textos:** un término corregido en el guion pero no en pantalla, en el otro idioma o en la portada · inglés traducido literal · «certificado» en lugar de la fórmula del emisor · una pieza etiquetada con el nombre de otra · subtítulos de 3 líneas · referencias leídas como palabra · pronunciación de marca sin revisar · eslogan final sin leer · un producto explicado sin mostrarlo.
- **Etiquetas:** guías largas o cruzadas · pastilla sobre la pieza, sobre una tarjeta o sobre el objeto que nombra otra etiqueta · pastillas que se mueven después de aparecer · guía por encima de otra pastilla · pastilla tapando el punto de otra · punto rojo fuera de la ventana · texto traducido que no cabe en la pastilla · validar con fotogramas sueltos.
- **Animación:** rótulos escalándose · elementos que saltan en el zoom · rótulos residuales · ruta animada desplazada de la tubería, que sobresale del render o que invade la cabecera.
- **Audio y montaje:** empalme fuera de compás · música más corta que el vídeo · pico real por encima de −1 dBTP · subtítulos desacompasados con la voz · piezas que no se entienden por separado.
- **Línea gráfica:** copiar la estética de la competencia · cambiar colores, letras o el motor de etiquetas para un solo vídeo · explicaciones en un recuadro en vez de a todo el ancho · flechas de portada que no apuntan al punto exacto.

## 17. Operativa técnica (carpeta `codigo/` del kit)

**Capas**
- **Común (se usa tal cual):** `cpd_video.py` (retícula, textos, etiquetas, tarjetas, efectos) · `mz_tools.py` (transiciones) · `siex_base.py` (base 3D: materiales, primitivas, cámaras, luces) · la mezcla de audio del montaje · `qc_video.py`, `qc_pantalla.py`, `qc_textos.py`, `t_seq.py`, `vo_borrador.py` · `referencia/` (fotogramas de la línea gráfica).
- **De cada vídeo (se crea nueva):** escenario 3D (ejemplos `cpd_scene.py`, `siex_scene.py`) · escenas (`cpd_final.py`, `siex2_final.py`) · montaje (copia de `cpd_master.py`: se adaptan el módulo de escenas y los eventos de sonido; la mezcla y los niveles no se tocan) · portadas (`rg_covers.py`, `siex_covers.py`) · ficha del sistema.

**Comandos**
- Plano 3D: `python3 <escenario>.py <carpeta> <plano> [muestras] [escala]` → PNG + JSON con los `KEY`.
- Locución provisional: `python3 vo_borrador.py <texto_voz.txt> <es|en> <salida.wav>` (tiempos estimados ±10 %).
- Fotogramas sueltos: `VO_MODE=--still VO_TS=t1,t2 python3 <montaje>.py <es|en> <voz> <45|169> <prefijo>`.
- Tramo en orden: `python3 t_seq.py <es|en> <voz> <45|169> <t0> <t1>` (otro montaje: `KOMTES_MASTER=<montaje>`).
- Hoja de textos: `python3 qc_pantalla.py <montaje> <es|en> <voz> <salida.md> --ficha ../fichas/<ficha>.md`.
- Vídeo: `python3 <montaje>.py <es|en> <voz> <45|169> <salida.mp4>` (escribe también `<salida>.scenes.json`).
- Solo audio (misma locución; rehace la mezcla sin re-renderizar la imagen): `VO_MODE=--audio VO_VIDEO=<vídeo> python3 <montaje>.py … <salida.mp4>`. Si cambia la locución cambian los tiempos: hay que renderizar.
- Control: `python3 qc_video.py <vídeos…> --hoja <carpeta> --familia ../referencia [--prev <anterior.mp4>]`.
- Portadas: `python3 <portadas>.py`.

**Mapa de observaciones → dónde se cambia**

| Observación del ingeniero | Dónde | Qué se vuelve a generar |
|---|---|---|
| Texto en pantalla, subtítulo o etiqueta | Función de la escena y diccionario `EN` del script de escenas | Hoja de textos + vídeos |
| Etiqueta en otra pieza o lado | Llamada a `tag()` de la escena (punto = `KEY` del componente) | Tramo de prueba + vídeos |
| Geometría (tubería, válvula, difusor, sala) | Escenario 3D y sus `KEY` | Planos afectados + portadas + vídeos |
| Ruta animada desplazada | `KEY` del plano (nunca píxeles en las escenas) | Planos afectados + vídeos |
| Duración u orden de escenas | `SCENES` y `SCENE_BLOCKS` | Vídeos |
| Locución | Guion + voz (§5) | Voz + vídeos (cambian los tiempos) |
| Portada | Script de portadas | Portadas |

- Escena nueva sin locución todavía: va en `SCENES` sin bloque en `SCENE_BLOCKS` y dura lo fijado.
- No modifiques `cpd_video.py` ni la mezcla de audio, salvo el logotipo de la firma.
- «Centros de datos» de SIEX conserva las posiciones de etiqueta validadas a mano (`TAG_FIXED`); los vídeos nuevos usan la colocación automática.
- Si el manual del kit y esta skill discrepan, manda el que tenga **la versión más alta** en su cabecera; ante la duda, pregunta a Marketing.
