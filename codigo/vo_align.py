"""Alinea una locución con su texto: dónde empieza y acaba cada bloque (para el montaje).

Uso:  python3 vo_align.py <texto.txt> <locucion.mp3> [salida.blocks.json]

El texto es el que se envió a la voz: bloques separados por [pause]. Además se puede marcar con [cut] un corte
dentro de un bloque largo (en una coma o un punto) que NO se envió a la voz: el montaje lo trata como un bloque
más y deja un respiro entre las dos partes, para que cada frase caiga sobre su imagen.

Busca los silencios de la locución y asigna cada corte al silencio más probable según la longitud del texto
(los [pause] prefieren silencios largos; los [cut], cualquier respiro cercano). Escribe <locucion>.blocks.json con
'blocks' (inicio, fin), 'texts', 'sil' (todos los silencios) y 'sentences' (inicio de cada bloque).
Revisa siempre la tabla que imprime: duración y caracteres por segundo de cada bloque (≈14–18 es normal)."""
import sys, re, json, subprocess, os

if len(sys.argv) < 3:
    print(__doc__); sys.exit(2)
txt, mp3 = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(mp3)[0] + '.blocks.json'

raw = open(txt, encoding='utf-8').read()
parts, kinds = [], []
for chunk in re.split(r'(\[pause\]|\[cut\])', raw):
    if chunk in ('[pause]', '[cut]'):
        kinds.append(chunk[1:-1]); continue
    t = re.sub(r'\s+', ' ', re.sub(r'\[[a-zA-Z ]+\]', ' ', chunk)).strip()
    if t:
        parts.append(t)
assert len(kinds) == len(parts) - 1, 'texto mal formado'

dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3],
                           capture_output=True, text=True).stdout)
log = subprocess.run(['ffmpeg', '-hide_banner', '-i', mp3, '-af', 'silencedetect=noise=-38dB:d=0.15', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
sil = [(a, b) for a, b in zip(st, en)]
if len(st) > len(en):
    sil.append((st[-1], dur))
t0 = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
t1 = sil[-1][0] if sil and sil[-1][1] >= dur - 0.05 else dur
inner = [s for s in sil if s[0] > t0 + 0.3 and s[1] < t1 - 0.3]

n_pause = kinds.count('pause')
speech = (t1 - t0) - 0.85 * n_pause
rate = sum(len(p) for p in parts) / speech            # caracteres por segundo de habla

bounds = []                                           # (fin del bloque k, inicio del bloque k+1)
prev = t0
for k, kind in enumerate(kinds):
    exp = prev + len(parts[k]) / rate
    win = max(1.5, 0.22 * len(parts[k]) / rate)
    cand = [s for s in inner if s[0] > prev + 0.6 and abs(s[0] - exp) < win]
    if kind == 'pause':
        long_ = [s for s in cand if s[1] - s[0] >= 0.4]
        cand = long_ or cand
        score = lambda s: (s[1] - s[0]) * 2.5 - abs(s[0] - exp) / win
    else:
        score = lambda s: (s[1] - s[0]) * 1.0 - abs(s[0] - exp) / win * 1.5
    if cand:
        s = max(cand, key=score)
    else:
        s = (exp, exp)
        print(f'  ⚠ corte {k} ({kind}) sin silencio cercano: estimado en {exp:.2f} s — revísalo')
    bounds.append(s)
    prev = s[1]

starts = [t0] + [b for _, b in bounds]
ends = [a for a, _ in bounds] + [t1]
blocks = [[round(a, 2), round(b, 2)] for a, b in zip(starts, ends)]
json.dump({'blocks': blocks, 'texts': parts, 'kinds': kinds, 'sil': [[round(a, 3), round(b, 3)] for a, b in sil],
           'sentences': [[a] for a, _ in blocks]}, open(out, 'w'), ensure_ascii=False)
print(f'{len(parts)} bloques · habla {rate:.1f} car/s · {out}')
for i, ((a, b), p) in enumerate(zip(blocks, parts)):
    sep = '' if i == len(parts) - 1 else ('  ‖' if kinds[i] == 'pause' else '  ·cut')
    print(f'  {i:2d}  {a:7.2f}–{b:7.2f}  {b - a:5.1f} s  {len(p) / max(0.1, b - a):5.1f} c/s  {p[:60]}{sep}')
