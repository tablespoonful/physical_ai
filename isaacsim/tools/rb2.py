import bpy, sys, json, math, mathutils, glob, os
a = sys.argv[sys.argv.index("--") + 1:]
src, outp, hdr, spp = a[0], a[1], a[2], int(a[3])
J = json.load(open(os.path.join(src, "scene.json")))
bpy.ops.wm.read_factory_settings(use_empty=True)
for f in glob.glob(os.path.join(src, "*.obj")):
    name = os.path.basename(f)[:-4]
    bpy.ops.wm.obj_import(filepath=f, forward_axis="Y", up_axis="Z")
    objs = list(bpy.context.selected_objects)
    v = J["mats"][name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*v["c"], 1); b.inputs["Roughness"].default_value = v["r"]; b.inputs["Metallic"].default_value = v["me"]
    TD = a[4] if len(a) > 4 else ""
    TEX = {"FR3_Shell_White": (1.0, 0.0, True), "FR3_Metal": (0.75, 0.0, False), "FR3_Anthracite": (1.0, 0.03, False)}
    if TD and name in TEX:
        rs, rb, hasb = TEX[name]; nt = m.node_tree; L = nt.links.new
        def img(f, cs):
            t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(os.path.join(TD, f)); t.image.colorspace_settings.name = cs; return t
        r = img("fr3_shell_roughness.png", "Non-Color"); mt = nt.nodes.new("ShaderNodeMath"); mt.operation = "MULTIPLY_ADD"; mt.inputs[1].default_value = rs; mt.inputs[2].default_value = rb
        L(r.outputs[0], mt.inputs[0]); L(mt.outputs[0], b.inputs["Roughness"])
        q = img("fr3_shell_normal.png", "Non-Color"); nm = nt.nodes.new("ShaderNodeNormalMap"); L(q.outputs[0], nm.inputs["Color"]); L(nm.outputs[0], b.inputs["Normal"])
        if hasb:
            c = img("fr3_shell_basecolor.png", "sRGB"); L(c.outputs[0], b.inputs["Base Color"])
    for o in objs:
        o.data.materials.clear(); o.data.materials.append(m)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.select_all(action="DESELECT"); o.select_set(True)
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(60))
lo, hi = mathutils.Vector(J["lo"]), mathutils.Vector(J["hi"]); c = (lo + hi) / 2; h = hi.z - lo.z
bpy.ops.mesh.primitive_plane_add(size=10, location=(c.x, c.y, 0))
fm = bpy.data.materials.new("Floor"); fm.use_nodes = True; b = fm.node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.18, 0.18, 0.19, 1); b.inputs["Roughness"].default_value = 0.6; bpy.context.object.data.materials.append(fm)
w = bpy.data.worlds.new("W"); w.use_nodes = True; bpy.context.scene.world = w
n = w.node_tree; t = n.nodes.new("ShaderNodeTexEnvironment"); t.image = bpy.data.images.load(hdr); n.links.new(t.outputs[0], n.nodes["Background"].inputs[0])
s = bpy.context.scene; s.render.engine = "CYCLES"; s.cycles.device = "CPU"; s.cycles.samples = spp; s.cycles.use_denoising = True
s.render.threads_mode = "FIXED"; s.render.threads = 4; s.view_settings.view_transform = "AgX"; s.render.image_settings.file_format = "PNG"
def shot(tag, pos, tgt, lens, rx, ry):
    cam = bpy.data.objects.new(tag, bpy.data.cameras.new(tag)); s.collection.objects.link(cam); cam.data.lens = lens
    p = mathutils.Vector(pos); cam.location = p; cam.rotation_euler = (mathutils.Vector(tgt) - p).to_track_quat("-Z", "Y").to_euler()
    s.camera = cam; s.render.resolution_x = rx; s.render.resolution_y = ry; s.render.filepath = outp + "_" + tag + ".png"
    bpy.ops.render.render(write_still=True); print("RENDER_OK", tag, flush=True)
bpy.ops.object.light_add(type="AREA", location=(1.3, -0.25, 1.05)); k = bpy.context.object; k.data.energy = 55; k.data.size = 0.35
k.rotation_euler = (mathutils.Vector((0, 0, 0.75)) - k.location).to_track_quat("-Z", "Y").to_euler()
shot("full", (1.55, -2.1, 0.95), (0.0, 0, 0.56), 58, 700, 1000)
shot("close", (0.5, -0.62, 0.92), (0.03, 0, 0.72), 60, 700, 700)
shot("detail", (0.33, -0.32, 0.72), (0.04, 0, 0.62), 70, 700, 700)
