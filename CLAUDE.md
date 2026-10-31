# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリの性質

Physical AI の論文と資料の収集物です。アプリケーションではないので、ビルド、lint、テストはありません。例外は `isaacsim/tools/` の単発スクリプトで、FR3 の USD アセットを修正したときのものです。

git で管理しています。`origin` は公開リポジトリ `tablespoonful/physical_ai` で、push した内容はすぐに公開されます。`.gitattributes` で改行変換を無効にしているので、原典のバイト列は変わりません。

## 構成

分野フォルダは `VLA`、`worldmodel`、`ヒューマノイド`、`franka(fr3)`、`franka_ROS2` の 5 つで、形式は共通です。

- `README.md`: 要点、主要論文、収集状況
- `_catalog.csv`: 全候補の一覧。列は `local_file,title,date,authors,source,venue,survey,url,pdf,abstract`。UTF-8 BOM 付き
- `_catalog.md`: CSV をリンク付きの表にしたもの
- 直下の `*.md`: PDF から `pymupdf4llm` で変換した論文本文。YAML front matter に `title`、`date`、`authors`、`url`、`pdf` がある
- `notes/`: 調査ノート。`*_candidates.tsv` は委譲先が出した候補で、`*_candidates.md` は同じ内容の読みやすい版
- `docs/`: 公式資料の取得時点の本文。`franka(fr3)/docs/` では `.rst.txt` や `.pdf` の原本と `.md` が並ぶ

`isaacsim/` だけ形式が異なり、`assets/`、`renders/`、`tools/`、`docs/`、`notes/` からなります。

## Wiki

`wiki/` は分野をまたぐ知識の層で、[OKF](https://github.com/GoogleCloudPlatform/open-knowledge-format) v0.2 の形式です。分野フォルダと `isaacsim/` は原典として扱い、wiki の作業では変更しません。現在の対象は FR3 + Isaac Sim だけです。

質問に答えるときは `wiki/index.md` から読み、数値や但し書きは出典の原典で確認します。ページの書き方は次のとおりです。

- frontmatter に `type`、`title`、`description`、`generated`、`status`、`sources` を書きます。LLM が書いたページは人が確認するまで `status: draft` とし、`verified` は実際に確認した人かプロセスだけを記録します。
- 主張には `sources[].id` をラベルにした脚注を付けます。
- `checked_with` と `not_checked_with` は OKF の外の独自キーです。何で確認し、何で確認していないかを書きます。原典の「未確認」は要約で消さず、確認済みの事実と未確認の推測を本文で分けます。
- 読んでいない論文は取り込みません。候補やカタログの全件処理はしません。
- ページを足したら `wiki/index.md` と `wiki/log.md` を更新し、lint を通します。

```powershell
uv run --no-project --with pyyaml python tools/wiki_lint.py
```

wiki の問題は ERROR で終了コード 1、既存カタログの問題は WARN です。参照先は Linux で失敗しないよう、大文字小文字まで一致するか検査します。分野を超えて使える教訓は `~/knowledge/` へ置きます。

## 収集物の扱い

- カタログ生成と PDF 変換のスクリプトは残っていません。`_catalog.csv` を変えたら `_catalog.md`、分野の `README.md` の収集状況、ルートの `README.md` の表も手で合わせます。
- 論文の PDF は、公開 URL を確認できたものは `.md` へ変換後に削除しています。残っている 17 本は、URL がないか本文を抽出できなかったものです。`README.md` の一部に残る `*.pdf` の記述は変換前のものです。
- `local_file` が空の行は、本文を保存していない候補です。同じファイルを複数行が指すこと、`.md` ではなく `.pdf` を指すことがあります。
- `source` の `delegated` は、Sonnet、Codex、Cursor への委譲で得た候補です。
- 関連度の判定と `notes/themes.md` の分類は機械的なもので、本文は読んでいません。調査ノートは出典と「未確認」を区別して書かれているので、追記でも区別を保ちます。
- 変換後の本文は数式と表が崩れている場合があります。数値を引用するときは、`.md` 先頭のリンクから PDF で確認します。

## シェル上の注意

`franka(fr3)` の括弧や `ヒューマノイド` の日本語、論文名の空白があるので、パスは必ず引用符で囲みます。PowerShell では `-LiteralPath` を使います。CSV は `-Encoding UTF8` を指定して読みます。

## Isaac Sim アセット

`assets/` の版は `realistic` → `textured` → `hand` の順に積み上げたものです。**最新は `assets/fr3v2_1_hand/` で、起動ファイルは `fr3v2_1.usda` です。** 経緯と未確認事項は `isaacsim/notes/fr3_usd_work_log.md` にあります。

### 実行方法

既定の Python には `pxr` と `trimesh` がありません。`usd-core` は `uv` で一時的に入れます。

```powershell
# USD を解決して OBJ + scene.json へ書き出す
uv run --no-project --python 3.12 --with usd-core python isaacsim/tools/ext.py isaacsim/assets/fr3v2_1_hand/fr3v2_1.usda <出力先>

# 上の出力を Blender Cycles (CPU) で描画する。Blender は PATH にない
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b -P isaacsim/tools/rb3.py -- <ext の出力先> <出力.png> <HDRI> <サンプル数> <テクスチャのフォルダ> <plain|alu|steel|alu_noenv|uni>
```

Blender の USD 読み込みでは配置が崩れるので、`ext.py` の OBJ を経由します。`rb2.py` は全身、近接、詳細の 3 カットを描画し、引数は `-- <src> <出力の接頭辞> <HDRI> <サンプル数> [テクスチャのフォルダ]` です。描画の確認用 HDRI (Poly Haven `studio_small_09`) はリポジトリにありません。

### スクリプトを再実行する前に

`tools/` は作業の記録で、再実行で最新版を再現することはできません。既存アセットに流すと壊れます。

- `patch_fr3.py`: 書き換え先のパスが固定で、材質を追記するだけなので、適用済みのファイルに流すと定義が重複します。
- `add_uv.py`: UV は 1m 繰り返しで出力されますが、最新版は 25cm 繰り返しです。4 倍にした処理のスクリプトは残っていません。
- `add_hand.py`: カレントディレクトリの `dl_hand/` にメッシュが必要ですが、リポジトリにありません。材質の値も初期値のままで、最終値は `fr3v2_1.usda` と作業記録の表にあります。
- `gen_tex.py` の「1 枚 1m」も、上の 4 倍処理の前の値です。

値の変更は `fr3v2_1.usda` や `payloads/materials.usda` を直接編集します。

### 既知の問題

- `payloads/materials.usda` は `../textures/` を参照していますが、実際のフォルダは `Textures/` です。Windows では解決できても、Linux の Isaac Sim ではテクスチャが見つからなくなります。
- ハンドの 9 メッシュには法線も UV もありません。腕の 50 メッシュにはどちらもあります。
- `SHA256SUMS` は元の配布物の値で、変更後のファイルとは一致しません。
- `Finger_Aluminum` と `Hand_Aluminum` は名前と違い、ユニクロメッキ調の値です。
- 色、粗さ、`ior` は実測値でも Franka 公式の値でもありません。ハンドは見た目だけで、関節、衝突判定、質量がありません。
- Isaac Sim では一度も開いていません。確認は `usd-core` と Blender だけです。
