# 主要学会別 VLA / ロボット基盤モデル論文 (ICLR 以外, 2024-2026)

調査基準日: 2026-10-31。候補の全リストは `venues_candidates.tsv` (約 275 件)。
方針: 公式の採択・proceedings ページのタイトルを機械的に抽出し、VLA、ロボット基盤モデル、汎用ロボットポリシーに該当するものを残した。件数は「タイトルに VLA 等を含む論文」の数で、網羅的な件数ではない。arxiv_id は CVF ページに載っているものだけ記入した (他は未確認として空欄)。

## 1. 公式ページで一覧を確認できた学会

| 学会 | 開催 | 公式の確認 URL | VLA 系 (TSV 件数) |
|---|---|---|---|
| CoRL 2024 (PMLR v270) | 2024-11 ミュンヘン | https://proceedings.mlr.press/v270/ | 8 |
| CoRL 2025 (PMLR v305) | 2025-09-27〜30 ソウル | https://proceedings.mlr.press/v305/ | 19 |
| RSS 2024 (roboticsproceedings rss20) | 2024 | https://www.roboticsproceedings.org/rss20/index.html | 6 |
| RSS 2025 (rss21) | 2025-06-21〜25 USC | https://www.roboticsproceedings.org/rss21/index.html | 9 |
| RSS 2026 (rss22) | 2026-07-13〜17 シドニー | https://www.roboticsproceedings.org/rss22/index.html | 20 |
| CVPR 2025 | 2025 | https://openaccess.thecvf.com/CVPR2025?day=all | 6 |
| CVPR 2026 | 2026-06-03〜07 デンバー | https://openaccess.thecvf.com/CVPR2026?day=all | 48 (open access 4,042 件中) |
| ICCV 2025 | 2025 | https://openaccess.thecvf.com/ICCV2025?day=all | 8 |
| ECCV 2024 | 2024 | https://www.ecva.net/papers.php | 1 (QUAR-VLA のみ) |
| ICML 2024 (PMLR v235) | 2024 | https://proceedings.mlr.press/v235/ | 1 (3D-VLA) |
| ICML 2025 (PMLR v267) | 2025-07 バンクーバー | https://proceedings.mlr.press/v267/ | 5 |
| ICML 2026 (PMLR v306) | 2026-07-06〜11 ソウル | https://proceedings.mlr.press/v306/ | 62 |
| NeurIPS 2024 | 2024 | https://proceedings.neurips.cc/paper_files/paper/2024 | 4 |
| NeurIPS 2025 | 2025 | https://neurips.cc/virtual/2025/papers.html | 22 (取得できた一覧の範囲。全数ではない可能性) |

重要な傾向: 2026 年は CVPR 2026 (48) と ICML 2026 (62) で、タイトルに VLA を含む論文が急増している。ICML 2025 は 5 件、CVPR 2025 は 6 件だった。

## 2. 学会別の代表論文 (すべて上記の公式ページで確認)

### CoRL
- 2024: OpenVLA https://proceedings.mlr.press/v270/kim25c.html / Embodied CoT (ECoT) / Mobility VLA https://proceedings.mlr.press/v270/xu25b.html / CrossFormer https://proceedings.mlr.press/v270/doshi25a.html / Steering Your Generalists (V-GPS)
- 2025 (v305): π0.5 https://proceedings.mlr.press/v305/black25a.html (oral) / GraspVLA https://proceedings.mlr.press/v305/deng25a.html / DexVLA https://proceedings.mlr.press/v305/wen25b.html / FLOWER https://proceedings.mlr.press/v305/reuss25a.html / ControlVLA / Long-VLA / 3DS-VLA / RICL / TrackVLA / RoboMonkey / RoboArena (評価) https://proceedings.mlr.press/v305/atreya25a.html

### RSS
- 2024: Octo, RT-H, Yell At Your Robot, NaVid, VLMPC (rss20)
- 2025: π0, SpatialVLA, FAST, Uni-NaVid, NaVILA, ConRFT, RLDG, CLIP-RT, Fine-Tuning VLA (OpenVLA-OFT 系) (rss21)
- 2026 (rss22 の全一覧を確認): π*0.6 (a VLA That Learns From Experience), Emergence of Human to Robot Transfer in VLAs, Steerable VLA Policies, Ψ0 (humanoid 基盤モデル), PointACT, StereoVLA, RLux-VLA, BagelVLA, X-DiffVLA, mimic-video, LAP, LIBERO-X, PolaRiS, RoboLab ほか

### CVPR / ICCV / ECCV
- CVPR 2025: CoT-VLA, MoManipVLA, Universal Actions for Embodied Foundation Models, Object-Centric Prompt-Driven VLA
- ICCV 2025: Dita, CoA-VLA, VQ-VLA, VLABench, FedVLA, 敵対的脆弱性の論文
- CVPR 2026: Fast-ThinkAct (arXiv 2601.09708), ACoT-VLA, Mantis, SRPO, MergeVLA, ActiveVLA, SwiftVLA, Evo-1, UniDex (ロボット基盤スイート), AT-VLA, ForceVLA2、運転 VLA (DriveMoE, ColaVLA 等)、攻撃 (FlowHijack 等) ほか
- ECCV 2024: QUAR-VLA (四脚ロボット VLA)

### ICML / NeurIPS
- ICML 2024: 3D-VLA
- ICML 2025: Hi Robot, OTTER, DiffusionVLA, UP-VLA, Video Prediction Policy
- ICML 2026: VLANeXt, VLA-Arena, XR-1, DreamDojo, Discrete Diffusion VLA, Vision-Language-Action Pretraining from Large-Scale Human Videos ほか 62 件
- NeurIPS 2024: RoboMamba, DeeR-VLA, OmniJARVIS, HumanVLA
- NeurIPS 2025: Knowledge Insulating VLA (π 系), ThinkAct, DreamVLA, BridgeVLA, VLA-Cache, SafeVLA, BadVLA, ForceVLA, SAFE, Self-Improving Embodied Foundation Models ほか

## 3. IEEE 系 (OpenAlex の書誌情報で確認。公式採択一覧は未確認)
ICRA / IROS の採択一覧は IEEE Xplore / PaperPlaza で、取得できなかった。ここでは OpenAlex (https://api.openalex.org/works?...) で DOI 接頭辞 (ICRA 2025: 10.1109/icra55743.2025, IROS 2025: 10.1109/iros60139.2025, RA-L / T-RO / Science Robotics は source id) を指定して検索した。検索は部分的で、網羅的ではない。
- ICRA 2025: Improving VLA with Online RL, MoRE (四脚 VLA), ReVLA, Run-time Observation Interventions, RT-Affordance, Effective Tuning Strategies for Generalist Robot Manipulation Policies
- IROS 2025: PD-VLA, CLAP, RoboNurse-VLA, Refined Policy Distillation
- IROS 2024: GeRM (四脚 generalist)
- RA-L (2024-2026): TinyVLA, PointVLA, CAST, Colosseum V2, CLARE, VAMOS, VLA-Touch ほか 20 件
- T-RO: FlowVLA, Tactile-Force Alignment in VLA (2 件のみ)
- AAAI 2026 (Singapore, 2026-01-20〜27, 一覧は OpenAlex 経由): ReconVLA, VLA-Adapter, DiTEA, DexGraspVLA, GraphCoT-VLA, TCoT, MoLe-VLA ほか 22 件
- Science Robotics: タイトルで VLA に該当する 2024-2026 年の論文は検索で見つからなかった (未確認)
- ICRA 2026 (ウィーン, 6 月) と IROS 2026 (10 月): 採択一覧を取得できず、未確認

## 4. 受賞 (best paper) と VLA の関係
- CoRL 2025 (公式 https://2025.corl.org/program/awards): Best Paper は Learning a Unified Policy for Position and Force Control in Legged Loco-Manipulation と Fabrica。Best Student Paper は Visual Imitation Enables Contextual Humanoid Control。入賞候補 (finalist) に π0.5 (VLA)、LocoFormer、DexUMI、The Sound of Simulation、Steering Your Diffusion Policy with Latent Space RL。VLA 本体の受賞はなく、π0.5 は finalist 止まり。
- RSS 2025 (公式 https://roboticsconference.org/2025/program/awards/): Outstanding Paper は FEAST。Outstanding Paper の finalist に FAST (VLA の action tokenization) と Distributed Epigraph Form MARL。
- RSS 2026: Outstanding Paper は FlashSAC、Student Paper は Muninn、Systems Paper は NeuralActuator。出典は解説ブログ https://www.bohrium.com/en/blog/rss-2026-papers/ (二次情報。公式ページ未確認)。いずれも VLA ではない。
- CVPR 2026 (公式 https://cvpr.thecvf.com/Conferences/2026/News/Closing): Best Paper は D4RT。Honorable Mention に NitroGen (ゲーム汎用エージェントの open foundation model)。採択 4,089 / 応募 16,092。
- CoRL 2024 Best Paper (Parental Guidance) は研究室ページ由来で未検証。
- ICRA 2026 の best paper は検索結果 (二次情報) で複数件の受賞があったとされるが、公式の受賞一覧は取得できず、VLA との関係は未確認。

## 5. VLA 関連ワークショップ
- CoRL 2025 (公式 https://2025.corl.org/program/workshops): "Workshop on Generalist Policies In the Wild & RoboArena Challenge" https://sites.google.com/view/corl-roboarena / "Robot Learning Done Right: Responsibly Developing Foundation Models for Robotics" https://sites.google.com/cam.ac.uk/robotlearningdoneright
- RSS 2026: RL4VLA (Reinforcement Learning for VLA Models), 2026-07-17, UTS シドニー (公式 https://sites.google.com/view/rl4vla-workshop 確認済み)
- ICRA 2026: "From Data to Decisions: VLA Pipelines for Real Robots" https://icra2026vlapipeline.github.io (検索結果で確認、ページ本体は未取得)
- CVPR 2026: 6/3 に "Bridging Vision, Language, and Action: What's Missing in Actionable Visual Perception for Robotics" および 3D-LLM/VLA 第 2 回 (検索結果のみ、公式未確認)
- CoRL 2026: 2026-11-09〜12, Austin, Texas (https://www.corl.org/)。基準日時点で PMLR 掲載なし。採択論文の一覧は取得できず、個別の採択報告 (企業・研究者の告知) のみ。論文一覧は未確認。

## 6. 注意点
- 取りこぼしあり: タイトルに VLA 等を含まない基盤モデル論文 (例: CoRL 2024 の Theia、RT-Sketch) は抽出条件の外にある。CoRL の候補は少なめ。
- arxiv_id は CVF 掲載分のみ。PMLR、RSS、NeurIPS 分は空欄 (未確認)。
- RSS 2026 の受賞は二次情報。
