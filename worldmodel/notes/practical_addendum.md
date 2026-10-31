# 世界モデル実務情報：未確認事項の追補

調査基準日：2026-10-31。既存の practical.md／venues.md を読み、未確認事項の追加調査だけを記録する。数値は特記しない限り原著者・開発元の報告であり、本調査での実測・追試ではない。「未確認」は非公開・実績なしの断定ではない。

## 1. 今回埋まった項目

| 既存メモの未確認事項 | 今回確認できた内容 | 残る限界・出典 |
|---|---|---|
| UWMの学習設備 | 論文付録 -A.3：DROIDで100K gradient steps、4枚のNVIDIA A100、PyTorch DDPで24時間。表Vの分散batchは事前学習36×4、微調整36×2。 | 使用設備の報告であり最小構成ではない。A100のメモリ容量と最小VRAMは未確認。[原論文HTML・付録](https://arxiv.org/html/2504.02792v3#A1) |
| DreamZero-AgiBot重みの条件 | 公式リポジトリからたどったHugging Face配布ページに `License: apache-2.0` の表示。 | 「配布ページのライセンス表示を確認」に更新できる。ただし本文は空で、個別の追加条項・来歴の詳細は未確認。DROID重みの条件をAgiBotへ転用しない。[配布ページ](https://huggingface.co/GEAR-Dreams/DreamZero-AgiBot)、[公式リンク元](https://github.com/dreamzero0/dreamzero) |
| Cosmos 3の実行設備 | Edgeモデルカードに、単一GPU／単一統合プラットフォーム、batch 1での推論表あり。推奨機種だけでなく実行報告まで確認できた。 | 最小VRAMは未確認。詳細は次節。[NVIDIAモデルカード・PBR](https://huggingface.co/nvidia/Cosmos3-Edge#pbr-performance-benchmark-reporting) |
| World Labsの実機評価 | R2S2R記事に実ロボットでの稼働と評価の試行数を記載。 | ベンダー自己申告であり独立追試ではない。詳細は第4節。[公式記事](https://www.worldlabs.ai/blog/real-to-sim-to-real) |
| CoRL 2026の個別世界モデル論文 | MoREとSafeDojoの著者側の採択表示を確認。 | 会議公式一覧の本文・個別decisionの直接取得には制限が残る。採択根拠の強さを第5節に明記。[MoRE著者ページ](https://stevenlsw.github.io/)、[SafeDojo著者ページ](https://easonai-5589.github.io/projects/safedojo/) |

## 2. 最小VRAM：実行報告と下限を分離

今回確認した範囲では、次表の未確認欄を「最小○GB」という値で埋められる根拠は得られなかった。モデル重みのファイルサイズやGPU製品の搭載メモリを、そのままピーク使用量に読み替えていない。

| 実装 | 今回の追加確認・判断 | 学習／推論の最小VRAM |
|---|---|---|
| DreamerV3 | 著者リポジトリはOOM切り分けに `--batch_size 1` を案内。Issue #152ではメモリ不足が最終的にreplay bufferによるホストRAM不足と報告されており、VRAM下限の証拠にはならない。[実装](https://github.com/danijar/dreamerv3)、[Issue](https://github.com/danijar/dreamerv3/issues/152) | 両方未確認。 |
| Dreamer 4 | 公式プロジェクトと論文HTMLから、GPUメモリ量付きの再現手順を確認できず。[公式](https://danijar.com/project/dreamer4/)、[論文HTML](https://arxiv.org/html/2509.24527v1) | 両方未確認。 |
| TD-MPC2 | 既存メモの推奨条件を今回「実測された最小値」へ格上げする追加根拠は得られず。[公式要件](https://github.com/nicklashansen/tdmpc2) | 既存の推奨値と、最小値の未確認を維持。 |
| V-JEPA 2／2-AC | 公式手順はGPUメモリに応じたbatch調整を案内。論文付録E.2の128 H100、E.3の512 H100はVQA用のLLMとの学習実験であり、2-AC推論の要件ではない。[実装](https://github.com/facebookresearch/vjepa2)、[原論文付録E](https://arxiv.org/html/2506.09985v1#A5) | 両方未確認。全事前学習・VQA学習・AC追加学習・計画推論を分ける。 |
| DINO-WM | 公式Issue #23にA100、48GBのGPUでの計画中OOMの利用者報告と、設定を変えたRTX 4060の簡単なwall事例の成功報告が併存する。GPU機種だけで必要量を決められない。著者の最低保証ではなく第三者利用者の報告。[Issue #23](https://github.com/gaoyuezhou/dino_wm/issues/23) | 両方未確認。4060のVRAM容量は当該投稿で未確認。 |
| UWM | 4 A100でのDROID事前学習設備は判明。使用したGPUの容量と推論ピークメモリは未確認。[論文付録 -A.3](https://arxiv.org/html/2504.02792v3) | 両方未確認。 |
| Cosmos 3 Edge | PBRにJetson T2000 16GBで画像→動画101.20秒の報告。ただし448×256、189フレーム、warm-runで、他機種の480p測定と条件が異なる。T3000 32GBではDROID policy 8.63秒の報告。いずれもNVIDIA自己申告。[Edgeモデルカード](https://huggingface.co/nvidia/Cosmos3-Edge) | 未確認。Jetsonの記載容量は統合プラットフォームの容量であり、専用VRAMの最低必要量とは扱わない。 |
| Cosmos 3 Super／Nano | 公式モデルカードまで確認。Edgeの小容量機種での結果を他モデルへ外挿しない。[Super](https://huggingface.co/nvidia/Cosmos3-Super)、[Nano](https://huggingface.co/nvidia/Cosmos3-Nano) | 両方未確認。 |
| DreamZero | 既存メモの分散推論GPU枚数から、1枚当たりの最低VRAMを導ける追加根拠は得られず。[公式要件](https://github.com/dreamzero0/dreamzero) | 両方未確認。 |
| Genie／GAIA | 公開ページからローカル実行の最低メモリ量を確認できず。[Genie](https://deepmind.google/models/genie/)、[GAIA-4](https://wayve.ai/thinking/gaia-4/) | 両方未確認。 |

Cosmos 3 Edgeの `--enable-layerwise-offload` はメモリ削減手段として公式カードに記載されているが、下限値の提示ではない。画像→動画の生成時間やpolicyのaction chunk生成時間を、ロボットの制御周期・閉ループ全体の遅延へ換算する根拠も未確認。[Edge実行案内・測定注記](https://huggingface.co/nvidia/Cosmos3-Edge)

## 3. Dreamer 4／Cosmos 3：重み公開とライセンスの確認深度

### Dreamer 4

公式プロジェクトだけでなく著者の研究一覧も照合した。DreamerV3にはCodeリンクがある一方、Dreamer 4の項目にはPaper／Twitterリンクがあり、今回確認した公式導線にはコード・checkpoint・そのライセンスの案内を見つけられなかった。したがって、公式コード、重み、重みライセンス、会議採択は引き続き**未確認**であり、「非公開が確定」とはしない。[著者研究一覧](https://danijar.com/)、[公式プロジェクト](https://danijar.com/project/dreamer4/)

実機に関する追加の区別：公式ページの「Real World Video」はロボットデータセット上での世界モデルの反実仮想生成である。これをDreamer 4の実ロボット閉ループ制御成功の根拠にはできない。実機制御実績は引き続き未確認。[該当セクション](https://danijar.com/project/dreamer4/#real-world-video)

### Cosmos 3

公式ドキュメントのリンク先として、Super／Nano／Edgeの各NVIDIAモデルカードを実際に確認した。Nano-Policy-DROIDもモデルカードとFiles一覧を確認し、一覧には `model.safetensors.index.json` 等が掲載されている。これは配布先・ファイル一覧の確認であり、重み本体の取得・整合性確認・実行確認ではない。[公式モデル参照](https://docs.nvidia.com/cosmos/latest/cosmos3/model_reference.html)、[Super](https://huggingface.co/nvidia/Cosmos3-Super)、[Nano](https://huggingface.co/nvidia/Cosmos3-Nano)、[Edge](https://huggingface.co/nvidia/Cosmos3-Edge)、[DROID Files一覧](https://huggingface.co/nvidia/Cosmos3-Nano-Policy-DROID/tree/main)

追加の実務条件は**gated配布**である。公式InstallationはHugging Faceでのアクセス申請とRead権限tokenによる認証を要求する。公開カードの閲覧と、誰でも即時に重みを取得できることを区別する。公式のコード・モデル条件はOpenMDW-1.1で、Nano-Policy-DROIDカードも同じ表示と商用／非商用利用可の説明を持つ。第三者依存物は別ライセンスである。[Installation](https://docs.nvidia.com/cosmos/latest/cosmos3/installation.html)、[License](https://docs.nvidia.com/cosmos/latest/license.html)、[DROIDモデルカード](https://huggingface.co/nvidia/Cosmos3-Nano-Policy-DROID)

DROIDカードのQuickstartで示されるRoboLabはシミュレーションbenchmarkである。サーバが実機クライアントにもactionを送れるという説明だけから、実機試行数・成功率を補わない。RoboArena順位はNVIDIAカード内の自己申告であり、独立評価主体の個別試行ログとの照合は未確認。[DROID評価・Quickstart](https://huggingface.co/nvidia/Cosmos3-Nano-Policy-DROID)

## 4. 実機評価と企業公式情報の追加確認

| 対象 | 今回補足できる根拠 | 未確認・解釈上の境界 |
|---|---|---|
| UWM | 付録 -C：Franka Panda、外部カメラ2台＋手首カメラ、制御10Hz。通常4タスクは50初期条件、Rice-Cookerは20初期条件。各初期条件に3回の試行機会。Rice-CookerはOOD評価を行わない。[原論文付録](https://arxiv.org/html/2504.02792v3) | 成功率を読む際には「初期条件数」と「attempt数」を区別する。著者報告であり、本調査の独立追試は未実施。コード／重みの明示ライセンスは今回も未確認。[実装](https://github.com/WEIRDLabUW/unified-world-model) |
| AMI Labs | 公式サイトを再確認したが、公開checkpoint、モデルカード、GPU要件、定量的な実機benchmarkへ進める導線は今回確認できなかった。 | 未確認を維持。open publications／open sourceへの方針表明は、特定モデルのリリース済み状態やライセンスの証拠にはならない。[公式サイト](https://amilabs.xyz/) |
| World Labs・Atlas | Atlas発表ページにearly access申請導線がある。 | early access案内は確認できたが、Atlasのダウンロード可能な学習コード・重み・重みライセンス・最小VRAMは未確認。MarbleやWorld APIの提供と区別する。[Atlas公式発表](https://www.worldlabs.ai/blog/atlas) |
| World Labs・R2S2R | RB-Y1の電源コード操作、YAMのケーブル操作、Flexivの試験管移送、xArmの物体取り分けについて、それぞれ1時間介入なしの稼働を報告。ALOHAのcube handover評価はcheckpointごとにシミュレーション2,000試行（ID／OOD各1,000）、実機100試行（各50）。 | **ベンダー自己申告**。policyが実機学習データなしで学習されたとの説明と、シーン再構成に実世界観測を使うR2S2Rの工程を区別する。生ログ、独立追試、Atlasそのものが当該全実験を実装するとの対応づけは未確認。[公式実機報告](https://www.worldlabs.ai/blog/real-to-sim-to-real) |
| Wayve・GAIA-4 | 公式記事はworld-on-railsでは自車だけを変化させ、他の道路利用者はログ軌跡を維持して自車へ反応しないと説明。reactive agentsはこの制約を緩める追加モード。カメラとradarの生成、路上とシミュレーションの軌跡照合を説明する。 | **ベンダー自己申告**。GAIAはAI Driverを評価するシミュレータであり、生成世界での反実仮想成功を実走成功と数えない。公式checkpoint／重みライセンス／最小VRAM、公開された実機試行の分母は今回も未確認。[GAIA-4原文](https://wayve.ai/thinking/gaia-4/) |

既存メモで実機実績が未確認だったDreamerV3、TD-MPC2、DINO-WMについて、今回の再確認だけで原論文・当該公式実装の実機成功を新たに確定できる根拠は得られなかった。派生実装や別世代の結果を移し替えていない。[DreamerV3](https://github.com/danijar/dreamerv3)、[TD-MPC2](https://github.com/nicklashansen/tdmpc2)、[DINO-WM](https://dino-wm.github.io/)

## 5. ICRA／IROS／CoRL 2026の追加候補と採択根拠

以下は既存のWorldPlanner等を繰り返さない追加分。会議主催者の一次情報、著者による一次情報、取得できなかった個別decisionを分ける。

| 会議・論文 | 確認できたこと | 採択・実機に関する限界 |
|---|---|---|
| ICRA 2026：OccLLaMA: A Unified Occupancy-Language-Action World Model for Understanding and Generation Tasks in Autonomous Driving | 著者プロジェクトに `Accepted by ICRA 2026`。占有表現・言語・行動を統合する世界モデル。[著者ページ](https://vilonge.github.io/OccLLaMA_Page/) | 著者による採択申告まで。会議主催者の個別proceedings照合と実車閉ループ評価は未確認。arXiv版の題名は異なる。[arXiv個別ページ](https://arxiv.org/abs/2409.03272) |
| IROS 2026：ImagiNav: Scalable Embodied Navigation via Generative Visual Prediction and Inverse Dynamics | 共著者の2026-06-18付採択告知、プロジェクトのIROS 2026表記・BibTeX、arXiv個別ページを照合。[共著者告知](https://yizhuo-wang.com/news/)、[プロジェクト](https://j1dan.github.io/ImagiNav/)、[arXiv](https://arxiv.org/abs/2603.13833) | 本会議採択の著者申告。公式proceedingsの個別照合は未確認。Unitree H1／VLN-PEの結果はシミュレーション評価であり、実機歩行成功率とは扱わない。[論文実験節](https://arxiv.org/html/2603.13833v2) |
| CoRL 2026：MoRE: Mixture-of-Experts for Multi-Physics Robotic World Models | 著者の研究一覧・プロジェクトにCoRL 2026 Spotlight。OpenReviewの検索索引にも同表示。物理レジームごとのmotion expertを持つ3D世界モデルで、実機MPC例を掲載。[著者研究一覧](https://stevenlsw.github.io/)、[実験ページ](https://alwaysleepy.github.io/MoRE-WM-site/)、[OpenReview検索](https://openreview.net/search?content=authors&group=all&sort=cdate%3Adesc&source=forum&term=~Albert_J._Zhai1) | 著者一次情報と投稿基盤の検索表示まで確認。OpenReview個別本文はブラウザ検証画面で取得不可。arXiv ID、実機試行の分母、最小VRAMは未確認。Spotlightを受賞と書かない。 |
| CoRL 2026：SafeDojo: Safe Reinforcement Learning for VLA via Interactive World Model | 著者ページに `CoRL 2026 · Accepted`。OpenReview検索索引にCoRL 2026 Poster。想像内の安全RLと実機Frankaの5タスク評価を報告。[著者ページ](https://easonai-5589.github.io/projects/safedojo/)、[OpenReview検索](https://openreview.net/search?content=authors&group=all&sort=cdate%3Adesc&source=forum&term=~Chun-Kai_Fan1)、[論文個別ページ](https://arxiv.org/abs/2606.20698) | 個別decisionの直接取得と公開code URLは未確認。実機優位性は原著者報告。 |
| IROS 2026 PWMS workshop：Learning Versatile Humanoid Manipulation with Touch Dreaming／Toward Physically Grounded JEPA World Models for Goal-Conditioned Robotic Planning | 主催者のAccepted Papersに掲載。前者はOral、後者はPoster。[主催者採択一覧](https://physical-world-models.github.io/IROS2026/#accepted-papers) | **non-archival workshop**で、主催者はIROS proceedingsに載らないと明記。本会議採択へ格上げしない。各論文のID・実機数値は未確認。 |

CoRL公式Accepted Papersページは今回も埋め込み一覧の本文が取得できなかった。この制約は「個別世界モデル論文が存在しない」ことを意味しない。上記候補の採択根拠は行ごとに示した範囲に限定する。[公式一覧](https://2026.corl.org/program/accepted-papers)

## 6. 論文候補・指定9列TSV

書き込み許可先が本Markdownだけのため、既存の candidates.tsv は変更せず、取り込み用TSVをここに埋め込む。`未確認`は欠損値。PDF URLはページ上のリンク先の確認であり、ローカル保存・ファイル整合性検証は行っていない。yearは会議年であり、arXiv初稿年とは異なることがある。

```tsv
title	year	venue	status	arxiv_id	pdf_url	code_url	topic	verify_url
OccLLaMA: A Unified Occupancy-Language-Action World Model for Understanding and Generation Tasks in Autonomous Driving	2026	ICRA	本会議採択の著者申告; 主催者個別照合未確認; arXiv版題名差あり	2409.03272	未確認	未確認	自動運転・占有表現・言語・行動	https://vilonge.github.io/OccLLaMA_Page/
ImagiNav: Scalable Embodied Navigation via Generative Visual Prediction and Inverse Dynamics	2026	IROS	本会議採択の著者申告; 主催者個別照合未確認	2603.13833	https://arxiv.org/pdf/2603.13833	https://github.com/J1dan/ImagiNav-release	生成視覚計画・逆動力学・ナビゲーション	https://j1dan.github.io/ImagiNav/
MoRE: Mixture-of-Experts for Multi-Physics Robotic World Models	2026	CoRL	著者一次情報とOpenReview検索でSpotlight表示; 個別decision直接取得未確認	未確認	https://alwaysleepy.github.io/MoRE-WM-site/assets/MoRE_CoRL2026.pdf	https://github.com/AlwaySleepy/MoRE-WM	3D世界モデル・混合専門家・実機MPC	https://alwaysleepy.github.io/MoRE-WM-site/
SafeDojo: Safe Reinforcement Learning for VLA via Interactive World Model	2026	CoRL	著者一次情報で採択申告; OpenReview検索でPoster表示; 個別decision直接取得未確認	2606.20698	https://arxiv.org/pdf/2606.20698	未確認	対話動画世界モデル・安全強化学習・Franka	https://easonai-5589.github.io/projects/safedojo/
Learning Versatile Humanoid Manipulation with Touch Dreaming	2026	IROS PWMS workshop	主催者一覧でOral掲載; non-archival; 本会議採択ではない	未確認	未確認	未確認	触覚・世界モデル・ヒューマノイド操作	https://physical-world-models.github.io/IROS2026/
Toward Physically Grounded JEPA World Models for Goal-Conditioned Robotic Planning	2026	IROS PWMS workshop	主催者一覧でPoster掲載; non-archival; 本会議採択ではない	未確認	未確認	未確認	JEPA・物理・ゴール条件付き計画	https://physical-world-models.github.io/IROS2026/
```

## 7. 作業記録と残る未確認

- 作成したファイルは本Markdownのみ。既存notes、PDF、README.md、_catalog.csv、docs/には書き込んでいない。モデル・コードのダウンロード／実行、GPU実測、実機追試は行っていない。arXiv APIとOpenAlex APIは利用していない。
- PDFリンク確認時にWeb閲覧ツールがMoRE／ImagiNavのPDF本文を取得し、SafeDojoのPDF取得はエラーになった。PDFダウンロード禁止の指示に対し、この操作は不適切だった。ローカルファイル保存はしていない。その後の確認はHTML・モデルカードを用いた。
- 優先して残る項目：Dreamer 4の公式checkpointとライセンス、AMI Labsの具体的モデル配布、Atlasの重み配布、GAIAのローカル実行条件、各実装の条件付きpeak VRAM、CoRL個別decisionとICRA／IROSの個別proceedings照合。上記各節のURLが今回確認した範囲であり、未取得の内容は補完していない。
