"""Base común (materiales/geometría) para escenas SIEX. Renderiza fotogramas fijos por plano
y exporta coordenadas 2D de puntos clave para la animación compuesta en 2D.
Uso: python3 cpd_scene.py <out_dir> <shot> [samples] [scale]"""
import bpy, bmesh, math, json, sys, random
from mathutils import Vector, Euler
from bpy_extras.object_utils import world_to_camera_view

OUT = sys.argv[1]
SHOT = sys.argv[2]
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 64
RS = float(sys.argv[4]) if len(sys.argv) > 4 else 1.25
LED_SEED = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
COL = sc.collection
random.seed(3)


# ---------------- materiales ----------------
def mat(name, col, rough=0.6, metal=0.0, emit=None, es=0.0, alpha=1.0, trans=0.0, ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = es
    if trans:
        b.inputs['Transmission Weight'].default_value = trans; b.inputs['IOR'].default_value = ior
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha
    return m


M = {
    'slab': mat('slab', (0.78, 0.745, 0.69), 0.85),
    'slab_side': mat('slab_side', (0.62, 0.58, 0.53), 0.9),
    'tile': mat('tile', (0.80, 0.81, 0.82), 0.45),
    'tile_perf': mat('tile_perf', (0.50, 0.52, 0.55), 0.5, 0.3),
    'ped': mat('ped', (0.35, 0.36, 0.38), 0.4, 0.6),
    'wall': mat('wall', (0.58, 0.60, 0.63), 0.9),
    'wallcap': mat('wallcap', (0.78, 0.79, 0.80), 0.8),
    'rack': mat('rack', (0.025, 0.027, 0.03), 0.35, 0.6),
    'tray': mat('tray', (0.62, 0.64, 0.66), 0.35, 1.0),
    'cable_b': mat('cable_b', (0.05, 0.18, 0.55), 0.5),
    'cable_y': mat('cable_y', (0.85, 0.62, 0.05), 0.5),
    'cable_g': mat('cable_g', (0.15, 0.15, 0.16), 0.6),
    'steel': mat('steel', (0.80, 0.80, 0.80), 0.22, 1.0),
    'steel_d': mat('steel_d', (0.55, 0.56, 0.58), 0.3, 1.0),
    'red': mat('red', (0.55, 0.035, 0.03), 0.35, 0.0),
    'redcab': mat('redcab', (0.42, 0.10, 0.08), 0.5),
    'green': mat('green', (0.08, 0.42, 0.18), 0.35),
    'crac': mat('crac', (0.86, 0.87, 0.88), 0.5),
    'grille': mat('grille', (0.12, 0.12, 0.13), 0.6),
    'motor': mat('motor', (0.08, 0.09, 0.10), 0.45, 0.4),
    'brass': mat('brass', (0.78, 0.58, 0.25), 0.3, 1.0),
    'panel_blue': mat('panel_blue', (0.12, 0.2, 0.6), 0.4, 0, (0.15, 0.25, 0.8), 0.6),
    'glass': mat('glass', (0.95, 0.97, 1.0), 0.02, 0.0, trans=1.0, ior=1.5),
    'bulb_liq': mat('bulb_liq', (0.85, 0.05, 0.04), 0.1, 0.0, (0.6, 0.02, 0.02), 0.6, trans=0.6, ior=1.35),
    'black': mat('black', (0.01, 0.01, 0.01), 0.6),
    'door_glass': mat('door_glass', (0.2, 0.25, 0.3), 0.05, 0.0, trans=0.4),
    'esc': mat('esc', (0.86, 0.87, 0.88), 0.3, 0.6),
    'steel_sat': mat('steel_sat', (0.78, 0.78, 0.79), 0.3, 1.0),
    'tank': mat('tank', (0.72, 0.73, 0.75), 0.45, 1.0),
}


def rack_door_mat(seed):
    m = bpy.data.materials.new(f'door{seed}'); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord'); mp = N.new('ShaderNodeMapping')
    mp.inputs['Location'].default_value = (seed * 7.3, seed * 3.1, 0)
    Lk.new(tc.outputs['Object'], mp.inputs['Vector'])
    br = N.new('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = 60
    br.inputs['Color1'].default_value = (0.06, 0.065, 0.07, 1); br.inputs['Color2'].default_value = (0.05, 0.055, 0.06, 1)
    br.inputs['Mortar'].default_value = (0.005, 0.005, 0.006, 1); br.inputs['Mortar Size'].default_value = 0.03
    Lk.new(mp.outputs['Vector'], br.inputs['Vector']); Lk.new(br.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Metallic'].default_value = 0.6; b.inputs['Roughness'].default_value = 0.4
    vo = N.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 26
    Lk.new(mp.outputs['Vector'], vo.inputs['Vector'])
    sep = N.new('ShaderNodeSeparateColor'); Lk.new(vo.outputs['Color'], sep.inputs['Color'])
    gt = N.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.93
    Lk.new(sep.outputs['Red'], gt.inputs[0])
    dist = N.new('ShaderNodeMath'); dist.operation = 'LESS_THAN'; dist.inputs[1].default_value = 0.12
    Lk.new(vo.outputs['Distance'], dist.inputs[0])
    mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    Lk.new(gt.outputs[0], mul.inputs[0]); Lk.new(dist.outputs[0], mul.inputs[1])
    ramp = N.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.1, 1.0, 0.35, 1); ramp.color_ramp.elements[1].color = (0.2, 0.55, 1.0, 1)
    Lk.new(sep.outputs['Green'], ramp.inputs['Fac'])
    Lk.new(ramp.outputs['Color'], b.inputs['Emission Color'])
    sm = N.new('ShaderNodeMath'); sm.operation = 'MULTIPLY'; sm.inputs[1].default_value = 14.0
    Lk.new(mul.outputs[0], sm.inputs[0]); Lk.new(sm.outputs[0], b.inputs['Emission Strength'])
    return m


DOOR = rack_door_mat(LED_SEED)


# ---------------- geometría ----------------
def box(name, loc, size, m, bevel=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(m)
    if bevel:
        bv = o.modifiers.new('b', 'BEVEL'); bv.width = bevel; bv.segments = 3
    return o


def cyl(name, loc, r, h, m, rot=(0, 0, 0), verts=32, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    if bevel:
        bv = o.modifiers.new('b', 'BEVEL'); bv.width = bevel; bv.segments = 2
    return o


def sph(name, loc, r, m, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16)
    o = bpy.context.object; o.name = name; o.scale = scale; o.data.materials.append(m)
    bpy.ops.object.shade_smooth(); return o


def pipe(name, a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a
    o = cyl(name, (a + b) / 2, r, d.length, m, verts=20)
    o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    return o



def lathe(name, prof, m, segs=96, loc=(0, 0, 0)):
    """perfil [(r, z), ...] de arriba abajo -> sólido de revolución"""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((r, 0, z)) for r, z in prof]
    for i in range(len(vs) - 1):
        bm.edges.new((vs[i], vs[i + 1]))
    bmesh.ops.spin(bm, geom=bm.verts[:] + bm.edges[:], cent=(0, 0, 0), axis=(0, 0, 1), angle=2 * math.pi, steps=segs)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-6)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); COL.objects.link(o); o.location = loc
    o.data.materials.append(m)
    for p in o.data.polygons:
        p.use_smooth = True
    bpy.context.view_layer.objects.active = o
    try:
        o.select_set(True); bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35)); o.select_set(False)
    except Exception:
        pass
    return o


def camera_iso(target, ortho, az=45, el=35.264):
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = ortho
    co = bpy.data.objects.new('cam', cam); COL.objects.link(co); sc.camera = co
    a, e = math.radians(az), math.radians(el)
    d = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    co.location = Vector(target) + d * 40
    co.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    cam.clip_end = 200
    return co


def camera_persp(loc, target, lens=85):
    cam = bpy.data.cameras.new('cam'); cam.lens = lens
    co = bpy.data.objects.new('cam', cam); COL.objects.link(co); sc.camera = co
    co.location = loc
    co.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return co


def lights():
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (1, 1, 1, 1); bg.inputs['Strength'].default_value = 0.45
    s = bpy.data.lights.new('sun', 'SUN'); s.energy = 2.6; s.angle = math.radians(12)
    so = bpy.data.objects.new('sun', s); COL.objects.link(so); so.rotation_euler = (math.radians(42), math.radians(8), math.radians(-35))
    a = bpy.data.lights.new('fill', 'AREA'); a.energy = 1100; a.size = 12
    ao = bpy.data.objects.new('fill', a); COL.objects.link(ao); ao.location = (12, -14, 14)
    ao.rotation_euler = (Vector((0, 0, 0)) - ao.location).to_track_quat('-Z', 'Y').to_euler()

