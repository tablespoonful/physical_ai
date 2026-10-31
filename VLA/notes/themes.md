# VLA 論文テーマ別整理

調査基準日: 2026-10-31

## データソースと制約

- 入力: `titles_VLA.tsv` 全 1994 件（Web 検索・PDF 取得なし）。
- 各エントリの `date`, `arxiv_or_openreview_id`, `title`, `abstract`（先頭 300 字）のみに基づく分類。
- 出典 URL は ID から機械的に生成（ページ内容は未再確認）。arXiv: `https://arxiv.org/abs/<id>`、OpenReview: `https://openreview.net/forum?id=<id>`。

## 分類基準

1. **キーワードルール**: タイトル＋アブストラクト先頭 300 字に対し、下記テーマごとに正規表現パターンを定義。1 件が複数テーマに該当しうる。
2. **主テーマ（件数集計）**: 複数該当時は優先順位 評価・ベンチマーク・分析 → 安全性・攻撃・信頼性 → データ・事前学習・シミュレーション → 応用領域（自動運転・移動・ヒューマノイド等） → 空間・3D・本体感覚 → 記憶・長期・非マルコフ → RL・経験・ポリシー改善 → 推論・計画・世界モデル・デュアルシステム → 効率化・トークナイザ・MoE・軽量化 → 行動表現・生成方式（AR / Diffusion / Flow） → VLM適応・基盤VLA・指示追従 → 未該当は「VLM適応・基盤VLA・指示追従」にフォールバック。
3. **代表論文**: 各主テーマから 5〜15 件。arXiv ID 付きを優先し、タイトル先頭 40 字で重複を除き、年が新しい順に選定。 主テーマ以外でも当該テーマのキーワードに該当する重要論文（例: OpenVLA がデータ＋VLM 適応の両方）は、該当テーマの代表リストに含めうる。
4. **年次**: `date` 列の先頭 4 桁。2026 行は会議投稿（OpenReview ID）が多く、arXiv 日付と一致しない場合がある。

## 全体サマリ

| 年 | 件数 |
| --- | ---: |
| 2017 | 2 |
| 2018 | 3 |
| 2019 | 3 |
| 2020 | 5 |
| 2021 | 12 |
| 2022 | 36 |
| 2023 | 87 |
| 2024 | 109 |
| 2025 | 417 |
| 2026 | 1320 |

主テーマ別件数（相互排他）:

| テーマ | 件数 |
| --- | ---: |
| 評価・ベンチマーク・分析 | 161 |
| 安全性・攻撃・信頼性 | 78 |
| データ・事前学習・シミュレーション | 243 |
| 応用領域（自動運転・移動・ヒューマノイド等） | 202 |
| 空間・3D・本体感覚 | 128 |
| 記憶・長期・非マルコフ | 145 |
| RL・経験・ポリシー改善 | 90 |
| 推論・計画・世界モデル・デュアルシステム | 160 |
| 効率化・トークナイザ・MoE・軽量化 | 135 |
| 行動表現・生成方式（AR / Diffusion / Flow） | 69 |
| VLM適応・基盤VLA・指示追従 | 583 |

キーワード該当件数（重複カウント可）:

| テーマ | 該当件数 |
| --- | ---: |
| 評価・ベンチマーク・分析 | 161 |
| 安全性・攻撃・信頼性 | 95 |
| データ・事前学習・シミュレーション | 257 |
| 応用領域（自動運転・移動・ヒューマノイド等） | 269 |
| 空間・3D・本体感覚 | 198 |
| 記憶・長期・非マルコフ | 193 |
| RL・経験・ポリシー改善 | 148 |
| 推論・計画・世界モデル・デュアルシステム | 381 |
| 効率化・トークナイザ・MoE・軽量化 | 308 |
| 行動表現・生成方式（AR / Diffusion / Flow） | 183 |
| VLM適応・基盤VLA・指示追従 | 289 |

キーワード未該当でフォールバックした件数（VLM適応・基盤VLA・指示追従 主テーマ）: 583。

---

## 評価・ベンチマーク・分析

**件数（主テーマ）**: 161

### 解いている問題

VLA の能力を何で・どう測るか、報告性能と実部署耐性のギャップをどう可視化するか。

### 主要な手法の対立軸

タスクベンチ vs 摂動・攻撃ベンチ / 成功率単指標 vs 多次元ロバストネス / 再現プロトコル統一 vs モデル固有評価。

### 代表論文（5〜15 本、一覧より）

- **RADAR: Benchmarking Vision-Language-Action Generalization via Real-World Dynamics, Spatial-Physical Intelligence, and Autonomous Evaluation** — arXiv:2602.10980 — 出典: https://arxiv.org/abs/2602.10980
- **Robust Skills, Brittle Grounding: Diagnosing Restricted Generalization in Vision-Language Action Policies via Multi-Object Picking** — arXiv:2602.24143 — 出典: https://arxiv.org/abs/2602.24143
- **Is Success All You Need? Investigating the Impact of Input Perturbations on VLA Behaviour in Tabletop Manipulation Tasks** — arXiv:2610.01351 — 出典: https://arxiv.org/abs/2610.01351
- **RoboSeed: Multidimensional Evaluation of Vision-Language-Action and World-Action Models: Capability, Resource Affordability, and Research Evidence** — arXiv:2610.40026 — 出典: https://arxiv.org/abs/2610.40026
- **VLAGuard: A Framework for Evaluating and Mitigating Physical Attention Hijacking in Vision-Language-Action Robots within Wireless Sensor Networks** — arXiv:2608.01028 — 出典: https://arxiv.org/abs/2608.01028
- **CMU-Drive and V2V-VLA: Cooperative Multi-agent Unified Driving with Reasoning Benchmark and Vehicle-to-Vehicle Vision-Language-Action Models** — arXiv:2608.07621 — 出典: https://arxiv.org/abs/2608.07621
- **Pedagogical Alignment for Vision-Language-Action Models: A Comprehensive Framework for Data, Architecture, and Evaluation in Education** — arXiv:2601.13876 — 出典: https://arxiv.org/abs/2601.13876
- **When Faster VLA Deployment Changes Closed-Loop Behavior: Task Success-Latency Analysis of SmolVLA Across PyTorch and ONNX Variants** — arXiv:2609.14146 — 出典: https://arxiv.org/abs/2609.14146
- **Closing the Lab-to-Store Gap: A Data-Efficient Post-Training and Experience-Driven Learning VLA Framework for Retail Humanoids** — arXiv:2607.20345 — 出典: https://arxiv.org/abs/2607.20345
- **Beyond Reconstruction Error: Analytical and Data-Driven Action Tokenization for Autoregressive Vision-Language-Action Models** — arXiv:2609.25820 — 出典: https://arxiv.org/abs/2609.25820
- **SEVO: Semantic-Enhanced Virtual Observation for Robust VLA Manipulation via Active Illumination and Data-Centric Collection** — arXiv:2605.11114 — 出典: https://arxiv.org/abs/2605.11114
- **When Does Language Matter? Multilingual Instructions Reveal Step-wise Language Sensitivity in Vision-Language-Action Models** — arXiv:2606.11906 — 出典: https://arxiv.org/abs/2606.11906
- **A Persian Vision-Language-Action Dataset and Benchmark for Ambiguity- and Infeasibility-Aware Instruction-to-Plan Grounding** — arXiv:2610.15666 — 出典: https://arxiv.org/abs/2610.15666
- **RoboCasa-Shift: Stage-Aware Robustness Evaluation of Vision-Language-Action Policies in Long-Horizon Household Manipulation** — arXiv:2610.27861 — 出典: https://arxiv.org/abs/2610.27861
- **LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination** — arXiv:2606.10862 — 出典: https://arxiv.org/abs/2606.10862

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 161（2025: 31, 2026: 118）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

実機・長期運用・マルチモーダル摂動を同時に扱う標準プロトコル、オープンリーダーボードの不足。

---

## 安全性・攻撃・信頼性

**件数（主テーマ）**: 78

### 解いている問題

指示・視覚・行動経路への悪用、失敗時の物理的リスクをどう定量化・緩和するか。

### 主要な手法の対立軸

検知 vs 堅牢学習 / デジタル攻撃 vs 物理摂動 / 不確実性注入 vs 明示的安全制約。

### 代表論文（5〜15 本、一覧より）

- **Capability and Robustness Cannot Both Be Free: An Information-Theoretic Bound for Vision-Language-Action Models** — arXiv:2605.25889 — 出典: https://arxiv.org/abs/2605.25889
- **State Backdoor: Towards Stealthy Real-world Poisoning Attack on Vision-Language-Action Model in State Space** — arXiv:2601.04266 — 出典: https://arxiv.org/abs/2601.04266
- **CycleVLA: Proactive Self-Correcting Vision-Language-Action Models via Subtask Backtracking and Minimum Bayes Risk Decoding** — arXiv:2601.02295 — 出典: https://arxiv.org/abs/2601.02295
- **Safe-Night VLA: Seeing the Unseen via Thermal-Perceptive Vision-Language-Action Models for Safety-Critical Manipulation** — arXiv:2603.05754 — 出典: https://arxiv.org/abs/2603.05754
- **ATAAT: Adaptive Threat-Aware Adversarial Tuning Framework against Backdoor Attacks on Vision-Language-Action Models** — arXiv:2605.08612 — 出典: https://arxiv.org/abs/2605.08612
- **SAFE-Pruner: Semantic Attention-Guided Future-Aware Token Pruning for Efficient Vision-Language-Action Manipulation** — arXiv:2605.29662 — 出典: https://arxiv.org/abs/2605.29662
- **CoFreeVLA: Short-Horizon Collision-Free Dual-Arm Manipulation via Vision-Language-Action Model and Risk Estimation** — arXiv:2601.21712 — 出典: https://arxiv.org/abs/2601.21712
- **VLA-Hijack: A Transferable Patch Attack against Vision-Language-Action Models via Visual Proprioception Hijacking** — arXiv:2605.28083 — 出典: https://arxiv.org/abs/2605.28083
- **ReasonBreak: Probing Vulnerabilities in Reasoning-Enabled Vision-Language-Action Models for Autonomous Driving** — arXiv:2605.29114 — 出典: https://arxiv.org/abs/2605.29114
- **LIBERO-VIFO: Benchmarking the Capability and Safety of Visual Cue Following in Vision-Language-Action Models** — arXiv:2608.17600 — 出典: https://arxiv.org/abs/2608.17600
- **MedVLA: A Hierarchical Vision-Language-Action Framework for Closed-Loop Precision Medical Robot Manipulation** — arXiv:2609.25756 — 出典: https://arxiv.org/abs/2609.25756
- **Seeing the Invisible: Physics-Guided Visual Prompting for Temperature- and Radiation-Aware VLA Navigation** — arXiv:2610.07558 — 出典: https://arxiv.org/abs/2610.07558
- **Bit-Flip Attacks on Vision-Language-Action Models: Action-Decoding Architecture Shapes the Vulnerability** — arXiv:2608.15475 — 出典: https://arxiv.org/abs/2608.15475
- **Measuring the Reasoning-Action Coupling in Driving Vision-Language-Action Models through Counterfactuals** — arXiv:2610.30953 — 出典: https://arxiv.org/abs/2610.30953
- **HiST-VLA: A Hierarchical Spatio-Temporal Vision-Language-Action Model for End-to-End Autonomous Driving** — arXiv:2602.13329 — 出典: https://arxiv.org/abs/2602.13329

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 78（2025: 13, 2026: 62）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

安全制約下 RL、認証可能なポリシー、ヒューマンインザループ安全の統合評価。

---

## データ・事前学習・シミュレーション

**件数（主テーマ）**: 243

### 解いている問題

人手デモのコスト、シムギャップ、エンボディメント heterogeneity をどうデータ設計で吸収するか。

### 主要な手法の対立軸

人間動画 vs ロボットデモ / 合成拡張 vs キュレーション / 単一ロボ vs cross-embodiment 混合。

### 代表論文（5〜15 本、一覧より）

- **From Human Videos to Robot Manipulation: A Survey on Scalable Vision-Language-Action Learning with Human-Centric Data** — arXiv:2606.00054 — 出典: https://arxiv.org/abs/2606.00054
- **Grounding Sim-to-Real Generalization in Robotic Manipulation: An Empirical Study with Vision-Language-Action Models** — arXiv:2603.22876 — 出典: https://arxiv.org/abs/2603.22876
- **OpenVLA: An Open-Source Vision-Language-Action Model** — arXiv:2406.09246 — 出典: https://arxiv.org/abs/2406.09246
- **SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning** — arXiv:2509.09674 — 出典: https://arxiv.org/abs/2509.09674
- **SAMBAR: Selective Anchoring via Method of Multipliers for Balanced Knowledge Acquisition and Retention in Vision-Language-Action Models** — arXiv:2609.32108 — 出典: https://arxiv.org/abs/2609.32108
- **Uncertainty-Gated Exploration Noise Suppresses Task Collapse in Online RL Fine-Tuning of a Flow-Matching Vision-Language-Action Policy** — arXiv:2609.28838 — 出典: https://arxiv.org/abs/2609.28838
- **TANDEM: Task and Motion Planning with As-Needed Demonstrations for Efficient Vision-Language-Action Model Fine-tuning** — arXiv:2609.28314 — 出典: https://arxiv.org/abs/2609.28314
- **Direction-Scale Decomposition in Action Representation: Rethinking What to Tokenize for Vision-Language-Action Models** — arXiv:2609.28865 — 出典: https://arxiv.org/abs/2609.28865
- **FineART: Fine-Grained Annotated Robotic Trajectory Dataset and Vision-Language-Action Model for Bimanual Manipulation** — arXiv:2609.36416 — 出典: https://arxiv.org/abs/2609.36416
- **Does VLA Even Know the Basics? Measuring Commonsense and World Knowledge Retention in Vision-Language-Action Models** — arXiv:2606.19297 — 出典: https://arxiv.org/abs/2606.19297
- **SimpleTouch: Can Vision-Language-Action Models Master Contact-Rich Manipulation Without Tactile Policy Pretraining?** — arXiv:2610.02784 — 出典: https://arxiv.org/abs/2610.02784
- **VISTA: Enhancing Visual Conditioning via Track-Following Preference Optimization in Vision-Language-Action Models** — arXiv:2602.05049 — 出典: https://arxiv.org/abs/2602.05049
- **AffordanceVLA: A Vision-Language-Action Model Empowering Action Generation through Affordance-Aware Understanding** — arXiv:2606.06155 — 出典: https://arxiv.org/abs/2606.06155
- **EATR-Stereo: Embodiment-Aware Token Routing of Paired Stereo Evidence for Humanoid Vision-Language-Action Control** — arXiv:2608.17453 — 出典: https://arxiv.org/abs/2608.17453
- **PhaseLoRA: Control-Regime-Conditioned Low-Rank Adaptation for Continuous-Action Vision-Language-Action Policies** — arXiv:2608.15285 — 出典: https://arxiv.org/abs/2608.15285

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 243（2025: 55, 2026: 153）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

ライセンス明確な大規模実世界データ、失敗軌道・修正軌道の体系収集。

---

## 応用領域（自動運転・移動・ヒューマノイド等）

**件数（主テーマ）**: 202

### 解いている問題

汎用 VLA を特定ドメイン（運転、移動操作、動的把持等）の制約下で使えるようにするか。

### 主要な手法の対立軸

2D 画像運転 vs 3D シーン / 室内移動 vs 固定アーム / 静的 vs 動的環境。

### 代表論文（5〜15 本、一覧より）

- **AutoMoT: A Unified Vision-Language-Action Model with Asynchronous Mixture-of-Transformers for End-to-End Autonomous Driving** — arXiv:2603.14851 — 出典: https://arxiv.org/abs/2603.14851
- **GR00T N1: An Open Foundation Model for Generalist Humanoid Robots** — arXiv:2503.14734 — 出典: https://arxiv.org/abs/2503.14734
- **AgenticTactileVLA: Contact-Guided Execution-Time Supervision for Generalizable Dexterous Manipulation without VLA Retraining** — arXiv:2610.04391 — 出典: https://arxiv.org/abs/2610.04391
- **BiliVLA: Scene-Aware Vision-Language-Action Model with Reinforcement Learning for Autonomous Biliary Endoscopic Navigation** — arXiv:2606.23531 — 出典: https://arxiv.org/abs/2606.23531
- **HAF: Adapting Generalist VLAs to Humanoid Whole-Body Loco-manipulation via Hierarchical Action Flow and Spectral Latent RL** — arXiv:2608.16837 — 出典: https://arxiv.org/abs/2608.16837
- **ETA-VLA: Efficient Token Adaptation via Temporal Fusion and Intra-LLM Sparsification for Vision-Language-Action Models** — arXiv:2603.25766 — 出典: https://arxiv.org/abs/2603.25766
- **DR-VLA: Learning Human-Like Quadruped Navigation from Egocentric Web Videos via Domain-Invariant Scene Representations** — arXiv:2610.18373 — 出典: https://arxiv.org/abs/2610.18373
- **CLIFT: Turning Gemini Robotics On-Device into Humanoid Specialists via Non-Invasive Closed-Loop Iterative Fine-Tuning** — arXiv:2607.29172 — 出典: https://arxiv.org/abs/2607.29172
- **DeCAL: Towards Physically-Grounded Dexterous Vision-Language-Action Models via Contact-Aware Latent Co-Imagination** — arXiv:2609.09119 — 出典: https://arxiv.org/abs/2609.09119
- **BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models** — arXiv:2605.30226 — 出典: https://arxiv.org/abs/2605.30226
- **Reflect-VLA: Internalizing Reflective Guidance via Dual-Path On-Policy Self-Distillation for Autonomous Driving** — arXiv:2610.13453 — 出典: https://arxiv.org/abs/2610.13453
- **DexHiL: A Human-in-the-Loop Framework for Vision-Language-Action Model Post-Training in Dexterous Manipulation** — arXiv:2603.09121 — 出典: https://arxiv.org/abs/2603.09121
- **S-squared-VLA: Decoupling Semantic and Spatial Streams in Vision-Language-Action Models for Autonomous Driving** — arXiv:2607.13926 — 出典: https://arxiv.org/abs/2607.13926
- **HapticVLA: Contact-Rich Manipulation via Vision-Language-Action Model without Inference-Time Tactile Sensing** — arXiv:2603.15257 — 出典: https://arxiv.org/abs/2603.15257
- **SpanVLA: Learning from Negative-Recovery Samples with Fast Action Bridging for Vision-Language-Action Model** — arXiv:2604.19710 — 出典: https://arxiv.org/abs/2604.19710

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 202（2025: 45, 2026: 139）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

ドメイン横断の単一ポリシー vs ドメイン特化アダプタの設計指針、長尾イベントデータ。

---

## 空間・3D・本体感覚

**件数（主テーマ）**: 128

### 解いている問題

VLM の 2D 言語偏りを補い、操作・運転に必要な 3D/空間・本体感覚を VLA に組み込むか。

### 主要な手法の対立軸

明示 3D 表現 vs 暗黙 occupancy 教師 / 視覚のみ vs proprio 能動推論 / 幾何ヘッド vs  end-to-end。

### 代表論文（5〜15 本、一覧より）

- **ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation** — arXiv:2601.08325 — 出典: https://arxiv.org/abs/2601.08325
- **3DThinkVLA: Endowing Vision-Language-Action Models with Latent 3D Priors via 3D-Thinking-Guided Co-training** — arXiv:2606.04436 — 出典: https://arxiv.org/abs/2606.04436
- **IMPACT-VLA: Interaction-aware Multimodal Propagation Attribution via Counterfactual Trajectories for Vision-Language-Action Policies** — arXiv:2609.15005 — 出典: https://arxiv.org/abs/2609.15005
- **StemVLA:An Open-Source Vision-Language-Action Model with Future 3D Spatial Geometry Knowledge and 4D Historical Representation** — arXiv:2602.23721 — 出典: https://arxiv.org/abs/2602.23721
- **ExecVLA: Following Fine-Grained Execution Constraints in Vision-Language-Action Models with Bi-Level Action Representation** — arXiv:2603.17524 — 出典: https://arxiv.org/abs/2603.17524
- **Recurrent-Depth VLA: Implicit Test-Time Compute Scaling of Vision-Language-Action Models via Latent Iterative Reasoning** — arXiv:2602.07845 — 出典: https://arxiv.org/abs/2602.07845
- **AWARE: Action-Entropy-Weighted and Attention-Guided Retrieval of Observation Evidence for Vision-Language-Action Models** — arXiv:2602.18020 — 出典: https://arxiv.org/abs/2602.18020
- **BridgeVLA++: A Data-Efficient, Generalizable, and Memory-Augmented Vision-Language-Action Framework for 3D Manipulation** — arXiv:2608.05042 — 出典: https://arxiv.org/abs/2608.05042
- **3D HAMSTER: Bridging Planning and Control in Hierarchical Vision Language Action Models through 3D Trajectory Guidance** — arXiv:2606.31329 — 出典: https://arxiv.org/abs/2606.31329
- **DySL-VLA: Efficient Vision-Language-Action Model Inference via Dynamic-Static Layer-Skipping for Robot Manipulation** — arXiv:2602.22896 — 出典: https://arxiv.org/abs/2602.22896
- **3D-Mix for VLA: A Plug-and-Play Module for Integrating VGGT-based 3D Information into Vision-Language-Action Models** — arXiv:2603.24393 — 出典: https://arxiv.org/abs/2603.24393
- **2D or 3D: Who Governs Salience in VLA Models? -- Tri-Stage Token Pruning Framework with Modality Salience Awareness** — arXiv:2604.09244 — 出典: https://arxiv.org/abs/2604.09244
- **AeroManip-VLA: Scalable Vision-Language-Action Learning for Aerial Manipulation with RL-Generated Demonstrations** — arXiv:2609.36915 — 出典: https://arxiv.org/abs/2609.36915
- **ARIES-Mission2: A Zero-Shot Vision-Language-Action Framework for Fast Large-Scale Aerial Mission Generation** — arXiv:2608.12763 — 出典: https://arxiv.org/abs/2608.12763
- **XS-VLA: Teaching Tiny Vision-Language-Action Models with Spatial Supervision and Demonstration Conditioning** — arXiv:2607.04171 — 出典: https://arxiv.org/abs/2607.04171

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 128（2025: 24, 2026: 80）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

軽量で校正可能な空間表現、シミュレータ非依存の 3D 教師信号。

---

## 記憶・長期・非マルコフ

**件数（主テーマ）**: 145

### 解いている問題

部分観測・多段タスクで Markov 仮定が破れるとき、過去情報をどう保持・更新するか。

### 主要な手法の対立軸

外部メモリ vs 潜在状態 / 言語要約 vs 連続埋め込み / オンライン更新 vs 固定コンテキスト。

### 代表論文（5〜15 本、一覧より）

- **From Sliding Windows to Self-evolving Lifelong Memory: A Dual-perspective Survey of Memory Paradigms for Long-Horizon Robotics VLA Models** — arXiv:2610.23319 — 出典: https://arxiv.org/abs/2610.23319
- **The Price Is Not Right: Neuro-Symbolic Methods Outperform VLAs on Structured Long-Horizon Manipulation Tasks with Significantly Lower Energy Consumption** — arXiv:2602.19260 — 出典: https://arxiv.org/abs/2602.19260
- **VLA-Corrector: Stage-Aware Observable State Understanding for Prompt-Based Closed-Loop Recovery of Vision-Language-Action Policies** — arXiv:2609.06508 — 出典: https://arxiv.org/abs/2609.06508
- **Global Prior Meets Local Consistency: Dual-Memory Augmented Vision-Language-Action Model for Efficient Robotic Manipulation** — arXiv:2602.20200 — 出典: https://arxiv.org/abs/2602.20200
- **RoboHarness: A Memory-Augmented Policy Harness for Vision-Language-Action Model Robustness via In-Context Adaptation** — arXiv:2603.24060 — 出典: https://arxiv.org/abs/2603.24060
- **CommitFlow: Semantic Commitment Verification and Local Correction for Long-Horizon Robot Manipulation VLA Execution** — arXiv:2609.21908 — 出典: https://arxiv.org/abs/2609.21908
- **PF-RL: Progress Field Reinforcement Learning via Goal-Conditioned Value Geometry for Vision-Language-Action Models** — arXiv:2609.32634 — 出典: https://arxiv.org/abs/2609.32634
- **PhysReflect-VLA: Physical Feasibility and Self-Reflective Regulation for Reliable Vision-Language-Action Policies** — arXiv:2606.27146 — 出典: https://arxiv.org/abs/2606.27146
- **ChainVLA: Chaining Vision-Language-Action Queries through a Unified Execution State for Long-Horizon Manipulation** — arXiv:2608.02326 — 出典: https://arxiv.org/abs/2608.02326
- **Retrieval-triggered Action Projection Adjustment for Frozen VLA Policies: An Empirical Study and Failure Analysis** — arXiv:2610.24573 — 出典: https://arxiv.org/abs/2610.24573
- **ActMem-VLA: Action-History Memory with Dual-Expert Denoising for Long-Horizon Vision-Language-Action Policies** — arXiv:2609.37307 — 出典: https://arxiv.org/abs/2609.37307
- **MMaDA-VLA: Large Diffusion Vision-Language-Action Model with Unified Multi-Modal Instruction and Generation** — arXiv:2603.25406 — 出典: https://arxiv.org/abs/2603.25406
- **CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models** — arXiv:2604.22238 — 出典: https://arxiv.org/abs/2604.22238
- **Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts** — arXiv:2605.22446 — 出典: https://arxiv.org/abs/2605.22446
- **StateMem: Single-State Residual Memory with Adaptive Inference for Vision-Language-Action Policies** — arXiv:2609.22684 — 出典: https://arxiv.org/abs/2609.22684

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 145（2025: 26, 2026: 111）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

長期記憶とリアルタイム制御の両立、忘却と再学習の評価。

---

## RL・経験・ポリシー改善

**件数（主テーマ）**: 90

### 解いている問題

模倣だけでは足りない改善（デプロイ後経験、段階報酬、批評家）を VLA にどう載せるか。

### 主要な手法の対立軸

軌道レベル RL vs トークン RL / 人手修正 vs 自動 advantage / オンライン vs バッチ fine-tune。

### 代表論文（5〜15 本、一覧より）

- **SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning** — arXiv:2509.09674 — 出典: https://arxiv.org/abs/2509.09674
- **$π^{*}_{0.6}$: a VLA That Learns From Experience** — arXiv:2511.14759 — 出典: https://arxiv.org/abs/2511.14759
- **Reinforcement Fine-Tuning of Flow-Matching Policies for Vision-Language-Action Models** — arXiv:2510.09976 — 出典: https://arxiv.org/abs/2510.09976
- **Leveraging Offline Supervision for Efficient and Generalizable Reinforcement Learning in Large-Scale Vision-Language-Action Models** — arXiv:2607.19399 — 出典: https://arxiv.org/abs/2607.19399
- **Generalists Act, Specialists Intervene: Modular Stage-Selective Reinforcement Learning for Vision-Language-Action Manipulation** — arXiv:2609.26467 — 出典: https://arxiv.org/abs/2609.26467
- **AcceRL: A Distributed Asynchronous Reinforcement Learning and World Model Framework for Vision-Language-Action Models** — arXiv:2603.18464 — 出典: https://arxiv.org/abs/2603.18464
- **D-VLA: A High-Concurrency Distributed Asynchronous Reinforcement Learning Framework for Vision-Language-Action Models** — arXiv:2605.13276 — 出典: https://arxiv.org/abs/2605.13276
- **Recovering Low-Bit Failures in Vision-Language-Action Policies via Quantization-Conditioned Reinforcement Learning** — arXiv:2610.15675 — 出典: https://arxiv.org/abs/2610.15675
- **What Frozen VLAs Already Know About Success: A Probing Study of Value-Like Structure in Foundation Robot Policies** — arXiv:2605.28527 — 出典: https://arxiv.org/abs/2605.28527
- **dVLA-RL: Reinforcement Learning over Denoising Trajectories for Discrete Diffusion Vision-Language-Action Models** — arXiv:2606.23623 — 出典: https://arxiv.org/abs/2606.23623
- **Simple Recipe Works: Vision-Language-Action Models are Natural Continual Learners with Reinforcement Learning** — arXiv:2603.11653 — 出典: https://arxiv.org/abs/2603.11653
- **FlowPRO: Reward-Free Reinforced Fine-Tuning of Flow-Matching VLAs via Proximalized Preference Optimization** — arXiv:2606.05468 — 出典: https://arxiv.org/abs/2606.05468
- **DyGRO-VLA: Cross-Task Scaling of Vision-Language-Action Models via Dynamic Grouped Residual Optimization** — arXiv:2605.17486 — 出典: https://arxiv.org/abs/2605.17486
- **VLaRL: Augmenting Vision-Language-Action Models with Simulation-Trained Latent-Conditioned Residual RL** — arXiv:2609.30868 — 出典: https://arxiv.org/abs/2609.30868
- **Find Something You Can't Do: Agentic Real-World Reinforcement Learning for Self-Improving VLA Models** — arXiv:2609.32069 — 出典: https://arxiv.org/abs/2609.32069

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 90（2025: 23, 2026: 58）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

サンプル効率の良い VLA-RL、理論保証と大規模 VLM バックボーンの両立。

---

## 推論・計画・世界モデル・デュアルシステム

**件数（主テーマ）**: 160

### 解いている問題

言語・視覚理解を実行可能な中間表現（計画、CoT、世界表現）に変換し latency と精度を両立するか。

### 主要な手法の対立軸

明示 CoT vs 潜在計画 / 単一システム vs dual-system / モデルベース vs 方策のみ。

### 代表論文（5〜15 本、一覧より）

- **MoTVLA: A Vision-Language-Action Model with Unified Fast-Slow Reasoning** — arXiv:2510.18337 — 出典: https://arxiv.org/abs/2510.18337
- **Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning** — arXiv:2601.09708 — 出典: https://arxiv.org/abs/2601.09708
- **HybridVLA: Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model** — arXiv:2503.10631 — 出典: https://arxiv.org/abs/2503.10631
- **BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation** — arXiv:2605.07306 — 出典: https://arxiv.org/abs/2605.07306
- **When to Ask for Help: A Decision-Theoretic Account and Measurement Standard for Slow-Module Scheduling in Dual-System Vision-Language-Action Models** — arXiv:2610.21160 — 出典: https://arxiv.org/abs/2610.21160
- **H-VLA: Hierarchical Vision-Language-Action Model with Key-Action Reasoning and Motion Planning in a Unified Action Space** — arXiv:2609.22895 — 出典: https://arxiv.org/abs/2609.22895
- **In-Context VLA: Endowing Vision-Language-Action Models with Language via In-Context Post-Training and Agentic Tool Use** — arXiv:2608.05738 — 出典: https://arxiv.org/abs/2608.05738
- **Differentiate-and-Inject: Enhancing VLAs via Functional Differentiation Induced by In-Parameter Structural Reasoning** — arXiv:2602.07541 — 出典: https://arxiv.org/abs/2602.07541
- **ATA: Bridging Implicit Reasoning with Attention-Guided and Action-Guided Inference for Vision-Language Action Models** — arXiv:2603.01490 — 出典: https://arxiv.org/abs/2603.01490
- **Latency-Tolerant Cloud-Edge Collaborative Vision-Language-Action Models via Emergent Representational Specialization** — arXiv:2608.00569 — 出典: https://arxiv.org/abs/2608.00569
- **From Inference Efficiency to Embodied Efficiency: Revisiting Efficiency Metrics for Vision-Language-Action Models** — arXiv:2603.19131 — 出典: https://arxiv.org/abs/2603.19131
- **Fast Plans, Faithful Actions: Closing the Planning-Execution Gap in Hierarchical Vision-Language-Action Models** — arXiv:2609.30833 — 出典: https://arxiv.org/abs/2609.30833
- **Inject Once Survive Later: Backdooring Vision-Language-Action Models to Persist Through Downstream Fine-tuning** — arXiv:2602.00500 — 出典: https://arxiv.org/abs/2602.00500
- **Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery** — arXiv:2605.01191 — 出典: https://arxiv.org/abs/2605.01191
- **Imagine the Future, Internalize the Gist: Efficient VLA Reasoning via Internalized Spatiotemporal Imagination** — arXiv:2610.02626 — 出典: https://arxiv.org/abs/2610.02626

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 160（2025: 41, 2026: 88）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

推論の検証可能性、推論失敗時のフォールバック制御。

---

## 効率化・トークナイザ・MoE・軽量化

**件数（主テーマ）**: 135

### 解いている問題

高頻度制御・エッジデプロイ向けに推論コスト（トークン長、モデルサイズ）を削るか。

### 主要な手法の対立軸

学習可能トークナイザ vs 固定離散化 / MoE vs 小型 dense / 蒸留 vs アーキテクチャ変更。

### 代表論文（5〜15 本、一覧より）

- **FAST: Efficient Action Tokenization for Vision-Language-Action Models** — arXiv:2501.09747 — 出典: https://arxiv.org/abs/2501.09747
- **SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics** — arXiv:2506.01844 — 出典: https://arxiv.org/abs/2506.01844
- **EdgeVLA: Efficient Vision-Language-Action Models** — arXiv:2507.14049 — 出典: https://arxiv.org/abs/2507.14049
- **ActTune: Action-Aware Precision and GPU Operating-Point Adaptation for Energy-Efficient Vision-Language-Action Inference** — arXiv:2610.08444 — 出典: https://arxiv.org/abs/2610.08444
- **AC^2-VLA: Action-Context-Aware Adaptive Computation in Vision-Language-Action Models for Efficient Robotic Manipulation** — arXiv:2601.19634 — 出典: https://arxiv.org/abs/2601.19634
- **FastVLA: Task-Conditioned and Temporally Adaptive Visual Token Compression for Efficient Vision-Language-Action Models** — arXiv:2610.22146 — 出典: https://arxiv.org/abs/2610.22146
- **AIR-VLA+: Decoupling Movement and Manipulation via Cascaded Dual-Action Decoders with Asymmetric MoE for Aerial Robots** — arXiv:2606.12859 — 出典: https://arxiv.org/abs/2606.12859
- **Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models** — arXiv:2606.25985 — 出典: https://arxiv.org/abs/2606.25985
- **CereVLA: Cerebellum-Inspired Consequence-Aware Residual Governance for Efficient Vision-Language-Action Execution** — arXiv:2609.27468 — 出典: https://arxiv.org/abs/2609.27468
- **Beyond Attention Magnitude: Leveraging Inter-layer Rank Consistency for Efficient Vision-Language-Action Models** — arXiv:2603.24941 — 出典: https://arxiv.org/abs/2603.24941
- **Acting While Understanding: Asynchronous Semantic-Action Decoupling for Real-Time Vision-Language-Action Models** — arXiv:2606.15285 — 出典: https://arxiv.org/abs/2606.15285
- **EcoVLA: Energy-Efficient Device-Edge Co-Inference for Vision-Language-Action Models under Real-Time Constraints** — arXiv:2608.15502 — 出典: https://arxiv.org/abs/2608.15502
- **Text-Vision Synergistic Token Caching: A Training-Free Framework for Efficient Vision-Language-Action Inference** — arXiv:2609.34319 — 出典: https://arxiv.org/abs/2609.34319
- **Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** — arXiv:2602.00780 — 出典: https://arxiv.org/abs/2602.00780
- **StreamingVLA: Streaming Vision-Language-Action Model with Action Flow Matching and Adaptive Early Observation** — arXiv:2603.28565 — 出典: https://arxiv.org/abs/2603.28565

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 135（2025: 30, 2026: 92）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

効率化が汎化・安全性を損なわない条件の体系的理解。

---

## 行動表現・生成方式（AR / Diffusion / Flow）

**件数（主テーマ）**: 69

### 解いている問題

連続行動をどう離散化・生成し、誤差蓄積・時間剛性・多峰性をどう扱うか。

### 主要な手法の対立軸

自己回帰 vs diffusion vs flow / 単步 vs 軌道 / ハイブリッド統合 vs 単一パラダイム。

### 代表論文（5〜15 本、一覧より）

- **HybridVLA: Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model** — arXiv:2503.10631 — 出典: https://arxiv.org/abs/2503.10631
- **FAST: Efficient Action Tokenization for Vision-Language-Action Models** — arXiv:2501.09747 — 出典: https://arxiv.org/abs/2501.09747
- **CrossVLA: Cross-Paradigm Post-Training and Inference Optimization for Vision-Language-Action Models** — arXiv:2605.21854 — 出典: https://arxiv.org/abs/2605.21854
- **The Lie We Tell: Correcting the Euclidean Fallacy in Vision Language Action Policies via Score Matching on Tangent Space** — arXiv:2606.01847 — 出典: https://arxiv.org/abs/2606.01847
- **EdgeDAE: Acceleration of Diffusion Action Experts for Real-Time Physical AI with Tiny VLAs on Edge FPGA-GPU Systems** — arXiv:2610.00311 — 出典: https://arxiv.org/abs/2610.00311
- **CHASE-VLA: Post-Training Quantization Framework for Vision-Language-Action Models with Chunk-Aware Scale Estimation** — arXiv:2610.02666 — 出典: https://arxiv.org/abs/2610.02666
- **Online Evolution Strategy for Flow-Matching VLA Policies via Self-Supervised Trajectory Distribution Optimization** — arXiv:2609.38855 — 出典: https://arxiv.org/abs/2609.38855
- **Devol-ONE: One Autoregressive Mixture of Transformers to Unify Vision-Language-Action and Latent World Modeling** — arXiv:2609.32193 — 出典: https://arxiv.org/abs/2609.32193
- **ActionCache: Training-Free Acceleration for Vision-Language-Action Models with Action Caching and Refinement** — arXiv:2607.06370 — 出典: https://arxiv.org/abs/2607.06370
- **Deltoris: Enabling Real-time VLA Inference in Embodied AI via Bit-level Sparsity and Speculative Inference** — arXiv:2608.04428 — 出典: https://arxiv.org/abs/2608.04428
- **Do Not Cut When Uncertain: Rejectable and Calibrated Decision Heads for VLA Policies in Robotic Harvesting** — arXiv:2609.35039 — 出典: https://arxiv.org/abs/2609.35039
- **Hidden in Plain Sight: Diffusion-Based Unrestricted Robotic Attacks on Vision-Language-Action Models** — arXiv:2608.10393 — 出典: https://arxiv.org/abs/2608.10393
- **Perturbation-Based Epistemic Uncertainty for Failure Detection in Vision-Language-Action Models** — arXiv:2606.20754 — 出典: https://arxiv.org/abs/2606.20754
- **Q-VGM: Q-Guided Value-Gradient Matching for Offline-to-Online RL of Flow-Matching VLA Policies** — arXiv:2606.08015 — 出典: https://arxiv.org/abs/2606.08015
- **GeoAAC: Geometry-Based Adaptive Action Chunking from Denoising Trajectories in VLA Policies** — arXiv:2609.20776 — 出典: https://arxiv.org/abs/2609.20776

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 69（2025: 16, 2026: 42）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

エンボディメント横断の統一行動 API、生成方式の理論比較。

---

## VLM適応・基盤VLA・指示追従

**件数（主テーマ）**: 583

### 解いている問題

Web スケール VLM をロボット方策に適応させ、意味知識と制御性能の trade-off をどう管理するか。

### 主要な手法の対立軸

フル fine-tune vs 部分凍結・insulation / 単体 generalist vs soft prompt 条件付け / オープン vs 商用基盤。

### 代表論文（5〜15 本、一覧より）

- **OpenVLA: An Open-Source Vision-Language-Action Model** — arXiv:2406.09246 — 出典: https://arxiv.org/abs/2406.09246
- **GR00T N1: An Open Foundation Model for Generalist Humanoid Robots** — arXiv:2503.14734 — 出典: https://arxiv.org/abs/2503.14734
- **$π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization** — arXiv:2504.16054 — 出典: https://arxiv.org/abs/2504.16054
- **Knowledge Insulating Vision-Language-Action Models: Train Fast, Run Fast, Generalize Better** — arXiv:2505.23705 — 出典: https://arxiv.org/abs/2505.23705
- **X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model** — arXiv:2510.10274 — 出典: https://arxiv.org/abs/2510.10274
- **VLA-InfoEntropy: A Training-Free Vision-Attention Information Entropy Approach for Vision-Language-Action Models Inference Acceleration and Success** — arXiv:2604.05323 — 出典: https://arxiv.org/abs/2604.05323
- **From Traditional Automation to Embodied Wireless Intelligence: Vision-Language-Action Empowered Physics-Aware Communication Networks** — arXiv:2606.13458 — 出典: https://arxiv.org/abs/2606.13458
- **Mamba-based Selective State Space Modeling Improves the Accuracy-Complexity Tradeoff of SmolVLA Vision-Language-Action Experts** — arXiv:2608.21407 — 出典: https://arxiv.org/abs/2608.21407
- **Think Only When Needed: Prompt-Authority Control for Selective Slow-Path Intervention in Vision-Language-Action Manipulation** — arXiv:2608.23224 — 出典: https://arxiv.org/abs/2608.23224
- **BICPO-VLA: Behavior-Identified Continuation Preference Optimization for Smooth Asynchronous Vision-Language-Action Control** — arXiv:2608.13924 — 出典: https://arxiv.org/abs/2608.13924
- **Task-Specified Active Metrological Inspection with Measurement-Steered VLA Manipulation and Deterministic Evidence Gating** — arXiv:2609.14219 — 出典: https://arxiv.org/abs/2609.14219
- **Correcting WHERE, Preserving HOW: Compositional Generalization for Vision-Language-Action Models via Referential Guidance** — arXiv:2609.38616 — 出典: https://arxiv.org/abs/2609.38616
- **DSDyn-VLA: A Dual-Stream Dynamic Manipulation Framework with Motion Perception, Future Awareness, and Realtime Correction** — arXiv:2609.39198 — 出典: https://arxiv.org/abs/2609.39198
- **Look Before You Act: Bridging Active Perception and Vision-Language-Action Models via Observation-Aligned Data Adaptation** — arXiv:2610.23378 — 出典: https://arxiv.org/abs/2610.23378
- **AnchorRefine: Synergy-Manipulation Based on Trajectory Anchor and Residual Refinement for Vision-Language-Action Models** — arXiv:2604.17787 — 出典: https://arxiv.org/abs/2604.17787

### 2026 年の増減（一覧上の date 列ベース）

テーマ内件数: 全体 583（2025: 113, 2026: 377）。2026 年の推移: 増加が顕著（2026 エントリが一覧上で 2025 を大きく上回る）。※ date 列が 2026 の行は OpenReview 投稿 ID を含み、arXiv 未付番のものが多い。

### 未開拓に見える方向

適応時の表現劣化メカニズム、少数ショットでの安定適応。

---

## テーマ横断の所見（一覧のみに基づく）

- **投稿の集中**: 2026 年ラベルが 1320/1994 件と過半を占め、VLA が評価・安全・RL 後処理とセットで研究されている。
- **手法軸**: 「推論・デュアルシステム」「diffusion/flow と AR のハイブリッド」「RL fine-tuning」がタイトル・アブストで頻出。
- **ギャップ**: ベンチマーク／ロバストネス／データセット系が増えている一方、標準化された比較は一覧上では未確認（各論文が個別プロトコルを提案）。
