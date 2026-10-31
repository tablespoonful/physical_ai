---
type: Verification Note
title: Blender の描画は Isaac Sim の確認にならない
description: 比較画像が USD のどこを読み、どこを補っているか
tags: [fr3, isaac-sim, blender, rendering]
status: draft
generated: { by: claude-code/claude-opus-5-5, at: 2026-10-31T10:17:48Z }
checked_with: [source-reading]
not_checked_with: [isaac-sim]
sources:
  - id: ext
    resource: ../../isaacsim/tools/ext.py
    title: USD を OBJ へ書き出すスクリプト
  - id: rb3
    resource: ../../isaacsim/tools/rb3.py
    title: Blender の描画スクリプト
  - id: work-log
    resource: ../../isaacsim/notes/fr3_usd_work_log.md
    title: FR3 USD の質感改善 作業記録
---

# 結論

`renders/` の画像は、USD を Blender で直接開いたものではありません。USD は Python と `usd-core` で書き換え、確認だけ Blender で行いました。Blender の USD 読み込みでは配置が崩れたので、OBJ を経由しています。[^work-log]

良い描画結果は「材質の値に見込みがある」ことの根拠にはなりますが、「USD が Isaac Sim で同じように見える」ことの根拠にはなりません。

# USD から渡るもの

位置、面、UV、材質の色、roughness、metallic は `ext.py` が書き出します。[^ext] 法線と `ior` は書き出していません。

# Blender 側で補っているもの

| 項目 | `rb3.py` の処理 | USD 側の状態 |
|---|---|---|
| 照明 | HDRI と面光源を配置[^rb3] | ライトなし |
| レンダラー | Cycles、デノイズあり[^rb3] | Isaac Sim の既定は Real-Time 2.0 |
| トーンマップ | AgX[^rb3] | 別の処理 |
| 法線 | 40° で自動スムージング[^rb3] | [ハンドに法線なし](../issues/hand-mesh-no-normals.md) |
| テクスチャ | フォルダを引数で指定[^rb3] | [参照の不一致あり](../issues/texture-path-case-mismatch.md) |
| `ior` | `Finger_Pad` と `Hand_Dark` に 1.35 を固定[^rb3] | `fr3v2_1.usda` に同じ値あり |
| カメラ | 85mm、700×700、手元に接近[^rb3] | 自分で設定 |

次の手順は [Isaac Sim で見た目を合わせる順序](../playbooks/isaac-sim-look-matching.md) を参照してください。

[^ext]: USD を OBJ へ書き出すスクリプト
[^rb3]: Blender の描画スクリプト
[^work-log]: FR3 USD の質感改善 作業記録
