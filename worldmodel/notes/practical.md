# 世界モデルの実務情報

調査基準日：2026-10-31。一次情報の公開ページを照合した調査メモ。コード・重みのダウンロード、実行、GPU測定、実機追試は行っていない。「未確認」は非公開の断定ではなく、本調査で確認できなかった項目を表す。性能値は特記がなくても原著者／開発元の報告であり、独立追試の結果ではない。

## 公開実装・重み・ライセンス・GPU

GPU欄では学習と推論を区別する。数値がない項目の最小VRAMは未確認。コードのライセンスを、重みや学習データのライセンスへ自動的に適用しない。

| モデル | 実装・重みの確認結果 | ライセンス | GPU・実行条件 | 実機での根拠 |
|---|---|---|---|---|
| DreamerV3 | 著者の[JAX再実装](https://github.com/danijar/dreamerv3)。同リポジトリはGoogle／DeepMindとは無関係な再実装と明記。配布済みの汎用事前学習重みは未確認。 | [コードはMIT](https://github.com/danijar/dreamerv3/blob/main/LICENSE)。重みの個別条件は未確認。 | 既定はGPU、CPU／TPU切替も記載。最小VRAM未確認。Linux／Macでのテストを記載し、Windowsネイティブ対応は未確認。[実行案内](https://github.com/danijar/dreamerv3) | 原論文の主評価はゲーム・制御ベンチマーク。これ自体を実機汎用ロボットでの実証と扱わない。[Nature論文](https://doi.org/10.1038/s41586-025-08744-2) |
| Dreamer 4 | [公式プロジェクト](https://danijar.com/project/dreamer4/)と[論文](https://arxiv.org/abs/2509.24527)を確認。公式コード・重みは未確認。[lucidrains実装](https://github.com/lucidrains/dreamer4)は第三者実装。 | 公式コード／重みのライセンス未確認。第三者実装を公式配布物と混同しない。[公式ページ](https://danijar.com/project/dreamer4/) | 世界モデルの対話的推論は単一GPUと原著者が報告。これは学習全体の必要GPU数や最小VRAMを意味しない。[論文](https://arxiv.org/abs/2509.24527) | Minecraftのオフライン学習を実証。ロボット適用は動機であり、このページでの実機制御実績は未確認。[公式ページ](https://danijar.com/project/dreamer4/) |
| TD-MPC2 | [公式PyTorch実装](https://github.com/nicklashansen/tdmpc2)。単一タスク・複数タスクのチェックポイントへのリンクあり。 | [コードMIT](https://github.com/nicklashansen/tdmpc2/blob/main/LICENSE)。外部依存は別条件。重み専用の独立ライセンスは未確認。[配布案内](https://github.com/nicklashansen/tdmpc2) | 単一タスク学習／配布モデル評価はVRAM 8 GB以上を推奨。317Mモデル学習は24 GB以上が必要と記載。ホストRAMは単一タスク12 GB以上、80タスクオフライン学習128 GB。GPU VRAMと混同しない。[公式要件](https://github.com/nicklashansen/tdmpc2) | 公開評価の中心はDMControl、Meta-World、ManiSkill2、MyoSuite。これらの結果をそのまま実機成功率へ換算しない。[実装](https://github.com/nicklashansen/tdmpc2) |
| V-JEPA 2／2-AC | [公式実装・encoder／AC predictor重み](https://github.com/facebookresearch/vjepa2)。画像・動画表現のencoderと、行動条件付き2-ACを区別。 | コードの大部分MIT、一部Apache 2.0。[コード条件](https://github.com/facebookresearch/vjepa2#license)。[HFのViT-g encoder](https://huggingface.co/facebook/vjepa2-vitg-fpc64-256/tree/main)はApache 2.0。AC重みの独立条件は未確認。 | CUDAを推奨、GPUメモリに応じたバッチ調整を案内。最小VRAMと全事前学習の設備要件は未確認。[実装](https://github.com/facebookresearch/vjepa2) | 2-ACはDROIDの62時間未満のロボット動画でpost-training、異なる2研究室のFrankaアームで画像ゴールに対するpick-and-placeを報告。評価先でのデータ収集・タスク固有学習なしという範囲のzero-shot。[Meta原著者説明](https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/) |
| DINO-WM | [公式実装](https://github.com/gaoyuezhou/dino_wm)。PointMaze／PushT／Wallの学習済み重みをOSFへ公開したとの案内あり。OSF実体の閲覧は403で未確認。 | コードMIT。DINOv2と配布checkpointの条件は別途照合が必要で、重み独立条件は未確認。[実装](https://github.com/gaoyuezhou/dino_wm) | MuJoCo、変形物体にはPyFlexの導入手順あり。最小VRAM／学習GPU機種は未確認。[実装](https://github.com/gaoyuezhou/dino_wm) | 原論文の6環境は主にシミュレーション。実機実績は本調査では未確認。[論文・実験](https://dino-wm.github.io/) |
| UWM（Unified World Models） | [公式実装](https://github.com/WEIRDLabUW/unified-world-model)。LIBERO-90、DROID事前学習／co-training重みのDriveリンクあり。配布ファイル自体は未検証。 | 確認したリポジトリで明示的なコード／重みライセンスを確認できず、未確認。公開閲覧可能という理由で商用利用可とはしない。[リポジトリ](https://github.com/WEIRDLabUW/unified-world-model) | 最小VRAM／学習設備は確認した実行案内では未確認。[実装](https://github.com/WEIRDLabUW/unified-world-model) | DROID事前学習後、実機で器の積み重ね、キャビネット、タオル、炊飯器などを評価。照明・背景・clutterのOOD条件あり。[実験ページ](https://weirdlabuw.github.io/uwm/) |
| Cosmos 3 | [NVIDIA実装](https://github.com/NVIDIA/Cosmos)と[公式モデル一覧](https://docs.nvidia.com/cosmos/latest/cosmos3/model_reference.html)。Super／Nano／EdgeとDROID policy派生を確認。 | コード・モデルは[OpenMDW-1.1](https://docs.nvidia.com/cosmos/latest/license.html)。従来世代のNVIDIA Open Model条件と一括扱いしない。 | 推奨：SuperはH200／B200／GB200、NanoはRTX PRO 6000／H100／B200、EdgeはJetson AGX Orin／Thor／RTX PRO 6000。これは機種の推奨表であり、GPU枚数・最小VRAM・学習要件は未確認。[2026-10-30更新のModel Matrix](https://docs.nvidia.com/cosmos/latest/cosmos3/model_matrix.html) | DROID policy重みがあることと、任意ロボットでの性能保証は別。公式発表のRoboArena等の優位性はベンダー自己申告。独立した実機追試は未確認。[モデル一覧](https://docs.nvidia.com/cosmos/latest/cosmos3/model_reference.html)、[発表](https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai/) |
| Genieシリーズ | Genie 1の[ICML論文](https://proceedings.mlr.press/v235/bruce24a.html)、[Genie 2](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/)、[Genie 3](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)、[Genie 4発表](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/)を確認。公式の学習コード・重みは未確認。 | 配布重みのライセンス未確認。Genie 4はtrusted testers向けresearch previewという公式説明。[発表](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/) | ローカル実行の必要GPU／VRAM未確認。Genie 3の720p・24 fpsは開発元のサービス実証値で、手元GPUの保証値ではない。[Genie 3](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) | 仮想世界・SIMAでのエージェント評価を、実ロボットの制御実験と同一視しない。[Genie 3](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) |
| GAIAシリーズ | Wayveの[GAIA-2](https://wayve.ai/thinking/gaia-2/)、[GAIA-3](https://wayve.ai/thinking/gaia-3/)、[GAIA-4](https://wayve.ai/thinking/gaia-4/)を確認。一般配布の公式学習コード・重みは未確認。 | 重み配布ライセンス未確認。[GAIA-4](https://wayve.ai/thinking/gaia-4/) | ローカル最小GPU／VRAM未確認。[GAIA-4](https://wayve.ai/thinking/gaia-4/) | 自動運転の学習・評価・閉ループシミュレーションが対象。GAIAそのものの路上運転政策としての成功率は未確認。[GAIA-3](https://wayve.ai/thinking/gaia-3/)、[GAIA-4](https://wayve.ai/thinking/gaia-4/) |
| DreamZero | [公式コード](https://github.com/dreamzero0/dreamzero)、[DROID重み](https://huggingface.co/GEAR-Dreams/DreamZero-DROID)、AgiBot重みへの公式リンクあり。 | コードApache 2.0。[DROID重みはCC BY-NC 4.0](https://huggingface.co/GEAR-Dreams/DreamZero-DROID)。AgiBot重みの条件は未確認。 | 公式分散推論は最低2 GPU、GB200／H100でテスト。学習に同じ条件が十分かは未確認。最小VRAM未確認。[要件](https://github.com/dreamzero0/dreamzero) | 実ロボットで未見タスク・環境とembodiment移行を原著者が評価。[原論文](https://arxiv.org/abs/2602.15922)。公開サーバのH100等の遅延と、論文の制御周波数は同一条件と仮定しない。 |

## 選び方（調査に基づく実務上の提案）

- 最小構成でモデルベース制御を再現する入口には、要件が明示されたTD-MPC2を候補にする。画像ゴールと潜在空間MPCを調べるならDINO-WM、Frankaでの転移計画を調べるならV-JEPA 2-ACを比較する。[TD-MPC2](https://github.com/nicklashansen/tdmpc2)、[DINO-WM](https://dino-wm.github.io/)、[V-JEPA 2-AC](https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/)
- 動画と行動の共同学習にはUWMとDreamZeroを候補にする。UWMの利用条件は未確認、DreamZero-DROID重みは非商用条件なので、実装選定前に配布物単位で確認する。[UWM](https://github.com/WEIRDLabUW/unified-world-model)、[DreamZero重み](https://huggingface.co/GEAR-Dreams/DreamZero-DROID)
- 大規模な生成・合成データ基盤にはCosmos 3を候補にする。Genie／GAIAは公式発表が豊富でも、今回確認できた情報からローカル再現可能とは判断しない。[Cosmos](https://docs.nvidia.com/cosmos/latest/cosmos3/model_matrix.html)、[Genie](https://deepmind.google/models/genie/)、[GAIA-4](https://wayve.ai/thinking/gaia-4/)

## World Action Model（WAM）の定義

NVIDIAの用語集ではWAMは「世界がどう変化するか」と「その変化を起こすロボット行動」を共に学習するモデルを指す。DreamZeroは事前学習済み動画拡散モデルを基盤として未来の動画と行動を共同予測する代表例。これは開発元の定義であり、全研究分野で統一された標準規格と確認したものではない。[NVIDIA定義](https://www.nvidia.com/en-us/glossary/world-action-model/)、[DreamZero原論文](https://arxiv.org/abs/2602.15922)

本メモでは、(a) 行動を入力して未来状態を予測するforward world model、(b) 観測・指示から行動を出すpolicy、(c) 動画と行動を結合して両者を扱えるWAMを実務上区別する。UWMは独立した拡散時刻によってpolicy／forward dynamics／inverse dynamics／video predictionを同じモデルで表し、WAM系設計を比較する好例となる。一方、DreamerやTD-MPC2は世界モデルと行動学習・探索を組み合わせるが、共同動画・行動生成器と同じ構造ではない。[UWM](https://weirdlabuw.github.io/uwm/)、[DreamerV3](https://github.com/danijar/dreamerv3)、[TD-MPC2](https://github.com/nicklashansen/tdmpc2)

2026年10月の候補にはVPP2もある。動画予測の事前学習と行動モジュールを結合するWAMと原著者が位置づける。プレプリントの実機優位性は原著者報告で、採択・独立追試は未確認。[論文](https://arxiv.org/abs/2610.10270)、[公開実装](https://github.com/roboterax/video-prediction-policy-2)

## ベンチマークと評価指標

| 評価する能力 | ベンチマーク／指標 | 実務で読む際の条件・限界 |
|---|---|---|
| 閉ループ制御とサンプル効率 | Dreamerの各ドメイン得点、TD-MPC2のDMControl／Meta-World等のreturn・成功率。[Dreamer論文](https://doi.org/10.1038/s41586-025-08744-2)、[TD-MPC2](https://github.com/nicklashansen/tdmpc2) | 環境、観測種、実環境interaction数、training ratio、seed数を揃えるという比較方針を推奨。ドメイン間で生のreturnを平均しない。 |
| 動画予測が計画に役立つか | VP²：モデル予測制御を介したロボット操作。知覚画質指標だけでは実行成功を予測できないことを原著者が報告。[プロジェクト](https://s-tian.github.io/projects/vp2/)、[実装](https://github.com/s-tian/vp2) | 動画のFVD／LPIPS／SSIMと閉ループ成功率を併記する。VP²とVideo Prediction Policy 2（VPP2）は別物。[VP²論文](https://arxiv.org/abs/2304.13723)、[VPP2](https://arxiv.org/abs/2610.10270) |
| 潜在空間の計画 | DINO-WMの画像ゴール到達、UWMのLIBERO／実機ID・OOD評価。[DINO-WM](https://dino-wm.github.io/)、[UWM](https://weirdlabuw.github.io/uwm/) | タスク成功率、ゴール距離、horizon、MPCの再計画頻度を記録する方針を推奨。予測誤差が小さいことだけで任意の行動分布を保証しない。 |
| 表現・動画理解 | Something-Something v2のtop-1 accuracy、EPIC-KITCHENS-100のrecall@5等。[V-JEPA 2論文](https://arxiv.org/abs/2506.09985) | 動画理解用encoderの得点をロボット制御成功率として扱わない。AC predictor・planner・評価タスクを別に記録する。 |
| 物理的一貫性 | Physics-IQ／Physics-IQ Verified：実写の物理現象を用いた評価。[公式実装](https://github.com/google-deepmind/physics-IQ-benchmark) | OriginalとVerified、入力形式、prompt最適化、best-of-N、評価日を分離する。ランキングの更新値をモデル固有の不変値として引用しない。 |
| 世界生成・カメラ制御 | WorldScore：controllability／quality／dynamics。[ICCV 2025論文](https://openaccess.thecvf.com/content/ICCV2025/html/Duan_WorldScore_A_Unified_Evaluation_Benchmark_for_World_Generation_ICCV_2025_paper.html) | 3D／4D／動画生成を比較する評価。ロボット行動の実行可能性や接触力の正確さを直接検証する指標とはしない。 |
| 行動条件の遵守 | 車両動作の生成誤差、物体操作の制御性。GEMはCOM（Control of Object Manipulation）指標を導入。[GEM](https://openaccess.thecvf.com/content/CVPR2025/html/Hassan_GEM_A_Generalizable_Ego-Vision_Multimodal_World_Model_for_Fine-Grained_Ego-Motion_CVPR_2025_paper.html)、[GAIA-3](https://wayve.ai/thinking/gaia-3/) | 同じ初期状態から異なる行動で反実仮想を生成し、画質と行動応答を別々に記録する方針を推奨。 |
| 実ロボットでの有用性 | タスク成功率、未見環境、embodiment移行。[V-JEPA 2-AC](https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/)、[DreamZero](https://arxiv.org/abs/2602.15922) | 成功条件、試行数、介入、reset、評価先の学習データ利用、制御周期を報告する方針を推奨。デモ動画だけから率を推計しない。 |

比較表を作る場合の推奨記録項目：checkpointの版、code commit、データ範囲、ロボット／カメラ／action表現、精度、解像度、rollout長、候補数、sampling steps、GPU機種・枚数、peak VRAM、モデル推論時間と計画全体の時間、実機試行の分母。これは本調査の再現性向上の提案であり、未測定値を補うものではない。

## 企業動向：一次情報で確認できた範囲

| 企業 | 確認できた方向性・発表 | 公開性・解釈 |
|---|---|---|
| AMI Labs | 抽象表現空間でセンサ情報の未来を予測し、行動条件付き世界モデルで計画する方針。産業制御、ロボット、医療等を対象に挙げる。[公式サイト](https://amilabs.xyz/) | 具体的な公開checkpoint、GPU要件、実機ベンチマークは未確認。検索で現れる類似名サイトを同一企業とみなさない。 |
| World Labs | Atlasを2026-09-01に発表。text／image／video／3Dを扱うomni world modelと説明。2026-09-28にAMD参加を発表。[Atlas](https://www.worldlabs.ai/blog/atlas)、[AMD発表](https://www.worldlabs.ai/blog/amd-announcement) | Atlasの学習コード・重み・利用ライセンスは未確認。参加発表を法的買収完了の確認とはしない。ロボット向けR2S2Rについての公式記事もある。[記事一覧](https://www.worldlabs.ai/blog) |
| Wayve | GAIA-2の多視点・条件制御からGAIA-3の評価用途へ、2026-08-03のGAIA-4ではAI Driverを閉ループに入れる方向へ展開。[GAIA-2](https://wayve.ai/thinking/gaia-2/)、[GAIA-3](https://wayve.ai/thinking/gaia-3/)、[GAIA-4](https://wayve.ai/thinking/gaia-4/) | 安全性や評価上の有効性は開発元の主張。生成シミュレーションの説明から路上安全認証の取得を推定しない。 |
| Runway | 2025-12-11のGWM-1はGen-4.5を基盤としたWorlds／Avatars／Robotics。Roboticsは行動条件付きrollout、合成データ、policy評価を用途として提示。[公式発表](https://runwayml.com/research/introducing-runway-gwm-1/) | SDK／APIのアクセス案内と一般公開重みは別。公開checkpoint・ローカルGPU要件・独立した実機性能は未確認。 |
| Google DeepMind | Genie 2／3に続き、2026-10-27にGenie 4を発表。音声を含む対話世界のresearch preview。[Genie 2](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/)、[Genie 3](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)、[Genie 4](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/) | 基準日時点のGenie 4はtrusted testers向け。将来のconsumer／developer展開計画と一般提供済みの状態を区別する。 |

## 日本の研究・日本語資料

| 資料・研究 | 確認内容と使い方 |
|---|---|
| 慶應義塾大学・藤井健太朗／村田真悟、JSAI 2025 | 「時間的階層性を持つ世界モデルを用いた深層能動的推論による実ロボット制御」。世界モデル、抽象行動モデル、抽象世界モデルを組み合わせ、不確実性下の実機物体操作を報告。公開実装・重み・GPUは未確認。[学会原文](https://www.jstage.jst.go.jp/article/pjsai/JSAI2025/0/JSAI2025_1B3OS41a01/_article/-char/ja) |
| 慶應義塾大学・太田衛／藤井健太朗／村田真悟、JSAI 2026 | 「時間的階層性を持つマルチモーダル世界モデル」。視覚・触覚、情報欠損と長期文脈を扱う。MoPoEとMTRSSMを統合。公開実装・重みは未確認。[学会原文](https://www.jstage.jst.go.jp/article/pjsai/JSAI2026/0/JSAI2026_1E3OS39a02/_article/-char/ja) |
| JDERW、JSAI 2025 | 日本語LLMの世界理解を要する演繹推論の研究。動画世界モデルや実機制御の直接ベンチマークとは分けて読む。[学会原文](https://www.jstage.jst.go.jp/article/pjsai/JSAI2025/0/JSAI2025_1B5OS41c04/_article/-char/en) |
| 東京大学「世界モデルとシミュレータ寄付講座」 | 日本語の研究・講義の入口。記載された設置期間は2021-07-01〜2026-06-30であり、現在も同じ形で継続と推定しない。[公式サイト](https://world-model.t.u-tokyo.ac.jp/) |
| 東京大学「世界モデル2026」／Physical AI応用編 | 大学公式の日本語講座案内。募集情報の公開と教材の一般公開は別で、講義資料一式の一般配布は未確認。[世界モデル2026](https://www.u-tokyo.ac.jp/focus/ja/events/z0104_02240.html)、[Physical AI](https://www.u-tokyo.ac.jp/focus/ja/events/z0104_02200.html) |
| Toyota Research Instituteを含む共同研究 | UWMの著者所属にはTRIが含まれる。ただし米国拠点を含む共同研究であり、日本国内だけの研究と数えない。[著者所属・実験](https://weirdlabuw.github.io/uwm/) |

## 確認の限界

ライセンス法務判断、全モデルの重み実体・checksum、学習再現、GPU実測は未実施。GPU未確認欄はパラメータ数からの推測値で埋めていない。学会採択・受賞の区別と論文候補は[venues.md](venues.md)および[candidates.tsv](candidates.tsv)を参照。
