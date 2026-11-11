"""Prueba rápida de un tramo, renderizado EN ORDEN (como en el vídeo final).
Las etiquetas se fijan según los fotogramas anteriores, así que un fotograma suelto (VO_MODE=--still)
no muestra cómo quedan en el vídeo. Guarda inicio (+0,5 s), mitad y final del tramo.
Uso: python3 t_seq.py <es|en> <voz.mp3> <45|169> <t0> <t1> [prefijo]
Ej.: python3 t_seq.py es ../trabajo/vo/es_v3.mp3 45 140 146 ../trabajo/chk/seq
Otro montaje: KOMTES_MASTER=siex2_master python3 t_seq.py …"""
import sys, os
lang, vo, asp, t0, t1 = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
pre = sys.argv[6] if len(sys.argv) > 6 else None
sys.argv = [os.environ.get('KOMTES_MASTER', 'cpd_master') + '.py', lang, vo, asp, 'x.mp4']
import importlib
M = importlib.import_module(os.environ.get('KOMTES_MASTER', 'cpd_master'))   # otro montaje: KOMTES_MASTER=siex2_master
from PIL import Image
F = M.F
pre = pre or (M.SP + 'chk/seq')
os.makedirs(os.path.dirname(pre), exist_ok=True)
f0, f1 = int(t0 * F.FPS), int(t1 * F.FPS)
keep = {min(f0 + 15, f1 - 1), (f0 + f1) // 2, f1 - 1}
for fi in range(f0, f1):
    fb = M.render(fi)
    if fi in keep:
        Image.frombytes('RGB', (M.OW, M.OH), fb).save(f'{pre}_{lang}{asp}_{fi / F.FPS:.1f}s.png')
print('ok', [f'{pre}_{lang}{asp}_{k / F.FPS:.1f}s.png' for k in sorted(keep)])
