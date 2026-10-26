"""Vídeo LinkedIn v4 · RG W-FOG en CPD: del inicio del fuego a la extinción, con planos detalle."""
import math, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
import cpd_video as B
from cpd_video import (W, H, SS, FPS, S, SW, ca, ss, win, clamp, fade_img, full, low, up, Cloud, spray, smoke, flames,
                       title, subtitle, tag, card, fit_logo, View, BG, BG_PLAIN, LOCK, LOCK_S, INK, INK2, RED, WHITE,
                       MISTC, F_T1, F_T2, F_SUB, F_SM, F_SMB, LOGO_IM)

R4 = B.SP + 'r4/'


def ld(n):
    return Image.open(R4 + n).convert('RGBA')


def ldj(n):
    return json.load(open(R4 + n))


B.SHOTS['wide'] = (ld('wide.png'), ld('wide_led1.png'), ldj('wide.json'))
B.SHOTS['med'] = (ld('med.png'), ld('med_led1.png'), ldj('med.json'))
B.SHOTS['floor'] = (ld('floor.png'), ld('floor_led1.png'), ldj('floor.json'))
B.SHOTS['floor_det'] = (ld('floor_det.png'), None, ldj('floor_det.json'))
import os
B.SHOTS['floor_det_b'] = (ld('floor_det_b.png') if os.path.exists(R4 + 'floor_det_b.png') else ld('floor_det.png'), None, ldj('floor_det.json'))
B.SHOTS['ceil_a'] = (ld('ceil_a.png'), None, ldj('ceil_a.json'))
B.SHOTS['ceil_b'] = (ld('ceil_b.png'), None, ldj('ceil_b.json'))
B.SHOTS['pump'] = (ld('pump.png'), None, ldj('pump.json'))
B.SHOTS['cyl'] = (ld('cyl.png'), None, ldj('cyl.json'))
draw_shot = B.draw_shot
FM_LOGO = LOGO_IM[0]

def mclip(im):
    a = np.array(im.getchannel('A')).astype(np.float32) * B.WINM
    im.putalpha(Image.fromarray(a.astype(np.uint8))); return im


STEPS = ['Inicio', 'Activación', 'Bombeo', 'Descarga', 'Bajo suelo', 'Extinción']


def step_header(d, n, name, sub, a):
    if not B.UI[0]:
        return
    if a <= 0.01:
        return
    d = B._ud(d)
    d.text((S(70), S(112)), f'{n:02d} · {name}', font=F_T1, fill=ca(INK, a))
    d.text((S(70), S(156)), sub, font=F_T2, fill=ca(INK, a))
    x = 70
    for i in range(6):
        col = RED if i + 1 == n else (INK if i + 1 < n else (215, 217, 220))
        d.rounded_rectangle([S(x), S(206), S(x + 52), S(212)], radius=S(3), fill=ca(col, a))
        x += 60


# ---------------- escenas ----------------
def sc_fm(t, L, img):
    v, js = draw_shot(img, 'wide', t, 0.86 + 0.05 * ss(0, L, t), ss(0, 0.5, t), dy=60)
    d = ImageDraw.Draw(img)
    title(d, 'CENTROS DE DATOS', 'Agua nebulizada RG W-FOG', ss(0.2, 0.7, t))
    a = ss(0.7, 1.3, t)
    if a > 0 and B.UI[0]:
        dy = 18 * (1 - a)
        box = (610, 250 + dy, 1010, 420 + dy)
        card(img, box, a)
        fit_logo(img, FM_LOGO, (box[0] + 10, box[1] + 10, box[0] + 170, box[3] - 10), a, pad=14)
        du = ImageDraw.Draw(B.uiimg(img))
        du.text((S(box[0] + 186), S(box[1] + 44)), 'Certificación', font=F_T2, fill=ca(INK, a))
        du.text((S(box[0] + 186), S(box[1] + 80)), 'FM', font=B.F_STAT, fill=ca(RED, a))
        d = ImageDraw.Draw(img)
    subtitle(d, 'Protección contra incendios con certificación FM para centros de datos: sobre y bajo suelo técnico.', win(t, 0.6, L))


def fire_fx(img, v, js, t, lvl_glow, fsize, smoke_lvl, t_smoke):
    glow, gd = low(); fog, fd = low(); fl, fld = full()
    p = v(js['fire']); pt = v(js['fire_top'])
    fk = 0.85 + 0.15 * math.sin(t * 11) * math.sin(t * 7.3)
    for rr, al in ((120, 70), (75, 120), (40, 170)):
        r = rr * (0.5 + 0.5 * lvl_glow) / 4
        gd.ellipse([p[0] / 4 - r * 0.55, p[1] / 4 - r * 1.4, p[0] / 4 + r * 0.55, p[1] / 4 + r * 1.2],
                   fill=(255, 105, 20, int(al * lvl_glow * fk)))
    flames(fld, gd, pt[0], pt[1] + 8, fsize, t)
    img.alpha_composite(up(glow, 6)); img.alpha_composite(fl)
    smoke(fd, t_smoke, pt[0], pt[1], 1.0, smoke_lvl, spread_x=1.6)
    img.alpha_composite(up(fog, 7))
    return p, pt


def sc_start(t, L, img):
    v, js = draw_shot(img, 'med', t, 1.0 + 0.06 * ss(0, L, t), ss(0, 0.5, t), window=True)
    lvl = ss(0.4, 3.0, t)
    p, pt = fire_fx(img, v, js, t, lvl, 58 * ss(1.4, 3.2, t), ss(1.0, 3.5, t), t)
    d = ImageDraw.Draw(img)
    step_header(d, 1, 'INICIO DEL FUEGO', 'Sobrecalentamiento en un rack', ss(0.2, 0.7, t))
    tag(d, pt[0] + 70, pt[1] - 170, 'Foco en rack', win(t, 1.2, L - 0.3), (pt[0], pt[1] + 20))
    subtitle(d, 'El calor, el humo y los gases corrosivos de un solo equipo amenazan a toda la sala.', win(t, 0.6, L))


CL_CEIL = [Cloud(100 + i, 900, 3.35, 9.0, (0.5, 1.1), 0.14, (240, 380)) for i in range(16)]
T_BREAK = 3.1


def sc_activation(t, L, img):
    name = 'ceil_a' if t < T_BREAK else 'ceil_b'
    zoom = 1.0 + 0.05 * ss(0, L, t)
    # calor y humo que suben desde abajo (antes de la imagen para quedar detrás de la boquilla)
    heat = ss(0.2, 2.6, t) * (1 - ss(4.5, 6.5, t))
    v = View(zoom, 0, 0)
    js = B.SHOTS['ceil_a'][2]
    bulb = v(js['bulb'])
    if heat > 0:
        glow, gd = low()
        for rr, al in ((420, 60), (260, 90), (140, 120)):
            r = rr * (0.6 + 0.4 * heat) / 4
            gd.ellipse([bulb[0] / 4 - r, (bulb[1] + 260) / 4 - r, bulb[0] / 4 + r, (bulb[1] + 260) / 4 + r],
                       fill=(255, 110, 30, int(al * heat)))
        img.alpha_composite(up(glow, 14))
    draw_shot(img, name, t, zoom, ss(0, 0.5, t), window=True)
    over, od = full(); fog, fd = low()
    # humo acumulándose bajo el techo
    sm = ss(0.5, 2.6, t) * (1 - ss(5.0, 7.0, t))
    if sm > 0:
        for i in range(16):
            ph = (t * 0.12 + i / 16) % 1
            x = -100 + ph * 1300; y = bulb[1] + 120 + math.sin(i * 1.9 + t) * 40 - 60 * ph
            r = (90 + 30 * math.sin(i)) / 4
            fd.ellipse([x / 4 - r, y / 4 - r * 0.55, x / 4 + r, y / 4 + r * 0.55], fill=(130, 132, 137, int(70 * sm)))
    # columna de aire caliente (ondas)
    if heat > 0.05:
        for k in range(5):
            xs = bulb[0] - 80 + k * 40
            pts = []
            for j in range(18):
                yy = bulb[1] + 420 - j * 18 - ((t * 90) % 18)
                pts.append((S(xs + 6 * math.sin(j * 0.8 + t * 6 + k)), S(yy)))
            od.line(pts, fill=(255, 150, 80, int(70 * heat)), width=SW(2))
    # rotura de la ampolla
    if T_BREAK < t < T_BREAK + 1.4:
        tb = t - T_BREAK
        rng = np.random.default_rng(5)
        for i in range(18):
            ang = rng.uniform(0, 6.28); spd = rng.uniform(160, 340)
            px = bulb[0] + math.cos(ang) * spd * tb; py = bulb[1] + math.sin(ang) * spd * tb + 380 * tb * tb
            r = 6; rot = rng.uniform(-8, 8) * tb
            od.polygon([(S(px + r * math.cos(rot + q)), S(py + r * math.sin(rot + q))) for q in (0, 2.3, 4.2)],
                       fill=(205, 215, 225, int(230 * clamp(1 - tb / 1.3))))
            if i < 8:
                od.ellipse([S(px - 3), S(py - 3), S(px + 3), S(py + 3)], fill=(225, 50, 40, int(220 * clamp(1 - tb))))
    # niebla desde los micro-orificios
    for cl, (a_, b_) in zip(CL_CEIL, js['orif']):
        p0 = v(a_); p1 = v(b_)
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        k = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / 260
        spray(od, fd, cl, t, p0[0], p0[1], ang, max(0.6, k), 1.0, drag=2.2, grav=90, fog_a=34, dot_a=235)
    img.alpha_composite(mclip(up(fog, 6))); img.alpha_composite(mclip(over))
    d = ImageDraw.Draw(img)
    step_header(d, 2, 'ACTIVACIÓN', 'Boquilla cerrada RG · techo', ss(0.2, 0.7, t))
    tag(d, 640, 820, 'Ampolla térmica', win(t, 0.8, T_BREAK + 0.2), bulb)
    tag(d, 640, 380, 'Embellecedor NS1', win(t, 1.2, T_BREAK), v(js['esc']))
    tag(d, 640, 820, 'Micro-orificios', win(t, T_BREAK + 1.0, L - 0.2), v(js['orif'][0][0]))
    subtitle(d, 'El calor del incendio sube hasta el techo y calienta la ampolla térmica de la boquilla más próxima al foco.',
             win(t, 0.5, T_BREAK + 0.1))
    subtitle(d, 'Al alcanzar su temperatura de tarado, la ampolla rompe y solo esa boquilla se abre.', win(t, T_BREAK + 0.1, L))


def pressure(t):
    p = 0.40
    p -= 0.28 * ss(0.5, 1.3, t)
    p += 0.80 * ss(1.9, 3.2, t)
    if t > 3.2:
        p += 0.012 * math.sin(t * 19)
    return p


def gauge(img, t, a, box):
    if not B.UI[0]:
        return
    img = B.uiimg(img)
    card(img, box, a)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    cx, cy, R = (x0 + x1) / 2, y0 + 120, 82
    d.arc([S(cx - R), S(cy - R), S(cx + R), S(cy + R)], start=150, end=390, fill=ca((220, 222, 225), a), width=SW(10))
    p = clamp(pressure(t))
    d.arc([S(cx - R), S(cy - R), S(cx + R), S(cy + R)], start=150, end=150 + 240 * p, fill=ca(RED, a), width=SW(10))
    th = math.radians(150 + 240 * p)
    d.line([(S(cx), S(cy)), (S(cx + math.cos(th) * (R - 22)), S(cy + math.sin(th) * (R - 22)))], fill=ca(INK, a), width=SW(4))
    d.ellipse([S(cx - 8), S(cy - 8), S(cx + 8), S(cy + 8)], fill=ca(INK, a))
    st = 'Red en reposo' if t < 0.6 else ('Caída de presión' if t < 1.9 else 'Bomba en marcha')
    col = INK if t < 0.6 else RED
    d.text((S(cx) - F_SMB.getlength(st) / 2, S(cy + 60)), st, font=F_SMB, fill=ca(col, a))
    lb = 'Presión en la red'
    d.text((S(cx) - F_SM.getlength(lb) / 2, S(y0 + 14)), lb, font=F_SM, fill=ca(INK2, a))


def sc_pump(t, L, img):
    v, js = draw_shot(img, 'pump', t, 0.78 + 0.04 * ss(0, L, t), ss(0, 0.5, t), dy=-40)
    d = ImageDraw.Draw(img)
    on = ss(1.9, 2.1, t)
    if on > 0:
        c = v(js['cab'])
        fk = 0.6 + 0.4 * math.sin(t * 9)
        d.ellipse([S(c[0] - 9), S(c[1] - 60), S(c[0] + 9), S(c[1] - 42)], fill=ca((40, 210, 90), on * fk))
    step_header(d, 3, 'ARRANQUE DEL BOMBEO', 'Grupo de bombeo RG W-FOG UAP', ss(0.2, 0.7, t))
    gauge(img, t, ss(0.3, 0.8, t), (700, 830, 1010, 1100))
    d = ImageDraw.Draw(img)
    tag(d, 80, 300, 'Bomba de alta presión', win(t, 2.0, L - 0.2), v(js['pump']))
    subtitle(d, 'La apertura de la boquilla hace caer la presión de la red; el cuadro de control lo detecta y arranca la bomba de alta presión.',
             win(t, 0.5, L))


CL_MED = Cloud(3, 2600, 0.0, 12.0, (0.7, 1.4), 0.40, (160, 290))


def sc_discharge(t, L, img):
    v, js = draw_shot(img, 'med', t + 20, 1.06 + 0.06 * ss(0, L, t), ss(0, 0.5, t), window=True)
    lvl = 1 - ss(1.5, 6.5, t)
    over, od = full(); fog, fd = low()
    p, pt = fire_fx(img, v, js, t, lvl, 58 * (1 - ss(1.0, 5.0, t)), 1 - ss(0.8, 4.5, t), t + 8)
    nz = v(js['fire_nozzle'])
    spray(od, fd, CL_MED, t, nz[0], nz[1] + 4, math.pi / 2, 1.0, 1.0, drag=1.5, grav=25, fog_a=30)
    hold = ss(1.0, 4.0, t)
    for i in range(9):
        x = p[0] + (i - 4) * 38 + math.sin(t + i) * 8; y = p[1] - 40 + math.cos(i * 1.7 + t * 0.7) * 30
        r = (70 + 20 * math.sin(i)) / 4
        fd.ellipse([x / 4 - r, y / 4 - r, x / 4 + r, y / 4 + r], fill=MISTC + (int(62 * hold),))
    img.alpha_composite(mclip(up(fog, 7))); img.alpha_composite(mclip(over))
    d = ImageDraw.Draw(img)
    step_header(d, 4, 'DESCARGA LOCALIZADA', 'Microgotas a alta presión', ss(0.2, 0.7, t))
    others = [v(q) for q in js['nozzles']]
    others = [q for q in others if 250 < q[1] < 1050 and math.hypot(q[0] - nz[0], q[1] - nz[1]) > 120]
    if others:
        tag(d, 640, 270, 'Resto de boquillas: cerradas', win(t, 3.2, L - 0.2), min(others, key=lambda q: q[1]))
    tag(d, 70, 960, 'Enfría: absorbe el calor', win(t, 1.0, 4.4))
    tag(d, 70, 1010, 'Sofoca: el vapor desplaza el oxígeno', win(t, 1.4, 4.4))
    subtitle(d, 'La niebla absorbe el calor del foco y el vapor generado desplaza el oxígeno junto a la llama.', win(t, 0.5, 4.4))
    subtitle(d, 'Eficaz con la climatización en marcha y sobre equipos en tensión.', win(t, 4.4, L))


CL_UF = [Cloud(200 + i, 2600, 0.6, 9.0, (0.6, 1.3), 0.45, (170, 290)) for i in range(2)]
CL_UF2 = Cloud(9, 1400, 0.0, 9.0, (2.0, 3.4), 0.5, (70, 160))


def sc_floor(t, L, img):
    T2 = 2.6
    over, od = full(); fog, fd = low()
    if t < T2 + 0.3:
        a = ss(0, 0.5, t) * (1 - ss(T2 - 0.1, T2 + 0.3, t))
        v, js = draw_shot(img, 'floor', t, 1.0 + 0.04 * ss(0, T2, t), a, window=True)
        d = ImageDraw.Draw(img)
        tag(d, 80, 930, 'Red bajo suelo técnico', win(t, 0.6, T2) * a, v(js['uf_noz'][1]))
    if t > T2 - 0.1:
        a = ss(T2 - 0.1, T2 + 0.3, t)
        tt = t - T2
        v, js = draw_shot(img, 'floor_det' if tt < 0.25 else 'floor_det_b', t, 1.0 + 0.05 * ss(T2, L, t), a, window=True)
        nz = v(js['uf_noz'][1])
        if 0.2 < tt < 1.4:
            rng = np.random.default_rng(7)
            tb = tt - 0.2
            for i in range(10):
                ang = rng.uniform(0, 6.28); spd = rng.uniform(60, 140)
                px = nz[0] + math.cos(ang) * spd * tb; py = nz[1] - 10 + math.sin(ang) * spd * tb + 200 * tb * tb
                od.ellipse([S(px - 2.5), S(py - 2.5), S(px + 2.5), S(py + 2.5)], fill=(225, 50, 40, int(220 * clamp(1 - tb))))
        for k_, cl in enumerate(CL_UF):
            spray(od, fd, cl, tt, nz[0], nz[1] - 6, math.radians(150 if k_ else 30), 1.0, a, drag=1.4, grav=60, fog_a=48, dot_a=255, col=(96, 150, 210))
        spray(od, fd, CL_UF2, tt, nz[0], nz[1] + 20, math.radians(10), 1.3, a * ss(0.8, 2.0, tt), drag=0.5, grav=4, fog_a=55, dot_a=170, col=(96, 150, 210))
        img.alpha_composite(mclip(up(fog, 6))); img.alpha_composite(mclip(over))
        d = ImageDraw.Draw(img)
        tag(d, 640, 860, 'Boquilla cerrada', win(tt, 0.3, L - T2 - 0.2), nz)
    d = ImageDraw.Draw(img)
    step_header(d, 5, 'BAJO EL SUELO TÉCNICO', 'Boquilla cerrada RG · bajo suelo', ss(0.2, 0.7, t))
    subtitle(d, 'Bajo el suelo técnico, una red independiente protege los mazos de cables con el mismo principio.', win(t, 0.5, T2 + 1.4))
    subtitle(d, 'La niebla llega a los huecos entre cables y aglutina las partículas de humo.', win(t, T2 + 1.4, L))


def sc_ext(t, L, img):
    v, js = draw_shot(img, 'wide', t, 0.92 + 0.04 * ss(0, L, t), ss(0, 0.5, t), dy=40)
    mist = 1 - ss(0.4, 3.8, t)
    if mist > 0:
        fog, fd = low()
        p = v(js['fire'])
        for i in range(10):
            ang = i * 0.63
            r = (60 + 30 * math.sin(i)) / 4
            x, y = p[0] + math.cos(ang) * 110 + 60, p[1] + math.sin(ang) * 50 - 40
            fd.ellipse([x / 4 - r, y / 4 - r * 0.7, x / 4 + r, y / 4 + r * 0.7], fill=MISTC + (int(80 * mist),))
        img.alpha_composite(up(fog, 8))
    d = ImageDraw.Draw(img)
    step_header(d, 6, 'EXTINCIÓN', 'Vuelta rápida a la actividad', ss(0.2, 0.7, t))
    subtitle(d, 'Fuego extinguido. La niebla restante se disipa con la ventilación y el CPD recupera rápidamente su actividad.', win(t, 0.5, L))


def sc_cyl(t, L, img):
    v, js = draw_shot(img, 'cyl', t, 0.74 + 0.04 * ss(0, L, t), ss(0, 0.5, t), dy=-20)
    d = ImageDraw.Draw(img)
    title(d, 'CPD PEQUEÑOS · RG W-FOG UAC', 'Baterías de cilindros: H₂O + N₂', ss(0.2, 0.7, t))
    tag(d, 120, 400, 'Cilindro de N₂', win(t, 0.9, L - 0.3), v(js['n2']))
    subtitle(d, 'Para salas pequeñas, el agua se impulsa con nitrógeno: compacto y sin bombas ni corriente eléctrica.', win(t, 0.5, L))


def sc_outro(t, L, img):
    a = ss(0.1, 0.8, t)
    img.alpha_composite(fade_img(LOCK, a), (S(W / 2) - LOCK.width // 2, S(H / 2) - LOCK.height // 2 - S(40)))
    d = ImageDraw.Draw(img)
    for i, (txt, f_, c) in enumerate([('Protección contra incendios para centros de datos', F_T2, INK), ('www.komtes.com', F_SMB, RED)]):
        d.text((S(W / 2) - f_.getlength(txt) / 2, S(H / 2 + 50 + i * 48)), txt, font=f_, fill=ca(c, ss(0.6, 1.3, t)))


SCENES = [(0.0, 2.4, B.sc_intro, False), (2.4, 7.8, sc_fm, True), (7.8, 13.2, sc_start, False),
          (13.2, 20.4, sc_activation, False), (20.4, 25.8, sc_pump, True), (25.8, 33.4, sc_discharge, False),
          (33.4, 40.6, sc_floor, False), (40.6, 46.0, sc_ext, True), (46.0, 50.4, sc_cyl, True), (50.4, 53.4, sc_outro, False)]
DUR = 53.4
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
            if fn not in (B.sc_intro, sc_outro):
                img.alpha_composite(LOCK_S, (S(1010) - LOCK_S.width, S(60)))
            out = img if out is None else Image.blend(out, img, al)
    return out.convert('RGB').resize((W, H), Image.LANCZOS).tobytes()


if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[3:]:
            Image.frombytes('RGB', (W, H), render(int(float(ts) * FPS))).save(f'{sys.argv[2]}/d_{ts}.png')
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
