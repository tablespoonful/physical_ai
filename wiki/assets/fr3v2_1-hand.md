---
type: Robot Asset
title: FR3 + Franka Hand の修正版 USD
description: 最新アセットの内容と、確認済みの範囲
resource: ../../isaacsim/assets/fr3v2_1_hand/fr3v2_1.usda
tags: [fr3, isaac-sim, usd]
status: draft
generated: { by: claude-code/claude-opus-5-5, at: 2026-10-31T10:17:48Z }
checked_with: [usd-core, blender-cycles]
not_checked_with: [isaac-sim, real-robot]
sources:
  - id: work-log
    resource: ../../isaacsim/notes/fr3_usd_work_log.md
    title: FR3 USD の質感改善 作業記録
  - id: changes
    resource: ../../isaacsim/assets/fr3v2_1_hand/CHANGES.txt
    title: fr3v2_1_hand の変更点
---

# 概要

最新版は `isaacsim/assets/fr3v2_1_hand/` で、起動ファイルは `fr3v2_1.usda` です。元データは `franka_simulation` v0.1.0 の `fr3v2_1-isaacsim6.tar.gz` です。[^work-log]

修正版は 3 段階で作られました。[^work-log]

| 版 | 追加した内容 |
|---|---|
| `fr3v2_1_realistic` | 外装、金属、黒、濃灰の材質の分離 |
| `fr3v2_1_textured` | box 投影の UV と、手続き生成のテクスチャ |
| `fr3v2_1_hand` | Franka Hand の見た目用メッシュ |

# 確認の範囲

- `usd-core` で開けること、材質の割り当て、全高が約 1.1m になることを確認しています。[^work-log]
- **Isaac Sim では一度も開いていません。** 配布物の対応版は `6.0.0-rc.59` で、6.2.0 の動作も未確認です。[^work-log]
- 見た目の確認方法の限界は [Blender の描画は Isaac Sim の確認にならない](../verification/blender-vs-isaac-sim.md) を参照してください。

# 使うときの制約

- ハンドは見た目だけで、関節、衝突判定、質量はありません。指は片側 0.03m の開いた姿勢で固定です。[^work-log]
- 色、粗さ、`ior` は実測値でも Franka 公式の値でもありません。[^work-log]
- テクスチャは手続き生成で、実物の傷とは関係ありません。[^changes]
- `SHA256SUMS` は元の配布物の値で、変更後のファイルとは一致しません。[^changes]
- 既知の問題: [テクスチャ参照の不一致](../issues/texture-path-case-mismatch.md)、[ハンドの法線と UV](../issues/hand-mesh-no-normals.md)

[^work-log]: FR3 USD の質感改善 作業記録
[^changes]: fr3v2_1_hand の変更点
