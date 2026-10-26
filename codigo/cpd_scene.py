"""Escena Blender: CPD isométrico protegido con RG W-FOG. Renderiza fotogramas fijos por plano
y exporta coordenadas 2D de puntos clave para la animación compuesta en 2D.
Uso: python3 cpd_scene.py <out_dir> <shot> [samples] [scale]"""
import bpy, bmesh, math, json, sys, random
from mathutils import Vector, Euler
from bpy_extras.object_utils import world_to_camera_view
import os as _os
KW = _os.environ.get('KOMTES_WORK', _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'trabajo'))) + '/'

OUT = sys.argv[1]
SHOT = sys.argv[2]
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 64
RS = float(sys.argv[4]) if len(sys.argv) > 4 else 1.25
LED_SEED = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
COL = sc.collection
exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'label_wrap.py')).read())
LABEL_RG = KW + 'assets/label_rg.png'
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
    'hole': mat('hole', (0.004, 0.004, 0.005), 0.9),
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



def make_nozzle(base, s, name, broken=False, escutcheon=False, detail=True):
    """Boquilla cerrada RG serie MM-P5x (colgante): hexágono único, rosca, cuerpo cónico con dos coronas
    de micro-orificios y jaula ranurada con ampolla. base = punto de conexión (arriba). s = metros por unidad real."""
    bx, by, bz = base
    out = {'orifices': [], 'bulb': None, 'tip': None}
    z = bz
    # hexágono (única llave)
    cyl(f'{name}_hex', (bx, by, z - 0.005 * s), 0.0125 * s, 0.010 * s, M['steel'], verts=6, bevel=0.0008 * s if detail else 0)
    z -= 0.010 * s
    # rosca
    cyl(f'{name}_thr', (bx, by, z - 0.006 * s), 0.0085 * s, 0.012 * s, M['steel_d'])
    if detail:
        for i in range(5):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.0086 * s, minor_radius=0.0007 * s, location=(bx, by, z - 0.0015 * s - i * 0.0022 * s),
                                             major_segments=32, minor_segments=8)
            bpy.context.object.data.materials.append(M['steel_d'])
    z -= 0.012 * s
    # collarín
    cyl(f'{name}_col', (bx, by, z - 0.002 * s), 0.0118 * s, 0.004 * s, M['steel'], bevel=0.0005 * s if detail else 0)
    z -= 0.004 * s
    if escutcheon:
        cyl(f'{name}_esc', (bx, by, z - 0.0018 * s), 0.030 * s, 0.0025 * s, M['esc'], verts=64, bevel=0.0008 * s)
        cyl(f'{name}_esc2', (bx, by, z - 0.0040 * s), 0.0165 * s, 0.002 * s, M['esc'], verts=64, bevel=0.0005 * s)
    # cuerpo cónico
    h = 0.017 * s
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.0072 * s, radius2=0.0112 * s, depth=h, location=(bx, by, z - h / 2))
    o = bpy.context.object; o.data.materials.append(M['steel']); bpy.ops.object.shade_smooth()
    if detail:
        bv = o.modifiers.new('b', 'BEVEL'); bv.width = 0.0006 * s; bv.segments = 2
    # micro-orificios (2 coronas x 8)
    for ring, (zf, rr, tilt) in enumerate([(0.35, 0.0098, 40), (0.72, 0.0084, 62)]):
        zz = z - h * zf
        for k in range(8):
            az = 2 * math.pi * k / 8 + ring * math.pi / 8
            nrm = Vector((math.cos(az), math.sin(az), 0.25)).normalized()
            p = Vector((bx + math.cos(az) * rr * s, by + math.sin(az) * rr * s, zz))
            if detail:
                hole = cyl(f'{name}_o{ring}{k}', p, 0.0011 * s, 0.0012 * s, M['black'], verts=16)
                hole.rotation_euler = nrm.to_track_quat('Z', 'Y').to_euler()
            dv = Vector((math.cos(az) * math.cos(math.radians(tilt)), math.sin(az) * math.cos(math.radians(tilt)), -math.sin(math.radians(tilt))))
            out['orifices'].append((tuple(p), tuple(dv)))
    z -= h
    # jaula ranurada con ampolla
    ch = 0.022 * s
    cage = cyl(f'{name}_cage', (bx, by, z - ch / 2), 0.0052 * s, ch, M['steel'], verts=48)
    if detail:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(bx, by, z - ch / 2 + 0.001 * s))
        cut = bpy.context.object; cut.scale = (0.0056 * s, 0.03 * s, ch * 0.8)
        cut.hide_render = True; cut.hide_viewport = True
        bo = cage.modifiers.new('slot', 'BOOLEAN'); bo.operation = 'DIFFERENCE'; bo.object = cut
    if not broken:
        sph(f'{name}_bulb', (bx, by, z - ch / 2), 0.0024 * s, M['glass'], (1, 1, 3.6))
        sph(f'{name}_liq', (bx, by, z - ch / 2), 0.0021 * s, M['bulb_liq'], (1, 1, 3.5))
    else:
        if detail:
            sph(f'{name}_stub', (bx, by, z - ch / 2 + 0.0072 * s), 0.0016 * s, M['glass'], (1, 1, 0.6))
    out['bulb'] = (bx, by, z - ch / 2)
    out['tip'] = (bx, by, z - ch)
    out['slot'] = (bx, by - 0.0052 * s, z - ch / 2)
    return out





_ENGRS = {}


def engrave_mat(text='RG SYSTEMS MM-P50-57-11', base=(0.80, 0.80, 0.80)):
    key = (text, base)
    if key in _ENGRS:
        return _ENGRS[key]
    from PIL import Image as PImage, ImageDraw as PDraw, ImageFont as PFont
    w, h = 2048, 96
    im = PImage.new('RGBA', (w, h), (0, 0, 0, 0))
    dr = PDraw.Draw(im)
    f = PFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 64)
    dr.text((420, 12), text, font=f, fill=(40, 42, 46, 235))
    p = KW + f'engrave_{len(_ENGRS)}.png'
    im.save(p)
    m = bpy.data.materials.new('engr'); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    bsdf = N['Principled BSDF']
    bsdf.inputs['Metallic'].default_value = 1.0; bsdf.inputs['Roughness'].default_value = 0.28
    tc = N.new('ShaderNodeTexCoord')
    tex = N.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(p); tex.projection = 'TUBE'
    tex.extension = 'CLIP'
    Lk.new(tc.outputs['Generated'], tex.inputs['Vector'])
    mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = (*base, 1)
    Lk.new(tex.outputs['Alpha'], mix.inputs['Factor']); Lk.new(tex.outputs['Color'], mix.inputs['B'])
    Lk.new(mix.outputs['Result'], bsdf.inputs['Base Color'])
    _ENGRS[key] = m
    return m


def lathe(name, prof, m, segs=96, loc=(0, 0, 0)):
    """perfil [(r, z), ...] de arriba abajo -> sólido de revolución"""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((r, 0, z)) for r, z in prof]
    for i in range(len(vs) - 1):
        bm.edges.new((vs[i], vs[i + 1]))
    bmesh.ops.spin(bm, geom=bm.verts[:] + bm.edges[:], cent=(0, 0, 0), axis=(0, 0, 1), angle=2 * math.pi, steps=segs)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-6)
    if prof[0][0] == 0 and prof[-1][0] == 0:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
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


def hole_cutters(name, pts, r, depth, m=None, segs=20):
    """une cilindros de corte (orificios reales) en un solo objeto oculto; pts = [(pos Vector, normal Vector)]"""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    for p, n in pts:
        q = n.to_track_quat('Z', 'Y')
        geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=depth)
        for v in geom['verts']:
            v.co = q @ v.co + p
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); COL.objects.link(o)
    o.data.materials.append(m or M['hole'])
    o.hide_render = True; o.hide_viewport = True
    return o


def cut_holes(target, cutter):
    bo = target.modifiers.new('holes', 'BOOLEAN'); bo.operation = 'DIFFERENCE'; bo.object = cutter
    bo.solver = 'EXACT'
    try:
        bo.use_hole_tolerant = True; bo.material_mode = 'TRANSFER'
    except Exception:
        pass
    return bo


def make_mmp50(base, k, name, variant='floor', broken=False, detail=True):
    """Boquilla cerrada RG MM-P50 (según renders del fabricante). base = cara superior del hexágono.
    k = metros por píxel del render de referencia. variant 'ceil' (adaptador M32 + embellecedor NS1) o 'floor' (adaptador M31)."""
    bx, by, bz = base
    Z = lambda y: bz - y * k
    out = {'orifices': []}
    cx = lambda r: r * k
    # hexágono superior (racor)
    hx = cyl(f'{name}_hex', (bx, by, Z(33)), cx(47), 66 * k, M['steel_sat'], verts=6, bevel=1.2 * k if detail else 0)
    hx.rotation_euler = (0, 0, math.radians(30))
    cyl(f'{name}_hexbore', (bx, by, Z(0) + 0.2 * k), cx(14), 1.5 * k, M['black'])
    if variant == 'm32':
        # adaptador M32 sin embellecedor
        lathe(f'{name}_adp', [(cx(27.5), Z(66)), (cx(27.5), Z(73)), (cx(55.5), Z(74)), (cx(55.5), Z(106)), (cx(54), Z(108)),
                              (cx(54), Z(110)), (cx(55.5), Z(112)), (cx(55.5), Z(152)), (cx(52), Z(156))],
              M['steel_sat'], loc=(bx, by, 0))
        if detail:
            for zz in (106, 112):
                bpy.ops.mesh.primitive_torus_add(major_radius=cx(55.2), minor_radius=cx(1.0), location=(bx, by, Z(zz)),
                                                 major_segments=64, minor_segments=8)
                bpy.context.object.data.materials.append(M['steel_d'])
    elif variant == 'ceil':
        lathe(f'{name}_adp', [(cx(27.5), Z(66)), (cx(27.5), Z(73)), (cx(55.5), Z(74)), (cx(55.5), Z(106)), (cx(54), Z(108))],
              M['steel_sat'], loc=(bx, by, 0))
        # embellecedor NS1 semienrasado
        lathe(f'{name}_esc', [(cx(56), Z(108)), (cx(157), Z(108)), (cx(158), Z(112)), (cx(118), Z(122)), (cx(106), Z(137)),
                              (cx(56), Z(140)), (cx(56), Z(155))], M['esc'], loc=(bx, by, 0))
        out['plate_z'] = Z(108)
        out['esc'] = (bx + cx(130), by, Z(116))
    else:
        lathe(f'{name}_neck', [(cx(39.5), Z(66)), (cx(39.5), Z(73))], M['steel_sat'], loc=(bx, by, 0))
        lathe(f'{name}_thr', [(cx(52), Z(73)), (cx(52), Z(119))], M['steel_d'], loc=(bx, by, 0))
        if detail:
            for i in range(9):
                bpy.ops.mesh.primitive_torus_add(major_radius=cx(53), minor_radius=cx(2.6), location=(bx, by, Z(77 + i * 5)),
                                                 major_segments=64, minor_segments=8)
                bpy.context.object.data.materials.append(M['steel_d'])
        h2 = cyl(f'{name}_hex2', (bx, by, Z(131)), cx(69), 24 * k, M['steel_sat'], verts=6, bevel=1.0 * k if detail else 0)
        lathe(f'{name}_col', [(cx(60), Z(143)), (cx(60), Z(154)), (cx(57), Z(157))], M['steel_sat'], loc=(bx, by, 0))
    # cuerpo grabado + cono
    band = lathe(f'{name}_band', [(cx(43), Z(156)), (cx(43), Z(175))], engrave_mat() if detail else M['steel_sat'], loc=(bx, by, 0))
    cone = lathe(f'{name}_cone', [(0, Z(175)), (cx(43), Z(175)), (cx(42.5), Z(176)), (cx(28.5), Z(217)), (cx(20.5), Z(219)), (0, Z(219))],
                 M['steel_sat'], loc=(bx, by, 0))
    hpts = []
    # micro-orificios en 2 coronas al tresbolillo (agujeros reales, no relieve)
    rows = [(186, 10), (204, 10)]
    for ri, (yy, n) in enumerate(rows):
        t_ = (yy - 176) / 41.0
        rr = 42.5 + (28.5 - 42.5) * t_
        for j in range(n):
            az = 2 * math.pi * j / n + ri * math.pi / n
            nrm = Vector((math.cos(az), math.sin(az), 0.33)).normalized()
            p = Vector((bx + math.cos(az) * cx(rr), by + math.sin(az) * cx(rr), Z(yy)))
            if detail:
                hpts.append((p.copy(), nrm))
            tilt = math.radians(38 + ri * 16)
            dv = Vector((math.cos(az) * math.cos(tilt), math.sin(az) * math.cos(tilt), -math.sin(tilt)))
            out['orifices'].append((tuple(p), tuple(dv)))
    if detail and hpts:
        cut_holes(cone, hole_cutters(f'{name}_hc', hpts, cx(3.4), cx(16)))
    # jaula con ranura y ampolla
    cage = lathe(f'{name}_cage', [(cx(0.1), Z(218)), (cx(20), Z(218)), (cx(20), Z(277)), (cx(18), Z(280)), (cx(0.1), Z(280.5))],
                 M['steel_sat'], segs=64, loc=(bx, by, 0))
    if detail:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(bx, by, Z(240)))
        cut = bpy.context.object; cut.scale = (cx(11), cx(60), 50 * k)
        cut.hide_render = True; cut.hide_viewport = True
        bo = cage.modifiers.new('slot', 'BOOLEAN'); bo.operation = 'DIFFERENCE'; bo.object = cut
        bpy.ops.mesh.primitive_cube_add(size=1, location=(bx, by, Z(240)))
        cut2 = bpy.context.object; cut2.scale = (cx(60), cx(11), 50 * k)
        cut2.hide_render = True; cut2.hide_viewport = True
        bo2 = cage.modifiers.new('slot2', 'BOOLEAN'); bo2.operation = 'DIFFERENCE'; bo2.object = cut2
    if not broken:
        sph(f'{name}_bulb', (bx, by, Z(240)), cx(5.2), M['glass'], (1, 1, 4.6))
        sph(f'{name}_liq', (bx, by, Z(240)), cx(4.4), M['bulb_liq'], (1, 1, 4.6))
    elif detail:
        sph(f'{name}_stub', (bx, by, Z(218.5)), cx(4.5), M['glass'], (1, 1, 0.5))
    out['bulb'] = (bx, by, Z(240)); out['tip'] = (bx, by, Z(280)); out['slot'] = (bx, by - cx(20), Z(240))
    out['hex'] = (bx + cx(30), by - cx(30), Z(30))
    return out


def make_emm_closed(base, k, name, broken=False, detail=True):
    """Boquilla cerrada RG EMM bajo suelo técnico (modelo de la referencia dorada), acabado acero.
    base = cara superior del hexágono; k = metros por px de la referencia (alto total ~445 px)."""
    bx, by, bz = base
    Z = lambda y: bz - y * k
    cx = lambda r: r * k
    out = {'orifices': []}
    hx = cyl(f'{name}_hex', (bx, by, Z(42)), cx(88), 84 * k, M['steel_sat'], verts=6, bevel=1.5 * k if detail else 0)
    hx.rotation_euler = (0, 0, math.radians(30))
    lathe(f'{name}_neck', [(cx(56), Z(84)), (cx(56), Z(138)), (cx(48), Z(141)), (cx(48), Z(151)), (cx(62), Z(155)),
                           (cx(62), Z(184)), (cx(58), Z(187))], M['steel_sat'], loc=(bx, by, 0))
    body = lathe(f'{name}_body', [(0, Z(186)), (cx(64), Z(186)), (cx(64), Z(300)), (cx(60), Z(306)), (cx(44), Z(318)), (0, Z(318))],
                 M['steel_sat'], loc=(bx, by, 0))
    if detail:
        lathe(f'{name}_engr', [(cx(64.4), Z(222)), (cx(64.4), Z(252))], engrave_mat('RG SYSTEMS EMM'), loc=(bx, by, 0))
    # orificios en dos coronas, por parejas
    hpts = []
    for ri, yy in enumerate((268, 291)):
        for pj in range(6):
            for dd in (-0.13, 0.13):
                az = 2 * math.pi * pj / 6 + dd + math.radians(15)
                nrm = Vector((math.cos(az), math.sin(az), 0.0))
                p = Vector((bx + math.cos(az) * cx(64), by + math.sin(az) * cx(64), Z(yy)))
                hpts.append((p, nrm))
                out['orifices'].append((tuple(p), tuple(Vector((nrm.x, nrm.y, -0.55)).normalized())))
    if detail:
        cut_holes(body, hole_cutters(f'{name}_hc', hpts, cx(5.5), cx(22)))
    # alojamiento de la ampolla con ventanas
    hs = lathe(f'{name}_hs', [(0, Z(316)), (cx(33), Z(316)), (cx(33), Z(415)), (cx(30), Z(428)), (cx(20), Z(440)), (0, Z(444))],
               M['steel_sat'], segs=64, loc=(bx, by, 0))
    if detail:
        for i_, (sx_, sy_) in enumerate(((cx(10), cx(80)), (cx(80), cx(10)))):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(bx, by, Z(385)))
            ct = bpy.context.object; ct.scale = (sx_, sy_, 80 * k); ct.hide_render = True; ct.hide_viewport = True
            ct.data.materials.append(M['hole'])
            bo = hs.modifiers.new(f'slot{i_}', 'BOOLEAN'); bo.operation = 'DIFFERENCE'; bo.object = ct
    if not broken:
        sph(f'{name}_bulb', (bx, by, Z(385)), cx(9), M['glass'], (1, 1, 4.2))
        sph(f'{name}_liq', (bx, by, Z(385)), cx(7.5), M['bulb_liq'], (1, 1, 4.2))
    out['bulb'] = (bx, by, Z(385)); out['tip'] = (bx, by, Z(444)); out['slot'] = (bx, by - cx(33), Z(385))
    out['ring'] = (bx, by, Z(280))
    out['hex'] = (bx + cx(60), by - cx(60), Z(40))
    return out


def studio_metal(name, stops, rough=0.22, right=(0.8, 0.6, 0.0)):
    """acero pulido de render de catálogo: reflejo en bandas verticales (independiente del entorno)"""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    b = N['Principled BSDF']
    b.inputs['Metallic'].default_value = 1.0; b.inputs['Roughness'].default_value = rough
    tc = N.new('ShaderNodeTexCoord')
    dp = N.new('ShaderNodeVectorMath'); dp.operation = 'DOT_PRODUCT'
    dp.inputs[1].default_value = right
    Lk.new(tc.outputs['Reflection'], dp.inputs[0])
    mr = N.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -1.0; mr.inputs['From Max'].default_value = 1.0
    Lk.new(dp.outputs['Value'], mr.inputs['Value'])
    cr = N.new('ShaderNodeValToRGB')
    el = cr.color_ramp.elements
    el[0].position, el[0].color = stops[0][0], (stops[0][1],) * 3 + (1,)
    el[1].position, el[1].color = stops[-1][0], (stops[-1][1],) * 3 + (1,)
    for pos, val in stops[1:-1]:
        e = el.new(pos); e.color = (val,) * 3 + (1,)
    Lk.new(mr.outputs['Result'], cr.inputs['Fac'])
    Lk.new(cr.outputs['Color'], b.inputs['Base Color'])
    return m


def make_emm_open(base, k, name, detail=True, face=-58.0):
    """Difusor abierto RG EMM, fiel al render del fabricante (medidas en px de la referencia a 2x).
    base = cara superior del hexágono; k = metros por px; face = azimut (grados) del grabado."""
    bx, by, bz = base
    Z = lambda y: bz - (y - 110) * k
    R = lambda r: r * k
    out = {'orifices': []}
    if 'emm_pol' not in M:
        M['emm_pol'] = studio_metal('emm_pol', [(0.0, 0.30), (0.18, 0.55), (0.30, 0.92), (0.40, 0.62), (0.48, 0.34), (0.56, 0.80),
                                                (0.66, 0.97), (0.78, 0.58), (0.90, 0.40), (1.0, 0.70)], rough=0.2)
        M['emm_hex'] = studio_metal('emm_hex', [(0.0, 0.55), (0.35, 0.72), (0.55, 0.80), (0.75, 0.68), (1.0, 0.55)], rough=0.38)
    body_m = M['emm_pol']
    # tuerca hexagonal
    hx = cyl(f'{name}_hex', (bx, by, Z(210)), R(148), 200 * k, M['emm_hex'], verts=6, bevel=6 * k if detail else 0)
    hx.rotation_euler = (0, 0, math.radians(face - 50))
    # cuello con collarines y garganta
    lathe(f'{name}_neck', [(R(124), Z(310)), (R(118), Z(318)), (R(118), Z(428)), (R(138), Z(431)), (R(138), Z(451)),
                           (R(120), Z(454)), (R(120), Z(465)), (R(137), Z(468)), (R(137), Z(489)), (R(125), Z(492)), (R(125), Z(506))],
          body_m, loc=(bx, by, 0))
    # cabeza: disco superior, banda grabada y cono inferior
    head = lathe(f'{name}_head', [(0, Z(505)), (R(262), Z(505)), (R(268), Z(511)), (R(268), Z(578)), (R(266), Z(584)),
                                  (R(160), Z(762)), (R(150), Z(775)), (R(140), Z(785)), (0, Z(785))], body_m, segs=128, loc=(bx, by, 0))
    if detail:
        txt = KW + 'emm_text.png'
        import os as _os
        if not _os.path.exists(txt):
            from PIL import Image as PImage, ImageDraw as PDraw, ImageFont as PFont
            im = PImage.new('RGBA', (1500, 120), (0, 0, 0, 0))
            f = PFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 100)
            tw = f.getlength('RG SYSTEMS EMM')
            PDraw.Draw(im).text(((1500 - tw) / 2, 2), 'RG SYSTEMS EMM', font=f, fill=(48, 50, 54, 235))
            im.save(txt)
        label_shell(f'{name}_engr', bx, by, R(268.6), Z(578), Z(516), txt, face=face, arc=118, segs=48)
    # 6 insertos de orificio en alojamientos rebajados del cono
    ins_m = M.get('insert') or studio_metal('insert', [(0.0, 0.58), (0.5, 0.76), (1.0, 0.64)], rough=0.55)
    M['insert'] = ins_m
    # insertos integrados en el cuerpo: asiento plano tangente al cono (generatriz) y apenas rebajado
    yc = 664
    rc = 268 - (yc - 584) / (762 - 584) * 108
    nr, nz = 0.855, -0.519
    spots = []
    for i in range(6):
        ph = math.radians(face + 30 + 60 * i)
        n = Vector((math.cos(ph) * nr, math.sin(ph) * nr, nz))
        p = Vector((bx + math.cos(ph) * R(rc), by + math.sin(ph) * R(rc), Z(yc))) - n * R(2)
        spots.append((p, n))
        out['orifices'].append((tuple(p + n * R(2)), tuple(n)))
    out['orifices'].append(((bx, by, Z(785)), (0.0, 0.0, -1.0)))
    if detail:
        if 'emm_pocket' not in M:
            M['emm_pocket'] = studio_metal('emm_pocket', [(0.0, 0.22), (0.4, 0.45), (0.7, 0.62), (1.0, 0.35)], rough=0.3)
        cut_holes(head, hole_cutters(f'{name}_spot', [(p - n * R(10) + n * R(20), n) for p, n in spots], R(72), R(40), m=M['emm_pocket'], segs=64))
        for i, (p, n) in enumerate(spots):
            c = p - n * R(5)
            ins = cyl(f'{name}_ins{i}', c, R(68), R(10), ins_m, verts=48, bevel=R(1.0))
            ins.rotation_euler = n.to_track_quat('Z', 'Y').to_euler()
            ph = math.radians(face + 30 + 60 * i)
            upv = (Vector((0, 0, 1)) - n * n.z).normalized()
            rt = Vector((-math.sin(ph), math.cos(ph), 0.0))
            sg = 1 if i % 2 == 0 else -1
            dpin = (upv * math.cos(math.radians(30)) + rt * sg * math.sin(math.radians(30))).normalized() * R(56)
            top = p
            hc = hole_cutters(f'{name}_ih{i}', [(top, n)], R(4.0), R(16))
            cut_holes(ins, hc)
            hc = hole_cutters(f'{name}_ip{i}', [(top + dpin, n), (top - dpin, n)], R(5.5), R(16))
            cut_holes(ins, hc)
    else:
        for i, (p, n) in enumerate(spots):
            ins = cyl(f'{name}_ins{i}', p - n * R(2), R(64), R(4), ins_m, verts=24)
            ins.rotation_euler = n.to_track_quat('Z', 'Y').to_euler()
    out['tip'] = (bx, by, Z(785)); out['head'] = (bx, by, Z(640))
    return out

def slab(cx, cy, sx, sy, h=0.55):
    box('slab', (cx, cy, -h / 2), (sx, sy, h), M['slab'], bevel=0.12)


KEY = {}


SITE = SHOT in ('site', 'proom2', 'site3', 'gen')


def build_hall():
    if SITE:
        slab(9.2, 0, 32.8, 11.2)
    else:
        slab(0, 0, 14.4, 11.2)
    # suelo técnico: pedestales, cableado y baldosas
    X0, X1, Y0, Y1 = -6.6, 6.6, -5.0, 5.0
    T = 0.6; FH = 0.42
    cut = SHOT in ('floor', 'floor_det', 'floor_det_b')
    hidden = set()
    if cut:
        for ix in range(22):
            for iy in range(17):
                x = X0 + (ix + 0.5) * T; y = Y0 + (iy + 0.5) * T
                if -1.4 < x < 4.6 and -4.95 < y < -3.3:
                    hidden.add((ix, iy))
    for ix in range(22):
        for iy in range(17):
            x = X0 + (ix + 0.5) * T; y = Y0 + (iy + 0.5) * T
            if x > X1 or y > Y1:
                continue
            if (ix, iy) in hidden:
                continue
            perf = (abs(y + 1.25) < 0.6 or abs(y - 1.75) < 0.6) and -4.6 < x < 1.6 and ix % 2 == 0
            box(f't{ix}_{iy}', (x, y, FH - 0.02), (T - 0.012, T - 0.012, 0.04), M['tile_perf' if perf else 'tile'])
    if cut:
        for ix in range(22):
            for iy in range(17):
                if (ix, iy) in hidden:
                    x = X0 + (ix + 0.5) * T; y = Y0 + (iy + 0.5) * T
                    if -4.6 < y - T / 2 + 0.02 < -3.55:
                        continue  # sin pedestales atravesando la bandeja de cables
                    cyl('ped', (x - T / 2 + 0.02, y - T / 2 + 0.02, FH / 2), 0.025, FH, M['ped'], verts=10)
        # bandejas y mazos de cables bajo suelo
        for k, (yy, mt) in enumerate([(-4.3, 'cable_b'), (-3.85, 'cable_y')]):
            box(f'uftray{k}', (1.6, yy, 0.035), (6.0, 0.36, 0.03), M['tray'])
            for j in range(6):
                pipe(f'ufc{k}{j}', (-1.4, yy - 0.12 + j * 0.05, 0.075 + (j % 2) * 0.03), (4.6, yy - 0.12 + j * 0.05, 0.075 + (j % 2) * 0.03), 0.026, M[mt])
        KEY['underfloor'] = [(0.4, -4.1, 0.3), (2.6, -4.1, 0.3), (3.8, -3.9, 0.3)]
        # red bajo suelo: ramal bajo las baldosas con boquillas colgantes
        UFZ = FH - 0.07
        pipe('ufmain', (-1.4, -4.08, UFZ), (4.6, -4.08, UFZ), 0.022, M['steel'])
        KEY['uf_noz'] = []
        for k, x in enumerate((0.0, 1.6, 3.2)):
            pipe(f'ufdr{k}', (x, -4.08, UFZ), (x, -4.08, UFZ - 0.03), 0.014, M['steel'])
            nz = make_emm_closed((x, -4.08, UFZ - 0.03), 0.00055, f'ufnz{k}', broken=(SHOT == 'floor_det_b' and k == 1), detail=True)
            KEY['uf_noz'].append(nz['tip'])
            KEY.setdefault('uf_ring', []).append(nz.get('ring', nz['tip']))
    # muros (corte)
    WH = 3.4
    box('wallL', (X0 - 0.1, 0, WH / 2), (0.2, Y1 - Y0 + 0.2, WH), M['wall'])
    box('wallB', (0, Y1 + 0.1, WH / 2), (X1 - X0 + 0.4, 0.2, WH), M['wall'])
    box('capL', (X0 - 0.1, 0, WH + 0.01), (0.22, Y1 - Y0 + 0.22, 0.02), M['wallcap'])
    box('capB', (0, Y1 + 0.1, WH + 0.01), (X1 - X0 + 0.42, 0.22, 0.02), M['wallcap'])
    # puerta con vidrio en muro trasero
    box('door', (4.6, Y1 - 0.0, 1.5), (1.4, 0.06, 2.3), M['door_glass'])
    box('doorf', (4.6, Y1 + 0.02, 1.5), (1.5, 0.05, 2.4), M['steel_d'])
    # filas de racks
    RW, RD, RH = 0.6, 1.1, 2.25
    rows = [-2.4, 0.6, 3.6]
    KEY['racks'] = []
    for r_i, yc in enumerate(rows):
        for k in range(10):
            x = -4.3 + k * RW
            box(f'rack{r_i}_{k}', (x, yc, FH + RH / 2), (RW - 0.02, RD, RH), M['rack'], bevel=0.008)
            dr = box(f'door{r_i}_{k}', (x, yc - RD / 2 - 0.006, FH + RH / 2), (RW - 0.06, 0.01, RH - 0.08), DOOR)
            KEY['racks'].append((x, yc - RD / 2, FH + RH))
        # bandeja portacables sobre la fila
        box(f'tray{r_i}', (-4.3 + 4.5 * RW, yc, FH + RH + 0.45), (10 * RW + 0.2, 0.45, 0.06), M['tray'])
        for j in range(5):
            pipe(f'cab{r_i}{j}', (-4.6, yc - 0.15 + j * 0.07, FH + RH + 0.5), (1.6, yc - 0.15 + j * 0.07, FH + RH + 0.5), 0.025,
                 M['cable_y' if j % 2 else 'cable_g'])
    # climatizadoras (CRAC) junto al muro izquierdo
    for j, yy in enumerate((-2.6, 1.2)):
        box(f'crac{j}', (-5.95, yy, FH + 1.0), (0.9, 2.2, 2.0), M['crac'], bevel=0.02)
        box(f'grl{j}', (-5.49, yy, FH + 1.45), (0.02, 1.9, 0.7), M['grille'])
    # SAI / cuadros eléctricos en zona derecha
    for j in range(3):
        box(f'ups{j}', (4.6 + j * 0.75, 3.9, FH + 1.0), (0.7, 0.8, 2.0), M['crac'], bevel=0.01)
        box(f'upsp{j}', (4.6 + j * 0.75, 3.49, FH + 1.4), (0.4, 0.02, 0.3), M['grille'])
    # red de agua nebulizada (acero inoxidable) y boquillas cerradas
    PZ = FH + RH + 1.0
    KEY['nozzles'] = []
    MX = X1 - 0.3
    pipe('main', (X0 + 0.2, -3.6, PZ), (X0 + 0.2, 2.1, PZ), 0.04, M['steel'])
    # colector del CPD: alimentado desde la sala de bombeo aledaña
    pipe('mainR', (MX, -3.6, PZ), (MX, Y1 - 0.15, PZ), 0.05, M['steel'])
    KEY['gp_main'] = [(MX, Y1 - 0.15, PZ), (MX, -3.6, PZ)]
    KEY['gp_br'] = [(MX, yy, PZ) for yy in (-3.6, -0.9, 2.1)] + [(X0 + 0.2, yy, PZ) for yy in (-3.6, -0.9, 2.1)]
    for yy in (-3.6, -0.9, 2.1):
        pipe(f'br{yy}', (X0 + 0.2, yy, PZ), (MX, yy, PZ), 0.03, M['steel'])
        for k in range(7):
            x = -4.6 + k * 1.75
            pipe(f'dr{yy}{k}', (x, yy, PZ), (x, yy, PZ - 0.12), 0.018, M['steel'])
            nz = make_mmp50((x, yy, PZ - 0.12), 0.00085, f'nz{yy}{k}', 'm32', detail=(SHOT == 'med'))
            KEY['nozzles'].append(nz['tip'])
    # foco: rack de la fila delantera
    KEY['fire'] = (-4.3 + 4 * RW, -2.4 - RD / 2 - 0.05, FH + 1.3)
    KEY['fire_top'] = (-4.3 + 4 * RW, -2.4, FH + RH)
    KEY['fire_nozzle'] = (-4.6 + 2 * 1.75, -3.6, PZ - 0.12 - 0.00085 * 280)
    KEY['crac_out'] = (-5.45, -2.6, FH + 1.45)
    if SITE:
        build_pump_annex(X1, Y0, Y1, PZ, MX)
        build_gen_annex(X1, Y1)
        build_front_rooms()
    KEY['aisle'] = [(-1.5, -0.9, FH + 0.5), (-1.5, 2.1, FH + 0.5), (1.0, -0.9, FH + 1.2)]



def build_ceiling_detail(broken):
    s = 10.0
    # bloque de falso techo (corte)
    c = box('ceil', (0, 0, 0.075), (4.0, 4.0, 0.15), M['crac'], bevel=0.01)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.0, -1.0, 0.075))
    cc = bpy.context.object; cc.scale = (2.0, 2.0, 0.4); cc.hide_render = True; cc.hide_viewport = True
    bo = c.modifiers.new('cut', 'BOOLEAN'); bo.operation = 'DIFFERENCE'; bo.object = cc
    for i in (-1, 1):
        box(f'tg{i}', (i * 0.0, 0, 0.0), (4.0, 0.04, 0.012), M['steel_d'])
        box(f'tgx{i}', (0, 0, 0.0), (0.04, 4.0, 0.012), M['steel_d'])
    # tubería por encima del techo (asoma por los cortes)
    pipe('pmain', (-2.6, 0.9, 0.62), (2.6, 0.9, 0.62), 0.17, M['steel'])
    pipe('pdrop', (0.9, 0.9, 0.62), (0.9, 0.0, 0.62), 0.09, M['steel'])
    pipe('pdrop2', (0.9, 0.0, 0.62), (0.0, 0.0, 0.62), 0.09, M['steel'])
    pipe('pdrop3', (0.0, 0.0, 0.62), (0.0, 0.0, 108 * 0.0034), 0.08, M['steel'])
    nz = make_mmp50((0, 0, 108 * 0.0034), 0.0034, 'det', 'ceil', broken=broken, detail=True)
    L = bpy.data.lights.new('under', 'AREA'); L.energy = 900; L.size = 6
    lo = bpy.data.objects.new('under', L); COL.objects.link(lo); lo.location = (2.5, -3.5, -4.0)
    lo.rotation_euler = (Vector((0, 0, 0)) - lo.location).to_track_quat('-Z', 'Y').to_euler()
    KEY['orif'] = [[p, (Vector(p) + Vector(dv) * 1.0)[:]] for p, dv in nz['orifices']]
    KEY['bulb'] = nz['bulb']; KEY['tip'] = nz['tip']; KEY['slot'] = nz['slot']
    KEY['esc'] = nz['esc']; KEY['hex'] = nz['hex']



def build_pumproom(annex=False):
    if not annex:
        slab(0, 0, 10.6, 8.6)
    X0, X1, Y0, Y1 = -4.9, 4.9, -3.9, 3.9
    WH = 3.6
    box('floor', (0, 0, 0.01), (X1 - X0, Y1 - Y0, 0.02), mat('epoxy', (0.70, 0.74, 0.72), 0.55))
    if not annex:
        box('wallL', (X0 - 0.1, 0, WH / 2), (0.2, Y1 - Y0 + 0.2, WH), M['wall'])
    box('wallB', (0, Y1 + 0.1, WH / 2), (X1 - X0 + 0.4, 0.2, WH), mat('wallbeige', (0.72, 0.68, 0.60), 0.9))
    if not annex:
        box('capL', (X0 - 0.1, 0, WH + 0.01), (0.22, Y1 - Y0 + 0.22, 0.02), M['wallcap'])
    box('capB', (0, Y1 + 0.1, WH + 0.01), (X1 - X0 + 0.42, 0.22, 0.02), M['wallcap'])
    # bandeja de cables perimetral
    box('trayB', (0.2, Y1 - 0.18, WH - 0.55), (9.2, 0.28, 0.05), M['tray'])
    fx, fy = 0.6, 2.2
    gx, gy = 3.0, -0.2
    # depósito principal (acero inox, fondo cónico sobre patas)
    tx, ty = -3.4, 2.4
    cyl('tank', (tx, ty, 2.05), 1.15, 2.1, M['tank'], verts=64, bevel=0.02)
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.15, radius2=1.25, depth=0.7, location=(tx, ty, 0.65))
    o = bpy.context.object; o.data.materials.append(M['tank']); bpy.ops.object.shade_smooth()
    cyl('tanklid', (tx, ty, 3.12), 1.27, 0.06, M['steel_d'], verts=64)
    cyl('manhole', (tx + 0.3, ty, 3.2), 0.32, 0.12, M['steel'], verts=32)
    for a_ in range(4):
        ang = a_ * math.pi / 2 + math.pi / 4
        cyl(f'leg{a_}', (tx + math.cos(ang) * 1.05, ty + math.sin(ang) * 1.05, 0.65), 0.05, 1.3, M['steel'], verts=12)
    pipe('lvl', (tx - 1.3, ty - 0.2, 1.1), (tx - 1.3, ty - 0.2, 2.9), 0.03, M['steel'])
    # depósito auxiliar
    sx_, sy_ = -1.0, 2.9
    cyl('tank2', (sx_, sy_, 1.35), 0.68, 1.1, M['tank'], verts=48, bevel=0.02)
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.12, radius2=0.68, depth=0.35, location=(sx_, sy_, 0.62))
    o = bpy.context.object; o.data.materials.append(M['tank']); bpy.ops.object.shade_smooth()
    sph('tank2top', (sx_, sy_, 1.9), 0.68, M['tank'], (1, 1, 0.25))
    for a_ in range(3):
        ang = a_ * 2 * math.pi / 3
        cyl(f'leg2{a_}', (sx_ + math.cos(ang) * 0.55, sy_ + math.sin(ang) * 0.55, 0.4), 0.035, 0.8, M['steel'], verts=12)
    # tubería de aspiración por el suelo: depósito -> filtros -> grupo
    pipe('s1', (tx + 0.3, ty - 0.9, 0.55), (tx + 0.3, ty - 0.9, 0.16), 0.07, M['steel'])
    pipe('s2', (tx + 0.3, ty - 0.9, 0.16), (tx + 0.3, 1.2, 0.16), 0.07, M['steel'])
    pipe('s3', (tx + 0.3, 1.2, 0.16), (fx - 0.28, 1.2, 0.16), 0.07, M['steel'])
    pipe('s4', (sx_, sy_, 0.4), (sx_, 1.2, 0.16), 0.05, M['steel'])
    # skid de filtros (bastidor rojo)
    red = M['redcab']
    box('fskid', (fx, fy, 0.08), (1.4, 1.1, 0.12), red)
    for dx in (-0.62, 0.62):
        box(f'fpost{dx}', (fx + dx, fy - 0.45, 0.85), (0.08, 0.08, 1.5), red)
        box(f'fpostb{dx}', (fx + dx, fy + 0.45, 0.85), (0.08, 0.08, 1.5), red)
    for i, dx in enumerate((-0.28, 0.28)):
        cyl(f'filt{i}', (fx + dx, fy, 0.95), 0.17, 0.95, M['steel'], verts=32, bevel=0.01)
        cyl(f'filtc{i}', (fx + dx, fy, 1.47), 0.19, 0.08, M['steel_d'], verts=32)
    pipe('fin2', (fx - 0.28, 1.2, 0.16), (fx - 0.28, fy, 0.48), 0.06, M['steel'])
    pipe('fout', (fx + 0.28, fy, 0.48), (fx + 0.28, gy - 0.35, 0.3), 0.06, M['steel'])
    cyl('fvalve', (fx + 0.28, fy - 0.55, 1.15), 0.09, 0.05, M['red'], rot=(math.pi / 2, 0, 0))
    # ---------- grupo de bombeo ----------
    blk = mat('skidblk', (0.03, 0.03, 0.035), 0.35, 0.2)
    box('gskid', (gx, gy, 0.14), (3.0, 1.25, 0.2), blk, bevel=0.02)
    for dx in (-1.35, 1.35):
        for dy in (-0.52, 0.52):
            cyl(f'gfoot{dx}{dy}', (gx + dx, gy + dy, 0.03), 0.06, 0.06, M['motor'])
    # motor eléctrico (protagonista)
    mx = gx + 0.65
    mot = mat('motorblk', (0.035, 0.037, 0.04), 0.4, 0.3)
    cyl('motor', (mx, gy, 0.82), 0.42, 1.05, mot, rot=(0, math.pi / 2, 0), verts=64, bevel=0.03)
    for f in range(16):
        cyl(f'mfin{f}', (mx - 0.42 + f * 0.056, gy, 0.82), 0.445, 0.018, mot, rot=(0, math.pi / 2, 0), verts=48)
    cyl('mfan', (mx + 0.62, gy, 0.82), 0.44, 0.22, mot, rot=(0, math.pi / 2, 0), verts=64, bevel=0.03)
    cyl('mfang', (mx + 0.735, gy, 0.82), 0.38, 0.01, M['grille'], rot=(0, math.pi / 2, 0), verts=64)
    box('mtb', (mx - 0.15, gy, 1.33), (0.42, 0.36, 0.2), mot, bevel=0.02)
    for dx in (-0.08, 0.08):
        cyl(f'mgland{dx}', (mx - 0.15 + dx, gy - 0.19, 1.33), 0.035, 0.05, M['crac'], rot=(math.pi / 2, 0, 0), verts=16)
    box('mfeet', (mx, gy, 0.33), (0.9, 0.7, 0.1), mot)
    box('mplate', (mx + 0.05, gy - 0.415, 0.86), (0.18, 0.02, 0.12), mat('plate', (0.85, 0.85, 0.8), 0.4))
    cyl('mshaft', (mx - 0.63, gy, 0.82), 0.12, 0.25, M['steel_d'], rot=(0, math.pi / 2, 0))
    # bomba de pistones (latón) + manifold inox
    px = gx - 0.35
    brass = M['brass']
    box('pump', (px, gy, 0.8), (0.42, 0.5, 0.36), brass, bevel=0.03)
    box('pumpbase', (px + 0.1, gy, 0.52), (0.6, 0.55, 0.2), M['motor'])
    for k_ in range(3):
        cyl(f'phead{k_}', (px - 0.25, gy - 0.16 + k_ * 0.16, 0.86), 0.05, 0.12, brass, rot=(0, math.pi / 2, 0))
    box('frame', (gx - 1.0, gy - 0.3, 0.9), (0.08, 0.08, 1.35), blk)
    pipe('mani1', (gx - 1.45, gy - 0.35, 1.25), (gx - 0.75, gy - 0.35, 1.25), 0.08, M['steel'])
    pipe('mani2', (gx - 1.45, gy - 0.35, 0.45), (gx - 0.75, gy - 0.35, 0.45), 0.06, M['steel'])
    cyl('fl1', (gx - 1.47, gy - 0.35, 1.25), 0.13, 0.04, M['steel'], rot=(0, math.pi / 2, 0))
    cyl('fl2', (gx - 1.47, gy - 0.35, 0.45), 0.11, 0.04, M['steel'], rot=(0, math.pi / 2, 0))
    pipe('disc', (px - 0.25, gy - 0.1, 0.9), (gx - 0.9, gy - 0.35, 1.25), 0.035, M['steel'])
    for k_, dx in enumerate((-1.3, -1.0)):
        cyl(f'gauge{k_}', (gx + dx, gy - 0.35, 1.48), 0.075, 0.035, M['crac'], rot=(math.pi / 2, 0, 0), verts=32)
        pipe(f'gst{k_}', (gx + dx, gy - 0.35, 1.3), (gx + dx, gy - 0.35, 1.42), 0.015, M['steel'])
    cyl('relief', (gx - 1.15, gy - 0.35, 1.55), 0.05, 0.35, M['steel'])
    box('rvalve', (gx - 0.82, gy - 0.35, 1.38), (0.12, 0.12, 0.12), M['red'])
    # conexión aspiración -> grupo y salida hacia la red (montantes por el muro)
    pipe('suc', (fx + 0.28, gy - 0.35, 0.3), (gx - 1.45, gy - 0.35, 0.45), 0.06, M['steel'])
    pipe('r1', (gx - 1.45, gy - 0.35, 1.25), (gx - 1.8, gy - 0.35, 1.25), 0.06, M['steel'])
    pipe('r2', (gx - 1.8, gy - 0.35, 1.25), (gx - 1.8, Y1 - 0.15, 1.25), 0.06, M['steel'])
    pipe('r3', (gx - 1.8, Y1 - 0.15, 1.25), (gx - 1.8, Y1 - 0.15, WH), 0.05, M['steel'])
    pipe('r4', (gx - 1.4, Y1 - 0.15, 1.25), (gx - 1.4, Y1 - 0.15, WH), 0.05, M['steel'])
    pipe('r5', (gx - 1.8, Y1 - 0.15, 1.25), (gx - 1.4, Y1 - 0.15, 1.25), 0.05, M['steel'])
    for zz in (2.0, 3.0):
        cyl(f'rv{zz}', (gx - 1.6, Y1 - 0.15, zz), 0.07, 0.12, M['brass'])
    # cuadro de control en el muro del fondo
    cx_, cy_ = 2.7, Y1 - 0.3
    box('cab', (cx_, cy_, 1.75), (0.95, 0.4, 1.3), M['redcab'], bevel=0.01)
    box('cabplinth', (cx_, cy_, 0.55), (0.3, 0.3, 1.1), M['redcab'])
    box('cabpanel', (cx_, cy_ - 0.205, 1.95), (0.5, 0.01, 0.35), M['panel_blue'])
    cg = mat('cgreen', (0.08, 0.38, 0.12), 0.5)
    for k_, dx in enumerate((-0.1, 0.1)):
        p1 = (cx_ + dx, cy_, 1.1); p2 = (cx_ + dx, cy_, 0.06); p3 = (mx - 0.15 + dx, cy_, 0.06)
        p4 = (mx - 0.15 + dx, gy + 0.9, 0.06); p5 = (mx - 0.15 + dx, gy + 0.1, 1.38)
        for q in range(4):
            pipe(f'cab_c{k_}{q}', (p1, p2, p3, p4)[q], (p2, p3, p4, p5)[q], 0.025, cg)
    KEY['motor'] = (mx + 0.1, gy - 0.4, 0.9)
    KEY['motor_c'] = (mx, gy, 0.85)
    KEY['pump'] = (px, gy - 0.25, 0.85)
    KEY['tank'] = (tx - 0.4, ty - 1.2, 2.3)
    KEY['filters'] = (fx, fy - 0.5, 1.2)
    KEY['cab'] = (cx_ - 0.2, cy_ - 0.2, 2.1)
    KEY['group'] = (gx, gy, 0.8)
    KEY['riser'] = (gx - 1.6, Y1 - 0.15, 2.6)


def build_pump_annex(X1h, Y0h, Y1h, PZ, MX):
    """sala de bombeo aledaña (lado +x): reutiliza build_pumproom desplazada, con muro medianero bajo"""
    before = set(bpy.data.objects)
    keys_before = dict(KEY)
    build_pumproom(annex=True)
    DXa, DYa = X1h + 0.2 + 5.1, Y1h - 3.9
    for o in set(bpy.data.objects) - before:
        if o.parent is None:
            o.location.x += DXa; o.location.y += DYa
    for k, v in list(KEY.items()):
        if k in keys_before and keys_before[k] is v:
            continue
        if isinstance(v, tuple) and len(v) == 3:
            KEY[k] = (v[0] + DXa, v[1] + DYa, v[2])
    RY0 = -3.9 + DYa
    box('awallM', (X1h + 0.1, (RY0 + Y1h) / 2, 0.55), (0.2, Y1h - RY0, 1.1), M['wall'])
    box('acapM', (X1h + 0.1, (RY0 + Y1h) / 2, 1.11), (0.22, Y1h - RY0, 0.02), M['wallcap'])
    box('askirt', (X1h + 0.02, (Y0h + RY0) / 2, 0.22), (0.06, RY0 - Y0h + 0.1, 0.44), M['wallcap'])
    # impulsión: montante de la sala de bombeo -> colector del CPD
    rx = KEY['riser'][0]
    ry = Y1h - 0.15
    pipe('feedA', (rx, ry, 3.6), (rx, ry, PZ), 0.05, M['steel'])
    pipe('feedB', (rx, ry, PZ), (MX, ry, PZ), 0.055, M['steel'])
    sph('feedel', (rx, ry, PZ), 0.06, M['steel'])
    KEY['gp_feed'] = [(rx, ry, 1.3), (rx, ry, PZ), (MX, ry, PZ)]
    KEY['annex'] = (X1h + 0.2 + 5.0, (RY0 + Y1h) / 2, 1.0)


def uac_cyl(x, y, name, n2=False, r=0.135, h=1.45):
    """cilindro UAC (agua o N2) con etiqueta blanca RG Systems"""
    cyl(name + 'b', (x, y, 0.06 + h / 2), r, h, M['red'], verts=40)
    sph(name + 't', (x, y, 0.06 + h), r, M['green'] if n2 else M['red'], (1, 1, 0.9))
    sph(name + 'f', (x, y, 0.06), r, M['red'], (1, 1, 0.3))
    top = 0.06 + h + r * 0.9
    cyl(name + 'fl', (x, y, top + 0.01), 0.06, 0.02, M['steel'])
    cyl(name + 'v', (x, y, top + 0.06), 0.04, 0.1, M['brass'])
    box(name + 'vb', (x, y, top + 0.12), (0.12, 0.05, 0.05), M['brass'])
    label_shell(name + 'lab', x, y, r + 0.003, 0.06 + h * 0.42, 0.06 + h * 0.42 + 0.44 * (r / 0.135), LABEL_RG, face=-50, arc=150)
    return (x, y, top + 0.15)


def build_front_rooms():
    """salas de apoyo del data center en la franja delantera: NOC, SAI/baterías y sala eléctrica"""
    Y0f, Y1f = -5.35, -2.95
    yc = (Y0f + Y1f) / 2
    # muros bajos de compartimentación (mismo lenguaje de corte que el resto)
    box('fwallB', (16.1, Y1f + 0.05, 0.55), (18.6, 0.2, 1.1), M['wall'])
    box('fcapB', (16.1, Y1f + 0.05, 1.11), (18.62, 0.22, 0.02), M['wallcap'])
    for xw in (12.1, 17.05):
        box(f'fwall{xw}', (xw, yc, 0.55), (0.2, Y1f - Y0f, 1.1), M['wall'])
        box(f'fcap{xw}', (xw, yc, 1.11), (0.22, Y1f - Y0f + 0.02, 0.02), M['wallcap'])
    box('fwallL', (6.9, yc, 0.55), (0.2, Y1f - Y0f, 1.1), M['wall'])
    box('fcapL', (6.9, yc, 1.11), (0.22, Y1f - Y0f + 0.02, 0.02), M['wallcap'])
    # --- sala de control (NOC) ---
    box('nocfloor', (9.5, yc, 0.012), (5.0, Y1f - Y0f, 0.02), mat('carpet', (0.32, 0.36, 0.42), 0.9))
    scr = mat('noc_scr', (0.05, 0.12, 0.25), 0.3, 0.0, (0.15, 0.45, 0.95), 1.4)
    dark = mat('noc_dark', (0.06, 0.065, 0.07), 0.4, 0.2)
    deskm = mat('noc_desk', (0.85, 0.85, 0.86), 0.5)
    box('vwall', (9.5, Y1f - 0.25, 1.35), (3.2, 0.12, 1.25), dark, bevel=0.01)
    box('vwalls', (9.5, Y1f - 0.32, 1.35), (3.0, 0.02, 1.1), scr)
    box('vwallst', (9.5, Y1f - 0.22, 0.38), (0.25, 0.25, 0.75), dark)
    for r_, yy in enumerate((yc + 0.05, yc - 0.95)):
        for dx in (-1.25, 1.25):
            x0 = 9.5 + dx
            box(f'desk{r_}{dx}', (x0, yy, 0.74), (1.9, 0.75, 0.05), deskm, bevel=0.01)
            for lx in (-0.85, 0.85):
                box(f'dleg{r_}{dx}{lx}', (x0 + lx, yy, 0.37), (0.05, 0.65, 0.72), dark)
            for mx_ in (-0.45, 0.45):
                box(f'mon{r_}{dx}{mx_}', (x0 + mx_, yy + 0.2, 1.0), (0.62, 0.04, 0.38), dark, bevel=0.005)
                box(f'mons{r_}{dx}{mx_}', (x0 + mx_, yy + 0.177, 1.0), (0.56, 0.01, 0.32), scr)
                box(f'monb{r_}{dx}{mx_}', (x0 + mx_, yy + 0.22, 0.8), (0.06, 0.06, 0.12), dark)
            for cx_ in (-0.45, 0.45):
                box(f'chs{r_}{dx}{cx_}', (x0 + cx_, yy - 0.6, 0.48), (0.48, 0.48, 0.08), dark, bevel=0.02)
                box(f'chb{r_}{dx}{cx_}', (x0 + cx_, yy - 0.82, 0.78), (0.46, 0.06, 0.5), dark, bevel=0.02)
                cyl(f'chp{r_}{dx}{cx_}', (x0 + cx_, yy - 0.6, 0.24), 0.03, 0.45, M['steel_d'])
    # --- sala de SAI y baterías ---
    box('upsfloor', (14.6, yc, 0.012), (4.8, Y1f - Y0f, 0.02), mat('epoxy2', (0.70, 0.72, 0.74), 0.55))
    cabm = mat('ups_cab', (0.80, 0.81, 0.82), 0.45)
    batm = mat('bat_cab', (0.22, 0.24, 0.27), 0.45, 0.2)
    for j in range(6):
        x = 12.7 + j * 0.62
        box(f'bat{j}', (x, Y1f - 0.55, 0.95), (0.58, 0.75, 1.9), batm, bevel=0.008)
        box(f'batv{j}', (x, Y1f - 0.93, 1.45), (0.4, 0.01, 0.3), M['grille'])
    for j in range(3):
        x = 13.0 + j * 0.85
        box(f'ups{j}', (x, Y0f + 0.55, 0.95), (0.8, 0.8, 1.9), cabm, bevel=0.008)
        box(f'upsp{j}', (x, Y0f + 0.95, 1.45), (0.35, 0.01, 0.25), M['panel_blue'])
    # --- sala eléctrica: transformadores y cuadros ---
    box('elfloor', (21.2, yc, 0.012), (8.2, Y1f - Y0f, 0.02), mat('epoxy3', (0.66, 0.68, 0.70), 0.55))
    trm = mat('trafo', (0.42, 0.47, 0.50), 0.45, 0.3)
    for j, x in enumerate((19.0, 21.4)):
        box(f'tr{j}', (x, yc + 0.1, 0.9), (1.5, 1.1, 1.7), trm, bevel=0.02)
        for f in range(7):
            box(f'trf{j}{f}', (x - 0.6 + f * 0.2, yc - 0.48, 0.85), (0.05, 0.12, 1.4), trm)
        for b_ in (-0.4, 0, 0.4):
            cyl(f'trb{j}{b_}', (x + b_, yc + 0.1, 1.9), 0.06, 0.2, M['crac'])
        box(f'trbase{j}', (x, yc + 0.1, 0.04), (1.7, 1.3, 0.08), M['motor'])
    swm = mat('switchgear', (0.78, 0.80, 0.81), 0.45)
    for j in range(5):
        x = 23.1 + j * 0.42
        box(f'sw{j}', (x, Y1f - 0.45, 1.05), (0.4, 0.6, 2.1), swm, bevel=0.005)
        box(f'swp{j}', (x, Y1f - 0.76, 1.5), (0.22, 0.01, 0.28), M['grille'])
    KEY['noc'] = (9.5, yc, 1.0); KEY['ups'] = (14.6, yc, 1.0); KEY['elec'] = (21.2, yc, 1.0)


def build_gen_annex(X1h, Y1h):
    """batería UAC en la sala intermedia (bombeo) + sala de generadores aledaña con difusores abiertos RG EMM"""
    RY0 = -2.8
    GX0, GX1 = 16.95, 25.4
    # ---- batería de cilindros UAC (N2 + agua) en la sala intermedia ----
    # batería anclada al muro del fondo de la sala intermedia (entre el cuadro de control y la sala de generadores)
    by_ = Y1h - 0.36
    WY = Y1h - 0.03
    xs = [15.42 + i * 0.30 for i in range(5)]
    tops = [uac_cyl(x, by_, f'uac{i}', n2=(i == 0)) for i, x in enumerate(xs)]
    for zz in (0.5, 1.15):
        box(f'uacbar{zz}', ((xs[0] + xs[-1]) / 2, by_ + 0.2, zz), (xs[-1] - xs[0] + 0.42, 0.05, 0.04), M['steel_d'])
        for x in xs:
            bpy.ops.mesh.primitive_torus_add(major_radius=0.141, minor_radius=0.01, location=(x, by_, zz))
            bpy.context.object.data.materials.append(M['steel'])
        for xx in (xs[0] - 0.21, xs[-1] + 0.21):
            box(f'uacbrk{zz}{xx}', (xx, (by_ + 0.2 + WY) / 2, zz), (0.05, WY - by_ - 0.2 + 0.03, 0.06), M['steel_d'])
    MZ = 2.15
    MY = by_ + 0.12
    pipe('uacmani', (xs[1] - 0.1, MY, MZ), (xs[-1] + 0.2, MY, MZ), 0.035, M['steel'])
    box('uacsol', (xs[2] + 0.15, MY, MZ + 0.1), (0.1, 0.08, 0.12), M['black'])
    for xx in (xs[1], xs[-1]):
        box(f'uacmb{xx}', (xx, (MY + WY) / 2, MZ), (0.04, WY - MY, 0.04), M['steel_d'])
    for i, t in enumerate(tops[1:], 1):
        pipe(f'uachose{i}', t, (t[0], MY, MZ), 0.012, M['black'])
    # actuador del N2 (pilotaje) anclado al muro sobre el cilindro de N2
    box('uacact', (xs[0], WY - 0.06, 2.05), (0.1, 0.1, 0.22), M['brass'])
    pipe('uacn2', tops[0], (xs[0], WY - 0.06, 1.94), 0.01, M['black'])
    pipe('uacn2b', (xs[0] + 0.05, WY - 0.06, 2.1), (xs[1] - 0.1, MY, MZ), 0.008, M['steel'])
    # impulsión por el muro del fondo hasta la sala de generadores
    FZ = 3.15
    rx = xs[-1] + 0.2
    pipe('uacr', (rx, MY, MZ), (rx, MY, FZ), 0.035, M['steel'])
    pipe('uacf', (rx, MY, FZ), (22.6, MY, FZ), 0.035, M['steel'])
    sph('uacel', (rx, MY, FZ), 0.04, M['steel'])
    # ---- sala de generadores ----
    box('gfloor', ((GX0 + GX1) / 2, (RY0 + Y1h) / 2, 0.01), (GX1 - GX0, Y1h - RY0, 0.02), mat('epoxyg', (0.66, 0.68, 0.70), 0.55))
    box('gwallB', ((17.02 + GX1) / 2, Y1h + 0.1, 1.8), (GX1 - 17.02, 0.2, 3.6), M['wall'])
    box('gcapB', ((17.02 + GX1) / 2, Y1h + 0.1, 3.61), (GX1 - 17.02, 0.22, 0.02), M['wallcap'])
    box('gwallM', (GX0, (RY0 + Y1h) / 2, 0.55), (0.2, Y1h - RY0, 1.1), M['wall'])
    box('gcapM', (GX0, (RY0 + Y1h) / 2, 1.11), (0.22, Y1h - RY0, 0.02), M['wallcap'])
    gs = mat('genset', (0.20, 0.27, 0.30), 0.45, 0.3)
    alt = mat('alter', (0.10, 0.14, 0.20), 0.4, 0.4)
    KEY['gens'] = []
    for gi, gx in enumerate((19.2, 22.6)):
        gy = 1.0
        box(f'gskid{gi}', (gx, gy, 0.12), (1.5, 3.8, 0.22), M['motor'], bevel=0.02)
        box(f'grad{gi}', (gx, gy - 1.55, 1.05), (1.35, 0.35, 1.6), gs, bevel=0.02)
        box(f'grill{gi}', (gx, gy - 1.735, 1.05), (1.15, 0.02, 1.3), M['grille'])
        box(f'geng{gi}', (gx, gy - 0.45, 0.95), (1.05, 1.6, 1.25), gs, bevel=0.04)
        box(f'gengt{gi}', (gx, gy - 0.45, 1.65), (0.7, 1.3, 0.2), M['motor'], bevel=0.02)
        cyl(f'galt{gi}', (gx, gy + 0.85, 0.95), 0.55, 1.0, alt, rot=(math.pi / 2, 0, 0), verts=48, bevel=0.03)
        box(f'gctrl{gi}', (gx + 0.0, gy + 0.85, 1.75), (0.6, 0.5, 0.45), M['redcab'], bevel=0.01)
        cyl(f'gsil{gi}', (gx + 0.25, gy - 0.3, 2.35), 0.22, 1.3, M['steel_d'], rot=(math.pi / 2, 0, 0), verts=32)
        pipe(f'gex{gi}', (gx + 0.25, gy - 0.3, 1.8), (gx + 0.25, gy - 0.3, 2.13), 0.07, M['steel_d'])
        pipe(f'gex2{gi}', (gx + 0.25, gy + 0.35, 2.35), (gx + 0.25, gy + 0.35, 3.6), 0.08, M['steel_d'])
        KEY['gens'].append((gx, gy - 0.45, 1.6))
        # ramal y difusores abiertos RG EMM sobre cada grupo
        pipe(f'gbr{gi}', (gx, MY, FZ), (gx, -1.0, FZ), 0.028, M['steel'])
        sph(f'gbrel{gi}', (gx, MY, FZ), 0.04, M['steel'])
        for ni, ny in enumerate((-0.75, 0.6, 1.95)):
            pipe(f'gdr{gi}{ni}', (gx, ny, FZ), (gx, ny, FZ - 0.1), 0.014, M['steel'])
            nz = make_emm_open((gx, ny, FZ - 0.1), 0.00027, f'gnz{gi}{ni}', detail=(SHOT in ('gen', 'gnoz', 'emm')))
            KEY.setdefault('gnoz', []).append(nz['tip'])
            if gi == 0 and ni == 0:
                KEY['cn_orif'] = [[p_, tuple(Vector(p_) + Vector(d_) * 0.25)] for p_, d_ in nz['orifices']]
                KEY['cn_tip'] = nz['tip']; KEY['cn_head'] = nz['head']
    if SHOT == 'gnoz':
        # techo solo para el primer plano del difusor
        box('gceil', ((6.8 + GX1) / 2, (RY0 + Y1h) / 2, 3.68), (GX1 - 6.8, Y1h - RY0 + 3.0, 0.12), M['crac'])
        Lc = bpy.data.lights.new('gunder', 'AREA'); Lc.energy = 40; Lc.size = 3
        lo_ = bpy.data.objects.new('gunder', Lc); COL.objects.link(lo_); lo_.location = (20.6, -2.6, 1.6)
        lo_.rotation_euler = (Vector((19.2, -0.75, 2.9)) - lo_.location).to_track_quat('-Z', 'Y').to_euler()
    # detección: detectores de llama UV/IR en el muro del fondo + central de extinción
    KEY['gdet'] = []
    for di, dxx in enumerate((18.3, 21.7)):
        box(f'gdetb{di}', (dxx, Y1h - 0.04, 2.85), (0.16, 0.08, 0.16), M['steel_d'])
        dt = cyl(f'gdet{di}', (dxx, Y1h - 0.13, 2.8), 0.07, 0.14, M['crac'], verts=24, bevel=0.01)
        dt.rotation_euler = (math.radians(55), 0, 0)
        cyl(f'gdetl{di}', (dxx, Y1h - 0.2, 2.75), 0.035, 0.01, M['panel_blue'], rot=(math.radians(55), 0, 0), verts=16)
        KEY['gdet'].append((dxx, Y1h - 0.2, 2.75))
    box('gpanel', (17.7, Y1h - 0.12, 1.55), (0.55, 0.16, 0.7), M['redcab'], bevel=0.01)
    box('gpanelp', (17.7, Y1h - 0.205, 1.62), (0.32, 0.01, 0.22), M['panel_blue'])
    pipe('gpanelc', (17.7, Y1h - 0.1, 1.9), (17.7, Y1h - 0.1, 3.3), 0.015, mat('cred', (0.6, 0.05, 0.04), 0.5))
    KEY['gpanel'] = (17.7, Y1h - 0.21, 1.6)
    KEY['gfire'] = (19.2, 0.55, 1.35)
    KEY['gfire_top'] = (19.2, 0.55, 1.78)
    # cuadro eléctrico de transferencia en el muro del fondo
    box('gats', (24.4, Y1h - 0.25, 1.3), (1.2, 0.4, 2.2), M['crac'], bevel=0.01)
    box('gatsp', (24.4, Y1h - 0.455, 1.6), (0.6, 0.02, 0.5), M['grille'])
    KEY['uac'] = (xs[3], by_ - 0.14, 1.0)
    KEY['uac_n2'] = (xs[0], by_ - 0.1, 1.7)
    KEY['uac_route'] = [(rx, MY, MZ), (rx, MY, FZ), (19.2, MY, FZ), (22.6, MY, FZ)]
    KEY['uac_br'] = [(19.2, MY, FZ), (19.2, -1.0, FZ), (22.6, MY, FZ), (22.6, -1.0, FZ)]
    KEY['genroom'] = ((GX0 + GX1) / 2, 1.2, 1.0)
    KEY['gen_noz'] = (19.2, 0.6, FZ - 0.2)


def build_gen_nozzle_detail():
    """primer plano del difusor abierto RG EMM en la sala de máquinas, mismo concepto que el detalle de techo del CPD"""
    FACE = -57.5
    box('gslab', (0, 0, 1.42), (5.2, 5.2, 0.32), M['crac'], bevel=0.01)
    pipe('gpipe', (-3.2, 0.0, 0.98), (3.2, 0.0, 0.98), 0.13, M['steel'])
    for hx_ in (-1.7, 1.7):
        pipe(f'grod{hx_}', (hx_, 0, 1.11), (hx_, 0, 1.27), 0.022, M['steel_d'])
        bpy.ops.mesh.primitive_torus_add(major_radius=0.145, minor_radius=0.02, location=(hx_, 0, 0.98), rotation=(0, math.pi / 2, 0))
        bpy.context.object.data.materials.append(M['steel_d'])
    cyl('gtee', (0, 0, 0.98), 0.165, 0.42, M['steel'], rot=(0, math.pi / 2, 0), verts=48)
    cyl('gteed', (0, 0, 0.80), 0.15, 0.22, M['steel'], verts=48)
    pipe('gdrop', (0, 0, 0.72), (0, 0, 0.60), 0.085, M['steel'])
    nz = make_emm_open((0, 0, 0.62), 0.0014, 'det', detail=True, face=FACE)
    KEY['cn_orif'] = [[p_, tuple(Vector(p_) + Vector(d_) * 1.0)] for p_, d_ in nz['orifices']]
    KEY['cn_head'] = nz['head']; KEY['cn_tip'] = nz['tip']
    ph = math.radians(FACE - 30)
    KEY['cn_ins'] = (math.cos(ph) * 216 * 0.0014, math.sin(ph) * 216 * 0.0014, 0.62 - (655 - 110) * 0.0014)
    KEY['cn_hex'] = (0.15, -0.2, 0.62 - 100 * 0.0014)
    L_ = bpy.data.lights.new('under', 'AREA'); L_.energy = 700; L_.size = 6
    lo = bpy.data.objects.new('under', L_); COL.objects.link(lo); lo.location = (2.5, -3.5, -4.0)
    lo.rotation_euler = (Vector((0, 0, 0)) - lo.location).to_track_quat('-Z', 'Y').to_euler()


def build_cyl_battery():
    slab(0, 0, 6.0, 4.4)
    box('wall', (0, 1.9, 1.5), (5.4, 0.15, 3.0), M['wall'])
    box('capw', (0, 1.9, 3.01), (5.42, 0.17, 0.02), M['wallcap'])
    KEY['cyl'] = []
    for i in range(6):
        x = -1.9 + i * 0.62
        isn2 = i == 0
        cyl(f'c{i}', (x, 1.45, 0.85), 0.25, 1.5, M['red'], bevel=0.0)
        sph(f'ct{i}', (x, 1.45, 1.6), 0.25, M['red'], (1, 1, 0.55))
        if isn2:
            sph(f'n2{i}', (x, 1.45, 1.64), 0.252, M['green'], (1, 1, 0.48))
        cyl(f'v{i}', (x, 1.45, 1.82), 0.06, 0.16, M['brass'])
        cyl(f'vh{i}', (x, 1.45, 1.93), 0.08, 0.06, M['steel'])
        pipe(f'hose{i}', (x, 1.45, 1.96), (x, 1.62, 2.25), 0.025, M['black'])
        box(f'strap{i}', (x, 1.45, 1.2), (0.52, 0.52, 0.05), M['steel_d'])
        KEY['cyl'].append((x, 1.45, 1.0))
    pipe('mani', (-2.2, 1.62, 2.25), (1.4, 1.62, 2.25), 0.05, M['red'])
    pipe('out', (1.4, 1.62, 2.25), (2.3, 1.62, 2.25), 0.05, M['red'])
    pipe('out2', (2.3, 1.62, 2.25), (2.3, 1.62, 2.9), 0.05, M['red'])
    box('panel', (2.2, 1.75, 1.2), (0.6, 0.2, 0.8), M['redcab'], bevel=0.01)
    KEY['n2'] = (-1.9, 1.45, 1.64)
    KEY['label'] = (0.0, 1.45, 2.0)


def build_pump():
    slab(0, 0, 6.4, 4.8)
    box('skid', (0, -0.2, 0.08), (4.4, 2.2, 0.16), M['motor'])
    for x in (-2.15, 2.15):
        for y in (-1.25, 0.85):
            box(f'post{x}{y}', (x, y, 0.95), (0.06, 0.06, 1.6), M['motor'])
    box('ftb', (0, 0.85, 1.75), (4.36, 0.06, 0.06), M['motor'])
    box('fsl', (-2.15, -0.2, 1.75), (0.06, 2.16, 0.06), M['motor'])
    for i, x in enumerate((-1.25, 0.55)):
        cyl(f'mot{i}', (x, -0.35, 0.62), 0.36, 1.0, M['motor'], rot=(0, math.pi / 2, 0))
        for f in range(5):
            cyl(f'fin{i}{f}', (x - 0.4 + f * 0.2, -0.35, 0.62), 0.375, 0.03, M['steel_d'], rot=(0, math.pi / 2, 0))
        cyl(f'fan{i}', (x - 0.55, -0.35, 0.62), 0.33, 0.12, M['motor'], rot=(0, math.pi / 2, 0))
        box(f'tb{i}', (x, -0.35, 1.03), (0.3, 0.3, 0.12), M['motor'])
        box(f'pump{i}', (x + 0.78, -0.35, 0.55), (0.42, 0.5, 0.36), M['steel'], bevel=0.02)
        pipe(f'disc{i}', (x + 0.78, -0.35, 0.73), (x + 0.78, -0.95, 1.35), 0.045, M['steel'])
    pipe('mani', (-2.0, -0.95, 1.35), (1.9, -0.95, 1.35), 0.08, M['steel'])
    for x in (-1.6, -0.6, 1.0):
        cyl(f'g{x}', (x, -1.05, 1.5), 0.09, 0.05, M['crac'], rot=(math.pi / 2, 0, 0))
    box('relief', (1.6, -0.95, 1.55), (0.14, 0.14, 0.3), M['brass'])
    box('cab', (1.2, 1.55, 1.45), (1.6, 0.6, 2.6), M['redcab'], bevel=0.01)
    box('cabp', (1.2, 1.24, 1.75), (0.8, 0.02, 0.9), M['panel_blue'])
    cyl('tank', (-1.9, 1.6, 0.95), 0.55, 1.8, M['tank'], bevel=0.02)
    sph('tanktop', (-1.9, 1.6, 1.85), 0.55, M['tank'], (1, 1, 0.3))
    pipe('suct', (-1.9, 0.9, 0.35), (-1.2, 0.2, 0.35), 0.06, M['steel'])
    KEY['pump'] = (1.33, -0.35, 0.55); KEY['cab'] = (1.2, 1.24, 1.75); KEY['tank'] = (-1.9, 1.0, 1.3)
    KEY['mani'] = (-0.2, -0.95, 1.35); KEY['motor'] = (-1.25, -0.73, 0.62)


def build_nozzle():
    # boquilla colgante (bulbo hacia abajo), escala real ×10
    S_ = 1.0
    cyl('pipe', (0, 0, 1.6), 0.28, 1.4, M['steel_d'], rot=(0, math.pi / 2, 0))
    cyl('tee', (0, 0, 1.25), 0.2, 0.5, M['steel_d'])
    cyl('nut', (0, 0, 0.95), 0.32, 0.25, M['steel'], verts=6, bevel=0.02)
    cyl('thr', (0, 0, 0.72), 0.22, 0.25, M['steel'])
    for i in range(6):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.018, location=(0, 0, 0.62 + i * 0.04))
        bpy.context.object.data.materials.append(M['steel'])
    cyl('body', (0, 0, 0.45), 0.42, 0.3, M['steel'], bevel=0.03)
    dome = sph('dome', (0, 0, 0.3), 0.55, M['steel'], (1, 1, 0.75))
    bm = bmesh.new(); bm.from_mesh(dome.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > 0.02], context='VERTS')
    bm.to_mesh(dome.data); bm.free()
    KEY['micro'] = []
    for ring, (elev, n) in enumerate([(math.radians(-30), 6), (math.radians(-62), 3)]):
        for k in range(n):
            az = 2 * math.pi * k / n + ring * 0.5
            dvec = Vector((math.cos(elev) * math.cos(az), math.cos(elev) * math.sin(az), math.sin(elev)))
            p = Vector((0, 0, 0.3)) + Vector((dvec.x * 0.55, dvec.y * 0.55, dvec.z * 0.41))
            o = cyl(f'mn{ring}{k}', p, 0.12, 0.08, M['steel'], bevel=0.01)
            o.rotation_euler = dvec.to_track_quat('Z', 'Y').to_euler()
            o2 = cyl(f'mh{ring}{k}', p + dvec * 0.045, 0.012, 0.01, M['black'])
            o2.rotation_euler = o.rotation_euler
            KEY['micro'].append((tuple(p + dvec * 0.05), tuple(dvec)))
    # marco y ampolla
    for sx in (-1, 1):
        box(f'arm{sx}', (sx * 0.1, 0, -0.32), (0.05, 0.08, 0.5), M['steel'])
    box('bridge', (0, 0, -0.58), (0.25, 0.08, 0.05), M['steel'])
    if SHOT != 'nozzle_b':
        sph('bulb', (0, 0, -0.32), 0.05, M['glass'], (1, 1, 4.6))
        sph('liq', (0, 0, -0.32), 0.04, M['bulb_liq'], (1, 1, 4.4))
    KEY['bulb'] = (0, 0, -0.32)
    KEY['orifice'] = (0, 0, -0.08)


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


# ---------------- construir según plano ----------------
W_, H_ = 1080, 1350
if SHOT in ('wide', 'med', 'floor', 'floor_det', 'floor_det_b', 'site', 'proom2', 'site3', 'gen'):
    build_hall()
    if SHOT == 'site':
        cam = camera_iso((8.6, 0.3, 0.8), 36.5)
    elif SHOT == 'proom2':
        cam = camera_iso((12.6, 1.4, 1.0), 12.8)
    elif SHOT == 'site3':
        cam = camera_iso((9.4, 0.3, 0.8), 37.5)
    elif SHOT == 'gen':
        cam = camera_iso((19.0, 1.9, 1.3), 13.0)
    elif SHOT == 'wide':
        cam = camera_iso((0.0, 0.0, 0.6), 23.5)
    elif SHOT == 'med':
        cam = camera_iso((-2.2, -2.9, 2.0), 7.2)
    elif SHOT == 'floor':
        cam = camera_iso((1.2, -3.2, 0.9), 9.5)
    else:
        cam = camera_iso((1.66, -4.1, 0.2), 0.78)
elif SHOT in ('proom', 'proom_det'):
    build_pumproom()
    cam = camera_iso((0.6, 0.2, 0.9), 12.8) if SHOT == 'proom' else camera_iso((2.8, -0.2, 0.85), 3.9)
elif SHOT == 'cyl':
    build_cyl_battery(); cam = camera_iso((0.1, 0.4, 1.0), 8.6)
elif SHOT == 'pump':
    build_pump(); cam = camera_iso((-0.2, 0.2, 0.8), 8.8)
elif SHOT == 'gnoz':
    build_gen_nozzle_detail()
    cam = camera_persp((1.75, -2.75, -0.95), (0, 0, -0.02), lens=55)
elif SHOT == 'emm':
    make_emm_open((0, 0, 0.0), 0.001, 'emm', detail=True, face=-90)
    cam = camera_persp((0, -2.4, -0.18), (0, 0, -0.39), lens=85)
elif SHOT in ('ceil_a', 'ceil_b'):
    build_ceiling_detail(SHOT == 'ceil_b')
    cam = camera_persp((1.9, -2.55, -1.15), (0, 0, -0.18), lens=60)
elif SHOT in ('nozzle_a', 'nozzle_b'):
    build_nozzle(); cam = camera_persp((3.4, -5.0, -0.35), (0, 0, 0.18), lens=75)
lights()
if SHOT in ('__off__',):
    # tiras luminosas (softbox) para reflejos en el acero pulido
    em = bpy.data.materials.new('softbox'); em.use_nodes = True
    nt_ = em.node_tree; nt_.nodes.remove(nt_.nodes['Principled BSDF'])
    e_ = nt_.nodes.new('ShaderNodeEmission'); e_.inputs['Strength'].default_value = 5.0
    nt_.links.new(e_.outputs['Emission'], nt_.nodes['Material Output'].inputs['Surface'])
    tgt = Vector(KEY.get('cn_head', (0, 0, -0.39)))
    camv = sc.camera.location
    for side in (-1, 1):
        d_ = (camv - tgt).normalized()
        sd = d_.cross(Vector((0, 0, 1))).normalized() * side
        dist = (camv - tgt).length
        pos = tgt + sd * dist * (0.45 if side > 0 else 0.8) + d_ * dist * 1.3 + Vector((0, 0, 0.15 * dist))
        bpy.ops.mesh.primitive_plane_add(size=1, location=pos)
        pl = bpy.context.object; pl.scale = (0.12 * dist, 1.0 * dist, 1); pl.data.materials.append(em)
        pl.rotation_euler = (tgt - pos).to_track_quat('Z', 'Y').to_euler()
        pl.visible_camera = False
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.18 if SHOT == 'emm' else 0.25
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.render.film_transparent = True
sc.render.resolution_x = int(W_ * RS); sc.render.resolution_y = int(H_ * RS)
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast'
tag = SHOT + (f'_led{int(LED_SEED)}' if LED_SEED else '')
sc.render.filepath = f'{OUT}/{tag}.png'
bpy.ops.render.render(write_still=True)


# exportar coordenadas 2D (en píxeles del fotograma renderizado)
def proj(p):
    v = world_to_camera_view(sc, cam, Vector(p))
    return [v.x * sc.render.resolution_x, (1 - v.y) * sc.render.resolution_y]


out = {}
for k, v in KEY.items():
    if k == 'micro':
        out[k] = [[proj(p), proj(Vector(p) + Vector(dv) * 0.5)] for p, dv in v]
    elif k in ('orif', 'cn_orif'):
        out[k] = [[proj(a), proj(b)] for a, b in v]
    elif isinstance(v, list):
        out[k] = [proj(p) for p in v]
    else:
        out[k] = proj(v)
out['res'] = [sc.render.resolution_x, sc.render.resolution_y]
json.dump(out, open(f'{OUT}/{SHOT}.json', 'w'))
print('RENDERED', tag)
