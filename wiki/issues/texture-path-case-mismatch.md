---
type: Known Issue
title: テクスチャ参照の大文字小文字の不一致
description: "`../textures/` の参照に対し、実際のフォルダは `Textures/`"
tags: [fr3, isaac-sim, usd, texture]
status: draft
generated: { by: claude-code/claude-opus-5-5, at: 2026-10-31T10:17:48Z }
checked_with: [usd-core-on-windows]
not_checked_with: [isaac-sim, linux]
sources:
  - id: materials
    resource: ../../isaacsim/assets/fr3v2_1_hand/payloads/materials.usda
    title: fr3v2_1_hand の materials.usda
---

# 内容

`fr3v2_1_hand` の `payloads/materials.usda` は、テクスチャを `../textures/fr3_shell_*.png` として参照しています。[^materials] 一方、実際のフォルダ名は `Textures/` です。

# 影響

- 確認済み: Windows の `usd-core` では `...\fr3v2_1_hand\textures\...` へ解決されました。Windows のファイルシステムは大文字小文字を区別しないためです。
- 未確認の推測: 大文字小文字を区別する Linux では、テクスチャが見つからないはずです。

対象は `FR3_Shell_White`、`FR3_Metal`、`FR3_Anthracite` です。[^materials]

# 対応

未修正です。参照先を `../Textures/` に直すか、フォルダ名を `textures` に変えるかの二択で、`add_uv.py` の出力先の前提に合わせるなら後者です。

Blender の比較画像はテクスチャのフォルダを引数で直接渡しているので、この問題の影響を受けません。詳しくは [Blender の描画は Isaac Sim の確認にならない](../verification/blender-vs-isaac-sim.md) を参照してください。

[^materials]: fr3v2_1_hand の materials.usda
