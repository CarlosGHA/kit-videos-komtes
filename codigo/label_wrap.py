# exec() desde los builders de Blender: etiqueta envolvente sobre un cilindro (bpy y bmesh ya importados)
import math as _m
_LABEL_MATS = {}


def label_mat(path):
    if path in _LABEL_MATS:
        return _LABEL_MATS[path]
    m = bpy.data.materials.new('lab_' + path.split('/')[-1]); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(path)
    tex.interpolation = 'Cubic'
    nt.links.new(tex.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(tex.outputs['Alpha'], b.inputs['Alpha'])
    b.inputs['Roughness'].default_value = 0.4
    try:
        m.blend_method = 'HASHED'
    except Exception:
        pass
    _LABEL_MATS[path] = m
    return m


def label_shell(name, x, y, r, z0, z1, path, face=-90.0, arc=150.0, segs=28):
    """franja cilíndrica con UV (u: arco, v: altura) centrada en el ángulo 'face' (grados, 0 = +x)"""
    me = bpy.data.meshes.new(name); ob = bpy.data.objects.new(name, me); COL.objects.link(ob)
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    a0 = _m.radians(face - arc / 2)  # izquierda de la etiqueta vista de frente -> u=0
    da = _m.radians(arc) / segs
    cols = []
    for i in range(segs + 1):
        a = a0 + da * i
        cols.append((bm.verts.new((x + r * _m.cos(a), y + r * _m.sin(a), z0)),
                     bm.verts.new((x + r * _m.cos(a), y + r * _m.sin(a), z1))))
    for i in range(segs):
        f = bm.faces.new((cols[i][0], cols[i + 1][0], cols[i + 1][1], cols[i][1]))
        for lp, (u, v) in zip(f.loops, ((i / segs, 0), ((i + 1) / segs, 0), ((i + 1) / segs, 1), (i / segs, 1))):
            lp[uvl].uv = (u, v)
    bm.normal_update(); bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(label_mat(path))
    # normales hacia fuera
    me.flip_normals() if False else None
    return ob
