"""Hoja de textos: lista TODOS los textos que salen en pantalla (títulos, subtítulos, etiquetas y tarjetas), en orden
de aparición, para que el ingeniero los revise de una vez antes de renderizar. No gasta créditos (≈3–5 min por idioma).

Uso:  python3 qc_pantalla.py <cpd_master|siex2_master> <es|en> <voz.mp3> <salida.md> [--ficha fichas/DIVISION-SISTEMA.md]

Recorre el vídeo a 1 fotograma por segundo sin escribirlo y anota cada texto dibujado. Además comprueba:
  · subtítulos de más de 2 líneas (formato 4:5)      · en inglés, textos que se han quedado sin traducir
  · con --ficha, los términos prohibidos de la ficha del sistema sobre lo que realmente se ve
Devuelve código 1 si hay algún fallo."""
import sys, os, re, importlib

if len(sys.argv) < 5:
    print(__doc__); sys.exit(2)
master, lang, vo, out = sys.argv[1:5]
ficha = sys.argv[sys.argv.index('--ficha') + 1] if '--ficha' in sys.argv else None
sys.argv = [master + '.py', lang, vo, '45', 'x.mp4']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.pop('VO_MODE', None)
M = importlib.import_module(master)
from PIL import ImageDraw
F, B = M.F, M.F.B
TR = getattr(F, 'TR', lambda s: s)
REV = {v: k for k, v in getattr(F, 'EN', {}).items() if isinstance(v, str)}
NOW = [0.0]
REC = {}            # (tipo, texto con cifras normalizadas) -> [t0, t1, mostrado, original, líneas, ancho]
FRAG = set()        # líneas sueltas de un párrafo ya anotado entero


def note(kind, shown, src, lines=1, maxw=0):
    if not re.search(r'[A-Za-zÁÉÍÓÚÑáéíóúñ]{2}', shown):
        return                                        # contadores y cifras sueltas que cambian cada fotograma
    key = (kind, re.sub(r'\d+', '#', shown))
    r = REC.get(key)
    if r is None:
        REC[key] = [NOW[0], NOW[0], shown, src, lines, maxw]
    else:
        r[1] = NOW[0]; r[4] = max(r[4], lines)


_wrap0 = B.wrap


def _wrap(text, f, maxw):
    lines = _wrap0(text, f, maxw)
    if isinstance(text, str) and text.strip():
        note('Subtítulo', ' '.join(lines), text, len(lines), maxw)
        FRAG.update(lines)
    return lines


B.wrap = _wrap
_text0 = ImageDraw.ImageDraw.text


def _text(self, xy, text, *a, **k):
    if isinstance(text, str) and text.strip() and text not in FRAG:
        fill = k.get('fill', a[0] if a else None)
        alpha = fill[3] if isinstance(fill, tuple) and len(fill) == 4 else 255
        if alpha > 60:
            shown = TR(text)
            note('Etiqueta' if k.get('font') is B.F_SMB else 'Título o tarjeta', shown, REV.get(text, text))
    return _text0(self, xy, text, *a, **k)


ImageDraw.ImageDraw.text = _text
fps = F.FPS
n = int(M.DUR * fps)
for fi in range(0, n, fps):
    NOW[0] = fi / fps
    M.render(fi)
    if fi % (30 * fps) == 0:
        print(f'{fi // fps} s de {n // fps}', flush=True)

mmss = lambda t: f'{int(t // 60)}:{int(t % 60):02d}'
rows = sorted(REC.items(), key=lambda kv: (kv[1][0], kv[0][0]))
en = lang == 'en'
L = [f'# Hoja de textos · {master.replace("_master", "")} · {lang.upper()}', '',
     'Todos los textos que aparecen en pantalla, en orden de aparición. Revisa ortografía, nombres, referencias, cifras y aprobaciones.', '',
     '| Aparece | Tipo | Texto en pantalla |' + (' Original en español |' if en else '') + ' Líneas |', '|---|---|---|' + ('---|' if en else '') + '---|']
long_ = []
for (kind, _), (t0, t1, shown, src, lines, maxw) in rows:
    L.append(f'| {mmss(t0)}–{mmss(t1 + 1)} | {kind} | {shown} |' + (f' {src if src != shown else "—"} |' if en else '') + f' {lines} |')
    if kind == 'Subtítulo' and lines > 2 and maxw >= 880:
        long_.append((t0, shown, lines))
fail = False
L += ['', '## Comprobaciones', '']
if long_:
    fail = True
    L += [f'- ✖ Subtítulo de {n_} líneas en {mmss(t)}: «{s}»' for t, s, n_ in long_]
else:
    L.append('- ✔ Ningún subtítulo pasa de 2 líneas.')
if en:
    miss = sorted(getattr(F, 'MISSING', ()))
    esp = sorted({shown for (_, _), (_, _, shown, _, _, _) in rows if re.search(r'[áéíóúñ¿¡]', shown)} - set(miss))
    if miss or esp:
        fail = True
        L += [f'- ✖ Sin traducir: «{s}»' for s in miss + esp]
    else:
        L.append('- ✔ Ningún texto se ha quedado en español.')
if ficha:
    import qc_textos
    hits = [(term, yes, shown, t0) for (_, _), (t0, _, shown, _, _, _) in rows for term, yes, pat in qc_textos.rules(ficha)
            if pat.search(qc_textos.norm(shown))]
    if hits:
        fail = True
        L += [f'- ✖ Término prohibido «{term}» en {mmss(t0)}: «{shown}»' + (f' → usar «{yes}»' if yes else '') for term, yes, shown, t0 in hits]
    else:
        L.append('- ✔ Ningún término prohibido de la ficha.')
open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L[L.index('## Comprobaciones'):]))
print(f'{len(rows)} textos → {out}')
sys.exit(1 if fail else 0)
