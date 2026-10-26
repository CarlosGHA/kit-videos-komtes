"""Versión final con transiciones: 1440x1800 (4:5), ES/EN.
Uso: python3 cpd_final.py es|en salida.mp4   |   python3 cpd_final.py still es|en dir t..."""
import sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LANG = sys.argv[2] if sys.argv[1] == 'still' else sys.argv[1]

EN = {
    'CENTROS DE DATOS': 'DATA CENTERS',
    'Agua nebulizada RG W-FOG': 'RG W-FOG water mist',
    'Certificación': 'Certified by',
    'Protección contra incendios con certificación FM para centros de datos: sobre y bajo suelo técnico.':
        'FM-certified fire protection for data centers: above and below the raised floor.',
    'INICIO DEL FUEGO': 'FIRE ONSET',
    'Sobrecalentamiento en un rack': 'Overheating in a rack',
    'Foco en rack': 'Fire source in rack',
    'El calor, el humo y los gases corrosivos de un solo equipo amenazan a toda la sala.':
        'The heat, smoke and corrosive gases from a single unit threaten the entire room.',
    'ACTIVACIÓN': 'ACTIVATION',
    'Boquilla cerrada RG · techo': 'RG closed nozzle · ceiling',
    'Ampolla térmica': 'Thermal bulb',
    'Embellecedor NS1': 'NS1 escutcheon',
    'Micro-orificios': 'Micro-orifices',
    'El calor del incendio sube hasta el techo y calienta la ampolla térmica de la boquilla más próxima al foco.':
        'Heat from the fire rises to the ceiling and warms the thermal bulb of the nozzle closest to the source.',
    'Al alcanzar su temperatura de tarado, la ampolla rompe y solo esa boquilla se abre.':
        'At its rated temperature the bulb bursts, and only that nozzle opens.',
    'Red en reposo': 'Network on standby',
    'Caída de presión': 'Pressure drop',
    'Bomba en marcha': 'Pump running',
    'Presión en la red': 'Network pressure',
    'ARRANQUE DEL BOMBEO': 'PUMP START-UP',
    'Grupo de bombeo RG W-FOG UAP': 'RG W-FOG UAP pump unit',
    'Bomba de alta presión': 'High-pressure pump',
    'Motor eléctrico': 'Electric motor',
    'La apertura de la boquilla hace caer la presión de la red; el grupo lo detecta y arranca la bomba de alta presión.':
        'The open nozzle causes a pressure drop in the network; the pump unit detects it and starts the high-pressure pump.',
    'DESCARGA LOCALIZADA': 'LOCALIZED DISCHARGE',
    'Microgotas a alta presión': 'High-pressure micro-droplets',
    'Resto de boquillas: cerradas': 'Other nozzles: closed',
    'Enfría: absorbe el calor': 'Cools: absorbs the heat',
    'Sofoca: el vapor desplaza el oxígeno': 'Smothers: steam displaces oxygen',
    'La niebla absorbe el calor del foco y el vapor generado desplaza el oxígeno junto a la llama.':
        'The mist absorbs heat from the fire, and the steam it generates displaces the oxygen next to the flame.',
    'Eficaz con la climatización en marcha y sobre equipos en tensión.':
        'Effective with cooling systems running and on energized equipment.',
    'BAJO EL SUELO TÉCNICO': 'BELOW THE RAISED FLOOR',
    'Boquilla cerrada RG · bajo suelo': 'RG closed nozzle · underfloor',
    'Red bajo suelo técnico': 'Underfloor network',
    'Boquilla cerrada': 'Closed nozzle',
    'Bajo el suelo técnico, una red independiente protege los mazos de cables con el mismo principio.':
        'Below the raised floor, an independent network protects the cable bundles on the same principle.',
    'La niebla llega a los huecos entre cables y aglutina las partículas de humo.':
        'The mist reaches the gaps between cables and captures smoke particles.',
    'EXTINCIÓN': 'EXTINGUISHMENT',
    'Vuelta rápida a la actividad': 'Fast return to operation',
    'Fuego extinguido. La niebla restante se disipa con la ventilación y el CPD recupera rápidamente su actividad.':
        'Fire extinguished. The remaining mist clears with ventilation and the data center quickly resumes operation.',
    'OTROS RIESGOS DEL EDIFICIO': 'OTHER RISKS IN THE BUILDING',
    'Generadores y transformadores · RG W-FOG UAC': 'Generators and transformers · RG W-FOG UAC',
    'Cilindro de N₂': 'N₂ cylinder',
    'Para salas de generadores y transformadores del edificio: baterías de cilindros de agua y nitrógeno, sin bombas ni corriente eléctrica.':
        'For generator and transformer rooms in the building: water and nitrogen cylinder banks, with no pumps or electrical power.',
    'Protección contra incendios para centros de datos': 'Fire protection for data centers',
    'Sala de bombeo': 'Pump room',
    'Sala de bombeo · RG W-FOG UAP': 'Pump room · RG W-FOG UAP',
    'Depósito de agua': 'Water tank',
    'Filtros': 'Filters',
    'Grupo de bombeo': 'Pump unit',
    'Cuadro de control': 'Control panel',
    'Montantes a la red': 'Risers to the network',
    'Motor eléctrico': 'Electric motor',
    '400 V · 50 Hz · 1.500 rpm': '400 V · 50 Hz · 1,500 rpm',
    'La apertura de la boquilla hace caer la presión. Desde la sala de bombeo, el cuadro de control lo detecta y arranca el grupo.':
        'The open nozzle causes a pressure drop. In the pump room, the control panel detects it and starts the pump unit.',
    'El motor eléctrico acciona la bomba de pistones, que impulsa el agua a alta presión hacia la red de boquillas.':
        'The electric motor drives the piston pump, which delivers water at high pressure to the nozzle network.',
    'Bomba de pistones': 'Piston pump',
    'Centro de datos': 'Data center', 'Sala de bombeo': 'Pump room',
    'Red de tuberías hasta las boquillas': 'Piping network to the nozzles',
    'Batería UAC en la sala intermedia': 'UAC battery in the intermediate room',
    'Sala de generadores': 'Generator room',
    'Cilindro de N₂': 'N₂ cylinder',
    'Cilindros de agua': 'Water cylinders',
    'Difusores abiertos RG EMM': 'RG EMM open nozzles',
    'Grupos electrógenos': 'Generator sets',
    'Batería RG W-FOG UAC': 'RG W-FOG UAC battery',
    'Difusor abierto RG EMM': 'RG EMM open nozzle',
    'Incendio en un grupo electrógeno': 'Fire in a generator set',
    'Detectores de llama': 'Flame detectors',
    'Central de extinción': 'Releasing panel',
    'El N₂ impulsa el agua': 'N₂ drives the water',
    'Descarga en toda la sala': 'Discharge across the room',
    'Fuego extinguido': 'Fire extinguished',
    'Cilindro de N₂: presuriza la batería': 'N₂ cylinder: pressurises the battery',
    'Salida hacia los difusores': 'Outlet to the nozzles',
    'Insertos de orificio': 'Orifice inserts',
    'Descarga simultánea en toda la sala': 'Simultaneous discharge across the room',
    'Si se declara un incendio en un grupo electrógeno, los detectores de llama lo identifican y la central activa la batería.':
        'If a fire breaks out in a generator set, the flame detectors pick it up and the releasing panel activates the battery.',
    'El nitrógeno impulsa el agua hasta los difusores abiertos, que descargan a la vez sobre toda la sala y extinguen el fuego.':
        'Nitrogen drives the water to the open nozzles, which discharge at once across the whole room and put the fire out.',
    'Sala de generadores · RG W-FOG UAC': 'Generator room · RG W-FOG UAC',
    'Para salas de generadores y transformadores: baterías de cilindros de agua y nitrógeno, sin bombas ni corriente eléctrica.':
        'For generator and transformer rooms: water and nitrogen cylinder batteries, with no pumps and no electrical power.',
    'La batería, en la sala intermedia, alimenta por tubería los difusores abiertos RG EMM.':
        'From the intermediate room, the battery feeds the RG EMM open nozzles through dedicated piping.',
    'Sala de bombeo aledaña · RG W-FOG UAP': 'Adjacent pump room · RG W-FOG UAP',
    'La sala de bombeo, junto al CPD, se conecta por tubería con el colector y los ramales de boquillas de la sala.':
        'The pump room, next to the data center, is piped to the room manifold and the nozzle branches.',
}


def TR(s):
    if LANG != 'en' or not isinstance(s, str):
        return s
    if s in EN:
        return EN[s]
    if len(s) > 5 and s[:2].isdigit() and s[2:5] == ' · ' and s[5:] in EN:
        return s[:5] + EN[s[5:]]
    return s


if LANG == 'en':
    _text = ImageDraw.ImageDraw.text
    ImageDraw.ImageDraw.text = lambda self, xy, text, *a, **k: _text(self, xy, TR(text), *a, **k)
    _gl = ImageFont.FreeTypeFont.getlength
    ImageFont.FreeTypeFont.getlength = lambda self, text, *a, **k: _gl(self, TR(text), *a, **k)

import cpd_video as B
if LANG == 'en':
    _wrap = B.wrap
    B.wrap = lambda text, f, maxw: _wrap(TR(text), f, maxw)
import cpd_v4 as V
import cpd_v5 as V5
import cpd_v6 as V6
from cpd_video import (W, H, SS, FPS, S, ss, win, clamp, full, low, up, spray, tag, subtitle, BG, BG_PLAIN, LOCK_S)

V6.B.SHOTS['ceil_a'] = V6.B.SHOTS['ceil_a']  # (cargados por cpd_v6 desde r5/)
OW, OH = 1440, 1800


# ---------------- herramientas de transición ----------------
def zoom_about(img, fx, fy, s, fill=(255, 255, 255, 255)):
    """escala img por s alrededor del punto (fx, fy) en coordenadas 1x"""
    if abs(s - 1) < 1e-4:
        return img
    c = (1 - 1 / s)
    return img.transform(img.size, Image.AFFINE, (1 / s, 0, S(fx) * c, 0, 1 / s, S(fy) * c),
                         resample=Image.BILINEAR, fillcolor=fill)


def ease_in(p, k=2.4):
    p = clamp(p)
    return p * p * (3 - 2 * p)


def ease_out(p, k=2.4):
    p = clamp(p)
    return p * p * (3 - 2 * p)


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


def zoom_pair(la, lb, p, fA, fB, R, panelA=False, panelB=False, clip=True):
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


# ---------------- escena bajo suelo con zoom interno ----------------
T2 = 2.6
DZ = 0.8


def sc_floor(t, L, img):
    js_f = B.SHOTS['floor'][2]
    p = clamp((t - (T2 - DZ)) / (2 * DZ))
    zA = 1.0 + 0.04 * ss(0, T2, min(t, T2))
    zB = 1.0 + 0.05 * ss(T2, L, t)
    layA = layB = None
    if t < T2 + DZ:
        layA = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        vA, js = B.draw_shot(layA, 'floor', t, zA, 1.0 if B.NOFADE[0] else ss(0, 0.5, t), window=True)
        d = ImageDraw.Draw(img)
        tag(d, 80, 930, 'Red bajo suelo técnico', win(t, 0.6, T2 - DZ), vA(js['uf_noz'][1]))
    if t > T2 - DZ:
        tt = t - T2
        layB = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        vB, jsB = B.draw_shot(layB, 'floor_det' if tt < 0.55 else 'floor_det_b', t, zB, 1.0, window=True)
        nz = vB(jsB['uf_noz'][1])
        nzr = vB(jsB['uf_ring'][1]) if 'uf_ring' in jsB else (nz[0], nz[1] - 6)
        o2, od2 = full(); f2, fd2 = low()
        if 0.5 < tt < 1.7:
            rng = np.random.default_rng(7)
            tb = tt - 0.5
            for i in range(10):
                ang = rng.uniform(0, 6.28); spd = rng.uniform(60, 140)
                px = nz[0] + math.cos(ang) * spd * tb; py = nz[1] - 10 + math.sin(ang) * spd * tb + 200 * tb * tb
                od2.ellipse([S(px - 2.5), S(py - 2.5), S(px + 2.5), S(py + 2.5)], fill=(225, 50, 40, int(220 * clamp(1 - tb))))
        for k_, cl in enumerate(V.CL_UF):
            spray(od2, fd2, cl, tt - 0.3, nzr[0], nzr[1], math.radians(150 if k_ else 30), 1.0, 1.0, drag=1.4, grav=60,
                  fog_a=48, dot_a=255, col=(96, 150, 210))
        spray(od2, fd2, V.CL_UF2, tt - 0.3, nz[0], nz[1] + 20, math.radians(10), 1.3, ss(1.1, 2.3, tt), drag=0.5, grav=4,
              fog_a=55, dot_a=170, col=(96, 150, 210))
        layB.alpha_composite(V.mclip(up(f2, 6))); layB.alpha_composite(V.mclip(o2))
        d = ImageDraw.Draw(img)
        tag(d, 640, 860, 'Boquilla cerrada', win(tt, DZ + 0.2, L - T2 - 0.2), nz)
    if layA is not None and layB is not None:
        fA, fB, R = matched(vA(js_f['uf_noz'][1]), kp_screen('floor', vA), kp_screen('floor_det', vB))
        lay, _ = zoom_pair(layA, layB, p, fA, fB, R, clip=True)
        img.alpha_composite(lay)
    else:
        img.alpha_composite(layA if layA is not None else layB)
    d = ImageDraw.Draw(img)
    V.step_header(d, 5, 'BAJO EL SUELO TÉCNICO', 'Boquilla cerrada RG · bajo suelo', ss(0.2, 0.7, t))
    subtitle(d, 'Bajo el suelo técnico, una red independiente protege los mazos de cables con el mismo principio.', win(t, 0.5, T2 + 1.4))
    subtitle(d, 'La niebla llega a los huecos entre cables y aglutina las partículas de humo.', win(t, T2 + 1.4, L))




# ---------------- escena de bombeo: sala 3D -> zoom -> motor ----------------
import os
B.SHOTS['proom'] = (Image.open(B.SP + 'r5/proom.png').convert('RGBA'), None, __import__('json').load(open(B.SP + 'r5/proom.json')))
# planos con la sala de bombeo aledaña (r7)
R7 = B.SP + ('r8/' if os.path.exists(B.SP + 'r8/site.json') else 'r7/')
_j = __import__('json')
def _l7(n, alt=None):
    D = R7 if os.path.exists(R7 + n + '.json') else B.SP + 'r7/'
    a_ = Image.open(D + n + '.png').convert('RGBA')
    b_ = Image.open(D + n + '_led1.png').convert('RGBA') if alt and os.path.exists(D + n + '_led1.png') else None
    return (a_, b_, _j.load(open(D + n + '.json')))
if os.path.exists(R7 + 'site.png'):
    B.SHOTS['wide'] = _l7('site', True)
    B.SHOTS['proom2'] = _l7('proom2')
    for n_ in ('med', 'floor'):
        if os.path.exists(R7 + n_ + '.png'):
            B.SHOTS[n_] = _l7(n_, True)
    for n_ in ('gen', 'gnoz', 'floor_det', 'floor_det_b', 'ceil_a', 'ceil_b'):
        if os.path.exists(R7 + n_ + '.json'):
            B.SHOTS[n_] = _l7(n_)
PUMP2 = V5.PUMP2
MOTOR_C = (700, 215); MOTOR_R = (200, 185)
TS = 3.0; TZ = 6.4; DZP = 0.8


def pump_detail(img, t, L):
    """foto real del grupo con foco en el motor; t = tiempo local de la escena"""
    k = 0.86 + 0.03 * ss(TZ, L, t)
    on = ss(TZ + 0.3, TZ + 0.5, t)
    jit = math.sin(t * 70) * 0.7 if on > 0.5 else 0
    cx, cy = 540, 760
    out = B.place_scaled(img, PUMP2, k, cx + jit, cy, kref=0.86)
    P = lambda px, py: (cx + (px - PUMP2.width / 2) * k, cy + (py - PUMP2.height / 2) * k)
    # foco en el motor: velo blanco sobre el resto del grupo
    spot = ss(TZ + 1.0, TZ + 1.8, t)
    if spot > 0:
        m = Image.new('L', (W // 4, H // 4), 0)
        mc = P(*MOTOR_C)
        ImageDraw.Draw(m).ellipse([(mc[0] - MOTOR_R[0] * k) / 4, (mc[1] - MOTOR_R[1] * k) / 4,
                                   (mc[0] + MOTOR_R[0] * k) / 4, (mc[1] + MOTOR_R[1] * k) / 4], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(10)).resize((W * SS, H * SS), Image.BILINEAR)
        veil = Image.new('RGBA', (W * SS, H * SS), (255, 255, 255, 0))
        a_ = Image.eval(m, lambda v: int((255 - v) * 0.55 * spot))
        full_a = out.getchannel('A')
        veil.putalpha(Image.fromarray((np.array(a_).astype(np.float32) * np.array(full_a) / 255).astype(np.uint8)))
        img.alpha_composite(veil)
        # anillo rojo pulsante
        d = ImageDraw.Draw(img)
        r_ = 1 + 0.03 * math.sin(t * 6)
        d.ellipse([S(mc[0] - MOTOR_R[0] * k * r_), S(mc[1] - MOTOR_R[1] * k * r_), S(mc[0] + MOTOR_R[0] * k * r_),
                   S(mc[1] + MOTOR_R[1] * k * r_)], outline=B.ca(B.RED, 0.85 * spot), width=B.SW(3))
    return P


def _flow_dots(d, path, t, a, n=14, speed=0.3, col=(255, 255, 255)):
    if a <= 0.01 or len(path) < 2:
        return
    segs = [(p, q, math.hypot(q[0] - p[0], q[1] - p[1])) for p, q in zip(path[:-1], path[1:])]
    tot = sum(sg[2] for sg in segs) or 1
    for i in range(n):
        u = ((t * speed + i / n) % 1) * tot
        for p, q, l in segs:
            if u <= l:
                k_ = u / l if l else 0
                x, y = p[0] + (q[0] - p[0]) * k_, p[1] + (q[1] - p[1]) * k_
                break
            u -= l
        d.ellipse([S(x - 6), S(y - 6), S(x + 6), S(y + 6)], fill=B.ca(B.RED, a), outline=B.ca(col, a), width=B.SW(1.5))


def water_route(img, v, js, t, a, t0=0.0):
    """resalta la red de tuberías: sala de bombeo -> colector del CPD -> ramales -> boquillas"""
    if a <= 0.01:
        return None
    feed = [v(p) for p in js['gp_feed']] + [v(js['gp_main'][1])]
    brs = [[v(js['gp_br'][k_]), v(js['gp_br'][k_ + 3])] for k_ in range(3)]
    glow, gd = low(); lay, ld = full()
    for path in [feed] + brs:
        gd.line([(x / 4, y / 4) for x, y in path], fill=(230, 30, 40, int(150 * a)), width=4, joint='curve')
        ld.line([(S(x), S(y)) for x, y in path], fill=B.ca(B.RED, a), width=B.SW(3.2), joint='curve')
    img.alpha_composite(up(glow, 4)); img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    _flow_dots(d, feed, t - t0, a * ss(t0, t0 + 0.5, t), n=16, speed=0.18)
    for bpath in brs:
        _flow_dots(d, bpath, t - t0 - 0.8, a * ss(t0 + 0.8, t0 + 1.3, t), n=10, speed=0.22)
    return feed


PUMP_R = 3.4  # motor en la sala 3D -> foto del grupo


def sc_pump(t, L, img):
    pS = clamp((t - (TS - DZP)) / (2 * DZP))
    p = clamp((t - (TZ - DZP)) / (2 * DZP))
    jsS = B.SHOTS['wide'][2]
    js = B.SHOTS['proom2'][2]
    L1 = L2 = L3 = None
    # 1) vista del conjunto: CPD + sala de bombeo aledaña, con la red resaltada
    if t < TS + DZP:
        zs = 0.95 + 0.04 * ss(0, TS, min(t, TS))
        vS = B.View(zs, 0, 90)
        L1 = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        B.draw_shot(L1, 'wide', t, zs, 1.0, dy=90, window=True)
        ua = 1 - ss(TS - DZP, TS - DZP + 0.2, t)
        feed = water_route(L1, vS, jsS, t, ss(0.3, 0.8, t) * ua, t0=0.5)
        fa = vS(jsS['annex'])
        d = ImageDraw.Draw(img)
        tag(d, 90, 330, 'Centro de datos', win(t, 0.3, L) * ua, vS(jsS['fire_top']))
        tag(d, 640, 960, 'Sala de bombeo', win(t, 0.6, L) * ua, fa)
        if feed:
            tag(d, 560, 330, 'Red de tuberías hasta las boquillas', win(t, 1.0, L) * ua, feed[2])
    # 2) sala de bombeo en 3D
    if TS - DZP < t < TZ + DZP:
        zoomv = 0.86 + 0.04 * ss(TS, TZ, min(t, TZ))
        v = B.View(zoomv, 0, 40)
        L2 = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        B.draw_shot(L2, 'proom2', t, zoomv, 1.0, dy=40, window=True)
        d = ImageDraw.Draw(img)
        ua = ss(TS + 0.2, TS + 0.6, t) * (1 - ss(TZ - DZP, TZ - DZP + 0.2, t))
        tag(d, 70, 300, 'Depósito de agua', ua * win(t, TS + 0.3, L), v(js['tank']))
        tag(d, 90, 960, 'Filtros', ua * win(t, TS + 0.6, L), v(js['filters']))
        tag(d, 640, 300, 'Cuadro de control', ua * win(t, TS + 0.9, L), v(js['cab']))
        tag(d, 640, 1010, 'Grupo de bombeo', ua * win(t, TS + 1.2, L), v(js['group']))
    # 3) foto real del grupo con foco en el motor
    if t > TZ - DZP:
        L3 = Image.new('RGBA', (W * SS, H * SS), CLEAR)
        P = pump_detail(L3, t, L)
        d = ImageDraw.Draw(img)
        ta = win(t, TZ + 1.4, L - 0.1)
        tag(d, 600, 1040, 'Motor eléctrico', ta, P(MOTOR_C[0] + 30, MOTOR_C[1] + 40))
        if ta > 0.01 and B.UI[0]:
            txt = '400 V · 50 Hz · 1.500 rpm'
            ImageDraw.Draw(B.uiimg(img)).text((S(612), S(1086)), txt, font=B.F_SM, fill=B.ca(B.INK2, ta))
        tag(d, 70, 1040, 'Bomba de pistones', win(t, TZ + 2.0, L - 0.1), P(445, 425))
    if L1 is not None and L2 is not None:
        fA, fB, R = matched(fa, kp_screen('wide', vS), kp_screen('proom2', v))
        lay, _ = zoom_pair(L1, L2, pS, fA, fB, R, clip=True)
    elif L2 is not None and L3 is not None:
        lay, _ = zoom_pair(L2, L3, p, v(js['motor_c']), P(*MOTOR_C), PUMP_R, False, True, clip=True)
    else:
        lay = L1 if L1 is not None else (L2 if L2 is not None else L3)
        if lay is L3 and B.PANEL_BG[3] > 0:
            img.alpha_composite(V.mclip(Image.new('RGBA', img.size, B.PANEL_BG)))
    img.alpha_composite(lay)
    if t > TZ - DZP:
        ga = ss(TZ + 0.4, TZ + 0.9, t)
        if ga > 0.01:
            V.gauge(img, t - TZ + 0.2, ga, (720, 236, 1010, 480))
    d = ImageDraw.Draw(img)
    V.step_header(d, 3, 'ARRANQUE DEL BOMBEO', 'Sala de bombeo aledaña · RG W-FOG UAP', ss(0.2, 0.7, t))
    subtitle(d, 'La sala de bombeo, junto al CPD, se conecta por tubería con el colector y los ramales de boquillas de la sala.',
             win(t, 0.5, TS + 0.6))
    subtitle(d, 'La apertura de la boquilla hace caer la presión. Desde la sala de bombeo, el cuadro de control lo detecta y arranca el grupo.',
             win(t, TS + 0.6, TZ + 1.0))
    subtitle(d, 'El motor eléctrico acciona la bomba de pistones, que impulsa el agua a alta presión hacia la red de boquillas.',
             win(t, TZ + 1.0, L))


# ---------------- guion y transiciones ----------------

# ---------------- otros riesgos: sala de generadores con batería UAC ----------------
from cpd_video import title, card, photo_box
UAC_PH = Image.open(B.SP + 'assets/rg/uac_bank_lab.png').convert('RGB')
UAC_PH_A = Image.open(B.SP + 'assets/rg/uac_bank_cut.png').convert('RGBA')  # recorte sin fondo
EMM_PH = Image.open(B.SP + 'assets/rg/emm_open.png').convert('RGB')
TU1 = 2.8
UF = 6.4; UD = 9.4; UP = 10.6; UA = 11.9
CA0 = 12.9; CB0 = 17.1; CC0 = 21.3; CD0 = 25.0; LU = 28.4
CL_EMM = [B.Cloud(300 + i, 2200, 0.0, 7.0, (0.55, 1.25), 0.2, (300, 470)) for i in range(7)]
UAC_BOX = (60, 230, 1020, 1100)
P_N2 = [(352, 186), (360, 150), (385, 142), (405, 165), (412, 190), (437, 197), (527, 200), (615, 200), (705, 200)]
P_W = [[(437, 182), (440, 150), (475, 128), (540, 118), (553, 98)], [(527, 182), (528, 150), (548, 128), (560, 98)],
       [(615, 182), (610, 148), (588, 128), (573, 98)], [(705, 182), (700, 140), (650, 118), (586, 98)]]
P_OUT = [(570, 100), (570, 168)]
P_PIL = [(250, 205), (300, 205), (340, 192)]


def photo_map(ph, box, z, fx, fy):
    x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
    s_ = max(bw / ph.width, bh / ph.height) * z
    vw, vh = bw / s_, bh / s_
    cx = clamp(fx * ph.width, vw / 2, ph.width - vw / 2); cy = clamp(fy * ph.height, vh / 2, ph.height - vh / 2)
    return lambda px, py: (x0 + (px - (cx - vw / 2)) * s_, y0 + (py - (cy - vh / 2)) * s_)


def pulse(d, p, t, t0, a, col=(214, 10, 32), n=3, rmax=46):
    """anillos de aviso que se expanden desde p"""
    if a <= 0.01 or t < t0:
        return
    for k in range(n):
        ph = ((t - t0) * 0.9 + k / n) % 1
        r = 8 + ph * rmax
        al = a * (1 - ph)
        d.ellipse([S(p[0] - r), S(p[1] - r), S(p[0] + r), S(p[1] + r)], outline=B.ca(col, al), width=B.SW(2.4))
    d.ellipse([S(p[0] - 6), S(p[1] - 6), S(p[0] + 6), S(p[1] + 6)], fill=B.ca(col, a))




def uac_route(img, v, js, t, a, t0=0.0):
    if a <= 0.01 or 'uac_route' not in js:
        return None
    main = [v(p) for p in js['uac_route']]
    brs = [[v(js['uac_br'][0]), v(js['uac_br'][1])], [v(js['uac_br'][2]), v(js['uac_br'][3])]]
    glow, gd = low(); lay, ld = full()
    for path in [main] + brs:
        gd.line([(x / 4, y / 4) for x, y in path], fill=(230, 30, 40, int(150 * a)), width=4, joint='curve')
        ld.line([(S(x), S(y)) for x, y in path], fill=B.ca(B.RED, a), width=B.SW(3.2), joint='curve')
    img.alpha_composite(up(glow, 4)); img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    _flow_dots(d, main, t - t0, a * ss(t0, t0 + 0.5, t), n=14, speed=0.2)
    for bp in brs:
        _flow_dots(d, bp, t - t0 - 0.7, a * ss(t0 + 0.7, t0 + 1.2, t), n=8, speed=0.25)
    return main


CL_GN = [B.Cloud(320 + i, 900, 0.0, 9.0, (0.5, 1.1), 0.15, (240, 380)) for i in range(7)]
UAC_K = 1.18


def _fire_level(t):
    return ss(UF, UF + 1.4, t) * (1 - ss(CB0 + 1.0, CC0 + 1.4, t))


def _st_site(t, L):
    js = B.SHOTS['wide'][2]
    zs = 0.95 + 0.04 * ss(0, TU1, min(t, TU1))
    v = B.View(zs, 0, 60)
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    B.draw_shot(lay, 'wide', t, zs, 1.0 if B.NOFADE[0] else ss(0, 0.4, t), dy=60, window=True)
    uac_route(lay, v, js, t, ss(0.3, 0.8, t), t0=0.5)
    gz = v(js['genroom']); uz = v(js['uac'])

    def tags(d, a):
        tag(d, 80, 330, 'Centro de datos', win(t, 0.3, L) * a, v(js['fire_top']))
        tag(d, 90, 1010, 'Batería UAC en la sala intermedia', win(t, 0.6, L) * a, uz)
        tag(d, 620, 1010, 'Sala de generadores', win(t, 0.9, L) * a, gz)
    return lay, tags, {'out': ((gz[0] + uz[0]) / 2, (gz[1] + uz[1]) / 2), 'room': gz, '_kp': kp_screen('wide', v)}


def _st_gen(t, L, second=False):
    jg = B.SHOTS['gen'][2]
    if not second:
        zg = 1.0 + 0.06 * ss(TU1, CA0, min(max(t, TU1), CA0))
    else:
        zg = 1.06 - 0.04 * ss(CC0, L, t)
    v = B.View(zg, 0, 40)
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    B.draw_shot(lay, 'gen', t, zg, 1.0, dy=40, window=True)
    fl = _fire_level(t)
    if not second:
        sysa = ss(TU1 + 0.1, TU1 + 0.5, t) * (1 - ss(UF - 0.4, UF, t))
        ra = max(sysa, ss(UA, UA + 0.5, t))
    else:
        ra = ss(CC0, CC0 + 0.4, t) * (1 - ss(CC0 + 2.0, CC0 + 3.0, t))
    uac_route(lay, v, jg, t, ra, t0=(TU1 + 0.4) if t < UF else UA)
    if fl > 0.01:
        jsF = {'fire': jg['gfire'], 'fire_top': jg['gfire_top']}
        V.fire_fx(lay, v, jsF, t, fl, 46 * fl, ss(UF + 0.4, UF + 2.2, t) * (1 - ss(CC0, CC0 + 3.0, t)), t - UF)
    if second:
        ma = ss(CC0 - 0.8, CC0, t) * (1 - ss(CD0 - 1.6, CD0 + 0.6, t))
        if ma > 0.01:
            o2, od2 = full(); f2, fd2 = low()
            for i_, q in enumerate(jg.get('gnoz', [])):
                nq = v(q)
                for k_, ang in enumerate((60, 90, 120)):
                    spray(od2, fd2, V.CL_UF2, t - CC0 + 1.2 - 0.05 * i_ - 0.1 * k_, nq[0], nq[1] + 4, math.radians(ang), 0.9, ma,
                          drag=0.7, grav=14, fog_a=46, dot_a=170, col=(96, 150, 210))
            lay.alpha_composite(up(f2, 6)); lay.alpha_composite(o2)

    def tags(d, a):
        if not second:
            sysa_ = ss(TU1 + 0.1, TU1 + 0.5, t) * (1 - ss(UF - 0.4, UF, t))
            tag(d, 70, 300, 'Cilindro de N₂', win(t, TU1 + 0.5, UF - 0.2) * sysa_ * a, v(jg['uac_n2']))
            tag(d, 420, 262, 'Cilindros de agua', win(t, TU1 + 0.8, UF - 0.2) * sysa_ * a, v(jg['uac']))
            tag(d, 600, 1010, 'Difusores abiertos RG EMM', win(t, TU1 + 1.1, UF - 0.2) * sysa_ * a, v(jg['gen_noz']))
            tag(d, 70, 1010, 'Grupos electrógenos', win(t, TU1 + 1.4, UF - 0.2) * sysa_ * a, v(jg['gens'][0]))
            tag(d, 70, 1010, 'Incendio en un grupo electrógeno', win(t, UF + 0.4, UD - 0.1) * a, v(jg['gfire_top']))
            for q in jg.get('gdet', []):
                pulse(d, v(q), t, UD, win(t, UD, UA + 0.4) * a)
            tag(d, 600, 262, 'Detectores de llama', win(t, UD + 0.2, UA) * a, v(jg['gdet'][1]))
            pulse(d, v(jg['gpanel']), t, UP, win(t, UP, CA0) * a)
            tag(d, 70, 300, 'Central de extinción', win(t, UP + 0.2, CA0) * a, v(jg['gpanel']))
            pulse(d, v(jg['uac_n2']), t, UA, win(t, UA, CA0) * a, col=(40, 150, 80))
        else:
            tag(d, 600, 1010, 'Descarga en toda la sala', win(t, CC0 + 0.6, CC0 + 2.6) * a, v(jg['gen_noz']))
            tag(d, 70, 1010, 'Fuego extinguido', win(t, CC0 + 2.0, CD0 - DZP) * a, v(jg['gfire_top']))
    return lay, tags, {'uac': v(jg['uac']), 'room': v(jg['genroom']), 'noz': v(jg['gen_noz']), '_kp': kp_screen('gen', v)}


def _uac_map(t):
    k = UAC_K * (1.0 + 0.04 * ss(CA0, CB0, t))
    cx, cy = 540, 640
    return k, cx, cy, (lambda px, py: (cx + (px - UAC_PH.width / 2) * k, cy + (py - UAC_PH.height / 2) * k))


def _st_photo(t, L):
    k, cx, cy, Pm = _uac_map(t)
    lay = Image.new('RGBA', (W * SS, H * SS), CLEAR)
    B.place_scaled(lay, UAC_PH_A, k, cx, cy, kref=UAC_K)
    ta = t - CA0
    aa = ss(0.2, 0.6, ta)
    if aa > 0.01:
        ld = ImageDraw.Draw(lay)
        _flow_dots(ld, [Pm(*q) for q in P_PIL], ta, aa * (1 - ss(1.6, 2.2, ta)), n=6, speed=0.6)
        _flow_dots(ld, [Pm(*q) for q in P_N2], ta - 0.6, aa * ss(0.6, 1.0, ta), n=18, speed=0.35, col=(60, 170, 90))
        for k_, pw_ in enumerate(P_W):
            _flow_dots(ld, [Pm(*q) for q in pw_], ta - 1.4 - 0.15 * k_, aa * ss(1.4, 1.9, ta), n=7, speed=0.45, col=(110, 170, 235))
        _flow_dots(ld, [Pm(*q) for q in P_OUT], ta - 2.2, aa * ss(2.2, 2.6, ta), n=5, speed=0.7, col=(110, 170, 235))
        pulse(ld, Pm(357, 300), t, CA0 + 0.3, aa * (1 - ss(2.4, 3.0, ta)), col=(40, 150, 80), rmax=70)

    def tags(d, a):
        tag(d, 70, 1010, 'Cilindro de N₂: presuriza la batería', win(t, CA0 + 0.5, CB0) * a, Pm(357, 420))
        tag(d, 600, 1010, 'Cilindros de agua', win(t, CA0 + 1.3, CB0) * a, Pm(700, 450))
        tag(d, 600, 262, 'Salida hacia los difusores', win(t, CA0 + 2.2, CB0) * a, Pm(572, 150))
    return lay, tags, {'bank': Pm(545, 450), 'out': Pm(570, 120), '_panel': True}


def _st_noz(t, L):
    jn = B.SHOTS['gnoz'][2]
    zn = 1.0 + 0.05 * ss(CB0, CC0, t)
    v = B.View(zn, 0, 110)
    lay = Image.new('RGBA', (W * SS, H * SS), CLEAR)
    hd = v(jn['cn_head'])
    heat = _fire_level(t)
    if heat > 0.01:
        glow, gd = low()
        for rr, al in ((420, 60), (260, 90), (140, 120)):
            r = rr * (0.6 + 0.4 * heat) / 4
            gd.ellipse([hd[0] / 4 - r, (hd[1] + 380) / 4 - r, hd[0] / 4 + r, (hd[1] + 380) / 4 + r], fill=(255, 110, 30, int(al * heat)))
        lay.alpha_composite(up(glow, 14))
    B.draw_shot(lay, 'gnoz', t, zn, 1.0, dy=110, window=True)
    over, od = full(); fog, fd = low()
    sa = ss(CB0 + 0.3, CB0 + 0.8, t)
    for i_, (a_, b_) in enumerate(jn.get('cn_orif', [])):
        p0 = v(a_); p1 = v(b_)
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        k = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / 260
        spray(od, fd, CL_GN[i_ % len(CL_GN)], t - CB0 - 0.3 - 0.04 * i_, p0[0], p0[1], ang, max(0.6, k), sa,
              drag=2.2, grav=90, fog_a=34, dot_a=235)
    lay.alpha_composite(up(fog, 6)); lay.alpha_composite(over)

    def tags(d, a):
        tag(d, 640, 380, 'Difusor abierto RG EMM', win(t, CB0 + 0.3, CC0) * a, v(jn['cn_hex']))
        tag(d, 640, 820, 'Insertos de orificio', win(t, CB0 + 1.0, CC0) * a, v(jn['cn_ins']))
        tag(d, 70, 1010, 'Descarga simultánea en toda la sala', win(t, CB0 + 1.8, CC0) * a, None)
    return lay, tags, {'head': hd, '_panel': True}


def _st_site_end(t, L):
    js = B.SHOTS['wide'][2]
    zs = 0.97 - 0.02 * ss(CD0, L, t)
    v = B.View(zs, 0, 60)
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    B.draw_shot(lay, 'wide', t, zs, 1.0, dy=60, window=True)
    gz = v(js['genroom'])

    def tags(d, a):
        return None
    return lay, tags, {'gen': gz, '_kp': kp_screen('wide', v)}


def _uac_stage(i, t, L):
    if i == 5:
        return _st_site_end(t, L)
    if i == 0:
        return _st_site(t, L)
    if i == 1:
        return _st_gen(t, L, False)
    if i == 2:
        return _st_photo(t, L)
    if i == 3:
        return _st_noz(t, L)
    return _st_gen(t, L, True)


# (instante, foco en A, foco en B, R) — R=None: ajuste exacto entre planos isométricos del mismo modelo
UAC_TR = [(TU1, 'room', None, None), (CA0, 'uac', 'bank', 4.1), (CB0, 'out', 'head', 3.0), (CC0, 'head', 'noz', 1 / 8.0),
          (CD0, 'room', None, None)]


def sc_uac(t, L, img):
    D = DZP
    done = False
    for k, (T, fa, fb, Rm) in enumerate(UAC_TR):
        if T - D <= t < T + D:
            p = (t - (T - D)) / (2 * D)
            la, ta, pa = _uac_stage(k, t, L)
            lb, tb, pb = _uac_stage(k + 1, t, L)
            if Rm is None:
                fA, fB, R = matched(pa[fa], pa['_kp'], pb['_kp'])
            else:
                fA, fB, R = pa[fa], pb[fb], Rm
            lay, _ = zoom_pair(la, lb, p, fA, fB, R, pa.get('_panel', False), pb.get('_panel', False), clip=True)
            img.alpha_composite(lay)
            d = ImageDraw.Draw(img)
            ta(d, 1 - ss(0.0, 0.3, p)); tb(d, ss(0.7, 1.0, p))
            done = True
            break
    if not done:
        bounds = [0.0] + [T for T, *_ in UAC_TR] + [L + 1]
        i = max(j for j in range(len(bounds) - 1) if t >= bounds[j]) if t >= 0 else 0
        lay, tg, fo = _uac_stage(min(i, 5), t, L)
        if fo.get('_panel') and B.PANEL_BG[3] > 0:
            img.alpha_composite(V.mclip(Image.new('RGBA', img.size, B.PANEL_BG)))
        img.alpha_composite(V.mclip(lay))
        tg(ImageDraw.Draw(img), 1.0)
    d = ImageDraw.Draw(img)
    title(d, 'OTROS RIESGOS DEL EDIFICIO', 'Sala de generadores · RG W-FOG UAC', ss(0.2, 0.7, t))
    subtitle(d, 'Para salas de generadores y transformadores: baterías de cilindros de agua y nitrógeno, sin bombas ni corriente eléctrica.',
             win(t, 0.5, UF))
    subtitle(d, 'Si se declara un incendio en un grupo electrógeno, los detectores de llama lo identifican y la central activa la batería.',
             win(t, UF, CA0 + 1.0))
    subtitle(d, 'El nitrógeno impulsa el agua hasta los difusores abiertos, que descargan a la vez sobre toda la sala y extinguen el fuego.',
             win(t, CA0 + 1.0, L))

SCENES = [(0.0, 2.4, B.sc_intro, False), (2.4, 7.8, V.sc_fm, True), (7.8, 13.2, V.sc_start, False),
          (13.2, 20.4, V.sc_activation, False), (20.4, 32.4, sc_pump, True), (32.4, 40.0, V.sc_discharge, False),
          (40.0, 48.0, sc_floor, False), (48.0, 53.4, V.sc_ext, True), (53.4, 81.8, sc_uac, True),
          (81.8, 84.8, V.sc_outro, False)]
DUR = 84.8


def M_wide_med(tA, LA, tB, LB):
    vA = B.View(0.86 + 0.05 * ss(0, LA, tA), 0, 60)
    vB = B.View(1.0 + 0.06 * ss(0, LB, tB))
    return matched(vA(B.SHOTS['wide'][2]['fire']), kp_screen('wide', vA), kp_screen('med', vB))


def M_med_ceil(tA, LA, tB, LB):
    vA = B.View(1.0 + 0.06 * ss(0, LA, tA))
    vB = B.View(1.0 + 0.05 * ss(0, LB, tB))
    return vA(B.SHOTS['med'][2]['fire_nozzle']), vB(B.SHOTS['ceil_a'][2]['bulb']), 8.0


def M_ceil_site(tA, LA, tB, LB):
    vA = B.View(1.0 + 0.05 * ss(0, LA, tA))
    vB = B.View(0.95 + 0.04 * ss(0, TS, min(tB, TS)), 0, 90)
    return vA(B.SHOTS['ceil_a'][2]['bulb']), vB(B.SHOTS['wide'][2]['fire_nozzle']), 1 / 6.0


def M_med_floor(tA, LA, tB, LB):
    vA = B.View(1.06 + 0.06 * ss(0, LA, tA))
    vB = B.View(1.0 + 0.04 * ss(0, T2, min(tB, T2)))
    return matched(vA(B.SHOTS['med'][2]['fire']), kp_screen('med', vA), kp_screen('floor', vB))


def M_det_ext(tA, LA, tB, LB):
    vA = B.View(1.0 + 0.05 * ss(T2, LA, tA))
    vB = B.View(0.92 + 0.04 * ss(0, LB, tB), 0, 40)
    fA, fB, _ = matched(vA(B.SHOTS['floor_det'][2]['uf_noz'][1]), kp_screen('floor_det', vA), kp_screen('wide', vB))
    return fA, fB, 1 / 7.0


def M_ext_site(tA, LA, tB, LB):
    vA = B.View(0.92 + 0.04 * ss(0, LA, tA), 0, 40)
    vB = B.View(0.95 + 0.04 * ss(0, TU1, min(tB, TU1)), 0, 60)
    return matched(vA(B.SHOTS['wide'][2]['genroom']), kp_screen('wide', vA), kp_screen('wide', vB))


# transición tras la escena i: (tipo, semiduración, función de cámara -> (fA, fB, R), -)
TRANS = {1: ('zin', 0.8, M_wide_med, None), 2: ('zin', 0.8, M_med_ceil, None), 3: ('zout', 0.8, M_ceil_site, None),
         5: ('zout', 0.8, M_med_floor, None), 6: ('zout', 0.8, M_det_ext, None), 7: ('match', 0.6, M_ext_site, None)}
PUSH = 0.4
PUSH_Z = 1.04
LOCK_POS = (S(1010) - LOCK_S.width, S(60))


def scene_frame(i, t, ui=True, nofade=True):
    a, b, fn, band = SCENES[i]
    B.UI[0] = ui; B.NOFADE[0] = nofade
    img = (BG if band else BG_PLAIN).copy()
    # capa de rótulos/tarjetas aparte: fundidos correctos (ImageDraw sobre RGBA reemplaza en vez de mezclar)
    B.UIL[0] = Image.new('RGBA', img.size, (0, 0, 0, 0)) if ui else None
    fn(t - a, b - a, img)
    if B.UIL[0] is not None:
        img.alpha_composite(B.UIL[0]); B.UIL[0] = None
    if ui and fn not in (B.sc_intro, V.sc_outro):
        img.alpha_composite(LOCK_S, LOCK_POS)
    B.UI[0] = True; B.NOFADE[0] = False
    return img


def scene_parts(i, t):
    """(escena sobre su fondo, capa de rótulos, ¿lleva logotipo?) — la cámara mueve solo la escena"""
    a, b, fn, band = SCENES[i]
    B.UI[0] = True; B.NOFADE[0] = True
    img = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    B.UIL[0] = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fn(t - a, b - a, img)
    ui = B.UIL[0]; B.UIL[0] = None; B.NOFADE[0] = False
    return img, ui, fn not in (B.sc_intro, V.sc_outro), (BG if band else BG_PLAIN)


def render_t(t):
    for i in range(len(SCENES) - 1):
        b = SCENES[i][1]
        kind, D, cam, _ = TRANS.get(i, ('push', PUSH, None, None))
        if b - D <= t < b + D:
            p = (t - (b - D)) / (2 * D)
            aA, bA = SCENES[i][0], SCENES[i][1]; aB, bB = SCENES[i + 1][0], SCENES[i + 1][1]
            cA, uiA, lgA, bgA = scene_parts(i, t)
            cB, uiB, lgB, bgB = scene_parts(i + 1, t)
            if kind == 'push':
                e = smoother(p); c = (W / 2, H / 2)
                Z = 1 + (PUSH_Z - 1) * e if (lgA and lgB) else 1.0  # intro/cierre: fundido puro, el logotipo no se mueve
                cA = aff(cA, Z, c, c); cB = aff(cB, Z / (PUSH_Z if (lgA and lgB) else 1.0), c, c); mix = ss(0, 1, p)
                ua, ub = 1 - ss(0.0, 0.6, p), ss(0.4, 1.0, p)
            else:
                fA, fB, R = cam(t - aA, bA - aA, t - aB, bB - aB)
                lay, mix = zoom_pair(cA, cB, p, fA, fB, R, clip='auto')
                ua, ub = 1 - ss(0.0, 0.3, p), ss(0.7, 1.0, p)
                out = Image.blend(bgA, bgB, ss(0.3, 0.7, p)) if bgA is not bgB else bgA.copy()
                out.alpha_composite(lay)
                cA = None
            if cA is not None:
                A = bgA.copy(); A.alpha_composite(cA)
                Bf = bgB.copy(); Bf.alpha_composite(cB)
                out = Image.blend(A, Bf, mix)
            if ua > 0.01:
                out.alpha_composite(fade_layer(uiA, ua))
            if ub > 0.01:
                out.alpha_composite(fade_layer(uiB, ub))
            la = 1.0 if (lgA and lgB) else (ua if lgA else (ub if lgB else 0))
            if la > 0.01:
                out.alpha_composite(fade_layer(LOCK_S, la), LOCK_POS)
            return out
    for i, (a, b, fn, band) in enumerate(SCENES):
        if a <= t < b or (i == len(SCENES) - 1 and t >= a):
            return scene_frame(i, t)


def render(fi):
    out = render_t(fi / FPS)
    return out.convert('RGB').resize((OW, OH), Image.LANCZOS).tobytes()


if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[4:]:
            Image.frombytes('RGB', (OW, OH), render(int(round(float(ts) * FPS)))).save(f'{sys.argv[3]}/{LANG}_{ts}.png')
    else:
        from multiprocessing import Pool
        n = int(DUR * FPS)
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}',
                               '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high',
                               '-pix_fmt', 'yuv420p', '-movflags', '+faststart', sys.argv[2]], stdin=subprocess.PIPE)
        with Pool(2) as pool:
            for i, fb in enumerate(pool.imap(render, range(n), chunksize=3)):
                ff.stdin.write(fb)
                if i % 300 == 0:
                    print(i, flush=True)
        ff.stdin.close(); ff.wait(); print('done')
