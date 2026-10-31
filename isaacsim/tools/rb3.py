import bpy, glob, json, math, mathutils, os, sys

a = sys.argv[sys.argv.index("--") + 1:]
src, out, hdr, spp, td, variant = a[0], a[1], a[2], int(a[3]), a[4], a[5]
J = json.load(open(os.path.join(src, "scene.json")))
V = {
    "plain": dict(c=(0.902, 0.922, 0.929), r=0.5, me=0.0),   # 公式 .dae の色のまま非金属
    "alu": dict(c=(0.913, 0.922, 0.924), r=0.35, me=1.0),    # アルミの F0
    "steel": dict(c=(0.56, 0.565, 0.578), r=0.3, me=1.0),    # 鉄の F0
    "alu_noenv": dict(c=(0.913, 0.922, 0.924), r=0.35, me=1.0),
    "uni": None,
}[variant]
TEX = {"FR3_Shell_White": (1.0, 0.0, True), "FR3_Metal": (0.75, 0.0, False), "FR3_Anthracite": (1.0, 0.03, False)}
bpy.ops.wm.read_factory_settings(use_empty=True)
for f in glob.glob(os.path.join(src, "*.obj")):
    name = os.path.basename(f)[:-4]
    bpy.ops.wm.obj_import(filepath=f, forward_axis="Y", up_axis="Z")
    objs = list(bpy.context.selected_objects)
    v = dict(J["mats"][name])
    if V and name in ("Finger_Aluminum", "Hand_Aluminum"):
        v = dict(c=list(V["c"]), r=V["r"], me=V["me"])
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*v["c"], 1)
    b.inputs["Roughness"].default_value = v["r"]
    b.inputs["Metallic"].default_value = v["me"]
    if name in ("Finger_Pad", "Hand_Dark"):
        b.inputs["IOR"].default_value = 1.35
    if name in TEX:
        rs, rb, hasb = TEX[name]
        L = nt.links.new
        def img(fn, cs):
            t = nt.nodes.new("ShaderNodeTexImage")
            t.image = bpy.data.images.load(os.path.join(td, fn))
            t.image.colorspace_settings.name = cs
            return t
        r = img("fr3_shell_roughness.png", "Non-Color")
        mt = nt.nodes.new("ShaderNodeMath")
        mt.operation = "MULTIPLY_ADD"
        mt.inputs[1].default_value = rs
        mt.inputs[2].default_value = rb
        L(r.outputs[0], mt.inputs[0])
        L(mt.outputs[0], b.inputs["Roughness"])
        q = img("fr3_shell_normal.png", "Non-Color")
        nm = nt.nodes.new("ShaderNodeNormalMap")
        L(q.outputs[0], nm.inputs["Color"])
        L(nm.outputs[0], b.inputs["Normal"])
        if hasb:
            L(img("fr3_shell_basecolor.png", "sRGB").outputs[0], b.inputs["Base Color"])
    for o in objs:
        o.data.materials.clear()
        o.data.materials.append(m)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
lo = mathutils.Vector(J["lo"])
bpy.ops.mesh.primitive_plane_add(size=10, location=(0.1, 0, 0))
fm = bpy.data.materials.new("Floor")
fm.use_nodes = True
b = fm.node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.18, 0.18, 0.19, 1)
b.inputs["Roughness"].default_value = 0.6
bpy.context.object.data.materials.append(fm)
w = bpy.data.worlds.new("W")
w.use_nodes = True
bpy.context.scene.world = w
n = w.node_tree
if variant == "alu_noenv":
    n.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
else:
    t = n.nodes.new("ShaderNodeTexEnvironment")
    t.image = bpy.data.images.load(hdr)
    n.links.new(t.outputs[0], n.nodes["Background"].inputs[0])
s = bpy.context.scene
s.render.engine = "CYCLES"
s.cycles.device = "CPU"
s.cycles.samples = spp
s.cycles.use_denoising = True
s.render.threads_mode = "FIXED"
s.render.threads = 4
s.view_settings.view_transform = "AgX"
s.render.image_settings.file_format = "PNG"
bpy.ops.object.light_add(type="AREA", location=(0.5, 0.05, 1.05))
k = bpy.context.object
k.data.energy = 7
k.data.size = 0.3
k.rotation_euler = (mathutils.Vector((0.09, 0, 0.84)) - k.location).to_track_quat("-Z", "Y").to_euler()
cam = bpy.data.objects.new("C", bpy.data.cameras.new("C"))
s.collection.objects.link(cam)
cam.data.lens = 85
p = mathutils.Vector((0.30, 0.235, 0.875))
cam.location = p
cam.rotation_euler = (mathutils.Vector((0.088, 0, 0.838)) - p).to_track_quat("-Z", "Y").to_euler()
s.camera = cam
s.render.resolution_x = 700
s.render.resolution_y = 700
s.render.filepath = out
bpy.ops.render.render(write_still=True)
print("RENDER_OK", variant, flush=True)
