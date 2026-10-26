"""v6: planos 3D de la v4 con la boquilla RG MM-P50 modelada a partir de los renders del fabricante,
grupo de bombeo real y escena de otros riesgos."""
import sys, json, subprocess, os
from PIL import Image
import cpd_video as B
import cpd_v4 as V
import cpd_v5 as V5
from cpd_video import W, H, FPS, S, ss, BG, BG_PLAIN, LOCK_S

R5 = B.SP + 'r5/'


def ld(n):
    return Image.open(R5 + n).convert('RGBA')


def ldj(n):
    return json.load(open(R5 + n))


B.SHOTS['wide'] = (ld('wide.png'), ld('wide_led1.png'), ldj('wide.json'))
B.SHOTS['med'] = (ld('med.png'), ld('med_led1.png'), ldj('med.json'))
B.SHOTS['floor'] = (ld('floor.png'), ld('floor_led1.png'), ldj('floor.json'))
B.SHOTS['floor_det'] = (ld('floor_det.png'), None, ldj('floor_det.json'))
B.SHOTS['floor_det_b'] = (ld('floor_det_b.png'), None, ldj('floor_det.json'))
B.SHOTS['ceil_a'] = (ld('ceil_a.png'), None, ldj('ceil_a.json'))
B.SHOTS['ceil_b'] = (ld('ceil_b.png'), None, ldj('ceil_b.json'))
B.SHOTS['cyl'] = (ld('cyl.png'), None, ldj('cyl.json'))

SCENES = [(0.0, 2.4, B.sc_intro, False), (2.4, 7.8, V.sc_fm, True), (7.8, 13.2, V.sc_start, False),
          (13.2, 20.4, V.sc_activation, False), (20.4, 25.8, V5.sc_pump, False), (25.8, 33.4, V.sc_discharge, False),
          (33.4, 40.6, V.sc_floor, False), (40.6, 46.0, V.sc_ext, True), (46.0, 50.8, V5.sc_other, True),
          (50.8, 53.8, V.sc_outro, False)]
DUR = 53.8
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
            Image.frombytes('RGB', (W, H), render(int(float(ts) * FPS))).save(f'{sys.argv[2]}/f_{ts}.png')
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
