"""Escenas Blender · CPD protegido con extinción por gas SIEX (INERT SIEX).
Uso: python3 siex_scene.py <out_dir> <shot> [samples] [scale] [led_seed]
Planos: gwide gmed gfloor gdoor gnoz groom"""
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'siex_base.py')).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'label_wrap.py')).read())
LABEL_SIEX = KW + 'assets/siex/label_siex.png'
from mathutils import Matrix
import os as _os
KW = _os.environ.get('KOMTES_WORK', _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'trabajo'))) + '/'

M['gal'] = mat('gal', (0.50, 0.52, 0.54), 0.38, 1.0)          # tubería de acero galvanizado
M['brushed'] = mat('brushed', (0.80, 0.80, 0.81), 0.26, 1.0)
M['det'] = mat('det', (0.93, 0.93, 0.92), 0.4)
M['led'] = mat('led', (0.9, 0.05, 0.03), 0.3, 0, (1.0, 0.05, 0.02), 4.0)
M['cyl_red'] = mat('cyl_red', (0.50, 0.03, 0.025), 0.28)
M['cyl_green'] = mat('cyl_green', (0.06, 0.48, 0.12), 0.3)
M['hose'] = mat('hose', (0.02, 0.02, 0.022), 0.55)
M['yellow'] = mat('yellow', (0.85, 0.62, 0.03), 0.4)
M['blue'] = mat('blue', (0.05, 0.20, 0.65), 0.4)
M['sign'] = mat('sign', (0.92, 0.92, 0.90), 0.4)
M['white'] = mat('white', (0.90, 0.90, 0.89), 0.45)
M['epoxy'] = mat('epoxy', (0.70, 0.72, 0.73), 0.55)


def mesh_mat():
    m = bpy.data.materials.new('mesh'); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord')
    br = N.new('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = 14; br.offset = 0.0
    br.inputs['Color1'].default_value = (0.03, 0.03, 0.035, 1); br.inputs['Color2'].default_value = (0.03, 0.03, 0.035, 1)
    br.inputs['Mortar'].default_value = (0.62, 0.63, 0.65, 1); br.inputs['Mortar Size'].default_value = 0.11
    br.inputs['Brick Width'].default_value = 0.5; br.inputs['Row Height'].default_value = 0.5
    Lk.new(tc.outputs['Generated'], br.inputs['Vector']); Lk.new(br.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Metallic'].default_value = 0.0; b.inputs['Roughness'].default_value = 0.6
    return m


M['mesh'] = mesh_mat()
KEY = {}


def parent_to(objs, emp):
    for o in objs:
        o.parent = emp


def make_silent(base, k, name, yaw=0.0, holes=True):
    """Difusor silencioso SIEX: cuerpo tubular horizontal con toma roscada superior, grupos de orificios
    en ambos extremos y malla en las bocas. Eje local X, toma en +Z. Devuelve puntos clave en mundo."""
    emp = bpy.data.objects.new(name, None); COL.objects.link(emp)
    emp.location = base; emp.rotation_euler = (0, 0, yaw); emp.scale = (k, k, k)
    objs = []
    L2, RO, RI = 0.95, 0.28, 0.235
    tube = lathe(name + '_tube', [(RI, L2), (RO, L2), (RO, -L2), (RI, -L2), (RI, L2)], M['brushed'], segs=72)
    tube.rotation_euler = (0, math.pi / 2, 0)
    objs.append(tube)
    pat = [(-0.06, 0.13), (0.07, 0.13), (0.0, 0.01), (-0.07, -0.11), (0.07, -0.11), (0.0, -0.21)]
    orif = []
    if holes:
        cutters = []
        for su in (-1, 1):
            for sy in (-1, 1):
                for (du, dv) in pat:
                    u = su * 0.70 + du
                    th = dv / RO
                    dvec = Vector((0, sy * math.cos(th), math.sin(th)))
                    p = Vector((u, 0, 0)) + dvec * RO
                    c = cyl(f'{name}_h', p, 0.034, 0.16, M['black'], verts=16)
                    c.rotation_euler = dvec.to_track_quat('Z', 'Y').to_euler()
                    cutters.append(c)
                    orif.append((p + dvec * 0.01, dvec))
        bpy.context.view_layer.update()
        # unir cortadores en un solo objeto para un único booleano
        for c in cutters:
            c.select_set(True)
        bpy.context.view_layer.objects.active = cutters[0]
        bpy.ops.object.join()
        cj = bpy.context.object; cj.hide_render = True; cj.hide_viewport = False
        bo = tube.modifiers.new('holes', 'BOOLEAN'); bo.operation = 'DIFFERENCE'; bo.object = cj; bo.solver = 'EXACT'
        objs.append(cj)
        cj.display_type = 'WIRE'
        bpy.context.view_layer.objects.active = tube
        for o_ in bpy.context.selected_objects:
            o_.select_set(False)
        tube.select_set(True)
        bpy.ops.object.modifier_apply(modifier='holes')
        try:
            bpy.ops.object.shade_smooth_by_angle(angle=math.radians(25))
        except Exception:
            pass
        tube.select_set(False)
    for su in (-1, 1):
        m_ = cyl(f'{name}_mesh', (su * (L2 - 0.07), 0, 0), RI + 0.002, 0.012, M['mesh'], rot=(0, math.pi / 2, 0), verts=48)
        objs.append(m_)
        bpy.ops.mesh.primitive_torus_add(major_radius=RI - 0.012, minor_radius=0.014, location=(su * (L2 - 0.075), 0, 0),
                                         rotation=(0, math.pi / 2, 0), major_segments=64, minor_segments=10)
        rim = bpy.context.object; rim.data.materials.append(M['steel_d']); objs.append(rim)
        for sz in (-1, 1):
            objs.append(sph(f'{name}_scr', (su * (L2 - 0.06), 0.0, sz * 0.19), 0.022, M['steel_d']))
        orif.append((Vector((su * L2, 0, 0)), Vector((su, 0, 0))))
    boss = cyl(name + '_boss', (0, 0, RO + 0.10), 0.13, 0.26, M['brushed'], verts=48, bevel=0.01)
    objs.append(boss)
    objs.append(cyl(name + '_bore', (0, 0, RO + 0.225), 0.085, 0.012, M['black'], verts=32))
    parent_to(objs, emp)
    R = Matrix.Rotation(yaw, 3, 'Z')
    W_ = lambda v: tuple(Vector(base) + R @ (Vector(v) * k))
    return {'center': tuple(base), 'top': W_((0, 0, RO + 0.23)),
            'orif': [(W_(p), tuple(R @ d)) for p, d in orif],
            'ends': [W_((L2, 0, 0)), W_((-L2, 0, 0))]}


def detector(x, y, z, top=3.95, name='det'):
    pipe(name + 'rod', (x, y, top), (x, y, z + 0.04), 0.006, M['steel_d'])
    cyl(name + 'b', (x, y, z + 0.02), 0.075, 0.03, M['det'], verts=32, bevel=0.005)
    sph(name + 'd', (x, y, z), 0.062, M['det'], (1, 1, 0.55))
    sph(name + 'l', (x + 0.045, y - 0.045, z - 0.008), 0.009, M['led'])
    return (x, y, z - 0.03)


def hanger(x, y, z, top=3.95):
    pipe('hg', (x, y, top), (x, y, z), 0.006, M['steel_d'])


def slab(cx, cy, sx, sy, h=0.55):
    box('slab', (cx, cy, -h / 2), (sx, sy, h), M['slab'], bevel=0.12)


def build_hall():
    if SHOT in ('gsite', 'gcyl'):
        slab(4.1, 0, 22.6, 11.2)          # losa única CPD + sala de cilindros
    else:
        slab(0, 0, 14.4, 11.2)
    X0, X1, Y0, Y1 = -6.6, 6.6, -5.0, 5.0
    T = 0.6; FH = 0.42
    cut = SHOT in ('gfloor',)
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
            if x > X1 or y > Y1 or (ix, iy) in hidden:
                continue
            perf = (abs(y + 1.25) < 0.6 or abs(y - 1.75) < 0.6) and -4.6 < x < 1.6 and ix % 2 == 0
            box(f't{ix}_{iy}', (x, y, FH - 0.02), (T - 0.012, T - 0.012, 0.04), M['tile_perf' if perf else 'tile'])
    if cut:
        for (ix, iy) in hidden:
            x = X0 + (ix + 0.5) * T; y = Y0 + (iy + 0.5) * T
            cyl('ped', (x - T / 2 + 0.02, y - T / 2 + 0.02, FH / 2), 0.025, FH, M['ped'], verts=10)
        for k, (yy, mt) in enumerate([(-4.3, 'cable_b'), (-3.85, 'cable_y')]):
            box(f'uftray{k}', (1.6, yy, 0.035), (6.0, 0.36, 0.03), M['tray'])
            for j in range(6):
                pipe(f'ufc{k}{j}', (-1.4, yy - 0.12 + j * 0.05, 0.075 + (j % 2) * 0.03), (4.6, yy - 0.12 + j * 0.05, 0.075 + (j % 2) * 0.03), 0.026, M[mt])
        # red de gas bajo suelo técnico, por encima de los cables
        UFZ = FH - 0.09
        pipe('ufmain', (-1.4, -4.08, UFZ), (4.6, -4.08, UFZ), 0.028, M['gal'])
        KEY['uf_noz'] = []
        for k, x in enumerate((0.5, 2.9)):
            nz = make_silent((x, -4.08, UFZ - 0.11), 0.17, f'ufnz{k}', yaw=math.pi / 2)
            pipe(f'ufdr{k}', (x, -4.08, UFZ), nz['top'], 0.018, M['gal'])
            KEY['uf_noz'].append(nz['center'])
            KEY[f'uf_ends{k}'] = nz['ends']
    WH = 3.4
    box('wallL', (X0 - 0.1, 0, WH / 2), (0.2, Y1 - Y0 + 0.2, WH), M['wall'])
    box('wallB', (0, Y1 + 0.1, WH / 2), (X1 - X0 + 0.4, 0.2, WH), M['wall'])
    box('capL', (X0 - 0.1, 0, WH + 0.01), (0.22, Y1 - Y0 + 0.22, 0.02), M['wallcap'])
    box('capB', (0, Y1 + 0.1, WH + 0.013), (X1 - X0 + 0.42, 0.22, 0.02), M['wallcap'])
    # acceso a sala: puerta, central de extinción, pulsadores, rótulo y sirena-flash
    DX = 4.3
    box('door', (DX, Y1 - 0.0, FH + 1.1), (1.2, 0.06, 2.2), M['door_glass'])
    box('doorf', (DX, Y1 + 0.02, FH + 1.12), (1.32, 0.05, 2.3), M['steel_d'])
    box('panel', (2.55, Y1 - 0.09, FH + 1.15), (0.62, 0.14, 0.82), M['white'], bevel=0.01)
    box('panelst', (2.55, Y1 - 0.165, FH + 1.5), (0.62, 0.012, 0.08), M['red'])
    box('panelscr', (2.55, Y1 - 0.165, FH + 1.2), (0.36, 0.01, 0.22), M['panel_blue'])
    box('pulsY', (3.35, Y1 - 0.06, FH + 1.05), (0.16, 0.08, 0.16), M['yellow'], bevel=0.01)
    box('pulsB', (3.35, Y1 - 0.06, FH + 0.8), (0.16, 0.08, 0.16), M['blue'], bevel=0.01)
    box('sign', (DX, Y1 - 0.07, FH + 2.55), (1.1, 0.1, 0.3), M['sign'], bevel=0.008)
    cyl('siren', (DX + 1.05, Y1 - 0.09, FH + 2.45), 0.11, 0.14, M['red'], rot=(math.pi / 2, 0, 0))
    sph('flash', (DX + 1.05, Y1 - 0.17, FH + 2.45), 0.085, mat('flashm', (0.9, 0.25, 0.2), 0.1, 0, None, 0, trans=0.3), (1, 0.6, 1))
    SZ = FH + 2.55; SY = Y1 - 0.125
    KEY['sign_q'] = [(DX - 0.53, SY, SZ + 0.13), (DX + 0.53, SY, SZ + 0.13), (DX + 0.53, SY, SZ - 0.13), (DX - 0.53, SY, SZ - 0.13)]
    KEY['scr_q'] = [(2.55 - 0.17, Y1 - 0.172, FH + 1.3), (2.55 + 0.17, Y1 - 0.172, FH + 1.3),
                    (2.55 + 0.17, Y1 - 0.172, FH + 1.1), (2.55 - 0.17, Y1 - 0.172, FH + 1.1)]
    KEY['flash'] = (DX + 1.05, Y1 - 0.2, FH + 2.45)
    KEY['panel'] = (2.55, Y1 - 0.16, FH + 1.35)
    KEY['puls'] = (3.35, Y1 - 0.1, FH + 0.95)
    KEY['door'] = (DX, Y1 - 0.05, FH + 1.0)
    # racks
    RW, RD, RH = 0.6, 1.1, 2.25
    rows = [-2.4, 0.6, 3.6]
    KEY['racks'] = []
    for r_i, yc in enumerate(rows):
        for k in range(10):
            x = -4.3 + k * RW
            box(f'rack{r_i}_{k}', (x, yc, FH + RH / 2), (RW - 0.02, RD, RH), M['rack'], bevel=0.008)
            box(f'door{r_i}_{k}', (x, yc - RD / 2 - 0.006, FH + RH / 2), (RW - 0.06, 0.01, RH - 0.08), DOOR)
            KEY['racks'].append((x, yc - RD / 2, FH + RH))
        box(f'tray{r_i}', (-4.3 + 4.5 * RW, yc, FH + RH + 0.45), (10 * RW + 0.2, 0.45, 0.06), M['tray'])
        for j in range(5):
            pipe(f'cab{r_i}{j}', (-4.6, yc - 0.15 + j * 0.07, FH + RH + 0.5), (1.6, yc - 0.15 + j * 0.07, FH + RH + 0.5), 0.025,
                 M['cable_y' if j % 2 else 'cable_g'])
    for j, yy in enumerate((-2.6, 1.2)):
        box(f'crac{j}', (-5.95, yy, FH + 1.0), (0.9, 2.2, 2.0), M['crac'], bevel=0.02)
        box(f'grl{j}', (-5.49, yy, FH + 1.45), (0.02, 1.9, 0.7), M['grille'])
    for j in range(3):
        box(f'ups{j}', (3.3 + j * 0.75, 0.9, FH + 1.0), (0.7, 0.8, 2.0), M['crac'], bevel=0.01)
        box(f'upsp{j}', (3.3 + j * 0.75, 0.49, FH + 1.4), (0.4, 0.02, 0.3), M['grille'])
    KEY['crac_out'] = (-5.45, -2.6, FH + 1.45)
    # red de gas (acero galvanizado) con difusores silenciosos
    PZ = FH + RH + 0.95
    TOP = 3.95
    pipe('gmain', (X0 + 0.25, -3.6, PZ), (X0 + 0.25, 2.1, PZ), 0.055, M['gal'])
    MX = X1 - 0.3          # colector de la sala, alimentado desde la sala de cilindros
    pipe('gmainR', (MX, -3.6, PZ), (MX, Y1 - 0.22, PZ), 0.06, M['gal'])
    for y in (-3.0, 0.0, 3.0):
        hanger(MX, y, PZ + 0.06, TOP)
    for y in (-3.0, 0.0, 3.0):
        hanger(X0 + 0.25, y, PZ + 0.055, TOP)
    KEY['nozzles'] = []
    KEY['noz_ends'] = []
    for yy in (-3.6, -0.9, 2.1):
        pipe(f'br{yy}', (X0 + 0.25, yy, PZ), (MX, yy, PZ), 0.04, M['gal'])
        for hx in (-3.0, 0.0, 3.0):
            hanger(hx, yy, PZ + 0.04, TOP)
        for k, x in enumerate((-3.7, -1.3, 1.1, 3.5, 5.6)):
            nz = make_silent((x, yy, PZ - 0.26), 0.2, f'nz{yy}{k}', yaw=math.pi / 2)
            pipe(f'dr{yy}{k}', (x, yy, PZ), nz['top'], 0.025, M['gal'])
            KEY['nozzles'].append(nz['center'])
            KEY['noz_ends'].append(nz['ends'])
    # detección: detectores puntuales en la losa
    KEY['gp_main'] = [(MX, Y1 - 0.22, PZ), (MX, -3.6, PZ)]
    KEY['gp_br'] = [(MX, yy, PZ) for yy in (-3.6, -0.9, 2.1)] + [(X0 + 0.25, yy, PZ) for yy in (-3.6, -0.9, 2.1)]
    KEY['det'] = []
    for yy in (-3.05, -0.3, 2.75):
        for x in (-3.4, -0.4, 2.3):
            KEY['det'].append(detector(x, yy, PZ + 0.12, TOP, f'det{x}{yy}'))
    KEY['fire'] = (-4.3 + 4 * RW, -2.4 - RD / 2 - 0.05, FH + 1.3)
    KEY['fire_top'] = (-4.3 + 4 * RW, -2.4, FH + RH)
    KEY['fire_nozzle'] = (-1.3, -3.6, PZ - 0.26)
    KEY['det_fire'] = [(-3.4, -3.05, PZ + 0.09), (-0.4, -3.05, PZ + 0.09)]
    KEY['inlet'] = (X0 + 0.25, -4.2, PZ)
    # caja del recinto (para la inundación total)
    KEY['room'] = [(X0, Y0, z) for z in (0.0,)] + [(X1, Y0, 0.0), (X1, Y1, 0.0), (X0, Y1, 0.0)]
    KEY['room_top'] = [(X0, Y0, 3.4), (X1, Y0, 3.4), (X1, Y1, 3.4), (X0, Y1, 3.4)]
    KEY['room_ff'] = [(X0, Y0, FH), (X1, Y0, FH), (X1, Y1, FH), (X0, Y1, FH)]
    if SHOT in ('gsite', 'gcyl'):
        build_cylroom(X0, X1, Y0, Y1, PZ)


def build_nozzle_detail():
    """plano detalle: difusor silencioso bajo el falso techo"""
    c = box('ceil', (0, 0.6, 0.98), (5.0, 4.4, 0.12), M['crac'], bevel=0.01)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, -0.4, 0.98))
    cc = bpy.context.object; cc.scale = (5.4, 1.6, 0.4); cc.hide_render = True; cc.hide_viewport = True
    bo = c.modifiers.new('cut', 'BOOLEAN'); bo.operation = 'DIFFERENCE'; bo.object = cc
    nz = make_silent((0, 0, 0.0), 1.0, 'det', yaw=0.0)
    pipe('pdrop', nz['top'], (0, 0, 1.6), 0.11, M['gal'])
    pipe('pmain', (-3.0, 0, 1.6), (3.0, 0, 1.6), 0.2, M['gal'])
    L = bpy.data.lights.new('under', 'AREA'); L.energy = 700; L.size = 6
    lo = bpy.data.objects.new('under', L); COL.objects.link(lo); lo.location = (2.0, -4.0, -3.0)
    lo.rotation_euler = (Vector((0, 0, 0)) - lo.location).to_track_quat('-Z', 'Y').to_euler()
    KEY['orif'] = [[p, (Vector(p) + Vector(d) * 1.0)[:]] for p, d in nz['orif']]
    KEY['center'] = nz['center']; KEY['ends'] = nz['ends']
    KEY['mesh_end'] = nz['ends'][0]
    KEY['holes'] = nz['orif'][13][0]


def cylinder(x, y, name, r=0.19, h=1.55):
    cyl(name + 'b', (x, y, 0.05 + h / 2), r, h, M['cyl_red'], verts=40)
    sph(name + 't', (x, y, 0.05 + h), r, M['cyl_green'], (1, 1, 0.9))
    sph(name + 'f', (x, y, 0.05), r, M['cyl_red'], (1, 1, 0.3))
    label_shell(name + 'lab', x, y, r + 0.003, 0.05 + h * 0.36, 0.05 + h * 0.36 + 0.675 * (r / 0.172), LABEL_SIEX, face=-48, arc=150)
    top = 0.05 + h + r * 0.9
    cyl(name + 'v', (x, y, top + 0.06), 0.05, 0.14, M['brass'])
    cyl(name + 'vh', (x, y, top + 0.15), 0.07, 0.06, M['brass'], verts=6)
    cyl(name + 'g', (x + 0.07, y - 0.02, top + 0.09), 0.03, 0.02, M['white'], rot=(0, math.pi / 2, 0))
    return (x, y, top + 0.18)


def hose(a, b, name, r=0.022):
    a, b = Vector(a), Vector(b)
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 4
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(1)
    p0, p1 = sp.bezier_points
    p0.co = a; p0.handle_left = a - Vector((0, 0, 0.2)); p0.handle_right = a + Vector((0, 0, 0.35))
    p1.co = b; p1.handle_left = b - Vector((0, -0.25, 0.05)) + Vector((0, 0, 0)); p1.handle_right = b + Vector((0, 0.1, 0))
    o = bpy.data.objects.new(name, cu); COL.objects.link(o); o.data.materials.append(M['hose'])
    return o


def bank(x0, name, n=6):
    tops = []
    for row, y in enumerate((3.1, 2.62)):
        for i in range(n):
            x = x0 + i * 0.44 + row * 0.22
            tops.append(cylinder(x, y, f'{name}{row}{i}'))
    MZ, MY = 2.42, 3.38
    xa, xb = x0 - 0.15, x0 + (n - 1) * 0.44 + 0.37
    pipe(name + 'man', (xa, MY, MZ), (xb, MY, MZ), 0.06, M['red'])
    for x in (xa + 0.1, xb - 0.1):
        box(name + 'brk', (x, MY + 0.12, MZ), (0.06, 0.2, 0.06), M['steel_d'])
    for j, tp in enumerate(tops):
        hose(tp, (tp[0], MY - 0.05, MZ - 0.02), f'{name}h{j}')
        for s in (-1, 1):
            box(name + 'str', (tp[0], tp[1], 1.0 + s * 0.45), (0.42, 0.42, 0.04), M['steel_d']) if j < 0 else None
    for y in (3.1, 2.62):
        for zz in (0.7, 1.35):
            box(name + 'bar', ((xa + xb) / 2, y - 0.2, zz), (xb - xa, 0.03, 0.05), M['steel_d'])
    box(name + 'ps', (xb - 0.05, MY - 0.02, MZ + 0.12), (0.1, 0.08, 0.12), M['blue'])
    return {'man': ((xa + xb) / 2, MY, MZ), 'end': (xb, MY, MZ), 'start': (xa, MY, MZ), 'ps': (xb - 0.05, MY - 0.06, MZ + 0.12),
            'mid': ((xa + xb) / 2, 2.6, 1.1)}


def build_gasroom():
    slab(0, 0, 10.6, 8.6)
    X0, X1, Y0, Y1 = -4.9, 4.9, -3.9, 3.9
    WH = 3.6
    box('floor', (0, 0, 0.01), (X1 - X0, Y1 - Y0, 0.02), M['epoxy'])
    box('wallL', (X0 - 0.1, 0, WH / 2), (0.2, Y1 - Y0 + 0.2, WH), M['wall'])
    box('wallB', (0, Y1 + 0.1, WH / 2), (X1 - X0 + 0.4, 0.2, WH), M['wall'])
    box('capL', (X0 - 0.1, 0, WH + 0.01), (0.22, Y1 - Y0 + 0.22, 0.02), M['wallcap'])
    box('capB', (0, Y1 + 0.1, WH + 0.013), (X1 - X0 + 0.42, 0.22, 0.02), M['wallcap'])
    main = bank(-4.2, 'A')
    resv = bank(0.6, 'R')
    # unión de colectores con válvulas antirretorno y colector común
    HZ, HY = 2.42, 1.55
    xj = (main['end'][0] + resv['start'][0]) / 2
    pipe('bridge', (main['end'][0], 3.38, HZ), (resv['start'][0], 3.38, HZ), 0.06, M['red'])
    for x in (main['end'][0] + 0.12, resv['start'][0] - 0.12):
        cyl('chk', (x, 3.38, HZ), 0.085, 0.16, M['brass'], rot=(0, math.pi / 2, 0))
    # válvulas direccionales: colector común entre ambas baterías
    HY = 2.4
    pipe('hdr', (xj, 3.38, HZ), (xj, 1.75, HZ), 0.07, M['red'])
    KEY['dirv'] = []; KEY['outs'] = []
    for j, yv in enumerate((2.95, 2.4, 1.85)):
        cyl(f'dv{j}', (xj, yv, HZ + 0.2), 0.14, 0.3, M['red'], verts=32, bevel=0.015)
        cyl(f'dva{j}', (xj + 0.22, yv, HZ + 0.24), 0.09, 0.28, M['motor'], rot=(0, math.pi / 2, 0))
        box(f'dvs{j}', (xj + 0.4, yv, HZ + 0.24), (0.08, 0.16, 0.16), M['red'])
        pipe(f'dvo{j}', (xj, yv, HZ + 0.34), (xj, yv, WH + 0.3), 0.075, M['gal'])
        cyl(f'fl{j}', (xj, yv, HZ + 0.7), 0.1, 0.03, M['steel_d'])
        KEY['dirv'].append((xj + 0.1, yv, HZ + 0.2))
        KEY['outs'].append((xj, yv, WH + 0.25))
    for y in (3.2, 1.8):
        pipe('hdrs', (xj, y, 0.0), (xj, y, HZ - 0.07), 0.03, M['steel_d'])
    # disparo: cilindro piloto con actuador electromagnético junto al banco principal
    px, py = -4.55, 2.2
    cyl('pilot', (px, py, 0.55), 0.07, 0.9, M['cyl_red'])
    sph('pilott', (px, py, 1.0), 0.07, M['cyl_green'], (1, 1, 0.8))
    cyl('pilotv', (px, py, 1.12), 0.04, 0.12, M['brass'])
    box('sol', (px, py, 1.25), (0.1, 0.1, 0.12), M['red'])
    hose((px, py, 1.3), (main['start'][0] + 0.15, 2.62, 1.98), 'pilh', 0.012)
    # central de extinción en el muro izquierdo
    box('cpanel', (X0 + 0.08, 0.9, 1.5), (0.14, 0.8, 0.95), M['white'], bevel=0.01)
    box('cpst', (X0 + 0.16, 0.9, 1.88), (0.012, 0.8, 0.08), M['red'])
    box('cpscr', (X0 + 0.16, 0.9, 1.55), (0.01, 0.42, 0.25), M['panel_blue'])
    for zz in (1.2, 1.9, 2.6):
        pipe('cable', (X0 + 0.02, -0.2, zz * 0 + 2.0), (X0 + 0.02, 2.2, 2.0), 0.012, M['green']) if zz == 1.2 else None
    KEY['main_bank'] = main['mid']; KEY['res_bank'] = resv['mid']
    KEY['main_man'] = main['man']; KEY['res_man'] = resv['man']
    KEY['ps'] = main['ps']; KEY['pilot'] = (px, py, 1.25); KEY['cpanel'] = (X0 + 0.16, 0.9, 1.55)
    KEY['hdr'] = (xj, HY, HZ)



M['copper'] = mat('copper', (0.72, 0.36, 0.20), 0.3, 1.0)
M['cyan'] = mat('cyan', (0.35, 0.75, 0.72), 0.45)
M['valve_grey'] = mat('valve_grey', (0.42, 0.43, 0.45), 0.45, 0.3)
M['silver'] = mat('silver', (0.75, 0.75, 0.76), 0.25, 1.0)


def wall_cyl(x, y, name, r=0.17, h=1.55):
    """cilindro de pie, anclado a la pared con abrazaderas (pared en +y)"""
    cyl(name + 'b', (x, y, 0.08 + h / 2), r, h, M['cyl_red'], verts=40)
    sph(name + 't', (x, y, 0.08 + h), r, M['cyl_green'], (1, 1, 0.95))
    sph(name + 'f', (x, y, 0.08), r, M['cyl_red'], (1, 1, 0.3))
    top = 0.08 + h + r * 0.95
    cyl(name + 'fl', (x, y, top + 0.01), 0.07, 0.02, M['silver'])
    cyl(name + 'v', (x, y, top + 0.07), 0.045, 0.11, M['brass'])
    box(name + 'vb', (x, y, top + 0.13), (0.16, 0.06, 0.06), M['brass'])
    for zz in (0.75, 1.3):
        bpy.ops.mesh.primitive_torus_add(major_radius=r + 0.006, minor_radius=0.012, location=(x, y, zz))
        bpy.context.object.data.materials.append(M['steel'])
    label_shell(name + 'lab', x, y, r + 0.003, 0.08 + h * 0.36, 0.08 + h * 0.36 + 0.675 * (r / 0.172), LABEL_SIEX, face=-48, arc=150)
    return (x, y, top + 0.16)


def dir_valve(x, y, zb, name):
    """válvula direccional sobre el montante: cuerpo gris, actuador con solenoide al frente, palanca manual y finales de carrera"""
    cyl(name + 'body', (x, y, zb), 0.12, 0.3, M['valve_grey'], verts=32, bevel=0.01)
    ay = y - 0.2
    cyl(name + 'col', (x, ay, zb + 0.1), 0.035, 0.5, M['motor'])
    cyl(name + 'brass', (x, ay, zb + 0.43), 0.055, 0.16, M['brass'])
    cyl(name + 'sol', (x, ay, zb + 0.58), 0.06, 0.16, M['silver'])
    cyl(name + 'cap', (x, ay, zb + 0.68), 0.035, 0.04, M['silver'])
    box(name + 'coil', (x - 0.07, ay, zb + 0.62), (0.05, 0.05, 0.08), M['motor'])
    box(name + 'lever', (x + 0.13, y - 0.08, zb - 0.02), (0.03, 0.02, 0.6), M['motor'])
    box(name + 'sw1', (x - 0.07, ay - 0.02, zb + 0.18), (0.05, 0.06, 0.13), M['cyan'])
    box(name + 'sw2', (x - 0.07, ay - 0.02, zb - 0.14), (0.05, 0.06, 0.13), M['cyan'])
    pipe(name + 'lnk', (x, ay, zb), (x, y - 0.1, zb), 0.03, M['motor'])
    return {'sol': (x, ay - 0.05, zb + 0.6), 'lever': (x + 0.13, y - 0.1, zb), 'body': (x, y - 0.12, zb)}


def build_cylroom(X0h, X1h, Y0h, Y1h, PZ):
    """sala de cilindros aledaña al CPD (lado +x): batería principal | válvulas direccionales | batería de reserva, todo en el muro"""
    RX0, RX1, RY0, RY1 = X1h + 0.2, X1h + 8.5, -1.2, Y1h
    WH = 3.4
    box('cfloor', ((RX0 + RX1) / 2, (RY0 + RY1) / 2, 0.01), (RX1 - RX0, RY1 - RY0, 0.02), M['epoxy'])
    box('cwallB', ((X1h + 0.2 + RX1 + 0.2) / 2, RY1 + 0.1, WH / 2), (RX1 - X1h, 0.2, WH), M['wall'])
    box('ccapB', ((X1h + 0.2 + RX1 + 0.2) / 2, RY1 + 0.1, WH + 0.013), (RX1 - X1h + 0.02, 0.22, 0.02), M['wallcap'])
    box('cwallM', (X1h + 0.1, (RY0 + RY1) / 2, 0.55), (0.2, RY1 - RY0, 1.1), M['wall'])
    box('ccapM', (X1h + 0.1, (RY0 + RY1) / 2, 1.11), (0.22, RY1 - RY0, 0.02), M['wallcap'])
    box('cskirt', (X1h + 0.02, (Y0h + RY0) / 2, 0.22), (0.06, RY0 - Y0h + 0.1, 0.44), M['wallcap'])
    WY = RY1 - 0.22
    MZ = 2.42
    banks = {}
    VX0 = RX0 + 3.55                       # zona central de válvulas direccionales
    for nm, x0 in (('A', RX0 + 0.75), ('R', VX0 + 2.05)):
        tops = [wall_cyl(x0 + i * 0.4, WY, f'{nm}c{i}') for i in range(6)]
        for zz in (0.75, 1.3):
            box(f'{nm}rail{zz}', (x0 + 1.0, RY1 - 0.04, zz), (2.4, 0.06, 0.05), M['steel_d'])
        cxm = x0 + 1.0
        box(f'{nm}man', (cxm, WY + 0.02, MZ), (0.9, 0.16, 0.12), M['red'], bevel=0.01)
        for dx in (-0.25, 0.25):
            box(f'{nm}brk', (cxm + dx, RY1 - 0.15, MZ + 0.25), (0.06, 0.3, 0.6), M['steel_d'])
        for j, tp in enumerate(tops):
            hose(tp, (cxm - 0.35 + j * 0.14, WY - 0.04, MZ - 0.06), f'{nm}h{j}')
        banks[nm] = {'man': (cxm, WY - 0.06, MZ), 'mid': (x0 + 1.0, WY - 0.2, 1.0), 'xa': cxm - 0.45, 'xb': cxm + 0.45, 'tops': tops}
    # colector de válvulas direccionales entre ambas baterías
    HZ = 0.62
    xs = [VX0 + 0.15 + j * 0.5 for j in range(4)]
    hx0, hx1 = xs[0] - 0.35, xs[-1] + 0.35
    pipe('chdr', (hx0, WY, HZ), (hx1, WY, HZ), 0.06, M['red'])
    for nm, xe, xh in (('A', banks['A']['xb'], hx0), ('R', banks['R']['xa'], hx1)):
        pipe(f'cfa{nm}', (xe, WY + 0.02, MZ), (xh, WY + 0.02, MZ), 0.05, M['red'])
        pipe(f'cfb{nm}', (xh, WY + 0.02, MZ), (xh, WY, HZ), 0.05, M['red'])
        cyl(f'cchk{nm}', (xh, WY + 0.01, 1.6), 0.07, 0.15, M['brass'])
    for x in (hx0 + 0.1, hx1 - 0.1):
        pipe('chs', (x, WY, 0.0), (x, WY, HZ - 0.06), 0.025, M['steel_d'])
    KEY['dirv'] = []; KEY['outs'] = []; KEY['levers'] = []; KEY['sols'] = []
    for j, x in enumerate(xs):
        top = PZ if j == 0 else WH + 0.35
        pipe(f'crs{j}', (x, WY, HZ), (x, WY, top), 0.05, M['red'])
        dv = dir_valve(x, WY, 1.3, f'dv{j}')
        KEY['dirv'].append(dv['body']); KEY['levers'].append(dv['lever']); KEY['sols'].append(dv['sol'])
        KEY['outs'].append((x, WY, top))
    # salida de la sala 1: cruza el muro medianero hacia el colector del CPD
    MX = X1h - 0.3
    pipe('cto1', (xs[0], WY, PZ), (MX, WY, PZ), 0.06, M['red'])
    sph('cel', (xs[0], WY, PZ), 0.065, M['red'])
    KEY['gp_feed'] = [(xs[0], WY, 1.3), (xs[0], WY, PZ), (MX, WY, PZ)]
    # cilindro piloto en el muro, a la derecha de la batería principal (como en el sistema real)
    px, py = RX0 + 3.15, WY - 0.05
    cyl('pilot', (px, py, 0.95), 0.075, 0.5, M['motor'])
    sph('pilott', (px, py, 1.2), 0.075, M['motor'], (1, 1, 0.6))
    cyl('pilotb', (px, py, 1.3), 0.04, 0.14, M['brass'])
    cyl('pilots', (px, py, 1.44), 0.045, 0.12, M['silver'])
    box('pilotc', (px - 0.07, py, 1.46), (0.05, 0.05, 0.07), M['motor'])
    box('pilotbr', (px, RY1 - 0.04, 1.0), (0.2, 0.08, 0.06), M['steel_d'])
    cz = 1.9
    pipe('cu0', (px, py, 1.5), (px, py, cz), 0.008, M['copper'])
    pipe('cu1', (px, WY - 0.3, cz), (banks['R']['tops'][-1][0], WY - 0.3, cz), 0.008, M['copper'])
    pipe('cu1b', (px, py, cz), (px, WY - 0.3, cz), 0.008, M['copper'])
    for tp in banks['A']['tops'] + banks['R']['tops']:
        pipe('cuv', (tp[0], WY - 0.3, cz), (tp[0], WY - 0.08, tp[2] - 0.03), 0.006, M['copper'])
    for x in xs:
        pipe('cuv2', (x, WY - 0.3, cz), (x, WY - 0.22, 1.95), 0.006, M['copper'])
    # central de extinción en el muro trasero (extremo derecho)
    box('ccp', (RX1 - 0.45, RY1 - 0.08, 1.5), (0.5, 0.14, 0.75), M['white'], bevel=0.01)
    box('ccps', (RX1 - 0.45, RY1 - 0.155, 1.82), (0.5, 0.012, 0.08), M['red'])
    KEY['main_bank'] = banks['A']['mid']; KEY['res_bank'] = banks['R']['mid']
    KEY['main_man'] = banks['A']['man']; KEY['res_man'] = banks['R']['man']
    KEY['pilot'] = (px, py, 1.4); KEY['cylroom'] = ((RX0 + RX1) / 2, (RY0 + RY1) / 2, 1.0)
    KEY['hdr'] = ((hx0 + hx1) / 2, WY, HZ)
    KEY['croom'] = [(RX0, RY0, 0.0), (RX1, RY0, 0.0), (RX1, RY1, 0.0), (RX0, RY1, 0.0)]

W_, H_ = 1080, 1350
if SHOT in ('gwide', 'gmed', 'gfloor', 'gdoor', 'gsite', 'gcyl'):
    build_hall()
    if SHOT == 'gsite':
        cam = camera_iso((4.4, 0.4, 0.8), 28.5)
    elif SHOT == 'gcyl':
        cam = camera_iso((11.0, 3.4, 1.6), 9.8)
    elif SHOT == 'gwide':
        cam = camera_iso((0.0, 0.0, 0.6), 23.5)
    elif SHOT == 'gmed':
        cam = camera_iso((-2.2, -2.9, 2.0), 7.2)
    elif SHOT == 'gfloor':
        cam = camera_iso((0.6, -2.6, 1.3), 11.5)
    else:
        cam = camera_iso((3.4, 4.4, 1.8), 5.4)
elif SHOT == 'gnoz':
    build_nozzle_detail()
    cam = camera_persp((2.6, -4.6, -1.0), (0, 0, 0.05), lens=62)
elif SHOT == 'groom':
    build_gasroom()
    cam = camera_iso((0.1, 2.2, 1.4), 9.2)
lights()
sc.render.engine = 'CYCLES'
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.render.film_transparent = True
sc.render.resolution_x = int(W_ * RS); sc.render.resolution_y = int(H_ * RS)
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast'
tag = SHOT + (f'_led{int(LED_SEED)}' if LED_SEED else '')
sc.render.filepath = f'{OUT}/{tag}.png'
bpy.ops.render.render(write_still=True)


def proj(p):
    v = world_to_camera_view(sc, cam, Vector(p))
    return [v.x * sc.render.resolution_x, (1 - v.y) * sc.render.resolution_y]


out = {}
for k, v in KEY.items():
    if k == 'orif':
        out[k] = [[proj(a), proj(b)] for a, b in v]
    elif k == 'noz_ends':
        out[k] = [[proj(a), proj(b)] for a, b in v]
    elif isinstance(v, list):
        out[k] = [proj(p) for p in v]
    else:
        out[k] = proj(v)
out['res'] = [sc.render.resolution_x, sc.render.resolution_y]
json.dump(out, open(f'{OUT}/{SHOT}.json', 'w'))
print('RENDERED', tag)
