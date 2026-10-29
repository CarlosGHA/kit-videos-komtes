"""Portadas RG W-FOG · centros de datos (16:9 y 4:5, ES/EN)."""
import sys, math
sys.argv = ['cpd_final.py', 'es']
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cpd_final as F
B, V = F.B, F.V
OUT = B.SP + 'covers_v3/'
import os
os.makedirs(OUT, exist_ok=True)
FD = '/usr/share/fonts/opentype/inter/'
INK, INK2, RED = B.INK, B.INK2, B.RED

TXT = {
    'es': dict(kicker='RG W-FOG · AGUA NEBULIZADA', head=['Protección contra', 'incendios para', 'centros de datos'],
               sub='Del inicio del fuego a la extinción, paso a paso', b1='Sistema aprobado', b2='FM APPROVED',
               noz=[('MM-P51', 'Ambiente'), ('MM-P52 / MM-P53', 'Falso suelo'), ('EMM-416549', 'Sala de máquinas')],
               extra=[('WF-PAV', 'Válvula de preacción'), ('W-FOG UAP', 'Grupo de bombeo'), ('RG W-FOG UAC', 'Batería agua + N₂')]),
    'en': dict(kicker='RG W-FOG · WATER MIST', head=['Fire protection', 'for data centers'],
               sub='From ignition to extinction, step by step', b1='Approved system', b2='FM APPROVED',
               noz=[('MM-P51', 'Room'), ('MM-P52 / MM-P53', 'Raised floor'), ('EMM-416549', 'Machinery spaces')],
               extra=[('WF-PAV', 'Pre-action valve'), ('W-FOG UAP', 'Pump unit'), ('RG W-FOG UAC', 'Water + N₂ bank')]),
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
# planta con el suelo técnico abierto en el frente de la sala (red y boquillas bajo baldosas a la vista)
_cov = F._l7('site_cov') if F._has('site_cov') else B.SHOTS['wide']
hall = _cov[0]
hj = _cov[2]
hb = hall.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
HALL = hall.crop(hb)
NOZ_PTS = [(p[0] - hb[0], p[1] - hb[1]) for p in hj['nozzles']]
_o = lambda p: (p[0] - hb[0], p[1] - hb[1])
ROUTE = ([[_o(p) for p in hj['gp_feed']] + [_o(hj['gp_main'][1])]] + [[_o(hj['gp_br'][k]), _o(hj['gp_br'][k + 3])] for k in range(3)]) if 'gp_feed' in hj else []


# red de la batería UAC: alimentación, válvulas y un colector por generador / sala de transformadores
if 'uac_feed' in hj:
    ROUTE = ROUTE + [[_o(p) for p in hj['uac_feed']]] + [[_o(p) for p in c[1:]] for c in hj.get('uac_c', [])]
    NOZ_PTS = NOZ_PTS + [_o(p) for c in hj.get('uac_noz', []) for p in c]


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

def _crop(img, c, r):
    cx_, cy_ = c[0] * B.SS, c[1] * B.SS
    R_ = r * B.SS
    return img.crop((int(cx_ - R_), int(cy_ - R_), int(cx_ + R_), int(cy_ + R_)))


# falso suelo: fotograma del primer plano MM-P52/53 descargando
B.UI[0] = False; B.NOFADE[0] = True
fl = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (255, 255, 255, 255))
_tf, _Lf = F.T2 + 2.6, 8.0
F.sc_floor(_tf, _Lf, fl)
NOZ_UF = _crop(fl, F._v_ufd(_tf, _Lf)(B.SHOTS['ufd_a'][2]['bulb']), 330)
# sala de máquinas: primer plano del difusor abierto EMM descargando
em = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (255, 255, 255, 255))
_te = F.CB0 + 2.2
_lay, _tg, _fo = F._st_noz(_te, F.LU)
em.alpha_composite(_lay)
NOZ_EMM = _crop(em, (_fo['head'][0], _fo['head'][1] + 120), 360)
B.UI[0] = True; B.NOFADE[0] = False
INSETS = [NOZ, NOZ_UF, NOZ_EMM]
# válvula WF-PAV (render de producto) y grupo de bombeo W-FOG UAP (foto), sin rótulo
_pv = Image.open(B.SP + 'assets/rg/wfpav_cut.png').convert('RGBA')        # foto real de la WF-PAV
_wb = Image.new('RGBA', (_pv.width + 800, _pv.height + 800), (255, 255, 255, 255)); _wb.alpha_composite(_pv, (400, 400))
_vb = _pv.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
_cxv, _cyv = (_vb[0] + _vb[2]) / 2 + 400, (_vb[1] + _vb[3]) / 2 + 400 - 40; _rv = max(_vb[2] - _vb[0], _vb[3] - _vb[1]) * 0.50
VALVE = _wb.crop((int(_cxv - _rv), int(_cyv - _rv), int(_cxv + _rv), int(_cyv + _rv)))
_pp = F.PUMP2
_PAD = 400
_wp = Image.new('RGBA', (_pp.width + 2 * _PAD, _pp.height + 2 * _PAD), (255, 255, 255, 255)); _wp.alpha_composite(_pp, (_PAD, _PAD))
_pb = _pp.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
_cxp, _cyp = (_pb[0] + _pb[2]) / 2 + _PAD, (_pb[1] + _pb[3]) / 2 + _PAD; _rp = max(_pb[2] - _pb[0], _pb[3] - _pb[1]) * 0.60
PUMP = _wp.crop((int(_cxp - _rp), int(_cyp - _rp), int(_cxp + _rp), int(_cyp + _rp)))
_ub = Image.open(B.SP + 'assets/rg/uac_bank_cut.png').convert('RGBA')
_wu = Image.new('RGBA', (_ub.width + 800, _ub.height + 800), (255, 255, 255, 255)); _wu.alpha_composite(_ub, (400, 400))
_bb = _ub.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
_cxu, _cyu = (_bb[0] + _bb[2]) / 2 + 400, (_bb[1] + _bb[3]) / 2 + 400; _ru = max(_bb[2] - _bb[0], _bb[3] - _bb[1]) * 0.58
UACB = _wu.crop((int(_cxu - _ru), int(_cyu - _ru), int(_cxu + _ru), int(_cyu + _ru)))
EXTRA = [(VALVE, _o(hj['pav'][1]) if 'pav' in hj else None), (PUMP, _o(hj['motor_c']) if 'motor_c' in hj else None),
         (UACB, _o(hj['uac']) if 'uac' in hj else None)]
TGT = [NOZ_PTS[10] if len(NOZ_PTS) > 10 else None,
       _o(hj['uf_noz'][1]) if 'uf_noz' in hj else None,
       _o(hj['gnoz'][1]) if hj.get('gnoz') else None]

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
    w, h = int(420 * s), int(118 * s)
    shadow(canvas, (x, y, x + w, y + h), int(16 * s), int(14 * s), 60)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(16 * s), fill=(255, 255, 255, 255), outline=(225, 227, 230, 255), width=2)
    lg = FM_LOGO
    lh = int(78 * s); lw = int(lg.width * lh / lg.height)
    if lw > 120 * s:
        lw = int(120 * s); lh = int(lg.height * lw / lg.width)
    canvas.alpha_composite(lg.resize((lw, lh), Image.LANCZOS), (int(x + 20 * s + (120 * s - lw) / 2), int(y + (h - lh) / 2)))
    d.text((x + 160 * s, y + 24 * s), t['b1'], font=font('InterDisplay-Medium.otf', 24 * s), fill=INK2)
    d.text((x + 160 * s, y + 56 * s), t['b2'], font=font('InterDisplay-Bold.otf', 31 * s), fill=RED)


def place_hall(canvas, x, y, w):
    k = w / HALL.width
    im = HALL.resize((int(HALL.width * k), int(HALL.height * k)), Image.LANCZOS)
    canvas.alpha_composite(im, (int(x), int(y)))
    return lambda p: (x + p[0] * k, y + p[1] * k)


def inset(canvas, cx_, cy_, d, target=None, im=None, label=None, s=1.0):
    if target:
        dr = ImageDraw.Draw(canvas)
        vx, vy = target[0] - cx_, target[1] - cy_
        ln = math.hypot(vx, vy) or 1.0
        ux, uy = vx / ln, vy / ln
        x0, y0 = cx_ + ux * (d / 2 + 10 * s), cy_ + uy * (d / 2 + 10 * s)
        if label and uy > 0.35:          # la línea sale por debajo del rótulo, sin tacharlo
            x0, y0 = cx_, cy_ + d / 2 + 10 * s + 132 * s
        ah = 30 * s; aw = 13 * s                      # punta de flecha sobre el componente
        bx_, by_ = target[0] - ux * ah, target[1] - uy * ah
        dr.line([(x0, y0), (bx_, by_)], fill=INK + (230,), width=int(4 * s))
        dr.polygon([target, (bx_ - uy * aw, by_ + ux * aw), (bx_ + uy * aw, by_ - ux * aw)], fill=RED + (255,))
    shadow(canvas, (cx_ - d / 2, cy_ - d / 2, cx_ + d / 2, cy_ + d / 2), 0, 22, 80, ellipse=True)
    dr = ImageDraw.Draw(canvas)
    rb = d / 2 + 10 * s
    dr.ellipse([cx_ - rb, cy_ - rb, cx_ + rb, cy_ + rb], fill=(255, 255, 255, 255))
    canvas.alpha_composite(circle_inset(im if im is not None else NOZ, int(d)), (int(cx_ - d / 2), int(cy_ - d / 2)))
    dr.ellipse([cx_ - rb, cy_ - rb, cx_ + rb, cy_ + rb], outline=RED + (255,), width=int(4 * s))
    if label:
        code, desc = label
        f1 = font('InterDisplay-Bold.otf', 46 * s); f2 = font('InterDisplay-Medium.otf', 36 * s)
        y = cy_ + rb + 22 * s
        dr.rounded_rectangle([cx_ - f1.getlength(code) / 2 - 22 * s, y - 6 * s, cx_ + f1.getlength(code) / 2 + 22 * s, y + 104 * s],
                             radius=int(14 * s), fill=(255, 255, 255, 235))
        dr.text((cx_, y), code, font=f1, fill=RED, anchor='mt')
        dr.text((cx_, y + 56 * s), desc, font=f2, fill=INK2, anchor='mt')


def insets_extra(canvas, P, pos, d, t, s=1.0):
    """válvula de preacción y grupo de bombeo, con su código"""
    for k, ((im, tg), (x, y)) in enumerate(zip(EXTRA, pos)):
        inset(canvas, x, y, d, P(tg) if tg is not None else None, im, t['extra'][k], s)


ROW_ORDER = (1, 0, 2)   # de izquierda a derecha como aparecen en la planta: falso suelo, ambiente, sala de máquinas (sin cruces)


def insets_row(canvas, P, xs, y, d, t, s=1.0):
    for x, k in zip(xs, ROW_ORDER):
        tg = P(TGT[k]) if TGT[k] is not None else None
        inset(canvas, x, y, d, tg, INSETS[k], t['noz'][k], s)


def cover_45(lang):
    t = TXT[lang]
    W_, H_ = 1080 * 2, 1350 * 2
    c = Image.new('RGBA', (W_, H_), (255, 255, 255, 255))
    band(c, 1560, 300)
    P = place_hall(c, 200, 1000, 1760)
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
    badge(c, 1270, 130, t, 1.75)
    insets_extra(c, P, ((1440, 700), (1705, 700), (1970, 700)), 240, t, 0.68)
    insets_row(c, P, (400, 1080, 1760), 2230, 420, t, 1.0)
    out = c.convert('RGB').resize((1080, 1350), Image.LANCZOS)
    fn = OUT + f'Portada_RG-WFOG_DataCenter_{lang.upper()}_1080x1350.png'
    out.save(fn); return fn


def cover_169(lang):
    """misma composición que el 4:5: titular arriba a la izquierda con aire debajo, componentes arriba a la derecha,
    planta en el centro y fila de boquillas abajo"""
    t = TXT[lang]
    W_, H_ = 1920 * 2, 1080 * 2
    c = Image.new('RGBA', (W_, H_), (255, 255, 255, 255))
    band(c, 1380, 260, 0.5, 0)
    P = place_hall(c, 1500, 560, 2200)
    draw_route(c, P, 5)
    L = lockup(62); c.alpha_composite(L, (180, 150))
    d = ImageDraw.Draw(c)
    d.text((180, 330), t['kicker'], font=font('Inter-Bold.otf', 40), fill=RED)
    fh = font('InterDisplay-Bold.otf', 128)
    y = 400
    for ln in t['head']:
        d.text((172, y), ln, font=fh, fill=INK); y += 146
    d.text((180, y + 20), t['sub'], font=font('InterDisplay-Medium.otf', 50), fill=INK2)
    d.rounded_rectangle([180, y + 106, 308, y + 120], radius=7, fill=RED)
    badge(c, 180, 1830, t, 1.75)
    insets_extra(c, P, ((2620, 330), (3050, 330), (3480, 330)), 300, t, 0.82)
    insets_row(c, P, (1760, 2330, 2900), 1810, 330, t, 0.88)
    out = c.convert('RGB').resize((1920, 1080), Image.LANCZOS)
    fn = OUT + f'Portada_RG-WFOG_DataCenter_{lang.upper()}_1920x1080.png'
    out.save(fn); return fn


if __name__ == '__main__':
    for lg in ('es', 'en'):
        print(cover_45(lg)); print(cover_169(lg))
