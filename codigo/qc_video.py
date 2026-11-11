"""Control de calidad automático de vídeos terminados (no gasta créditos).

Uso:
  python3 qc_video.py <video.mp4> [más vídeos...] [--prev <anterior.mp4>] [--hoja <carpeta>] [--familia <referencia/>]

Por cada vídeo comprueba:
  · formato de entrega (H.264 High, yuv420p, 30 fps, 1080x1350 o 1920x1080, AAC 48 kHz estéreo, faststart)
  · audio (sonoridad −15 LUFS ±1, pico real ≤ −1 dBTP medido en el archivo final, sin silencios de más de 1,5 s)
  · imagen (sin fotogramas negros ni vacíos, sin congelados de más de 6 s)
  · que ES y EN del mismo formato existen y que 4:5 y 16:9 del mismo idioma duran lo mismo
--prev   compara con la versión anterior y lista los segundos que han cambiado (control de regresión: deben
         coincidir con las correcciones pedidas y con nada más). Solo con un vídeo.
--familia <carpeta referencia/>  guarda una hoja con fotogramas de los vídeos de referencia encima de los del vídeo
         nuevo, para comprobar a ojo que mantiene la línea gráfica común.
--hoja   guarda hojas de contactos con un fotograma por escena (dos en las largas) usando <video>.scenes.json
         (lo escribe el montaje; para un vídeo ya hecho: VO_MODE=--scenes python3 cpd_master.py <es|en> <voz> <45|169> <video>.scenes.json).
         Sin ese archivo, un fotograma cada 6 s.
Devuelve código 1 si hay algún fallo (✖). Los avisos (!) se revisan a ojo."""
import sys, os, re, json, subprocess, struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OK, WARN, BAD = '✔', '!', '✖'


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def mmss(t):
    return f'{int(t // 60)}:{t % 60:04.1f}'


def probe(v):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', v]).stdout)


def faststart(v):
    """True si el índice (moov) va antes que los datos (mdat): el vídeo empieza a reproducirse sin descargarse entero."""
    with open(v, 'rb') as f:
        pos, size = 0, os.path.getsize(v)
        while pos < size:
            f.seek(pos); h = f.read(16)
            if len(h) < 8:
                break
            n, typ = struct.unpack('>I4s', h[:8])
            if n == 1:
                n = struct.unpack('>Q', h[8:16])[0]
            if typ == b'moov':
                return True
            if typ == b'mdat':
                return False
            if n < 8:
                break
            pos += n
    return False


def gray_frames(v, fps=2, w=160):
    """Fotogramas en gris a baja resolución (para detectar vacíos y comparar versiones)."""
    st = next(s for s in probe(v)['streams'] if s['codec_type'] == 'video')
    h = int(round(w * st['height'] / st['width'] / 2)) * 2
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', v, '-vf', f'fps={fps},scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.int16)


def ranges(ts, step):
    """Agrupa instantes consecutivos en tramos [(inicio, fin)]."""
    out = []
    for t in ts:
        if out and t - out[-1][1] <= step * 1.5:
            out[-1][1] = t
        else:
            out.append([t, t])
    return [(a, b + step) for a, b in out]


def check(v):
    res = []          # (símbolo, texto)
    add = lambda ok, txt, warn=False: res.append(((OK if ok else (WARN if warn else BAD)), txt))
    p = probe(v)
    vs = next(s for s in p['streams'] if s['codec_type'] == 'video')
    aus = [s for s in p['streams'] if s['codec_type'] == 'audio']
    dur = float(p['format']['duration'])
    wh = (vs['width'], vs['height'])
    add(wh in ((1080, 1350), (1920, 1080)), f'tamaño {wh[0]}x{wh[1]}')
    add(vs['codec_name'] == 'h264' and vs.get('profile') == 'High' and vs['pix_fmt'] == 'yuv420p',
        f"vídeo {vs['codec_name']} {vs.get('profile')} {vs['pix_fmt']}")
    add(vs['r_frame_rate'] == '30/1', f"{vs['r_frame_rate']} fps")
    add(len(aus) == 1 and aus[0]['codec_name'] == 'aac' and aus[0]['sample_rate'] == '48000' and aus[0]['channels'] == 2,
        'audio ' + (f"{aus[0]['codec_name']} {aus[0]['sample_rate']} Hz {aus[0]['channels']} canales" if aus else 'AUSENTE'))
    add(faststart(v), 'faststart (índice al principio)')
    # audio: silencios + sonoridad y pico real en una sola pasada
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-i', v, '-vn', '-af', 'silencedetect=noise=-50dB:d=1.5,loudnorm=print_format=json',
             '-f', 'null', '-']).stderr
    m = re.search(r'\{[^{}]*"input_i"[^{}]*\}', r, re.S)
    if m:
        ln = json.loads(m.group(0)); I, TP = float(ln['input_i']), float(ln['input_tp'])
        add(-16.0 <= I <= -14.0, f'sonoridad {I:.1f} LUFS (objetivo −15 ±1)')
        res.append((OK if TP <= -1.0 else (WARN if TP <= -0.5 else BAD), f'pico real {TP:.2f} dBTP (objetivo ≤ −1; fallo por encima de −0,5)'))
    else:
        add(False, 'no se pudo medir el audio')
    sil = [(float(a), float(b)) for a, b in zip(re.findall(r'silence_start: ([\d.]+)', r), re.findall(r'silence_end: ([\d.]+)', r))]
    sil = [(a, b) for a, b in sil if b < dur - 0.2]       # el final se desvanece: no cuenta
    add(not sil, 'sin silencios' if not sil else 'silencio en ' + ', '.join(f'{mmss(a)}–{mmss(b)}' for a, b in sil))
    # imagen: negros y congelados
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-i', v, '-an', '-vf', 'scale=270:-2,blackdetect=d=0.2:pix_th=0.10,freezedetect=n=0.002:d=6',
             '-f', 'null', '-']).stderr
    blk = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', r)
    add(not blk, 'sin fotogramas negros' if not blk else 'negro en ' + ', '.join(f'{mmss(float(a))}–{mmss(float(b))}' for a, b in blk))
    fz = [(float(a), float(b)) for a, b in zip(re.findall(r'freeze_start: ([\d.]+)', r), re.findall(r'freeze_end: ([\d.]+)', r))]
    add(not fz, 'sin imagen congelada > 6 s' if not fz else 'imagen quieta en ' + ', '.join(f'{mmss(a)}–{mmss(b)}' for a, b in fz) + ' (comprobar)',
        warn=True)
    g = gray_frames(v)
    empty = [i / 2 for i, fr in enumerate(g) if fr.std() < 2.0]
    first = [t for t in empty if t < 1.0]
    empty = [t for t in empty if 1.0 <= t < dur - 0.6]            # el fundido final tampoco cuenta
    add(not empty, 'sin fotogramas vacíos' if not empty else 'fotograma vacío (un solo color) en ' + ', '.join(f'{mmss(a)}–{mmss(b)}' for a, b in ranges(empty, 0.5)))
    if first:
        add(False, 'el primer fotograma está vacío: al publicar hay que subir la portada como miniatura', warn=True)
    return dur, wh, res


def compare(v, prev):
    a, b = gray_frames(v, fps=1, w=192), gray_frames(prev, fps=1, w=192)
    da, db = float(probe(v)['format']['duration']), float(probe(prev)['format']['duration'])
    if a.shape[1:] != b.shape[1:]:
        return [(BAD, 'la versión anterior tiene otro formato: no se puede comparar')]
    n = min(len(a), len(b))
    d = np.abs(a[:n] - b[:n])
    # cambia si una zona apreciable de la imagen es distinta (una etiqueta movida ya cuenta)
    changed = [i for i in range(n) if (d[i] > 24).mean() > 0.0015]
    out = [((OK if abs(da - db) < 0.15 else WARN), f'duración {da:.1f} s (antes {db:.1f} s)')]
    if not changed:
        out.append((WARN, 'ningún cambio visible respecto a la versión anterior'))
    else:
        tot = sum(e - s for s, e in ranges(changed, 1))
        out.append((WARN, f'cambios respecto a la versión anterior ({tot:.0f} s de {n} s): '
                    + ', '.join(f'{mmss(s)}–{mmss(e)}' for s, e in ranges(changed, 1))
                    + '  → deben coincidir con las correcciones pedidas'))
    return out


def sheets(v, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = probe(v); dur = float(p['format']['duration'])
    vs = next(s for s in p['streams'] if s['codec_type'] == 'video')
    sj = os.path.splitext(v)[0] + '.scenes.json'
    shots = []
    if os.path.exists(sj):
        for i, (t0, t1, name) in enumerate(json.load(open(sj))['scenes']):
            L = t1 - t0
            for k in ((0.35, 0.8) if L > 14 else (0.62,)):
                shots.append((min(t0 + L * k, dur - 0.1), f'{i:02d} {name.replace("sc_", "")}'))
    else:
        shots = [(t, '') for t in np.arange(3, dur, 6)]
    wide = vs['width'] > vs['height']
    tw = 560 if wide else 400
    th = int(tw * vs['height'] / vs['width'])
    cols, rows = (3, 4) if wide else (4, 3)
    try:
        font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 17)
    except OSError:
        font = ImageFont.load_default()
    base = os.path.splitext(os.path.basename(v))[0]
    paths = []
    for s0 in range(0, len(shots), cols * rows):
        part = shots[s0:s0 + cols * rows]
        sheet = Image.new('RGB', (cols * tw, -(-len(part) // cols) * (th + 26)), (255, 255, 255))
        dr = ImageDraw.Draw(sheet)
        for j, (t, name) in enumerate(part):
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', v, '-frames:v', '1', '-vf', f'scale={tw}:{th}',
                                  '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
            x, y = (j % cols) * tw, (j // cols) * (th + 26)
            sheet.paste(Image.frombytes('RGB', (tw, th), raw), (x, y + 26))
            dr.rectangle([x, y, x + tw - 1, y + 25], fill=(43, 45, 47))
            dr.text((x + 8, y + 3), f'{mmss(t)}  {name}', fill=(255, 255, 255), font=font)
        path = os.path.join(outdir, f'{base}_hoja{s0 // (cols * rows) + 1}.png')
        sheet.save(path); paths.append(path)
    return paths, len(shots), os.path.exists(sj)


def family(v, refdir, outdir):
    """Hoja de familia: arriba, fotogramas de los vídeos de referencia; abajo, los del vídeo nuevo. Deben parecer hermanos:
    misma cabecera, mismos tamaños de letra, mismas etiquetas, misma franja, misma luz y mismos materiales."""
    os.makedirs(outdir, exist_ok=True)
    p = probe(v); dur = float(p['format']['duration'])
    vs = next(s for s in p['streams'] if s['codec_type'] == 'video')
    wide = vs['width'] > vs['height']
    refs = sorted(f for f in os.listdir(refdir) if f.startswith('169_' if wide else '45_'))[:4]
    if not refs:
        return None
    sj = os.path.splitext(v)[0] + '.scenes.json'
    if os.path.exists(sj):
        sc = json.load(open(sj))['scenes']; n = len(sc)
        ts = [sc[i][0] + (sc[i][1] - sc[i][0]) * 0.62 for i in sorted({1, n // 3, 2 * n // 3, n - 1})]
    else:
        ts = [dur * k for k in (0.06, 0.35, 0.6, 0.985)]
    tw = 640 if wide else 430
    th = int(tw * vs['height'] / vs['width'])
    sheet = Image.new('RGB', (4 * tw, 2 * th + 52), (255, 255, 255))
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 17)
    except OSError:
        font = ImageFont.load_default()
    for y, lab in ((0, 'REFERENCIA (línea gráfica común)'), (th + 26, 'VÍDEO NUEVO')):
        dr.rectangle([0, y, 4 * tw, y + 25], fill=(43, 45, 47)); dr.text((8, y + 3), lab, fill=(255, 255, 255), font=font)
    for i, f in enumerate(refs):
        sheet.paste(Image.open(os.path.join(refdir, f)).convert('RGB').resize((tw, th)), (i * tw, 26))
    for i, t in enumerate(ts[:4]):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{min(t, dur - 0.1):.2f}', '-i', v, '-frames:v', '1', '-vf', f'scale={tw}:{th}',
                              '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        sheet.paste(Image.frombytes('RGB', (tw, th), raw), (i * tw, th + 52))
    path = os.path.join(outdir, os.path.splitext(os.path.basename(v))[0] + '_familia.png')
    sheet.save(path)
    return path


if __name__ == '__main__':
    args = sys.argv[1:]
    prev = hoja = fam = None
    if '--familia' in args:
        i = args.index('--familia'); fam = args[i + 1]; del args[i:i + 2]
    if '--prev' in args:
        i = args.index('--prev'); prev = args[i + 1]; del args[i:i + 2]
    if '--hoja' in args:
        i = args.index('--hoja'); hoja = args[i + 1]; del args[i:i + 2]
    if not args:
        print(__doc__); sys.exit(2)
    fail = False
    info = {}
    for v in args:
        dur, wh, res = check(v)
        info[v] = (dur, wh)
        print(f'\n{os.path.basename(v)} · {mmss(dur)} ({dur:.1f} s)')
        if prev and len(args) == 1:
            res += compare(v, prev)
        for sym, txt in res:
            print(f'  {sym} {txt}'); fail |= sym == BAD
        if hoja:
            paths, n, by_scene = sheets(v, hoja)
            print(f'  hojas ({n} fotogramas, ' + ('uno o dos por escena' if by_scene else 'uno cada 6 s: falta .scenes.json') + '): ' + ' '.join(paths))
        if fam:
            fp = family(v, fam, hoja or os.path.dirname(os.path.abspath(v)))
            print('  hoja de familia: ' + (fp or 'no hay fotogramas de referencia para este formato'))
    # coherencia entre versiones
    if len(args) > 1:
        print('\nCoherencia entre versiones')
        lang = lambda v: (re.search(r'_(ES|EN)_', os.path.basename(v)) or [None, '?'])[1]
        for lg in sorted({lang(v) for v in args}):
            ds = [info[v][0] for v in args if lang(v) == lg]
            same = max(ds) - min(ds) < 0.15
            print(f"  {OK if same else BAD} {lg}: {len(ds)} formatos, duración " + ('igual' if same else 'DISTINTA: ' + ', '.join(f'{d:.1f}' for d in ds)))
            fail |= not same
        fm = {}
        for v in args:
            fm.setdefault(info[v][1], set()).add(lang(v))
        for wh, lgs in fm.items():
            ok = lgs >= {'ES', 'EN'}
            print(f"  {OK if ok else WARN} {wh[0]}x{wh[1]}: idiomas {', '.join(sorted(lgs))}")
    sys.exit(1 if fail else 0)
