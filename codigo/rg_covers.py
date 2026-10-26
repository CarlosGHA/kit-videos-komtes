"""Portadas RG W-FOG · centros de datos (16:9 y 4:5, ES/EN)."""
import sys, math
sys.argv = ['cpd_final.py', 'es']
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cpd_final as F
B, V = F.B, F.V
OUT = B.SP + 'covers/'
import os
os.makedirs(OUT, exist_ok=True)
FD = '/usr/share/fonts/opentype/inter/'
INK, INK2, RED = B.INK, B.INK2, B.RED

TXT = {
    'es': dict(kicker='RG W-FOG · AGUA NEBULIZADA', head=['Protección contra', 'incendios para', 'centros de datos'],
               sub='Del inicio del fuego a la extinción, paso a paso', b1='Certificación', b2='FM'),
    'en': dict(kicker='RG W-FOG · WATER MIST', head=['Fire protection', 'for data centers'],
               sub='From ignition to extinction, step by step', b1='Certified by', b2='FM'),
}


def font(n, px):
    return ImageFont.truetype(FD + n, int(px))


def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


# ---------------- capas gráficas ----------------
hall = B.SHOTS['wide'][1] if B.SHOTS['wide'][1] is not None else B.SHOTS['wide'][0]
hall = Image.blend(B.SHOTS['wide'][0], hall, 0.6)
hj = B.SHOTS['wide'][2]
hb = hall.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
HALL = hall.crop(hb)
NOZ_PTS = [(p[0] - hb[0], p[1] - hb[1]) for p in hj['nozzles']]
_o = lambda p: (p[0] - hb[0], p[1] - hb[1])
ROUTE = ([[_o(p) for p in hj['gp_feed']] + [_o(hj['gp_main'][1])]] + [[_o(hj['gp_br'][k]), _o(hj['gp_br'][k + 3])] for k in range(3)]) if 'gp_feed' in hj else []


def draw_route(canvas, P, wpx):
    glow = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    d = ImageDraw.Draw(canvas)
    for path in ROUTE:
        gd.line([P(q) for q in path], fill=(230, 30, 40, 150), width=int(wpx * 4), joint='curve')
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(wpx * 2)))
    for path in ROUTE:
        d.line([P(q) for q in path], fill=RED + (255,), width=int(wpx), joint='curve')
    for q in NOZ_PTS:
        x, y = P(q)
        d.ellipse([x - wpx * 1.4, y - wpx * 1.4, x + wpx * 1.4, y + wpx * 1.4], fill=RED + (255,))

# boquilla descargando: fotograma de la escena de activación sin rótulos
B.UI[0] = False; B.NOFADE[0] = True
noz = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (255, 255, 255, 255))
V.sc_activation(5.4, 7.2, noz)
B.UI[0] = True; B.NOFADE[0] = False
bulb = B.View(1.0 + 0.05 * B.ss(0, 7.2, 5.4))(B.SHOTS['ceil_a'][2]['bulb'])
cx, cy = bulb[0] * B.SS, (bulb[1] + 10) * B.SS
R0 = 320 * B.SS
NOZ = noz.crop((int(cx - R0), int(cy - R0), int(cx + R0), int(cy + R0)))

FM_LOGO = V.FM_LOGO


def circle_inset(im, d):
    im = im.resize((d, d), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (d * 2, d * 2), 0)
    ImageDraw.Draw(m).ellipse([0, 0, d * 2 - 1, d * 2 - 1], fill=255)
    m = m.resize((d, d), Image.LANCZOS)
    im.putalpha(m)
    return im


def shadow(canvas, box, r, blur, alpha=70, ellipse=False):
    lay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box
    if ellipse:
        d.ellipse([x0, y0 + blur * 0.6, x1, y1 + blur * 0.8], fill=(20, 22, 26, alpha))
    else:
        d.rounded_rectangle([x0, y0 + blur * 0.5, x1, y1 + blur * 0.7], radius=r, fill=(20, 22, 26, alpha))
    canvas.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def lockup(h):
    L = B.lockup(22)
    k = h / L.height
    return L.resize((int(L.width * k), int(L.height * k)), Image.LANCZOS)


def band(canvas, y0, th, k=0.5, x_from=0):
    d = ImageDraw.Draw(canvas)
    W_, H_ = canvas.size
    d.polygon([(x_from, y0), (W_, y0 + (W_ - x_from) * k), (W_, y0 + (W_ - x_from) * k + th), (x_from, y0 + th)], fill=RED)


def badge(canvas, x, y, t, s=1.0):
    w, h = int(330 * s), int(118 * s)
    shadow(canvas, (x, y, x + w, y + h), int(16 * s), int(14 * s), 60)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(16 * s), fill=(255, 255, 255, 255), outline=(225, 227, 230, 255), width=2)
    lg = FM_LOGO
    lh = int(78 * s); lw = int(lg.width * lh / lg.height)
    if lw > 120 * s:
        lw = int(120 * s); lh = int(lg.height * lw / lg.width)
    canvas.alpha_composite(lg.resize((lw, lh), Image.LANCZOS), (int(x + 20 * s + (120 * s - lw) / 2), int(y + (h - lh) / 2)))
    d.text((x + 160 * s, y + 24 * s), t['b1'], font=font('InterDisplay-Medium.otf', 24 * s), fill=INK2)
    d.text((x + 160 * s, y + 50 * s), t['b2'], font=font('InterDisplay-Bold.otf', 52 * s), fill=RED)


def place_hall(canvas, x, y, w):
    k = w / HALL.width
    im = HALL.resize((int(HALL.width * k), int(HALL.height * k)), Image.LANCZOS)
    canvas.alpha_composite(im, (int(x), int(y)))
    return lambda p: (x + p[0] * k, y + p[1] * k)


def inset(canvas, cx_, cy_, d, target=None):
    if target:
        dr = ImageDraw.Draw(canvas)
        dr.line([target, (cx_, cy_)], fill=INK + (200,), width=3)
        dr.ellipse([target[0] - 8, target[1] - 8, target[0] + 8, target[1] + 8], fill=RED)
    shadow(canvas, (cx_ - d / 2, cy_ - d / 2, cx_ + d / 2, cy_ + d / 2), 0, 22, 80, ellipse=True)
    dr = ImageDraw.Draw(canvas)
    rb = d / 2 + 10
    dr.ellipse([cx_ - rb, cy_ - rb, cx_ + rb, cy_ + rb], fill=(255, 255, 255, 255))
    canvas.alpha_composite(circle_inset(NOZ, int(d)), (int(cx_ - d / 2), int(cy_ - d / 2)))
    dr.ellipse([cx_ - rb, cy_ - rb, cx_ + rb, cy_ + rb], outline=RED + (255,), width=4)


def cover_45(lang):
    t = TXT[lang]
    W_, H_ = 1080 * 2, 1350 * 2
    c = Image.new('RGBA', (W_, H_), (255, 255, 255, 255))
    band(c, 1760, 330)
    P = place_hall(c, 60, 1180, 2040)
    draw_route(c, P, 5)
    L = lockup(66); c.alpha_composite(L, (140, 130))
    d = ImageDraw.Draw(c)
    d.text((140, 320), t['kicker'], font=font('Inter-Bold.otf', 40), fill=RED)
    fh = font('InterDisplay-Bold.otf', 146)
    y = 392
    for ln in t['head']:
        d.text((132, y), ln, font=fh, fill=INK); y += 168
    d.text((140, y + 26), t['sub'], font=font('InterDisplay-Medium.otf', 56), fill=INK2)
    d.rounded_rectangle([140, y + 120, 268, y + 134], radius=7, fill=RED)
    tgt = P(NOZ_PTS[7]) if len(NOZ_PTS) > 7 else None
    inset(c, 1660, 1130, 640, tgt)
    badge(c, 140, 2380, t, 2.0)
    out = c.convert('RGB').resize((1080, 1350), Image.LANCZOS)
    fn = OUT + f'Portada_RG-WFOG_DataCenter_{lang.upper()}_1080x1350.png'
    out.save(fn); return fn


def cover_169(lang):
    t = TXT[lang]
    W_, H_ = 1920 * 2, 1080 * 2
    c = Image.new('RGBA', (W_, H_), (255, 255, 255, 255))
    band(c, 1240, 300, 0.5, 1500)
    P = place_hall(c, 1620, 360, 2140)
    draw_route(c, P, 5)
    L = lockup(62); c.alpha_composite(L, (180, 150))
    d = ImageDraw.Draw(c)
    d.text((180, 470), t['kicker'], font=font('Inter-Bold.otf', 40), fill=RED)
    fh = font('InterDisplay-Bold.otf', 140)
    y = 545
    for ln in t['head']:
        d.text((172, y), ln, font=fh, fill=INK); y += 160
    d.text((180, y + 24), t['sub'], font=font('InterDisplay-Medium.otf', 54), fill=INK2)
    d.rounded_rectangle([180, y + 116, 308, y + 130], radius=7, fill=RED)
    tgt = P(NOZ_PTS[7]) if len(NOZ_PTS) > 7 else None
    inset(c, 3330, 520, 600, tgt)
    badge(c, 180, 1780, t, 1.9)
    out = c.convert('RGB').resize((1920, 1080), Image.LANCZOS)
    fn = OUT + f'Portada_RG-WFOG_DataCenter_{lang.upper()}_1920x1080.png'
    out.save(fn); return fn


if __name__ == '__main__':
    for lg in ('es', 'en'):
        print(cover_45(lg)); print(cover_169(lg))
