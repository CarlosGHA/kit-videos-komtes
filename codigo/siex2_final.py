"""Vídeo LinkedIn · Extinción por gas SIEX en centros de datos (ES/EN), 4:5.
Misma interfaz que cpd_final para reutilizar el montaje (siex_master.py)."""
import sys, math, json, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ('es', 'en') else (sys.argv[2] if len(sys.argv) > 2 else 'es')

EN = {
    'CENTROS DE DATOS': 'DATA CENTERS',
    'Extinción automática por gas SIEX': 'SIEX automatic gas suppression',
    'Certificaciones': 'Certified',
    'Extinción automática por gas con certificaciones UL y FM para proteger centros de datos.':
        'Automatic gas fire suppression, UL listed and FM approved, to protect data centers.',
    'DETECCIÓN': 'DETECTION', 'Detección temprana del humo': 'Early smoke detection',
    'Foco en rack': 'Fire in a rack', 'Detector 1 · alarma': 'Detector 1 · alarm', 'Detector 2 · confirmación': 'Detector 2 · confirmation',
    'Un rack se sobrecalienta y empieza a generar humo.': 'A rack overheats and starts to smoke.',
    'Los detectores lo identifican en su fase más temprana.': 'Detectors pick it up at the earliest stage.',
    'ALARMA': 'ALARM', 'Prealarma y evacuación': 'Pre-alarm and evacuation',
    'EXTINCIÓN DISPARADA': 'GAS RELEASED', 'PREALARMA': 'PRE-ALARM', 'DESCARGA': 'DISCHARGE',
    'Retardo de descarga': 'Discharge delay', 'Central de extinción': 'Extinguishing panel',
    'Sirena y flash': 'Sounder and beacon', 'Rótulo de extinción': 'Gas release sign', 'Pulsadores disparo / paro': 'Release / hold buttons',
    'Evacuación del personal': 'Staff evacuation', 'Climatización detenida': 'HVAC shut down', 'Puertas cerradas': 'Doors closed',
    'Al confirmarse el incendio, la central activa la alarma y la cuenta atrás.':
        'Once the fire is confirmed, the panel triggers the alarm and the countdown.',
    'El personal evacúa la sala y la climatización se detiene.': 'Staff evacuate the room and the air conditioning shuts down.',
    'DISPARO': 'RELEASE', 'Sala de cilindros · INERT SIEX': 'Cylinder room · INERT SIEX',
    'Batería principal': 'Main bank', 'Batería de reserva': 'Reserve bank', 'Válvulas direccionales': 'Directional valves',
    'Actuador de disparo': 'Release actuator', 'Colector': 'Manifold', 'Presostato': 'Pressure switch',
    'Carga supervisada': 'Monitored charge', 'Presión': 'Pressure', 'Peso': 'Weight', 'Descargando': 'Discharging',
    'En la sala de cilindros, la central acciona el disparo y la batería descarga.':
        'In the cylinder room, the panel releases the system and the bank discharges.',
    'Presostatos y sistemas de pesaje vigilan la carga en todo momento.':
        'Pressure switches and weighing systems monitor the charge at all times.',
    'Difusor silencioso SIEX': 'SIEX silent nozzle', 'Malla difusora': 'Diffuser mesh', 'Orificios de descarga': 'Discharge orifices',
    'Nivel sonoro': 'Sound level',
    'El gas entra en la sala por difusores silenciosos, por debajo de 90 dB, para proteger los equipos sensibles.':
        'Gas enters the room through silent nozzles, below 90 dB, to protect sensitive equipment.',
    'INUNDACIÓN TOTAL': 'TOTAL FLOODING', 'Sobre y bajo el suelo técnico': 'Above and below the raised floor',
    'Concentración de diseño': 'Design concentration', 'Alcanzada': 'Reached',
    'Difusores de sala': 'Room nozzles', 'Difusores bajo suelo': 'Underfloor nozzles',
    'El agente inunda todo el recinto, sobre y bajo el suelo técnico, hasta la concentración de extinción.':
        'The agent floods the whole enclosure, above and below the raised floor, up to the extinguishing concentration.',
    'Sin agua y sin residuos.': 'No water, no residue.',
    'EXTINCIÓN': 'EXTINCTION', 'Vuelta a la actividad': 'Back in service',
    'Sin agua': 'No water', 'Sin residuos': 'No residue', 'Sin daños en los equipos': 'No damage to equipment',
    'Fuego extinguido. Tras ventilar la sala, el centro de datos vuelve a la actividad, sin limpiezas ni daños.':
        'Fire out. Once the room is ventilated, the data center is back in service, with no clean-up and no damage.',
    'VÁLVULAS DIRECCIONALES': 'DIRECTIONAL VALVES', 'Una batería, varias salas': 'One bank, several rooms',
    'Sala 1': 'Room 1', 'Sala 2': 'Room 2', 'Sala 3': 'Room 3',
    'Con válvulas direccionales, una sola batería protege varias salas.': 'With directional valves, a single bank protects several rooms.',
    'Una batería de reserva mantiene la protección durante el mantenimiento.':
        'A reserve bank keeps protection in place during maintenance.',
    'AGENTES LIMPIOS': 'CLEAN AGENTS', 'Gases inertes y FK-5-1-12': 'Inert gases and FK-5-1-12',
    'Gases inertes': 'Inert gases', 'Obtenidos de la atmósfera': 'Taken from the atmosphere',
    'Argón': 'Argon', 'Nitrógeno': 'Nitrogen', '50% Argón · 50% Nitrógeno': '50% Argon · 50% Nitrogen',
    '52% N₂ · 40% Ar · 8% CO₂': '52% N₂ · 40% Ar · 8% CO₂',
    '150 · 200 · 300 bar': '150 · 200 · 300 bar', 'Agente químico limpio': 'Clean chemical agent',
    'No conductor · sin residuos': 'Non-conductive · no residue',
    'Gases inertes obtenidos de la atmósfera o FK-5-1-12: una solución limpia para cada centro de datos.':
        'Inert gases taken from the atmosphere, or FK-5-1-12: a clean solution for every data center.',
    'Ingeniería contra incendios para infraestructuras críticas': 'Fire protection engineering for critical infrastructure',
    'Agentes limpios de inundación total': 'Clean agent total flooding systems',
    'Sistemas SIEX de agentes limpios de inundación total, con certificaciones UL y FM.': 'SIEX clean agent total flooding systems, UL listed and FM approved.',
    'Centro de datos': 'Data center', 'Red de tuberías hasta los difusores': 'Piping network to the nozzles', 'Hacia los difusores del CPD': 'To the data center nozzles', 'Sala de cilindros': 'Cylinder room', 'Anclaje a la pared': 'Wall-mounted',
    'SALA DE CILINDROS': 'CYLINDER ROOM', 'Aledaña al centro de datos': 'Next to the data center',
    'En una sala aledaña al CPD, las baterías de cilindros se anclan a la pared.': 'In a room next to the data center, the cylinder banks are mounted on the wall.',
    'La batería de reserva mantiene la protección durante el mantenimiento.': 'The reserve bank keeps protection in place during maintenance.',
    'Cilindro piloto': 'Pilot cylinder', 'Latiguillos': 'Flexible hoses', 'Línea de pilotaje': 'Pilot line',
    'Presión de la carga': 'Charge pressure', 'Cilindro piloto y colector': 'Pilot cylinder and manifold',
    'Al disparar, el cilindro piloto abre las válvulas de los cilindros y el gas llega al colector.':
        'On release, the pilot cylinder opens the cylinder valves and the gas flows to the manifold.',
    'Los presostatos pueden vigilar la presión de la carga.': 'Pressure switches can monitor the charge pressure.',
    'Sala 4': 'Room 4', 'Actuador': 'Actuator', 'Palanca de accionamiento manual': 'Manual release lever',
    'El gas, solo a la sala afectada': 'Gas only to the affected room',
    'Las válvulas direccionales envían el gas solo a la sala afectada: una batería protege varias salas.':
        'Directional valves send the gas only to the affected room: one bank protects several rooms.',
    'Cada válvula cuenta con palanca de accionamiento manual.': 'Each valve has a manual release lever.',
    'Difusor silencioso SALCXX': 'SALCXX silent nozzle',
    'El gas entra en la sala por los difusores silenciosos SALCXX, por debajo de 90 dB.':
        'The gas enters the room through SALCXX silent nozzles, below 90 dB.',
    'SOFTWARE DE DISEÑO': 'DESIGN SOFTWARE', 'Diseño acústico adaptado a cada CPD': 'Acoustic design for each data center',
    'Comparar y adaptar instalaciones': 'Compare and retrofit installations',
    'Diseño acústico · CPD': 'Acoustic design · Data center', 'Comparar configuraciones': 'Compare configurations',
    'Datos del CPD': 'Data center inputs', 'Geometría de la sala': 'Room geometry',
    'Equipos sensibles: discos duros': 'Sensitive equipment: hard drives', 'Ruido máximo admisible': 'Maximum admissible noise',
    'Resultados': 'Results', 'Nivel acústico final': 'Final sound level', 'Límite admisible': 'Admissible limit',
    'Por debajo del límite': 'Below the limit', 'Distancias de seguridad': 'Safety distances', 'Calculadas': 'Calculated',
    'Criterios de diseño': 'Design criteria', 'Validados': 'Validated',
    'El software analiza cada CPD, calcula los niveles acústicos finales y las distancias de seguridad, y valida los criterios de diseño.':
        'The software analyses each data center, calculates final sound levels and safety distances, and validates the design criteria.',
    'Sustitución de difusores': 'Nozzle replacement', 'Difusor tradicional  →  Difusor silencioso': 'Traditional nozzle  →  Silent nozzle',
    'Sustitución viable': 'Replacement feasible', 'Instalación existente': 'Existing installation',
    'Sin cálculos manuales': 'No manual calculations', 'Cálculo automático': 'Automatic calculation',
    'Solución documentada': 'Documented solution', 'Informe del proyecto': 'Project report',
    'Menos tiempo de diseño': 'Shorter design time', 'Menor riesgo en la implantación': 'Lower implementation risk',
    'Compara configuraciones y evalúa sustituir difusores tradicionales FEDRXX por silenciosos, sin cálculos manuales.':
        'It compares configurations and assesses replacing traditional FEDRXX nozzles with silent ones, with no manual calculations.',
    'Certificaciones': 'Certifications',
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
import mz_tools as MZ
from cpd_video import (W, H, SS, FPS, S, SW, ss, win, clamp, full, low, up, spray, Cloud, tag, subtitle, title, card, ca,
                       BG, BG_PLAIN, INK, INK2, RED, WHITE)

RS1 = B.SP + 'rs1/'
AS = B.SP + 'assets/siex/'
OW, OH = 1440, 1800
F_STAT2 = ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf', 52 * SS)
GASC = (120, 170, 225)


def _ld(n):
    if not os.path.exists(RS1 + n):
        n = 'gmed.png'
    return Image.open(RS1 + n).convert('RGBA')


def _ldj(n):
    if not os.path.exists(RS1 + n):
        n = 'gmed.json'
    return json.load(open(RS1 + n))


for s_ in ('gwide', 'gmed', 'gfloor'):
    B.SHOTS[s_] = (_ld(f'{s_}.png'), _ld(f'{s_}_led1.png') if os.path.exists(RS1 + f'{s_}_led1.png') else None, _ldj(f'{s_}.json'))
for s_ in ('gdoor', 'gnoz', 'groom', 'gcyl'):
    B.SHOTS[s_] = (_ld(f'{s_}.png'), None, _ldj(f'{s_}.json'))
B.SHOTS['gsite'] = (_ld('gsite.png'), _ld('gsite_led1.png') if os.path.exists(RS1 + 'gsite_led1.png') else None, _ldj('gsite.json'))
AS2 = B.SP + 'assets/siex2/'
ULFM = Image.open(AS2 + 'ul_fm_new.png').convert('RGBA')
ULV = Image.open(AS2 + 'ul_verified.png').convert('RGBA')
SYS = Image.open(AS2 + 'sys_iso_lab.png').convert('RGBA')
VALV = Image.open(AS2 + 'valves4.png').convert('RGBA')

# ---------------- logos ----------------
SXL = Image.open(AS + 'siex_logo.png').convert('RGBA')
UL = Image.open(AS + 'ul.png').convert('RGBA')
FM = Image.open(AS + 'fm.png').convert('RGBA')
CYL = Image.open(AS + 'cyl_bank.png').convert('RGBA')


def lockup(h_sx=52):
    """solo marca SIEX"""
    return SXL.resize((S(int(SXL.width * h_sx / SXL.height)), S(h_sx)), Image.LANCZOS)


B.LOCK = lockup(84)
B.LOCK_S = lockup(30)
LOCK_S = B.LOCK_S
OUTRO_TXT = 'Ingeniería contra incendios para infraestructuras críticas'
OUTRO_URL = 'www.siex2001.com'


def put_logo(img, logo, box, a):
    x0, y0, x1, y1 = box
    k = min((x1 - x0) / logo.width, (y1 - y0) / logo.height)
    im = logo.resize((S(int(logo.width * k)), S(int(logo.height * k))), Image.LANCZOS)
    img.alpha_composite(B.fade_img(im, a), (int(S((x0 + x1) / 2) - im.width / 2), int(S((y0 + y1) / 2) - im.height / 2)))


# ---------------- herramientas ----------------
def zoom_about(img, fx, fy, s, fill=(255, 255, 255, 255)):
    if abs(s - 1) < 1e-4:
        return img
    c = (1 - 1 / s)
    return img.transform(img.size, Image.AFFINE, (1 / s, 0, S(fx) * c, 0, 1 / s, S(fy) * c), resample=Image.BILINEAR, fillcolor=fill)


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


def persp_coeffs(dst, src):
    A_, b_ = [], []
    for (x, y), (u, v) in zip(dst, src):
        A_.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b_.append(u)
        A_.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b_.append(v)
    return np.linalg.solve(np.array(A_, float), np.array(b_, float)).tolist()


def warp_onto(img, src, quad):
    """pega la imagen src deformada sobre el cuadrilátero quad (pantalla 1x, orden TL TR BR BL)"""
    dst = [(S(x), S(y)) for x, y in quad]
    w, h = src.size
    co = persp_coeffs(dst, [(0, 0), (w, 0), (w, h), (0, h)])
    out = src.transform(img.size, Image.PERSPECTIVE, co, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    img.alpha_composite(out)


FB = '/usr/share/fonts/opentype/inter/'


def text_panel(txt, w, h, bg, fg, fsize, sub=None):
    im = Image.new('RGBA', (w, h), bg)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FB + 'InterDisplay-Bold.otf', fsize)
    t = TR(txt)
    while f.getlength(t) > w * 0.92 and fsize > 8:
        fsize -= 2; f = ImageFont.truetype(FB + 'InterDisplay-Bold.otf', fsize)
    if sub:
        fs = ImageFont.truetype(FB + 'InterDisplay-Bold.otf', int(fsize * 1.9))
        d.text((w / 2 - f.getlength(t) / 2, h * 0.12), t, font=f, fill=fg)
        st = TR(sub)
        d.text((w / 2 - fs.getlength(st) / 2, h * 0.38), st, font=fs, fill=fg)
    else:
        d.text((w / 2 - f.getlength(t) / 2, h / 2 - fsize * 0.62), t, font=f, fill=fg)
    return im


def chip(img, x, y, txt, a, col=RED, icon=True):
    if not B.UI[0] or a <= 0.01:
        return
    im = B.uiimg(img)
    d = ImageDraw.Draw(im)
    tw = B.F_SMB.getlength(TR(txt)) / SS
    w = tw + 26 + (30 if icon else 0)
    dy = 10 * (1 - a)
    d.rounded_rectangle([S(x), S(y + dy), S(x + w), S(y + 40 + dy)], radius=S(20), fill=ca(WHITE, 0.95 * a), outline=ca(INK, 0.3 * a), width=SW(1))
    if icon:
        cx, cy = x + 22, y + 20 + dy
        d.ellipse([S(cx - 9), S(cy - 9), S(cx + 9), S(cy + 9)], fill=ca(col, a))
        d.line([(S(cx - 4.5), S(cy)), (S(cx - 1), S(cy + 4)), (S(cx + 5), S(cy - 4))], fill=ca(WHITE, a), width=SW(2.2))
    d.text((S(x + 13 + (30 if icon else 0)), S(y + 8 + dy)), txt, font=B.F_SMB, fill=ca(INK, a))


NSTEPS = 8


def step_header(d, n, name, sub, a):
    if not B.UI[0] or a <= 0.01:
        return
    d = B._ud(d)
    d.text((S(70), S(112)), f'{n:02d} · {name}', font=B.F_T1, fill=ca(INK, a))
    d.text((S(70), S(156)), sub, font=B.F_T2, fill=ca(INK, a))
    x = 70
    for i in range(NSTEPS):
        col = RED if i + 1 == n else (INK if i + 1 < n else (215, 217, 220))
        d.rounded_rectangle([S(x), S(206), S(x + 40), S(212)], radius=S(3), fill=ca(col, a))
        x += 47


def step(d, n, name, sub, a):
    step_header(d, n, name, sub, a)


def ring(d, p, r, a, col=RED, w=3):
    if a <= 0.01:
        return
    d.ellipse([S(p[0] - r), S(p[1] - r), S(p[0] + r), S(p[1] + r)], outline=ca(col, a), width=SW(w))


def gas_jets(od, fd, clouds, t, pairs, alpha, scale=1.0, col=GASC, speed=1.0):
    if alpha <= 0.01 or t <= 0:
        return
    for j, (a_, b_) in enumerate(pairs):
        dx, dy = b_[0] - a_[0], b_[1] - a_[1]
        n_ = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n_, dy / n_
        Lj = 230 * scale
        for i in range(10):
            ph = (t * 1.6 + i / 10 + j * 0.137) % 1
            if t * 1.6 < ph:
                continue
            x = a_[0] + ux * Lj * ph + math.sin(i * 3.1 + j) * 6 * ph * scale
            y = a_[1] + uy * Lj * ph + math.cos(i * 2.3 + j) * 6 * ph * scale
            r = (5 + 34 * ph) * scale / 4
            al = int(150 * alpha * (1 - ph) ** 1.3 * min(1, ph * 6))
            fd.ellipse([x / 4 - r, y / 4 - r, x / 4 + r, y / 4 + r], fill=col + (al,))


# ---------------- escenas ----------------
def sc_cert(t, L, img):
    v, js = B.draw_shot(img, 'gsite', t, 1.0 + 0.05 * ss(0, L, t), ss(0, 0.5, t), dy=110)
    d = ImageDraw.Draw(img)
    title(d, 'CENTROS DE DATOS', 'Agentes limpios de inundación total', ss(0.2, 0.7, t))
    a = ss(0.7, 1.3, t)
    if a > 0 and B.UI[0]:
        dy = 18 * (1 - a)
        box = (600, 250 + dy, 1010, 450 + dy)
        ui = B.uiimg(img)
        card(img, box, a)
        du = ImageDraw.Draw(ui)
        du.text((S(box[0] + 22), S(box[1] + 14)), 'Certificaciones', font=B.F_SM, fill=ca(INK2, a))
        put_logo(ui, ULFM, (box[0] + 22, box[1] + 46, box[2] - 22, box[3] - 16), a)
    d = ImageDraw.Draw(img)
    subtitle(d, 'Sistemas SIEX de agentes limpios de inundación total, con certificaciones UL y FM.', win(t, 0.6, L))


T_D1, T_D2 = 2.6, 3.5


def sc_detect(t, L, img):
    v, js = B.draw_shot(img, 'gmed', t, 1.0 + 0.06 * ss(0, L, t), ss(0, 0.5, t), window=True)
    lvl = ss(0.4, 3.0, t)
    p, pt = V.fire_fx(img, v, js, t, lvl, 46 * ss(1.4, 3.2, t), ss(0.6, 2.6, t) * 1.1, t)
    d = ImageDraw.Draw(img)
    dets = [v(q) for q in js['det_fire']]
    for k, (dp, td) in enumerate(zip(dets, (T_D1, T_D2))):
        on = ss(td, td + 0.15, t)
        blink = 0.5 + 0.5 * math.sin(t * 9)
        glow, gd = low()
        a_led = on * (0.75 + 0.25 * blink) + (1 - on) * (0.25 if (t * 1.3 + k) % 1 < 0.12 else 0)
        if a_led > 0.02:
            r = 16
            gd.ellipse([dp[0] / 4 - r / 4 * 2, dp[1] / 4 - r / 4 * 2, dp[0] / 4 + r / 4 * 2, dp[1] / 4 + r / 4 * 2], fill=(255, 40, 30, int(200 * a_led)))
            img.alpha_composite(up(glow, 3))
            d = ImageDraw.Draw(img)
            d.ellipse([S(dp[0] - 4), S(dp[1] - 4), S(dp[0] + 4), S(dp[1] + 4)], fill=ca((255, 60, 40), a_led))
        if on > 0:
            pr = ((t - td) * 1.3) % 1
            ring(d, dp, 10 + 40 * pr, on * (1 - pr) * 0.9)
    d = ImageDraw.Draw(img)
    step(d, 1, 'DETECCIÓN', 'Detección temprana del humo', ss(0.2, 0.7, t))
    tag(d, pt[0] + 60, pt[1] + 150, 'Foco en rack', win(t, 1.0, L - 0.3), (pt[0], pt[1] + 20))
    tag(d, 70, 300, 'Detector 1 · alarma', win(t, T_D1 + 0.1, L - 0.2), dets[0])
    tag(d, 600, 300, 'Detector 2 · confirmación', win(t, T_D2 + 0.1, L - 0.2), dets[1])
    subtitle(d, 'Un rack se sobrecalienta y empieza a generar humo.', win(t, 0.5, T_D1))
    subtitle(d, 'Los detectores lo identifican en su fase más temprana.', win(t, T_D1, L))


def countdown_card(img, t, a, box, t0, dur=4.6):
    if not B.UI[0] or a <= 0.01:
        return
    img = B.uiimg(img)
    card(img, box, a)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    cx, cy, R = (x0 + x1) / 2, y0 + 118, 70
    p = clamp((t - t0) / dur)
    n = int(math.ceil(30 * (1 - p)))
    d.ellipse([S(cx - R), S(cy - R), S(cx + R), S(cy + R)], outline=ca((222, 224, 227), a), width=SW(9))
    if p < 1:
        d.arc([S(cx - R), S(cy - R), S(cx + R), S(cy + R)], start=-90, end=-90 + 360 * (1 - p), fill=ca(RED, a), width=SW(9))
    txt = f'{n}' if p < 1 else '0'
    f = B.F_STAT
    d.text((S(cx) - f.getlength(txt) / 2, S(cy - 40)), txt, font=f, fill=ca(INK, a))
    lb = 'Retardo de descarga'
    d.text((S(cx) - B.F_SM.getlength(lb) / 2, S(y0 + 14)), lb, font=B.F_SM, fill=ca(INK2, a))
    st = 'PREALARMA' if p < 1 else 'DESCARGA'
    d.text((S(cx) - B.F_SMB.getlength(st) / 2, S(cy + 82)), st, font=B.F_SMB, fill=ca(RED, a))


T_AL = 0.4


def sc_alarm(t, L, img):
    v, js = B.draw_shot(img, 'gdoor', t, 1.14 + 0.04 * ss(0, L, t), ss(0, 0.5, t), dy=40, window=True)
    on = ss(T_AL, T_AL + 0.2, t)
    fl = 0.5 + 0.5 * math.sin(t * 7.5)
    # rótulo luminoso
    q = [v(p) for p in js['sign_q']]
    lit = on * (0.65 + 0.35 * fl)
    sign_off = text_panel('EXTINCIÓN DISPARADA', 880, 240, (236, 236, 233, 255), (180, 182, 186, 255), 92)
    warp_onto(img, sign_off, q)
    if lit > 0.02:
        s_on = text_panel('EXTINCIÓN DISPARADA', 880, 240, (220, 20, 30, 255), (255, 255, 255, 255), 92)
        warp_onto(img, B.fade_img(s_on, lit), q)
        glow, gd = low()
        cx = sum(p[0] for p in q) / 4; cy = sum(p[1] for p in q) / 4
        gd.ellipse([cx / 4 - 40, cy / 4 - 18, cx / 4 + 40, cy / 4 + 18], fill=(255, 40, 40, int(70 * lit)))
        img.alpha_composite(up(glow, 8))
    # pantalla de la central
    qs = [v(p) for p in js['scr_q']]
    p_cd = clamp((t - (T_AL + 0.6)) / 4.6)
    scr_txt = ('PREALARMA', f'{int(math.ceil(30 * (1 - p_cd)))} s') if p_cd < 1 else ('DESCARGA', '')
    scr = text_panel(scr_txt[0], 400, 240, (30, 60, 150, 255), (255, 255, 255, 255), 52, sub=scr_txt[1] or None)
    warp_onto(img, B.fade_img(scr, on), qs)
    # flash
    fp = v(js['flash'])
    if on > 0:
        glow, gd = low()
        a_ = on * (0.4 + 0.6 * (fl > 0.5))
        for rr, al in ((70, 60), (36, 140)):
            gd.ellipse([fp[0] / 4 - rr / 4, fp[1] / 4 - rr / 4, fp[0] / 4 + rr / 4, fp[1] / 4 + rr / 4], fill=(255, 50, 40, int(al * a_)))
        img.alpha_composite(up(glow, 5))
    d = ImageDraw.Draw(img)
    step(d, 2, 'ALARMA', 'Prealarma y evacuación', ss(0.2, 0.7, t))
    tag(d, 70, 960, 'Central de extinción', win(t, 0.9, L - 0.2), v(js['panel']))
    tag(d, 640, 330, 'Sirena y flash', win(t, 1.2, L - 0.2), fp)
    tag(d, 70, 330, 'Rótulo de extinción', win(t, 1.5, L - 0.2), q[0])
    countdown_card(img, t, ss(T_AL + 0.3, T_AL + 0.8, t), (740, 760, 1010, 1060), T_AL + 0.6)
    for k, (txt, tc) in enumerate((('Evacuación del personal', 2.4), ('Climatización detenida', 3.0))):
        chip(img, 70 + k * 300, 1060, txt, win(t, tc, L - 0.1))
    d = ImageDraw.Draw(img)
    subtitle(d, 'Al confirmarse el incendio, la central activa la alarma y la cuenta atrás.', win(t, 0.5, 2.4))
    subtitle(d, 'El personal evacúa la sala y la climatización se detiene.', win(t, 2.4, L))


# ---------------- disparo: sala 3D -> foto de la batería ----------------
TZ = 3.4; DZP = 0.8


def route_paths(v, js):
    feed = [v(p) for p in js['gp_feed']] + [v(js['gp_main'][1])]
    brs = [[v(js['gp_br'][k]), v(js['gp_br'][k + 3])] for k in range(3)]
    return feed, brs


def gas_route(img, v, js, t, a, t0=0.0, dots=True):
    """resalta la red de tuberías desde la sala de cilindros hasta los difusores del CPD"""
    if a <= 0.01:
        return
    feed, brs = route_paths(v, js)
    glow, gd = low()
    lay, ld = full()
    k = ss(t0, t0 + 1.2, t)
    for path in [feed] + brs:
        pts = path if path is feed else path
        gd.line([(x / 4, y / 4) for x, y in pts], fill=(230, 30, 40, int(150 * a)), width=4, joint='curve')
        ld.line([(S(x), S(y)) for x, y in pts], fill=ca(RED, a), width=SW(3.2), joint='curve')
    img.alpha_composite(up(glow, 4)); img.alpha_composite(lay)
    if dots:
        d = ImageDraw.Draw(img)
        flow_dots(d, feed, t - t0, a * k, n=16, speed=0.18, col=(255, 255, 255))
        for b in brs:
            flow_dots(d, b, t - t0 - 0.8, a * ss(t0 + 0.8, t0 + 1.6, t), n=10, speed=0.22, col=(255, 255, 255))
        for i, q in enumerate(js['nozzles']):
            p = v(q)
            pr = ((t - t0 - 1.4 + i * 0.07) * 1.0) % 1
            ring(d, p, 4 + 16 * pr, a * (1 - pr) * ss(t0 + 1.4, t0 + 1.8, t), w=2)




def sc_cylroom(t, L, img):
    """vista del conjunto (CPD + sala aledaña) -> acercamiento continuo a la sala de cilindros"""
    p = clamp((t - (TZ - DZP)) / (2 * DZP))
    jsS = B.SHOTS['gsite'][2]; jsC = B.SHOTS['gcyl'][2]
    zs = 1.0 + 0.04 * ss(0, TZ, min(t, TZ))
    vS = B.View(zs, 0, 110)
    layS = layC = None
    if t < TZ + DZP:
        layS = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        B.draw_shot(layS, 'gsite', t, zs, 1.0, dy=110, window=True)
        fc = vS(jsS['cylroom'])
        ua = 1 - ss(TZ - DZP, TZ - DZP + 0.2, t)
        gas_route(layS, vS, jsS, t, ss(0.6, 1.0, t) * ua, t0=0.8)
        d = ImageDraw.Draw(img)
        tag(d, 90, 330, 'Centro de datos', win(t, 0.3, L) * ua, vS(jsS['fire_top']))
        tag(d, 640, 960, 'Sala de cilindros', win(t, 0.6, L) * ua, fc)
        feed, _ = route_paths(vS, jsS)
        tag(d, 600, 330, 'Red de tuberías hasta los difusores', win(t, 1.2, L) * ua, feed[2])
    if t > TZ - DZP:
        zc = 1.0 + 0.05 * ss(TZ, L, t)
        vC = B.View(zc, 0, 120)
        layC = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        B.draw_shot(layC, 'gcyl', t, zc, 1.0, dy=120, window=True)
        fpts = [vC(p_) for p_ in jsC['gp_feed']]
        aa = ss(TZ + 0.3, TZ + 0.8, t)
        if aa > 0.01:
            glow, gd = low(); lay2, ld2 = full()
            gd.line([(x / 4, y / 4) for x, y in fpts], fill=(230, 30, 40, int(150 * aa)), width=5)
            ld2.line([(S(x), S(y)) for x, y in fpts], fill=ca(RED, aa), width=SW(3.5))
            layC.alpha_composite(up(glow, 4)); layC.alpha_composite(lay2)
            flow_dots(ImageDraw.Draw(layC), fpts, t - TZ - 0.3, aa, n=10, speed=0.3, col=(255, 255, 255))
        d = ImageDraw.Draw(img)
        tag(d, 70, 330, 'Hacia los difusores del CPD', win(t, TZ + 0.6, L - 0.1), fpts[-1])
        tag(d, 70, 960, 'Batería principal', win(t, TZ + 0.5, L - 0.1), vC(jsC['main_bank']))
        T_R = TZ + 2.6
        tag(d, 640, 1010, 'Batería de reserva', win(t, T_R, L - 0.1), vC(jsC['res_bank']))
        if t > T_R:
            pr = ((t - T_R) * 1.1) % 1
            ring(d, vC(jsC['res_bank']), 20 + 50 * pr, (1 - pr) * ss(T_R, T_R + 0.4, t))
        tag(d, 640, 330, 'Válvulas direccionales', win(t, TZ + 1.0, L - 0.1), vC(jsC['dirv'][2]))
        chip(img, 70, 1060, 'Anclaje a la pared', win(t, TZ + 1.8, L - 0.1))
    if layS is not None and layC is not None:
        fA, fB, R = MZ.matched(fc, MZ.kp_screen('gsite', vS), MZ.kp_screen('gcyl', vC))
        lay, _ = MZ.zoom_pair(layS, layC, p, fA, fB, R, clip=True)
        img.alpha_composite(lay)
    else:
        img.alpha_composite(layS if layS is not None else layC)
    d = ImageDraw.Draw(img)
    step(d, 3, 'SALA DE CILINDROS', 'Aledaña al centro de datos', ss(0.2, 0.7, t))
    subtitle(d, 'En una sala aledaña al CPD, las baterías de cilindros se anclan a la pared.', win(t, 0.5, TZ + 2.6))
    subtitle(d, 'La batería de reserva mantiene la protección durante el mantenimiento.', win(t, TZ + 2.6, L))


# coordenadas en la foto del sistema (px de SYS)
SYS_PILOT = (1206, 870); SYS_PILOTB = (1196, 1045)
SYS_MAN = (543, 382); SYS_HOSE = (362, 540); SYS_CU = (1156, 527); SYS_DV = (1528, 543)
SYS_PATH = [(663, 362), (1226, 262), (1236, 714), (1990, 613)]


def photo(img, im, k, cx, cy, kref=None):
    B.place_scaled(img, im, k, cx, cy, kref=kref)
    return lambda px, py: (cx + (px - im.width / 2) * k, cy + (py - im.height / 2) * k)


def along(path, u):
    segs = [(a, b, math.hypot(b[0] - a[0], b[1] - a[1])) for a, b in zip(path[:-1], path[1:])]
    tot = sum(sg[2] for sg in segs); dd = u * tot
    for a, b, l in segs:
        if dd <= l:
            k = dd / l if l else 0
            return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        dd -= l
    return path[-1]


def flow_dots(d, path, t, a, n=14, speed=0.35, col=(70, 140, 220)):
    if a <= 0.01:
        return
    for i in range(n):
        u = (t * speed + i / n) % 1
        p = along(path, u)
        r = 6
        d.ellipse([S(p[0] - r), S(p[1] - r), S(p[0] + r), S(p[1] + r)], fill=ca(col, a * 0.9), outline=ca(WHITE, a), width=SW(1.5))


T_FIRE = 0.6


def sc_release(t, L, img):
    k = 0.44 + 0.015 * ss(0, L, t)
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    P = photo(lay, SYS, k, 560, 680, kref=0.44)
    img.alpha_composite(V.mclip(B.fade_img(lay, 1.0 if B.NOFADE[0] else ss(0, 0.5, t))))
    d = ImageDraw.Draw(img)
    pp = P(*SYS_PILOT)
    if t > T_FIRE:
        pr = ((t - T_FIRE) * 1.3) % 1
        ring(d, pp, 14 + 44 * pr, (1 - pr) * ss(T_FIRE, T_FIRE + 0.2, t))
    flow_dots(d, [P(*q) for q in SYS_PATH], t - 1.6, ss(1.6, 2.0, t))
    tag(d, 640, 900, 'Cilindro piloto', win(t, 0.4, L - 0.1), P(*SYS_PILOTB))
    tag(d, 70, 300, 'Colector', win(t, 1.4, L - 0.1), P(*SYS_MAN))
    tag(d, 70, 960, 'Latiguillos', win(t, 1.8, L - 0.1), P(*SYS_HOSE))
    tag(d, 640, 300, 'Línea de pilotaje', win(t, 1.0, L - 0.1), P(*SYS_CU))
    charge_card(img, t, ss(2.6, 3.1, t), (640, 990, 1010, 1100), 1.6)
    d = ImageDraw.Draw(img)
    step(d, 4, 'DISPARO', 'Cilindro piloto y colector', ss(0.2, 0.7, t))
    subtitle(d, 'Al disparar, el cilindro piloto abre las válvulas de los cilindros y el gas llega al colector.', win(t, 0.5, 3.4))
    subtitle(d, 'Los presostatos pueden vigilar la presión de la carga.', win(t, 3.4, L))


def charge_card(img, t, a, box, tr):
    if not B.UI[0] or a <= 0.01:
        return
    img = B.uiimg(img)
    card(img, box, a)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    d.text((S(x0 + 20), S(y0 + 14)), 'Presión de la carga', font=B.F_SMB, fill=ca(INK, a))
    val = 1 - 0.85 * ss(tr, tr + 5, t)
    yy = y0 + 56
    bx0, bx1 = x0 + 20, x1 - 24
    d.rounded_rectangle([S(bx0), S(yy + 8), S(bx1), S(yy + 20)], radius=S(6), fill=ca((222, 224, 227), a))
    d.rounded_rectangle([S(bx0), S(yy + 8), S(bx0 + (bx1 - bx0) * val), S(yy + 20)], radius=S(6), fill=ca(RED, a))
    st = 'Descargando' if t > tr else ''
    if st:
        d.text((S(x1 - 20) - B.F_SM.getlength(st), S(y0 + 16)), st, font=B.F_SM, fill=ca(RED, a * (0.6 + 0.4 * math.sin(t * 6))))


# válvulas direccionales (px de VALV)
V_RISERS = [658, 1186, 1704, 2219]
V_TEE2 = (1186, 1330); V_SOL2 = (1008, 470); V_LEV2 = (1122, 1040)
T_OPEN = 1.0; T_LEV = 3.6


def sc_valves(t, L, img):
    k = 0.40 + 0.012 * ss(0, L, t)
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    P = photo(lay, VALV, k, 540, 735, kref=0.40)
    img.alpha_composite(V.mclip(B.fade_img(lay, 1.0 if B.NOFADE[0] else ss(0, 0.5, t))))
    d = ImageDraw.Draw(img)
    # salas de destino
    for j, xr in enumerate(V_RISERS):
        tp = P(xr, 0)
        on = j == 1
        aj = ss(0.3 + j * 0.12, 0.7 + j * 0.12, t)
        if aj > 0.01 and B.UI[0]:
            du = ImageDraw.Draw(B.uiimg(img))
            txt = TR(f'Sala {j + 1}')
            tw = B.F_SMB.getlength(txt) / SS + 28
            act = ss(T_OPEN, T_OPEN + 0.3, t) if on else 0
            fill = tuple(int(WHITE[c] + (RED[c] - WHITE[c]) * act) for c in range(3))
            fg = tuple(int(INK[c] + (WHITE[c] - INK[c]) * act) for c in range(3))
            x0 = tp[0] - tw / 2; y0 = 262
            du.rounded_rectangle([S(x0), S(y0), S(x0 + tw), S(y0 + 38)], radius=S(19), fill=ca(fill, aj), outline=ca(INK, 0.3 * aj), width=SW(1))
            du.text((S(x0 + 14), S(y0 + 7)), txt, font=B.F_SMB, fill=ca(fg, aj))
            du.line([(S(tp[0]), S(y0 + 38)), (S(tp[0]), S(tp[1] + 6))], fill=ca(INK, 0.35 * aj), width=SW(1.5))
    # apertura de la válvula de la sala 2 y paso del gas
    sp = P(*V_SOL2)
    if t > T_OPEN:
        pr = ((t - T_OPEN) * 1.3) % 1
        ring(d, sp, 14 + 40 * pr, (1 - pr) * ss(T_OPEN, T_OPEN + 0.2, t) * (1 - ss(T_LEV - 0.4, T_LEV, t)))
    flow_dots(d, [P(*V_TEE2), P(V_RISERS[1], 0)], t - T_OPEN - 0.3, ss(T_OPEN + 0.3, T_OPEN + 0.7, t), n=10, speed=0.5)
    tag(d, 70, 360, 'Actuador', win(t, T_OPEN + 0.2, L - 0.1), sp)
    lp = P(*V_LEV2)
    if t > T_LEV:
        pr = ((t - T_LEV) * 1.2) % 1
        ring(d, lp, 14 + 40 * pr, (1 - pr) * ss(T_LEV, T_LEV + 0.2, t))
    tag(d, 70, 1020, 'Palanca de accionamiento manual', win(t, T_LEV, L - 0.1), lp)
    d = ImageDraw.Draw(img)
    step(d, 5, 'VÁLVULAS DIRECCIONALES', 'El gas, solo a la sala afectada', ss(0.2, 0.7, t))
    subtitle(d, 'Las válvulas direccionales envían el gas solo a la sala afectada: una batería protege varias salas.', win(t, 0.5, T_LEV))
    subtitle(d, 'Cada válvula cuenta con palanca de accionamiento manual.', win(t, T_LEV, L))


CL_NOZ = [Cloud(400 + i, 70, 0.0, 9.0, (0.35, 0.8), 0.10, (300, 520)) for i in range(26)]
CL_END = [Cloud(480 + i, 600, 0.0, 9.0, (0.5, 1.2), 0.30, (260, 460)) for i in range(2)]
T_GAS = 0.8


def sc_nozzle(t, L, img):
    v, js = B.draw_shot(img, 'gnoz', t, 1.0 + 0.05 * ss(0, L, t), ss(0, 0.5, t), window=True)
    over, od = full(); fog, fd = low()
    a = ss(T_GAS, T_GAS + 0.4, t)
    pairs = [(v(a_), v(b_)) for a_, b_ in js['orif']]
    side = pairs[0:6] + pairs[12:18]; ends = pairs[-2:]
    gas_jets(od, fd, None, t - T_GAS, side, a, 0.9)
    gas_jets(od, fd, None, t - T_GAS, ends, a, 1.8)
    img.alpha_composite(V.mclip(up(fog, 3))); img.alpha_composite(V.mclip(over))
    d = ImageDraw.Draw(img)
    step(d, 6, 'DESCARGA', 'Difusor silencioso SALCXX', ss(0.2, 0.7, t))
    tag(d, 70, 860, 'Orificios de descarga', win(t, 1.0, L - 0.2), v(js['holes']))
    db_card(img, t, ss(1.4, 1.9, t), (590, 250, 1010, 470))
    d = ImageDraw.Draw(img)
    subtitle(d, 'El gas entra en la sala por los difusores silenciosos SALCXX, por debajo de 90 dB.', win(t, 0.5, L))


def db_card(img, t, a, box):
    if not B.UI[0] or a <= 0.01:
        return
    img = B.uiimg(img)
    card(img, box, a)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    d.text((S(x0 + 20), S(y0 + 14)), 'Nivel sonoro', font=B.F_SM, fill=ca(INK2, a))
    d.text((S(x0 + 20), S(y0 + 40)), '< 90 dB', font=B.F_STAT, fill=ca(RED, a))
    put_logo(img, ULV, (x1 - 128, y0 + 18, x1 - 16, y0 + 112), a)
    n = 12
    for i in range(n):
        lv = 0.35 + 0.25 * math.sin(t * 9 + i * 1.7) * math.sin(t * 4.3 + i)
        hh = 14 + 46 * clamp(lv + 0.1 * (i % 3))
        xx = x0 + 22 + i * 19
        col = INK if i < 9 else RED
        d.rounded_rectangle([S(xx), S(y1 - 20 - hh), S(xx + 11), S(y1 - 20)], radius=S(3), fill=ca(col, a * (0.85 if i < 9 else 0.35)))


CL_FLN = [Cloud(500 + i, 120, 0.0, 6.0, (0.6, 1.2), 0.25, (90, 170)) for i in range(40)]
T_FL0, T_FL1 = 0.3, 5.2


def lerp(a, b, k):
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


def hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def sc_flood(t, L, img):
    v, js = B.draw_shot(img, 'gfloor', t, 1.0 + 0.04 * ss(0, L, t), ss(0, 0.5, t), window=True)
    lvl = 1 - ss(1.0, 4.6, t)
    if lvl > 0.01:
        V.fire_fx(img, v, js, t + 6, lvl, 40 * lvl, lvl * 0.8, t + 6)
    over, od = full(); fog, fd = low()
    a = ss(0.0, 0.4, t) * (1 - ss(4.5, 6.5, t))
    pairs = []
    for e in js['noz_ends']:
        c = ((e[0][0] + e[1][0]) / 2, (e[0][1] + e[1][1]) / 2)
        pairs += [(v(e[0]), v(lerp(c, e[0], 3.0))), (v(e[1]), v(lerp(c, e[1], 3.0)))]
    for k in range(2):
        e = js.get(f'uf_ends{k}')
        if e:
            c = ((e[0][0] + e[1][0]) / 2, (e[0][1] + e[1][1]) / 2)
            pairs += [(v(e[0]), v(lerp(c, e[0], 3.0))), (v(e[1]), v(lerp(c, e[1], 3.0)))]
    gas_jets(od, fd, None, t, pairs, a, 0.45)
    img.alpha_composite(V.mclip(up(fog, 6))); img.alpha_composite(V.mclip(over))
    # volumen inundado
    h = ease_out(ss(T_FL0, T_FL1, t), 1.6)
    if h > 0.003:
        bot = [v(p) for p in js['room']]
        top = [v(p) for p in js['room_top']]
        lv = [lerp(b, tp, h) for b, tp in zip(bot, top)]
        lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        dl.polygon([(S(x), S(y)) for x, y in hull(bot + lv)], fill=(110, 165, 225, 62))
        dl.polygon([(S(x), S(y)) for x, y in lv], fill=(140, 190, 240, 58))
        dl.line([(S(x), S(y)) for x, y in lv + [lv[0]]], fill=(70, 130, 205, 190), width=SW(3))
        lay = lay.filter(ImageFilter.GaussianBlur(SS * 1.2))
        img.alpha_composite(V.mclip(lay))
    d = ImageDraw.Draw(img)
    step(d, 7, 'INUNDACIÓN TOTAL', 'Sobre y bajo el suelo técnico', ss(0.2, 0.7, t))
    noz = [v(q) for q in js['nozzles']]
    noz = [q for q in noz if 280 < q[1] < 1000]
    if noz:
        tag(d, 640, 300, 'Difusores de sala', win(t, 0.6, 4.4), min(noz, key=lambda q: q[1]))
    if js.get('uf_noz'):
        tag(d, 70, 1000, 'Difusores bajo suelo', win(t, 1.0, 4.4), v(js['uf_noz'][0]))
    conc_card(img, t, ss(0.8, 1.3, t), (740, 760, 1010, 900))
    d = ImageDraw.Draw(img)
    subtitle(d, 'El agente inunda todo el recinto, sobre y bajo el suelo técnico, hasta la concentración de extinción.', win(t, 0.5, L - 1.8))
    subtitle(d, 'Sin agua y sin residuos.', win(t, L - 1.8, L))


def conc_card(img, t, a, box):
    if not B.UI[0] or a <= 0.01:
        return
    img = B.uiimg(img)
    card(img, box, a)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    k = ease_out(ss(T_FL0, T_FL1, t), 1.6)
    d.text((S(x0 + 20), S(y0 + 14)), 'Concentración de diseño', font=B.F_SM, fill=ca(INK2, a))
    pct = f'{int(round(100 * k))} %'
    d.text((S(x0 + 20), S(y0 + 40)), pct, font=B.F_T1, fill=ca(INK, a))
    bx0, bx1, by = x0 + 20, x1 - 20, y1 - 34
    d.rounded_rectangle([S(bx0), S(by), S(bx1), S(by + 12)], radius=S(6), fill=ca((222, 224, 227), a))
    d.rounded_rectangle([S(bx0), S(by), S(bx0 + (bx1 - bx0) * max(k, 0.03)), S(by + 12)], radius=S(6), fill=ca(RED, a))
    if k > 0.99:
        st = 'Alcanzada'
        d.text((S(x1 - 20) - B.F_SMB.getlength(st), S(y0 + 46)), st, font=B.F_SMB, fill=ca(RED, a))


def sc_ext(t, L, img):
    v, js = B.draw_shot(img, 'gsite', t, 1.0 + 0.04 * ss(0, L, t), ss(0, 0.5, t), dy=110)
    haze = 1 - ss(0.3, 3.5, t)
    if haze > 0.01:
        bot = [v(p) for p in js['room']]; top = [v(p) for p in js['room_top']]
        lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        dl.polygon([(S(x), S(y)) for x, y in hull(bot + top)], fill=(120, 175, 230, int(46 * haze)))
        img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    step(d, 8, 'EXTINCIÓN', 'Vuelta a la actividad', ss(0.2, 0.7, t))
    for k, (txt, tc) in enumerate((('Sin agua', 1.2), ('Sin residuos', 1.6), ('Sin daños en los equipos', 2.0))):
        chip(img, 70, 900 + k * 52, txt, win(t, tc, L - 0.1))
    d = ImageDraw.Draw(img)
    subtitle(d, 'Fuego extinguido. Tras ventilar la sala, el centro de datos vuelve a la actividad, sin limpiezas ni daños.', win(t, 0.5, L))


def arrow(d, a, b, al, col=RED, w=3, head=12):
    if al <= 0.01:
        return
    d.line([(S(a[0]), S(a[1])), (S(b[0]), S(b[1]))], fill=ca(col, al), width=SW(w))
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - head * math.cos(ang - 0.45), b[1] - head * math.sin(ang - 0.45))
    p2 = (b[0] - head * math.cos(ang + 0.45), b[1] - head * math.sin(ang + 0.45))
    d.polygon([(S(b[0]), S(b[1])), (S(p1[0]), S(p1[1])), (S(p2[0]), S(p2[1]))], fill=ca(col, al))


# ---------------- software de diseño ----------------
FUI = '/usr/share/fonts/opentype/inter/'


def ui_font(n, px):
    return ImageFont.truetype(FUI + n, int(px * SS))


U_T = ui_font('Inter-SemiBold.otf', 19); U_S = ui_font('Inter-Regular.otf', 17); U_B = ui_font('Inter-Bold.otf', 19)
U_H = ui_font('InterDisplay-Bold.otf', 22)
GREEN = (30, 150, 90)


def app_window(img, a, title_txt):
    """ventana de la aplicación; devuelve área de contenido"""
    box = (60, 262, 1020, 1090)
    card(img, box, a, radius=14)
    d = ImageDraw.Draw(B.uiimg(img))
    x0, y0, x1, y1 = box
    d.rounded_rectangle([S(x0), S(y0), S(x1), S(y0 + 52)], radius=S(14), fill=ca(INK, a))
    d.rectangle([S(x0), S(y0 + 30), S(x1), S(y0 + 52)], fill=ca(INK, a))
    for i, c in enumerate(((236, 96, 90), (240, 190, 70), (90, 190, 110))):
        d.ellipse([S(x0 + 22 + i * 22), S(y0 + 20), S(x0 + 34 + i * 22), S(y0 + 32)], fill=ca(c, a))
    sx = SXL.resize((S(int(SXL.width * 22 / SXL.height)), S(22)), Image.LANCZOS)
    wl = Image.new('RGBA', sx.size, (0, 0, 0, 0)); wl.paste((255, 255, 255, 255), (0, 0), sx)
    B.uiimg(img).alpha_composite(B.fade_img(wl, a), (S(x0 + 110), S(y0 + 15)))
    d.text((S(x0 + 110) + sx.width + S(14), S(y0 + 15)), title_txt, font=U_T, fill=ca((220, 222, 225), a))
    return d, box


def check(d, x, y, a, ok=True):
    if a <= 0.01:
        return
    col = GREEN if ok else RED
    d.ellipse([S(x - 11), S(y - 11), S(x + 11), S(y + 11)], fill=ca(col, a))
    if ok:
        d.line([(S(x - 5), S(y)), (S(x - 1), S(y + 5)), (S(x + 6), S(y - 5))], fill=ca(WHITE, a), width=SW(2.4))
    else:
        d.line([(S(x - 5), S(y - 5)), (S(x + 5), S(y + 5))], fill=ca(WHITE, a), width=SW(2.4))
        d.line([(S(x - 5), S(y + 5)), (S(x + 5), S(y - 5))], fill=ca(WHITE, a), width=SW(2.4))


def plan_view(d, box, t, a, t0):
    """planta del CPD con difusores y distancias de seguridad"""
    x0, y0, x1, y1 = box
    d.rounded_rectangle([S(x0), S(y0), S(x1), S(y1)], radius=S(8), fill=ca((246, 247, 248), a), outline=ca((210, 212, 215), a), width=SW(1.5))
    w, h = x1 - x0, y1 - y0
    for r in range(3):
        ry = y0 + h * (0.22 + r * 0.28)
        d.rectangle([S(x0 + w * 0.12), S(ry), S(x0 + w * 0.88), S(ry + h * 0.1)], fill=ca((40, 42, 46), a))
    noz = [(x0 + w * (0.25 + 0.25 * i), y0 + h * (0.37 + 0.28 * j)) for i in range(3) for j in range(2)]
    for k, (nx, ny) in enumerate(noz):
        ak = a * ss(t0 + k * 0.12, t0 + 0.3 + k * 0.12, t)
        if ak <= 0.01:
            continue
        rr = (w * 0.11) * ss(t0 + 0.6 + k * 0.1, t0 + 1.4 + k * 0.1, t)
        if rr > 1:
            n = 28
            for q in range(0, n, 2):
                a1 = 2 * math.pi * q / n; a2 = 2 * math.pi * (q + 1) / n
                d.line([(S(nx + rr * math.cos(a1)), S(ny + rr * math.sin(a1))), (S(nx + rr * math.cos(a2)), S(ny + rr * math.sin(a2)))],
                       fill=ca(RED, ak * 0.8), width=SW(1.6))
        d.ellipse([S(nx - 6), S(ny - 6), S(nx + 6), S(ny + 6)], fill=ca(RED, ak))


def result_row(d, x, y, w, label, a, ok_a, value=None):
    d.text((S(x), S(y)), label, font=U_T, fill=ca(INK, a))
    if value:
        d.text((S(x), S(y + 26)), value, font=U_S, fill=ca(INK2, a))
    check(d, x + w - 14, y + 14, ok_a)


def level_bars(d, x, y, w, h, a, fills, labels, cols, lim_lbl):
    """barras verticales con línea de límite admisible"""
    lim_y = y + h * 0.38
    n = len(fills)
    bw = w / (n * 2 + 1)
    for i, (f, lb, c) in enumerate(zip(fills, labels, cols)):
        bx = x + bw * (1 + i * 2)
        top = y + h - h * f
        d.rounded_rectangle([S(bx), S(top), S(bx + bw), S(y + h)], radius=S(5), fill=ca(c, a))
        tw = U_S.getlength(lb) / SS
        d.text((S(bx + bw / 2 - tw / 2), S(y + h + 8)), lb, font=U_S, fill=ca(INK, a))
    xx = x
    while xx < x + w:
        d.line([(S(xx), S(lim_y)), (S(min(xx + 12, x + w)), S(lim_y))], fill=ca(INK, a), width=SW(2))
        xx += 20
    d.text((S(x + w - U_S.getlength(TR(lim_lbl)) / SS), S(lim_y - 26)), lim_lbl, font=U_S, fill=ca(INK, a))


def sc_soft1(t, L, img):
    a = ss(0.2, 0.7, t)
    d = ImageDraw.Draw(img)
    title(d, 'SOFTWARE DE DISEÑO', 'Diseño acústico adaptado a cada CPD', ss(0.2, 0.7, t))
    if B.UI[0] and a > 0.01:
        du, (x0, y0, x1, y1) = app_window(img, a, 'Diseño acústico · CPD')
        du.text((S(x0 + 34), S(y0 + 78)), 'Datos del CPD', font=U_H, fill=ca(INK, a))
        rows = [('Geometría de la sala', 0.8), ('Equipos sensibles: discos duros', 1.1), ('Ruido máximo admisible', 1.4)]
        for i, (lb, tt) in enumerate(rows):
            ai = a * ss(tt, tt + 0.3, t)
            yy = y0 + 122 + i * 46
            du.rounded_rectangle([S(x0 + 34), S(yy), S(x0 + 440), S(yy + 36)], radius=S(8), fill=ca((242, 243, 245), ai))
            du.text((S(x0 + 48), S(yy + 8)), lb, font=U_S, fill=ca(INK, ai))
            check(du, x0 + 420, yy + 18, ai)
        plan_view(du, (x0 + 34, y0 + 280, x0 + 440, y1 - 40), t, a, 1.8)
        du.text((S(x0 + 480), S(y0 + 78)), 'Resultados', font=U_H, fill=ca(INK, a))
        xr, wr = x0 + 480, x1 - x0 - 514
        fill = 0.52 * ss(2.4, 3.4, t)
        level_bars(du, xr + 20, y0 + 130, wr - 40, 250, a * ss(2.2, 2.6, t), [fill], ['SALCXX'], [INK], 'Límite admisible')
        du.text((S(xr), S(y0 + 122)), 'Nivel acústico final', font=U_T, fill=ca(INK, a * ss(2.2, 2.6, t)))
        result_row(du, xr, y0 + 470, wr, 'Nivel acústico final', a * ss(3.2, 3.5, t), a * ss(3.5, 3.7, t), 'Por debajo del límite')
        result_row(du, xr, y0 + 545, wr, 'Distancias de seguridad', a * ss(3.6, 3.9, t), a * ss(3.9, 4.1, t), 'Calculadas')
        result_row(du, xr, y0 + 620, wr, 'Criterios de diseño', a * ss(4.0, 4.3, t), a * ss(4.3, 4.5, t), 'Validados')
    d = ImageDraw.Draw(img)
    subtitle(d, 'El software analiza cada CPD, calcula los niveles acústicos finales y las distancias de seguridad, y valida los criterios de diseño.', win(t, 0.5, L))


def sc_soft2(t, L, img):
    a = 1.0 if B.NOFADE[0] else ss(0, 0.3, t)
    d = ImageDraw.Draw(img)
    title(d, 'SOFTWARE DE DISEÑO', 'Comparar y adaptar instalaciones', ss(0.0, 0.3, t))
    if B.UI[0]:
        du, (x0, y0, x1, y1) = app_window(img, a, 'Comparar configuraciones')
        du.text((S(x0 + 34), S(y0 + 78)), 'Sustitución de difusores', font=U_H, fill=ca(INK, a))
        f1 = 0.86 * ss(0.6, 1.6, t); f2 = 0.5 * ss(1.2, 2.2, t)
        level_bars(du, x0 + 60, y0 + 140, 520, 330, a, [f1, f2], ['FEDRXX', 'SALCXX'], [(160, 163, 168), RED], 'Límite admisible')
        du.text((S(x0 + 60), S(y0 + 520)), 'Difusor tradicional  →  Difusor silencioso', font=U_S, fill=ca(INK2, a))
        xr, wr = x0 + 640, x1 - x0 - 674
        items = [('Sustitución viable', 2.4, 'Instalación existente'), ('Sin cálculos manuales', 2.9, 'Cálculo automático'),
                 ('Solución documentada', 3.4, 'Informe del proyecto'), ('Menos tiempo de diseño', 3.9, 'Menor riesgo en la implantación')]
        for i, (lb, tt, sub) in enumerate(items):
            ai = a * ss(tt, tt + 0.3, t)
            yy = y0 + 140 + i * 92
            du.rounded_rectangle([S(xr), S(yy), S(xr + wr), S(yy + 76)], radius=S(10), fill=ca((246, 247, 248), ai), outline=ca((222, 224, 227), ai), width=SW(1))
            du.text((S(xr + 18), S(yy + 12)), lb, font=U_T, fill=ca(INK, ai))
            du.text((S(xr + 18), S(yy + 42)), sub, font=U_S, fill=ca(INK2, ai))
            check(du, xr + wr - 26, yy + 38, ai)
    d = ImageDraw.Draw(img)
    subtitle(d, 'Compara configuraciones y evalúa sustituir difusores tradicionales FEDRXX por silenciosos, sin cálculos manuales.', win(t, 0.0, L))


def sc_agents(t, L, img):
    a0 = ss(0, 0.5, t)
    k = 0.27 + 0.01 * ss(0, L, t)
    B.place_scaled(img, CYL, k, 790, 700, kref=0.27, alpha=a0)
    d = ImageDraw.Draw(img)
    title(d, 'AGENTES LIMPIOS', 'Gases inertes y FK-5-1-12', ss(0.2, 0.7, t))
    if B.UI[0]:
        ui = B.uiimg(img)
        a = ss(0.6, 1.1, t)
        box = (70, 290, 520, 720)
        card(ui, (box[0], box[1] + 14 * (1 - a), box[2], box[3] + 14 * (1 - a)), a)
        du = ImageDraw.Draw(ui)
        y = box[1] + 20 + 14 * (1 - a)
        du.text((S(box[0] + 24), S(y)), 'INERT SIEX', font=B.F_T2, fill=ca(RED, a))
        du.text((S(box[0] + 24), S(y + 40)), 'Obtenidos de la atmósfera', font=B.F_SM, fill=ca(INK2, a))
        rows = [('IG-01', 'Argón'), ('IG-100', 'Nitrógeno'), ('IG-55', '50% Argón · 50% Nitrógeno'), ('IG-541', '52% N₂ · 40% Ar · 8% CO₂')]
        for i, (g, dsc) in enumerate(rows):
            ai = a * ss(0.9 + i * 0.2, 1.3 + i * 0.2, t)
            yy = y + 86 + i * 56
            du.text((S(box[0] + 24), S(yy)), g, font=B.F_SMB, fill=ca(INK, ai))
            du.text((S(box[0] + 130), S(yy + 1)), dsc, font=B.F_SM, fill=ca(INK, ai))
            du.line([(S(box[0] + 24), S(yy + 42)), (S(box[2] - 24), S(yy + 42))], fill=ca((225, 227, 230), ai), width=SW(1))
        du.text((S(box[0] + 24), S(y + 322)), '150 · 200 · 300 bar', font=B.F_SMB, fill=ca(RED, a * ss(1.8, 2.2, t)))
        a2 = ss(2.0, 2.5, t)
        box2 = (70, 750, 520, 900)
        card(ui, (box2[0], box2[1] + 14 * (1 - a2), box2[2], box2[3] + 14 * (1 - a2)), a2)
        y2 = box2[1] + 20 + 14 * (1 - a2)
        du.text((S(box2[0] + 24), S(y2)), 'FK-5-1-12', font=B.F_T2, fill=ca(RED, a2))
        du.text((S(box2[0] + 24), S(y2 + 42)), 'Agente químico limpio', font=B.F_SMB, fill=ca(INK, a2))
        du.text((S(box2[0] + 24), S(y2 + 76)), 'No conductor · sin residuos', font=B.F_SM, fill=ca(INK2, a2))
    d = ImageDraw.Draw(img)
    subtitle(d, 'Gases inertes obtenidos de la atmósfera o FK-5-1-12: una solución limpia para cada centro de datos.', win(t, 0.5, L))


def sc_intro(t, L, img):
    B.sc_intro(t, L, img)


def sc_outro(t, L, img):
    a = ss(0.1, 0.8, t)
    LK = B.LOCK
    img.alpha_composite(B.fade_img(LK, a), (S(W / 2) - LK.width // 2, S(H / 2) - LK.height // 2 - S(40)))
    d = ImageDraw.Draw(img)
    for i, (txt, f_, c) in enumerate([(OUTRO_TXT, B.F_T2, INK), (OUTRO_URL, B.F_SMB, RED)]):
        d.text((S(W / 2) - f_.getlength(txt) / 2, S(H / 2 + 50 + i * 48)), txt, font=f_, fill=ca(c, ss(0.6, 1.3, t)))


# ---------------- guion y transiciones ----------------
SCENES = [(0.0, 2.4, sc_intro, False), (2.4, 7.6, sc_cert, True), (7.6, 13.6, sc_detect, False),
          (13.6, 19.6, sc_alarm, False), (19.6, 27.6, sc_cylroom, True), (27.6, 33.6, sc_release, True),
          (33.6, 40.6, sc_valves, True), (40.6, 46.6, sc_nozzle, False), (46.6, 53.6, sc_flood, False),
          (53.6, 59.0, sc_ext, True), (59.0, 66.0, sc_soft1, True), (66.0, 72.0, sc_soft2, True),
          (72.0, 77.4, sc_agents, True), (77.4, 80.4, sc_outro, False)]
DUR = 80.4


def _vS(z, dy=110):
    return B.View(z, 0, dy)


def M_cert_med(tA, LA, tB, LB):
    vA = B.View(1.0 + 0.05 * ss(0, LA, tA), 0, 110); vB = B.View(1.0 + 0.06 * ss(0, LB, tB))
    return MZ.matched(vA(B.SHOTS['gsite'][2]['fire']), MZ.kp_screen('gsite', vA), MZ.kp_screen('gmed', vB))


V_UNDER = B.View(1.0, 0, 0)


def under_layer():
    """plano general del edificio sin ventana, para rellenar barridos largos"""
    if 'u' not in _UNDER:
        lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        B.draw_shot(lay, 'gsite', 0.0, 1.0, 1.0, dy=0, window=False)
        _UNDER['u'] = lay
    return _UNDER['u']


_UNDER = {}


def M_med_door(tA, LA, tB, LB):
    vA = B.View(1.0 + 0.06 * ss(0, LA, tA)); vB = B.View(1.14 + 0.04 * ss(0, LB, tB), 0, 40)
    kA = MZ.kp_screen('gmed', vA)
    fA, fB, R = MZ.matched(vA(B.SHOTS['gmed'][2]['door']), kA, MZ.kp_screen('gdoor', vB))
    Ru, Tu = MZ.fit_sim(MZ.kp_screen('gsite', V_UNDER), kA)   # A ≈ Ru·U + Tu
    fu = ((fA[0] - Tu[0]) / Ru, (fA[1] - Tu[1]) / Ru)
    return fA, fB, R, (under_layer(), Ru, fu)


def M_door_site(tA, LA, tB, LB):
    vA = B.View(1.14 + 0.04 * ss(0, LA, tA), 0, 40); vB = B.View(1.0 + 0.04 * ss(0, TZ, min(tB, TZ)), 0, 110)
    return MZ.matched(vA(B.SHOTS['gdoor'][2]['door']), MZ.kp_screen('gdoor', vA), MZ.kp_screen('gsite', vB))


def M_noz_flood(tA, LA, tB, LB):
    vA = B.View(1.0 + 0.05 * ss(0, LA, tA)); vB = B.View(1.0 + 0.04 * ss(0, LB, tB))
    return vA(B.SHOTS['gnoz'][2]['center']), vB(B.SHOTS['gfloor'][2]['nozzles'][1]), 1 / 6.0


def M_flood_ext(tA, LA, tB, LB):
    vA = B.View(1.0 + 0.04 * ss(0, LA, tA)); vB = B.View(1.0 + 0.04 * ss(0, LB, tB), 0, 110)
    return MZ.matched(vA(B.SHOTS['gfloor'][2]['fire']), MZ.kp_screen('gfloor', vA), MZ.kp_screen('gsite', vB))


def _P(im, k, cx, cy):
    return lambda px, py: (cx + (px - im.width / 2) * k, cy + (py - im.height / 2) * k)


def M_cyl_sys(tA, LA, tB, LB):
    """batería 3D de la sala de cilindros -> misma batería en la foto del sistema"""
    vA = B.View(1.0 + 0.05 * ss(TZ, LA, tA), 0, 120)
    P = _P(SYS, 0.44 + 0.015 * ss(0, LB, tB), 560, 680)
    return vA(B.SHOTS['gcyl'][2]['main_bank']), P(570, 1080), 1.5


def M_sys_valv(tA, LA, tB, LB):
    """válvulas direccionales en la foto del sistema -> detalle de las válvulas"""
    PA = _P(SYS, 0.44 + 0.015 * ss(0, LA, tA), 560, 680)
    PB = _P(VALV, 0.40 + 0.012 * ss(0, LB, tB), 540, 735)
    return PA(1640, 510), PB(1290, 800), 2.7


# transición tras la escena i: (tipo, semiduración, cámara -> (fA, fB, R), -)
TRANS = {1: ('zin', 0.8, M_cert_med, None), 2: ('zin', 0.8, M_med_door, None), 3: ('zout', 0.8, M_door_site, None),
         4: ('zin', 0.8, M_cyl_sys, None), 5: ('zin', 0.8, M_sys_valv, None),
         7: ('zout', 0.8, M_noz_flood, None), 8: ('zout', 0.8, M_flood_ext, None), 10: ('cut', 0.3, None, None)}
PUSH = 0.4
PUSH_Z = 1.04
T2 = 0.0   # compatibilidad con el montaje (sin zoom interno bajo suelo)
LOCK_POS = (S(1010) - B.LOCK_S.width, S(60))


def scene_frame(i, t, ui=True, nofade=True):
    a, b, fn, band = SCENES[i]
    B.UI[0] = ui; B.NOFADE[0] = nofade
    img = (BG if band else BG_PLAIN).copy()
    # capa de rótulos/tarjetas aparte: fundidos correctos (ImageDraw sobre RGBA reemplaza en vez de mezclar)
    B.UIL[0] = Image.new('RGBA', img.size, (0, 0, 0, 0)) if ui else None
    fn(t - a, b - a, img)
    if B.UIL[0] is not None:
        img.alpha_composite(B.UIL[0]); B.UIL[0] = None
    if ui and fn not in (sc_intro, sc_outro):
        img.alpha_composite(B.LOCK_S, LOCK_POS)
    B.UI[0] = True; B.NOFADE[0] = False
    return img


def scene_parts(i, t):
    """(escena sobre lienzo transparente, capa de rótulos, ¿lleva logotipo?, fondo)"""
    a, b, fn, band = SCENES[i]
    B.UI[0] = True; B.NOFADE[0] = True
    img = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    B.UIL[0] = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fn(t - a, b - a, img)
    ui = B.UIL[0]; B.UIL[0] = None; B.NOFADE[0] = False
    return img, ui, fn not in (sc_intro, sc_outro), (BG if band else BG_PLAIN)


def render_t(t):
    for i in range(len(SCENES) - 1):
        b = SCENES[i][1]
        kind, D, cam, _ = TRANS.get(i, ('push', PUSH, None, None))
        if b - D <= t < b + D:
            p = (t - (b - D)) / (2 * D)
            aA, bA = SCENES[i][0], SCENES[i][1]; aB, bB = SCENES[i + 1][0], SCENES[i + 1][1]
            cA, uiA, lgA, bgA = scene_parts(i, t)
            cB, uiB, lgB, bgB = scene_parts(i + 1, t)
            if kind in ('push', 'cut'):
                e = MZ.smoother(p); c = (W / 2, H / 2)
                zk = PUSH_Z if (kind == 'push' and lgA and lgB) else 1.0
                Z = 1 + (zk - 1) * e
                cA = MZ.aff(cA, Z, c, c); cB = MZ.aff(cB, Z / zk, c, c)
                A = bgA.copy(); A.alpha_composite(cA)
                Bf = bgB.copy(); Bf.alpha_composite(cB)
                out = Image.blend(A, Bf, ss(0, 1, p))
                ua, ub = 1 - ss(0.0, 0.6, p), ss(0.4, 1.0, p)
            else:
                cm = cam(t - aA, bA - aA, t - aB, bB - aB)
                fA, fB, R = cm[:3]
                lay, _ = MZ.zoom_pair(cA, cB, p, fA, fB, R, clip='auto', under=cm[3] if len(cm) > 3 else None)
                out = Image.blend(bgA, bgB, ss(0.3, 0.7, p)) if bgA is not bgB else bgA.copy()
                out.alpha_composite(lay)
                ua, ub = 1 - ss(0.0, 0.3, p), ss(0.7, 1.0, p)
            if ua > 0.01:
                out.alpha_composite(MZ.fade_layer(uiA, ua))
            if ub > 0.01:
                out.alpha_composite(MZ.fade_layer(uiB, ub))
            la = 1.0 if (lgA and lgB) else (ua if lgA else (ub if lgB else 0))
            if la > 0.01:
                out.alpha_composite(MZ.fade_layer(B.LOCK_S, la), LOCK_POS)
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
