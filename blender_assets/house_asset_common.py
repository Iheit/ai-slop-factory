import bpy, math, os, re
from mathutils import Vector

# Shared helpers for Creepy House procedural asset batches.
# Blender 5.1 compatible.

ROOT = 'CreepyHouse'


def safe_filename(name):
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', str(name)).strip('._') or 'Asset'


def output_root():
    """Return the generated_assets directory next to this helper script when possible."""
    path = ''
    for text in bpy.data.texts:
        if text.name == 'house_asset_common.py' and text.filepath:
            path = os.path.dirname(bpy.path.abspath(text.filepath))
            break
    if not path:
        path = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd()
    return os.path.abspath(os.path.join(path, 'generated_assets'))


def clean_collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    return col


def mat(name, color, metallic=0.0, rough=0.65):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.metallic = metallic
    m.roughness = rough
    return m


WOOD = mat('Old Painted Wood', (0.20, 0.13, 0.09), 0, 0.82)
DARKWOOD = mat('Dark Wood', (0.07, 0.045, 0.028), 0, 0.88)
METAL = mat('Worn Metal', (0.16, 0.18, 0.18), 0.65, 0.58)
GLASS = mat('Dirty Glass', (0.12, 0.16, 0.15), 0.05, 0.25)
CERAMIC = mat('Aged Ceramic', (0.42, 0.40, 0.35), 0, 0.7)
FABRIC = mat('Faded Fabric', (0.18, 0.17, 0.15), 0, 0.95)
PAPER = mat('Yellowed Paper', (0.55, 0.48, 0.33), 0, 0.9)
RUBBER = mat('Rubber', (0.025, 0.025, 0.022), 0, 0.9)


def cube(name, loc, scale, material=WOOD, bevel=0.05, col=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (scale[0] / 2, scale[1] / 2, scale[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new('Soft edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 2
    o.data.materials.append(material)
    if col and o.name not in col.objects:
        col.objects.link(o)
        if o.name in bpy.context.collection.objects:
            bpy.context.collection.objects.unlink(o)
    return o


def cyl(name, loc, r, depth, material=METAL, verts=20, col=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    if col:
        col.objects.link(o)
        if o.name in bpy.context.collection.objects:
            bpy.context.collection.objects.unlink(o)
    return o


def sphere(name, loc, r, material=METAL, col=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=r, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    if col:
        col.objects.link(o)
        if o.name in bpy.context.collection.objects:
            bpy.context.collection.objects.unlink(o)
    return o


def join_objects(objs, name):
    objs = [o for o in objs if o is not None and o.name in bpy.data.objects]
    if not objs:
        return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    objs[0].name = name
    return objs[0]


def plaque(name, text='WARNING', col=None):
    base = cube(name, (0, 0, 0), (0.8, 0.06, 0.32), METAL, 0.02, col)
    bpy.ops.object.text_add(location=(0, -0.035, 0), rotation=(math.pi / 2, 0, 0))
    t = bpy.context.object
    t.data.body = text
    t.data.align_x = 'CENTER'
    t.data.size = 0.12
    t.data.extrude = 0.008
    t.data.materials.append(PAPER)
    t.name = name + '_Text'
    if col:
        col.objects.link(t)
        if t.name in bpy.context.collection.objects:
            bpy.context.collection.objects.unlink(t)
    return base


def build(kind, name, col):
    o = []
    if kind == 'wall': o = [cube(name, (0, 0, 1.5), (4, .18, 3), WOOD, .04, col)]
    elif kind == 'floor': o = [cube(name, (0, 0, .05), (4, 4, .1), DARKWOOD, .02, col)]
    elif kind == 'ceiling': o = [cube(name, (0, 0, 1.5), (4, 4, .12), WOOD, .02, col)]
    elif kind == 'door': o = [cube(name, (0, 0, 1.2), (1.0, .14, 2.4), WOOD, .035, col), cube(name + '_Handle', (.35, -.10, 1.2), (.08, .08, .08), METAL, .02, col)]
    elif kind == 'window':
        o = [cube(name, (0, 0, 1.4), (1.5, .10, 1.2), DARKWOOD, .025, col), cube(name + '_Glass', (0, -.065, 1.4), (1.25, .03, .95), GLASS, .01, col)]
        for x in (-.62, 0, .62): o.append(cube(name + '_Mullion', (x, -.09, 1.4), (.035, .04, 1.0), WOOD, .005, col))
        o.append(cube(name + '_Cross', (0, -.09, 1.4), (1.25, .04, .035), WOOD, .005, col))
    elif kind == 'table':
        o = [cube(name, (0, 0, 1.0), (1.8, 1.0, .14), WOOD, .04, col)]
        for x in (-.72, .72):
            for y in (-.32, .32): o.append(cube(name + '_Leg', (x, y, .5), (.12, .12, 1.0), DARKWOOD, .02, col))
    elif kind == 'chair':
        o = [cube(name, (0, 0, .65), (.55, .55, .12), WOOD, .04, col), cube(name + '_Back', (0, .22, 1.1), (.55, .10, .95), WOOD, .035, col)]
        for x in (-.2, .2):
            for y in (-.2, .2): o.append(cube(name + '_Leg', (x, y, .32), (.07, .07, .55), DARKWOOD, .015, col))
    elif kind == 'cabinet':
        o = [cube(name, (0, 0, 1.0), (1.2, .5, 2), WOOD, .04, col)]
        for x in (-.3, .3): o.append(cyl(name + '_Knob', (x, -.29, 1.0), .045, .07, METAL, 16, col))
    elif kind == 'shelf':
        o = [cube(name, (0, 0, 1.25), (1.4, .38, .08), WOOD, .02, col), cube(name + '_Top', (0, 0, 2.45), (1.4, .38, .08), WOOD, .02, col)]
        for z in (.5, 1.1, 1.7, 2.3): o.append(cube(name + '_Shelf', (0, 0, z), (1.3, .35, .06), WOOD, .015, col))
        for x in (-.62, .62): o.append(cube(name + '_Side', (x, 0, 1.25), (.08, .38, 2.5), WOOD, .015, col))
    elif kind == 'sofa': o = [cube(name, (0, 0, .48), (2.0, .8, .35), FABRIC, .12, col), cube(name + '_Back', (0, .27, 1.0), (2.0, .28, 1.0), FABRIC, .12, col), cube(name + '_ArmL', (-.78, 0, .8), (.25, .8, .7), FABRIC, .1, col), cube(name + '_ArmR', (.78, 0, .8), (.25, .8, .7), FABRIC, .1, col)]
    elif kind == 'bed': o = [cube(name, (0, 0, .45), (2.0, 2.0, .28), DARKWOOD, .04, col), cube(name + '_Mattress', (0, 0, .7), (1.9, 1.9, .35), FABRIC, .1, col), cube(name + '_Headboard', (0, .86, 1.45), (2.0, .12, 1.5), WOOD, .04, col)]
    elif kind == 'lamp': o = [cyl(name, (0, 0, .65), .06, 1.2, METAL, 16, col), cyl(name + '_Base', (0, 0, .05), .22, .1, METAL, 20, col), cyl(name + '_Shade', (0, 0, 1.35), .28, .42, FABRIC, 24, col)]
    elif kind == 'rug': o = [cube(name, (0, 0, .025), (2.5, 1.6, .04), FABRIC, .04, col)]
    elif kind == 'mirror': o = [cube(name, (0, 0, 1.2), (1.0, .08, 1.5), DARKWOOD, .04, col), cube(name + '_Glass', (0, -.05, 1.2), (.82, .025, 1.3), GLASS, .01, col)]
    elif kind == 'toilet': o = [cyl(name, (0, 0, .38), .34, .5, CERAMIC, 24, col), cyl(name + '_Tank', (0, .2, .85), .3, .7, CERAMIC, 20, col), cyl(name + '_Seat', (0, 0, .65), .29, .08, CERAMIC, 24, col)]
    elif kind == 'sink': o = [cube(name, (0, 0, .9), (1.1, .55, .15), CERAMIC, .06, col), cyl(name + '_Basin', (0, 0, .82), .32, .18, CERAMIC, 20, col), cyl(name + '_Faucet', (0, .18, 1.2), .035, .5, METAL, 16, col)]
    elif kind == 'bathtub': o = [cube(name, (0, 0, .45), (1.7, .75, .55), CERAMIC, .14, col), cube(name + '_Inner', (0, -.01, .7), (1.35, .55, .18), GLASS, .08, col)]
    elif kind == 'fridge': o = [cube(name, (0, 0, 1.2), (1.0, .8, 2.4), METAL, .05, col), cube(name + '_Handle', (.42, -.06, 1.3), (.05, .05, .8), METAL, .01, col)]
    elif kind == 'stove':
        o = [cube(name, (0, 0, .55), (1.1, .7, .9), METAL, .04, col)]
        for x in (-.3, .3):
            for y in (-.2, .2): o.append(cyl(name + '_Burner', (x, y, 1.02), .12, .025, DARKWOOD, 20, col))
    elif kind == 'box': o = [cube(name, (0, 0, .4), (1.0, .8, .8), WOOD, .035, col), cube(name + '_Band', (0, 0, .4), (1.02, .06, .82), METAL, .01, col)]
    elif kind == 'crate':
        o = [cube(name, (0, 0, .45), (1.0, 1.0, .9), WOOD, .025, col)]
        for x in (-.3, 0, .3): o.append(cube(name + '_Slat', (x, -.51, .45), (.08, .04, .75), DARKWOOD, .01, col))
    elif kind == 'barrel': o = [cyl(name, (0, 0, .65), .45, 1.3, WOOD, 24, col), cyl(name + '_RingA', (0, 0, .35), .47, .06, METAL, 24, col), cyl(name + '_RingB', (0, 0, .95), .47, .06, METAL, 24, col)]
    elif kind == 'bucket': o = [cyl(name, (0, 0, .35), .35, .55, METAL, 24, col), cyl(name + '_Rim', (0, 0, .65), .36, .05, METAL, 24, col)]
    elif kind == 'pipe': o = [cyl(name, (0, 0, 1.0), .08, 2.0, METAL, 16, col)]
    elif kind == 'fusebox': o = [cube(name, (0, 0, 1.1), (.8, .25, 1.2), METAL, .03, col), cube(name + '_Door', (0, -.14, 1.1), (.65, .03, .9), DARKWOOD, .01, col)]
    elif kind == 'boiler': o = [cyl(name, (0, 0, 1.1), .55, 1.8, METAL, 24, col), cyl(name + '_Pipe', (0, .5, 1.8), .08, .9, METAL, 16, col)]
    elif kind == 'workbench':
        o = [cube(name, (0, 0, 1.0), (1.8, .7, .14), WOOD, .04, col)]
        for x in (-.75, .75): o.append(cube(name + '_Leg', (x, 0, .5), (.12, .55, 1.0), METAL, .02, col))
    elif kind == 'toolbox': o = [cube(name, (0, 0, .3), (.9, .5, .5), METAL, .05, col), cyl(name + '_Handle', (0, 0, .62), .04, .55, METAL, 16, col)]
    elif kind == 'clock':
        o = [cyl(name, (0, 0, 1.2), .38, .08, DARKWOOD, 32, col), cyl(name + '_Face', (0, -.05, 1.2), .31, .02, CERAMIC, 32, col)]
        for a in (0, math.pi / 2): o.append(cube(name + '_Hand', (math.sin(a) * .12, -.08, 1.2 + math.cos(a) * .12), (.025, .02, .25), DARKWOOD, .005, col))
    elif kind == 'painting': o = [cube(name, (0, 0, 1.4), (1.4, .08, 1.0), DARKWOOD, .035, col), cube(name + '_Canvas', (0, -.05, 1.4), (1.15, .025, .75), PAPER, .01, col)]
    elif kind == 'phone': o = [cube(name, (0, 0, .15), (.65, .35, .18), DARKWOOD, .05, col), cyl(name + '_Dial', (0, -.2, .23), .11, .04, CERAMIC, 20, col)]
    elif kind == 'safe': o = [cube(name, (0, 0, .8), (1.0, .7, 1.3), METAL, .05, col), cyl(name + '_Dial', (0, -.38, .85), .16, .06, METAL, 20, col)]
    elif kind == 'keypad': o = [cube(name, (0, 0, 1.2), (.45, .12, .7), METAL, .025, col)]
    elif kind == 'switch': o = [cube(name, (0, 0, 1.2), (.35, .08, .5), CERAMIC, .02, col), cyl(name + '_Toggle', (0, -.08, 1.2), .035, .12, METAL, 12, col)]
    elif kind == 'lever': o = [cube(name, (0, 0, .9), (.25, .2, .5), METAL, .02, col), cyl(name + '_Lever', (0, 0, 1.35), .05, .65, METAL, 16, col)]
    elif kind == 'note': o = [cube(name, (0, 0, .03), (.7, .5, .025), PAPER, .01, col)]
    elif kind == 'padlock': o = [cube(name, (0, 0, .22), (.25, .1, .3), METAL, .025, col), cyl(name + '_Shackle', (0, 0, .45), .09, .22, METAL, 16, col)]
    elif kind == 'trunk': o = [cube(name, (0, 0, .5), (1.3, .75, .8), DARKWOOD, .08, col), cube(name + '_Latch', (0, -.4, .55), (.12, .04, .18), METAL, .01, col)]
    elif kind == 'suitcase': o = [cube(name, (0, 0, .45), (1.1, .7, .45), FABRIC, .06, col), cyl(name + '_Handle', (0, 0, .75), .035, .35, METAL, 12, col)]
    elif kind == 'typewriter': o = [cube(name, (0, 0, .22), (.75, .45, .3), METAL, .04, col), cube(name + '_Paper', (0, .04, .43), (.42, .03, .35), PAPER, .01, col)]
    elif kind == 'toy': o = [sphere(name, (0, 0, .35), .3, FABRIC, col), sphere(name + '_EyeL', (-.1, -.27, .42), .035, DARKWOOD, col), sphere(name + '_EyeR', (.1, -.27, .42), .035, DARKWOOD, col)]
    elif kind == 'photograph': o = [cube(name, (0, 0, .04), (.5, .38, .03), DARKWOOD, .01, col), cube(name + '_Image', (0, -.025, .04), (.42, .30, .015), PAPER, .005, col)]
    elif kind == 'drawer': o = [cube(name, (0, 0, .55), (1.0, .6, .7), WOOD, .04, col), cyl(name + '_Pull', (0, -.34, .62), .04, .12, METAL, 16, col)]
    elif kind == 'secret_bookcase': o = [cube(name, (0, 0, 1.3), (1.5, .4, 2.6), DARKWOOD, .04, col), cube(name + '_Gap', (0, -.23, 1.3), (.9, .03, 2.1), DARKWOOD, .01, col)]
    elif kind == 'puzzle_box': o = [cube(name, (0, 0, .3), (.65, .5, .5), DARKWOOD, .05, col), cyl(name + '_Dial', (0, -.27, .32), .09, .05, METAL, 20, col)]
    elif kind == 'ritual_table': o = [cube(name, (0, 0, .9), (1.2, .7, .14), DARKWOOD, .04, col), cyl(name + '_Leg', (0, 0, .45), .18, .9, DARKWOOD, 16, col)]
    elif kind == 'hanging_bulb': o = [cyl(name, (0, 0, 1.4), .025, 1.4, RUBBER, 12, col), sphere(name + '_Bulb', (0, 0, .68), .12, CERAMIC, col)]
    elif kind == 'vent': o = [cube(name, (0, 0, 1.2), (.8, .08, .5), METAL, .02, col)]
    elif kind == 'rug_round':
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=.04, location=(0, 0, .03))
        x = bpy.context.object
        x.name = name
        x.data.materials.append(FABRIC)
        col.objects.link(x)
        if x.name in bpy.context.collection.objects:
            bpy.context.collection.objects.unlink(x)
        o = [x]
    elif kind == 'stair':
        for i in range(6): o.append(cube(name + f'_Step{i}', (i * .35, 0, i * .22), (.5, 1.2, .22), WOOD, .025, col))
    else:
        o = [cube(name, (0, 0, .5), (1, 1, 1), WOOD, .03, col)]
    return join_objects(o, name)


def save_isolated_blend(obj, path):
    """Write a .blend containing only obj and its required dependency datablocks."""
    if obj is None:
        raise RuntimeError('Cannot save an empty asset.')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # libraries.write follows the object's mesh/material/modifier dependencies,
    # unlike save_as_mainfile(copy=True), which copies the entire current scene.
    bpy.data.libraries.write(
        path,
        {obj},
        path_remap='RELATIVE',
        fake_user=True,
        compress=True,
    )
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        raise RuntimeError(f'Blender did not create {path}')


def finalize_asset(name, obj, batch_name):
    """Normalize an asset name and export a truly isolated .blend file."""
    asset_name = safe_filename(name)
    if obj is None:
        raise RuntimeError(f'{asset_name}: build() returned no object')
    obj.name = asset_name
    if obj.data:
        obj.data.name = asset_name + '_Mesh'
    folder = os.path.join(output_root(), safe_filename(batch_name))
    path = os.path.join(folder, asset_name + '.blend')
    save_isolated_blend(obj, path)
    return path


def generate_batch(batch_name, specs):
    col = clean_collection(batch_name)
    saved = []
    for index, (name, kind) in enumerate(specs, 1):
        obj = build(kind, safe_filename(name), col)
        path = finalize_asset(name, obj, batch_name)
        saved.append(path)
        print(f'[{batch_name}] {index}/{len(specs)} saved: {path}')
    bpy.ops.object.select_all(action='DESELECT')
    print(f'{batch_name}: generated and isolated {len(saved)} assets')
    return saved
