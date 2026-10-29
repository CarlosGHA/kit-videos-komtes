"""Texturas de etiqueta para cilindros: SIEX (agente limpio) y RG Systems (UAC)."""
import random
from PIL import Image, ImageDraw, ImageFont
import os as _os
KW = _os.environ.get('KOMTES_WORK', _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'trabajo'))) + '/'
SP = KW + ''
A = SP + 'assets/'
FD = '/usr/share/fonts/opentype/inter/'
random.seed(7)
RED = (214, 10, 32, 255)
INK = (30, 32, 36, 255)
GREY = (150, 152, 156, 255)


def fit(im, w=None, h=None):
    im = im.crop(im.getbbox())
    k = (w / im.width) if w else (h / im.height)
    if w and h:
        k = min(w / im.width, h / im.height)
    return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)


def text_block(d, x0, y0, x1, y1, bars=True, lh=26):
    y = y0
    while y < y1 - lh:
        w = random.uniform(0.35, 0.95) * (x1 - x0)
        if bars and random.random() < 0.45:
            d.rectangle([x0, y + 3, x0 + w * 0.7, y + lh - 5], fill=INK)
        else:
            d.rectangle([x0, y + 8, x0 + w, y + 13], fill=GREY)
        y += lh


def siex_label():
    """ancho = arco visible del cilindro; alto = 0.95 m aprox. (pegatina UL/FM arriba + etiqueta principal)"""
    W, H = 1000, 1500
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # pegatina de certificaciones
    sx0, sy0, sx1, sy1 = 560, 0, 880, 190
    d.rectangle([sx0, sy0, sx1, sy1], fill=(250, 250, 250, 255))
    ul = Image.open('/root/.claude/uploads/9170677f-e914-5fad-9582-ded74f623b9a/f3a186a2-image.png').convert('RGBA')
    ul = fit(ul, h=120); im.alpha_composite(ul, (sx0 + 22, sy0 + 18))
    fm = fit(Image.open(A + 'siex/fm.png').convert('RGBA'), w=130); im.alpha_composite(fm, (sx0 + 170, sy0 + 40))
    f = ImageFont.truetype(FD + 'Inter-Bold.otf', 30)
    d.text((sx0 + 30, sy0 + 145), 'LISTED', font=f, fill=INK)
    # etiqueta principal
    y0 = 300
    d.rectangle([0, y0, W, H], fill=(250, 250, 250, 255))
    d.rectangle([24, y0 + 20, W - 24, H - 24], outline=(60, 60, 64, 255), width=5)
    # cabecera: triángulo rojo + logo SIEX
    d.polygon([(70, y0 + 230), (150, y0 + 90), (230, y0 + 230)], fill=RED)
    d.polygon([(118, y0 + 230), (150, y0 + 170), (182, y0 + 230)], fill=(250, 250, 250, 255))
    lg = fit(Image.open(A + 'siex/siex_logo.png').convert('RGBA'), w=560)
    im.alpha_composite(lg, (270, y0 + 70))
    d.line([(40, y0 + 270), (W - 40, y0 + 270)], fill=(60, 60, 64, 255), width=4)
    text_block(d, 60, y0 + 300, 470, H - 220)
    d.rectangle([500, y0 + 300, W - 50, H - 220], outline=(60, 60, 64, 255), width=3)
    text_block(d, 525, y0 + 320, W - 70, H - 240, bars=False, lh=22)
    text_block(d, 60, H - 200, W - 300, H - 50, bars=True, lh=30)
    d.polygon([(W - 200, H - 120), (W - 140, H - 180), (W - 80, H - 120), (W - 140, H - 60)], outline=INK, fill=(250, 250, 250, 255))
    im.save(A + 'siex/label_siex.png')
    return im


def rg_label(H=1100, out='label_rg.png'):
    W = 1000
    im = Image.new('RGBA', (W, H), (250, 250, 250, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([24, 24, W - 24, H - 24], outline=(70, 70, 74, 255), width=5)
    lg = Image.open(A + 'rg_logo_hi.png').convert('RGBA')
    import numpy as np
    a = np.array(lg); wm = (a[:, :, 0] > 170) & (a[:, :, 1] > 170) & (a[:, :, 2] > 170)
    a[wm, 0], a[wm, 1], a[wm, 2] = 52, 54, 58
    lg = fit(Image.fromarray(a), w=760)
    im.alpha_composite(lg, ((W - lg.width) // 2, 90))
    f = ImageFont.truetype(FD + 'Inter-Bold.otf', 70)
    t = 'W-FOG · UAC'
    d.text(((W - f.getlength(t)) / 2, 90 + lg.height + 50), t, font=f, fill=INK)
    yy = 90 + lg.height + 160
    d.line([(60, yy), (W - 60, yy)], fill=RED, width=10)
    text_block(d, 70, yy + 40, W - 70, H - 60, bars=False, lh=34)
    im.save(A + out)
    return im


if __name__ == '__main__':
    a = siex_label(); b = rg_label(); rg_label(1500, 'label_rg_tall.png')
    c = Image.new('RGB', (2100, 1500), (120, 20, 20)); c.paste(a, (0, 0), a); c.paste(b, (1050, 0))
    c.resize((1050, 750)).save(SP + 'chk/labels.jpg')
