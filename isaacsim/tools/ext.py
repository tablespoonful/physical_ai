"""USD を解決し、世界座標のメッシュ、UV、材質値を OBJ + JSON へ書き出す。"""
import collections, json, sys
from pathlib import Path
from pxr import Usd, UsdShade, UsdGeom, Gf

sys.stdout.reconfigure(encoding="utf-8")
usd, out = sys.argv[1], Path(sys.argv[2])
out.mkdir(exist_ok=True)
st = Usd.Stage.Open(usd)
xc = UsdGeom.XformCache(Usd.TimeCode.Default())
groups = collections.defaultdict(list)
mats = {}
lo, hi = [1e9] * 3, [-1e9] * 3
NL = chr(10)
for p in Usd.PrimRange(st.GetPseudoRoot(), Usd.TraverseInstanceProxies()):
    if not p.IsA(UsdGeom.Mesh):
        continue
    if UsdGeom.Imageable(p).ComputePurpose() in ("guide", "proxy"):
        continue
    m, _ = UsdShade.MaterialBindingAPI(p).ComputeBoundMaterial()
    key = "NONE"
    val = dict(c=[0.5, 0.5, 0.5], r=0.5, me=0.0)
    if m:
        key = m.GetPrim().GetPrimStack()[-1].path.name
        sh = m.ComputeSurfaceSource()[0]

        def g(k, d):
            for o in (m, sh):
                i = o.GetInput(k) if o else None
                if i and i.Get() is not None:
                    return i.Get()
            return d
        val = dict(c=list(g("diffuseColor", (0.5, 0.5, 0.5))), r=float(g("roughness", 0.5)), me=float(g("metallic", 0.0)))
    mats[key] = val
    M = xc.GetLocalToWorldTransform(p)
    me = UsdGeom.Mesh(p)
    pts = [M.Transform(Gf.Vec3d(*v)) for v in me.GetPointsAttr().Get()]
    for v in pts:
        for i in range(3):
            lo[i] = min(lo[i], v[i])
            hi[i] = max(hi[i], v[i])
    pv = UsdGeom.PrimvarsAPI(p).GetPrimvar("st")
    uv = list(pv.Get()) if pv and pv.HasValue() else None
    groups[key].append((pts, list(me.GetFaceVertexCountsAttr().Get()), list(me.GetFaceVertexIndicesAttr().Get()), uv))
print("bbox", [round(x, 3) for x in lo], [round(x, 3) for x in hi], "with_uv", sum(1 for g in groups.values() for x in g if x[3]))
for k, gs in groups.items():
    b, t, L = 1, 1, []
    for pts, cnt, idx, uv in gs:
        L.append("o part" + NL)
        L += [f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}" + NL for v in pts]
        if uv:
            L += [f"vt {u[0]:.6f} {u[1]:.6f}" + NL for u in uv]
        i = 0
        for c in cnt:
            f = idx[i:i + c]
            for j in range(1, c - 1):
                if uv:
                    L.append(f"f {f[0]+b}/{i+t} {f[j]+b}/{i+j+t} {f[j+1]+b}/{i+j+1+t}" + NL)
                else:
                    L.append(f"f {f[0]+b} {f[j]+b} {f[j+1]+b}" + NL)
            i += c
        b += len(pts)
        if uv:
            t += len(uv)
    (out / f"{k}.obj").write_text("".join(L), encoding="ascii", errors="ignore")
json.dump(dict(mats=mats, lo=lo, hi=hi), open(out / "scene.json", "w"), indent=0)
