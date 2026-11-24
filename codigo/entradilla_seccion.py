"""ENTRADILLA de la sección de redes «Risk by Risk» / «Riesgo a riesgo» — COMÚN a todos los vídeos de redes del proyecto
(cualquier división, sistema y aplicación). Es solo la sección: sin logotipos, sin sector, sin aplicación y sin número de
episodio (todo eso va después, en el título-pregunta de cada pieza).

Animación (10 s, 1080x1350 lógicos), solo fundidos y desplazamientos suaves:
  · fondo grafito de marca (#2B2D2F, nunca negro puro) que entra desde el blanco
  · «RISK BY RISK» en Bio Sans Bold: aparece con un fundido, sube unos píxeles y se cierra el espaciado; «BY» en rojo
  · filo rojo que crece desde el centro y el lema en inglés (Bio Sans Regular)
  · salida: el texto sube y se desvanece y el grafito se funde a blanco para el título-pregunta
  · sonido: solo la música de fondo (sin efectos)

Tipografía: copia la familia Bio Sans (OTF) en  <kit>/fuentes/  (no se versiona: licencia). Si falta, usa Inter y avisa.
Uso directo (clip suelto, para editar en otro programa):
  python3 entradilla_seccion.py <salida.mp4> [45|169]
Uso desde un montaje:  import entradilla_seccion as E;  E.draw(img_rgba, t, S, W, H)"""
import os, sys, math, glob, subprocess
from PIL import Image, ImageDraw, ImageFont

DUR = 10.0
MUSICA = 'music_loop2.wav'                    # la música de fondo de los vídeos: suena continua de la entradilla al episodio
MUS_LUFS = -22.5                              # nivel de la música en la entradilla (igual que dentro de los episodios)
SERIE = 'A SERIES BY'                         # vínculo con el grupo, sobre el logotipo de Grupo Komtes
NOMBRE = ['RISK', 'BY', 'RISK']                 # la palabra central va en rojo
LEMA_EN = 'Fire protection, one risk at a time'
GRAPH = (43, 45, 47); OFF = (249, 249, 249); RED = (228, 3, 19); GREY = (167, 171, 176); GREY2 = (128, 132, 137)

KIT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
FUENTES = os.path.join(KIT, 'fuentes')
INTER = '/usr/share/fonts/opentype/inter/'
_WARNED = [False]


def _font(weight, px, ss):
    """Bio Sans del peso pedido; si no está, Inter equivalente"""
    pats = {'Bold': ['*BioSans*Bold.otf', '*Bio*Sans*Bold*.otf'], 'Regular': ['*BioSans*Regular.otf', '*Bio*Sans*Regular*.otf'],
            'Light': ['*BioSans*Light.otf', '*Bio*Sans*Light*.otf']}[weight]
    for p in pats:
        hits = [h for h in glob.glob(os.path.join(FUENTES, p)) if 'Italic' not in h and 'Extra' not in h and 'Semi' not in h]
        if hits:
            return ImageFont.truetype(sorted(hits)[0], int(px * ss))
    if not _WARNED[0]:
        print('⚠ Bio Sans no encontrada en', FUENTES, '→ uso Inter provisionalmente', flush=True); _WARNED[0] = True
    alt = {'Bold': 'InterDisplay-Bold.otf', 'Regular': 'Inter-Regular.otf', 'Light': 'Inter-Light.otf'}[weight]
    if not os.path.exists(INTER + alt):
        alt = 'Inter-Regular.otf'
    return ImageFont.truetype(INTER + alt, int(px * ss))


def _ss(a, b, t):
    x = min(1.0, max(0.0, (t - a) / (b - a)))
    return x * x * (3 - 2 * x)


def _ease_out(a, b, t):
    x = min(1.0, max(0.0, (t - a) / (b - a)))
    return 1 - (1 - x) ** 3


def _c(col, a):
    return col + (int(255 * max(0.0, min(1.0, a))),)


_FC = {}


_LOGO = {}


def _logo(px_w):
    """logotipo de Grupo Komtes para fondo oscuro: el gris pasa a blanco y el rojo se mantiene"""
    k = int(px_w)
    if k not in _LOGO:
        im = Image.open(os.path.join(KIT, 'marcas', 'logo_GroupKomtes.png')).convert('RGBA')
        im = im.resize((k, int(im.height * k / im.width)), Image.LANCZOS)
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g_, b, a = px[x, y]
                if a and not (r > 150 and r - g_ > 90):
                    px[x, y] = OFF + (a,)
        _LOGO[k] = im
    return _LOGO[k]


def draw(img, t, S, W, H, ss_=None):
    """dibuja la entradilla en el instante t (s) sobre img (RGBA, tamaño S(W) x S(H))"""
    ssf = S(1.0)
    key = round(ssf, 3)
    if key not in _FC:
        _FC[key] = dict(big=_font('Bold', 150, ssf), lema=_font('Regular', 38, ssf), serie=_font('Regular', 22, ssf))
    fb, fl, fs = _FC[key]['big'], _FC[key]['lema'], _FC[key]['serie']
    # entrada (blanco -> grafito) y salida (grafito -> blanco), largas y suaves
    g = _ss(0.0, 1.1, t) * (1 - _ss(DUR - 1.1, DUR - 0.05, t))
    bg = tuple(int(OFF[j] + (GRAPH[j] - OFF[j]) * g) for j in range(3))
    base = Image.new('RGBA', img.size, bg + (255,))
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))   # todo se dibuja en una capa aparte (los fundidos no agujerean el fondo)
    d = ImageDraw.Draw(layer)
    o_ = _ss(DUR - 2.1, DUR - 1.1, t)                     # el texto sale antes de que vuelva el blanco
    out = 1 - o_
    up = -18 * o_
    drift = -10 * _ss(0.0, DUR, t)                       # deriva muy lenta: la pantalla no queda congelada
    up += drift
    cy = H / 2 - 70 + up                                 # línea base visual del nombre

    # nombre: fundido + subida suave + espaciado que se cierra
    a = _ss(0.7, 2.3, t) * out
    p = _ease_out(0.7, 3.0, t)
    dy = (1 - p) * 30
    sp = fb.getlength(' ') * (0.9 + 0.7 * (1 - p))
    ws = [fb.getlength(w) for w in NOMBRE]
    x = S(W / 2) - (sum(ws) + sp * (len(NOMBRE) - 1)) / 2
    for i, w in enumerate(NOMBRE):
        d.text((x, S(cy + dy)), w, font=fb, fill=_c(RED if i == 1 else OFF, a), anchor='ls')
        x += ws[i] + sp

    # filo rojo bajo el nombre: crece desde el centro
    bw = 150 * _ease_out(2.1, 3.3, t)
    if bw > 0.5:
        d.rectangle([S(W / 2 - bw / 2), S(cy + 38), S(W / 2 + bw / 2), S(cy + 45)], fill=_c(RED, out))

    # lema en inglés
    a2 = _ss(2.7, 3.8, t) * out
    d.text((S(W / 2), S(cy + 122 + (1 - _ease_out(2.7, 4.0, t)) * 14)), LEMA_EN, font=fl, fill=_c(OFF, a2 * 0.9), anchor='ms')

    # vínculo con Grupo Komtes: «A SERIES BY» + logotipo, abajo
    a3 = _ss(3.9, 5.0, t) * out
    if a3 > 0.01:
        yl = H - 300 + up + (1 - _ease_out(3.9, 5.2, t)) * 12
        sp_ = S(4)                                         # versalitas espaciadas
        tw = sum(fs.getlength(c) for c in SERIE) + sp_ * (len(SERIE) - 1)
        xx = S(W / 2) - tw / 2
        for c in SERIE:
            d.text((xx, S(yl)), c, font=fs, fill=_c(GREY, a3), anchor='ls'); xx += fs.getlength(c) + sp_
        lg = _logo(S(300))
        la = lg.copy(); la.putalpha(la.getchannel('A').point(lambda v: int(v * a3)))
        layer.alpha_composite(la, (int(S(W / 2) - lg.width / 2), int(S(yl + 26))))
    base.alpha_composite(layer)
    img.alpha_composite(base)


def music_gain(path, dur=None):
    """ganancia (dB) para dejar el tramo de música de la entradilla en MUS_LUFS"""
    import re as _re
    dur = dur or DUR
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-t', f'{dur}', '-af', 'ebur128', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    m = _re.findall(r'I:\s+(-?[\d.]+) LUFS', r)
    return MUS_LUFS - float(m[-1]) if m else -12.0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    out = sys.argv[1]; asp = sys.argv[2] if len(sys.argv) > 2 else '45'
    W, H = (1080, 1350) if asp == '45' else (1920, 1080)
    SSF, FPS = 2, 30
    S = lambda v: v * SSF
    if os.environ.get('STILL'):
        for ts in os.environ['STILL'].split(','):
            im = Image.new('RGBA', (W * SSF, H * SSF)); draw(im, float(ts), S, W, H)
            im.convert('RGB').resize((W, H), Image.LANCZOS).save(f'{out}_{ts}.png')
        sys.exit()
    sfx = os.path.join(KIT, 'trabajo', 'sfx')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                           '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', out + '.v.mp4'],
                          stdin=subprocess.PIPE)
    for fi in range(int(DUR * FPS)):
        im = Image.new('RGBA', (W * SSF, H * SSF)); draw(im, fi / FPS, S, W, H)
        ff.stdin.write(im.convert('RGB').resize((W, H), Image.LANCZOS).tobytes())
    ff.stdin.close(); ff.wait()
    mus = os.path.join(sfx, os.environ.get('MUSICA', MUSICA))
    gdb = music_gain(mus)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out + '.v.mp4', '-i', mus, '-filter_complex',
                    f'[1:a]atrim=0:{DUR},asetpts=PTS-STARTPTS,aresample=48000,lowpass=f=12000,volume={gdb:.2f}dB,'
                    f'afade=t=in:d=0.3,afade=t=out:st={DUR - 1.6}:d=1.6[o]',
                    '-map', '0:v', '-map', '[o]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    '-movflags', '+faststart', out], check=True)
    os.remove(out + '.v.mp4'); print('done', out)
