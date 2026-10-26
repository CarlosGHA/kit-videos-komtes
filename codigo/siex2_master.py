"""Montaje SIEX gas: locución + música + efectos, en 4:5 (1440x1800) o 16:9 Full HD (1920x1080).
Uso: python3 cpd_master.py <es|en> <vo.mp3> <45|169> <salida.mp4>   [VO_MODE=--still VO_TS=t1,t2 para fotogramas]"""
import sys, subprocess, re, os, math
LANG, VO, ASPECT, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
sys.argv = ['siex2_final.py', LANG]
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import siex2_final as F
B, V, V5 = F.B, F.V, F.V5
SP = B.SP
SFX = SP + 'sfx/'

# ------------------------------------------------------------------ voz
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', VO, '-af', f"silencedetect=noise=-40dB:d={0.45 if LANG == 'es' else 0.7}", '-f', 'null', '-'],
                   capture_output=True, text=True).stderr
sil = [(float(a), float(b)) for a, b in zip(re.findall(r'silence_start: ([\d.]+)', r), re.findall(r'silence_end: ([\d.]+)', r))]
VODUR = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VO],
                             capture_output=True, text=True).stdout)
NB = len(F.SCENES) - 1
# longitud de texto de cada bloque (para repartir la locución sin depender solo de las pausas)
BLK = {
    'es': [119, 134, 145, 201, 177, 196, 139, 133, 125, 226, 180, 123, 65],
    'en': [86, 82, 128, 160, 143, 136, 70, 110, 61, 168, 140, 92, 62],
}[LANG]
assert len(BLK) == NB
import itertools
thr = 1.4
while True:
    cand = [c for c in sil if c[1] - c[0] >= thr]
    if len(cand) >= NB - 1 or thr < 0.5:
        break
    thr -= 0.1
kps = VODUR / sum(BLK)


def cost(sub):
    st = [0.0] + [b for a, b in sub]; en = [a for a, b in sub] + [VODUR]
    tot_sp = sum(e - s_ for s_, e in zip(st, en)); k = tot_sp / sum(BLK)
    return sum(((e - s_) - k * n) ** 2 / (k * n) for s_, e, n in zip(st, en, BLK))


sep = list(min(itertools.combinations(cand, NB - 1), key=cost))
starts = [0.0] + [b for a, b in sep]
ends = [a for a, b in sep] + [VODUR]
blocks = list(zip(starts, ends))
SPEED = 1.0 if LANG == 'es' else 1.08  # ES v4 con entonación natural: sin acelerar
LEAD, TAIL = 0.3, 0.55
orig = F.SCENES
new = [(0.0, orig[0][1], orig[0][2], orig[0][3], 1.0)]
t = orig[0][1]
vo_place = []
for i in range(1, len(orig)):
    a, b, fn, band = orig[i]
    L0 = b - a
    L = max(L0, LEAD + (blocks[i - 1][1] - blocks[i - 1][0]) / SPEED + TAIL)
    new.append((t, t + L, fn, band, L / L0))
    vo_place.append((t + LEAD, blocks[i - 1]))
    t += L
DUR = t
print('blocks', [(round(a, 2), round(b - a, 2)) for a, b in blocks])
print('scenes', [(round(s[0], 2), round(s[1] - s[0], 2)) for s in new], 'DUR', round(DUR, 2))


def stretch(fn, f):
    if f <= 1.0001:
        return fn
    return lambda tl, L, img: fn(tl / f, L / f, img)


F.SCENES = [(a, b, stretch(fn, f), band) for (a, b, fn, band, f) in new]
TR2 = {}
for k, (kind, D, fa, fb) in F.TRANS.items():
    fA, fB = new[k][4], new[k + 1][4]
    if fa is None:
        TR2[k] = (kind, D, None, None); continue
    TR2[k] = (kind, D, (lambda fa, f1, f2: lambda ta, La, tb, Lb: fa(ta / f1, La / f1, tb / f2, Lb / f2))(fa, fA, fB), None)
F.TRANS = TR2
F.DUR = DUR

# ------------------------------------------------------------------ eventos de sonido (tiempo global)
def g(i, tl):
    """tiempo local original de la escena i -> global"""
    return new[i][0] + tl * new[i][4]


EV = []
for k, (kind, *_r) in F.TRANS.items():
    if kind in ('zin', 'zout'):
        EV.append(('whoosh', new[k][1] - 0.55, 0.15))
EV += [('whoosh', g(4, F.TZ - 0.55), 0.13)]
EV += [('fire', g(2, 0.8), 0.25)]
EV += [('alarm', g(3, F.T_AL), 0.10)]
EV += [('click', g(5, F.T_FIRE), 0.6), ('gas', g(5, F.T_FIRE + 0.3), 0.08)]
EV += [('click', g(6, F.T_OPEN), 0.45), ('click', g(6, F.T_LEV), 0.35)]
EV += [('gas', g(7, F.T_GAS), 0.12), ('gas', g(8, 0.0), 0.08)]


if os.environ.get('VO_TRT'):
    _tr = {('z%d' if F.TRANS.get(k, ('push',))[0] not in ('push', 'cut') else 'push%d') % k:
           (new[k][1], F.TRANS.get(k, ('push', F.PUSH))[1]) for k in range(len(new) - 1)}
    _tr['cyl'] = (g(4, F.TZ), F.DZP * new[4][4])
    print('TRT', __import__('json').dumps(_tr)); sys.exit()


def build_audio(video_in, out):
    vow = out + '.vo.wav'
    fl = []
    for k, (pos, (a, b)) in enumerate(vo_place):
        fl.append(f"[0:a]atrim={max(0, a - 0.05):.3f}:{b + 0.15:.3f},asetpts=PTS-STARTPTS,atempo={SPEED},afade=t=in:d=0.03,"
                  f"afade=t=out:st={(b - a) / SPEED + 0.03:.3f}:d=0.12,adelay={int(pos * 1000)}|{int(pos * 1000)}[v{k}]")
    fl.append(''.join(f'[v{k}]' for k in range(len(vo_place))) + f"amix=inputs={len(vo_place)}:normalize=0,apad=whole_dur={DUR:.3f}[o]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', VO, '-filter_complex', ';'.join(fl), '-map', '[o]', '-ar', '48000', '-ac', '2', vow], check=True)
    inp = ['-i', vow, '-i', SFX + 'music_loop.wav', '-stream_loop', '-1', '-i', SFX + 'amb.mp3']
    names = {'whoosh': 'whoosh.mp3', 'fire': 'fire.mp3', 'gas': 'gas.mp3', 'alarm': 'alarm.mp3', 'click': 'click.mp3'}
    idx = {}
    for nm, fn in names.items():
        if os.path.exists(SFX + fn):
            idx[nm] = 3 + len(idx); inp += ['-i', SFX + fn]
    vi = 3 + len(idx); inp += ['-i', video_in]
    fl = [f"[0:a]atrim=0:{DUR:.3f},asplit=2[vo][key]"]
    fl.append(f"[1:a]atrim=0:{DUR:.3f},afade=t=in:d=1.2,afade=t=out:st={DUR - 2.5:.3f}:d=2.5,volume=0.26[mus0]")
    fl.append("[mus0][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[mus]")
    fl.append(f"[2:a]atrim=0:{DUR:.3f},afade=t=in:d=1.5,afade=t=out:st={DUR - 2:.3f}:d=2,volume=0.06[amb]")
    sfx_labels = []
    for j, (nm, at, vol) in enumerate(EV):
        if nm not in idx:
            continue
        d = int(max(0, at) * 1000)
        fl.append(f"[{idx[nm]}:a]volume={vol},afade=t=out:st=5.0:d=1.5,adelay={d}|{d}[s{j}]")
        sfx_labels.append(f'[s{j}]')
    mix_in = '[vo][mus][amb]' + ''.join(sfx_labels)
    n = 3 + len(sfx_labels)
    fl.append(f"{mix_in}amix=inputs={n}:normalize=0:duration=first,apad,atrim=0:{DUR:.3f},loudnorm=I=-15:TP=-1.5:LRA=11,apad,atrim=0:{DUR:.3f}[aout]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', f'{vi}:v',
                    '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out],
                   check=True)


# ------------------------------------------------------------------ 16:9
if ASPECT == '169':
    OW, OH = 1920, 1080
    SS = B.SS
    WS, HS = OW * SS, OH * SS
    CY0, CY1 = 200, 1150                     # franja vertical útil del lienzo 4:5
    K = OH / (CY1 - CY0)                      # 1.137
    CW = int(B.W * K)                         # ancho de la imagen en 16:9
    OX = OW - CW                              # columna de texto a la izquierda
    FD = '/usr/share/fonts/opentype/inter/'
    FK = ImageFont.truetype(FD + 'Inter-Bold.otf', 22 * SS)
    FH = ImageFont.truetype(FD + 'InterDisplay-Bold.otf', 38 * SS)
    FH2 = ImageFont.truetype(FD + 'InterDisplay-Medium.otf', 27 * SS)
    FSB = ImageFont.truetype(FD + 'Inter-Medium.otf', 29 * SS)
    B.PANEL_BG = (0, 0, 0, 0)

    def make_bg16(band):
        im = Image.new('RGBA', (WS, HS), (255, 255, 255, 255))
        if band:
            d = ImageDraw.Draw(im)
            k_ = 0.5; y0 = 650; th = 150
            pts = [(0, y0), (OW, y0 + OW * k_), (OW, y0 + OW * k_ + th), (0, y0 + th)]
            d.polygon([(x * SS, y * SS) for x, y in pts], fill=B.RED)
        return im

    BG16 = {True: make_bg16(True), False: make_bg16(False)}
    LOCK16 = B.LOCK_S
    REC = []

    o_tag, o_card, o_fit = B.tag, B.card, B.fit_logo

    def tag16(d, x, y, txt, a, anchor=None):
        if B.UIL[0] is None:
            return o_tag(d, x, y, txt, a, anchor)
        return o_tag(ImageDraw.Draw(B.UIL[0]), x, y, txt, a, anchor)

    def card16(img, box, a, lift=0.0, radius=16):
        return o_card(B.uiimg(img), box, a, lift, radius)

    def fit16(img, logo, box, a, pad=26):
        return o_fit(B.uiimg(img), logo, box, a, pad)

    def title16(d, t1, t2, a):
        if B.UI[0] and a > 0.01:
            REC.append(('title', t1, t2, a))

    def subtitle16(d, text, a):
        if B.UI[0] and a > 0.01:
            REC.append(('sub', text, a))

    def step16(d, n, name, sub, a):
        if B.UI[0] and a > 0.01:
            REC.append(('step', n, name, sub, a))

    for mod in (B, V, V5, F):
        for nm, fn in (('tag', tag16), ('card', card16), ('fit_logo', fit16), ('title', title16), ('subtitle', subtitle16),
                       ('step_header', step16)):
            if hasattr(mod, nm):
                setattr(mod, nm, fn)

    TR = F.TR

    def wrap(text, f, maxw):
        words, lines, cur = text.split(), [], ''
        for w in words:
            tst = (cur + ' ' + w).strip()
            if f.getlength(tst) <= maxw * SS:
                cur = tst
            else:
                lines.append(cur); cur = w
        lines.append(cur); return lines

    def draw_column(ov, recs):
        d = ImageDraw.Draw(ov)
        x0, colw = 80, OX - 150
        for r_ in recs:
            if r_[0] == 'step':
                _, n, name, sub, a = r_
                d.text((x0 * SS, 150 * SS), f'{n:02d} · {TR(name)}', font=FH, fill=B.ca(B.INK, a))
                d.text((x0 * SS, 206 * SS), TR(sub), font=FH2, fill=B.ca(B.INK2, a))
                x = x0
                for i_ in range(F.NSTEPS):
                    col = B.RED if i_ + 1 == n else (B.INK if i_ + 1 < n else (215, 217, 220))
                    d.rounded_rectangle([x * SS, 272 * SS, (x + 46) * SS, 279 * SS], radius=4 * SS, fill=B.ca(col, a))
                    x += 54
            elif r_[0] == 'title':
                _, t1, t2, a = r_
                d.text((x0 * SS, 150 * SS), TR(t1), font=FH, fill=B.ca(B.INK, a))
                if t2:
                    d.text((x0 * SS, 206 * SS), TR(t2), font=FH2, fill=B.ca(B.INK2, a))
                d.rounded_rectangle([x0 * SS, 272 * SS, (x0 + 64) * SS, 279 * SS], radius=4 * SS, fill=B.ca(B.RED, a))
            elif r_[0] == 'sub':
                _, text, a = r_
                lines = wrap(TR(text), FSB, colw)
                y = 360
                for ln in lines:
                    d.text((x0 * SS, y * SS), ln, font=FSB, fill=B.ca(B.INK, a)); y += 46

    FADE = np.clip(np.arange(CW * SS) / (170 * SS), 0, 1)
    FADE = (FADE * FADE * (3 - 2 * FADE))[None, :]

    def place(content, out, fade=False):
        """recorta la franja útil del lienzo 4:5 y la sitúa a la derecha del 16:9"""
        crop = content.crop((0, CY0 * SS, B.W * SS, CY1 * SS)).resize((CW * SS, HS), Image.BICUBIC)
        if fade:
            al = np.asarray(crop.getchannel('A')).astype(np.float32) * FADE
            crop.putalpha(Image.fromarray(al.astype(np.uint8)))
        out.alpha_composite(crop, (OX * SS, 0))

    def scene_content(i, t):
        """(contenido 4:5 transparente, capa UI 4:5, registros de columna)"""
        a, b, fn, band = F.SCENES[i]
        img = Image.new('RGBA', (B.W * SS, B.H * SS), (0, 0, 0, 0))
        ui = Image.new('RGBA', (B.W * SS, B.H * SS), (0, 0, 0, 0))
        REC.clear(); B.UIL[0] = ui; B.UI[0] = True; B.NOFADE[0] = True
        fn(t - a, b - a, img)
        B.UIL[0] = None; B.UI[0] = True; B.NOFADE[0] = False
        return img, ui, list(REC)

    def compose(i, t, content=None, zoom=None):
        a, b, fn, band = F.SCENES[i]
        out = BG16[band].copy()
        c, ui, recs = scene_content(i, t)
        if zoom:
            fx, fy, s, bl = zoom
            c = F.zblur(F.zoom_about(c, fx, fy, s, fill=(0, 0, 0, 0)), bl)
        place(c, out, fade=True)
        place(ui, out)
        ov = Image.new('RGBA', (WS, HS), (0, 0, 0, 0))
        draw_column(ov, recs)
        out.alpha_composite(ov)
        out.alpha_composite(LOCK16, (80 * SS, 64 * SS))
        return out

    def intro_outro(i, t):
        a, b, fn, band = F.SCENES[i]
        tl = t - a
        out = BG16[False].copy()
        al = B.ss(0.1, 0.8, tl)
        L = B.LOCK
        out.alpha_composite(B.fade_img(L, al), (WS // 2 - L.width // 2, HS // 2 - L.height // 2 - (40 * SS if i else 0)))
        if i:
            d = ImageDraw.Draw(out)
            for k_, (txt, f_, c_) in enumerate([(F.OUTRO_TXT, B.F_T2, B.INK),
                                                (F.OUTRO_URL, B.F_SMB, B.RED)]):
                tt = TR(txt)
                d.text((WS // 2 - f_.getlength(tt) / 2, HS // 2 + (50 + k_ * 48) * SS), tt, font=f_, fill=B.ca(c_, B.ss(0.6, 1.3, tl)))
        return out

    def frame16(t):
        last = len(F.SCENES) - 1
        for i in range(last):
            b = F.SCENES[i][1]
            kind, D, fa, fb = F.TRANS.get(i, ('push', F.PUSH, None, None))
            if b - D <= t < b + D:
                p = (t - (b - D)) / (2 * D)
                getf = lambda j: intro_outro(j, t) if j in (0, last) else None
                if kind in ('push', 'cut'):
                    A = intro_outro(i, t) if i in (0, last) else compose(i, t)
                    Bf = intro_outro(i + 1, t) if i + 1 in (0, last) else compose(i + 1, t)
                    return Image.blend(A, Bf, B.ss(0, 1, p))
                aA, bA = F.SCENES[i][0], F.SCENES[i][1]; aB, bB = F.SCENES[i + 1][0], F.SCENES[i + 1][1]
                cm = fa(t - aA, bA - aA, t - aB, bB - aB)
                fA, fB, R = cm[:3]
                cA, uiA, recA = scene_content(i, t)
                cB, uiB, recB = scene_content(i + 1, t)
                lay, mix = F.MZ.zoom_pair(cA, cB, p, fA, fB, R, clip='auto', under=cm[3] if len(cm) > 3 else None)
                bA_, bB_ = F.SCENES[i][3], F.SCENES[i + 1][3]
                out = Image.blend(BG16[bA_], BG16[bB_], B.ss(0.3, 0.7, p)) if bA_ != bB_ else BG16[bA_].copy()
                place(lay, out, fade=True)
                ua, ub = 1 - B.ss(0.0, 0.3, p), B.ss(0.7, 1.0, p)
                for ui_, recs_, al_ in ((uiA, recA, ua), (uiB, recB, ub)):
                    if al_ > 0.01:
                        place(F.MZ.fade_layer(ui_, al_), out)
                        ov = Image.new('RGBA', (WS, HS), (0, 0, 0, 0))
                        draw_column(ov, recs_)
                        out.alpha_composite(F.MZ.fade_layer(ov, al_))
                out.alpha_composite(LOCK16, (80 * SS, 64 * SS))
                return out
        for i, (a, b, fn, band) in enumerate(F.SCENES):
            if a <= t < b or (i == last and t >= a):
                return intro_outro(i, t) if i in (0, last) else compose(i, t)

    def render(fi):
        return frame16(fi / F.FPS).convert('RGB').resize((OW, OH), Image.LANCZOS).tobytes()
else:
    F.OW, F.OH = 1080, 1350
    OW, OH = F.OW, F.OH
    render = F.render


if __name__ == '__main__':
    if os.environ.get('VO_MODE') == '--still':
        for ts in os.environ['VO_TS'].split(','):
            Image.frombytes('RGB', (OW, OH), render(int(float(ts) * F.FPS))).save(f'{OUT}_{ts}.png')
        sys.exit()
    if os.environ.get('VO_MODE') == '--audio':
        build_audio(os.environ['VO_VIDEO'], OUT); print('done', OUT); sys.exit()
    from multiprocessing import Pool
    tmpv = OUT + '.noaudio.mp4'
    n = int(DUR * F.FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}',
                           '-r', str(F.FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high',
                           '-pix_fmt', 'yuv420p', tmpv], stdin=subprocess.PIPE)
    with Pool(2) as pool:
        for i, fb in enumerate(pool.imap(render, range(n), chunksize=3)):
            ff.stdin.write(fb)
            if i % 300 == 0:
                print(i, flush=True)
    ff.stdin.close(); ff.wait()
    build_audio(tmpv, OUT)
    print('done', OUT)
