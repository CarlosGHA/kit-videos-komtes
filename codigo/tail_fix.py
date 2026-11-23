"""Rehace SOLO el final de un vídeo ya renderizado (p. ej. cuando cambia la última frase de la locución).
Requisito: todas las escenas anteriores a la escena final empiezan y duran lo mismo (compruébalo con VO_MODE=--scenes).
Renderiza desde el inicio de la última escena (pasado el fundido), lo une a la parte inicial del vídeo anterior
y vuelve a montar el audio con la nueva locución. Ahorra horas de render.

Uso:  python3 tail_fix.py <es|en> <voz.mp3> <45|169> <video_anterior.mp4> <salida.mp4> [master]"""
import sys, os, subprocess, importlib
if len(sys.argv) < 6:
    print(__doc__); sys.exit(2)
lang, vo, asp, prev, out = sys.argv[1:6]
master = sys.argv[6] if len(sys.argv) > 6 else 'cpd_master'
sys.argv = [master + '.py', lang, vo, asp, out]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
M = importlib.import_module(master)
F = M.F
last = F.SCENES[-1]
f0 = int(round((last[0] + getattr(F, 'XF', 0.35) + 0.1) * F.FPS))
n = int(M.DUR * F.FPS)
tmp = out + '.noaudio.mp4'
print(f'cabeza: {f0} fotogramas del vídeo anterior · cola: {n - f0} nuevos', flush=True)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-i', prev,
                       '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{M.OW}x{M.OH}', '-r', str(F.FPS), '-i', '-',
                       '-filter_complex', f'[0:v]trim=end_frame={f0},setpts=PTS-STARTPTS,format=rgb24[h];[h][1:v]concat=n=2:v=1:a=0[v]',
                       '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high',
                       '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
for fi in range(f0, n):
    ff.stdin.write(M.render(fi))
ff.stdin.close(); ff.wait()
assert ff.returncode == 0
M.build_audio(tmp, out)
M.dump_scenes(os.path.splitext(out)[0] + '.scenes.json')
os.remove(tmp)
print('done', out)
