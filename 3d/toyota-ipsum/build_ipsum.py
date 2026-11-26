"""Build a low-poly Toyota Ipsum (2nd generation, ACM20/21, 2001) in Blender.

Run (background, factory settings so your preferences are not touched):
    blender --factory-startup -b -P build_ipsum.py -- <out_dir> [render] [CYCLES]

Car faces -Y (Blender front view). Units are metres.
Approximate real dimensions: 4.40 m long, 1.70 m wide, 1.65 m tall, 2.70 m wheelbase.
This is a stylised model from remembered proportions, not a measured replica.
"""
import math
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else "."
DO_RENDER = "render" in argv
FORCE_CYCLES = "CYCLES" in argv

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "IpsumScene"


# ---------- helpers ----------
def new_mat(name, color, metallic=0.0, rough=0.5, emit=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m


M_PAINT = new_mat("Paint_Silver", (0.62, 0.64, 0.68), metallic=0.85, rough=0.28)
M_GLASS = new_mat("Glass", (0.01, 0.015, 0.02), metallic=0.0, rough=0.04)
M_TIRE = new_mat("Tire", (0.02, 0.02, 0.02), rough=0.85)
M_RIM = new_mat("Rim", (0.75, 0.76, 0.78), metallic=1.0, rough=0.25)
M_PLASTIC = new_mat("BlackPlastic", (0.03, 0.03, 0.035), rough=0.6)
M_CHROME = new_mat("Chrome", (0.85, 0.86, 0.88), metallic=1.0, rough=0.12)
M_HEAD = new_mat("Headlight", (0.9, 0.92, 0.95), rough=0.1, emit=(1.0, 0.97, 0.88), strength=2.0)
M_TAIL = new_mat("Taillight", (0.35, 0.01, 0.01), rough=0.15, emit=(0.9, 0.03, 0.02), strength=0.8)
M_GROUND = new_mat("Ground", (0.07, 0.07, 0.08), rough=0.8)


def make_obj(name, bm, material, parent=None, smooth=True):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    if material:
        ob.data.materials.append(material)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    if parent:
        ob.parent = parent
    return ob


def loft(rings):
    """rings: list of lists of Vector, all with the same vertex count."""
    bm = bmesh.new()
    vr = [[bm.verts.new(v) for v in ring] for ring in rings]
    n = len(vr[0])
    for i in range(len(vr) - 1):
        for j in range(n):
            bm.faces.new((vr[i][j], vr[i][(j + 1) % n], vr[i + 1][(j + 1) % n], vr[i + 1][j]))
    bm.faces.new(vr[0])
    bm.faces.new(vr[-1][::-1])
    return bm


def add_box(bm, center, size):
    m = Matrix.Translation(center) @ Matrix.Diagonal(Vector((size[0], size[1], size[2], 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=m)


def add_cyl_x(bm, radius, depth, center, segments=32):
    """Cylinder whose axis runs along X."""
    m = Matrix.Translation(center) @ Matrix.Rotation(math.pi / 2, 4, "Y")
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                          radius1=radius, radius2=radius, depth=depth, matrix=m)


def poly(bm, pts):
    bm.faces.new([bm.verts.new(p) for p in pts])


# ---------- key dimensions ----------
Z0 = 0.22          # underbody height
BELT = 0.95        # top of lower body (beltline)
GB = 0.85          # greenhouse base (sits inside lower body)
HB = 0.84          # greenhouse half-width at its base
HR = 0.71          # greenhouse half-width at the roof
ROOF_Z = 1.65
WHEEL_R = 0.31
WB = 1.35          # axle offset from centre (wheelbase 2.70 m)
TRACK = 0.73


def hw_g(z):
    """Greenhouse half-width at height z (linear taper)."""
    return HB - (HB - HR) / (ROOF_Z - GB) * (z - GB)


root = bpy.data.objects.new("Ipsum", None)
scene.collection.objects.link(root)

# ---------- lower body ----------
# (y, top z, half width)
lower_st = [(-2.20, 0.74, 0.80), (-2.10, 0.84, 0.83), (-1.45, 0.93, 0.85), (-1.00, BELT, 0.85),
            (2.00, BELT, 0.85), (2.20, BELT, 0.82)]
rings = [[Vector((-hw, y, Z0)), Vector((hw, y, Z0)), Vector((hw, y, top)), Vector((-hw, y, top))]
         for (y, top, hw) in lower_st]
body = make_obj("Body_Lower", loft(rings), M_PAINT, root)
bev = body.modifiers.new("Bevel", "BEVEL")
bev.width = 0.06
bev.segments = 3
bev.limit_method = "ANGLE"

# wheel arch cutters
bm = bmesh.new()
for sx in (-1, 1):
    for sy in (-1, 1):
        add_cyl_x(bm, 0.39, 0.5, Vector((sx * 0.85, sy * WB, WHEEL_R)))
cutters = make_obj("ArchCutters", bm, None, root, smooth=False)
cutters.hide_render = True
cutters.hide_set(True)
boo = body.modifiers.new("Arches", "BOOLEAN")
boo.operation = "DIFFERENCE"
boo.object = cutters
boo.solver = "EXACT"

# ---------- greenhouse ----------
gh_st = [(-1.45, 0.96, HR), (-0.55, 1.62, HR), (1.75, ROOF_Z, HR), (2.12, 1.58, HR), (2.20, 1.42, 0.69)]
rings = [[Vector((-HB, y, GB)), Vector((HB, y, GB)), Vector((hr, y, top)), Vector((-hr, y, top))]
         for (y, top, hr) in gh_st]
cabin = make_obj("Body_Cabin", loft(rings), M_PAINT, root)
bev = cabin.modifiers.new("Bevel", "BEVEL")
bev.width = 0.04
bev.segments = 2
bev.limit_method = "ANGLE"

# ---------- glass ----------
bm = bmesh.new()
off = 0.012


ws = lambda z: -1.45 + (z - 0.96) * (0.90 / 0.66)   # windshield line: y as a function of z
GH_TOP = [(-1.45, 0.96), (-0.55, 1.62), (1.75, ROOF_Z), (2.12, 1.58)]


def ztop(y):
    """Greenhouse roof height at y (piecewise linear between the loft stations)."""
    for (ya, za), (yb, zb) in zip(GH_TOP, GH_TOP[1:]):
        if ya <= y <= yb:
            return za + (zb - za) * (y - ya) / (yb - ya)
    return GH_TOP[-1][1]


def side_x(y, z):
    """Exact x of the greenhouse side surface at (y, z), so glass hugs the body."""
    return HB - (HB - HR) * (z - GB) / (ztop(y) - GB)


def side_window(y_front_fn, y1, z0, z1, cols=10):
    """Window strip on both sides. y_front_fn(z) gives the (possibly sloped) front edge."""
    for s in (-1, 1):
        bmw = bm
        grid = []
        for k in range(cols + 1):
            t = k / cols
            col = []
            for z in (z0, z1):
                yf = y_front_fn(z)
                y = yf + (y1 - yf) * t
                col.append(bmw.verts.new(Vector((s * (side_x(y, z) + off), y, z))))
            grid.append(col)
        for k in range(cols):
            quad = (grid[k][0], grid[k + 1][0], grid[k + 1][1], grid[k][1])
            bmw.faces.new(quad if s > 0 else quad[::-1])


# front door (front edge follows the windshield slope), sliding door, rear quarter window
side_window(lambda z: ws(z) + 0.11, -0.12, 1.07, 1.55)
side_window(lambda z: 0.03, 0.88, 1.07, 1.56)
side_window(lambda z: 0.98, 1.88, 1.07, 1.56)
# windshield
n_off = Vector((0, -0.0035, 0.0048))
poly(bm, [Vector((-0.66, ws(0.99), 0.99)) + n_off, Vector((0.66, ws(0.99), 0.99)) + n_off,
          Vector((0.66, ws(1.58), 1.58)) + n_off, Vector((-0.66, ws(1.58), 1.58)) + n_off])
# rear glass
rg = lambda z: 0.84 - 0.3 * (z - 0.85) - 0.17
poly(bm, [Vector((-rg(0.95), 2.206, 0.95)), Vector((rg(0.95), 2.206, 0.95)),
          Vector((rg(1.36), 2.206, 1.36)), Vector((-rg(1.36), 2.206, 1.36))][::-1])
make_obj("Glass", bm, M_GLASS, root, smooth=False)

# ---------- door shut lines ----------
bm = bmesh.new()
for y in (-0.90, -0.05, 0.92):
    for s in (-1, 1):
        w = 0.008
        z_lo, z_hi = 0.34, BELT
        pts = [Vector((s * 0.855, y, z_lo)), Vector((s * 0.855, y + w, z_lo)),
               Vector((s * 0.855, y + w, z_hi)), Vector((s * 0.855, y, z_hi))]
        if s < 0:
            pts = pts[::-1]
        poly(bm, pts)
        z1 = 1.50
        pts = [Vector((s * (side_x(y, z_hi) + 0.003), y, z_hi)), Vector((s * (side_x(y + w, z_hi) + 0.003), y + w, z_hi)),
               Vector((s * (side_x(y + w, z1) + 0.003), y + w, z1)), Vector((s * (side_x(y, z1) + 0.003), y, z1))]
        if s < 0:
            pts = pts[::-1]
        poly(bm, pts)
make_obj("DoorLines", bm, M_PLASTIC, root, smooth=False)

# ---------- bumpers, grille, lights, mirrors ----------
bm = bmesh.new()
add_box(bm, Vector((0, -2.19, 0.38)), (1.62, 0.07, 0.24))      # front bumper lower
add_box(bm, Vector((0, 2.20, 0.37)), (1.64, 0.07, 0.26))       # rear bumper
add_box(bm, Vector((0, -2.21, 0.60)), (0.74, 0.03, 0.17))      # grille opening
bump = make_obj("Bumpers", bm, M_PLASTIC, root, smooth=False)
bev = bump.modifiers.new("Bevel", "BEVEL")
bev.width = 0.02
bev.segments = 2

bm = bmesh.new()
add_box(bm, Vector((0, -2.225, 0.60)), (0.5, 0.01, 0.025))     # chrome grille bar
make_obj("GrilleBar", bm, M_CHROME, root, smooth=False)

bm = bmesh.new()
for s in (-1, 1):
    add_box(bm, Vector((s * 0.60, -2.205, 0.66)), (0.34, 0.03, 0.13))
make_obj("Headlights", bm, M_HEAD, root, smooth=False)

bm = bmesh.new()
for s in (-1, 1):
    add_box(bm, Vector((s * 0.69, 2.215, 0.87)), (0.14, 0.02, 0.42))
make_obj("Taillights", bm, M_TAIL, root, smooth=False)

bm = bmesh.new()
for s in (-1, 1):
    add_box(bm, Vector((s * 0.915, -0.78, 1.08)), (0.10, 0.06, 0.10))
mir = make_obj("Mirrors", bm, M_PAINT, root, smooth=False)
bev = mir.modifiers.new("Bevel", "BEVEL")
bev.width = 0.015
bev.segments = 2

# ---------- wheels ----------
bm_tire, bm_rim, bm_cap, bm_well = bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new()
for sx in (-1, 1):
    for sy in (-1, 1):
        c = Vector((sx * TRACK, sy * WB, WHEEL_R))
        add_cyl_x(bm_tire, WHEEL_R, 0.20, c)
        add_cyl_x(bm_rim, 0.21, 0.205, c)
        add_cyl_x(bm_cap, 0.05, 0.215, c, segments=16)
        add_cyl_x(bm_well, 0.385, 0.02, Vector((sx * 0.62, sy * WB, WHEEL_R)))
make_obj("Tires", bm_tire, M_TIRE, root)
make_obj("Rims", bm_rim, M_RIM, root)
make_obj("HubCaps", bm_cap, M_CHROME, root)
make_obj("WheelWells", bm_well, M_PLASTIC, root, smooth=False)

# ---------- stage: ground, lights, camera ----------
bm = bmesh.new()
poly(bm, [Vector((-20, -20, 0)), Vector((20, -20, 0)), Vector((20, 20, 0)), Vector((-20, 20, 0))][::-1])
make_obj("Ground", bm, M_GROUND, None, smooth=False)

world = bpy.data.worlds.new("World")
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.06, 0.07, 0.09, 1)
bg.inputs["Strength"].default_value = 1.0
scene.world = world

sun = bpy.data.lights.new("Sun", "SUN")
sun.energy = 3.0
sun.angle = math.radians(25)
sun_ob = bpy.data.objects.new("Sun", sun)
sun_ob.rotation_euler = (math.radians(50), math.radians(10), math.radians(35))
scene.collection.objects.link(sun_ob)

fill = bpy.data.lights.new("Fill", "AREA")
fill.energy = 500
fill.size = 6
fill_ob = bpy.data.objects.new("Fill", fill)
fill_ob.location = (-5, -5, 4)
fill_ob.rotation_euler = (math.radians(60), 0, math.radians(-45))
scene.collection.objects.link(fill_ob)

rim = bpy.data.lights.new("Rim", "AREA")
rim.energy = 600
rim.size = 5
rim_ob = bpy.data.objects.new("Rim", rim)
rim_ob.location = (4, 6, 3.5)
rim_ob.rotation_euler = (math.radians(65), 0, math.radians(150))
scene.collection.objects.link(rim_ob)

cam_data = bpy.data.cameras.new("Cam")
cam_data.lens = 45
cam = bpy.data.objects.new("Cam", cam_data)
cam.location = (6.2, -8.4, 2.0)
scene.collection.objects.link(cam)
target = bpy.data.objects.new("CamTarget", None)
target.location = (0, 0, 0.75)
scene.collection.objects.link(target)
tc = cam.constraints.new("TRACK_TO")
tc.target = target
tc.track_axis = "TRACK_NEGATIVE_Z"
tc.up_axis = "UP_Y"
scene.camera = cam

# ---------- render settings (TikTok portrait) ----------
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 50   # preview size; set to 100 for the final
scene.render.fps = 30
scene.frame_start, scene.frame_end = 1, 150

engine_ok = False
if not FORCE_CYCLES:
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            scene.render.engine = eng
            engine_ok = True
            break
        except TypeError:
            continue
if not engine_ok:
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
else:
    try:
        scene.eevee.taa_render_samples = 32
    except AttributeError:
        pass
    try:
        scene.eevee.use_raytracing = False
    except AttributeError:
        pass

# ---------- turntable (not rendered unless you ask) ----------
try:
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
except Exception:
    pass
root.rotation_euler = (0, 0, 0)
root.keyframe_insert("rotation_euler", index=2, frame=1)
root.rotation_euler = (0, 0, math.radians(360))
root.keyframe_insert("rotation_euler", index=2, frame=151)
scene.frame_set(1)

# ---------- save ----------
bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/toyota_ipsum_2001.blend")
print("SAVED", f"{OUT}/toyota_ipsum_2001.blend", "engine:", scene.render.engine)

if DO_RENDER:
    scene.render.image_settings.file_format = "PNG"
    for name, loc in (("preview.png", (6.2, -8.4, 2.0)), ("preview_rear.png", (-6.2, 8.4, 2.0))):
        cam.location = loc
        scene.render.filepath = f"{OUT}/{name}"
        bpy.ops.render.render(write_still=True)
        print("RENDERED", scene.render.filepath)
    cam.location = (6.2, -8.4, 2.0)
    bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/toyota_ipsum_2001.blend")
