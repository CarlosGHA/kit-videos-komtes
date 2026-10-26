# Manual de producción de vídeos técnicos de aplicación · Grupo Komtes

**Versión 1.1 · octubre de 2026 · Responsable: Marketing y Comunicación**
Referencia de origen: vídeos «Centros de datos» de RG W-FOG (agua nebulizada) y SIEX (agentes limpios de inundación total), en ES/EN, 4:5 y 16:9.

---

## 0. Para qué sirve este documento

Permite que una persona de I+D, con conocimiento de producto pero sin formación en diseño, produzca junto a Claude un vídeo técnico de aplicación (vertical + sistema) con el mismo nivel visual que los vídeos de referencia.

**Toda la estética ya está decidida en este documento.** El ingeniero no elige colores, tipografías, encuadres, transiciones ni música: aporta la verdad técnica y valida. Si algo no está aquí, se pregunta a Marketing; no se improvisa.

### Reparto de papeles

| Quién | Aporta | Valida |
|---|---|---|
| **Ingeniero/a de I+D** | Vertical, división, producto(s), funcionamiento, secuencia real de actuación, renders y fotos de producto, datos técnicos y certificaciones | Exactitud técnica del guion, del 3D y de cada fotograma clave |
| **Claude** | Guion, locución, escenas 3D, composición, animación, audio, montaje, portadas, exportación | Cumplimiento de este manual (checklist del §12) |
| **Marketing** | Este estándar, imagen de marca de cada división, música | Aprobación final y publicación |

---

## 1. Flujo de trabajo (7 fases con puertas de validación)

No se pasa de fase sin la validación indicada. Cada corrección posterior a una puerta cuesta más (horas de render y créditos de voz).

| Fase | Qué se hace | Entregable | Puerta (quién aprueba) |
|---|---|---|---|
| **1. Briefing** | El ingeniero rellena la ficha del §2 y adjunta los materiales del §11 | Ficha completa | Claude confirma que no falta nada |
| **2. Guion técnico** | Claude redacta el guion por escenas (§4 y §5) | Tabla escena · texto · imagen | **Ingeniero:** exactitud técnica |
| **3. Locución** | Claude genera la voz ES y EN con ElevenLabs, **una sola toma por idioma** | Audio ES + EN | **Ingeniero:** pronunciación de marcas y términos |
| **4. Fotogramas clave** | Claude modela el 3D y entrega 1 fotograma por escena (y tiras de cada transición) | Hoja de fotogramas | **Ingeniero:** fidelidad de producto y de la secuencia. **Marketing:** encuadre |
| **5. Render** | Render de las 4 versiones (ES/EN × 4:5/16:9), una tras otra | 4 vídeos MP4 | — |
| **6. Revisión** | Visionado completo con el checklist del §12 | Lista de cambios numerada | **Ingeniero + Marketing** |
| **7. Entrega** | Correcciones, portadas y entrega unificada | 4 vídeos + 4 portadas en un solo mensaje | **Marketing** publica |

**Regla de créditos:** cualquier generación de pago (voz, música) se hace **una sola vez por corrección** (`generations_count = 1`), primero con estimación de coste. Los arreglos de pronunciación se intentan antes editando el audio existente, sin regenerar.

**Regla de correcciones:** las correcciones se entregan en una lista numerada, cada una con su minuto y segundo. Claude corrige y revisa los fotogramas afectados antes de volver a renderizar.

---

## 2. Ficha de briefing (la rellena el ingeniero)

Copiar, rellenar y entregar a Claude al inicio de la sesión.

```text
FICHA DE BRIEFING · VÍDEO TÉCNICO DE APLICACIÓN

1. División de Grupo Komtes:      [ AG Fire | RG Systems | SIEX | Koneba | Komttech | Ribo-Macoin ]
2. Sistema / línea de producto:    (p. ej. RG W-FOG alta presión; SIEX agentes limpios)
3. Vertical (aplicación):          (p. ej. centros de datos, hospitales, túneles de cables, parkings…)
4. Riesgo principal protegido:     (qué arde y dónde: rack, cuadro, transformador, cinta…)
5. Riesgos secundarios a mostrar:  (p. ej. sala de generadores, bajo suelo técnico) — máx. 2
6. Secuencia real de actuación, paso a paso (máx. 8 pasos):
   1) inicio del fuego …  2) detección …  3) alarma/retardo …  4) disparo …  5) descarga …  6) extinción …
7. Componentes que deben aparecer (nombre comercial exacto + referencia):
   - Boquilla/difusor:  …     - Detección: …     - Central: …
   - Almacenamiento (cilindros, bombas, depósito): …    - Válvulas: …
8. Certificaciones que se pueden citar (solo las vigentes y aplicables a ESTE sistema): FM / UL / VdS / CEPREVEN…
9. Cifras que se pueden decir (con fuente): presiones, tiempos, dB, concentraciones, tamaño de gota…
10. Lo que NO se debe decir o mostrar (limitaciones, claims no certificados, competidores):
11. Instalación física: dónde se ubica cada equipo (sala aledaña, pared, falso techo, bajo suelo…)
12. Materiales adjuntos (ver §11): renders · fotos · fichas técnicas · etiquetas · planos
13. Público y uso: LinkedIn / web / feria / comercial. Idiomas: ES + EN (por defecto)
```

---

## 3. Imagen de marca por división

| División | Archivo de logotipo (kit `marcas/`) | Firma en vídeo y portada | Web en el cierre | Voz ES / EN |
|---|---|---|---|---|
| **RG Systems** | `logo_RGSystems.png` | «RG Systems │ Group Komtes» | www.rg-systems.com | Gabo / Brad |
| **SIEX** | `logo_SIEX.png` | Solo SIEX (sin Komtes) | www.siex2001.com | Gabo / Brad |
| **AG Fire** | `logo_AGSprinkler.png` | «AG Sprinkler │ Group Komtes» | agfiresprinkler.com | Gabo / Brad |
| **Koneba** | `logo_Koneba.png` | «Koneba │ Group Komtes» | www.koneba.com | Gabo / Brad |
| **Komttech** | `logo_Komttech.png` | «Komttech │ Group Komtes» | www.komtesdeteccion.com | Gabo / Brad |
| **Ribo-Macoin** | `logo_RiboMacoin.png` | «Ribo Macoin │ Group Komtes» | www.komtesproteccion.com | Gabo / Brad |
| **Grupo** | `logo_GroupKomtes.png` | Segunda marca de la firma doble | — | — |

**Construcción de la firma doble:** logotipo de la división a la izquierda, filete vertical de 2 px en `INK2` con 26 px de aire a cada lado y logotipo de Group Komtes a la derecha, con su altura a 1,18 × la del logotipo de división y ambos alineados por la base. Los logotipos se usan tal cual (rojo `#D60A20` + gris oscuro), sin recolorear, deformar ni añadir efectos, siempre sobre fondo blanco.

- La firma pequeña va siempre arriba a la derecha (4:5) o arriba a la izquierda (16:9) y **no se mueve nunca**, ni siquiera en las transiciones.
- No se mezclan marcas de divisiones distintas en un mismo vídeo.
- Las etiquetas de los equipos en 3D llevan la marca de la división (p. ej. todos los cilindros SIEX con etiqueta SIEX; los cilindros RG UAC con etiqueta blanca RG Systems).

---

## 4. Estructura narrativa estándar

Duración objetivo: **90–140 s**. La marca la locución: cada escena dura lo que su bloque de voz + 0,3 s antes + 0,55 s después.

| # | Escena | Imagen | Rótulo superior | Fondo |
|---|---|---|---|---|
| 0 | **Intro** (2,4 s) | Logotipo grande centrado, aparece en 0,7 s | — | Blanco liso |
| 1 | **Contexto + certificación** | Plano general isométrico del edificio/instalación | Título: «VERTICAL» + sistema | Blanco con franja roja |
| 2 | **01 · Inicio del fuego** | Plano medio del riesgo (rack, máquina…) con fuego y humo | Cabecera de paso 01 | Blanco liso |
| 3 | **02 · Detección / activación** | Detectores o boquilla de cerca | Paso 02 | Blanco liso |
| 4 | **03 · Alarma o arranque del sistema** | Central, cilindros, grupo de bombeo | Paso 03 | Según plano |
| 5 | **04 · Descarga** | Producto en primer plano descargando | Paso 04 | Blanco liso |
| 6 | **05 · Zona secundaria** (bajo suelo, otra sala) | Corte o detalle | Paso 05 | Blanco liso |
| 7 | **06 · Extinción y vuelta a la actividad** | Vuelta al plano general, sin fuego | Paso 06 | Franja roja |
| 8 | **Otros riesgos del edificio** (opcional) | Sala aledaña con su propio sistema y su secuencia completa detección → extinción | Título | Franja roja |
| 9 | **Software / gama** (opcional) | Interfaz o familia de producto | Título | Franja roja |
| 10 | **Cierre** (3–5 s) | Logotipo + frase + web | — | Blanco liso |

Reglas:

- Entre 6 y 8 pasos numerados. Los números de paso son correlativos y la barra de progreso los refleja.
- **Un mensaje por escena.** Si una escena necesita dos ideas, se parte en dos.
- Cada vez que la locución nombra un componente, ese componente debe estar en pantalla con su etiqueta.
- Cuando la voz explica cómo funciona un producto (p. ej. «el nitrógeno impulsa el agua»), se hace un **acercamiento a ese producto** y se da el tiempo que haga falta.
- Toda secuencia de incendio se cierra: si aparece fuego, se muestra su detección, la descarga y la extinción, y se vuelve al plano general.

---

## 5. Guion y locución

### Redacción
- Bloques de **18–35 palabras por escena** (120–230 caracteres). Frases afirmativas, presente, sin subordinadas largas.
- Vocabulario técnico correcto y constante (el mismo término para el mismo equipo en todo el vídeo).
- Sin superlativos («el mejor», «el único») salvo que estén certificados.
- Solo cifras y certificaciones de la ficha de briefing.
- Subtítulos en pantalla: versión condensada del bloque, **máximo 2 líneas** (≈110 caracteres).

### Generación de voz (ElevenLabs)
| Parámetro | ES | EN |
|---|---|---|
| Voz | Gabo | Brad |
| Modelo | Expresivo (eleven_v4) con etiquetas de emoción | El mismo flujo |
| Velocidad en montaje | 1,00 | 1,06–1,08 |
| Tomas | 1 | 1 |

- Etiquetas permitidas: `[warmly]` en la apertura y el cierre, `[serious]` en el incendio, `[confident]` al explicar el sistema, y `[pause]` entre bloques. Las pausas separan los bloques y son las que usa el montaje para sincronizar las escenas.
- **Pronunciación:** las siglas se escriben como se leen en el texto para la voz. Por ejemplo, en español «UL» se escribe «u ele» y «FM», «efe eme»; las cifras, en letra («noventa decibelios»). Antes de generar, se revisa la lista de marcas con el ingeniero. En inglés, comprobar «SIEX».

---

## 6. Sistema gráfico (valores fijos)

### 6.1 Lienzo
| | 4:5 (vertical, LinkedIn) | 16:9 (web, presentaciones) |
|---|---|---|
| Resolución de salida | 1080 × 1350 | 1920 × 1080 |
| Trabajo interno | ×2 (2160 × 2700), reducción final con Lanczos | ×2 |
| Fotogramas por segundo | 30 | 30 |

### 6.2 Colores
| Token | Uso | HEX | RGB |
|---|---|---|---|
| `INK` | Títulos, textos, iconos | `#2B2D2F` | 43, 45, 47 |
| `INK2` | Subtítulos de cabecera, separador de firma | `#5F6368` | 95, 99, 104 |
| `RED` | Marca, franja, acentos, puntos de anclaje, red de tuberías del sistema | `#D60A20` | 214, 10, 32 |
| `WHITE` | Fondo y tarjetas | `#FFFFFF` | 255, 255, 255 |
| `PENDIENTE` | Pasos aún no alcanzados en la barra de progreso | `#D7D9DC` | 215, 217, 220 |
| Agua / niebla | Partículas de agua | `#6096D2` | 96, 150, 210 |
| Gas extintor | Chorros de gas | `#78AAE1` | 120, 170, 225 |
| Nitrógeno / impulsión | Flujo de N₂ | `#289650` | 40, 150, 80 |
| Fuego (halo) | Resplandor del incendio | `#FF6E1E` | 255, 110, 30 |

No se usa negro puro en ningún texto ni fondo.

### 6.3 Tipografía (Inter / Inter Display)
| Elemento | Fuente | Tamaño (px en 1080 de ancho) |
|---|---|---|
| Título o cabecera de paso | Inter Display Bold | 34 |
| Subtítulo de cabecera | Inter Display Medium | 28 |
| Subtítulo de locución | Inter Medium | 29 (interlínea 42) |
| Etiqueta de componente | Inter SemiBold | 21 |
| Texto pequeño de tarjeta | Inter Regular | 20 |
| Cifra destacada en tarjeta | Inter Display Bold | 64 |

### 6.4 Maquetación 4:5 (coordenadas en px, origen arriba a la izquierda)
| Elemento | Posición y reglas |
|---|---|
| Firma pequeña | Altura del logotipo 22 px; borde derecho en x = 1010; y = 60 |
| Cabecera de paso | «NN · TÍTULO» en (70, 112); subtítulo en (70, 156); barras de progreso de 52 × 6 px cada 60 px en y = 206 (6 pasos). Con 8 pasos: barras de 40 × 6 cada 47 px. Paso actual en RED, hechos en INK, pendientes en `#D7D9DC` |
| Título (escenas sin paso) | (70, 118) y subtítulo en (70, 162) |
| Ventana de imagen | De y = 250 a y = 1100, con desvanecido suave de 250 a 340 y de 1020 a 1100. La imagen 3D nunca invade cabecera ni subtítulos |
| Subtítulos | Centrados, ancho máximo 900 px, centro vertical en y = 1170 |
| Etiquetas | Pastilla blanca al 94 %, alto 38 px, radio 19, borde INK al 35 %. Línea guía INK al 80 % (1,5 px) hasta un punto RED de radio 5 sobre el componente. Se colocan en los márgenes (x ≈ 70 o x ≈ 600–640; y ≈ 260–330 o y ≈ 960–1060), nunca encima del producto. Máximo 4 a la vez |
| Tarjetas de dato | Blancas, radio 16, sombra suave. Esquina superior derecha de la ventana (≈ 590–1010 × 250–470) |
| Franja roja | Polígono diagonal desde (0, 420) con pendiente 0,5 y grosor 180 px. Solo en planos generales; estática en todas las transiciones |

### 6.5 Adaptación 16:9
- Columna de texto a la izquierda: firma en (80, 64); título o paso en Inter Display Bold 38; subtítulo de cabecera en Inter Display Medium 27; locución en Inter Medium 29 dentro de la columna.
- A la derecha va la imagen 4:5 recortada entre y = 200 e y = 1150, escalada ×1,137 y con un desvanecido de 170 px hacia la columna de texto.
- Franja roja: desde y = 650, pendiente 0,5 y grosor 150.

### 6.6 Portadas
- 4:5 y 16:9 por idioma. Antetítulo en mayúsculas, Inter Bold 40 px (sobre lienzo ×2), en RED; titular en Inter Display Bold 140–146 en INK; subtítulo en Inter Display Medium 54–56 en INK2; barra roja de 128 × 14 bajo el subtítulo.
- Imagen: plano general isométrico con la red del sistema resaltada en rojo y un círculo con el detalle del producto.
- Nombres: `Portada_<DIVISION>-<SISTEMA>_<Vertical>_<IDIOMA>_<ancho>x<alto>.png`

---

## 7. Estándar 3D (Blender, motor Cycles)

### 7.1 Cámaras
- **Planos generales y medios:** isométrica ortográfica con acimut 45° y elevación 35,264°. **Todos los planos del mismo edificio se hacen desde el mismo modelo y la misma orientación**, cambiando solo la escala y el encuadre. Es condición necesaria para que los zooms sean continuos (§8).
- **Primeros planos de producto:** perspectiva con objetivo de 55–85 mm, producto centrado y fondo de estudio blanco.

### 7.2 Render
| Parámetro | Valor |
|---|---|
| Muestras | 80–96, con eliminación de ruido |
| Rebotes | 6 |
| Fondo | Transparente |
| Resolución | 1350 × 1687 (vertical) |
| Iluminación | Sol 2,6 con ángulo de 12° + luz de relleno de área (1100 W, tamaño 12) + entorno a 0,25 |
| Salida adicional | JSON con la posición en pantalla de cada componente (para las etiquetas y los anclajes de zoom) |

### 7.3 Paleta de materiales (no se cambia)
| Elemento | Color base (RGB lineal) | Rugosidad / metálico |
|---|---|---|
| Suelo técnico (baldosa) | 0,80 · 0,81 · 0,82 | 0,45 |
| Paredes | 0,58 · 0,60 · 0,63 | 0,9 |
| Racks | 0,025 · 0,027 · 0,03 | 0,35 / 0,6 |
| Bandejas | 0,62 · 0,64 · 0,66 | 0,35 / metálico |
| Cable azul / amarillo | 0,05 · 0,18 · 0,55 / 0,85 · 0,62 · 0,05 | 0,5 |
| Acero inoxidable | 0,80 · 0,80 · 0,80 | 0,22 / metálico |
| Tubería de extinción, cilindros | Rojo 0,55 · 0,035 · 0,03 | 0,35 |
| Latón (válvulas) | 0,78 · 0,58 · 0,25 | 0,3 / metálico |
| Cilindro de nitrógeno | Verde 0,08 · 0,42 · 0,18 | 0,35 |

### 7.4 Fidelidad de producto (reglas aprendidas)
1. **Se modela a partir de los renders o fotos del fabricante.** El ingeniero valida el fotograma de producto antes del render final.
2. **Los agujeros son geometría real** (operaciones booleanas), nunca textura o relieve.
3. Las piezas van **integradas en su cuerpo**: insertos, placas y tornillería no pueden verse despegados.
4. **Cada cilindro lleva su etiqueta de marca** (franja envolvente con la etiqueta real), en el 3D y en las fotos.
5. **Sin geometría sobrante:** nada que no exista en la instalación real (varillas, soportes inventados).
6. Instalación verosímil: baterías ancladas a la pared, tuberías visibles y conectadas de punta a punta, el cilindro piloto en el lado correcto, las salas aledañas conectadas por tubería.
7. El plano general es un edificio real, no un pasillo vacío: incluye salas contiguas coherentes con la vertical.
8. Si un primer plano usa una foto de producto, se recorta el fondo para que pueda superponerse al 3D.

---

## 8. Animación y transiciones

### 8.1 Principio: una sola cámara
En toda transición, la imagen que sale y la que entra comparten **el mismo punto de anclaje y una escala proporcional**. Ningún elemento puede saltar de posición.

| Tipo | Cuándo | Cómo |
|---|---|---|
| **Zoom encajado** | Entre dos planos del mismo modelo 3D | La relación de escala y la posición se calculan a partir de los puntos 3D comunes. Zoom geométrico suave en 1,6 s. El plano general sigue debajo y el detalle se revela con una máscara circular suave |
| **Zoom anclado a producto** | Del 3D a la foto o al render del mismo producto, o a su detalle | Ancla en el mismo objeto (p. ej. la batería 3D → la foto de la batería). Relación de escala aproximada: tamaño real en pantalla de cada vista |
| **Barrido con relleno** | Dos encuadres del mismo modelo que no se solapan | Se rellena el recorrido con el plano general alineado |
| **Fundido** | Escenas sin relación espacial | 0,8 s, con un leve acercamiento común del 4 % y fondo fijo |

Reglas fijas:
- **Logotipos, títulos, subtítulos, tarjetas y franja roja no se escalan nunca.** Los rótulos se funden: los de la escena que sale desaparecen en el primer 30 % de la transición y los de la que entra aparecen en el último 30 %.
- Durante el zoom, las capas se recortan a la ventana de imagen.
- Ningún rótulo de la escena anterior puede quedar visible al terminar la transición.
- Cada zoom lleva un efecto de «whoosh» sincronizado.

### 8.2 Efectos visuales (biblioteca fija)
- **Fuego:** halo naranja + llamas + humo gris que sube. Siempre en un punto concreto del equipo afectado.
- **Agua nebulizada:** partículas azules desde cada orificio real de la boquilla, con niebla que baja.
- **Gas:** chorros azul claro desde los orificios del difusor, con inundación progresiva de la sala.
- **Flujo por tubería:** puntos rojos con borde blanco que recorren el trazado real (agua: azul; N₂: verde).
- **Avisos:** anillos rojos que se expanden desde el detector o la central.
- **Datos:** tarjetas con indicador (presión, dB, concentración) que se animan con la acción.

---

## 9. Audio

| Capa | Fuente | Nivel |
|---|---|---|
| Locución | ElevenLabs (§5) | Referencia |
| Música | Pista corporativa (100,1 BPM) | 0,26, atenuada bajo la voz con compresión por cadena lateral (umbral 0,03, ratio 6, ataque 20 ms, liberación 400 ms). Entrada en 1,2 s y salida en los últimos 2,5 s |
| Ambiente | Zumbido de sala técnica en bucle | 0,06 |
| Efectos | whoosh 0,13 · fuego 0,15–0,25 · alarma 0,05 · clic 0,35 · gas 0,06 · niebla 0,08–0,12 · cristal (ampolla) 1,1–1,5 · motor 0,4 | Sincronizados con la imagen |
| Máster | Normalización de sonoridad | −15 LUFS integrados, pico real −1,5 dBTP, AAC 192 kbps, 48 kHz |

**Regla de música:** si la pista es más corta que el vídeo, se alarga **con un único empalme cuya distancia sea un número entero de compases** (1 compás = 2,397 s a 100,1 BPM), en dos puntos de intensidad parecida. Un empalme fuera de compás hace que la música suene «dos veces a la vez».

---

## 10. Exportación y nombres

| Parámetro | Valor |
|---|---|
| Códec | H.264 High, CRF 16, preset *slow*, yuv420p, *faststart* |
| Versiones | ES 4:5 · ES 16:9 · EN 4:5 · EN 16:9 |
| Vídeo | `<DIVISION>-<SISTEMA>_<Vertical>_<IDIOMA>_<ancho>x<alto>.mp4` → p. ej. `RG-WFOG_DataCenter_ES_1080x1350.mp4` |
| Portada | `Portada_` + mismo nombre en `.png` |
| Entrega | **Un único mensaje** con los 4 vídeos y las 4 portadas, más una tabla con idioma, formato y duración |

---

## 11. Materiales que debe aportar el ingeniero

| Material | Formato mínimo | Para qué |
|---|---|---|
| Renders de cada producto (vista frontal, ¾ y detalle) | PNG ≥ 2000 px, fondo blanco o transparente | Modelar el 3D fiel y hacer los primeros planos |
| Fotos de la instalación tipo | JPG/PNG ≥ 2000 px | Disposición real de equipos y tuberías |
| Fichas técnicas | PDF | Datos, certificaciones, nombres comerciales |
| Etiquetas reales de cilindros y equipos | PDF/PNG | Etiquetado de los modelos 3D |
| Esquema de principio o plano | PDF | Recorrido de tuberías y ubicación de salas |
| Logotipos de certificación vigentes | Vectorial o PNG grande | Tarjeta de certificación |
| Secuencia de funcionamiento | Texto (ficha §2, punto 6) | Guion y orden de escenas |

**Cómo pedírselos (texto que Claude envía al ingeniero):**
> «Para el vídeo de [sistema] en [vertical] necesito: 1) renders de [producto] en vista frontal y ¾ con fondo blanco; 2) la etiqueta real de [cilindro/equipo]; 3) confirmación de dónde se instala [equipo] respecto a la sala protegida; 4) la ficha técnica con las certificaciones vigentes.»

---

## 12. Checklist de calidad (antes de cada entrega)

**Técnico (lo valida el ingeniero)**
- [ ] Todos los nombres comerciales, cifras y certificaciones coinciden con la ficha.
- [ ] La secuencia de actuación es la real y completa (detección → alarma → disparo → descarga → extinción).
- [ ] Cada producto mostrado es fiel: forma, acabado, agujeros reales, piezas integradas, etiquetas de marca.
- [ ] La instalación es verosímil: anclajes, tuberías continuas, ubicación de salas y equipos.

**Gráfico (lo valida Claude con fotogramas)**
- [ ] Logotipo, títulos y franja inmóviles en todas las transiciones.
- [ ] Ningún elemento salta de posición en los zooms (revisar la tira de cada transición).
- [ ] Ningún rótulo queda visible después de su escena.
- [ ] Las etiquetas no tapan el producto, máximo 4 a la vez, dentro de márgenes.
- [ ] Imagen siempre dentro de la ventana; subtítulos legibles, en 2 líneas como máximo.
- [ ] Marca correcta para la división (§3); textos de EN sin restos en español.

**Audio**
- [ ] La locución está sincronizada con su escena; no se corta ninguna palabra.
- [ ] La música no suena doble ni se corta (empalmes a compás); continúa hasta el final con salida suave.
- [ ] Siglas y marcas bien pronunciadas en los dos idiomas.
- [ ] Sonoridad del máster en −15 LUFS.

---

## 13. Errores ya cometidos (no repetir)

| Error | Corrección estándar |
|---|---|
| Cilindros sin etiqueta o con la etiqueta de otra marca | Etiqueta de marca en todos los cilindros, en 3D y en foto |
| Agujeros de boquilla representados como relieve | Agujeros reales por geometría |
| Insertos o placas de la boquilla despegados del cuerpo | Integrados y encajados en el cuerpo |
| Piezas inventadas (p. ej. una varilla junto a la boquilla en la bandeja) | Nada que no exista en la instalación real |
| Batería de cilindros exenta | Anclada a la pared, con la de reserva y las válvulas direccionales entre baterías |
| Producto explicado sin mostrarse | Acercamiento al producto cuando la voz lo explica |
| Explicaciones en un recuadro con aire | Ocupan todo el ancho de la ventana, igual que el resto |
| Logotipo y rótulos escalándose en los zooms | Capa de rótulos fija |
| Elementos que cambian de posición en el zoom | Cámara única con anclaje común (§8) |
| Rótulo («Fuego extinguido») que se queda en el zoom de salida | Los rótulos terminan antes de la transición |
| Plano general con un pasillo vacío | Edificio completo con salas coherentes |
| Música solapada o duplicada | Empalme único a compás (§9) |
| Pronunciación incorrecta de una marca en EN | Revisar la lista de marcas antes de generar y corregir editando el audio |

---

## 14. Anexo A · Mensaje de arranque para Claude

Pegar al inicio de cada sesión nueva, junto con este manual y la ficha de briefing:

```text
Vamos a producir un vídeo técnico de aplicación siguiendo el «Manual de producción de vídeos técnicos de aplicación · Grupo Komtes» (adjunto). 
Aplícalo de forma estricta: no tomes decisiones estéticas fuera de él.
División: [ ]   Sistema: [ ]   Vertical: [ ]
Adjunto la ficha de briefing y los materiales.
Trabaja por fases (§1) y no pases de fase sin mi validación. 
Las generaciones de pago (voz/música) se hacen una sola vez por corrección.
Empieza revisando la ficha y dime qué materiales faltan.
```

## 15. Anexo B · Herramientas de producción

El código de producción (escenas 3D, composición, transiciones con cámara única, montaje de audio y portadas) se publica, junto a este manual, en el repositorio público https://github.com/CarlosGHA/kit-videos-komtes (descarga: `git clone --depth 1 https://github.com/CarlosGHA/kit-videos-komtes`, o **Code → Download ZIP** desde el navegador). El kit es autónomo: incluye los recursos, los renders de referencia, las locuciones, la música, las tipografías y los logotipos. La instalación y los comandos están en su `LEEME.md`. También existe la skill `videos-tecnicos-komtes`, que aplica este manual automáticamente en cualquier sesión de Claude. Para cada vídeo nuevo se reutiliza el kit y solo se cambian las escenas 3D, el guion y los textos; el sistema gráfico, las transiciones y el audio no se tocan.

| Archivo | Función |
|---|---|
| `cpd_scene.py` / `siex_scene.py` | Modelos 3D y cámaras en Blender (base para nuevas verticales) |
| `label_wrap.py`, `make_labels.py`, `label_photo.py`, `cutout.py` | Etiquetas de cilindros y recorte de fotos de producto |
| `cpd_video.py` | Sistema gráfico: colores, tipografías, firma, franja, rótulos, etiquetas, tarjetas |
| `mz_tools.py` | Transiciones con cámara única (zoom encajado, anclado y barrido con relleno) |
| `cpd_final.py` / `siex2_final.py` | Escenas, tiempos y transiciones de cada vídeo de referencia |
| `cpd_master.py` / `siex2_master.py` | Sincronización con la locución, mezcla de audio, versión 16:9 y exportación |
| `rg_covers.py` / `siex_covers.py` | Portadas 4:5 y 16:9 |
| `sfx/` | Música corporativa (con el empalme a compás) y efectos de sonido |
| `marcas/` | Logotipos oficiales de las seis divisiones y de Group Komtes (PNG con fondo transparente) |
