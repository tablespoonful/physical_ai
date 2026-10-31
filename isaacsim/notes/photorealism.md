# Isaac Sim で実物に近い質感を出すノウハウ

調査日: 2026-10-31。対象は Isaac Sim 6.x です。実機での検証はしていません。「経験則」と書いた項目は公式の記載ではなく、一般的な PBR の知識に基づく判断です。

## 結論

質感が悪いときは、シェーダーを作り込む前に次の順で確認します。

1. テクスチャの色空間
2. ノーマルマップの形式
3. レンダリングモード
4. 照明 (HDRI)
5. 物体のスケールとメッシュの法線

設定で足りない場合は、見た目を作り込むより、実物をスキャンする (NuRec) か、シミュレーション映像を生成 AI で写実化する (Cosmos Transfer) ほうが早いことがあります。

## 1. 色空間

最も見落としやすい原因です。

SimReady の仕様では、テクスチャの色空間の既定値は `auto` で、**8 ビットの 3 チャンネルまたは 4 チャンネルの画像は sRGB として解釈されます**。ファイル形式ではなく、ビット深度とチャンネル数で決まります ([SimReady Materials](https://nvidia.github.io/simready-foundation/2026.08.0-post1/capabilities/visualization/materials/requirements.html))。OmniPBR の `auto` も同様です ([OmniPBR](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/templates/OmniPBR.html))。

このため、3 チャンネルで保存した roughness や metallic、normal のマップが、意図せず sRGB として読まれることがあります。SimReady の文書も、1 チャンネルの roughness を 3 チャンネルに替えるだけで解釈が変わると警告しています。

| マップ | 色空間 |
|---|---|
| Albedo / Base Color | sRGB |
| Emissive | 通常は sRGB (経験則) |
| Roughness | raw |
| Metallic | raw |
| Normal | raw |
| Opacity | raw |
| ORM | raw |

## 2. ノーマルマップ

- 公式のベストプラクティスは、Substance で **DirectX 形式**の法線を使うよう案内しています ([Materials Best Practices](https://docs.omniverse.nvidia.com/simready/latest/simready-asset-creation/material-best-practices.html))。
- OmniPBR には `flip_tangent_u` (既定 false) と `flip_tangent_v` (既定 true) があります。凹凸が逆に見えるときは、まず V 方向の反転を切り替えます。
- Poly Haven などは OpenGL 形式を配布している場合があるので、入手時に形式を確認します (経験則)。

## 3. レンダリングモード

出典: [Rendering modes](https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/rendering_modes.html)、[RTX Path Tracing](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/rtx-renderer_pt.html)

| モード | `renderer` の値 | 用途 |
|---|---|---|
| RTX - Real-Time 2.0 | `RealTimePathTracing` | 既定。対話操作と合成データ |
| RTX - Interactive (Path Tracing) | `PathTracing` | 最終画像、見た目の検証 |
| RTX - Minimal | `MinimalRendering` | 学習ループなど速度優先。間接光なし |

```python
from isaacsim import SimulationApp
simulation_app = SimulationApp({"renderer": "PathTracing"})
```

見た目を調整するときは Path Tracing で正解を確認し、そのあと Real-Time 2.0 でどこまで再現できるかを見ます (経験則)。Minimal は間接光がないので、質感の評価には使いません。

| 設定 | 既定値 | 調整の方針 |
|---|---|---|
| `/rtx/pathtracing/spp` | 1 | フレームごとのサンプル数。範囲は 1〜32 |
| `/rtx/pathtracing/totalSpp` | 512 | 累積サンプルの上限。ノイズが残るなら増やす |
| `/rtx/pathtracing/maxBounces` | 4 | 増やすと正確になるが遅くなる |
| `/rtx/pathtracing/optixDenoiser/enabled` | true | 細かいテクスチャが消えるなら弱める |
| `/rtx/pathtracing/optixDenoiser/blendFactor` | 1.0 と記載 | 公式の説明では 0 がノイズ除去のみ、1.0 が除去なし。既定値と Denoising の有効設定の関係は実機で確認する |
| `/rtx/pathtracing/optixDenoiser/temporalMode/enabled` | false | 動画のちらつき対策 |

ガラスや金属、液体が暗いときは、`maxBounces` と透過、反射の最大バウンス数を確認します。

## 4. マテリアルの選択

出典: [Material Templates](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/materials_templates.html)、[SimReady Materials](https://nvidia.github.io/simready-foundation/2026.08.0-post1/capabilities/visualization/materials/requirements.html)

| マテリアル | 向いている用途 |
|---|---|
| OpenPBR | 新規作成の第一候補。SimReady が将来の標準としている |
| OmniPBR | 既存の Omniverse 資産、一般的な不透明物 |
| OmniSurface | 複雑な多層の質感 |
| OmniGlass | ガラス |
| UsdPreviewSurface | 軽量。大規模学習向け |

SimReady は、MDL (OmniPBR) を NVIDIA 固有とし、レガシー用途でのみ追加するよう案内しています。

プラスチックのように見える物体の見直し点は次のとおりです (経験則を含む)。

- 実物の表面は roughness が均一ではありません。指紋、擦り傷、ムラを roughness マップに入れます。
- 金属は metallic を 1 付近に、非金属は 0 にします。中間の値は錆など混在部分だけに使います。
- `reflection_roughness_texture_influence` の既定値は 0.0 です。マップを接続しても 1 にしないと効きません。金属の `metallic_texture_influence` も確認します。
- 素材の継ぎ目や角の面取り (bevel) がないと CG らしく見えます。
- 透明や半透明の物体 (ペットボトル、牛乳、皮膚) は OmniPBR だけでは再現しにくいので、OmniGlass や OmniSurface を使います。

## 5. 照明

- 背景と反射の両方に HDRI を使います。Isaac Sim の同梱資産にも HDRI があります。
- Omniverse の [環境マテリアルの解説](https://docs.omniverse.nvidia.com/guide_rtx-best-practices/latest/environment/environment-materials.html) は、Skydome の露出と回転を Dome Light に合わせるよう案内しています。
- 実験室を再現するなら、現場で撮影した HDRI か、実際の照明と同じ位置と色温度のライトを使います (経験則)。
- 光源は矩形や円盤の面光源にすると、影の縁が自然になります (経験則)。

## 6. カメラ

手元の資料では詳細を確認できていません。以下は実機カメラに合わせるための経験則です。

- 焦点距離と画角を実機カメラに合わせます。D405 の深度視野は 87°×58° です。
- 露出、ホワイトバランス、モーションブラー、被写界深度、レンズの歪みを合わせます。
- 実機の画像と並べて、ヒストグラムと色を比較します。

## 7. テクスチャとアセット

- **解像度**: 公式の推奨は 1K か 2K を基本に、最大 4K です。8K は避けます ([Best Practices](https://docs.omniverse.nvidia.com/simready/latest/simready-asset-creation/material-best-practices.html))。
- **テクセル密度**: シミュレーション用の目標は 2048 ピクセル/メートルです。
- **小物**: 手首カメラで近くから写る物体は、解像度不足が目立ちます。把持対象だけ解像度を上げます (経験則)。
- **入手先**: [Poly Haven](https://polyhaven.com/) と [ambientCG](https://ambientcg.com/) は CC0 の PBR 素材があります。
- **スキャン**: 写真測量のテクスチャは撮影時の影が焼き込まれるので、影の除去 (de-lighting) が必要です (経験則)。

## 8. 実物を取り込む: NuRec

[公式ブログ](https://developer.nvidia.com/blog/reconstruct-a-scene-in-nvidia-isaac-sim-using-only-a-smartphone/) の手順です。

1. 十分に重なる写真を約 100 枚撮影します。手ブレを避けます。
2. COLMAP でカメラ位置を推定します。
3. 3DGUT で再構成します。
4. USDZ で出力し、Isaac Sim 5.0 以降に読み込みます。

再構成結果は見た目だけで、衝突判定を持ちません。Ground Plane とプロキシメッシュを追加して、物理と影に対応させます。照明の変更や物体の移動ができるかは、資料の範囲では確認できていません。

背景は NuRec、操作する物体は通常のメッシュ、と分ける構成が現実的です (経験則)。

## 9. 映像を写実化する: Cosmos Transfer

Isaac Sim の `CosmosWriter` で RGB、深度、セグメンテーション、エッジを記録し、Cosmos Transfer で写実的な動画に変換します ([公式チュートリアル](https://docs.isaacsim.omniverse.nvidia.com/6.1.0/replicator_tutorials/tutorial_replicator_cosmos.html))。SO-101 の [Sim-to-Real 教材](https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/14-strategy3-cosmos.html) にも手順があります。

見た目は大きく改善できますが、生成された映像が物理的に正しいとは限らないので、把持の接触などは実機で確認します (経験則)。

## 写実性は本当に必要か

方策の学習が目的なら、写実性だけを追う必要はありません。ドメインランダマイゼーションと写実的な画像を組み合わせるほうが、片方だけより転移に成功しやすいという研究があります ([NVIDIA GTC 2019 の発表](https://developer.nvidia.com/gtc/2019/video/s9596) の検索要約)。この結論は 2019 年前後の研究が中心で、VLA での検証は今回確認していません。

## 未確認の項目

- Isaac Sim 6.x のカメラ露出、トーンマッピングの推奨値
- RTX Real-Time 2.0 の詳細設定
- NuRec のリライティング機能の有無
- Cosmos Transfer の必要 GPU

## FR3 本体の質感

### 原因

公式の Isaac Sim 6 用アセット [franka_simulation v0.1.0](https://github.com/frankarobotics/franka_simulation/releases) の `fr3v2_1-isaacsim6.tar.gz` を解析しました。このアセットは URDF から自動変換されたもので、質感の情報がほとんどありません。

| 項目 | 実際の値 |
|---|---|
| シェーダー | 全 20 個が `UsdPreviewSurface` |
| テクスチャ | 0 枚 |
| roughness | 全マテリアルで 0.5 |
| metallic | 全マテリアルで 0 |
| 外装の白 | `Shell_White` などの実体は `Connectors_Metal`。色は (1, 1, 1) |
| 金属部品 | 外装と同じ `Connectors_Metal`。metallic も 0 |
| 黒いコネクタ | 線形値 0.001。ほぼ完全な黒 |

外装と金属が同じマテリアルで、光沢差もムラもありません。色 1.0 は反射率 100% で、実在する白い塗装より明るい値です。設定を調整しても実物に近づかないのは、このためと考えられます。

`franka_description` の visual メッシュ (`.dae`) と MuJoCo Menagerie の `fr3.xml` も、白は `1 1 1` です。Isaac Sim 同梱の `Robots/FrankaRobotics/FrankaFR3` は未確認です。

### 修正手順

1. `fr3v2_1-isaacsim6.tar.gz` を展開し、元を残してコピーする。
2. `payloads/materials.usda` に外装、金属、黒部品のマテリアルを追加する。
3. `payloads/instances.usda` で `def Material "Shell*"` の参照先を `Connectors_Metal` から新しい外装用へ替える。金属部品 (`Connectors_Metal`、`Flange_Tie_Metal` など) も同様に分ける。
4. HDRI を当て、Path Tracing で実物の写真と並べて比較する。
5. 数値を調整し、最後に Real-Time 2.0 で確認する。

### 開始値

実測値ではありません。一般的な PBR の値に基づく開始値で、実物の写真に合わせて調整します。

| 部位 | 色 (線形) | roughness | metallic |
|---|---|---|---|
| 白い外装 | 0.75〜0.82 | 0.35〜0.5 | 0 |
| 黒、濃灰の部品 | 0.02〜0.05 | 0.4〜0.6 | 0 |
| 金属コネクタ、フランジ | 0.7〜0.8 | 0.25〜0.4 | 1 |

マテリアル名の `7016_Buttons_Logos` は RAL 7016 (アンスラサイトグレー) を示す可能性がありますが、公式の色指定は確認できていません。

### 色を実測する方法

カラーチェッカーを FR3 の横に置いて、実機カメラで撮影します。同じ位置に同じチャートを置いた Isaac Sim の画像と比べると、色と露出を照明込みで合わせられます。

### 質感を上げる追加の作業

- 外装の継ぎ目と面の違いを見せるため、roughness マップで汚れや擦れを足す。
- 手首カメラに写るフランジとハンドは、優先して作り込む。
- リンクごとの微妙な色差を残す (同じ値を全リンクに使わない)。

### 修正版アセット

`assets/fr3v2_1_realistic/` に作成しました。修正前後の比較は `renders/fr3_compare_full.png` と `renders/fr3_compare_close.png` です。

- 描画は Blender Cycles (CPU) です。Isaac Sim の RTX ではありません。
- USD の材質の割り当ては usd-core で検証しましたが、Isaac Sim で開く確認はしていません。
- 外装 8、金属 3、黒 2、濃灰 5 の材質を変更しました。
- 値を変えるだけでは、金属部は改善しますが、外装はまだ滑らかすぎます。実物らしさには roughness マップと細かな傷が必要です。

### テクスチャ版アセット

`assets/fr3v2_1_textured/` に、手続き生成の basecolor、roughness、normal と box 投影の UV を追加しました。テクスチャの繰り返しは 25cm です。

- 傷はテクスチャには入っていますが、Blender の描画ではほとんど見えません。白く明るい外装と柔らかい照明では、粗さの差が目立たないためと考えられます。
- 初回は凹凸が強すぎて革のように見えたので、normal の強さを下げました。
- 肘の同心円状の模様は修正前にもあり、メッシュのポリゴンの粗さが原因と考えられます。
- 次の手段は、実機の接写写真からマップを作ること、公式 CAD (SolidWorks) から滑らかなメッシュを作り直すこと、傷を部位ごとに手で配置することです。
- Isaac Sim では未確認です。

## Franka Hand の指

`assets/fr3v2_1_hand/` に、FR3 の link8 へ Franka Hand の見た目用メッシュを追加しました。**関節はなく、見た目だけです。** 指は開いた姿勢で固定です。比較は `renders/fr3_hand_finger_metal_compare.png` です。

- 公式 `.dae` の指本体は色 (0.90, 0.92, 0.93) だけで、金属度の情報がありません。
- 金属の色は metallic=1 のときの反射色で、見た目は周囲の映り込みで決まります。白い環境ではアルミも白く見え、環境光がないと映り込む物がなく暗くなります。
- 文献の F0: アルミ (0.913, 0.922, 0.924)、鉄 (0.562, 0.565, 0.578)、クロム (0.549, 0.556, 0.554)。
- マニュアルに指の素材の記載はありません。アルミという判断は色からの推定です。
