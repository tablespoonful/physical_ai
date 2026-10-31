"""FR3 の link8 へ Franka Hand の見た目用メッシュを追加する。関節は作らない。"""
import math, sys
import numpy as np
import trimesh
from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade

sys.stdout.reconfigure(encoding="utf-8")
ROOT = sys.argv[1]
LINK8 = "/fr3v2_1/Geometry/base/fr3v2_1_link0/fr3v2_1_link1/fr3v2_1_link2/fr3v2_1_link3/fr3v2_1_link4/fr3v2_1_link5/fr3v2_1_link6/fr3v2_1_link7/fr3v2_1_link8"
st = Usd.Stage.Open(ROOT + "/fr3v2_1.usda")
assert st.GetPrimAtPath(LINK8).IsValid()
hand = UsdGeom.Xform.Define(st, LINK8 + "/franka_hand_visual")
hand.AddRotateZOp().Set(-45.0)  # URDF の rpy_ee: 0 0 -pi/4

looks = LINK8 + "/franka_hand_visual/Looks"
UsdGeom.Scope.Define(st, looks)
MATS = {  # 実測値ではない。アルミは文献の F0、他は開始値
    "Hand_Shell": ((0.78, 0.78, 0.77), 0.42, 0.0),
    "Finger_Aluminum": ((0.913, 0.922, 0.924), 0.35, 1.0),
    "Hand_Aluminum": ((0.913, 0.922, 0.924), 0.35, 1.0),
    "Hand_Dark": ((0.03, 0.03, 0.03), 0.5, 0.0),
    "Finger_Pad": ((0.03, 0.03, 0.03), 0.7, 0.0),
}
mat = {}
for n, (c, r, me) in MATS.items():
    m = UsdShade.Material.Define(st, f"{looks}/{n}")
    s = UsdShade.Shader.Define(st, f"{looks}/{n}/PreviewSurface")
    s.CreateIdAttr("UsdPreviewSurface")
    s.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*c))
    s.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(r)
    s.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(me)
    s.CreateInput("useSpecularWorkflow", Sdf.ValueTypeNames.Int).Set(0)
    m.CreateSurfaceOutput().ConnectToSource(s.ConnectableAPI(), "surface")
    mat[n] = m


def add(parent, name, scene, key_to_mat):
    n = 0
    for node in scene.graph.nodes_geometry:
        T, gname = scene.graph[node]
        g = scene.geometry[gname]
        key = next(v for k, v in key_to_mat.items() if k in gname)
        P = trimesh.transformations.transform_points(g.vertices, T)
        me = UsdGeom.Mesh.Define(st, f"{parent}/{name}_{n}")
        me.CreatePointsAttr([Gf.Vec3f(*map(float, v)) for v in P])
        me.CreateFaceVertexCountsAttr([3] * len(g.faces))
        me.CreateFaceVertexIndicesAttr([int(i) for i in np.asarray(g.faces).ravel()])
        me.CreateSubdivisionSchemeAttr("none")
        UsdShade.MaterialBindingAPI.Apply(me.GetPrim()).Bind(mat[key])
        n += 1
    return n


HAND = {"Feature002": "Hand_Aluminum", "Feature005_005": "Hand_Shell", "Feature005_000": "Hand_Aluminum", "Feature_011": "Hand_Dark", "Feature001_011": "Hand_Dark"}
FINGER = {"Feature_007": "Finger_Pad", "Feature001_006": "Finger_Aluminum"}
base = LINK8 + "/franka_hand_visual"
print("hand parts", add(base, "hand", trimesh.load("dl_hand/white_hand.dae", force="scene"), HAND))
fs = trimesh.load("dl_hand/white_finger.dae", force="scene")
Q = 0.03  # 開いた姿勢
for name, rz, y in (("finger_left", 0.0, Q), ("finger_right", 180.0, Q)):
    x = UsdGeom.Xform.Define(st, f"{base}/{name}")
    x.AddRotateZOp().Set(rz)
    x.AddTranslateOp().Set(Gf.Vec3d(0, y, 0.0584))
    print(name, add(f"{base}/{name}", "part", fs, FINGER))
st.GetRootLayer().Save()
print("saved")
