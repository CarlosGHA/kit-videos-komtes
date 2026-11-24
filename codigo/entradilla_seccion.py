"""ENTRADILLA de la sección de redes «Risk by Risk» / «Riesgo a riesgo» — COMÚN a todos los vídeos de redes del proyecto
(cualquier división, sistema y aplicación). Es solo la sección: sin logotipos, sin sector, sin aplicación y sin número de
episodio (todo eso va después, en el título-pregunta de cada pieza).

Animación (3,2 s, 1080x1350 lógicos):
  · fondo grafito de marca (#2B2D2F, nunca negro puro)
  · «RISK BY RISK» en Bio Sans Bold, cada palabra sube desde detrás de una línea; «BY» en rojo de marca
  · el lema en inglés (Bio Sans Regular) y debajo su subtítulo en español (Bio Sans Light), como la plantilla corporativa
  · cinco cubos isométricos: el rojo recorre los riesgos uno a uno y cada riesgo recorrido queda marcado («one risk at a time»)
  · salida: una cortina blanca con filo rojo sube y deja la pantalla en blanco para el título-pregunta

Tipografía: copia la familia Bio Sans (OTF) en  <kit>/fuentes/  (no se versiona: licencia). Si falta, usa Inter y avisa.
Uso directo (clip suelto, para editar en otro programa):
  python3 entradilla_seccion.py <salida.mp4> [45|169]
Uso desde un montaje:  import entradilla_seccion as E;  E.draw(img_rgba, t, S, W, H)"""
import os, sys, math, glob, subprocess
from PIL import Image, ImageDraw, ImageFont

DUR = 3.2
NOMBRE = ['RISK', 'BY', 'RISK']                 # la palabra central va en rojo
LEMA_EN = 'Fire protection, one risk at a time'
LEMA_ES = 'Protección contra incendios, un riesgo cada vez'
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


def draw(img, t, S, W, H, ss_=None):
    """dibuja la entradilla en el instante t (s) sobre img (RGBA, tamaño S(W) x S(H))"""
    ssf = S(1.0)
    key = round(ssf, 3)
    if key not in _FC:
        _FC[key] = dict(big=_font('Bold', 150, ssf), lema=_font('Regular', 36, ssf), es=_font('Light', 30, ssf))
    fb, fl, fe = _FC[key]['big'], _FC[key]['lema'], _FC[key]['es']
    base = Image.new('RGBA', img.size, GRAPH + (255,))
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))   # todo se dibuja en una capa aparte (los fundidos no agujerean el fondo)
    d = ImageDraw.Draw(layer)
    cy = H / 2 - 130                                       # línea base visual del nombre

    # nombre: cada palabra sube desde detrás de la línea (máscara) con un pequeño escalonado
    sp = fb.getlength(' ') * 0.9
    ws = [fb.getlength(w) for w in NOMBRE]
    x = S(W / 2) - (sum(ws) + sp * (len(NOMBRE) - 1)) / 2
    asc, desc = fb.getmetrics()
    top, bot = S(cy) - asc, S(cy) + desc * 0.25          # ventana visible de las letras
    for i, w in enumerate(NOMBRE):
        p = _ease_out(0.15 + 0.14 * i, 0.75 + 0.14 * i, t)
        dy = (1 - p) * (asc + desc)
        strip = Image.new('RGBA', (int(ws[i]) + 4, int(bot - top) + 2), (0, 0, 0, 0))
        ImageDraw.Draw(strip).text((0, asc + dy), w, font=fb, fill=(RED if i == 1 else OFF) + (255,), anchor='ls')
        layer.alpha_composite(strip, (int(x), int(top)))
        x += ws[i] + sp

    # filo rojo bajo el nombre: crece desde el centro
    bw = 150 * _ease_out(0.7, 1.3, t)
    d.rectangle([S(W / 2 - bw / 2), S(cy + 38), S(W / 2 + bw / 2), S(cy + 45)], fill=RED + (255,))

    # lema en inglés (Regular) + español (Light)
    a = _ss(0.95, 1.45, t)
    d.text((S(W / 2), S(cy + 120)), LEMA_EN, font=fl, fill=_c(OFF, a * 0.92), anchor='ms')
    a2 = _ss(1.15, 1.65, t)
    _b = sys.modules.get('cpd_video')               # dentro de un montaje en inglés: el español no se traduce
    if _b is not None:
        _b.RAW[0] = True
    try:
        d.text((S(W / 2), S(cy + 166)), LEMA_ES, font=fe, fill=_c(GREY, a2), anchor='ms')
    finally:
        if _b is not None:
            _b.RAW[0] = False

    # cubos isométricos: el riesgo activo en rojo recorre la fila; los recorridos quedan con el filo rojo
    n, s_, gap = 5, 44, 136
    yc = cy + 270
    x0 = W / 2 - gap * (n - 1) / 2
    cw, ch = s_ * math.cos(math.radians(30)), s_ * math.sin(math.radians(30))
    t0, step = 1.25, 0.26
    for k in range(n):
        ap = _ss(0.9 + 0.06 * k, 1.3 + 0.06 * k, t)
        if ap <= 0.01:
            continue
        cx = x0 + k * gap
        act = _ss(t0 + k * step - 0.08, t0 + k * step + 0.06, t) * (1 - _ss(t0 + (k + 1) * step - 0.04, t0 + (k + 1) * step + 0.12, t))
        done = _ss(t0 + (k + 1) * step - 0.04, t0 + (k + 1) * step + 0.12, t)
        lift = -14 * act
        T = [(cx, yc - ch + lift), (cx + cw, yc + lift), (cx, yc + ch + lift), (cx - cw, yc + lift)]
        Lf = [T[3], T[2], (T[2][0], T[2][1] + s_), (T[3][0], T[3][1] + s_)]
        Rf = [T[2], T[1], (T[1][0], T[1][1] + s_), (T[2][0], T[2][1] + s_)]
        mix = lambda c1, c2, m: tuple(int(c1[j] + (c2[j] - c1[j]) * m) for j in range(3))
        top_c = mix((78, 81, 85), RED, act); l_c = mix((62, 65, 69), (176, 4, 18), act); r_c = mix((54, 56, 60), (140, 3, 14), act)
        P = lambda pts: [(S(px), S(py)) for px, py in pts]
        d.polygon(P(Lf), fill=_c(l_c, ap)); d.polygon(P(Rf), fill=_c(r_c, ap)); d.polygon(P(T), fill=_c(top_c, ap))
        if done > 0.01:                                   # riesgo resuelto: filo rojo en la cara superior
            d.line(P(T + [T[0]]), fill=_c(RED, ap * done), width=max(1, int(S(2.2))), joint='curve')

    # salida: cortina blanca con filo rojo que sube
    w_ = _ss(DUR - 0.85, DUR - 0.42, t)               # termina antes del fundido con la pieza siguiente
    if w_ > 0:
        yb = H * (1 - w_)
        d.rectangle([0, S(yb), S(W), S(H)], fill=OFF + (255,))
        if w_ < 0.999:
            d.rectangle([0, S(yb - 7), S(W), S(yb)], fill=RED + (255,))
    base.alpha_composite(layer)
    img.alpha_composite(base)


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
    wh = os.path.join(sfx, 'whoosh.mp3'); ck = os.path.join(sfx, 'click.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out + '.v.mp4', '-i', wh, '-i', ck, '-i', wh, '-filter_complex',
                    '[1:a]volume=0.5,adelay=100|100[a];[2:a]volume=0.6,adelay=1300|1300[b];[3:a]volume=0.45,adelay=2800|2800[c];'
                    f'[a][b][c]amix=inputs=3:normalize=0,apad,atrim=0:{DUR}[o]', '-map', '0:v', '-map', '[o]', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out], check=True)
    os.remove(out + '.v.mp4'); print('done', out)
