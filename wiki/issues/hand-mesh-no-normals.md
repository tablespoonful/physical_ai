---
type: Known Issue
title: ハンドのメッシュに法線と UV がない
description: ハンド 9 メッシュの法線と UV が USD に入っていない
tags: [fr3, isaac-sim, usd, mesh]
status: draft
generated: { by: claude-code/claude-opus-5-5, at: 2026-10-31T10:17:48Z }
checked_with: [usd-core]
not_checked_with: [isaac-sim]
sources:
  - id: add-hand
    resource: ../../isaacsim/tools/add_hand.py
    title: ハンドを追加したスクリプト
  - id: asset
    resource: ../../isaacsim/assets/fr3v2_1_hand/fr3v2_1.usda
    title: fr3v2_1_hand の起動ファイル
---

# 内容

`usd-core` で調べた結果は次のとおりです。[^asset]

| 対象 | メッシュ数 | 法線 | UV (`st`) | `subdivisionScheme` |
|---|---:|---|---|---|
| 腕 | 50 | あり (vertex) | あり | `none` |
| ハンド | 9 | なし | なし | `none` |

ハンドを追加したスクリプトは、頂点、面、材質だけを書き込んでいます。[^add-hand]

# 影響

- 確認済み: ハンドにはテクスチャを適用できません。UV がないためです。
- 未確認の推測: Isaac Sim でハンドの面が角張って見える可能性があります。

Blender の比較画像は `rb3.py` が 40° で自動スムージングしているので、この問題が見えません。

# 対応

未修正です。元の `.dae` の法線を移すか、ハンドのメッシュから法線を計算して USD に書き込みます。

[^asset]: fr3v2_1_hand の起動ファイル
[^add-hand]: ハンドを追加したスクリプト
