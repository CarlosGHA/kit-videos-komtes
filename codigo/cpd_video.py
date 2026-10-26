"""Vídeo LinkedIn · RG W-FOG en centros de datos. Composición 2D sobre renders Cycles.
1080x1350, 30 fps, sin audio. Estilo: fondo blanco + banda roja diagonal, lockup RG Systems | Komtes."""
import math, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os as _os
KW = _os.environ.get('KOMTES_WORK', _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'trabajo'))) + '/'

_ac = Image.Image.alpha_composite


def _ac2(self, im, dest=(0, 0), source=(0, 0)):
    return _ac(self, im, tuple(int(round(v)) for v in dest), source)


Image.Image.alpha_composite = _ac2

W, H, SS, FPS = 1080, 1350, 2, 30
WS, HS = W * SS, H * SS
DUR = 59.2
SP = KW
R = SP + 'r3/'
A = SP + 'assets/'
FD = '/usr/share/fonts/opentype/inter/'

INK = (43, 45, 47); INK2 = (95, 99, 104); RED = (214, 10, 32); WHITE = (255, 255, 255)
MISTC = (165, 205, 242); SMOKE = (150, 152, 157)


def F(n, px):
    return ImageFont.truetype(FD + n, int(px * SS))


F_T1 = F('InterDisplay-Bold.otf', 34); F_T2 = F('InterDisplay-Medium.otf', 28); F_SUB = F('Inter-Medium.otf', 29)
F_SM = F('Inter-Regular.otf', 20); F_SMB = F('Inter-SemiBold.otf', 21); F_REF = F('InterDisplay-SemiBold.otf', 30)
F_STAT = F('InterDisplay-Bold.otf', 64)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ss(a, b, t):
    x = clamp((t - a) / (b - a)); return x * x * (3 - 2 * x)


def win(t, a, b, f=0.4):
    return ss(a, a + f, t) * (1 - ss(b - f, b, t))


def S(v):
    return v * SS


def SW(v):
    return max(1, int(round(v * SS)))


def ca(c, a):
    return tuple(c[:3]) + (int(255 * clamp(a)),)


def fade_img(im, a):
    if a >= 0.999:
        return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a))); return im


# ---------------- fondo: blanco + banda roja ----------------
def make_bg():
    im = Image.new('RGBA', (WS, HS), WHITE + (255,))
    d = ImageDraw.Draw(im)
    k = math.tan(math.radians(30))
    k = 0.5; y0 = 420; th = 180
    pts = [(0, y0), (W, y0 + W * k), (W, y0 + W * k + th), (0, y0 + th)]
    d.polygon([(S(x), S(y)) for x, y in pts], fill=RED)
    return im


BG = make_bg()
BG_PLAIN = Image.new('RGBA', (WS, HS), WHITE + (255,))


# ---------------- logos ----------------
def logo_light():
    rg = np.array(Image.open(A + 'x729.png').convert('RGBA')).astype(float)
    bb = Image.fromarray(rg.astype(np.uint8)).getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    rg = rg[bb[1]:bb[3], bb[0]:bb[2]]
    red = (rg[..., 0] > 150) & (rg[..., 1] < 100)
    rg[~red, 0:3] = INK
    rg[red, 0:3] = RED
    rgi = Image.fromarray(rg.astype(np.uint8))
    k = np.array(Image.open(A + 'x8.png').convert('RGBA')).astype(float)
    lum = k[..., :3].mean(-1); redk = (k[..., 0] > 150) & (k[..., 1] < 120)
    k[..., 3] = np.where(redk, np.clip((255 - k[..., 1]) * 1.3, 0, 255), np.clip((255 - lum) * 1.4, 0, 255))
    k[~redk, 0:3] = INK; k[redk, 0:3] = RED
    ki = Image.fromarray(k.astype(np.uint8))
    return rgi, ki


RGI, KOMI = logo_light()


def lockup(h_rg=58):
    rg = RGI.resize((S(int(RGI.width * h_rg / RGI.height)), S(h_rg)), Image.LANCZOS)
    hk = int(h_rg * 1.18)
    km = KOMI.resize((S(int(KOMI.width * hk / KOMI.height)), S(hk)), Image.LANCZOS)
    gap = S(26)
    w = rg.width + gap * 2 + SW(2) + km.width; h = max(rg.height, km.height) + S(10)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    im.alpha_composite(rg, (0, h - rg.height - S(4)))
    d = ImageDraw.Draw(im)
    d.rectangle([rg.width + gap, S(2), rg.width + gap + SW(2), h - S(2)], fill=INK2 + (255,))
    im.alpha_composite(km, (rg.width + gap * 2 + SW(2), h - km.height))
    return im


LOCK = lockup(58)
LOCK_S = lockup(22)


# ---------------- renders ----------------
import os


def ld(n):
    if not os.path.exists(R + n):
        n = n.replace('_led1', '') if os.path.exists(R + n.replace('_led1', '')) else 'wide.png'
    return Image.open(R + n).convert('RGBA')


def ldj(n):
    if not os.path.exists(R + n):
        n = 'wide.json'
    return json.load(open(R + n))


SHOTS = {}
for s in ('wide', 'med', 'floor'):
    SHOTS[s] = (ld(f'{s}.png'), ld(f'{s}_led1.png'), ldj(f'{s}.json'))
for s in ('cyl', 'pump'):
    SHOTS[s] = (ld(f'{s}.png'), None, ldj(f'{s}.json'))
RES = SHOTS['wide'][2]['res']   # 1350 x 1688


_yy = np.arange(HS)[:, None] / SS
WINM = np.repeat((np.clip((_yy - 250) / 90, 0, 1) * np.clip((1100 - _yy) / 80, 0, 1)) ** 1.2, WS, axis=1).astype(np.float32)


class View:
    """mapea px del render (RES) a pantalla con zoom y desplazamiento"""
    def __init__(self, zoom, dx=0, dy=0):
        self.k = zoom * W / RES[0]; self.dx, self.dy = dx, dy

    def __call__(self, p):
        return (W / 2 + (p[0] - RES[0] / 2) * self.k + self.dx, H / 2 + (p[1] - RES[1] / 2) * self.k + self.dy)


UI = [True]
NOFADE = [False]
UIL = [None]
PANEL_BG = (255, 255, 255, 255)


def uiimg(img):
    return UIL[0] if UIL[0] is not None else img


def _ud(d):
    """rótulos a la capa UI (si existe) para que no se escalen con la escena en las transiciones"""
    return ImageDraw.Draw(UIL[0]) if UIL[0] is not None else d


def draw_shot(img, name, t, zoom, a=1.0, dy=0, led=True, window=False):
    if NOFADE[0]:
        a = 1.0
    base, alt, js = SHOTS[name]
    v = View(zoom, 0, dy)
    im = base
    if alt is not None and led:
        f = 0.5 + 0.5 * math.sin(t * 5.3) * math.sin(t * 2.1 + 1)
        im = Image.blend(base, alt, clamp(f))
    # escalado con transformación afín de precisión subpíxel (zoom suave, sin saltos de 1 px)
    sc_ = v.k * SS
    x0 = S(W / 2 + v.dx) - RES[0] * sc_ / 2
    y0 = S(H / 2 + v.dy) - RES[1] * sc_ / 2
    full_ = im.convert('RGBa').transform((WS, HS), Image.AFFINE, (1 / sc_, 0, -x0 / sc_, 0, 1 / sc_, -y0 / sc_), resample=Image.BICUBIC).convert('RGBA')
    if window:
        al = Image.fromarray((np.array(full_.getchannel('A')).astype(np.float32) * WINM).astype(np.uint8))
        full_.putalpha(al)
    img.alpha_composite(fade_img(full_, a))
    return v, js


_PS = {}


def place_scaled(img, src, k, cx, cy, kref=None, alpha=1.0):
    """pega src escalado k (px fuente -> px 1x) centrado en (cx, cy) con precisión subpíxel"""
    kref = kref or k
    key = (id(src), round(kref, 4))
    if key not in _PS:
        _PS[key] = src.resize((max(1, round(src.width * kref * SS)), max(1, round(src.height * kref * SS))), Image.LANCZOS).convert('RGBa')
    pre = _PS[key]
    s_ = k / kref
    x0 = S(cx) - pre.width * s_ / 2; y0 = S(cy) - pre.height * s_ / 2
    out = pre.transform((WS, HS), Image.AFFINE, (1 / s_, 0, -x0 / s_, 0, 1 / s_, -y0 / s_), resample=Image.BICUBIC).convert('RGBA')
    if alpha < 0.999:
        out = fade_img(out, alpha)
    img.alpha_composite(out)
    return out


# ---------------- partículas ----------------
class Cloud:
    def __init__(self, seed, n, t0, t1, life, spread, speed):
        r = np.random.default_rng(seed)
        self.b = r.uniform(t0, t1, n); self.L = r.uniform(*life, n)
        self.da = r.normal(0, spread, n); self.sp = r.uniform(*speed, n)
        self.rad = r.uniform(0.7, 1.5, n); self.wob = r.uniform(0, 6.28, n)

    def pos(self, t, ox, oy, ang, scale, drag, grav):
        a = t - self.b
        m = (a > 0) & (a < self.L)
        a = a[m]; th = ang + self.da[m]; sp = self.sp[m] * scale
        dist = sp * (1 - np.exp(-drag * a)) / drag
        x = ox + np.cos(th) * dist + np.sin(a * 2 + self.wob[m]) * 5 * scale
        y = oy + np.sin(th) * dist + grav * a * a * scale
        fade = np.clip(a / 0.12, 0, 1) * np.clip((self.L[m] - a) / 0.6, 0, 1)
        return x, y, fade, self.rad[m] * scale, a


def spray(over, fog, cl, t, ox, oy, ang, scale=1.0, alpha=1.0, drag=1.2, grav=30, fog_a=16, col=MISTC, dot_a=190):
    if alpha <= 0.01:
        return
    x, y, fade, rr, age = cl.pos(t, ox, oy, ang, scale, drag, grav)
    for i in range(len(x)):
        al = int(dot_a * fade[i] * alpha)
        if al < 5:
            continue
        X, Y, Rr = S(x[i]), S(y[i]), S(rr[i])
        over.ellipse([X - Rr, Y - Rr, X + Rr, Y + Rr], fill=col + (al,))
        if i % 2 == 0:
            g = (5 + 20 * min(age[i], 1.4)) * scale / 4
            fog.ellipse([x[i] / 4 - g, y[i] / 4 - g, x[i] / 4 + g, y[i] / 4 + g], fill=col + (int(fog_a * fade[i] * alpha),))


def smoke(fog, t, ox, oy, k, lvl, seed=1, n=40, spread_x=1.0):
    if lvl <= 0.01:
        return
    for i in range(n):
        ph = (t * 0.32 + i / n) % 1
        rise = ph * 230 * k
        drift = ph * ph * 260 * k * spread_x * (1 if i % 2 else -0.7)
        x = ox + math.sin(i * 2.7 + t * 0.8) * (8 + ph * 40) * k + drift
        y = oy - rise
        r = (22 + ph * 80) * k / 4
        al = int(235 * lvl * (1 - ph) ** 0.6)
        fog.ellipse([x / 4 - r, y / 4 - r, x / 4 + r, y / 4 + r], fill=SMOKE + (al,))


def flames(d, glow, bx, by, size, t):
    if size <= 0.5:
        return
    for rr, al in ((3.0, 55), (1.6, 90)):
        Rr = rr * size / 4
        glow.ellipse([bx / 4 - Rr, by / 4 - Rr, bx / 4 + Rr, by / 4 + Rr], fill=(255, 120, 30, al))
    for col, f in [((236, 96, 26), 1.0), ((252, 160, 40), 0.68), ((255, 226, 150), 0.38)]:
        for k in range(4):
            dx = (k - 1.5) * 0.2 * size
            h = size * f * (1.15 + 0.3 * math.sin(t * 8 + k * 2.1) + 0.15 * math.sin(t * 13 + k)) * (1 - 0.18 * abs(k - 1.5))
            w = 0.19 * size * f
            sway = 0.15 * size * math.sin(t * 5 + k * 1.3)
            L, Rt = [], []
            for s_ in np.linspace(0, 1, 10):
                bul = math.sin(math.pi * min(1, s_ * 1.15)) ** 0.7 * (1 - s_ * 0.35)
                xx = bx + dx + sway * s_ * s_; yy = by - h * s_
                L.append((S(xx - w * bul), S(yy))); Rt.append((S(xx + w * bul), S(yy)))
            d.polygon(L + Rt[::-1], fill=col)


def low():
    im = Image.new('RGBA', (W // 4, H // 4), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


def full():
    im = Image.new('RGBA', (WS, HS), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


def up(im, blur):
    return im.convert('RGBa').filter(ImageFilter.GaussianBlur(blur)).resize((WS, HS), Image.BILINEAR).convert('RGBA')


# ---------------- textos ----------------
def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if f.getlength(test) <= S(maxw):
            cur = test
        else:
            lines.append(cur); cur = w
    lines.append(cur); return lines


def title(d, t1, t2, a):
    if not UI[0]:
        return
    if a <= 0.01:
        return
    d = _ud(d)
    d.text((S(70), S(118)), t1, font=F_T1, fill=ca(INK, a))
    if t2:
        y = 162
        for ln in t2.split('\n'):
            d.text((S(70), S(y)), ln, font=F_T2, fill=ca(INK, a)); y += 38


def subtitle(d, text, a):
    if not UI[0]:
        return
    if a <= 0.01:
        return
    d = _ud(d)
    lines = wrap(text, F_SUB, 900)
    y = 1170 - (len(lines) - 1) * 21
    for ln in lines:
        w = F_SUB.getlength(ln)
        d.text((S(W / 2) - w / 2, S(y)), ln, font=F_SUB, fill=ca(INK, a)); y += 42


def tag(d, x, y, txt, a, anchor=None):
    if not UI[0]:
        return
    if a <= 0.01:
        return
    d = _ud(d)
    w = F_SMB.getlength(txt) / SS + 26
    if anchor:
        d.line([(S(anchor[0]), S(anchor[1])), (S(x + 12), S(y + 18))], fill=ca(INK, a * 0.8), width=SW(1.5))
        d.ellipse([S(anchor[0] - 5), S(anchor[1] - 5), S(anchor[0] + 5), S(anchor[1] + 5)], fill=ca(RED, a))
    d.rounded_rectangle([S(x), S(y), S(x + w), S(y + 38)], radius=S(19), fill=ca(WHITE, 0.94 * a), outline=ca(INK, 0.35 * a), width=SW(1))
    d.text((S(x + 13), S(y + 7)), txt, font=F_SMB, fill=ca(INK, a))


# ---------------- boquilla (render real) ----------------
NOZ = Image.open(A + 'a7300.png').convert('RGBA')
_n = np.array(NOZ); _n[92:150, 180:197, 3] = 0
NOZ_B = Image.fromarray(_n).rotate(180)
NOZ = NOZ.rotate(180)
# coords tras rotar 180: (x,y) -> (351-x, 621-y)
BULB = (351 - 190, 621 - 125)
HOLES = [((351 - 263, 621 - 228), math.pi - 0.35 + math.pi), ((351 - 160, 621 - 243), 0.45 + math.pi * 0 + math.pi * 0),
         ((351 - 92, 621 - 205), 0.15), ((351 - 298, 621 - 188), math.pi + 0.1), ((351 - 190, 621 - 92), math.pi / 2)]
# direcciones (pantalla): hacia fuera y hacia abajo
HOLES = [((351 - 263, 621 - 228), math.radians(150)), ((351 - 160, 621 - 243), math.radians(35)),
         ((351 - 92, 621 - 205), math.radians(12)), ((351 - 298, 621 - 188), math.radians(168)),
         ((351 - 190, 621 - 92), math.radians(90))]

REFS = [Image.open(A + 'ref55_9265.png').convert('RGBA'), Image.open(A + 'ref55_9266.png').convert('RGBA'),
        Image.open(A + 'ref60_9444.png').convert('RGBA')]


# ================== ESCENAS ==================
CL_MED = Cloud(3, 2400, 0.0, 12.0, (0.7, 1.4), 0.38, (160, 280))
CL_NOZ = [Cloud(20 + i, 900, 2.6, 7.0, (0.45, 1.0), 0.22, (380, 540)) for i in range(5)]
CL_FLOOR = Cloud(9, 600, 0.0, 9.0, (2.0, 3.4), 0.5, (70, 140))


def sc_intro(t, L, img):
    d = ImageDraw.Draw(img)
    a = ss(0.2, 0.9, t)
    img.alpha_composite(fade_img(LOCK, a), (S(W / 2) - LOCK.width // 2, S(H / 2) - LOCK.height // 2 - S(10 * (1 - a))))


def sc_wide(t, L, img, mist=0.0):
    zoom = 0.9 + 0.05 * ss(0, L, t)
    v, js = draw_shot(img, 'wide', t, zoom, ss(0, 0.5, t))
    if mist > 0:
        fog, fd = low()
        p = v(js['fire'])
        for i in range(10):
            ang = i * 0.63
            r = (60 + 30 * math.sin(i)) / 4
            x, y = p[0] + math.cos(ang) * 110 + 60, p[1] + math.sin(ang) * 50 - 40
            fd.ellipse([x / 4 - r, y / 4 - r * 0.7, x / 4 + r, y / 4 + r * 0.7], fill=MISTC + (int(70 * mist),))
        img.alpha_composite(up(fog, 8))
    return v, js


def sc_s1(t, L, img):
    v, js = sc_wide(t, L, img)
    d = ImageDraw.Draw(img)
    title(d, 'CENTROS DE DATOS', 'RG W-FOG · agua nebulizada', ss(0.2, 0.7, t))
    subtitle(d, 'Funcionan 24/365: su rentabilidad depende de no interrumpir nunca el servicio.', win(t, 0.5, L))


def sc_s2(t, L, img):
    zoom = 1.0 + 0.06 * ss(0, L, t)
    v, js = draw_shot(img, 'med', t, zoom, ss(0, 0.5, t), window=True)
    glow, gd = low(); fog, fd = low(); fl, fld = full()
    lvl = ss(0.4, 3.0, t)
    p = v(js['fire']); pt = v(js['fire_top'])
    # sobrecalentamiento: resplandor en la puerta del rack
    fk = 0.85 + 0.15 * math.sin(t * 11) * math.sin(t * 7.3)
    for rr, al in ((120, 70), (75, 120), (40, 170)):
        r = rr * (0.5 + 0.5 * lvl) / 4
        gd.ellipse([p[0] / 4 - r * 0.55, p[1] / 4 - r * 1.4, p[0] / 4 + r * 0.55, p[1] / 4 + r * 1.2], fill=(255, 105, 20, int(al * lvl * fk)))
    fs = 58 * ss(1.4, 3.2, t)
    flames(fld, gd, pt[0], pt[1] + 8, fs, t)
    img.alpha_composite(up(glow, 6)); img.alpha_composite(fl)
    smoke(fd, t, pt[0], pt[1], 1.0, ss(1.0, 3.5, t), spread_x=1.6)
    img.alpha_composite(up(fog, 7))
    d = ImageDraw.Draw(img)
    title(d, 'EL RIESGO', 'Humo y gases corrosivos', ss(0.2, 0.7, t))
    subtitle(d, 'Un incendio puede afectar a un solo equipo, pero el humo y los gases corrosivos pueden inutilizar toda la sala.',
             win(t, 0.6, L))
    tag(d, pt[0] + 60, pt[1] - 150, 'Sobrecalentamiento en rack', win(t, 1.2, L - 0.3), (pt[0], pt[1] + 20))


def sc_nozzle(t, L, img):
    k = ss(0, L, t)
    sc = 1.22 + 0.1 * k
    cx, cy = 540, 650
    heat = ss(0.6, 2.2, t) * (1 - ss(3.2, 4.6, t))

    def P(px, py):
        return (cx + (px - 175.5) * sc, cy + (py - 310.5) * sc)

    if heat > 0:
        glow, gd = low()
        bx, by = P(*BULB)
        r = 230 * (0.6 + 0.4 * heat) / 4
        gd.ellipse([bx / 4 - r, by / 4 - r, bx / 4 + r, by / 4 + r], fill=(255, 120, 30, int(120 * heat)))
        img.alpha_composite(up(glow, 12))
    nz = NOZ if t < 2.5 else NOZ_B
    w, h = int(nz.width * sc * SS), int(nz.height * sc * SS)
    img.alpha_composite(fade_img(nz.resize((w, h), Image.LANCZOS), ss(0, 0.4, t)), (int(S(cx) - w / 2), int(S(cy) - h / 2)))
    over, od = full(); fog, fd = low()
    if 2.5 < t < 4.2:
        tb = t - 2.5; bx, by = P(*BULB)
        rng = np.random.default_rng(5)
        for i in range(16):
            ang = rng.uniform(0, 6.28); spd = rng.uniform(140, 320)
            px = bx + math.cos(ang) * spd * tb; py = by + math.sin(ang) * spd * tb + 320 * tb * tb
            r = 7; rot = rng.uniform(-8, 8) * tb
            od.polygon([(S(px + r * math.cos(rot + q)), S(py + r * math.sin(rot + q))) for q in (0, 2.3, 4.2)],
                       fill=(205, 215, 225, int(230 * clamp(1 - tb / 1.5))))
            if i < 7:
                od.ellipse([S(px - 2.5), S(py - 2.5), S(px + 2.5), S(py + 2.5)], fill=(225, 70, 40, int(220 * clamp(1 - tb))))
    for cl, ((hx, hy), ang) in zip(CL_NOZ, HOLES):
        X, Y = P(hx, hy)
        spray(od, fd, cl, t, X, Y, ang, sc / 1.4, 1.0, drag=0.9, grav=60, fog_a=22)
    img.alpha_composite(up(fog, 6)); img.alpha_composite(over)
    d = ImageDraw.Draw(img)
    title(d, 'BOQUILLA CERRADA', 'RG EMM-633656CM', ss(0.2, 0.7, t))
    subtitle(d, 'La ampolla térmica rompe con el calor del foco: descarga solo sobre la zona afectada, no en toda la sala.',
             win(t, 0.5, L))
    tag(d, 680, 880, 'Ampolla térmica', win(t, 0.8, 2.4), P(*BULB))


def sc_s4(t, L, img):
    zoom = 1.06 + 0.06 * ss(0, L, t)
    v, js = draw_shot(img, 'med', t + 20, zoom, ss(0, 0.5, t), window=True)
    glow, gd = low(); fog, fd = low(); over, od = full(); fl, fld = full()
    p = v(js['fire']); pt = v(js['fire_top']); nz = v(js['fire_nozzle'])
    lvl = 1 - ss(1.5, 6.0, t)
    for rr, al in ((120, 70), (75, 120), (40, 170)):
        r = rr * (0.5 + 0.5 * lvl) / 4
        gd.ellipse([p[0] / 4 - r * 0.55, p[1] / 4 - r * 1.4, p[0] / 4 + r * 0.55, p[1] / 4 + r * 1.2], fill=(255, 105, 20, int(al * lvl)))
    flames(fld, gd, pt[0], pt[1] + 8, 58 * (1 - ss(1.0, 4.0, t)), t)
    img.alpha_composite(up(glow, 6)); img.alpha_composite(fl)
    smoke(fd, t + 8, pt[0], pt[1], 1.0, 1 - ss(0.8, 4.0, t), spread_x=1.6)
    spray(od, fd, CL_MED, t, nz[0], nz[1] + 4, math.pi / 2, 1.0, 1.0, drag=1.5, grav=25, fog_a=30)
    # nube que envuelve el rack y el pasillo
    hold = ss(1.0, 4.0, t)
    for i in range(9):
        x = p[0] + (i - 4) * 38 + math.sin(t + i) * 8; y = p[1] - 40 + math.cos(i * 1.7 + t * 0.7) * 30
        r = (70 + 20 * math.sin(i)) / 4
        fd.ellipse([x / 4 - r, y / 4 - r, x / 4 + r, y / 4 + r], fill=MISTC + (int(62 * hold),))
    img.alpha_composite(up(fog, 7)); img.alpha_composite(over)
    d = ImageDraw.Draw(img)
    title(d, 'RG W-FOG', 'Descarga localizada', ss(0.2, 0.7, t))
    subtitle(d, 'La niebla absorbe el calor del foco y el vapor desplaza el oxígeno junto a la llama.', win(t, 0.5, 4.6))
    subtitle(d, 'Eficaz con la ventilación y la climatización en marcha, también sobre equipos en tensión.', win(t, 4.6, L))
    tag(d, 70, 300, 'Solo descarga esta boquilla', win(t, 0.8, 4.2), (nz[0], nz[1]))


def sc_s5(t, L, img):
    zoom = 1.0 + 0.05 * ss(0, L, t)
    v, js = draw_shot(img, 'floor', t, zoom, ss(0, 0.5, t), window=True)
    fog, fd = low(); over, od = full()
    ufs = [v(p) for p in js['underfloor']]
    for k_, p in enumerate(ufs):
        spray(od, fd, CL_FLOOR, t + k_ * 1.7, p[0] - 60, p[1] - 30, math.radians(20), 1.0, 0.9, drag=0.5, grav=4, fog_a=48, dot_a=190)
    lvl = ss(0, 1.5, t)
    for i in range(12):
        ph = (t * 0.15 + i / 12) % 1
        x = ufs[0][0] - 120 + ph * 420; y = ufs[0][1] - 10 + math.sin(i * 1.3 + t) * 20 - ph * 30
        r = (40 + 20 * math.sin(i)) / 4
        fd.ellipse([x / 4 - r, y / 4 - r * 0.6, x / 4 + r, y / 4 + r * 0.6], fill=MISTC + (int(85 * lvl),))
    img.alpha_composite(up(fog, 6)); img.alpha_composite(over)
    d = ImageDraw.Draw(img)
    title(d, 'ALCANCE', 'Suelo técnico y pasillos', ss(0.2, 0.7, t))
    subtitle(d, 'Su alta permanencia en suspensión le permite llegar a suelos técnicos, pasillos entre racks y mazos de cables.',
             win(t, 0.5, 3.4))
    subtitle(d, 'Además, aglutina las partículas contaminantes y evita que lleguen a otros equipos.', win(t, 3.4, L))
    tag(d, ufs[2][0] - 40, ufs[2][1] + 70, 'Suelo técnico', win(t, 0.8, L - 0.3), ufs[1])


def sc_s6(t, L, img):
    v, js = sc_wide(t, L, img, mist=1 - ss(0.3, 3.5, t))
    d = ImageDraw.Draw(img)
    title(d, 'CONTINUIDAD', 'Vuelta rápida a la actividad', ss(0.2, 0.7, t))
    subtitle(d, 'Tras la descarga, la niebla se disipa con la ventilación y la actividad se reanuda rápido.', win(t, 0.5, L))


def sc_cyl(t, L, img):
    v, js = draw_shot(img, 'cyl', t, 0.74 + 0.04 * ss(0, L, t), ss(0, 0.5, t), dy=-20)
    d = ImageDraw.Draw(img)
    title(d, 'CPD PEQUEÑO · RG W-FOG UAC', 'Baterías de cilindros: H₂O + N₂', ss(0.2, 0.7, t))
    subtitle(d, 'Agua impulsada por nitrógeno: compacto y sin necesidad de bombas ni de corriente eléctrica.', win(t, 0.5, L))
    tag(d, 120, 400, 'Cilindro de N₂', win(t, 0.9, L - 0.3), v(js['n2']))


def sc_pump(t, L, img):
    v, js = draw_shot(img, 'pump', t, 0.74 + 0.04 * ss(0, L, t), ss(0, 0.5, t), dy=-20)
    d = ImageDraw.Draw(img)
    title(d, 'CPD MEDIANO Y GRANDE · RG W-FOG UAP', 'Grupos de bombeo eléctricos o diésel', ss(0.2, 0.7, t))
    subtitle(d, 'Grupo de bombeo con válvulas de sección: una sola instalación para grandes volúmenes y varios sectores.',
             win(t, 0.5, L))
    tag(d, 690, 410, 'Cuadro de control', win(t, 0.9, L - 0.3), v(js['cab']))
    tag(d, 90, 930, 'Bomba de alta presión', win(t, 1.3, L - 0.3), v(js['pump']))


def sc_refs(t, L, img):
    d = ImageDraw.Draw(img)
    title(d, 'REFERENCIAS', 'Centros de datos protegidos con RG W-FOG', ss(0.2, 0.7, t))
    items = [(REFS[1], 'Ministerio de Defensa', 'Madrid · CPD'), (REFS[0], 'Ministerio de Defensa', 'Madrid · grupo de bombeo'),
             (REFS[2], 'Microsoft Data Center', 'Ámsterdam · salas de máquinas')]
    boxes = [(70, 290, 1010, 650), (70, 680, 530, 1060), (550, 680, 1010, 1060)]
    for i, ((ph, n1, n2), bx) in enumerate(zip(items, boxes)):
        a = ss(0.4 + i * 0.35, 0.9 + i * 0.35, t)
        if a <= 0:
            continue
        x0, y0, x1, y1 = bx; bw, bh = x1 - x0, y1 - y0
        z = 1.0 + 0.06 * ss(0, L, t)
        s_ = max(bw / ph.width, bh / ph.height) * z
        vw, vh = bw / s_, bh / s_
        crop = ph.crop((int((ph.width - vw) / 2), int((ph.height - vh) / 2), int((ph.width + vw) / 2), int((ph.height + vh) / 2)))
        crop = crop.resize((S(bw), S(bh)), Image.LANCZOS)
        m = Image.new('L', crop.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, crop.width, crop.height], radius=S(14), fill=int(255 * a))
        crop.putalpha(m)
        img.alpha_composite(crop, (S(x0), S(y0)))
        d.rounded_rectangle([S(x0 + 14), S(y1 - 72), S(x0 + 14) + F_SMB.getlength(n1) + S(28), S(y1 - 14)], radius=S(10),
                            fill=ca(WHITE, 0.94 * a))
        d.text((S(x0 + 28), S(y1 - 66)), n1, font=F_SMB, fill=ca(INK, a))
        d.text((S(x0 + 28), S(y1 - 40)), n2, font=F_SM, fill=ca(INK2, a))
    subtitle(d, 'Proyecto, fabricación y ensayos propios en Burgos, con sistemas homologados por FM y VdS.', win(t, 1.4, L))



CERT = A + 'cert/'
LOGOS = [('FM Approved', 'p18_1103.png'), ('VdS', 'p18_1104.png'), ('Bureau Veritas', 'p18_1106.png'),
         ('SINTEF', 'p18_886.png'), ('Efectis', 'p18_1107.png'), ('CNPP', 'p18_1105.png')]
def _crop_logo(im):
    a = np.array(im.convert('RGBA')).astype(int)
    ink = (a[..., 3] > 30) & (a[..., :3].min(-1) < 235)
    ys, xs = np.nonzero(ink)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)) if len(xs) else im


LOGO_IM = [_crop_logo(Image.open(CERT + f).convert('RGBA')) for _, f in LOGOS]
LAB_FIRE = Image.open(CERT + 'p5_166.png').convert('RGBA')
LAB_MIST = Image.open(CERT + 'p5_127.png').convert('RGBA')


def card(img, box, a, lift=0.0, radius=16):
    if not UI[0]:
        return
    """tarjeta blanca con sombra suave"""
    img = uiimg(img)
    x0, y0, x1, y1 = box
    sh, sd = low()
    sd.rounded_rectangle([x0 / 4, (y0 + 10) / 4, x1 / 4, (y1 + 14) / 4], radius=radius / 4, fill=(20, 22, 26, int(70 * a)))
    img.alpha_composite(up(sh, 5))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([S(x0), S(y0), S(x1), S(y1)], radius=S(radius), fill=ca(WHITE, a), outline=ca((225, 227, 230), a), width=SW(1))


def fit_logo(img, logo, box, a, pad=26):
    if not UI[0]:
        return
    img = uiimg(img)
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0 - 2 * pad, y1 - y0 - 2 * pad
    k = min(bw / logo.width, bh / logo.height)
    w, h = int(logo.width * k * SS), int(logo.height * k * SS)
    im = logo.resize((w, h), Image.LANCZOS)
    img.alpha_composite(fade_img(im, a), (int(S((x0 + x1) / 2) - w / 2), int(S((y0 + y1) / 2) - h / 2)))


def sc_cert(t, L, img):
    d = ImageDraw.Draw(img)
    title(d, 'HOMOLOGACIONES', 'Tecnología RG W-FOG ensayada y aprobada', ss(0.2, 0.7, t))
    cw, ch, gx, gy = 296, 186, 26, 26
    x_start = (W - (3 * cw + 2 * gx)) / 2; y_start = 340
    for i, logo in enumerate(LOGO_IM):
        a = ss(0.5 + i * 0.22, 0.95 + i * 0.22, t)
        if a <= 0:
            continue
        col, row = i % 3, i // 3
        dy = 26 * (1 - a)
        x0 = x_start + col * (cw + gx); y0 = y_start + row * (ch + gy) + dy
        box = (x0, y0, x0 + cw, y0 + ch)
        card(img, box, a)
        fit_logo(img, logo, box, a, pad=[30, 42, 28, 40, 40, 38][i])
    d = ImageDraw.Draw(img)
    x = 70
    chips = ['FM Approved · FM 5560', 'VdS', 'Diseño según EN 14972']
    tw = sum(F_SMB.getlength(c) / SS + 26 for c in chips) + 12 * (len(chips) - 1)
    x = (W - tw) / 2
    for i, c in enumerate(chips):
        aa = ss(2.3 + i * 0.25, 2.7 + i * 0.25, t)
        tag(d, x, 820, c, aa)
        x += F_SMB.getlength(c) / SS + 26 + 12
    subtitle(d, 'Sistemas ensayados y aprobados por los organismos certificadores de referencia a nivel internacional.', win(t, 0.6, L))


def sc_cert_cpd(t, L, img):
    zoom = 1.0 + 0.05 * ss(0, L, t)
    v, js = draw_shot(img, 'floor', t, zoom, ss(0, 0.5, t), window=True)
    d = ImageDraw.Draw(img)
    title(d, 'CPD · SOBRE Y BAJO SUELO TÉCNICO', 'Ensayado según protocolo FM', ss(0.2, 0.7, t))
    noz = [v(p) for p in js['nozzles']]
    noz = [p for p in noz if 120 < p[0] < 960 and 300 < p[1] < 1000]
    above = min(noz, key=lambda p: abs(p[0] - 560) + abs(p[1] - 520)) if noz else (560, 520)
    uf = v(js['underfloor'][1])
    tag(d, 610, 330, 'Sobre suelo · MM-P51-57-11', win(t, 0.7, L - 0.2), above)
    tag(d, 80, 930, 'Bajo suelo · MM-P52-57-11', win(t, 1.1, L - 0.2), uf)
    a = ss(1.6, 2.2, t)
    if a > 0:
        box = (600, 880, 1010, 1090)
        card(img, box, a)
        fit_logo(img, LOGO_IM[2], (box[0] + 10, box[1] + 10, box[0] + 150, box[1] + 160), a, pad=14)
        fit_logo(img, LOGO_IM[0], (box[0] + 150, box[1] + 10, box[0] + 300, box[1] + 160), a, pad=18)
        d = ImageDraw.Draw(img)
        d.text((S(box[0] + 300), S(box[1] + 50)), 'Data', font=F_SMB, fill=ca(INK, a))
        d.text((S(box[0] + 300), S(box[1] + 78)), 'Center', font=F_SMB, fill=ca(INK, a))
        t2 = 'Protocolo FM · sobre y bajo suelo'
        d.text((S((box[0] + box[2]) / 2) - F_SM.getlength(t2) / 2, S(box[1] + 168)), t2, font=F_SM, fill=ca(INK2, a))
    subtitle(d, 'Boquillas para CPD sobre y bajo suelo técnico, ensayadas por Bureau Veritas según el protocolo FM.', win(t, 0.5, L))


def photo_box(img, ph, box, z, a, fx=0.5, fy=0.5):
    x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
    s_ = max(bw / ph.width, bh / ph.height) * z
    vw, vh = bw / s_, bh / s_
    cx = clamp(fx * ph.width, vw / 2, ph.width - vw / 2); cy = clamp(fy * ph.height, vh / 2, ph.height - vh / 2)
    crop = ph.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((S(bw), S(bh)), Image.LANCZOS)
    m = Image.new('L', crop.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, crop.width, crop.height], radius=S(16), fill=int(255 * a))
    crop.putalpha(m)
    img.alpha_composite(crop, (S(x0), S(y0)))


def sc_lab(t, L, img):
    d = ImageDraw.Draw(img)
    title(d, 'LABORATORIOS PROPIOS', 'Ensayos con fuego real', ss(0.2, 0.7, t))
    box = (70, 270, 1010, 760)
    a = ss(0.2, 0.7, t)
    card(img, box, a)
    z = 1.04 + 0.08 * ss(0, L, t)
    photo_box(img, LAB_FIRE, box, z, a, 0.42, 0.5)
    k = ss(2.2, 2.9, t)
    if k > 0:
        photo_box(img, LAB_MIST, box, z, a * k, 0.5, 0.5)
    d = ImageDraw.Draw(img)
    stats = [('2.500 m²', 'de áreas de', 'ensayo propias'), ('2', 'laboratorios de', 'fuego real homologados'),
             ('3', 'áreas de fuego,', 'hasta 20 × 20 × 18 m')]
    cw = 296; gx = 26; x = (W - (3 * cw + 2 * gx)) / 2
    for i, (big, l1, l2) in enumerate(stats):
        aa = ss(0.9 + i * 0.3, 1.4 + i * 0.3, t)
        if aa <= 0:
            continue
        bx = (x + i * (cw + gx), 800, x + i * (cw + gx) + cw, 1060)
        card(img, bx, aa)
        d = ImageDraw.Draw(img)
        d.text((S(bx[0] + 26), S(bx[1] + 34)), big, font=F_STAT, fill=ca(RED, aa))
        d.text((S(bx[0] + 26), S(bx[1] + 136)), l1, font=F_SMB, fill=ca(INK, aa))
        d.text((S(bx[0] + 26), S(bx[1] + 166)), l2, font=F_SMB, fill=ca(INK, aa))
    subtitle(d, 'Grupo Komtes dispone de laboratorios homologados para ensayar sus sistemas con fuego real.', win(t, 0.6, L))


def sc_outro(t, L, img):
    a = ss(0.1, 0.8, t)
    img.alpha_composite(fade_img(LOCK, a), (S(W / 2) - LOCK.width // 2, S(H / 2) - LOCK.height // 2 - S(40)))
    d = ImageDraw.Draw(img)
    for i, (txt, f_, c) in enumerate([('Protección contra incendios ensayada y aprobada para centros de datos', F_T2, INK), ('www.komtes.com', F_SMB, RED)]):
        d.text((S(W / 2) - f_.getlength(txt) / 2, S(H / 2 + 50 + i * 48)), txt, font=f_, fill=ca(c, ss(0.6, 1.3, t)))


SCENES = [(0.0, 2.4, sc_intro, False), (2.4, 7.4, sc_s1, True), (7.4, 12.8, sc_s2, False), (12.8, 18.4, sc_nozzle, True),
          (18.4, 26.0, sc_s4, False), (26.0, 31.6, sc_s5, False), (31.6, 35.8, sc_cyl, True), (35.8, 40.2, sc_pump, True),
          (40.2, 45.8, sc_cert, True), (45.8, 51.2, sc_cert_cpd, False), (51.2, 56.4, sc_lab, False), (56.4, 59.2, sc_outro, False)]
XF = 0.35


def render(fi):
    t = fi / FPS
    out = None
    for (a, b, fn, band) in SCENES:
        if a - XF <= t <= b + XF:
            al = (ss(a - XF, a + 0.02, t) if a > 0 else 1.0) * ((1 - ss(b - 0.02, b + XF, t)) if b < DUR else 1.0)
            if al <= 0.01:
                continue
            img = (BG if band else BG_PLAIN).copy()
            fn(t - a, b - a, img)
            # lockup pequeño (como en la referencia) arriba a la derecha
            if fn not in (sc_intro, sc_outro):
                img.alpha_composite(LOCK_S, (S(1010) - LOCK_S.width, S(60)))
            out = img if out is None else Image.blend(out, img, al)
    return out.convert('RGB').resize((W, H), Image.LANCZOS).tobytes()


if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[3:]:
            Image.frombytes('RGB', (W, H), render(int(float(ts) * FPS))).save(f'{sys.argv[2]}/c_{ts}.png')
    else:
        from multiprocessing import Pool
        n = int(DUR * FPS)
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                               '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17',
                               '-pix_fmt', 'yuv420p', '-movflags', '+faststart', sys.argv[2]], stdin=subprocess.PIPE)
        with Pool(2) as pool:
            for i, fb in enumerate(pool.imap(render, range(n), chunksize=3)):
                ff.stdin.write(fb)
                if i % 150 == 0:
                    print(i, flush=True)
        ff.stdin.close(); ff.wait(); print('done')
