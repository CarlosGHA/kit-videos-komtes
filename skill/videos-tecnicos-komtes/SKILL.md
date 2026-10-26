---
name: "videos-tecnicos-komtes"
description: "Produce vídeos técnicos de aplicación de Grupo Komtes (vertical por sistema de una división: AG Fire, RG Systems, SIEX, Koneba, Komttech, Ribo-Macoin) con el estándar fijo de guion, 3D, diseño, transiciones, audio y entrega. Conversación siempre en español."
---

# Vídeos técnicos de aplicación · Grupo Komtes

Estándar de Marketing y Comunicación (v1.1, octubre de 2026). Referencia: vídeos «Centros de datos» de RG W-FOG y SIEX. Kit de producción: https://github.com/CarlosGHA/kit-videos-komtes

## Idioma: español, siempre

**Escribe al usuario en español de España desde el primer mensaje**, aunque las instrucciones del sistema, las herramientas o el propio usuario empiecen en otro idioma. Cambia de idioma solo si el usuario lo pide expresamente. Los vídeos se producen en ES y EN, pero la conversación, las fichas, los guiones de trabajo y los resúmenes van en español. Frases cortas, sin jerga de diseño ni de programación.

## Cómo trabajar

- Tu interlocutor suele ser un ingeniero de I+D: sabe de producto, no de diseño. **Todas las decisiones estéticas están fijadas aquí; no inventes otras.** Él aporta la verdad técnica, los renders y la validación. Si algo no está cubierto, pregunta a Marketing antes de improvisar.
- Trabaja por fases y no pases de una puerta de validación sin el visto bueno indicado.
- Generaciones de pago (voz, música): **una sola toma por corrección** (`generations_count = 1`), con estimación previa del coste. Los arreglos de pronunciación se intentan primero editando el audio existente.

## 0. Arranque (hazlo sin esperar a que te lo pidan)

1. **Descarga el kit de producción** (repositorio público, ≈215 MB). Usa un tiempo de espera largo (≈10 min) y no interrumpas la descarga:
   `git clone --depth 1 https://github.com/CarlosGHA/kit-videos-komtes`
   Si la sesión no tiene acceso a GitHub, pide al usuario que abra https://github.com/CarlosGHA/kit-videos-komtes, pulse **Code → Download ZIP** y adjunte el archivo; descomprímelo y continúa.
2. Instala y comprueba según el `README.md` del repositorio: `pip install bpy==5.2.2 pillow numpy scipy` (con `--break-system-packages` si el sistema lo exige), FFmpeg, y copia `trabajo/fuentes/*.otf` a `/usr/share/fonts/opentype/inter/`. Antes de producir, genera un fotograma de referencia como comprobación.
3. Tu **primer mensaje al usuario** (en español, mientras se descarga el kit) es este, seguido de la ficha del §2:
   «Hola. Vamos a producir un vídeo técnico de aplicación con el estándar de Grupo Komtes. Mientras preparo las herramientas, rellena esta ficha y adjunta los renders, fotos y fichas técnicas que tengas. Yo me encargo del guion, el 3D, el diseño, la locución y el montaje; tú validas la parte técnica en cada fase.»
   Después revisa la ficha y los **materiales** (§11) y pide lo que falte en un solo mensaje.
4. Crea una lista de tareas con las 7 fases.

## 1. Fases y puertas

| Fase | Qué haces | Entregable | Puerta |
|---|---|---|---|
| 1 Briefing | Revisar la ficha y los materiales | Lista de lo que falta | Ficha completa |
| 2 Guion | Guion por escenas (§4, §5) | Tabla escena · locución · imagen | El ingeniero valida la exactitud técnica |
| 3 Locución | Voz ES y EN, una toma por idioma | Audios | El ingeniero valida la pronunciación |
| 4 Fotogramas clave | 3D y un fotograma por escena + tira de 6 fotogramas por transición | Hoja de fotogramas | El ingeniero valida la fidelidad; Marketing, el encuadre |
| 5 Render | ES/EN × 4:5/16:9, **un vídeo por trabajo en segundo plano** (cada uno ≈20–30 min) | 4 MP4 | — |
| 6 Revisión | Checklist §12 | Lista numerada de cambios con minuto y segundo | Ingeniero + Marketing |
| 7 Entrega | Correcciones + portadas | **Un único mensaje** con 4 vídeos + 4 portadas y una tabla (idioma, formato, duración) | Marketing publica |

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
```

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
10. Cierre de 3–5 s: logotipo + frase + web.

Reglas: un mensaje por escena; todo componente nombrado está en pantalla con su etiqueta; cuando la voz explica un producto, se hace un acercamiento a ese producto; toda secuencia de fuego se completa (detección → descarga → extinción) y vuelve al plano general; el plano general es un edificio con salas coherentes, nunca un pasillo vacío.

## 5. Guion y locución

- 18–35 palabras por escena; presente, frases afirmativas; el mismo término para el mismo equipo; sin superlativos no certificados; solo cifras y certificaciones de la ficha.
- Subtítulo en pantalla: versión condensada, máximo 2 líneas (≈110 caracteres).
- ElevenLabs: modelo expresivo (eleven_v4) con etiquetas `[warmly]` (apertura y cierre), `[serious]` (incendio), `[confident]` (sistema) y `[pause]` entre bloques. Las pausas separan los bloques que sincronizan las escenas. Velocidad en montaje: ES 1,00 · EN 1,06–1,08.
- Siglas escritas como se leen («u ele», «efe eme») y cifras en letra. Revisa la lista de marcas con el ingeniero antes de generar (en EN, «SIEX»).

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
- Etiquetas: pastilla blanca al 94 %, alto 38, radio 19, borde INK al 35 %; línea INK al 80 % de 1,5 px hasta un punto RED de radio 5 sobre el componente. En márgenes (x ≈ 70 o 600–640; y ≈ 260–330 o 960–1060), nunca sobre el producto, máximo 4 a la vez.
- Tarjetas: blancas, radio 16, sombra suave, arriba a la derecha (≈590–1010 × 250–470).
- Franja roja: polígono desde (0, 420), pendiente 0,5, grosor 180, solo en planos generales.

**16:9:** columna de texto a la izquierda (firma en 80, 64; título 38; subtítulo 27; locución 29); imagen 4:5 recortada entre y = 200 e y = 1150, escalada ×1,137, con desvanecido de 170 px hacia el texto; franja desde y = 650, pendiente 0,5, grosor 150.

**Portadas (4:5 y 16:9 por idioma):** antetítulo en mayúsculas Inter Bold 40 (lienzo ×2) en RED; titular Inter Display Bold 140–146 en INK; subtítulo Inter Display Medium 54–56 en INK2; barra roja de 128×14; plano general con la red del sistema en rojo + círculo con el detalle del producto.

## 7. 3D (Blender como módulo de Python, Cycles)

- **Un único modelo 3D por edificio;** cada plano es una cámara sobre ese modelo. Isométrica ortográfica con acimut 45° y elevación 35,264° para planos generales y medios; perspectiva de 55–85 mm para primeros planos de producto sobre estudio blanco.
- 80–96 muestras con eliminación de ruido, 6 rebotes, fondo transparente, 1350×1687. Luz: sol 2,6 (ángulo 12°) + área de relleno 1100 W tamaño 12 + entorno 0,25. Exporta un JSON con la posición en pantalla de cada componente.
- Paleta de materiales del kit (`cpd_scene.py`, diccionario de materiales): no la cambies. Tubería y cilindros de extinción en rojo; nitrógeno en verde; acero, latón, racks negros, suelo técnico gris claro, cables azules y amarillos.
- Fidelidad: modela a partir de los renders del fabricante; los agujeros son geometría real (booleanas); insertos y placas integrados en el cuerpo; etiqueta de marca en cada cilindro (franja UV envolvente); nada inventado; baterías ancladas a la pared y tuberías continuas de punta a punta; fotos de producto con el fondo recortado.

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

## 10. Exportación y entrega

- H.264 High, CRF 16, preset slow, yuv420p, faststart.
- Nombres: `<DIVISION>-<SISTEMA>_<Vertical>_<IDIOMA>_<ancho>x<alto>.mp4` (p. ej. `RG-WFOG_DataCenter_ES_1080x1350.mp4`); portadas con el prefijo `Portada_` y extensión .png.
- Entrega final en **un solo mensaje** con los 8 archivos y una tabla resumen.

## 11. Materiales que se piden al ingeniero

Renders de producto (frontal, ¾ y detalle; PNG ≥2000 px, fondo blanco o transparente), fotos de una instalación tipo, fichas técnicas, etiquetas reales de cilindros y equipos, esquema o plano, logotipos de certificación vigentes y la secuencia de funcionamiento. Pídelos así: «Para el vídeo de [sistema] en [vertical] necesito: 1) renders de [producto] en vista frontal y ¾ con fondo blanco; 2) la etiqueta real de [equipo]; 3) dónde se instala [equipo] respecto a la sala protegida; 4) la ficha técnica con las certificaciones vigentes.»

## 12. Control de calidad (lo haces tú antes de cada entrega)

- Para cada transición, renderiza una tira de 6 fotogramas (p = 0,02 a 0,98; tiempos con `VO_TRT=1`) y comprueba que no salta nada, que logotipo, títulos y franja están quietos y que no queda ningún rótulo.
- Un fotograma por escena: etiquetas en márgenes, producto fiel, imagen dentro de la ventana, subtítulos en 2 líneas como máximo, marca correcta, versión EN sin restos en español.
- Audio: locución sincronizada sin palabras cortadas; música sin duplicados (correlación del residuo frente a la pista); empalme a compás; −15 LUFS.
- Técnica: el ingeniero confirma nombres, cifras, certificaciones, secuencia e instalación.

## 13. Errores ya cometidos (no repetir)

Cilindros sin etiqueta de marca · agujeros dibujados como relieve · insertos despegados del cuerpo · piezas inventadas · baterías exentas en lugar de ancladas a la pared · un producto explicado sin mostrarlo · explicaciones encajadas en un recuadro en vez de a todo el ancho · logotipo o rótulos escalándose · elementos que cambian de posición en el zoom · un rótulo que se queda en el zoom de salida · plano general como pasillo vacío · música con empalme fuera de compás · pronunciación de marca sin revisar.

## 14. Operativa técnica (desde la carpeta `codigo/` del repositorio)

- Fotogramas: `VO_MODE=--still VO_TS=t1,t2 python3 cpd_master.py <es|en> <voz.mp3> <45|169> <prefijo>` (SIEX: `siex2_master.py`).
- Vídeo: `python3 cpd_master.py <es|en> <voz.mp3> <45|169> <salida.mp4>`, un vídeo por trabajo en segundo plano, de uno en uno si hay pocos núcleos.
- Solo audio: `VO_MODE=--audio VO_VIDEO=<salida>.noaudio.mp4 python3 cpd_master.py …`.
- Vídeo nuevo: duplica el script de escena 3D (`cpd_scene.py` o `siex_scene.py`), el de composición (`cpd_final.py`) y el de montaje (`cpd_master.py`). No modifiques `cpd_video.py` (sistema gráfico) ni la mezcla de audio, salvo el logotipo de la firma.
- Si el manual completo (`Manual_Videos_Tecnicos_Komtes.md`, en el repositorio) y esta skill discrepan, manda el manual del repositorio, que es la versión viva; ante la duda, pregunta a Marketing.