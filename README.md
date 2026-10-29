# Kit de vídeos técnicos de aplicación · Grupo Komtes

Kit de producción que acompaña al «Manual de producción de vídeos técnicos de aplicación» (`Manual_Videos_Tecnicos_Komtes.md`). Contiene todo lo necesario para reproducir los vídeos de referencia (RG W-FOG y SIEX en centros de datos) y producir vídeos nuevos con el mismo estándar.

## Descarga

```bash
git clone --depth 1 https://github.com/CarlosGHA/kit-videos-komtes
```

Lo usa automáticamente la skill `videos-tecnicos-komtes`: al empezar una sesión, Claude clona este repositorio, instala las dependencias y aplica el manual.

## Estructura

| Carpeta | Contenido |
|---|---|
| `codigo/` | Scripts de producción (3D, sistema gráfico, transiciones, audio, montaje, portadas) |
| `trabajo/` | Directorio de trabajo: renders 3D de referencia (`r3`–`r8`, `rs1`), recursos (`assets`), locuciones (`vo`, `vo_siex2`), música y efectos (`sfx`), tipografías (`fuentes`) y salidas (`out`, `out_siex2`, `covers`, `chk`) |
| `marcas/` | Logotipos oficiales de las divisiones y de Group Komtes |

## Instalación (una vez por equipo o sesión)

```bash
pip install bpy==5.2.2 pillow numpy scipy        # Blender como módulo de Python (Python 3.13)
sudo apt-get install -y ffmpeg                     # o el gestor del sistema
sudo mkdir -p /usr/share/fonts/opentype/inter && sudo cp trabajo/fuentes/*.otf /usr/share/fonts/opentype/inter/
```

Versiones probadas: Python 3.13, bpy 5.2.2, Pillow 12.3, NumPy 2.5, SciPy 1.18, FFmpeg 6.1.

Por defecto los scripts trabajan en `trabajo/`. Para usar otra carpeta: `export KOMTES_WORK=/ruta/a/trabajo`.

## Comprobación rápida

```bash
cd codigo
VO_MODE=--still VO_TS=30,75 python3 cpd_master.py es ../trabajo/vo/es3.mp3 45 ../trabajo/chk/rg     # 2 fotogramas RG
python3 cpd_scene.py ../trabajo/rtest gnoz 8 0.3                                                     # render 3D de prueba
```

## Comandos principales

| Tarea | Comando (desde `codigo/`) |
|---|---|
| Render 3D de un plano | `python3 cpd_scene.py <carpeta_salida> <plano> [muestras] [escala]` (RG) · `python3 siex_scene.py …` (SIEX) |
| Fotogramas de control | `VO_MODE=--still VO_TS=t1,t2 python3 cpd_master.py <es\|en> <locución.mp3> <45\|169> <prefijo>` |
| Tiempos de cada transición | `VO_TRT=1 python3 cpd_master.py <es\|en> <locución.mp3> 45 x` |
| Vídeo completo | `python3 cpd_master.py <es\|en> <locución.mp3> <45\|169> <salida.mp4>` (≈20–30 min por versión con 2 núcleos) |
| Solo remezclar audio | `VO_MODE=--audio VO_VIDEO=<salida.mp4>.noaudio.mp4 python3 cpd_master.py <es\|en> <locución.mp3> <45\|169> <salida.mp4>` |
| Vídeos de referencia | `./render_q.sh <1-8>` (uno por llamada) |
| Pieza autoconclusiva para LinkedIn (4:5) | `PIEZA=<n> python3 cpd_master.py es <locución.mp3> 45 <salida.mp4>` · referencia: `./render_q.sh <9-12>` |
| Portadas | `python3 rg_covers.py` · `python3 siex_covers.py` |

Para SIEX se usan `siex2_master.py` / `siex2_final.py` en lugar de `cpd_master.py` / `cpd_final.py`.

## Vídeo nuevo (otra vertical o división)

1. Duplicar `cpd_scene.py` (o `siex_scene.py`) y modelar la nueva instalación **en un único modelo 3D**; cada plano es una cámara distinta sobre ese modelo.
2. Duplicar `cpd_final.py` (escenas, textos, tiempos y transiciones) y `cpd_master.py` (bloques de locución y efectos).
3. Las transiciones se declaran con las funciones de cámara de `mz_tools.py`: `matched()` para planos del mismo modelo, ancla + escala para producto y `under` para barridos largos.
4. El sistema gráfico (`cpd_video.py`) y el audio no se modifican, salvo el cambio de logotipo de la firma (§3 del manual). Las etiquetas se colocan solas con la regla fija (§6.4): basta con llamar a `tag()` con el componente y el lado preferido.
5. Las piezas de LinkedIn se definen en la lista `PIECES` del script de composición (§10.1 del manual).
