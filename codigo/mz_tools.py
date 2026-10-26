"""Transiciones de zoom con cámara única (compartido por RG y SIEX)."""
import math
import numpy as np
from PIL import Image, ImageFilter
import cpd_video as B
import cpd_v4 as V
from cpd_video import W, H, SS, S, ss, clamp


def zblur(img, r):
    if r < 0.6:
        return img
    return img.filter(ImageFilter.GaussianBlur(r))


# ---------------- zoom con cámara única (A y B comparten ancla y escala) ----------------
CLEAR = (0, 0, 0, 0)


def smoother(p):
    p = clamp(p)
    return p * p * p * (p * (6 * p - 15) + 10)


def aff(img, Z, f, c, fill=CLEAR):
    """lleva el punto f (1x) a c y escala por Z alrededor de él"""
    if abs(Z - 1) < 1e-4 and abs(f[0] - c[0]) < 1e-3 and abs(f[1] - c[1]) < 1e-3:
        return img
    return img.transform(img.size, Image.AFFINE, (1 / Z, 0, S(f[0]) - S(c[0]) / Z, 0, 1 / Z, S(f[1]) - S(c[1]) / Z),
                         resample=Image.BILINEAR, fillcolor=fill)


def mz(p, fA, fB, R):
    """cámara virtual: zoom geométrico 1 -> R; el foco viaja de fA a fB. Devuelve (ZA, ZB, c, mezcla, desenfoque)"""
    e = smoother(p)
    Z = R ** e
    c = (fA[0] + (fB[0] - fA[0]) * e, fA[1] + (fB[1] - fA[1]) * e)
    m0 = 0.44 if R >= 1 else 0.56
    mix = ss(m0 - 0.2, m0 + 0.2, p)
    bl = 2.4 * SS * math.sin(math.pi * p) * min(1.0, abs(math.log(R)) / 1.4)
    return Z, Z / R, c, mix, bl


def pblend(A, Bm, m):
    """mezcla premultiplicada de dos capas RGBA (sin halos oscuros en bordes transparentes)"""
    if m <= 0.001:
        return A
    if m >= 0.999:
        return Bm
    a = np.asarray(A, dtype=np.float32); b = np.asarray(Bm, dtype=np.float32)
    aa = a[..., 3:4] / 255; ba = b[..., 3:4] / 255
    al = aa * (1 - m) + ba * m
    rgb = a[..., :3] * aa * (1 - m) + b[..., :3] * ba * m
    rgb = np.where(al > 1e-4, rgb / np.maximum(al, 1e-4), 0)
    return Image.fromarray(np.concatenate([rgb, al * 255], -1).clip(0, 255).astype(np.uint8), 'RGBA')


def fade_layer(lay, a):
    if a >= 0.999:
        return lay
    out = lay.copy()
    out.putalpha(out.getchannel('A').point(lambda x: int(x * a)))
    return out


_KPC = {}


def kp_flat(js):
    """todos los puntos 2D con nombre de un json de render"""
    k_ = id(js)
    if k_ not in _KPC:
        out = {}
        def add(n, v):
            if isinstance(v, list) and len(v) == 2 and all(isinstance(x, (int, float)) for x in v):
                out[n] = v
            elif isinstance(v, list):
                for i_, q in enumerate(v):
                    add(f'{n}.{i_}', q)
        for n, v in js.items():
            if n != 'res':
                add(n, v)
        _KPC[k_] = out
    return _KPC[k_]


def kp_screen(name, v):
    return {n: v(p) for n, p in kp_flat(B.SHOTS[name][2]).items()}


def fit_sim(dA, dB):
    """B ≈ R·A + T (planos isométricos del mismo modelo: ajuste exacto)"""
    ks = [k for k in dA if k in dB]
    A_ = np.array([dA[k] for k in ks]); B_ = np.array([dB[k] for k in ks])
    ma, mb = A_.mean(0), B_.mean(0)
    R = float(((A_ - ma) * (B_ - mb)).sum() / ((A_ - ma) ** 2).sum())
    return R, mb - R * ma


def matched(fA, kA, kB):
    R, T = fit_sim(kA, kB)
    return fA, (R * fA[0] + T[0], R * fA[1] + T[1]), R


_RG = {}


def radial(c, r, f0=0.5, f1=1.0):
    """máscara suave circular (0..1) en coordenadas 1x, a 1/8 de resolución"""
    if 'g' not in _RG:
        yy, xx = np.mgrid[0:H // 8, 0:W // 8].astype(np.float32)
        _RG['g'] = (xx * 8 + 4, yy * 8 + 4)
    xx, yy = _RG['g']
    d = np.hypot(xx - c[0], yy - c[1]) / max(r, 1)
    t_ = np.clip((d - f0) / (f1 - f0), 0, 1)
    return 1 - t_ * t_ * (3 - 2 * t_)


def _amul(lay, m):
    """multiplica el alfa de lay por m (array a 1/8 o escalar)"""
    if np.isscalar(m):
        return fade_layer(lay, float(m))
    mm = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).resize(lay.size, Image.BILINEAR)
    out = lay.copy()
    out.putalpha(Image.fromarray((np.asarray(lay.getchannel('A'), dtype=np.float32) * np.asarray(mm, dtype=np.float32) / 255)
                                 .astype(np.uint8)))
    return out


def clip_k(lay, k):
    """recorte a la ventana con intensidad k (0 = sin recorte)"""
    if k <= 0.001:
        return lay
    m = 1 - k * (1 - B.WINM)
    out = lay.copy()
    out.putalpha(Image.fromarray((np.asarray(lay.getchannel('A'), dtype=np.float32) * m).astype(np.uint8)))
    return out


R_DET = 560  # radio (px 1x, en coordenadas del plano de detalle) de la máscara que revela el detalle


def zoom_pair(la, lb, p, fA, fB, R, panelA=False, panelB=False, clip=True, under=None):
    """transición con una sola cámara: el plano general sigue debajo y el de detalle se revela encima,
    anclado en el mismo punto y con escala proporcional (sin saltos de posición)."""
    ZA, ZB, c, _, bl = mz(p, fA, fB, R)
    A = zblur(aff(la, ZA, fA, c), bl)
    Bz = zblur(aff(lb, ZB, fB, c), bl)
    if clip == 'auto':   # recorte a la ventana según cuánto se aleja cada capa de su escala de reposo
        dA = math.hypot(c[0] - fA[0], c[1] - fA[1]); dB = math.hypot(c[0] - fB[0], c[1] - fB[1])
        A = clip_k(A, min(1.0, abs(math.log(ZA)) / 0.15 + dA / 30)); Bz = clip_k(Bz, min(1.0, abs(math.log(ZB)) / 0.15 + dB / 30))
        clip = False
    if abs(math.log(R)) < 0.2:   # mismo encuadre: fundido con la geometría alineada
        m_ = ss(0.15, 0.85, p)
        out = Image.new('RGBA', la.size, (0, 0, 0, 0))
        if B.PANEL_BG[3] > 0 and (panelA or panelB):
            out.alpha_composite(Image.new('RGBA', la.size, B.PANEL_BG[:3] + (int(255 * ((1 - m_) * panelA + m_ * panelB)),)))
        out.alpha_composite(pblend(A, Bz, m_))
        if clip is True:
            out = V.mclip(out)
        elif clip:
            out = clip_k(out, float(clip))
        return out, m_
    if R >= 1:   # acercamiento: A general, B detalle
        wide, det, Zd, pw_, pd_ = A, Bz, ZB, panelA, panelB
        wa = 1 - ss(0.8, 1.0, p); da = ss(0.12, 0.58, p); ramp = ss(0.62, 1.0, p)
    else:        # alejamiento: A detalle, B general
        wide, det, Zd, pw_, pd_ = Bz, A, ZA, panelB, panelA
        wa = ss(0.0, 0.2, p); da = 1 - ss(0.42, 0.88, p); ramp = 1 - ss(0.0, 0.38, p)
    panel_on = B.PANEL_BG[3] > 0
    out = Image.new('RGBA', la.size, (0, 0, 0, 0))
    if under is not None:   # plano general alineado con la cámara: rellena el recorrido entre encuadres
        lu, Ru, fu = under   # capa, escala respecto a A, punto de la capa que corresponde a fA
        ua_ = ss(0.0, 0.2, p) * (1 - ss(0.8, 1.0, p))
        if ua_ > 0.001:
            U = zblur(aff(lu, ZA * Ru, fu, c), bl)
            if clip == 'auto' or clip is False:
                U = clip_k(U, 1.0)
            out.alpha_composite(fade_layer(U, ua_))
    if pw_ and panel_on and wa > 0.001:
        out.alpha_composite(Image.new('RGBA', la.size, B.PANEL_BG[:3] + (int(255 * wa),)))
    out.alpha_composite(fade_layer(wide, wa))
    if da > 0.001:
        m = np.maximum(radial(c, Zd * R_DET), ramp) * da
        if pd_ and panel_on:
            out.alpha_composite(_amul(Image.new('RGBA', la.size, B.PANEL_BG), m))
        out.alpha_composite(_amul(det, m))
    if clip is True:
        out = V.mclip(out)
    elif clip:
        out = clip_k(out, float(clip))
    return out, (da if R >= 1 else 1 - da)
