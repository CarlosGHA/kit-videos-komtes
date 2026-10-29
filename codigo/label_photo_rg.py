"""Etiqueta blanca RG Systems sobre los cilindros de la foto UAC (vista frontal)."""
import math
import numpy as np
from PIL import Image
import os as _os
KW = _os.environ.get('KOMTES_WORK', _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'trabajo'))) + '/'
SP = KW + ''
im = np.array(Image.open(SP + 'assets/rg/uac_bank.png').convert('RGBA')).astype(np.float32)
lab = np.array(Image.open(SP + 'assets/label_rg_tall.png').convert('RGBA')).astype(np.float32)
LH, LW = lab.shape[:2]
R, G, B = im[..., 0], im[..., 1], im[..., 2]
red = (R > 70) & (G < 90) & (B < 90) & (R > G * 1.5)
ARC = math.radians(150)
for cx in (357, 443, 530, 617, 703):
    a = 37.5
    s = (a * ARC) / LW
    y0 = 362
    x0, x1 = int(cx - a), int(cx + a) + 1
    y1 = int(y0 + LH * s) + 1
    X, Y = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
    th = np.arcsin(np.clip((X - cx) / a, -0.999, 0.999))
    u = (th + ARC / 2) / ARC
    tr = (Y - y0) / s
    tc = u * (LW - 1)
    ok = (u >= 0) & (u <= 1) & (tr < LH - 1) & red[y0:y1, x0:x1]
    c0 = np.clip(tc.astype(int), 0, LW - 1); r0 = np.clip(tr.astype(int), 0, LH - 1)
    samp = lab[r0, c0]
    la = samp[..., 3] / 255 * ok
    reg = im[y0:y1, x0:x1]
    shade = np.clip(reg[..., 0] / 215.0, 0.35, 1.12)
    spec = np.clip((np.minimum(reg[..., 1], reg[..., 2]) - 50) / 150.0, 0, 0.5)
    col = samp[..., :3] * shade[..., None] * (1 - spec[..., None]) + 255 * spec[..., None]
    reg[..., :3] = reg[..., :3] * (1 - la[..., None]) + col * la[..., None]
    im[y0:y1, x0:x1] = reg
out = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).convert('RGB')
out.save(SP + 'assets/rg/uac_bank_lab.png')
out.crop((280, 180, 780, 689)).save(SP + 'chk/uac_lab.jpg')
