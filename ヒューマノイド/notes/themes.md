# ヒューマノイド論文のテーマ別整理

**調査基準日**: 2026-10-31  
**入力**: `C:\Users\table\AppData\Local\Temp\claude\C--Users-table-vla\96a5b191-79ac-4772-a63d-62f0b328cb07\scratchpad\pa\titles_humanoid.tsv`（全 1579 件）  
**整理対象**: 1228 件（除外: 351 件）  
**出典**: 上記 TSV のタイトル・要約先頭 300 字のみ（Web 検索なし）。OpenReview 形式 ID と arXiv ID が混在。

**一覧ファイル**: `file:///C:/Users/table/AppData/Local/Temp/claude/C--Users-table-vla/96a5b191-79ac-4772-a63d-62f0b328cb07/scratchpad/pa/titles_humanoid.tsv`

**論文メタデータの出典**: 同一 TSV 行。確認用 URL は arXiv / OpenReview 形式 ID から機械生成。

## 除外基準

1. **ヒューマノイド中核なし**: タイトル/要約で humanoid ロボットの制御・歩行・全身運動が主題でない（一般 RL/LLM のみ等）。
2. **CG・アニメーション中心**: humanoid mesh/character animation が主で実機制御・simulation policy が薄い。
3. **テーマキーワード不足**: humanoid はあるが下記分野に分類できず、かつ汎用バケットにも入れないもの。

## テーマ一覧（件数）

- **モーション追従・模倣 (Motion Tracking / Mimic)**: 177 件
- **全身運動・歩行 (Locomotion)**: 322 件
- **言語・VLA・LLM によるヒューマノイド制御**: 59 件
- **行動基盤モデル・汎用ポリシー (BFM / Foundation)**: 34 件
- **Sim-to-Real・ドメイン適応**: 58 件
- **データ収集・テレオペ・Real2Sim**: 108 件
- **操作・リARRANGE・双腕**: 117 件
- **階層制御・Whole-Body Control アーキテクチャ**: 30 件
- **表情・上半身・コミュニケーション**: 22 件
- **学習効率・RL アルゴリズム (ヒューマノイド文脈)**: 47 件
- **汎用・その他のヒューマノイド研究**: 254 件

## モーション追従・模倣 (Motion Tracking / Mimic)（177 件）

### 解いている問題
人間動作を自然に再現し、多様スキルへ拡張する。

### 主要な手法の対立軸
拡散ガイド vs 純 tracking RL / 人間 mocap vs 学習データ拡張 / retarget あり vs retarget-free

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.39327 | 2026 | SONIC-K1: Porting a Universal Humanoid Motion Tracker to a Small Humanoid on ... | [リンク](https://arxiv.org/abs/2610.39327) |
| 2610.37801 | 2026 | An Empirical Study of Wrist-Target Construction and Joint-Angle Limits in Hum... | [リンク](https://arxiv.org/abs/2610.37801) |
| 2610.36615 | 2026 | HumiMimic: Mimetic Embodiment Transfer of Human-Humanoid Interaction from In-... | [リンク](https://arxiv.org/abs/2610.36615) |
| 2610.34126 | 2026 | HumanoidNDM: Closing the Training-Deployment Gap of Motion Tracking via Human... | [リンク](https://arxiv.org/abs/2610.34126) |
| 2610.33508 | 2026 | MimicAll: Structured Embodiment Conditioning for Cross-Humanoid Whole-Body Mo... | [リンク](https://arxiv.org/abs/2610.33508) |
| 2610.32966 | 2026 | ViT-H: Generative Video-To-Humanoid Control with Motion Tracking Feedback | [リンク](https://arxiv.org/abs/2610.32966) |
| 2610.32460 | 2026 | CoCarry: Contact-Support-Structured Retargeting for Dual-Humanoid Cooperative... | [リンク](https://arxiv.org/abs/2610.32460) |
| 2610.30540 | 2026 | Motion Retargeting with Spatiotemporal Preferences for Humanoid Loco-Manipula... | [リンク](https://arxiv.org/abs/2610.30540) |
| 2610.29903 | 2026 | HuMiT: Low-Latency Whole-Body Humanoid Teleoperation via Compact Reference Tr... | [リンク](https://arxiv.org/abs/2610.29903) |
| 2610.29169 | 2026 | SMR: Learning streaming motion retargeting for humanoids from human semantic | [リンク](https://arxiv.org/abs/2610.29169) |
| 2610.28523 | 2026 | VLM-Guided Contact Retargeting and Generative Partner Modeling for Humanoid-H... | [リンク](https://arxiv.org/abs/2610.28523) |
| 2610.28480 | 2026 | SuperMimic: Scaling Humanoid Whole-Body Control with One Differentiable World... | [リンク](https://arxiv.org/abs/2610.28480) |
| 2610.28470 | 2026 | Fast Motion Retargeting Pipeline for Scalable Humanoid Robot Learning | [リンク](https://arxiv.org/abs/2610.28470) |
| 2610.22119 | 2026 | Compliant GMT: Making General Motion Tracking Compliant via Residual Referenc... | [リンク](https://arxiv.org/abs/2610.22119) |
| 2610.15274 | 2026 | Embodiment-Aware Inference-Time Search for Human Reaction Selection in Humano... | [リンク](https://arxiv.org/abs/2610.15274) |

### 2026 年の増減（TSV 内カウント）
2026年 113 件 / 2025年 42 件。

### 未開拓に見える方向
小形ロボット (K1 等) へのスケール則の体系化（SONIC-K1 等は出始め）。

## 全身運動・歩行 (Locomotion)（322 件）

### 解いている問題
複雑な関節系で多様環境を歩行・平衡する低レベル〜全身制御。

### 主要な手法の対立軸
階層 WBC vs 端到端 RL / 地形汎化 vs 平坦 / モデルベース補助 vs 純 sim RL

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.37974 | 2026 | FORGE: Feasible Online Reduced-Order Reference Generation and Whole-Body Exec... | [リンク](https://arxiv.org/abs/2610.37974) |
| 2610.36825 | 2026 | HC2Robot: Hyper-Connection Transformers with Predicted Foresight for Multi-Te... | [リンク](https://arxiv.org/abs/2610.36825) |
| 2610.36546 | 2026 | REACH: An RL-based Hierarchical Humanoid Crawling Framework for Adaptable Con... | [リンク](https://arxiv.org/abs/2610.36546) |
| 2610.30876 | 2026 | LocoManiLab: A Unified Testbed for Data, Policies, Controllers, and Deploymen... | [リンク](https://arxiv.org/abs/2610.30876) |
| 2610.30334 | 2026 | MPBRS: Multi-Potential-Based Reward Shaping for Unified Reward Configuration ... | [リンク](https://arxiv.org/abs/2610.30334) |
| 2610.30080 | 2026 | Do Earth-Trained Humanoid Controllers Walk on the Moon? Gravity, Terrain, and... | [リンク](https://arxiv.org/abs/2610.30080) |
| 2610.29612 | 2026 | Watch Your Step: Anticipated Perception for Humanoid Locomotion | [リンク](https://arxiv.org/abs/2610.29612) |
| 2610.27688 | 2026 | Adaptive Traversal Tubes for Posture-Aware Navigation of Bipedal Humanoids | [リンク](https://arxiv.org/abs/2610.27688) |
| 2610.26584 | 2026 | HAF-VLA: Hierarchical Action Flow Framework for Humanoid Vision-Language-Acti... | [リンク](https://arxiv.org/abs/2610.26584) |
| 2610.25701 | 2026 | Validation of Human Motor Development Scales with Humanoid Robots | [リンク](https://arxiv.org/abs/2610.25701) |
| 2610.24847 | 2026 | DiPLO: Self-distilled Diffusion Planning for Loco-manipulation | [リンク](https://arxiv.org/abs/2610.24847) |
| 2610.23879 | 2026 | Adaptive Rejection of Unknown Hybrid Sinusoidal Disturbances with Application... | [リンク](https://arxiv.org/abs/2610.23879) |
| 2610.23872 | 2026 | DUET: Decoupled Upper- and Lower-Body Execution for Task-Agnostic Humanoid Lo... | [リンク](https://arxiv.org/abs/2610.23872) |
| 2610.18950 | 2026 | $λ_0$: Scaling Open-World Egocentric Human Data for Humanoid Loco-Manipulation | [リンク](https://arxiv.org/abs/2610.18950) |
| 2610.18872 | 2026 | EgoExplorer: A Vision-Motion-Touch Observatory for Human Loco-Manipulation In... | [リンク](https://arxiv.org/abs/2610.18872) |

### 2026 年の増減（TSV 内カウント）
2026年 154 件 / 2025年 104 件。

### 未開拓に見える方向
外乱・非平坦での安全保証、エネルギー効率と敏捷性の Pareto（要約ベース）。

## 言語・VLA・LLM によるヒューマノイド制御（59 件）

### 解いている問題
自然言語で全身動作を指示し、オープン環境で汎化する。

### 主要な手法の対立軸
低レベル既存 WBC 前提 vs 端到端 / オープ語彙 vs 固定コマンド / VLM ラッパ vs 統合 VLA

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.37330 | 2026 | Tokens of Motion: Primitive Motion Learning for Human-Humanoid Skill Transfer | [リンク](https://arxiv.org/abs/2610.37330) |
| 2610.36507 | 2026 | GRAFT: Geometry-Aware Residual Adaptation for Foundation Trackers | [リンク](https://arxiv.org/abs/2610.36507) |
| 2610.34186 | 2026 | HuGe: Scaling Humanoid Generalist Vision-Language-Action Models with Egocentr... | [リンク](https://arxiv.org/abs/2610.34186) |
| 2610.31166 | 2026 | Memory before Goal: Role of Pre-History Memory for Humanoid Loco-Manipulation | [リンク](https://arxiv.org/abs/2610.31166) |
| 2610.23288 | 2026 | CoEvolve: Self-Evolving Code Policies from Skills to Strategies for Humanoid ... | [リンク](https://arxiv.org/abs/2610.23288) |
| 2610.21152 | 2026 | KODA: Kinematics--Observation Data Alignment for Humanoid Learning from Human... | [リンク](https://arxiv.org/abs/2610.21152) |
| 2610.12026 | 2026 | HWAM: Humanoid World Action Model With Joint State--Action Generation | [リンク](https://arxiv.org/abs/2610.12026) |
| 2609.35709 | 2026 | Humanoid Loco-Manipulation With Discrete VLA Model | [リンク](https://arxiv.org/abs/2609.35709) |
| 2609.35450 | 2026 | Uni-VLaT: Whole-Body Tactile Adaptation of VLA Policies for Humanoid Loco-Man... | [リンク](https://arxiv.org/abs/2609.35450) |
| 2609.26420 | 2026 | Sample, Simulate, Select: Physics-in-the-Loop Text-to-Motion for Humanoids Wi... | [リンク](https://arxiv.org/abs/2609.26420) |
| 2609.23968 | 2026 | Opt2VLA: Force-Aware Vision-Language-Action for Contact-Rich Humanoid Whole-B... | [リンク](https://arxiv.org/abs/2609.23968) |
| 2609.23414 | 2026 | EmoPose: Vision-Language Model Guided Emotion-Aware Gesture Generation for Hu... | [リンク](https://arxiv.org/abs/2609.23414) |
| 2609.22538 | 2026 | FRAMES: Failure Recovery And Monitoring of Embodied Skills for Humanoid Loco-... | [リンク](https://arxiv.org/abs/2609.22538) |
| 2609.18869 | 2026 | KINO: A Keyframe Interface for VLM Planning and Whole-Body Control in Humanoi... | [リンク](https://arxiv.org/abs/2609.18869) |
| 2609.13679 | 2026 | How to Better Train VLAs: Lessons Learned From the REAL-I Challenge at ICRA 2026 | [リンク](https://arxiv.org/abs/2609.13679) |

### 2026 年の増減（TSV 内カウント）
2026年 42 件 / 2025年 12 件。

### 未開拓に見える方向
幻覚命令に対する物理 feasible 性チェック。

## 行動基盤モデル・汎用ポリシー (BFM / Foundation)（34 件）

### 解いている問題
単一モデルで多タスク・プロンプト可能な humanoid 制御。

### 主要な手法の対立軸
プロンプト可能単一方策 vs タスク特化 / sim のみ vs 実機 / 教師なし RL vs デモ

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.38027 | 2026 | METATRON: A Promptable Whole-Body Execution Layer for Humanoids | [リンク](https://arxiv.org/abs/2610.38027) |
| 2610.29030 | 2026 | PHD-Hand: A Printable Humanoid Dexterous Hand with Linkage-Driven 3-DOA Digits | [リンク](https://arxiv.org/abs/2610.29030) |
| 2610.17999 | 2026 | TRACE: Efficient Transfer Learning for Neural Whole-Body Control Across Human... | [リンク](https://arxiv.org/abs/2610.17999) |
| 2610.15833 | 2026 | P-BFM: Perceptive Behavioral Foundation Models for Humanoid Control via Unsup... | [リンク](https://arxiv.org/abs/2610.15833) |
| 2610.14896 | 2026 | Test-Time Compute for Humanoid Behavior Foundation Models | [リンク](https://arxiv.org/abs/2610.14896) |
| 2610.12435 | 2026 | VioLA: Learning Generalist Humanoid Control Policies from Human Data | [リンク](https://arxiv.org/abs/2610.12435) |
| 2610.10198 | 2026 | Benchmarking Behavioral Steerability in Behavior Foundation Models | [リンク](https://arxiv.org/abs/2610.10198) |
| 2610.06129 | 2026 | I-BFM: Reward-Conditioned Robust Humanoid Interaction via Unsupervised Reinfo... | [リンク](https://arxiv.org/abs/2610.06129) |
| 2609.38172 | 2026 | Counterfactual Video Generation Enables Scalable Humanoid Loco-Manipulation | [リンク](https://arxiv.org/abs/2609.38172) |
| 2609.38087 | 2026 | CrossBFM: Distilling a Shared Latent Behavior Space Across Humanoid Embodiments | [リンク](https://arxiv.org/abs/2609.38087) |
| 2609.37677 | 2026 | Learning Expressive and Compositional Motion Representation via Spectral Skills | [リンク](https://arxiv.org/abs/2609.37677) |
| 2609.36151 | 2026 | KPI: A Promptable Kernel for Physical Interaction on Humanoids | [リンク](https://arxiv.org/abs/2609.36151) |
| 2609.15213 | 2026 | X-WBC: A Cross-Embodiment Foundation Model for Humanoid Whole-Body Control | [リンク](https://arxiv.org/abs/2609.15213) |
| 2607.29172 | 2026 | CLIFT: Turning Gemini Robotics On-Device into Humanoid Specialists via Non-In... | [リンク](https://arxiv.org/abs/2607.29172) |
| 2607.15163 | 2026 | Scaling Behavior Foundation Model for Humanoid Robots | [リンク](https://arxiv.org/abs/2607.15163) |

### 2026 年の増減（TSV 内カウント）
2026年 25 件 / 2025年 8 件。

### 未開拓に見える方向
実機プロンプト可能 BFM の公開再現（BFM-Zero は sim 寄り）。

## Sim-to-Real・ドメイン適応（58 件）

### 解いている問題
シミュレーション方策を実機・接触付きタスクへ移す。

### 主要な手法の対立軸
ドメインランダム化 vs 学習補正 (operator 等) / ペイロード・接触 vs 歩行のみ

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.39044 | 2026 | Catch It All!: Generalizable Dynamic Catching with a Dexterous Hand | [リンク](https://arxiv.org/abs/2610.39044) |
| 2610.35075 | 2026 | Zero-HLM: Generalizable Humanoid Loco-Manipulation without Real Robot Data | [リンク](https://arxiv.org/abs/2610.35075) |
| 2610.34740 | 2026 | Networked Humanoid Intelligence: Communication, Coordination, Collaboration, ... | [リンク](https://arxiv.org/abs/2610.34740) |
| 2610.31923 | 2026 | Not an Accident: Exploiting Safety Filter Inadequacy in Humanoid Robots | [リンク](https://arxiv.org/abs/2610.31923) |
| 2610.22176 | 2026 | Inertially Significant Humanoid Teleoperation via Whole Body Model Predictive... | [リンク](https://arxiv.org/abs/2610.22176) |
| 2610.18991 | 2026 | Contact-UAN: Unsupervised Actuator Networks as a Residual World Model for Hum... | [リンク](https://arxiv.org/abs/2610.18991) |
| 2610.14237 | 2026 | Composable Dynamics for Cooperative Humanoids: A RoboCompiler Extension | [リンク](https://arxiv.org/abs/2610.14237) |
| 2610.00198 | 2026 | HumanoidTTT: Test-Time Capability Reuse for Efficient Humanoid Control | [リンク](https://arxiv.org/abs/2610.00198) |
| 2608.30832 | 2026 | A Dual-Cam Parallel Elastic Actuator with Shared Gas-Spring Compensation for ... | [リンク](https://arxiv.org/abs/2608.30832) |
| 2607.28623 | 2026 | PAC-MAN: Perception-Aware CBF-RL for Whole-Body Safety in Humanoid Dodgeball | [リンク](https://arxiv.org/abs/2607.28623) |
| 2607.20399 | 2026 | Towards Miniature Humanoid Tele-Loco-Manipulation Using Virtual Reality and R... | [リンク](https://arxiv.org/abs/2607.20399) |
| 2607.18210 | 2026 | Optimization of sim-to-real transfer in the humanoid robot NICO | [リンク](https://arxiv.org/abs/2607.18210) |
| 2607.07972 | 2026 | In vivo feasibility study of humanoid robots in surgery | [リンク](https://arxiv.org/abs/2607.07972) |
| 2606.28476 | 2026 | FADA: Few-Shot Domain Adaptation via Dynamics Alignment for Humanoid Control | [リンク](https://arxiv.org/abs/2606.28476) |
| 2606.16600 | 2026 | WaveSync: Constrained Wavefront Optimization for Synchronized Co-Speech Gestu... | [リンク](https://arxiv.org/abs/2606.16600) |

### 2026 年の増減（TSV 内カウント）
2026年 33 件 / 2025年 13 件。

### 未開拓に見える方向
操作時ペイロード変動の一般化（GapONet 等は言及）。

## データ収集・テレオペ・Real2Sim（108 件）

### 解いている問題
大規模学習用の humanoid デモ・動画・sim 再現パイプライン。

### 主要な手法の対立軸
テレオペ一体型 vs 既存 mocap / egocentric 人間動画 vs ロボットログ

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.28712 | 2026 | Warping the Workspace: Expanding Visual Access with Adjustable Reach Mapping ... | [リンク](https://arxiv.org/abs/2610.28712) |
| 2610.27242 | 2026 | EmbodyHOI: Embodiment-Aware Generation of Hand-Object Interactions for Humano... | [リンク](https://arxiv.org/abs/2610.27242) |
| 2610.26170 | 2026 | Data-Efficient Learning from Demonstration for Humanoid Robots via Feature-Le... | [リンク](https://arxiv.org/abs/2610.26170) |
| 2610.26169 | 2026 | Compositional Humanoid Manipulation through Isomorphic Teleoperation and Inde... | [リンク](https://arxiv.org/abs/2610.26169) |
| 2610.24559 | 2026 | SocialCoAct: Enabling and Benchmarking Egocentric Social Co-Action for VLM-Ba... | [リンク](https://arxiv.org/abs/2610.24559) |
| 2610.24257 | 2026 | Evaluating Lightweight Contact Feedback in Dual-Operator Collaborative Humano... | [リンク](https://arxiv.org/abs/2610.24257) |
| 2610.16855 | 2026 | Human-Like Redundancy Resolution for Real-Time Bimanual Humanoid Teleoperation | [リンク](https://arxiv.org/abs/2610.16855) |
| 2610.13572 | 2026 | ATHLETE: Learning Reactive Humanoid Tennis via Trajectory-Guided Motion Matching | [リンク](https://arxiv.org/abs/2610.13572) |
| 2610.09117 | 2026 | Workhorse: Learning Robust Whole-Body Humanoid Loco-Manipulation from Human Data | [リンク](https://arxiv.org/abs/2610.09117) |
| 2610.07594 | 2026 | BiGym 2.0: Benchmarking Learned and Agent-Developed Policies for Humanoid Hou... | [リンク](https://arxiv.org/abs/2610.07594) |
| 2610.07511 | 2026 | MobileVISTA: Generative Data Augmentation for Pose Generalization in Mobile M... | [リンク](https://arxiv.org/abs/2610.07511) |
| 2610.05792 | 2026 | DASH: A da Vinci Adapter for Serial-link and Humanoid Robots as an Accessible... | [リンク](https://arxiv.org/abs/2610.05792) |
| 2610.05678 | 2026 | Dataset-Free Compliant Humanoid Loco-Manipulation with Dynamic Online Posture | [リンク](https://arxiv.org/abs/2610.05678) |
| 2610.02341 | 2026 | Filter-Aware Fine-Tuning for Safe Humanoid Whole-Body Tracking | [リンク](https://arxiv.org/abs/2610.02341) |
| 2609.39403 | 2026 | IronMind: Scaling Humanoid Dexterous Manipulation via Camera-Space Ego-Centri... | [リンク](https://arxiv.org/abs/2609.39403) |

### 2026 年の増減（TSV 内カウント）
2026年 67 件 / 2025年 28 件。

### 未開拓に見える方向
低コスト portable 系の標準フォーマット。

## 操作・リARRANGE・双腕（117 件）

### 解いている問題
人型ロボットでの物体操作・長期 rearrange。

### 主要な手法の対立軸
VLA 長期 rearrange vs 単一 grasp / sim 多物体 vs 単一物体

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.35862 | 2026 | Learning Force-Reactive Humanoid Loco-Manipulation | [リンク](https://arxiv.org/abs/2610.35862) |
| 2610.33446 | 2026 | MOTIO: Agentic Skill Engineering for Reality-Grounded Humanoid Loco-Manipulation | [リンク](https://arxiv.org/abs/2610.33446) |
| 2610.30044 | 2026 | SP-HLM: Sparse-Pose-Driven Motion Generation and Whole-Body Control for Human... | [リンク](https://arxiv.org/abs/2610.30044) |
| 2610.25628 | 2026 | Humanoid SRL: Augmenting Humanoids with Supernumerary Limbs for Coordinated L... | [リンク](https://arxiv.org/abs/2610.25628) |
| 2610.24675 | 2026 | Action-Aligned Latent Planning for Versatile Humanoid Loco-Manipulation | [リンク](https://arxiv.org/abs/2610.24675) |
| 2610.23894 | 2026 | Language-Forcing: Advancing Humanoid Loco-Manipulation via Semantic Alignment... | [リンク](https://arxiv.org/abs/2610.23894) |
| 2610.22184 | 2026 | Whole-Body Dexterity | [リンク](https://arxiv.org/abs/2610.22184) |
| 2610.20552 | 2026 | KinoGen: Customizable Humanoid Loco-Manipulation References via Kinematically... | [リンク](https://arxiv.org/abs/2610.20552) |
| 2610.14911 | 2026 | Scalable Multi-Human Cooperative Manipulation via Commander-Executor Coordina... | [リンク](https://arxiv.org/abs/2610.14911) |
| 2610.14561 | 2026 | From Video to Vision: Learning Generalizable Humanoid Carrying from Human Motion | [リンク](https://arxiv.org/abs/2610.14561) |
| 2610.13087 | 2026 | Belief-Overlap Partial Inversion: Object-Centric Flow Replanning for Humanoid... | [リンク](https://arxiv.org/abs/2610.13087) |
| 2610.12558 | 2026 | PanTact: Teaching Whole-Body Dexterity with a Wearable Contact Interface | [リンク](https://arxiv.org/abs/2610.12558) |
| 2610.08970 | 2026 | HULK: Learning Whole-Body Forceful Loco-Manipulation for Humanoids | [リンク](https://arxiv.org/abs/2610.08970) |
| 2610.08320 | 2026 | Humanoid Horizon: Extending Task Horizon in Whole-Body Loco-Manipulation via ... | [リンク](https://arxiv.org/abs/2610.08320) |
| 2610.08120 | 2026 | iGPC: Generative Motion Priors for Object-Aware Humanoid Interaction | [リンク](https://arxiv.org/abs/2610.08120) |

### 2026 年の増減（TSV 内カウント）
2026年 65 件 / 2025年 29 件。

### 未開拓に見える方向
長期 multi-object の実機検証記述は TSV 上まだ sim 比率高め。

## 階層制御・Whole-Body Control アーキテクチャ（30 件）

### 解いている問題
VLA と低レベル WBC の分割統合。

### 主要な手法の対立軸
潜在 VLA + WBC vs 単層 / 手 crafted action 語彙 vs 学習

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.32909 | 2026 | HoloBoxing: A Simple Recipe for Humanoid Boxing with 7 Minutes of Single-GPU ... | [リンク](https://arxiv.org/abs/2610.32909) |
| 2610.19393 | 2026 | Beyond Kinematic Tracking: Preserving Expressive Characteristics in Humanoid ... | [リンク](https://arxiv.org/abs/2610.19393) |
| 2610.12972 | 2026 | Adaptive Whole-Body MPC with Optimal Posture Planning for Humanoid Robots und... | [リンク](https://arxiv.org/abs/2610.12972) |
| 2610.04231 | 2026 | Continual Humanoid Motion Learning | [リンク](https://arxiv.org/abs/2610.04231) |
| 2609.21100 | 2026 | Dynamics-Induced Commitment in Learning-Based Robotic Penalty Kicks | [リンク](https://arxiv.org/abs/2609.21100) |
| 2609.16405 | 2026 | Collision-Aware Humanoid Whole-Body Control under Imperfect Tracking Targets | [リンク](https://arxiv.org/abs/2609.16405) |
| 2609.03497 | 2026 | BRIDGE: An Open-Source Humanoid Platform via Morphology-Control Co-Design for... | [リンク](https://arxiv.org/abs/2609.03497) |
| 2607.04837 | 2026 | Athena-WBC: Capability-Aligned Policy Experts for Long-Tail Humanoid Whole-Bo... | [リンク](https://arxiv.org/abs/2607.04837) |
| 2606.25706 | 2026 | Learning Asynchronous Upper-body Task-space Trajectory Tracking Policy for Hu... | [リンク](https://arxiv.org/abs/2606.25706) |
| 2605.25546 | 2026 | Safety-Critical Whole-Body Control for Humanoid Robots via Input-to-State Saf... | [リンク](https://arxiv.org/abs/2605.25546) |
| 2605.14417 | 2026 | Before the Body Moves: Learning Anticipatory Joint Intent for Language-Condit... | [リンク](https://arxiv.org/abs/2605.14417) |
| 2604.21355 | 2026 | RPG: Robust Policy Gating for Smooth Multi-Skill Transitions in Humanoid Figh... | [リンク](https://arxiv.org/abs/2604.21355) |
| 2604.21351 | 2026 | Learn Weightlessness: Imitate Non-Self-Stabilizing Motions on Humanoid Robot | [リンク](https://arxiv.org/abs/2604.21351) |
| 2603.23983 | 2026 | SafeFlow: Real-Time Text-Driven Humanoid Whole-Body Control via Physics-Guide... | [リンク](https://arxiv.org/abs/2603.23983) |
| 2603.02856 | 2026 | Rhythm: Learning Interactive Whole-Body Control for Dual Humanoids | [リンク](https://arxiv.org/abs/2603.02856) |

### 2026 年の増減（TSV 内カウント）
2026年 18 件 / 2025年 8 件。

### 未開拓に見える方向
学習可能な action 語彙の自動獲得。

## 表情・上半身・コミュニケーション（22 件）

### 解いている問題
対人コミュニケーション向け表情・上半身模倣。

### 主要な手法の対立軸
人間→ヒューマノイド表情写像 vs 音声のみ

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.25288 | 2026 | Vision as Proprioception: Estimating Humanoid Robot Pose from Video | [リンク](https://arxiv.org/abs/2610.25288) |
| 2610.14269 | 2026 | RoboFake: Are Deepfake Detectors Ready for Humanoid Face Robots? | [リンク](https://arxiv.org/abs/2610.14269) |
| 2610.06153 | 2026 | Talk, Render, Act: Integrating Social Gesture and Digital Face with Synchroni... | [リンク](https://arxiv.org/abs/2610.06153) |
| 2609.33311 | 2026 | SocialHumanoid: Towards Expressive Humanoid Behavior via One-Step Co-Speech M... | [リンク](https://arxiv.org/abs/2609.33311) |
| 2609.32250 | 2026 | RoboSTAR: Next-Scale Autoregressive Sign Language Translation for Humanoid Ro... | [リンク](https://arxiv.org/abs/2609.32250) |
| 2608.28213 | 2026 | PAMoR: Parameterized Affective Motion Generation in Real Time for Humanoid Ro... | [リンク](https://arxiv.org/abs/2608.28213) |
| 2605.11825 | 2026 | Mapping Embodied Affective Touch Strategies on a Humanoid Robot | [リンク](https://arxiv.org/abs/2605.11825) |
| 2602.07506 | 2026 | VividFace: Real-Time and Realistic Facial Expression Shadowing for Humanoid R... | [リンク](https://arxiv.org/abs/2602.07506) |
| NowxIlTGtU | 2026 | X2C: Enabling Realistic Human-to-Humanoid Facial Expression Imitation | [リンク](https://openreview.net/forum?id=NowxIlTGtU) |
| 2512.17183 | 2025 | Semantic Co-Speech Gesture Synthesis and Real-Time Control for Humanoid Robots | [リンク](https://arxiv.org/abs/2512.17183) |
| 2505.24266 | 2025 | SignBot: Learning Human-to-Humanoid Sign Language Interaction | [リンク](https://arxiv.org/abs/2505.24266) |
| 2505.11146 | 2025 | X2C: A Large-Scale Benchmark for Nuanced Humanoid Facial Expression Imitation | [リンク](https://arxiv.org/abs/2505.11146) |
| 2504.14477 | 2025 | ExFace: Expressive Facial Control for Humanoid Robots with Diffusion Transfor... | [リンク](https://arxiv.org/abs/2504.14477) |
| 2503.16449 | 2025 | Affective and Conversational Predictors of Re-Engagement in Human-Robot Inter... | [リンク](https://arxiv.org/abs/2503.16449) |
| 2503.00284 | 2025 | Human-Robot Collaboration: A Non-Verbal Approach with the NAO Humanoid Robot | [リンク](https://arxiv.org/abs/2503.00284) |

### 2026 年の増減（TSV 内カウント）
2026年 9 件 / 2025年 6 件。

### 未開拓に見える方向
全身運動との同時制御統合。

## 学習効率・RL アルゴリズム (ヒューマノイド文脈)（47 件）

### 解いている問題
大規模 sim 前提の PPO 以外の効率的学習・ファインチューニング。

### 主要な手法の対立軸
on-policy PPO 大規模 sim vs off-policy 効率 / pretrain-finetune vs scratch

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.31608 | 2026 | Humanoid Mobility via Attention-based Contacts | [リンク](https://arxiv.org/abs/2610.31608) |
| 2610.30061 | 2026 | Test-Time Motion Steering for Perceptive Humanoid Fall Recovery | [リンク](https://arxiv.org/abs/2610.30061) |
| 2610.28925 | 2026 | One Policy, Many Styles: Where to Aggregate Preferences for Steerable Humanoi... | [リンク](https://arxiv.org/abs/2610.28925) |
| 2609.25674 | 2026 | Teaching Reinforcement Learning and Humanoid Robotics to High-School Students... | [リンク](https://arxiv.org/abs/2609.25674) |
| 2609.02222 | 2026 | FOCUS: Foot Observation Confidence for Robust Humanoid Proprioceptive Odometry | [リンク](https://arxiv.org/abs/2609.02222) |
| 2608.16195 | 2026 | RoboStriker: Latent-Space Strategic Games for Autonomous Humanoid Boxing | [リンク](https://arxiv.org/abs/2608.16195) |
| 2608.03227 | 2026 | PFM-HR: Pose Flow Matching for Humanoid Robots | [リンク](https://arxiv.org/abs/2608.03227) |
| 2608.00820 | 2026 | LooperMuscle: Fast and Stable Learning of Humanoid Whole-Body Tracking via St... | [リンク](https://arxiv.org/abs/2608.00820) |
| 2607.14182 | 2026 | Semantic Audio-driven Understanding for Dynamic Humanoid Whole Body Control | [リンク](https://arxiv.org/abs/2607.14182) |
| 2607.10815 | 2026 | Learning Roller-Skating Motions of Humanoid Robots Based on Adversarial Motio... | [リンク](https://arxiv.org/abs/2607.10815) |
| 2606.31807 | 2026 | Reinforcement Learning-Based Control for an Inline Skating Humanoid Robot | [リンク](https://arxiv.org/abs/2606.31807) |
| 2606.08253 | 2026 | Mind Your Steps: A General Learning Framework for Accurate Humanoid Foothold ... | [リンク](https://arxiv.org/abs/2606.08253) |
| 2604.12909 | 2026 | Tree Learning: A Multi-Skill Continual Learning Framework for Humanoid Robots | [リンク](https://arxiv.org/abs/2604.12909) |
| 2604.08509 | 2026 | Visually-grounded Humanoid Agents | [リンク](https://arxiv.org/abs/2604.08509) |
| 2603.12612 | 2026 | FastDSAC: Unlocking the Potential of Maximum Entropy RL in High-Dimensional H... | [リンク](https://arxiv.org/abs/2603.12612) |

### 2026 年の増減（TSV 内カウント）
2026年 19 件 / 2025年 22 件。

### 未開拓に見える方向
世界モデル連携 humanoid MBRL（WIMLE 等は humanoid TSV に混在するが主題は WM）。

## 汎用・その他のヒューマノイド研究（254 件）

### 解いている問題
上記横断の humanoid 研究。

### 主要な手法の対立軸
横断課題

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.40003 | 2026 | Humanoid Dodgeball: Learning Fast Dynamic Obstacle Avoidance Motions for Huma... | [リンク](https://arxiv.org/abs/2610.40003) |
| 2610.36789 | 2026 | A fully articulated humanoid dexterous hand with human-level joint structure ... | [リンク](https://arxiv.org/abs/2610.36789) |
| 2610.36452 | 2026 | Whole-Body Humanoid Control via Stochastic Motion Tokenization | [リンク](https://arxiv.org/abs/2610.36452) |
| 2610.33317 | 2026 | Active Reachability Learning for Humanoid Recoverability Monitoring | [リンク](https://arxiv.org/abs/2610.33317) |
| 2610.32277 | 2026 | Delay Randomization Widens the Delay Margin of Learned Humanoid Motion Trackers | [リンク](https://arxiv.org/abs/2610.32277) |
| 2610.30817 | 2026 | Robot Motion Transition with a Human Motion Prior | [リンク](https://arxiv.org/abs/2610.30817) |
| 2610.27162 | 2026 | Visual Task Modeling and Automated Planning for Humanoid Robots in Education ... | [リンク](https://arxiv.org/abs/2610.27162) |
| 2610.26043 | 2026 | OmniInteract: Towards Unified Whole-Body Interaction Control for Dual Humanoids | [リンク](https://arxiv.org/abs/2610.26043) |
| 2610.25711 | 2026 | SWAP: Test-Time Steerable Humanoid Whole-Body Collision Avoidance | [リンク](https://arxiv.org/abs/2610.25711) |
| 2610.24312 | 2026 | Beyond Human-Derived Motion: Exploring Robot-Specific Execution for Construct... | [リンク](https://arxiv.org/abs/2610.24312) |
| 2610.23127 | 2026 | BeJEPA: A Goal-Conditioned Humanoid Behavior World Model via Unsupervised RL | [リンク](https://arxiv.org/abs/2610.23127) |
| 2610.21515 | 2026 | TRACE: Typed Reference-Aware Conversational Editing for Humanoid Motion Diffu... | [リンク](https://arxiv.org/abs/2610.21515) |
| 2610.20606 | 2026 | Modeling and Understanding Neural Weights of Humanoid Policies with Diffusion | [リンク](https://arxiv.org/abs/2610.20606) |
| 2610.20579 | 2026 | PingpongDuo: Agile Humanoid Table Tennis Doubles with Safe Team Coordination | [リンク](https://arxiv.org/abs/2610.20579) |
| 2610.15073 | 2026 | Modeling and Control of a Rigid-soft Hybrid-link Humanoid Robot | [リンク](https://arxiv.org/abs/2610.15073) |

### 2026 年の増減（TSV 内カウント）
2026年 101 件 / 2025年 67 件。

### 未開拓に見える方向
ベンチマーク統一。

## 除外サンプル（最大 10 件）

- `mzLOnTb3WH` WIMLE: Uncertainty‑Aware World Models with IMLE for Sample‑E… — ヒューマノイドロボット制御・身体性が中核でない
- `JoK1hJg0Td` In-and-On: Scaling Egocentric Manipulation with in-the-wild … — ヒューマノイドロボット制御・身体性が中核でない
- `DIPeQTxpe7` Animating the Uncaptured: Humanoid Mesh Animation with Video… — CG/アニメーション中心で実機制御との関連が薄い
- `7lw6s9ELfr` MVR: Multi-view Video Reward Shaping for Reinforcement Learn… — ヒューマノイドロボット制御・身体性が中核でない
- `VBVCqm2t1J` ROBOWHEEL: A HELICAL DATA ENGINE FROM REAL-WORLD HUMAN DEMON… — ヒューマノイドロボット制御・身体性が中核でない
- `xlr3NqxUqY` Contact-guided Real2Sim from Monocular Video with Planar Sce… — ヒューマノイドロボット制御・身体性が中核でない
- `Ta98BucJY6` DHP: Discrete Hierarchical Planning for Hierarchical Reinfor… — ヒューマノイドロボット制御・身体性が中核でない
- `Cqdsw3yteP` Entropy Regularizing Activation: Boosting Continuous Control… — ヒューマノイドロボット制御・身体性が中核でない
- `f9u34Xxh6p` Guided Actor-Critic: Off-Policy Partially Observable Reinfor… — ヒューマノイドロボット制御・身体性が中核でない
- `CfZLxT3zIZ` FIRE: Frobenius-Isometry Reinitialization for Balancing the … — ヒューマノイドロボット制御・身体性が中核でない