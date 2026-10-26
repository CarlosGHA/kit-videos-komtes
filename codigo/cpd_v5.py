"""v5: planos detalle en sección con los renders reales de la boquilla MM-P50 y del grupo de bombeo RG."""
import math, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import cpd_v4 as V
import cpd_video as B
from cpd_video import (W, H, SS, FPS, S, SW, ca, ss, win, clamp, fade_img, full, low, up, Cloud, spray, tag, card,
                       BG, BG_PLAIN, LOCK_S, INK, INK2, RED, WHITE, MISTC, F_SM, F_SMB, title, subtitle)
from cpd_v4 import step_header, gauge

U = B.SP + 'assets/user/'


def prep_nozzle(name, cx, red_box, holes_rows):
    im = Image.open(U + name + '.png').convert('RGBA')
    a = np.array(im).astype(np.int32)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    # placa/techo morado del CAD -> gris claro neutro
    pur = (b > r + 12) & (b > g + 8) & (al > 60)
    ys = np.arange(a.shape[0])[:, None]
    pur &= ys > 60
    lum = a[..., :3].mean(-1)
    a[pur, 0] = np.clip(lum[pur] * 0.98 + 18, 0, 255); a[pur, 1] = np.clip(lum[pur] * 0.99 + 20, 0, 255); a[pur, 2] = np.clip(lum[pur] + 24, 0, 255)
    intact = Image.fromarray(a.astype(np.uint8))
    # variante rota: sustituir líquido rojo por el interior de la ranura
    x0, x1, y0, y1 = red_box
    red = (r > 120) & (r - b > 45) & (al > 60)
    red[:y0 - 3] = False; red[y1 + 4:] = False
    brk = a.copy()
    ring = np.zeros_like(red); ring[y0:y1, max(0, x0 - 4):x0 - 1] = True; ring[y0:y1, x1 + 2:x1 + 5] = True
    col = np.median(a[ring & (al > 200)][:, :3], axis=0) if (ring & (al > 200)).any() else np.array([150, 152, 156])
    brk[red, 0:3] = col
    broken = Image.fromarray(brk.astype(np.uint8))
    return intact, broken, (cx, (y0 + y1) / 2), holes_rows


CEIL_I, CEIL_B, CEIL_BULB, CEIL_HOLES = prep_nozzle(
    'noz_ceil', 158, (154, 161, 216, 258),
    [(124, 165), (133, 166), (141, 165), (149, 166), (157, 163), (127, 179), (146, 180), (192, 179), (133, 195), (152, 195), (189, 195)])
FLR_I, FLR_B, FLR_BULB, FLR_HOLES = prep_nozzle(
    'noz_floor', 70, (66, 73, 220, 261),
    [(46, 172), (59, 173), (67, 170), (40, 184), (60, 185), (104, 184), (46, 199), (65, 200), (102, 199)])
PUMP = Image.open(U + 'pump.png').convert('RGBA')
PUMP_OFF = (67, 42)


def sharp(im, k):
    w, h = int(im.width * k * SS), int(im.height * k * SS)
    out = im.resize((w, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2 * SS, percent=60, threshold=2))
    return out


CEIL_K = 1.85
CEIL_I_S, CEIL_B_S = sharp(CEIL_I, CEIL_K), sharp(CEIL_B, CEIL_K)
FLR_K = 1.45
FLR_I_S, FLR_B_S = sharp(FLR_I, FLR_K), sharp(FLR_B, FLR_K)


def hatch(d, box, col, step=14, a=1.0):
    x0, y0, x1, y1 = box
    for x in range(int(x0) - int(y1 - y0), int(x1), step):
        xa, ya, xb, yb = x, y1, x + (y1 - y0), y0
        # recorte simple a la caja
        if xa < x0:
            ya -= (x0 - xa); xa = x0
        if xb > x1:
            yb += (xb - x1); xb = x1
        d.line([(S(xa), S(ya)), (S(xb), S(yb))], fill=ca(col, a), width=SW(1))


def hole_dirs(holes, cx):
    out = []
    for hx, hy in holes:
        dx = (hx - cx)
        if abs(dx) < 8:
            ang = math.pi / 2 + (0.35 if dx >= 0 else -0.35)
        else:
            ang = math.pi / 2 - math.copysign(math.radians(58), dx)
        out.append(((hx, hy), ang))
    return out


CL_C = [Cloud(300 + i, 1500, 3.35, 9.0, (0.5, 1.15), 0.24, (230, 380)) for i in range(11)]
T_BRK = 3.1


def sc_ceil_section(t, L, img):
    # plano detalle en sección del falso techo con la boquilla real
    ox, oy = 540 - CEIL_BULB[0] * CEIL_K, 300    # esquina sup. izq. de la imagen de la boquilla
    P = lambda px, py: (ox + px * CEIL_K, oy + py * CEIL_K)
    a0 = ss(0, 0.5, t)
    d = ImageDraw.Draw(img)
    plate_y = P(0, 125)[1]
    # calor desde abajo
    heat = ss(0.2, 2.6, t) * (1 - ss(4.5, 6.5, t))
    if heat > 0:
        glow, gd = low()
        for rr, al in ((460, 55), (300, 85), (170, 115)):
            r = rr * (0.6 + 0.4 * heat) / 4
            gd.ellipse([540 / 4 - r, 1180 / 4 - r, 540 / 4 + r, 1180 / 4 + r], fill=(255, 110, 30, int(al * heat)))
        img.alpha_composite(up(glow, 14))
    d = ImageDraw.Draw(img)
    # plenum: tubería que baja a la boquilla
    pc = (200, 204, 210); pd = (150, 154, 160)
    py_ = 262
    d.rectangle([S(0), S(py_ - 20), S(540 - 6), S(py_ + 20)], fill=ca(pc, a0))
    d.line([(S(0), S(py_ - 20)), (S(534), S(py_ - 20))], fill=ca(pd, a0), width=SW(2))
    d.line([(S(0), S(py_ + 20)), (S(518), S(py_ + 20))], fill=ca(pd, a0), width=SW(2))
    d.pieslice([S(540 - 46), S(py_ - 20), S(540 + 34), S(py_ + 60)], 270, 360, fill=ca(pc, a0))
    d.rectangle([S(540 - 18), S(py_ + 10), S(540 + 18), S(oy + 6)], fill=ca(pc, a0))
    # falso techo seccionado
    ty0, ty1 = plate_y - 10, plate_y + 10
    for (x0, x1) in ((0, 540 - 150), (540 + 150, W)):
        d.rectangle([S(x0), S(ty0), S(x1), S(ty1)], fill=ca((228, 229, 231), a0), outline=ca((170, 173, 178), a0), width=SW(1))
        hatch(d, (x0, ty0, x1, ty1), (185, 188, 193), 12, a0)
    d.text((S(70), S(ty1 + 10)), 'Falso techo', font=F_SM, fill=ca(INK2, a0))
    d.text((S(70), S(ty0 - 34)), 'Plenum', font=F_SM, fill=ca(INK2, a0))
    # boquilla
    nz = CEIL_I_S if t < T_BRK else CEIL_B_S
    img.alpha_composite(fade_img(nz, a0), (int(S(ox)), int(S(oy))))
    over, od = full(); fog, fd = low()
    # humo acumulado bajo el techo
    sm = ss(0.5, 2.6, t) * (1 - ss(5.0, 7.0, t))
    if sm > 0:
        for i in range(18):
            ph = (t * 0.12 + i / 18) % 1
            x = -100 + ph * 1300; y = ty1 + 90 + math.sin(i * 1.9 + t) * 40 - 30 * ph
            r = (90 + 30 * math.sin(i)) / 4
            fd.ellipse([x / 4 - r, y / 4 - r * 0.5, x / 4 + r, y / 4 + r * 0.5], fill=(120, 122, 127, int(80 * sm)))
    bulb = P(*CEIL_BULB)
    if heat > 0.05:
        for k in range(5):
            xs = 540 - 90 + k * 45
            pts = [(S(xs + 6 * math.sin(j * 0.8 + t * 6 + k)), S(1150 - j * 18 - ((t * 90) % 18))) for j in range(16)]
            od.line(pts, fill=(255, 150, 80, int(70 * heat)), width=SW(2))
    if T_BRK < t < T_BRK + 1.4:
        tb = t - T_BRK
        rng = np.random.default_rng(5)
        for i in range(18):
            ang = rng.uniform(0, 6.28); spd = rng.uniform(140, 300)
            px = bulb[0] + math.cos(ang) * spd * tb; py = bulb[1] + math.sin(ang) * spd * tb + 380 * tb * tb
            r = 6; rot = rng.uniform(-8, 8) * tb
            od.polygon([(S(px + r * math.cos(rot + q)), S(py + r * math.sin(rot + q))) for q in (0, 2.3, 4.2)],
                       fill=(205, 215, 225, int(230 * clamp(1 - tb / 1.3))))
            if i < 8:
                od.ellipse([S(px - 3), S(py - 3), S(px + 3), S(py + 3)], fill=(225, 50, 40, int(220 * clamp(1 - tb))))
    for cl, ((hx, hy), ang) in zip(CL_C, hole_dirs(CEIL_HOLES, CEIL_BULB[0])):
        X, Y = P(hx, hy)
        spray(od, fd, cl, t, X, Y, ang, 1.25, 1.0, drag=1.8, grav=110, fog_a=42, dot_a=240, col=(100, 158, 220))
    img.alpha_composite(up(fog, 6)); img.alpha_composite(over)
    d = ImageDraw.Draw(img)
    step_header(d, 2, 'ACTIVACIÓN', 'Boquilla cerrada de techo · detalle en sección', ss(0.2, 0.7, t))
    tag(d, 700, 860, 'Ampolla térmica', win(t, 0.8, T_BRK + 0.2), bulb)
    tag(d, 700, 470, 'Embellecedor', win(t, 1.2, T_BRK), P(300, 127))
    tag(d, 700, 860, 'Micro-orificios', win(t, T_BRK + 1.0, L - 0.2), P(*CEIL_HOLES[9]))
    subtitle(d, 'El calor del incendio sube hasta el techo y calienta la ampolla térmica de la boquilla más próxima al foco.',
             win(t, 0.5, T_BRK + 0.1))
    subtitle(d, 'Al alcanzar su temperatura de tarado, la ampolla rompe y solo esa boquilla se abre.', win(t, T_BRK + 0.1, L))


CL_F = [Cloud(400 + i, 1400, 0.6, 9.0, (0.5, 1.1), 0.26, (190, 300)) for i in range(9)]
CL_FD = Cloud(41, 1400, 0.4, 9.0, (2.0, 3.4), 0.5, (70, 160))


def sc_floor_section(t, L, img):
    T2 = 2.6
    if t < T2 + 0.3:
        a = ss(0, 0.5, t) * (1 - ss(T2 - 0.1, T2 + 0.3, t))
        v, js = B.draw_shot(img, 'floor', t, 1.0 + 0.04 * ss(0, T2, t), a, window=True)
        d = ImageDraw.Draw(img)
        tag(d, 80, 930, 'Red bajo suelo técnico', win(t, 0.6, T2) * a, v(js['uf_noz'][1]))
    if t > T2 - 0.1:
        a = ss(T2 - 0.1, T2 + 0.3, t); tt = t - T2
        d = ImageDraw.Draw(img)
        # sección del suelo técnico
        fy0, fy1 = 300, 334           # baldosa
        sy0, sy1 = 1040, 1100         # forjado
        d.rectangle([S(0), S(fy0), S(W), S(fy1)], fill=ca((232, 233, 235), a), outline=ca((165, 168, 173), a), width=SW(1))
        for x in range(0, W, 200):
            d.line([(S(x), S(fy0)), (S(x), S(fy1))], fill=ca((165, 168, 173), a), width=SW(2))
        hatch(d, (0, fy0, W, fy1), (190, 192, 197), 12, a)
        d.rectangle([S(0), S(sy0), S(W), S(sy1)], fill=ca((214, 210, 203), a))
        hatch(d, (0, sy0, W, sy1), (178, 172, 163), 16, a)
        for px in (200, 800):
            d.rectangle([S(px - 7), S(fy1), S(px + 7), S(sy0)], fill=ca((150, 154, 160), a))
            d.rectangle([S(px - 30), S(fy1), S(px + 30), S(fy1 + 10)], fill=ca((150, 154, 160), a))
            d.rectangle([S(px - 30), S(sy0 - 10), S(px + 30), S(sy0)], fill=ca((150, 154, 160), a))
        # bandeja y cables (sección)
        d.rectangle([S(560), S(960), S(1040), S(972)], fill=ca((175, 178, 183), a))
        for i in range(12):
            cx_ = 590 + i * 38; col = (60, 120, 205) if i % 3 else (225, 175, 40)
            d.ellipse([S(cx_ - 17), S(925), S(cx_ + 17), S(959)], fill=ca(col, a))
            d.ellipse([S(cx_ - 17 + 22), S(892), S(cx_ + 17 + 22), S(926)], fill=ca((60, 120, 205) if i % 2 else (40, 44, 50), a)) if i < 11 else None
        # tubería del ramal
        py0, py1 = 360, 392
        d.rectangle([S(0), S(py0), S(W), S(py1)], fill=ca((200, 204, 210), a))
        d.line([(S(0), S(py0)), (S(W), S(py0))], fill=ca((150, 154, 160), a), width=SW(2))
        d.line([(S(0), S(py1)), (S(W), S(py1))], fill=ca((150, 154, 160), a), width=SW(2))
        d.text((S(70), S(fy0 - 34)), 'Suelo técnico', font=F_SM, fill=ca(INK2, a))
        d.text((S(70), S(sy1 + 6)), 'Forjado', font=F_SM, fill=ca(INK2, a))
        # boquilla real colgada del ramal
        ox, oy = 380 - FLR_BULB[0] * FLR_K, py1 - 4
        P = lambda px, py: (ox + px * FLR_K, oy + py * FLR_K)
        nz = FLR_I_S if tt < 2.2 else FLR_B_S
        img.alpha_composite(fade_img(nz, a), (int(S(ox)), int(S(oy))))
        over, od = full(); fog, fd = low(); glow, gd = low()
        # conato en el cableado
        fl = ss(0.0, 1.0, tt) * (1 - ss(3.0, 5.0, tt))
        if fl > 0:
            for rr, al in ((140, 70), (80, 120)):
                r = rr / 4
                gd.ellipse([720 / 4 - r, 905 / 4 - r, 720 / 4 + r, 905 / 4 + r], fill=(255, 110, 25, int(al * fl)))
            img.alpha_composite(up(glow, 8))
            B.flames(od, gd, 720, 900, 30 * fl, t)
            B.smoke(fd, t, 720, 890, 0.8, fl, spread_x=1.2)
        bulb = P(*FLR_BULB)
        if 2.2 < tt < 3.6:
            tb = tt - 2.2; rng = np.random.default_rng(7)
            for i in range(12):
                ang = rng.uniform(0, 6.28); spd = rng.uniform(90, 200)
                px = bulb[0] + math.cos(ang) * spd * tb; py = bulb[1] + math.sin(ang) * spd * tb + 300 * tb * tb
                od.ellipse([S(px - 3), S(py - 3), S(px + 3), S(py + 3)], fill=(225, 50, 40, int(220 * clamp(1 - tb))))
        for cl, ((hx, hy), ang) in zip(CL_F, hole_dirs(FLR_HOLES, FLR_BULB[0])):
            X, Y = P(hx, hy)
            spray(od, fd, cl, tt - 1.8, X, Y, ang, 1.15, a, drag=1.6, grav=70, fog_a=46, dot_a=245, col=(96, 150, 210))
        spray(od, fd, CL_FD, tt - 2.6, 380, 760, math.radians(8), 1.4, a * ss(2.8, 4.0, tt), drag=0.5, grav=4, fog_a=55,
              dot_a=170, col=(96, 150, 210))
        img.alpha_composite(up(fog, 6)); img.alpha_composite(over)
        d = ImageDraw.Draw(img)
        tag(d, 90, 860, 'Boquilla cerrada bajo suelo', win(tt, 0.3, L - T2 - 0.2), P(FLR_BULB[0], 120))
    d = ImageDraw.Draw(img)
    step_header(d, 5, 'BAJO EL SUELO TÉCNICO', 'Detalle en sección', ss(0.2, 0.7, t))
    subtitle(d, 'Si el fuego se inicia en el cableado bajo el suelo técnico, actúa su propia red con el mismo principio.',
             win(t, 0.5, T2 + 2.4))
    subtitle(d, 'La niebla llega a los huecos entre cables y aglutina las partículas de humo.', win(t, T2 + 2.4, L))


PUMP2 = Image.open(U + 'pump2.png').convert('RGBA')


def sc_pump(t, L, img):
    k = 0.86 + 0.04 * ss(0, L, t)
    on = ss(1.9, 2.1, t)
    jit = (math.sin(t * 70) * 0.7 if on > 0.5 else 0)
    cx, cy = 540, 790
    w, h = int(PUMP2.width * k * SS), int(PUMP2.height * k * SS)
    im = PUMP2.resize((w, h), Image.LANCZOS)
    img.alpha_composite(fade_img(im, 1.0 if B.NOFADE[0] else ss(0, 0.5, t)), (int(S(cx + jit) - w / 2), int(S(cy) - h / 2)))
    P = lambda px, py: (cx + (px - PUMP2.width / 2) * k, cy + (py - PUMP2.height / 2) * k)
    d = ImageDraw.Draw(img)
    step_header(d, 3, 'ARRANQUE DEL BOMBEO', 'Grupo de bombeo RG W-FOG UAP', ss(0.2, 0.7, t))
    gauge(img, t, ss(0.3, 0.8, t), (720, 236, 1010, 480))
    d = ImageDraw.Draw(img)
    tag(d, 70, 300, 'Bomba de alta presión', win(t, 2.0, L - 0.2), P(445, 425))
    tag(d, 700, 1096, 'Motor eléctrico', win(t, 2.4, L - 0.2), P(760, 300))
    subtitle(d, 'La apertura de la boquilla hace caer la presión de la red; el grupo lo detecta y arranca la bomba de alta presión.',
             win(t, 0.5, L))


def sc_other(t, L, img):
    v, js = B.draw_shot(img, 'cyl', t, 0.74 + 0.04 * ss(0, L, t), ss(0, 0.5, t), dy=-20)
    d = ImageDraw.Draw(img)
    title(d, 'OTROS RIESGOS DEL EDIFICIO', 'Generadores y transformadores · RG W-FOG UAC', ss(0.2, 0.7, t))
    tag(d, 120, 400, 'Cilindro de N₂', win(t, 0.9, L - 0.3), v(js['n2']))
    subtitle(d, 'Para salas de generadores y transformadores del edificio: baterías de cilindros de agua y nitrógeno, sin bombas ni corriente eléctrica.',
             win(t, 0.5, L))


SCENES = [(0.0, 2.4, B.sc_intro, False), (2.4, 7.8, V.sc_fm, True), (7.8, 13.2, V.sc_start, False),
          (13.2, 20.4, sc_ceil_section, False), (20.4, 25.8, sc_pump, False), (25.8, 33.4, V.sc_discharge, False),
          (33.4, 41.4, sc_floor_section, False), (41.4, 46.8, V.sc_ext, True), (46.8, 51.6, sc_other, True),
          (51.6, 54.6, V.sc_outro, False)]
DUR = 54.6
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
            if fn not in (B.sc_intro, V.sc_outro):
                img.alpha_composite(LOCK_S, (S(1010) - LOCK_S.width, S(60)))
            out = img if out is None else Image.blend(out, img, al)
    return out.convert('RGB').resize((W, H), Image.LANCZOS).tobytes()


if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[3:]:
            Image.frombytes('RGB', (W, H), render(int(float(ts) * FPS))).save(f'{sys.argv[2]}/e_{ts}.png')
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
