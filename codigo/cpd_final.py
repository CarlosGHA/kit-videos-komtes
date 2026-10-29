"""Versión final con transiciones: 1440x1800 (4:5), ES/EN.
Uso: python3 cpd_final.py es|en salida.mp4   |   python3 cpd_final.py still es|en dir t..."""
import sys, subprocess, math, re
MISSING = set()
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
    'Sistema aprobado': 'Approved system',
    'Protección contra incendios aprobada por FM para centros de datos, en ambiente y en falso suelo.': 'FM Approved fire protection for data centers, above and below the raised floor.',
    'El calor, el humo y los gases tóxicos de un solo equipo amenazan a toda la sala.': 'The heat, smoke and toxic gases from a single unit threaten the entire room.',
    'Boquilla cerrada RG MMP · ambiente': 'RG MMP closed nozzle · room',
    'Cuando la temperatura alcanza su valor de disparo, se rompe la ampolla de la boquilla RG MMP más cercana al foco.': 'When the temperature reaches its rating, the bulb of the RG MMP nozzle closest to the fire bursts.',
    'Solo esa boquilla se abre.': 'Only that nozzle opens.',
    'Enfría el fuego: absorbe su calor': 'Cools the fire: absorbs its heat',
    'Desplaza el oxígeno junto a la llama': 'Displaces the oxygen around the flame',
    'La niebla enfría el fuego al absorber su calor, y el vapor que genera desplaza el oxígeno junto a la llama.': 'The mist cools the fire by absorbing its heat, and the steam it produces displaces the oxygen around the flame.',
    'Es eficaz incluso con la climatización en marcha.': 'It works even with the cooling system running.',
    'El fuego se extingue. La niebla restante se elimina con la ventilación y el centro de datos recupera pronto su actividad.': 'The fire is out. The remaining mist clears with ventilation and the data center is quickly back in operation.',
    'FALSO SUELO': 'BELOW THE RAISED FLOOR',
    'Boquilla cerrada RG MMP · falso suelo': 'RG MMP closed nozzle · raised floor',
    'Red de falso suelo': 'Raised-floor network',
    'Boquilla cerrada RG MMP': 'RG MMP closed nozzle',
    'En el falso suelo, una red independiente con boquillas RG MMP y su propia válvula de preacción protege el cableado.': 'Below the raised floor, an independent network with RG MMP nozzles and its own pre-action valve protects the cabling.',
    'DETECCIÓN': 'DETECTION',
    'Detección electrónica y central': 'Electronic detection and panel',
    'Detector electrónico': 'Electronic detector',
    'Central de detección': 'Detection panel',
    'Señal a la válvula de preacción': 'Signal to the pre-action valve',
    'Los detectores electrónicos reaccionan antes que la ampolla de la boquilla.': 'Electronic detectors react before the nozzle bulb does.',
    'La central da la alarma y envía la señal a la válvula de preacción de su zona.': 'The panel raises the alarm and signals the pre-action valve for that zone.',
    'PREACCIÓN': 'PRE-ACTION',
    'Válvula de preacción · sala de bombeo': 'Pre-action valve · pump room',
    'Red húmeda: agua': 'Wet pipe: water',
    'Red seca: aire a presión': 'Dry pipe: pressurised air',
    'Válvulas de preacción: una por zona': 'Pre-action valves: one per zone',
    'Solenoide': 'Solenoid',
    'Presostato de supervisión': 'Supervisory pressure switch',
    'Disparo manual': 'Manual release',
    'Válvula abierta': 'Valve open',
    'La válvula de preacción divide la red: con agua hasta la válvula y seca, con aire a presión, hasta las boquillas.': 'The pre-action valve splits the network: water up to the valve, and dry, pressurised air up to the nozzles.',
    'Cada zona tiene su válvula en la sala de bombeo. Al recibir la señal, la solenoide abre la válvula.': 'Each zone has its own valve in the pump room. On the signal, the solenoid opens the valve.',
    'Grupo de bombeo · sala aledaña': 'Pump unit · adjacent room',
    'La caída de presión arranca el grupo de bombeo, en una sala aledaña.': 'The pressure drop starts the pump unit in the adjacent room.',
    'El motor eléctrico acciona la bomba de pistones, y el agua circula solo hacia la válvula que se ha activado.': 'The electric motor drives the piston pump, and water flows only to the valve that has been activated.',
    'Hacia la zona activada': 'To the activated zone',
    'Resto de válvulas: cerradas': 'Other valves: closed',
    'SEGURIDAD DE LA PREACCIÓN': 'PRE-ACTION SAFETY',
    'Rotura accidental de una ampolla': 'Accidental bulb breakage',
    'Falsa alarma de detección': 'False detection alarm',
    'Ampolla rota sin incendio': 'Bulb broken, no fire',
    'Sale el aire de la tubería': 'Air escapes from the pipe',
    'Presostato: alarma': 'Pressure switch: alarm',
    'Válvula cerrada: sin detección': 'Valve closed: no detection',
    'No sale agua': 'No water released',
    'Falsa alarma': 'False alarm',
    'La central avisa': 'The panel warns',
    'Ampolla intacta: boquilla cerrada': 'Bulb intact: nozzle closed',
    'Sin descarga': 'No discharge',
    'La preacción también protege frente a errores. Si una ampolla se rompe por accidente, el aire de la tubería se escapa.': 'Pre-action also protects against mistakes. If a bulb breaks by accident, air escapes from the pipe.',
    'El presostato da la alarma, pero la válvula sigue cerrada porque no hay detección: no sale agua.': 'The pressure switch raises an alarm, but the valve stays closed because there is no detection: no water is released.',
    'Y si la detección da una falsa alarma, la central avisa, pero tampoco hay descarga.': 'And if detection gives a false alarm, the panel warns, but there is still no discharge.',
    'Sin fuego no se rompe ninguna ampolla y las boquillas permanecen cerradas.': 'With no fire, no bulb breaks and the nozzles stay closed.',
    'Detectores': 'Detectors',
    'Para la sala de generadores: RG W-FOG UAC, baterías de cilindros de agua y nitrógeno, sin bombas ni corriente eléctrica.': 'For the generator room: RG W-FOG UAC, water and nitrogen cylinder banks, with no pumps or electrical power.',
    'Si se declara un incendio en un grupo electrógeno, los detectores lo identifican y la central activa la batería.': 'If a fire breaks out in a generator set, the detectors pick it up and the releasing panel activates the battery.',
    'Boquilla cerrada MM-P51 · ambiente': 'MM-P51 closed nozzle · room',
    'Cuando la temperatura alcanza su valor de disparo, se rompe la ampolla de la boquilla MM-P51 más cercana al foco.': 'When the temperature reaches its operating point, the bulb of the MM-P51 nozzle closest to the fire breaks.',
    'Boquilla MM-P51': 'MM-P51 nozzle',
    'Boquillas MM-P52 / MM-P53 · falso suelo': 'MM-P52 / MM-P53 nozzles · raised floor',
    'Boquilla MM-P52 / MM-P53': 'MM-P52 / MM-P53 nozzle',
    'Red seca bajo el suelo técnico': 'Dry pipework below the raised floor',
    'Mazos de cables': 'Cable bundles',
    'En el falso suelo, una red independiente con boquillas MM-P52 y MM-P53 y su propia válvula de preacción protege los mazos de cables.': 'Below the raised floor, a separate network with MM-P52 and MM-P53 nozzles and its own pre-action valve protects the cable bundles.',
    'Válvula de preacción WF-PAV · sala de bombeo': 'WF-PAV pre-action valve · pump room',
    'Válvulas WF-PAV: una por zona': 'WF-PAV valves: one per zone',
    'La válvula de preacción WF-PAV divide la red: con agua hasta la válvula y seca, con aire a presión, hasta las boquillas.': 'The WF-PAV pre-action valve splits the network: water up to the valve, and dry, pressurized with air, up to the nozzles.',
    'Grupo de bombeo W-FOG UAP': 'W-FOG UAP pump unit',
    'Grupo de bombeo W-FOG UAP · sala aledaña': 'W-FOG UAP pump unit · adjacent room',
    'La caída de presión arranca el grupo de bombeo W-FOG UAP, en una sala aledaña.': 'The pressure drop starts the W-FOG UAP pump unit in the adjacent room.',
    'Difusores abiertos EMM-416549': 'EMM-416549 open nozzles',
    'Difusor abierto EMM-416549': 'EMM-416549 open nozzle',
    'Válvulas WF-PAV: una por generador': 'WF-PAV valves: one per generator',
    'Sala de transformadores': 'Transformer room',
    'Generadores y transformadores · RG W-FOG UAC': 'Generators and transformers · RG W-FOG UAC',
    'Para generadores y transformadores: RG W-FOG UAC, baterías de cilindros de agua y nitrógeno, sin bombas ni corriente eléctrica.': 'For generator and transformer rooms: RG W-FOG UAC, water and nitrogen cylinder banks, with no pumps or electrical power.',
    'Cada generador tiene su propia válvula de preacción WF-PAV junto a la batería.': 'Each generator has its own WF-PAV pre-action valve next to the bank.',
    'Si se declara un incendio en un grupo electrógeno, los detectores lo identifican y la central abre solo la válvula de ese generador.': "If a fire breaks out in a generator set, the detectors identify it and the panel opens only that generator's valve.",
    'El nitrógeno impulsa el agua por su colector hasta los difusores abiertos EMM-416549, que descargan a la vez sobre ese grupo.': 'Nitrogen drives the water through its manifold to the EMM-416549 open nozzles, which discharge at once over that unit.',
    'Se abre solo esta válvula': 'Only this valve opens',
    'Resto de válvulas: cerradas': 'Other valves: closed',
    'Salida hacia las válvulas WF-PAV': 'Outlet to the WF-PAV valves',
    'Descarga sobre el generador afectado': 'Discharge over the affected generator',
    'Descarga simultánea sobre el generador': 'Simultaneous discharge over the generator',
    'Señal a la válvula del generador': "Signal to the generator's valve",
    'Batería UAC junto a las válvulas': 'UAC bank next to the valves',
    'Bajo el suelo técnico, una red independiente con boquillas MM-P52 / MM-P53 y su propia válvula de preacción.': 'Below the raised floor, a separate network with MM-P52 / MM-P53 nozzles and its own pre-action valve.',
    'Generadores y transformadores: RG W-FOG UAC, baterías de agua y nitrógeno, sin bombas ni corriente eléctrica.': 'Generators and transformers: RG W-FOG UAC, water and nitrogen banks, with no pumps or electrical power.',
    'Ante un incendio en un generador, los detectores lo identifican y la central abre solo su válvula.': 'If a generator catches fire, the detectors identify it and the panel opens only its valve.',
    'El nitrógeno impulsa el agua por su colector hasta los difusores EMM-416549, que descargan sobre ese grupo.': 'Nitrogen drives the water through its manifold to the EMM-416549 nozzles, which discharge over that unit.',
    'Así se protege un centro de datos': 'How a data center is protected',
    'La válvula de preacción WF-PAV': 'The WF-PAV pre-action valve',
    'De la ampolla a la extinción': 'From bulb to extinction',
    'Generadores y transformadores': 'Generators and transformers',
    'EN EL PRÓXIMO CAPÍTULO': 'IN THE NEXT EPISODE',
    'CAPÍTULO 1/4 · RG W-FOG EN CENTROS DE DATOS': 'EPISODE 1/4 · RG W-FOG IN DATA CENTERS',
    'CAPÍTULO 2/4 · RG W-FOG EN CENTROS DE DATOS': 'EPISODE 2/4 · RG W-FOG IN DATA CENTERS',
    'CAPÍTULO 3/4 · RG W-FOG EN CENTROS DE DATOS': 'EPISODE 3/4 · RG W-FOG IN DATA CENTERS',
    'CAPÍTULO 4/4 · RG W-FOG EN CENTROS DE DATOS': 'EPISODE 4/4 · RG W-FOG IN DATA CENTERS',
}


def TR(s):
    if LANG != 'en' or not isinstance(s, str):
        return s
    if s in EN:
        return EN[s]
    if len(s) > 5 and s[:2].isdigit() and s[2:5] == ' · ' and s[5:] in EN:
        return s[:5] + EN[s[5:]]
    if any(c in s for c in 'áéíóúñ¿') or re.search(r'\b(de|la|el|los|las|con|sin|en)\b', s):
        MISSING.add(s)
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


CL_UFD = [B.Cloud(500 + i, 900, 0.0, 9.0, (0.5, 1.1), 0.14, (240, 380)) for i in range(16)]
UFD_R = 5.0
UFD_TB = 0.9      # rotura de la ampolla (s después de T2)


def _v_ufd(t, L):
    return B.View(1.0 + 0.05 * ss(T2, L, t), 0, 40)


def sc_floor(t, L, img):
    """falso suelo: plano general de la red bajo baldosas -> primer plano de la boquilla MM-P52/53 (mismo detalle que la de techo)"""
    js_f = B.SHOTS['floor'][2]
    p = clamp((t - (T2 - DZ)) / (2 * DZ))
    zA = 1.0 + 0.04 * ss(0, T2, min(t, T2))
    layA = layB = None
    d = ImageDraw.Draw(img)
    if t < T2 + DZ:
        layA = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        vA, js = B.draw_shot(layA, 'floor', t, zA, 1.0 if B.NOFADE[0] else ss(0, 0.5, t), window=True)
        ua = 1 - ss(T2 - DZ, T2 - DZ + 0.2, t)
        tag(d, 80, 930, 'Red seca bajo el suelo técnico', win(t, 0.6, L) * ua, vA(js['uf_noz'][1]))
    if t > T2 - DZ:
        tt = t - T2
        layB = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        vB = _v_ufd(t, L)
        jsB = B.SHOTS['ufd_a'][2]
        bulb = vB(jsB['bulb'])
        heat = ss(-0.6, 0.6, tt) * (1 - ss(2.6, 4.0, tt))
        if heat > 0.01:
            glow, gd = low()
            for rr, al in ((420, 50), (260, 80), (140, 110)):
                r = rr * (0.6 + 0.4 * heat) / 4
                gd.ellipse([bulb[0] / 4 - r, (bulb[1] + 300) / 4 - r, bulb[0] / 4 + r, (bulb[1] + 300) / 4 + r],
                           fill=(255, 110, 30, int(al * heat)))
            layB.alpha_composite(up(glow, 14))
        B.draw_shot(layB, 'ufd_a' if tt < UFD_TB else 'ufd_b', t, vB.k * B.RES[0] / W, 1.0, dy=40, window=True)
        over, od = full(); fog, fd = low()
        if UFD_TB < tt < UFD_TB + 1.4:
            tb = tt - UFD_TB
            rng = np.random.default_rng(9)
            for i in range(14):
                ang = rng.uniform(0, 6.28); spd = rng.uniform(160, 320)
                px = bulb[0] + math.cos(ang) * spd * tb; py = bulb[1] + math.sin(ang) * spd * tb + 380 * tb * tb
                od.ellipse([S(px - 3), S(py - 3), S(px + 3), S(py + 3)], fill=(225, 50, 40, int(220 * clamp(1 - tb))))
        sa = ss(UFD_TB + 0.2, UFD_TB + 0.6, tt)
        if sa > 0.01:
            for i_, (a_, b_) in enumerate(jsB['orif']):
                p0 = vB(a_); p1 = vB(b_)
                ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
                k = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / 260
                spray(od, fd, CL_UFD[i_ % len(CL_UFD)], tt - UFD_TB - 0.2 - 0.03 * i_, p0[0], p0[1], ang, max(0.6, k), sa,
                      drag=2.2, grav=90, fog_a=34, dot_a=235)
        layB.alpha_composite(up(fog, 6)); layB.alpha_composite(over)
        ub = ss(T2 + DZ - 0.1, T2 + DZ + 0.2, t)
        tag(d, 640, 300, 'Boquilla MM-P52 / MM-P53', win(tt, DZ + 0.1, L - T2 - 0.2) * ub, vB(jsB['hex']))
        tag(d, 640, 820, 'Micro-orificios', win(tt, UFD_TB + 0.8, L - T2 - 0.2) * ub, vB(jsB['orif'][0][0]))
        tag(d, 70, 1010, 'Mazos de cables', win(tt, DZ + 0.6, L - T2 - 0.2) * ub, (bulb[0] - 170, bulb[1] + 150))
    if layA is not None and layB is not None:
        vA = B.View(zA); vB = _v_ufd(t, L)
        lay, _ = zoom_pair(layA, layB, p, vA(js_f['uf_noz'][1]), vB(B.SHOTS['ufd_a'][2]['hex']), UFD_R, False, True, clip=True)
        img.alpha_composite(V.mclip(lay))
    elif layA is not None:
        img.alpha_composite(V.mclip(layA))
    else:
        img.alpha_composite(_panel_layer(layB))
    d = ImageDraw.Draw(img)
    V.step_header(d, 7, 'FALSO SUELO', 'Boquillas MM-P52 / MM-P53 · falso suelo', ss(0.2, 0.7, t))
    subtitle(d, 'Bajo el suelo técnico, una red independiente con boquillas MM-P52 / MM-P53 y su propia válvula de preacción.',
             win(t, 0.5, L))


# ---------------- escena de bombeo: sala 3D -> zoom -> motor ----------------
# ---------------- escena de bombeo: sala 3D -> zoom -> motor ----------------
import os
B.SHOTS['proom'] = (Image.open(B.SP + 'r5/proom.png').convert('RGBA'), None, __import__('json').load(open(B.SP + 'r5/proom.json')))
# planos con la sala de bombeo aledaña (r7)
R7 = B.SP + ('r8/' if os.path.exists(B.SP + 'r8/site.json') else 'r7/')
_j = __import__('json')
_DIRS = [B.SP + d_ for d_ in ('r10/', 'r9/', 'r8/', 'r7/')]


def _l7(n, alt=None):
    D = next(d_ for d_ in _DIRS if os.path.exists(d_ + n + '.json'))
    a_ = Image.open(D + n + '.png').convert('RGBA')
    b_ = Image.open(D + n + '_led1.png').convert('RGBA') if alt and os.path.exists(D + n + '_led1.png') else None
    return (a_, b_, _j.load(open(D + n + '.json')))


def _has(n):
    return any(os.path.exists(d_ + n + '.json') for d_ in _DIRS)


B.SHOTS['wide'] = _l7('site', True)
for n_ in ('proom2', 'gen', 'gnoz', 'floor_det', 'floor_det_b', 'ceil_a', 'ceil_b', 'pavd', 'ufd_a', 'ufd_b'):
    if _has(n_):
        B.SHOTS[n_] = _l7(n_)
for n_ in ('med', 'floor'):
    if _has(n_):
        B.SHOTS[n_] = _l7(n_, True)
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
UF = 6.4; UD = 8.3; UP = 9.2; UA = 10.2
TV = 4.7          # «Cada generador tiene su propia válvula…»
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




def uac_route(img, v, js, t, a, t0=0.0, active=None, dry=0.0):
    """batería UAC -> válvulas WF-PAV -> un colector por generador (+ sala de transformadores).
    a: realce de la alimentación; active: índice del colector por el que circula el agua; dry: colectores en reposo"""
    if 'uac_feed' not in js:
        return None
    feed = [v(p) for p in js['uac_feed']]
    cols = [[v(p) for p in c] for c in js.get('uac_c', [])]
    if dry > 0.01:
        for ci, c in enumerate(cols):
            if ci != active or a <= 0.01:
                _route(img, lambda q: q, c[1:], AIR, dry, w=2.8, dashed=True, glow=False)
    if a > 0.01:
        _route(img, lambda q: q, feed, WATER, a, w=3.4)
        _dots(img, feed, t - t0, a * ss(t0, t0 + 0.4, t), WATER, n=10, speed=0.3)
        if active is not None and active < len(cols):
            c = cols[active]
            ca = a * ss(t0 + 0.5, t0 + 1.0, t)
            _route(img, lambda q: q, c, WATER, ca, w=3.4)
            _dots(img, c, t - t0 - 0.5, ca, WATER, n=14, speed=0.22)
    return feed


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
    uac_route(lay, v, js, t, 0.0, dry=ss(0.3, 0.8, t))
    gz = v(js['genroom']); uz = v(js['uac'])

    def tags(d, a):
        tag(d, 80, 330, 'Centro de datos', win(t, 0.3, L) * a, v(js['fire_top']))
        tag(d, 90, 1010, 'Batería UAC junto a las válvulas', win(t, 0.6, L) * a, uz)
        tag(d, 620, 262, 'Sala de generadores', win(t, 0.9, L) * a, gz)
        if 'trafo' in js:
            tag(d, 620, 1010, 'Sala de transformadores', win(t, 1.2, L) * a, v(js['trafo']))
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
        uac_route(lay, v, jg, t, ss(UA + 0.2, UA + 0.6, t), t0=UA + 0.2, active=0, dry=max(sysa, ss(UF, UF + 0.4, t)))
        # señal de la central a la válvula del generador 1
        if 'gpanel' in jg and 'uac_pav' in jg:
            sp = [v(jg['gpanel']), v(jg['uac_pav'][0])]
            pr = ss(UP + 0.2, UA, t) * (1 - ss(CA0 - 0.6, CA0, t))
            if pr > 0.01:
                part = _partial(sp, ss(UP + 0.2, UA, t))
                ll, lld = full()
                lld.line([(S(x), S(y)) for x, y in part], fill=B.ca(B.RED, 0.9 * pr), width=B.SW(2.6))
                lay.alpha_composite(ll)
    else:
        ra = ss(CC0 - 0.6, CC0, t) * (1 - ss(CD0 - 1.0, CD0, t))
        uac_route(lay, v, jg, t, ra, t0=CC0 - 1.6, active=0, dry=ra)
    if fl > 0.01:
        jsF = {'fire': jg['gfire'], 'fire_top': jg['gfire_top']}
        V.fire_fx(lay, v, jsF, t, fl, 46 * fl, ss(UF + 0.4, UF + 2.2, t) * (1 - ss(CC0, CC0 + 3.0, t)), t - UF)
    if second:
        ma = ss(CC0 - 0.8, CC0, t) * (1 - ss(CD0 - 1.6, CD0 + 0.6, t))
        if ma > 0.01:
            o2, od2 = full(); f2, fd2 = low()
            noz = jg['uac_noz'][0] if 'uac_noz' in jg else jg.get('gnoz', [])
            for i_, q in enumerate(noz):
                nq = v(q)
                for k_, ang in enumerate((60, 90, 120)):
                    spray(od2, fd2, V.CL_UF2, t - CC0 + 1.2 - 0.05 * i_ - 0.1 * k_, nq[0], nq[1] + 4, math.radians(ang), 0.9, ma,
                          drag=0.7, grav=14, fog_a=46, dot_a=170, col=(96, 150, 210))
            lay.alpha_composite(up(f2, 6)); lay.alpha_composite(o2)

    def tags(d, a):
        if not second:
            sysa_ = ss(TU1 + 0.1, TU1 + 0.5, t) * (1 - ss(UF - 0.4, UF, t))
            tag(d, 70, 300, 'Cilindro de N₂', win(t, TU1 + 0.5, TV) * sysa_ * a, v(jg['uac_n2']))
            tag(d, 420, 262, 'Cilindros de agua', win(t, TU1 + 0.8, TV) * sysa_ * a, v(jg['uac']))
            tag(d, 70, 1010, 'Válvulas WF-PAV: una por generador', win(t, TV, UF - 0.2) * sysa_ * a,
                v(jg['uac_pav'][1]) if 'uac_pav' in jg else None)
            tag(d, 600, 1010, 'Difusores abiertos EMM-416549', win(t, TU1 + 1.1, UF - 0.2) * sysa_ * a, v(jg['gen_noz']))
            tag(d, 70, 1010, 'Incendio en un grupo electrógeno', win(t, UF + 0.4, UD - 0.1) * a, v(jg['gfire_top']))
            if jg.get('gdet'):
                pulse(d, v(jg['gdet'][0]), t, UD, win(t, UD, UA + 0.4) * a)
                tag(d, 600, 262, 'Detectores', win(t, UD + 0.2, UP) * a, v(jg['gdet'][0]))
            pulse(d, v(jg['gpanel']), t, UP, win(t, UP, CA0) * a)
            tag(d, 70, 300, 'Central de extinción', win(t, UP + 0.2, CA0) * a, v(jg['gpanel']))
            if 'uac_pav' in jg:
                pulse(d, v(jg['uac_pav'][0]), t, UA, win(t, UA, CA0) * a)
                tag(d, 600, 262, 'Se abre solo esta válvula', win(t, UA + 0.1, CA0) * a, v(jg['uac_pav'][0]))
                tag(d, 70, 1010, 'Resto de válvulas: cerradas', win(t, UA + 0.5, CA0) * a, v(jg['uac_pav'][2]))
        else:
            tag(d, 600, 1010, 'Descarga sobre el generador afectado', win(t, CC0 + 0.6, CC0 + 2.6) * a, v(jg['gen_noz']))
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
        tag(d, 600, 262, 'Salida hacia las válvulas WF-PAV', win(t, CA0 + 2.2, CB0) * a, Pm(572, 150))
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
        tag(d, 640, 380, 'Difusor abierto EMM-416549', win(t, CB0 + 0.3, CC0) * a, v(jn['cn_hex']))
        tag(d, 640, 820, 'Insertos de orificio', win(t, CB0 + 1.0, CC0) * a, v(jn['cn_ins']))
        tag(d, 70, 1010, 'Descarga simultánea sobre el generador', win(t, CB0 + 1.8, CC0) * a, None)
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
    title(d, 'OTROS RIESGOS DEL EDIFICIO', 'Generadores y transformadores · RG W-FOG UAC', ss(0.2, 0.7, t))
    subtitle(d, 'Generadores y transformadores: RG W-FOG UAC, baterías de agua y nitrógeno, sin bombas ni corriente eléctrica.',
             win(t, 0.5, TV))
    subtitle(d, 'Cada generador tiene su propia válvula de preacción WF-PAV junto a la batería.', win(t, TV, UF))
    subtitle(d, 'Ante un incendio en un generador, los detectores lo identifican y la central abre solo su válvula.',
             win(t, UF, CA0 + 1.0))
    subtitle(d, 'El nitrógeno impulsa el agua por su colector hasta los difusores EMM-416549, que descargan sobre ese grupo.',
             win(t, CA0 + 1.0, L))

# =====================================================================================
# v2 (revisión de I+D): detección electrónica, preacción y casos de seguridad
# =====================================================================================
WATER = (70, 140, 215)
AIR = (112, 122, 136)


def _route(img, v, path, col, a, w=3.2, dashed=False, glow=True):
    """resalta un tramo de tubería (puntos 3D) con color propio"""
    if a <= 0.01 or len(path) < 2:
        return []
    pts = [v(q) for q in path]
    if glow:
        gl, gd = low()
        gd.line([(x / 4, y / 4) for x, y in pts], fill=col + (int(120 * a),), width=4, joint='curve')
        img.alpha_composite(up(gl, 4))
    lay, ld = full()
    if dashed:
        for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
            L_ = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L_ / 14))
            for k in range(0, n, 2):
                u0, u1 = k / n, min(1, (k + 1) / n)
                ld.line([(S(x0 + (x1 - x0) * u0), S(y0 + (y1 - y0) * u0)), (S(x0 + (x1 - x0) * u1), S(y0 + (y1 - y0) * u1))],
                        fill=B.ca(col, a), width=B.SW(w))
    else:
        ld.line([(S(x), S(y)) for x, y in pts], fill=B.ca(col, a), width=B.SW(w), joint='curve')
    img.alpha_composite(lay)
    return pts


def _dots(img, pts, t, a, col, n=12, speed=0.3, r=6):
    if a <= 0.01 or len(pts) < 2:
        return
    d = ImageDraw.Draw(img)
    segs = [(p, q, math.hypot(q[0] - p[0], q[1] - p[1])) for p, q in zip(pts[:-1], pts[1:])]
    tot = sum(sg[2] for sg in segs) or 1
    for i in range(n):
        u = ((t * speed + i / n) % 1) * tot
        for p, q, l in segs:
            if u <= l:
                k_ = u / l if l else 0
                x, y = p[0] + (q[0] - p[0]) * k_, p[1] + (q[1] - p[1]) * k_
                break
            u -= l
        d.ellipse([S(x - r), S(y - r), S(x + r), S(y + r)], fill=B.ca(col, a), outline=B.ca((255, 255, 255), a), width=B.SW(1.5))


def _partial(pts, u):
    """primer tramo de una polilínea (u = 0..1 de su longitud)"""
    if u >= 1 or len(pts) < 2:
        return pts
    segs = [math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts[:-1], pts[1:])]
    tot = sum(segs) * max(0.0, u); out = [pts[0]]
    for (p, q), l in zip(zip(pts[:-1], pts[1:]), segs):
        if tot <= l:
            k_ = tot / l if l else 0
            out.append((p[0] + (q[0] - p[0]) * k_, p[1] + (q[1] - p[1]) * k_)); return out
        out.append(q); tot -= l
    return out


def _push_pair(la, lb, p, zk=1.04):
    """fundido entre capas sin relación espacial: acercamiento común, sin saltos"""
    e = smoother(p); c = (W / 2, H / 2); Z = 1 + (zk - 1) * e
    return pblend(aff(la, Z, c, c), aff(lb, Z / zk, c, c), ss(0.15, 0.85, p))


def _panel_layer(lay):
    """capa de producto sobre panel blanco (ventana)"""
    if B.PANEL_BG[3] == 0:
        return V.mclip(lay)
    out = V.mclip(Image.new('RGBA', lay.size, B.PANEL_BG))
    out.alpha_composite(V.mclip(lay))
    return out


# ---------------- 02 · DETECCIÓN ----------------
TD_A = 3.6


def _v_detA(t):
    return B.View(1.06 + 0.03 * ss(0, TD_A, min(t, TD_A)))


def _v_detB(t, L):
    return B.View(0.95 + 0.03 * ss(TD_A, L, t), 0, 60)


def sc_detect(t, L, img):
    p = clamp((t - (TD_A - DZP)) / (2 * DZP))
    la = lb = None
    d = ImageDraw.Draw(img)
    if t < TD_A + DZP:
        la = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        vA = _v_detA(t)
        B.draw_shot(la, 'med', t + 6, vA.k * B.RES[0] / W, 1.0, window=True)
        jm = B.SHOTS['med'][2]
        V.fire_fx(la, vA, jm, t + 6, 1.0, 58, 1.0, t + 6)
        dp = vA(jm['det_fire'])
        ua = 1 - ss(TD_A - DZP, TD_A - DZP + 0.2, t)
        pulse(ImageDraw.Draw(la), dp, t, 0.5, ua * ss(0.5, 0.8, t))
        tag(d, 640, 300, 'Detector electrónico', win(t, 0.8, L) * ua, dp)
    if t > TD_A - DZP:
        lb = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        vB = _v_detB(t, L)
        B.draw_shot(lb, 'wide', t, vB.k * B.RES[0] / W, 1.0, dy=60, window=True)
        js = B.SHOTS['wide'][2]
        V.fire_fx(lb, vB, js, t, 0.8, 22, 0.6, t)
        path = [vB(js['det_fire']), vB(js['dpanel']), vB(js['pav'][0])]
        pr = ss(TD_A + 0.5, TD_A + 2.6, t)
        if pr > 0.01:
            part = _partial(path, pr)
            lay, ld = full()
            ld.line([(S(x), S(y)) for x, y in part], fill=B.ca(B.RED, 0.9), width=B.SW(2.6), joint='curve')
            lb.alpha_composite(lay)
            hx, hy = part[-1]
            ImageDraw.Draw(lb).ellipse([S(hx - 7), S(hy - 7), S(hx + 7), S(hy + 7)], fill=B.ca(B.RED, 1), outline=B.ca((255, 255, 255), 1), width=B.SW(2))
        pulse(ImageDraw.Draw(lb), path[1], t, TD_A + 1.4, ss(TD_A + 1.4, TD_A + 1.7, t))
        pulse(ImageDraw.Draw(lb), path[2], t, TD_A + 2.6, ss(TD_A + 2.6, TD_A + 2.9, t))
        ub = ss(TD_A + DZP - 0.1, TD_A + DZP + 0.2, t)
        tag(d, 600, 262, 'Central de detección', win(t, TD_A + 1.3, L) * ub, path[1])
        tag(d, 600, 1010, 'Señal a la válvula de preacción', win(t, TD_A + 2.5, L) * ub, path[2])
    if la is not None and lb is not None:
        jm = B.SHOTS['med'][2]; js = B.SHOTS['wide'][2]
        vA = _v_detA(t); vB = _v_detB(t, L)
        fA, fB, R = matched(vA(jm['fire']), kp_screen('med', vA), kp_screen('wide', vB))
        lay, _ = zoom_pair(la, lb, p, fA, fB, R, clip=True)
        img.alpha_composite(V.mclip(lay))
    else:
        img.alpha_composite(V.mclip(la if la is not None else lb))
    d = ImageDraw.Draw(img)
    V.step_header(d, 2, 'DETECCIÓN', 'Detección electrónica y central', ss(0.2, 0.7, t))
    subtitle(d, 'Los detectores electrónicos reaccionan antes que la ampolla de la boquilla.', win(t, 0.5, TD_A + 0.6))
    subtitle(d, 'La central da la alarma y envía la señal a la válvula de preacción de su zona.', win(t, TD_A + 0.6, L))


# ---------------- 03 · PREACCIÓN ----------------
TP_B = 6.0
PAV_R = 6.0


def _v_preA(t):
    return B.View(0.86 + 0.04 * ss(0, TP_B, min(t, TP_B)), 0, 40)


def _v_pavd(t, t0, L):
    return B.View(1.0 + 0.04 * ss(t0, L, t), 0, 20)


def _networks(img, v, js, t, a_wet, a_dry, water_dc=0.0, t0=0.0):
    wet = _route(img, v, js['wet_all'] + [], WATER, a_wet, w=3.6)
    _route(img, v, js['wet'], WATER, a_wet, w=3.6, glow=False)
    for k_ in ('dry_dc', 'dry_uf', 'dry_ctrl', 'dry_pump'):
        if k_ in js:
            _route(img, v, js[k_], AIR, a_dry, w=3.0, dashed=True, glow=False)
    if water_dc > 0.01:
        pts = _route(img, v, js['dry_dc'], WATER, water_dc, w=3.6)
        _dots(img, [v(q) for q in js['wet']] + pts[1:], t - t0, water_dc, WATER, n=16, speed=0.25)
    return wet


def sc_preaction(t, L, img):
    p = clamp((t - (TP_B - DZP)) / (2 * DZP))
    la = lb = None
    d = ImageDraw.Draw(img)
    if t < TP_B + DZP:
        la = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        vA = _v_preA(t)
        B.draw_shot(la, 'proom2', t, vA.k * B.RES[0] / W, 1.0, dy=40, window=True)
        js = B.SHOTS['proom2'][2]
        ua = 1 - ss(TP_B - DZP, TP_B - DZP + 0.2, t)
        _networks(la, vA, js, t, ss(0.5, 1.0, t) * ua, ss(1.6, 2.1, t) * ua)
        wm = vA(js['wet_all'][1]); dm = vA(js['dry_ctrl'][-1])
        tag(d, 70, 1010, 'Red húmeda: agua', win(t, 0.8, L) * ua, wm)
        tag(d, 600, 262, 'Red seca: aire a presión', win(t, 1.9, L) * ua, vA(js['dry_pump'][-1]))
        tag(d, 600, 1010, 'Válvulas WF-PAV: una por zona', win(t, 2.8, L) * ua, vA(js['pav'][1]))
    if t > TP_B - DZP:
        lb = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        vB = _v_pavd(t, TP_B, L)
        jv = B.SHOTS['pavd'][2]
        B.draw_shot(lb, 'pavd', t, vB.k * B.RES[0] / W, 1.0, dy=20, window=True)
        ub = ss(TP_B + DZP - 0.1, TP_B + DZP + 0.2, t)
        _route(lb, vB, jv['pv_wet'], WATER, ub * 0.85, w=3.0, glow=False)
        open_ = ss(L - 2.6, L - 2.3, t)
        if open_ > 0.01:
            pulse(ImageDraw.Draw(lb), vB(jv['pv_sol']), t, L - 2.6, open_)
            _dots(lb, [vB(q) for q in jv['pv_wet']] + [vB(q) for q in jv['pv_dry']], t - (L - 2.3), ss(L - 2.3, L - 1.9, t), WATER, n=10, speed=0.4)
        tag(d, 640, 300, 'Solenoide', win(t, TP_B + 1.0, L) * ub, vB(jv['pv_sol']))
        tag(d, 70, 960, 'Presostato de supervisión', win(t, TP_B + 1.6, L) * ub, vB(jv['pv_ps']))
        tag(d, 70, 300, 'Disparo manual', win(t, TP_B + 2.2, L) * ub, vB(jv['pv_top']))
        tag(d, 640, 1010, 'Válvula abierta', win(t, L - 2.2, L) * ub, vB(jv['pv_body']))
    if la is not None and lb is not None:
        js = B.SHOTS['proom2'][2]; jv = B.SHOTS['pavd'][2]
        vA = _v_preA(t); vB = _v_pavd(t, TP_B, L)
        lay, _ = zoom_pair(la, lb, p, vA(js['pav'][0]), vB(jv['pv_body']), PAV_R, False, True, clip=True)
        img.alpha_composite(V.mclip(lay))
    elif la is not None:
        img.alpha_composite(V.mclip(la))
    else:
        img.alpha_composite(_panel_layer(lb))
    d = ImageDraw.Draw(img)
    V.step_header(d, 3, 'PREACCIÓN', 'Válvula de preacción WF-PAV · sala de bombeo', ss(0.2, 0.7, t))
    subtitle(d, 'La válvula de preacción WF-PAV divide la red: con agua hasta la válvula y seca, con aire a presión, hasta las boquillas.',
             win(t, 0.5, TP_B + 0.4))
    subtitle(d, 'Cada zona tiene su válvula en la sala de bombeo. Al recibir la señal, la solenoide abre la válvula.', win(t, TP_B + 0.4, L))


# ---------------- 05 · ARRANQUE DEL BOMBEO ----------------
TZ2 = 4.4
TC2 = 8.2


def _v_pump(t):
    return B.View(0.86 + 0.04 * ss(0, TC2 + 3, t), 0, 40)


def sc_pump2(t, L, img):
    pAB = clamp((t - (TZ2 - DZP)) / (2 * DZP))
    pBC = clamp((t - (TC2 - DZP)) / (2 * DZP))
    js = B.SHOTS['proom2'][2]
    d = ImageDraw.Draw(img)
    LA = LB = LC = None
    if t < TZ2 + DZP:
        LA = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        v = _v_pump(t)
        B.draw_shot(LA, 'proom2', t, v.k * B.RES[0] / W, 1.0, dy=40, window=True)
        _networks(LA, v, js, t, 1.0, 0.6)
        ua = 1 - ss(TZ2 - DZP, TZ2 - DZP + 0.2, t)
        tag(d, 640, 1010, 'Grupo de bombeo W-FOG UAP', win(t, 0.6, L) * ua, v(js['group']))
        tag(d, 70, 262, 'Cuadro de control', win(t, 1.0, L) * ua, v(js['cab']))
    if TZ2 - DZP < t < TC2 + DZP:
        LB = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        P = pump_detail(LB, t + (TZ - TZ2), L + (TZ - TZ2))
        ub = ss(TZ2 + 0.2, TZ2 + 0.6, t) * (1 - ss(TC2 - DZP, TC2 - DZP + 0.2, t))
        tag(d, 600, 1040, 'Motor eléctrico', win(t, TZ2 + 1.2, L) * ub, P(MOTOR_C[0] + 30, MOTOR_C[1] + 40))
        tag(d, 70, 1040, 'Bomba de pistones', win(t, TZ2 + 1.8, L) * ub, P(445, 425))
    if t > TC2 - DZP:
        LC = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        v = _v_pump(t)
        B.draw_shot(LC, 'proom2', t, v.k * B.RES[0] / W, 1.0, dy=40, window=True)
        _networks(LC, v, js, t, 1.0, 0.6, water_dc=ss(TC2 + 0.3, TC2 + 0.8, t), t0=TC2 + 0.3)
        uc = ss(TC2 + DZP - 0.1, TC2 + DZP + 0.2, t)
        tag(d, 600, 262, 'Hacia la zona activada', win(t, TC2 + 1.0, L) * uc, v(js['dry_dc'][1]))
        tag(d, 70, 1010, 'Resto de válvulas: cerradas', win(t, TC2 + 1.6, L) * uc, v(js['pav'][2]))
    if LA is not None and LB is not None:
        v = _v_pump(t)
        Pm = _pump_map(t)
        lay, _ = zoom_pair(LA, LB, pAB, v(js['motor_c']), Pm(*MOTOR_C), PUMP_R, False, True, clip=True)
    elif LB is not None and LC is not None:
        v = _v_pump(t); Pm = _pump_map(t)
        lay, _ = zoom_pair(LB, LC, pBC, Pm(*MOTOR_C), v(js['motor_c']), 1 / PUMP_R, True, False, clip=True)
    elif LB is not None:
        lay = _panel_layer(LB)
    else:
        lay = LA if LA is not None else LC
    img.alpha_composite(V.mclip(lay))
    if TZ2 - DZP < t < TC2 + DZP:
        ga = ss(TZ2 + 0.4, TZ2 + 0.9, t) * (1 - ss(TC2 - DZP, TC2 - DZP + 0.3, t))
        if ga > 0.01:
            V.gauge(img, t - TZ2 + 0.2, ga, (720, 236, 1010, 480))
    elif t < TZ2:
        V.gauge(img, t, ss(0.4, 0.9, t) * (1 - ss(TZ2 - DZP, TZ2 - DZP + 0.3, t)), (720, 236, 1010, 480))
    d = ImageDraw.Draw(img)
    V.step_header(d, 5, 'ARRANQUE DEL BOMBEO', 'Grupo de bombeo W-FOG UAP · sala aledaña', ss(0.2, 0.7, t))
    subtitle(d, 'La caída de presión arranca el grupo de bombeo W-FOG UAP, en una sala aledaña.', win(t, 0.5, TZ2 + 0.6))
    subtitle(d, 'El motor eléctrico acciona la bomba de pistones, y el agua circula solo hacia la válvula que se ha activado.',
             win(t, TZ2 + 0.6, L))


def _pump_map(t):
    """misma colocación que pump_detail (foto del grupo) para anclar las transiciones"""
    tt = t + (TZ - TZ2)
    k = 0.86 + 0.03 * ss(TZ, TZ + 12, tt)
    cx, cy = 540, 760
    return lambda px, py: (cx + (px - PUMP2.width / 2) * k, cy + (py - PUMP2.height / 2) * k)


# ---------------- SEGURIDAD DE LA PREACCIÓN ----------------
TS1 = 4.6
CL_AIR = [B.Cloud(700 + i, 300, 0.0, 6.0, (0.4, 0.9), 0.2, (160, 300)) for i in range(10)]


def sc_safety1(t, L, img):
    """rotura accidental de una ampolla: sale el aire, el presostato avisa y la válvula sigue cerrada"""
    p = clamp((t - (TS1 - DZP)) / (2 * DZP))
    d = ImageDraw.Draw(img)
    la = lb = None
    if t < TS1 + DZP:
        la = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        v = B.View(1.0 + 0.05 * ss(0, TS1, t))
        B.draw_shot(la, 'ceil_b', t, v.k * B.RES[0] / W, 1.0, window=True)
        jc = B.SHOTS['ceil_b'][2]
        over, od = full(); fog, fd = low()
        air = ss(0.4, 0.8, t) * (1 - ss(2.8, 4.2, t))
        for cl, (a_, b_) in zip(CL_AIR, jc['orif'][::2]):
            p0 = v(a_); p1 = v(b_)
            ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
            spray(od, fd, cl, t - 0.4, p0[0], p0[1], ang, 0.7, air, drag=3.0, grav=-10, fog_a=18, dot_a=120, col=(185, 192, 200))
        la.alpha_composite(V.mclip(up(fog, 6))); la.alpha_composite(V.mclip(over))
        ua = 1 - ss(TS1 - DZP, TS1 - DZP + 0.2, t)
        tag(d, 640, 820, 'Ampolla rota sin incendio', win(t, 0.6, L) * ua, v(jc['bulb']))
        tag(d, 70, 1010, 'Sale el aire de la tubería', win(t, 1.4, L) * ua, v(jc['orif'][3][0]))
    if t > TS1 - DZP:
        lb = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        v = _v_pavd(t, TS1, L)
        jv = B.SHOTS['pavd'][2]
        B.draw_shot(lb, 'pavd', t, v.k * B.RES[0] / W, 1.0, dy=20, window=True)
        ub = ss(TS1 + DZP - 0.1, TS1 + DZP + 0.2, t)
        _route(lb, v, jv['pv_wet'], WATER, ub * 0.85, w=3.0, glow=False)
        _route(lb, v, jv['pv_dry'], AIR, ub, w=3.0, dashed=True, glow=False)
        pulse(ImageDraw.Draw(lb), v(jv['pv_ps']), t, TS1 + 0.6, ub * ss(TS1 + 0.6, TS1 + 0.9, t), col=(230, 150, 20))
        tag(d, 70, 960, 'Presostato: alarma', win(t, TS1 + 0.9, L) * ub, v(jv['pv_ps']))
        tag(d, 640, 1010, 'Válvula cerrada: sin detección', win(t, TS1 + 1.6, L) * ub, v(jv['pv_body']))
        tag(d, 640, 300, 'No sale agua', win(t, TS1 + 2.4, L) * ub, None)
    if la is not None and lb is not None:
        lay = _push_pair(la, _panel_layer(lb), p)
    elif la is not None:
        lay = la
    else:
        lay = _panel_layer(lb)
    img.alpha_composite(V.mclip(lay))
    d = ImageDraw.Draw(img)
    title(d, 'SEGURIDAD DE LA PREACCIÓN', 'Rotura accidental de una ampolla', ss(0.2, 0.7, t))
    subtitle(d, 'La preacción también protege frente a errores. Si una ampolla se rompe por accidente, el aire de la tubería se escapa.',
             win(t, 0.5, TS1 + 0.4))
    subtitle(d, 'El presostato da la alarma, pero la válvula sigue cerrada porque no hay detección: no sale agua.', win(t, TS1 + 0.4, L))


TS2 = 4.4


def _v_s2A(t):
    return B.View(1.0 + 0.06 * ss(0, TS2, t))


def _v_s2B(t, L):
    return B.View(1.0 + 0.05 * ss(TS2, L, t))


def sc_safety2(t, L, img):
    """falsa alarma de detección: la central avisa pero, sin fuego, ninguna ampolla se rompe"""
    p = clamp((t - (TS2 - DZP)) / (2 * DZP))
    d = ImageDraw.Draw(img)
    la = lb = None
    if t < TS2 + DZP:
        la = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        v = _v_s2A(t)
        B.draw_shot(la, 'med', t, v.k * B.RES[0] / W, 1.0, window=True)
        jm = B.SHOTS['med'][2]
        ua = 1 - ss(TS2 - DZP, TS2 - DZP + 0.2, t)
        pulse(ImageDraw.Draw(la), v(jm['det_fire']), t, 0.5, ua * ss(0.5, 0.8, t))
        tag(d, 640, 300, 'Falsa alarma', win(t, 0.7, L) * ua, v(jm['det_fire']))
        tag(d, 70, 1010, 'La central avisa', win(t, 1.5, L) * ua, None)
    if t > TS2 - DZP:
        lb = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        v = _v_s2B(t, L)
        B.draw_shot(lb, 'ceil_a', t, v.k * B.RES[0] / W, 1.0, window=True)
        jc = B.SHOTS['ceil_a'][2]
        ub = ss(TS2 + DZP - 0.1, TS2 + DZP + 0.2, t)
        tag(d, 640, 820, 'Ampolla intacta: boquilla cerrada', win(t, TS2 + 1.0, L) * ub, v(jc['bulb']))
        tag(d, 70, 1010, 'Sin descarga', win(t, TS2 + 1.8, L) * ub, None)
    if la is not None and lb is not None:
        vA = _v_s2A(t); vB = _v_s2B(t, L)
        lay, _ = zoom_pair(la, lb, p, vA(B.SHOTS['med'][2]['fire_nozzle']), vB(B.SHOTS['ceil_a'][2]['bulb']), 8.0, clip=True)
    else:
        lay = la if la is not None else lb
    img.alpha_composite(V.mclip(lay))
    d = ImageDraw.Draw(img)
    title(d, 'SEGURIDAD DE LA PREACCIÓN', 'Falsa alarma de detección', ss(0.2, 0.7, t))
    subtitle(d, 'Y si la detección da una falsa alarma, la central avisa, pero tampoco hay descarga.', win(t, 0.5, TS2 + 0.4))
    subtitle(d, 'Sin fuego no se rompe ninguna ampolla y las boquillas permanecen cerradas.', win(t, TS2 + 0.4, L))


SCENES = [(0.0, 2.4, B.sc_intro, False), (2.4, 7.8, V.sc_fm, True), (7.8, 13.2, V.sc_start, False),
          (13.2, 21.2, sc_detect, False), (21.2, 33.2, sc_preaction, True), (33.2, 40.4, V.sc_activation, False),
          (40.4, 52.4, sc_pump2, True), (52.4, 60.0, V.sc_discharge, False), (60.0, 68.0, sc_floor, False),
          (68.0, 73.4, V.sc_ext, True), (73.4, 83.4, sc_safety1, False), (83.4, 92.4, sc_safety2, False),
          (92.4, 120.8, sc_uac, True), (120.8, 123.8, V.sc_outro, False)]
DUR = 123.8

# anclajes con la locución: (tiempo local original, bloque, frase ES/EN o None = inicio del bloque)
ANCHORS = {
    3: [(TD_A + 0.6, 2, {'es': 'la central de detección', 'en': 'the detection panel'})],
    4: [(TP_B + 0.4, 3, {'es': 'Cada zona tiene', 'en': 'Each zone has'}), (9.4, 3, {'es': 'Al recibir la señal', 'en': 'When it receives'})],
    5: [(V.T_BREAK + 1.2, 4, {'es': 'y solo esa', 'en': 'and only that'})],
    6: [(TZ2 + 0.6, 5, {'es': 'El motor eléctrico', 'en': 'The electric motor'}), (TC2 + 0.3, 5, {'es': 'y el agua circula', 'en': 'and water flows'})],
    7: [(4.4, 6, {'es': 'Es eficaz', 'en': 'It is effective'})],
    10: [(TS1 + 0.4, 9, {'es': 'y el presostato', 'en': "and the valve's"})],
    11: [(TS2 + 0.4, 10, {'es': 'sin fuego no', 'en': 'with no fire'})],
    12: [(TV, 11, {'es': 'Cada generador tiene', 'en': 'Each generator has'}), (UF, 12, None), (CA0 + 1.0, 13, None)],
}
SCENE_TAIL = {12: 4.0}   # tiempo extra tras la voz (escenas con varias fases después de la última frase)
# bloques de locución por escena (en orden)
SCENE_BLOCKS = {1: [0], 2: [1], 3: [2], 4: [3], 5: [4], 6: [5], 7: [6], 8: [7], 9: [8], 10: [9], 11: [10], 12: [11, 12, 13]}


def M_wide_med(tA, LA, tB, LB):
    vA = B.View(0.86 + 0.05 * ss(0, LA, tA), 0, 60)
    vB = B.View(1.0 + 0.06 * ss(0, LB, tB))
    return matched(vA(B.SHOTS['wide'][2]['fire']), kp_screen('wide', vA), kp_screen('med', vB))


def M_med_med(tA, LA, tB, LB):
    vA = B.View(1.0 + 0.06 * ss(0, LA, tA)); vB = _v_detA(tB)
    return matched(vA(B.SHOTS['med'][2]['fire']), kp_screen('med', vA), kp_screen('med', vB))


def M_det_pre(tA, LA, tB, LB):
    vA = _v_detB(tA, LA); vB = _v_preA(tB)
    return matched(vA(B.SHOTS['wide'][2]['pav'][0]), kp_screen('wide', vA), kp_screen('proom2', vB))


def M_med_floor(tA, LA, tB, LB):
    vA = B.View(1.06 + 0.06 * ss(0, LA, tA))
    vB = B.View(1.0 + 0.04 * ss(0, T2, min(tB, T2)))
    return matched(vA(B.SHOTS['med'][2]['fire']), kp_screen('med', vA), kp_screen('floor', vB))


def M_det_ext(tA, LA, tB, LB):
    vA = B.View(1.0 + 0.05 * ss(T2, LA, tA))
    vB = B.View(0.92 + 0.04 * ss(0, LB, tB), 0, 40)
    fA, fB, _ = matched(vA(B.SHOTS['floor_det'][2]['uf_noz'][1]), kp_screen('floor_det', vA), kp_screen('wide', vB))
    return fA, fB, 1 / 7.0


def M_ceil_uac(tA, LA, tB, LB):
    vA = _v_s2B(tA, LA)
    vB = B.View(0.95 + 0.04 * ss(0, TU1, min(tB, TU1)), 0, 60)
    return vA(B.SHOTS['ceil_a'][2]['bulb']), vB(B.SHOTS['wide'][2]['fire_nozzle']), 1 / 6.0


# transición tras la escena i: (tipo, semiduración, función de cámara -> (fA, fB, R), -)
TRANS = {1: ('zin', 0.8, M_wide_med, None), 2: ('match', 0.6, M_med_med, None), 3: ('zin', 0.8, M_det_pre, None),
         7: ('zout', 0.8, M_med_floor, None), 8: ('zout', 0.8, M_det_ext, None), 11: ('zout', 0.8, M_ceil_uac, None)}
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
    B.flush_tags(img)
    if B.UIL[0] is not None:
        img.alpha_composite(B.UIL[0]); B.UIL[0] = None
    if ui and fn not in NO_LOCK:
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
    B.flush_tags(img)
    ui = B.UIL[0]; B.UIL[0] = None; B.NOFADE[0] = False
    return img, ui, fn not in NO_LOCK, (BG if band else BG_PLAIN)


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


# =====================================================================================
# piezas autoconclusivas para LinkedIn (solo 4:5)
#   cada pieza: gancho sobre la imagen (0–HOOK s) -> una historia completa -> cierre con frase + web
#   sin «capítulo n/N» ni «próximo capítulo»: se entienden solas aunque se publiquen con semanas de diferencia
# =====================================================================================
PIECES = [
    dict(slug='Incendio-rack', hook='Arde un rack. ¿Cómo se apaga sin mojar el resto de la sala?',
         scenes=[2, 3, 5, 7, 9], steps=({1: 1, 2: 2, 4: 3, 6: 4, 8: 5}, 5)),
    dict(slug='Preaccion', hook='¿Y si una ampolla se rompe por accidente sobre los servidores?',
         scenes=[4, 10, 11], steps=({}, 0)),
    dict(slug='Falso-suelo', hook='Un centro de datos tiene dos zonas que proteger: la sala y el falso suelo.',
         scenes=[1, 8], steps=({}, 0)),
    dict(slug='Generadores', hook='¿Cómo se protege un generador sin bombas ni corriente eléctrica?',
         scenes=[12], steps=({}, 0)),
]
KICKER = 'RG W-FOG · CENTROS DE DATOS'
PC_CUR = [0]
HOOK = 3.2                       # s que dura el gancho sobre la primera escena
F_HK = B.F('Inter-Bold.otf', 22)
F_HT = B.F('InterDisplay-Bold.otf', 50)
F_CHN = B.F('InterDisplay-Medium.otf', 30)


def hooked(fn):
    """primera escena de la pieza: el gancho ocupa la cabecera y la cabecera de la escena entra después"""
    def f(t, L, img):
        B.HDR_A[0] = ss(HOOK, HOOK + 0.5, t)
        try:
            fn(t, L, img)
        finally:
            B.HDR_A[0] = 1.0
        a = ss(0.0, 0.35, t) * (1 - ss(HOOK - 0.4, HOOK, t))
        if a <= 0.01 or not B.UI[0]:
            return
        d = B._ud(ImageDraw.Draw(img))
        pc = PIECES[PC_CUR[0]]
        d.text((S(70), S(92)), KICKER, font=F_HK, fill=B.ca(B.RED, a))
        y = 128
        for ln in B.wrap(pc['hook'], F_HT, 930):
            d.text((S(70), S(y)), ln, font=F_HT, fill=B.ca(B.INK, a)); y += 58
        d.rounded_rectangle([S(70), S(y + 14), S(134), S(y + 21)], radius=S(3.5), fill=B.ca(B.RED, a))
    f.__name__ = 'hooked_' + fn.__name__
    return f


def sc_close(t, L, img):
    """cierre de cada pieza: firma + frase + web (igual en todas)"""
    a = ss(0.1, 0.7, t)
    img.alpha_composite(B.fade_img(B.LOCK, a), (S(W / 2) - B.LOCK.width // 2, S(H / 2 - 150) - B.LOCK.height // 2))
    d = ImageDraw.Draw(img)
    for i, (txt, f_, c) in enumerate([('Protección contra incendios para centros de datos', F_CHN, B.INK), ('www.rg-systems.com', B.F_SMB, B.RED)]):
        d.text((S(W / 2) - f_.getlength(TR(txt)) / 2, S(H / 2 - 20 + i * 52)), txt, font=f_, fill=B.ca(c, ss(0.5, 1.1, t)))


NO_LOCK = (B.sc_intro, V.sc_outro, sc_close)
