"""Locución provisional GRATUITA (silenciosa) para trabajar antes de pagar la voz definitiva.

Uso:  python3 vo_borrador.py <texto_locucion.txt> <es|en> <salida.wav>

El texto es el mismo que leerá la voz: bloques separados por [pause] (las etiquetas [warmly], [serious]… se ignoran).
Calcula cuánto durará cada bloque (≈16,5 caracteres/s en español y ≈17,5 en inglés, ±10 %) y escribe:
  · <salida.wav>           audio en silencio con esa duración total
  · <salida>.blocks.json   inicio y fin de cada bloque (el montaje lo lee en lugar de buscar las pausas)
Con ella se sacan fotogramas clave, la hoja de textos y un vídeo piloto con subtítulos y música pero sin voz, y se
valida todo con el ingeniero ANTES de generar la locución de pago. También sirve para una versión sin voz (pantalla
de feria). Al llegar la voz definitiva solo se cambia el archivo de locución: los tiempos se reajustan solos."""
import sys, re, json, wave, os

if len(sys.argv) < 4:
    print(__doc__); sys.exit(2)
txt, lang, out = sys.argv[1:4]
CPS = {'es': 16.5, 'en': 17.5}[lang]
PAUSE = 1.0
blocks = [re.sub(r'\[[a-zA-Z ]+\]', ' ', b) for b in re.split(r'\[pause\]', open(txt, encoding='utf-8').read())]
blocks = [re.sub(r'\s+', ' ', b).strip() for b in blocks if b.strip()]
t = 0.3
times = []
for b in blocks:
    d = max(1.2, len(b) / CPS)
    times.append([round(t, 2), round(t + d, 2)])
    t += d + PAUSE
total = t - PAUSE + 0.3
with wave.open(out, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes(b'\x00\x00' * int(total * 48000))
json.dump({'blocks': times, 'borrador': True}, open(os.path.splitext(out)[0] + '.blocks.json', 'w'))
print(f'{len(blocks)} bloques · {total:.1f} s de locución estimada → {out}')
for i, (b, (a, e)) in enumerate(zip(blocks, times)):
    print(f'  {i:2d}  {e - a:5.1f} s  {b[:70]}')
