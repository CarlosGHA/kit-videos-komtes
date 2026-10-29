"""Pega la etiqueta SIEX envolvente sobre los cilindros de la foto del sistema (sys_iso.png)."""
import math
import numpy as np
from PIL import Image
import os as _os
KW = _os.environ.get('KOMTES_WORK', _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'trabajo'))) + '/'
SP = KW + ''
src = Image.open(SP + 'assets/siex2/sys_iso.png').convert('RGBA')
im = np.array(src).astype(np.float32)
lab = np.array(Image.open(SP + 'assets/siex/label_siex.png').convert('RGBA')).astype(np.float32)
LH, LW = lab.shape[:2]
R, G, B, A = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
red = (R > 70) & (G < 80) & (B < 80) & (A > 200) & (R > G * 1.6)
# cilindros: centro x, semiancho, y frontal del borde inferior de la abrazadera superior
CYLS = [(160, 79, 1009), (326, 79, 979), (494, 79, 948), (662, 79, 917), (829, 79, 887), (995, 79, 856)]
ARC = math.radians(150)
BR = 0.577  # b/a de la elipse en isométrica
for cx, a, yb in CYLS:
    b = BR * a
    s = (a * ARC) / LW  # px de foto por px de textura
    ytop = yb + 10  # fila 300 de la textura (inicio de la etiqueta principal)
    x0, x1 = int(cx - a), int(cx + a) + 1
    y0, y1 = int(ytop - 300 * s - b - 4), int(ytop + (LH - 300) * s + 4)
    xs = np.arange(x0, x1); ys = np.arange(y0, y1)
    X, Y = np.meshgrid(xs, ys)
    sn = np.clip((X - cx) / a, -0.999, 0.999)
    th = np.arcsin(sn)
    u = (th + ARC / 2) / ARC
    h = Y - ytop + b * (1 - np.cos(th))
    tr = 300 + h / s
    tc = u * (LW - 1)
    ok = (u >= 0) & (u <= 1) & (tr >= 0) & (tr < LH - 1) & red[y0:y1, x0:x1]
    # muestreo bilineal
    tci = np.clip(tc, 0, LW - 2); tri = np.clip(tr, 0, LH - 2)
    c0 = np.floor(tci).astype(int); r0 = np.floor(tri).astype(int); fc = tci - c0; fr = tri - r0
    samp = (lab[r0, c0] * ((1 - fc) * (1 - fr))[..., None] + lab[r0, c0 + 1] * (fc * (1 - fr))[..., None]
            + lab[r0 + 1, c0] * ((1 - fc) * fr)[..., None] + lab[r0 + 1, c0 + 1] * (fc * fr)[..., None])
    la = samp[..., 3] / 255 * ok
    # sombreado del cilindro a partir del rojo de la foto (difuso) + brillo especular
    reg = im[y0:y1, x0:x1]
    shade = np.clip(reg[..., 0] / 205.0, 0.35, 1.15)
    spec = np.clip((np.minimum(reg[..., 1], reg[..., 2]) - 40) / 160.0, 0, 0.5)
    col = samp[..., :3] * shade[..., None] * (1 - spec[..., None]) + 255 * spec[..., None]
    reg[..., :3] = reg[..., :3] * (1 - la[..., None]) + col * la[..., None]
    im[y0:y1, x0:x1] = reg
out = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8))
out.save(SP + 'assets/siex2/sys_iso_lab.png')
bg = Image.new('RGBA', out.size, (255, 255, 255, 255)); bg.alpha_composite(out)
bg.convert('RGB').crop((0, 450, 1200, 1700)).resize((720, 750)).save(SP + 'chk/sys_lab.jpg')
