# VLA 実務エコシステム調査 (調査基準日 2026-10-31)

注意: 取得ツールの要約は誤りを含み得る。例として LeRobot の GitHub releases ページは v0.6.1 の日付を 2024-08-03 と返したが、PyPI は 2026-08-03 と返した。本書は PyPI を採用した。一次情報で直接確認できなかった点は「未確認」と書いた。ベンダー自己申告やまとめサイト由来の数値はそう明記した。

## 1. 公開モデルと重み

| モデル | 最新状況 | ライセンス | 必要 GPU・遅延 | 出典 |
|---|---|---|---|---|
| π0 / π0-FAST / π0.5 (openpi) | 公開重みは π0、π0-FAST、π0.5。π0.5 は 2025-09 公開。PyTorch 対応も 2025-09 | コードは Apache-2.0。Gemma ライセンスのファイルが付属 | 推論 8GB 超 (RTX 4090 例)、LoRA 微調整 22.5GB 超、フル微調整 70GB 超 | https://github.com/Physical-Intelligence/openpi |
| π*0.6 (2025-11-17) / π0.7 (2026-04-16) | Physical Intelligence のブログ上では発表のみ。ブログ要約には重み公開の記載なし。**重み公開は未確認** (検索まとめサイトは π*0.6 が openpi で公開と書くが、一次情報では確認できず採用しない) | 未確認 | 未確認 | https://www.pi.website/blog , https://www.pi.website/blog/pi07 |
| π0.5-DROID (openpi) | DROID 用の最強の汎用ポリシーと説明されるが、単純な机上 pick-and-place 程度で、複雑な操作は失敗すると明記 | openpi と同じ | 推論サーバは 4090 級。チャンクあたり 0.5〜1 秒の遅延が通常と明記 | https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README.md |
| NVIDIA Isaac GR00T N1.7 | 2026-04-17 公開。3B、VLM は Cosmos-Reason2-2B、EgoScale 約 2 万時間の人の一人称映像で事前学習。Unitree G1、YAM、AgiBot Genie 1 で検証 (NVIDIA 自己申告) | コード Apache-2.0、重みは NVIDIA Open Model License。商用利用可と NVIDIA は記載 | 推論 16GB 以上 VRAM、微調整 40GB 以上推奨。TensorRT で RTX PRO 6000 Blackwell 約 40Hz、Jetson AGX Thor 約 28Hz (LIBERO、バッチ 1、NVIDIA 自己申告) | https://github.com/NVIDIA/Isaac-GR00T , https://huggingface.co/blog/nvidia/gr00t-n1-7 |
| SmolVLA (lerobot/smolvla_base) | 450M (約 0.5B)、2025-06 公開。HF 上で 184k ダウンロード。LeRobot 上に LIBERO、VLABench、RoboMME 用の微調整版あり | Apache-2.0 (重みと学習データ、検索結果の記載) | 消費者向け GPU や MacBook で動作と報じられる。遅延の実測は未確認 | https://huggingface.co/lerobot/models?sort=trending , https://huggingface.co/lerobot |
| OpenVLA (7B) | 2024 年のモデル。OFT 手法 (2025-03) で推論が 25〜50 倍高速化とされる | コード MIT。重みは Llama 2 由来で Llama Community License | LoRA 微調整で約 27GB VRAM、フル微調整は A100 8 枚ノード | https://github.com/openvla/openvla |
| LeRobot Hub 上のその他 | xvla-base (0.9B)、wall-oss-0.5 (4B)、lingbot_vla_v2_base (6B)、cosmos3-nano (16B)、cosmos3-edge (5B)、FineART-VLA | 個別に未確認 | 未確認 | https://huggingface.co/lerobot |
| LingBot-VLA 2.0 (Robbyant、Ant Group) | 2026-07-08 公開。6B、約 6 万時間、20 種の機体 (企業発表と報道。一次の確認は未実施) | Apache-2.0 と報道 | 未確認 | https://lasvegassun.com/news/2026/jul/08/robbyant-upgrades-and-open-sources-lingbot-vla-20-/ |
| pi05_hsr_base (AIRoA) | 2026-07-31 公開。π0.5 を HSR データで継続事前学習。H200 64 枚で約 0.8 エポック | π0.5 を継承し Gemma 条件 | 未確認 | https://exawizards.com/column/ai-trend/news-0823-2026/ |

### Gemini Robotics 2 (一次情報の確認結果)
- DeepMind のモデルカード一覧は、Gemini Robotics-ER 2 と On-Device 2 を 2026-07-30 付けで掲載する。ER 1.6 は 2026-04-20、1.5 は 2025-09-25。https://deepmind.google/models/model-cards/
- On-Device 2 のカード (一次): Gemini Robotics 1.5 の技術と on-device Gemma に基づく VLA。信頼できるテスターのみに提供。SO101 で成功率 53.3% (v1 は 6.7%)、Dexmate で 75.6% (v1 は 33.3%)。ただし「拡張した学習期間の後」の値。分布外タスクに弱く、高自由度ロボットは制御できず、対象は立位の双腕操作に限る。https://deepmind.google/models/model-cards/gemini-robotics-on-device-2/
- ER 2 のカード (一次): Google AI Studio、Gemini API で公開。Gemini Enterprise Agent Platform は private preview。基盤は Gemini 3.5 Flash。医療や交通など安全が critical な用途には使うなと明記。https://deepmind.google/models/model-cards/gemini-robotics-er-2/
- 本体の Gemini Robotics 2 (VLA) は報道ではアーリーアクセスのパートナー限定。VLA 本体のモデルカードのページは未確認 (推測 URL は 404)。
- 全身制御 (Apptronik Apollo 2 などの人型) や 22 自由度の手の主張は報道ベース。DeepMind 本文のブログ URL と技術レポートの URL は取得できず**未確認**。https://www.therobotreport.com/google-deepmind-says-gemini-robotics-2-enables-full-body-control/
- 数値の注意 (二次情報): 11 タスクの成功率が 92% (電球を外す) から 32% (ちりとり掃き) まで分散。電球を外す 92% に対し、はめ込みは 36%。ER 2 プランナは人への指示 74.0%、ロボットへの指示 60.0%。出典は解説ブログで、DeepMind の原表との照合は未実施。https://www.eesel.ai/blog/gemini-robotics-2
- 前世代の技術レポート: Gemini Robotics 1.5 は arXiv 2510.03342 (2025-10-02 投稿) で確認済み。https://arxiv.org/abs/2510.03342
- 結論: 重みは非公開。再現も外部評価もできない。研究に使えるのは ER 2 の API のみ。

## 2. ツール

- LeRobot: PyPI 最新は 0.6.1 (2026-08-03)、Python 3.12 以上、Apache-2.0。https://pypi.org/project/lerobot/ 。v0.6.0 で GR00T N1.5 を N1.7 に置換、PyTorch 2.7 以上、RL スタックを再構築と記載。v0.5.0 で Unitree G1 の全身制御を追加。https://github.com/huggingface/lerobot/releases (日付の表記が不正のため日付は PyPI を採用)。ドキュメントは ACT、π0、SmolVLA を掲載し、LIBERO や Meta-World での評価に対応。https://huggingface.co/docs/lerobot/index 。RoboTwin 2.0 の文書ページも存在する (検索結果)。https://huggingface.co/docs/lerobot/robotwin.md
- openpi: 公開モデルは π0、π0-FAST、π0.5。2025-06 に DROID 全データの学習手順を追加、2025-09 に PyTorch 対応。取得した README の更新記録は 2025 年までで、2026 年のモデルは載っていない (ページのキャッシュが古い可能性があり、最新リリースのタグは未確認)。https://github.com/Physical-Intelligence/openpi
- Isaac GR00T: N1.7 が最新の GA 版。N1.6 までは few thousand 時間のロボット遠隔操作データ中心。https://github.com/NVIDIA/Isaac-GR00T 。NVIDIA と Hugging Face が LeRobot への GR00T N1.7 と Isaac Teleop の統合を発表 (フォーラム投稿)。https://forums.developer.nvidia.com/t/nvidia-and-hugging-face-bring-new-models-and-frameworks-to-lerobot-for-the-open-robotics-community/376499
- ManiSkill3: Apache-2.0、アセットは CC BY-NC 4.0。4090 で RGBD とセグメンテーションを 30,000 FPS 以上 (自己申告)。https://github.com/haosulab/ManiSkill

## 3. データセット

| 名称 | 規模 | ライセンス | 出典 |
|---|---|---|---|
| Open X-Embodiment | 22 種のロボット、21 機関、527 スキル、100 万以上の軌道、60 データセット統合 | 未確認 | https://robotics-transformer-x.github.io/ |
| DROID | 7.6 万軌道、350 時間、564 シーン、86 タスク、Franka Panda、ZED 2 を 2 台と ZED Mini、Oculus Quest 2 で遠隔操作。論文は arXiv 2403.12945 | 公式サイトでは未確認。LeRobot 形式の再配布版 (droid_1.0.1、95,600 エピソード、2,760 万フレーム、399GB) は Apache-2.0 表記 | https://droid-dataset.github.io/ , https://huggingface.co/datasets/cadene/droid_1.0.1 |
| LIBERO | 130 タスク、4 スイート (Spatial、Object、Goal、100) | コード MIT、データ CC BY 4.0 | https://github.com/Lifelong-Robot-Learning/LIBERO |
| RoboCasa365 | 365 タスク、2,500 キッチン、2,200 時間超の実演 (人と合成)、v1.0.1、公開リーダーボードあり | 未確認 | https://robocasa.ai/ |
| AgiBot World Beta | 2,976.4 時間、100 万エピソード超、48.1TB | CC BY-NC-SA 4.0 (非商用) | https://huggingface.co/datasets/agibot-world/AgiBotWorld-Beta |
| Galaxea Open-World | 500 時間、約 10 万軌道、150 以上のタスク、50 シーン、R1 Lite で収集。arXiv 2509.00576 (2025-08-30 投稿を確認) | cc-by-nc-sa-4.0 (検索結果の記載、リポジトリ未確認) | https://arxiv.org/abs/2509.00576 |
| AIRoA MoMa (初期版) | 25,469 エピソード、約 94 時間、HSR、LeRobot v2.1 形式。arXiv 2509.25032 | 未確認 | https://arxiv.org/abs/2509.25032 , https://huggingface.co/datasets/airoa-org/airoa-moma |
| AIRoA MoMa 5k | 5,025 時間、118.4 万エピソード、約 4TB、44 台、5 拠点 | 研究開発用に限定。第三者への販売と再配布は禁止 | https://exawizards.com/column/ai-trend/news-0823-2026/ |

規模の比較 (同記事の記載で、一次未確認): Xiaomi が 2026-08 に 10 万時間超を公開、LingBot-VLA 2.0 は約 6 万時間。AgiBot World や Galaxea は CC BY-NC-SA で、商用利用には使えない。

## 4. ベンチマークと評価の落とし穴

- LIBERO は飽和している。PatchWAM 論文 (arXiv 2609.25961、2026-09-22) の比較で QuoVLA が 99.6%、PatchWAM が 98.4% (検索結果の記載)。https://arxiv.org/abs/2609.25961
- LIBERO-Plus (arXiv 2510.13626): 7 種の摂動 (配置、視点、初期状態、言語、照明、背景、ノイズ) で成功率が 95% から 30% 未満に低下。言語指示を無視するモデルが多い。https://arxiv.org/abs/2510.13626
- LIBERO-PRO (arXiv 2510.03827): 標準設定で 90% 超のモデルが一般化設定で 0.0%。物体を置換しても把持動作を続け、壊れた指示でも出力が同じ。https://arxiv.org/abs/2510.03827
- PatchWAM は LIBERO-Plus で 91.8% (拡張実演を含む full-data 設定)、RoboTwin 2.0 で 96.12%。同じ数字でも学習データの設定が違う。
- RoboTwin 2.0 (arXiv 2506.18088): 50 タスク、公式プロトコルは 1 タスク 100 エピソード、Easy (demo_clean) と Hard (demo_randomized) を別に報告 (検索結果の記載)。論文は 731 物体、147 カテゴリ。https://arxiv.org/abs/2506.18088 。π0.5 の素の値は取得できず**未確認**。
- RoboArena (arXiv 2506.18123): DROID 上で二重盲検のペア比較。7 機関、7 ポリシー、612 ペア評価、4,284 ロールアウト。ツール使用、変形物、精密な位置合わせ、多段推論が弱いと分析。リーダーボードの現在値は未確認。https://arxiv.org/abs/2506.18123v1
- Isaac Lab-Arena (NVIDIA、Lightwheel 共同): GR00T N、π0、SmolVLA の並列評価に対応。RoboCasa と LIBERO のタスク 250 以上を移植。LeRobot EnvHub と連携。リーダーボードの値は未確認。https://developer.nvidia.com/blog/simplify-generalist-robot-policy-evaluation-in-simulation-with-nvidia-isaac-lab-arena
- Meta-World、ManiSkill のリーダーボードの現在値は今回取得できず**未確認**。
- 落とし穴の整理: (1) 標準 LIBERO はテストが学習分布に近く暗記で通る。(2) 成功率だけでは安全性、軌道品質、効率が見えない。(3) シミュレーションの点数と実機成功率の相関は、実機環境で較正しない限り弱いとするサーベイがある (検索結果の要約、要確認)。(4) 学習データの設定 (拡張、微調整の有無) が揃っていない表が多い。

## 5. FR3 で VLA を動かす事例

- DROID の標準構成は Franka Panda、ZED 2 を 2 台、ZED Mini の手首カメラ、Oculus Quest 2 の遠隔操作。公式サイトは FR3 を標準構成として記載していない。https://droid-dataset.github.io/ 。ハードの買い物リストのページは取得できず、FR3 互換の公式記述は**未確認**。
- 実務構成 (openpi): 4090 級 GPU のポリシーサーバに DROID 制御ノート PC がネットワークで接続し、チャンクあたり 0.5〜1 秒の遅延は正常。有線接続を推奨。https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README.md
- FR3 向けの第三者実装: PyPI の inspect-robots-franka は FR3 と Panda を OpenPI の DROID ポリシーで動かす。π0.5-DROID の行動は 15Hz、関節速度 7 とグリッパ 1。ガード、ウォームアップ、遅延チェック、E-stop を備える。実時間制御には直結の有線、PREEMPT_RT カーネル、ファームウェアに合う libfranka が必要。https://pypi.org/project/inspect-robots-franka/ (検索結果の要約。ページ本文は未精読)
- FR3 上での π0.5 微調整チェックポイントの例 (HF 上): msbutt1/pi0.5-fr3-v3-pick-place、THU98/pi05_franka_5task_full_20k。内容と評価は未確認。https://huggingface.co/msbutt1/pi0.5-fr3-v3-pick-place
- 示唆: FR3 で動かす最短経路は、DROID 構成の再現と pi05_droid の利用。ただし汎用ポリシーは机上の単純な pick-and-place までと公式に断っており、自前タスクは微調整が前提。

## 6. 批判的検討と実環境の信頼性

- How VLAs (Really) Work In Open-World Environments (arXiv 2604.21192、2026-04-23): BEHAVIOR-1K Challenge の分析。最終状態だけの成功率は安全性を測れず、性能を誇張し得る。複雑な open-world では成功率が低く、支援用途や安全 critical 用途に信頼できないと主張。https://arxiv.org/abs/2604.21192
- VLA Safety サーベイ (arXiv 2604.23775、2026-04-26、改訂 2026-08-25): データ汚染、バックドア、敵対的パッチ、freezing 攻撃など。認証付きの頑健性が未解決。https://arxiv.org/abs/2604.23775
- The Evaluation Bottleneck of VLA (582 本のサーベイ、2026-05 まで) は検索結果の要約のみで、arXiv ID は**未確認**。
- ベンダー自身の限界の記載: π0.5-DROID は複雑な操作で失敗。Gemini Robotics On-Device 2 は分布外タスクと高自由度ロボットに弱い。ER 2 は安全 critical 用途を禁止。
- LIBERO-Plus と LIBERO-PRO は、高い点数が頑健性ではなく暗記の産物であることを示す。

## 7. 日本の動向

- AIRoA (AI Robot Association): HSR 遠隔操作データ MoMa を公開。2026-07-31 に MoMa 5k (5,025 時間) と pi05_hsr_base を公開。ICRA 2026 でワークショップと約 1 万時間のデータの国際コンペを開催。https://exawizards.com/column/ai-trend/news-0823-2026/ , https://ascii.jp/elem/000/004/372/4372987/ 。1 機種に限るため多様性は海外に劣ると同記事は指摘。
- NII 栗田研: ロボット基盤モデル、VLA。ICRA 2026 に egocentric 映像からの VLA、IROS 2026 に flow matching の方策学習。https://www.vla.nii.ac.jp/projects/robot/
- LLM-jp チューニングコンペ 2026 の RAMEN チーム (Team035): llm-jp-4-8b-instruct と llm-jp-3.1-1.8b-instruct4 をベースに日本語ロボット基盤モデル (VLA) を開発。https://llm-jp.github.io/tuning-competition/2026/pdfs/free_team035_slide.pdf
- 日本語の解説: https://www.ai-souken.com/article/what-is-vla-model
- Preferred Networks、東大、産総研など他のグループは今回の検索では確認できず**未確認**。

## 8. 実務上の要点

1. 公開重みで再現可能なのは π0 系 (π0、π0-FAST、π0.5)、GR00T N1.7、SmolVLA、LingBot-VLA 2.0 (報道)。π0.7 と Gemini Robotics 2 の VLA は重みが非公開。
2. ライセンス: コードは Apache-2.0 が多いが、重みは Gemma 条件 (π0.5 系)、NVIDIA Open Model License (GR00T)、Llama 条件 (OpenVLA) で異なる。大規模データは非商用 (AgiBot World、Galaxea) や用途限定 (AIRoA MoMa 5k) がある。
3. 評価は LIBERO の高得点を信用せず、LIBERO-Plus/PRO、RoboArena、自前の実機試験を併用する。
