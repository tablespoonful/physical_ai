import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
R = Path("C:/Users/table/physical_ai/isaacsim/assets/fr3v2_1_realistic/payloads")
MATS = {  # 実測値ではなく開始値
 "FR3_Shell_White": ((0.78, 0.78, 0.77), 0.42, 0),
 "FR3_Metal": ((0.76, 0.76, 0.75), 0.30, 1),
 "FR3_Black": ((0.03, 0.03, 0.03), 0.50, 0),
 "FR3_Anthracite": ((0.022, 0.031, 0.033), 0.45, 0),
}
m = (R / "materials.usda").read_text(encoding="utf-8")
blk = re.search(r'    def Material "Connectors_Metal"\n.*?\n    }\n', m, re.S).group(0)
new = ""
for n, (c, r, me) in MATS.items():
    b = blk.replace("Connectors_Metal", n)
    b = b.replace("color3f inputs:diffuseColor = (1, 1, 1)", f"color3f inputs:diffuseColor = {c}")
    b = b.replace("float inputs:metallic = 0", f"float inputs:metallic = {me}").replace("float inputs:roughness = 0.5", f"float inputs:roughness = {r}")
    new += "\n" + b
i = m.rstrip().rfind("}")
(R / "materials.usda").write_text(m[:i] + new + m[i:], encoding="utf-8")
s = (R / "instances.usda").read_text(encoding="utf-8")
def tgt(name):
    if re.match(r"Shells?_[Ww]hite", name): return "FR3_Shell_White"
    if re.match(r"(Flange_Tie_Metal|Connectors_Metal)", name): return "FR3_Metal"
    if re.match(r"Connectors_[Bb]lack", name): return "FR3_Black"
    if name.startswith("tn__7016"): return "FR3_Anthracite"
n = {}
def rep(x):
    t = tgt(x.group(2))
    if not t: return x.group(0)
    n[t] = n.get(t, 0) + 1
    return x.group(1) + "</Materials/" + t + ">"
s2 = re.sub(r'(def Material "([^"]+)" \(\s*instanceable = true\s*prepend references = @\./materials\.usda@)</Materials/[^>]+>', rep, s)
(R / "instances.usda").write_text(s2, encoding="utf-8")
print(n)
(R.parent / "CHANGES.txt").write_text("franka_simulation v0.1.0 の fr3v2_1 を元に、materials.usda に 4 材質を追加し、instances.usda の参照先を変更。\n値は実測ではなく開始値。SHA256SUMS は元の配布物の値で、変更ファイルとは一致しない。\n", encoding="utf-8")
