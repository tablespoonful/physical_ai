---
type: Known Issue
title: tools のスクリプトでは最新アセットを再現できない
description: 元データと一部の処理が欠けており、再実行すると既存アセットを壊すものもある
tags: [fr3, isaac-sim, usd, tools]
status: draft
generated: { by: claude-code/claude-opus-5-5, at: 2026-10-31T10:17:48Z }
checked_with: [source-reading]
not_checked_with: [script-rerun]
sources:
  - id: work-log
    resource: ../../isaacsim/notes/fr3_usd_work_log.md
    title: FR3 USD の質感改善 作業記録
  - id: patch
    resource: ../../isaacsim/tools/patch_fr3.py
    title: 材質を分離したスクリプト
  - id: add-hand
    resource: ../../isaacsim/tools/add_hand.py
    title: ハンドを追加したスクリプト
---

# 内容

`isaacsim/tools/` は作業の記録で、再実行用には整備されていません。スクリプトは実行せず、コードと作業記録を読んで判断しました。

| 欠けているもの | 内容 |
|---|---|
| 元の配布物 | `fr3v2_1-isaacsim6.tar.gz` はリポジトリにありません。入手元は作業記録にあります。[^work-log] |
| UV の 4 倍処理 | `add_uv.py` は 1m 繰り返しですが、最新版は 25cm 繰り返しです。この処理のスクリプトはありません。[^work-log] |
| ハンドのメッシュ | `add_hand.py` はカレントディレクトリの `dl_hand/*.dae` を読みますが、リポジトリにありません。[^add-hand] |
| ハンドの最終値 | `add_hand.py` の材質は初期値のままです。[^add-hand] 最終値は作業記録の表にあります。[^work-log] |

# 再実行の危険

`patch_fr3.py` は `fr3v2_1_realistic` の絶対パスに固定で、`materials.usda` へ材質を追記します。[^patch] 適用済みのファイルに流すと定義が重複します。

# 対応

値の変更は USD を直接編集します。詳しくは [FR3 + Franka Hand の修正版 USD](../assets/fr3v2_1-hand.md) を参照してください。

[^work-log]: FR3 USD の質感改善 作業記録
[^patch]: 材質を分離したスクリプト
[^add-hand]: ハンドを追加したスクリプト
