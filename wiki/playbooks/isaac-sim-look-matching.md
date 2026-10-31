---
type: Playbook
title: Isaac Sim で見た目を合わせる順序
description: 値を調整する前に確認する項目と順序
tags: [fr3, isaac-sim, rendering]
status: draft
generated: { by: claude-code/claude-opus-5-5, at: 2026-10-31T10:17:48Z }
checked_with: []
not_checked_with: [isaac-sim]
sources:
  - id: photorealism
    resource: ../../isaacsim/notes/photorealism.md
    title: Isaac Sim で実物に近い質感を出すノウハウ
  - id: work-log
    resource: ../../isaacsim/notes/fr3_usd_work_log.md
    title: FR3 USD の質感改善 作業記録
---

# 位置づけ

この順序は調査と USD の読み取りから組み立てた案で、Isaac Sim では試していません。

# 手順

1. **テクスチャが読めているか確認する。** Linux なら [参照の不一致](../issues/texture-path-case-mismatch.md) を先に直します。
2. **色空間とノーマルマップの形式を確認する。** roughness と normal は `raw`、basecolor は `sRGB` です。normal は OpenGL 形式 (+Y) です。[^work-log][^photorealism]
3. **Path Tracing で見る。** 調整中は `PathTracing` で正解を確認し、最後に Real-Time 2.0 で再現度を見ます。Minimal は間接光がないので評価に使いません。[^photorealism]
4. **照明をそろえる。** Dome Light に HDRI を使います。比較用には Poly Haven の `studio_small_09` を使っていました。[^work-log] 金属の見え方は周囲の映り込みで大きく変わります。[^photorealism]
5. **法線を確認する。** ハンドが角張るなら [法線の不足](../issues/hand-mesh-no-normals.md) を疑います。
6. **露出とトーンマップをそろえ、最後に値を調整する。** Isaac Sim 6.x の推奨値は未確認です。[^photorealism]

# 値の決め方

Blender の値をそのまま移しても、同じ見た目にはなりません。[Blender と条件が違う](../verification/blender-vs-isaac-sim.md) ためです。実物に合わせるなら、カラーチェッカーを FR3 の横に置いて撮影し、同じ配置の Isaac Sim の画像と比べます。[^photorealism]

[^photorealism]: Isaac Sim で実物に近い質感を出すノウハウ
[^work-log]: FR3 USD の質感改善 作業記録
