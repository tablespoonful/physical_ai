"""geometries.usd へ box 投影の st を追加し、材質へテクスチャを接続する。"""
import numpy as np, sys
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf
sys.stdout.reconfigure(encoding="utf-8")
R = sys.argv[1]
st = Usd.Stage.Open(R + "/payloads/geometries.usd"); xc = UsdGeom.XformCache(Usd.TimeCode.Default()); n = 0; ext = []; had = 0
for p in st.TraverseAll():
    if not p.IsA(UsdGeom.Mesh): continue
    m = UsdGeom.Mesh(p); api = UsdGeom.PrimvarsAPI(p)
    had += bool(api.GetPrimvar("st") and api.GetPrimvar("st").HasValue())
    P = np.array(m.GetPointsAttr().Get(), dtype=np.float64)
    if len(P) == 0: continue
    M = np.array(xc.GetLocalToWorldTransform(p)).T          # 列ベクトル
    W = (M[:3, :3] @ P.T).T + M[:3, 3]
    ext.append(float(np.ptp(W, axis=0).max()))
    C = np.array(m.GetFaceVertexCountsAttr().Get()); I = np.array(m.GetFaceVertexIndicesAttr().Get())
    uv = np.zeros((len(I), 2), np.float32); o = 0
    for c in C:
        f = I[o:o + c]; a, b, d = W[f[0]], W[f[1]], W[f[-1]]
        nrm = np.abs(np.cross(b - a, d - a)); ax = int(np.argmax(nrm)); keep = [i for i in range(3) if i != ax]
        uv[o:o + c] = W[f][:, keep]; o += c
    n += 1
    p.GetAttribute  # noqa
    api.CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying).Set([Gf.Vec2f(float(u), float(v)) for u, v in uv])
print("meshes", n, "had_st", had, "max extent", round(max(ext), 3))
K = 1.0 if max(ext) < 10 else 0.001
if K != 1.0:
    for p in st.TraverseAll():
        if p.IsA(UsdGeom.Mesh):
            pv = UsdGeom.PrimvarsAPI(p).GetPrimvar("st")
            if pv: pv.Set([Gf.Vec2f(u * K, v * K) for u, v in pv.Get()])
print("uv scale to meters", K); st.GetRootLayer().Save()
ms = Usd.Stage.Open(R + "/payloads/materials.usda")
def wire(name, rough_scale, rough_bias, base=None):
    mp = f"/Materials/{name}"; pv = UsdShade.Shader.Get(ms, mp + "/PreviewSurface")
    rd = UsdShade.Shader.Define(ms, mp + "/stReader"); rd.CreateIdAttr("UsdPrimvarReader_float2"); rd.CreateInput("varname", Sdf.ValueTypeNames.Token).Set("st"); out = rd.CreateOutput("result", Sdf.ValueTypeNames.Float2)
    def tex(nm, f, cs):
        t = UsdShade.Shader.Define(ms, mp + "/" + nm); t.CreateIdAttr("UsdUVTexture"); t.CreateInput("file", Sdf.ValueTypeNames.Asset).Set("../textures/" + f)
        t.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(out); t.CreateInput("sourceColorSpace", Sdf.ValueTypeNames.Token).Set(cs)
        t.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat"); t.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat"); return t
    tr = tex("roughnessTex", "fr3_shell_roughness.png", "raw"); tr.CreateInput("scale", Sdf.ValueTypeNames.Float4).Set(Gf.Vec4f(rough_scale)); tr.CreateInput("bias", Sdf.ValueTypeNames.Float4).Set(Gf.Vec4f(rough_bias))
    pv.GetInput("roughness").ClearSources() if False else None
    pv.GetInput("roughness").ConnectToSource(tr.CreateOutput("r", Sdf.ValueTypeNames.Float))
    tn = tex("normalTex", "fr3_shell_normal.png", "raw"); tn.CreateInput("scale", Sdf.ValueTypeNames.Float4).Set(Gf.Vec4f(2, 2, 2, 1)); tn.CreateInput("bias", Sdf.ValueTypeNames.Float4).Set(Gf.Vec4f(-1, -1, -1, 0))
    pv.CreateInput("normal", Sdf.ValueTypeNames.Normal3f).ConnectToSource(tn.CreateOutput("rgb", Sdf.ValueTypeNames.Float3))
    if base:
        tb = tex("baseTex", base, "sRGB"); pv.GetInput("diffuseColor").ConnectToSource(tb.CreateOutput("rgb", Sdf.ValueTypeNames.Float3))
wire("FR3_Shell_White", 1.0, 0.0, "fr3_shell_basecolor.png")
wire("FR3_Metal", 0.75, 0.0)
wire("FR3_Anthracite", 1.0, 0.03)
ms.GetRootLayer().Save(); print("materials ok")
