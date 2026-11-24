"""Música original de la entradilla «Risk by Risk» (6 s, sintetizada, sin derechos de terceros).
Pad cálido (sierras desafinadas filtradas) Am9 -> Fmaj7(#11), arpegio de pulsos suaves, sub y reverberación.
Uso: python3 musica_entradilla.py <salida.wav> [duración_s]"""
import sys, numpy as np, wave
SR = 48000
out = sys.argv[1]; D = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
n = int(SR * D); t = np.arange(n) / SR
rng = np.random.default_rng(7)
f = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def lp(x, fc):                      # paso bajo de un polo (dos pasadas)
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for _ in range(2):
        for i in range(len(x)):
            s = (1 - a) * x[i] + a * s; y[i] = s
        x = y.copy()
    return y


def saw(fr, ph=0.0):
    return 2 * ((fr * t + ph) % 1.0) - 1


def env(a, d, s0, s1):              # ataque, caída, inicio y fin (s)
    e = np.clip((t - s0) / a, 0, 1) * np.clip((s1 - t) / d, 0, 1)
    return e * e * (3 - 2 * e)


L = np.zeros(n); R = np.zeros(n)
ch1 = [57, 60, 64, 67, 71]          # Am9
ch2 = [53, 57, 60, 64, 71]          # Fmaj7(#11) aprox. (B como color)
for chord, s0, s1 in [(ch1, 0.0, 3.4), (ch2, 2.9, D)]:
    for k, m in enumerate(chord):
        for det, pan in [(-0.08, 0.3), (0.08, 0.7)]:
            v = saw(f(m) * (1 + det / 100 * 12), rng.random()) * env(1.2, 1.3, s0, s1) * 0.05
            L += v * (1 - pan); R += v * pan
pad_cut = 900 + 1400 * np.clip(t / 2.5, 0, 1)        # el filtro se abre: sensación de «entrada»
L = lp(L, 1600); R = lp(R, 1600)

# arpegio de pulsos suaves (corcheas a 96 bpm), entra con el título
step = 60 / 96 / 2
notes = [69, 72, 76, 79, 76, 72, 69, 72, 65, 69, 72, 76, 72, 69, 65, 69]
for i, m in enumerate(notes):
    s0 = 0.9 + i * step
    if s0 > D - 0.6:
        break
    tt = t - s0; msk = tt >= 0
    e = np.where(msk, np.exp(-tt * 9) * np.clip(tt / 0.004, 0, 1), 0)
    v = (np.sin(2 * np.pi * f(m + 12) * tt) + 0.3 * np.sin(2 * np.pi * f(m + 24) * tt)) * e * 0.06
    v *= np.clip((t - 0.9) / 1.0, 0, 1) * np.clip((D - 0.4 - t) / 1.2, 0, 1)
    pan = 0.35 + 0.3 * (i % 2)
    L += v * (1 - pan); R += v * pan

# sub suave bajo el título y bajo el cambio de acorde
for s0, m in [(0.6, 33), (2.9, 29)]:
    tt = t - s0
    e = np.where(tt >= 0, np.clip(tt / 0.08, 0, 1) * np.exp(-np.clip(tt, 0, None) * 1.1), 0)
    v = np.sin(2 * np.pi * f(m) * tt) * e * 0.16
    L += v; R += v

# reverberación (ruido con caída exponencial, distinta por canal)
ir_n = int(SR * 2.2); it = np.arange(ir_n) / SR
for i, X in enumerate((L, R)):
    ir = rng.standard_normal(ir_n) * np.exp(-it * 3.2); ir[0] = 0; ir /= np.sqrt((ir ** 2).sum())
    wet = np.fft.irfft(np.fft.rfft(X, 2 * n + ir_n) * np.fft.rfft(ir, 2 * n + ir_n))[:n]
    if i == 0:
        L = X * 0.75 + wet * 0.45
    else:
        R = X * 0.75 + wet * 0.45
fade = np.clip(t / 0.5, 0, 1) * np.clip((D - t) / 1.2, 0, 1)
L *= fade; R *= fade
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pk * 0.7, R / pk * 0.7
data = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
print('done', out)
