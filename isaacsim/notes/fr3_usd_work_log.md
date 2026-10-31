# FR3 USD の質感改善 作業記録

作業日: 2026-10-31

Isaac Sim で FR3 本体と Franka Hand の質感を実物に近づけるため、公式 USD を元に修正版を作った記録です。

## 結論

- 質感が出ない主因は、公式 USD のマテリアルにありました。全マテリアルがテクスチャなし、粗さ 0.5、金属度 0 で、外装と金属部品が同じマテリアルを共有していました。
- 材質の分離と、金属部の `metallic=1` は効果が大きく、金属部品は明確に改善しました。
- 白い外装は、粗さマップと細かい傷を入れても差が小さいままです。傷は描画でほとんど見えていません。
- **現在の最新版は `assets/fr3v2_1_hand/` です。**
- **Isaac Sim では一度も開いていません。** 確認は USD ライブラリ (`usd-core`) と Blender Cycles (CPU) で行いました。

## 成果物

すべて `C:\Users\table\physical_ai\isaacsim\` の下にあります。

| パス | 内容 | 状態 |
|---|---|---|
| `assets/fr3v2_1_realistic/` | 材質の値を修正した版 | 中間成果 |
| `assets/fr3v2_1_textured/` | 上に UV とテクスチャを追加した版 | 中間成果 |
| `assets/fr3v2_1_hand/` | 上に Franka Hand の見た目を追加した版 | **最新** |
| `renders/` | 比較画像 | 最新は `fr3_hand_unichrome_v3.png` |
| `tools/` | 使ったスクリプト | パスは今回の環境に固定 |
| `notes/photorealism.md` | 質感のノウハウ全般 | |

各版の起動ファイルは、フォルダ内の `fr3v2_1.usda` です。

## 元データ

- [frankarobotics/franka_simulation](https://github.com/frankarobotics/franka_simulation/releases) v0.1.0 の `fr3v2_1-isaacsim6.tar.gz`
- 配布物の対応バージョンは Isaac Sim `6.0.0-rc.59` です。
- Franka Hand のメッシュは [franka_description](https://github.com/frankarobotics/franka_description) の `meshes/robot_ee/franka_hand_white/visual/` を使いました。取り付け位置は同リポジトリの URDF 定義に合わせました。
- 照明の確認には Poly Haven の HDRI `studio_small_09` (1K) を使いました。アセットには含めていません。

## 公式 USD の分析結果

| 項目 | 値 |
|---|---|
| シェーダー | 全 20 個が `UsdPreviewSurface` |
| テクスチャ | 0 枚 |
| UV | なし |
| roughness | 全マテリアルで 0.5 |
| metallic | 全マテリアルで 0 |
| 外装 `Shell_White` などの参照先 | `Connectors_Metal` |
| `Connectors_Metal` の色 | (1, 1, 1) |

外装と金属部品は、同じ「完全な白の非金属」でした。別の公式資料である `franka_description` のメッシュと MuJoCo Menagerie の `fr3.xml` でも、白は `1 1 1` です。

## 作業の流れ

### 1. 材質の分離と値の修正 (`fr3v2_1_realistic`)

`payloads/materials.usda` に 4 つのマテリアルを追加し、`payloads/instances.usda` の参照先を変更しました。スクリプトは `tools/patch_fr3.py` です。

| マテリアル | 変更したメッシュ数 | 色 (線形) | roughness | metallic |
|---|---:|---|---:|---:|
| `FR3_Shell_White` | 8 | (0.78, 0.78, 0.77) | 0.42 | 0 |
| `FR3_Metal` | 3 | (0.76, 0.76, 0.75) | 0.30 | 1 |
| `FR3_Black` | 2 | (0.03, 0.03, 0.03) | 0.50 | 0 |
| `FR3_Anthracite` | 5 | (0.022, 0.031, 0.033) | 0.45 | 0 |

### 2. 粗さマップと傷の追加 (`fr3v2_1_textured`)

- メッシュ 58 個に box 投影で UV (`primvars:st`) を追加しました。`tools/add_uv.py` です。
- `textures/` に basecolor、roughness、normal を置きました。いずれも 2048px で、`tools/gen_tex.py` で手続き生成したものです。
- テクスチャは 25cm ごとに繰り返します。`add_uv.py` の出力は 1m 繰り返しなので、その後に UV を 4 倍しました。この処理のスクリプトは残していません。
- roughness と normal は `raw`、basecolor は `sRGB` を明示しました。normal は OpenGL 形式 (+Y) で、`UsdUVTexture` の scale 2、bias -1 で読みます。

テクスチャの調整は 3 回行いました。

| 回 | 結果 | 対応 |
|---|---|---|
| 1 | 凹凸が強すぎて革のように見えた | 模様を細かくして、normal を弱めた |
| 2 | 傷がほぼ消えた (画素の 0.02%) | 傷を太く増やした |
| 3 | テクスチャには傷があるが、描画ではほとんど見えない | ここで打ち切り |

### 3. Franka Hand の追加 (`fr3v2_1_hand`)

`link8` の下に `franka_hand_visual` を追加しました。スクリプトは `tools/add_hand.py` で、メッシュは `fr3v2_1.usda` に直接入っています。

- ハンド本体は Z 軸まわりに -45 度回転しています。
- 指は開いた姿勢 (片側 0.03m) で固定です。
- **見た目だけです。** 指の関節、衝突判定、質量はありません。

### 4. 指の金属とゴムの調整

金属の見え方を確認するため、4 条件で比較しました (`renders/fr3_hand_finger_metal_compare.png`)。金属の見た目は、色の値より `metallic` の設定と周囲の映り込みで大きく変わります。

その後、ユーザーの指定に合わせて変更しました。

- 金属部: ユニクロメッキのような青白い色。2 回調整した。
- 非金属部: 硬質ゴムのようなほぼ黒。色を暗くするだけでは足りず、`ior` を下げて反射を弱めた。

## Franka Hand の最終的な値

| マテリアル | 対象 | 色 (線形) | roughness | metallic | ior |
|---|---|---|---:|---:|---:|
| `Finger_Aluminum` | 指本体 | (0.56, 0.70, 0.92) | 0.30 | 1 | 既定 |
| `Hand_Aluminum` | ハンドの金属部品 | (0.56, 0.70, 0.92) | 0.30 | 1 | 既定 |
| `Finger_Pad` | 指先パッド | (0.006, 0.006, 0.0065) | 0.72 | 0 | 1.35 |
| `Hand_Dark` | ハンドの黒い部品 | (0.006, 0.006, 0.0065) | 0.72 | 0 | 1.35 |
| `Hand_Shell` | ハンドの白い外装 | (0.78, 0.78, 0.77) | 0.42 | 0 | 既定 |

名前は `Aluminum` のままですが、現在の値はユニクロメッキ調です。

マテリアルの場所:

```text
/fr3v2_1/Geometry/base/.../fr3v2_1_link8/franka_hand_visual/Looks/
```

## 確認したこと

- 修正版の USD を `usd-core` で開けること
- 外装、金属、黒、濃灰の材質の割り当て
- 3 種類のマテリアルのテクスチャ参照が解決できること
- 手元の配置で全高が約 1.1m になること

## 確認していないこと

- Isaac Sim で開けるか、エラーが出ないか
- Isaac Sim の RTX での見え方。Blender とはレンダラーもトーンマッピングも異なります。
- ハンドが腕の動きに追従するか
- 物理シミュレーションへの影響
- Isaac Sim 6.2.0 での動作。配布物の対応は `6.0.0-rc.59` です。
- 実物との比較。写真やカラーチェッカーとは比べていません。

## 注意点

- 色、粗さ、`ior` の値は実測ではありません。Franka 公式に指定された値でもありません。
- ハンドの金属部と黒い部品を、どの部品に割り当てるかは、部品名と公式の色からの推定です。
- テクスチャは手続き生成で、実物の傷の位置や形とは関係ありません。
- `SHA256SUMS` は元の配布物の値です。変更したファイルとは一致しません。
- 肘の同心円状の模様は、修正前にもあります。公式メッシュのポリゴンの粗さが原因と考えられます。
- 箱投影の UV は、面の向きが変わる部分に境目が出る可能性があります。
- Blender の USD 読み込みでは配置が崩れたので、確認には `tools/ext.py` で書き出した OBJ を使いました。

## 次にやること

1. NVIDIA GPU 環境の Isaac Sim で `assets/fr3v2_1_hand/fr3v2_1.usda` を開いて確認する
2. 指を動かす場合は、URDF からハンドの関節ごと組み込む
3. 実機の写真やカラーチェッカーで色を合わせる
4. 実機の接写写真から粗さマップを作る
5. 公式 CAD (SolidWorks) から滑らかなメッシュを作り直す
