---
okf_version: "0.2"
---

# physical_ai wiki

## アセット

* [FR3 + Franka Hand の修正版 USD](assets/fr3v2_1-hand.md) - 最新アセットの内容と、確認済みの範囲

## 既知の問題

* [テクスチャ参照の大文字小文字の不一致](issues/texture-path-case-mismatch.md) - `../textures/` の参照に対し、実際のフォルダは `Textures/`
* [ハンドのメッシュに法線と UV がない](issues/hand-mesh-no-normals.md) - ハンド 9 メッシュの法線と UV が USD に入っていない
* [tools のスクリプトでは最新アセットを再現できない](issues/tools-not-reproducible.md) - 元データと一部の処理が欠けており、再実行すると既存アセットを壊すものもある

## 検証の注意

* [Blender の描画は Isaac Sim の確認にならない](verification/blender-vs-isaac-sim.md) - 比較画像が USD のどこを読み、どこを補っているか

## 手順

* [Isaac Sim で見た目を合わせる順序](playbooks/isaac-sim-look-matching.md) - 値を調整する前に確認する項目と順序
