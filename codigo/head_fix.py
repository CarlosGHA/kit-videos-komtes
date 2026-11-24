"""Rehace SOLO el principio de un vídeo ya renderizado (p. ej. cambia la entradilla o su tipografía) y conserva el resto
y el audio del vídeo anterior. Requisito: la duración y los tiempos de las escenas no cambian.

Uso:  [PIEZA=n SUB_LANG=es] python3 head_fix.py <es|en> <voz.mp3> <45|169> <video_anterior.mp4> <salida.mp4> <segundos>"""
import sys, os, subprocess, importlib
if len(sys.argv) < 7:
    print(__doc__); sys.exit(2)
lang, vo, asp, prev, out, secs = sys.argv[1:7]
sys.argv = ['cpd_master.py', lang, vo, asp, out]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
M = importlib.import_module('cpd_master')
F = M.F
f1 = int(round(float(secs) * F.FPS))
tmp = out + '.noaudio.mp4'
print(f'cabeza: {f1} fotogramas nuevos · resto del vídeo anterior', flush=True)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{M.OW}x{M.OH}',
                       '-r', str(F.FPS), '-i', '-', '-i', prev,
                       '-filter_complex', f'[0:v]format=rgb24[h];[1:v]trim=start_frame={f1},setpts=PTS-STARTPTS,format=rgb24[t];'
                                          '[h][t]concat=n=2:v=1:a=0[v]',
                       '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high',
                       '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
for fi in range(f1):
    ff.stdin.write(M.render(fi))
ff.stdin.close(); ff.wait()
assert ff.returncode == 0
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', prev, '-map', '0:v', '-map', '1:a', '-c', 'copy',
                '-movflags', '+faststart', out], check=True)
os.remove(tmp)
print('done', out)
