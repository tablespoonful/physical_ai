# 世界モデル論文のテーマ別整理

**調査基準日**: 2026-10-31  
**入力**: `C:\Users\table\AppData\Local\Temp\claude\C--Users-table-vla\96a5b191-79ac-4772-a63d-62f0b328cb07\scratchpad\pa\titles_worldmodel.tsv`（全 3100 件）  
**整理対象**: 2614 件（関連薄いものを除外: 486 件）  
**出典**: 本整理は上記 TSV のタイトル・要約先頭 300 字のみに基づく（Web 検索なし）。

**一覧ファイル**: `file:///C:/Users/table/AppData/Local/Temp/claude/C--Users-table-vla/96a5b191-79ac-4772-a63d-62f0b328cb07/scratchpad/pa/titles_worldmodel.tsv`

**論文メタデータの出典**: 各代表論文の ID・タイトル・年は同一 TSV 行。確認用 URL は arXiv ID から `https://arxiv.org/abs/<id>`、OpenReview ID から `https://openreview.net/forum?id=<id>` を機械生成（ページ内容は未検証）。

## 除外基準

1. **中核テーマ外**: タイトル/要約に世界モデル、World Foundation Model、Dreamer 系潜在モデル、JEPA、操作/運転向け interactive world model 等の中核語がない論文。
2. **応用のみの弱関連**: 「world model」を一度も触れず、一般 RL/LLM/分類のみの記述。
3. **テーマ未分類**: 中核語はあるが、下記いずれの分野キーワードにも該当しないもの（汎用バケットへ移す前に再判定）。

## テーマ一覧（件数）

- **自動運転・ドライビング世界モデル**: 238 件
- **ロボット操作・エンボディド操作の世界モデル**: 197 件
- **VLA・World-Action・方策統合**: 126 件
- **潜在ダイナミクス・MBRL (Dreamer 系)**: 305 件
- **動画拡散・生成型世界基盤 (WFM / Cosmos / Genie)**: 228 件
- **自己教師あり動画表現 (JEPA 等) と予測**: 91 件
- **触覚・マルチモーダル知覚世界モデル**: 13 件
- **3D・幾何一貫性・シーン理解**: 70 件
- **評価・ベンチマーク・シミュレーション用途**: 104 件
- **計画・想像ロールアウトと方策学習**: 215 件
- **動画・視覚未来予測（ドメイン非特化）**: 18 件
- **エンボディド AI・Physical AI（横断）**: 41 件
- **言語モデル・エージェント連携の世界モデル**: 16 件
- **連続制御・汎用 MBRL 世界モデル**: 30 件
- **離散・ゲーム・Atari 世界モデル**: 34 件
- **汎用・その他の世界モデル**: 888 件

## 自動運転・ドライビング世界モデル（238 件）

### 解いている問題
将来シーン・多エージェント相互作用を生成/予測し、E2E 計画・合成データ・評価に使う。

### 主要な手法の対立軸
動画拡散 vs 潜在 RL 世界モデル / 多視点一貫性 vs 単眼 / 幾何・軌道連携 vs 見た目生成中心

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.35044 | 2026 | DriveUniTok: A Unified Multimodal Tokenizer for Driving World-Action Models | [リンク](https://arxiv.org/abs/2610.35044) |
| 2610.34650 | 2026 | Dream to Assist: Intent-Conditioned World Models for Shared Vehicle Control | [リンク](https://arxiv.org/abs/2610.34650) |
| 2610.23886 | 2026 | EvoAD: Self-Evolving Autonomous Driving via Latent World-Model Guided Post-ho... | [リンク](https://arxiv.org/abs/2610.23886) |
| 2610.22450 | 2026 | DriveWorld3D Evidence Constrained 3D World Modeling and Generative Simulation... | [リンク](https://arxiv.org/abs/2610.22450) |
| 2610.20609 | 2026 | SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware ... | [リンク](https://arxiv.org/abs/2610.20609) |
| 2610.17688 | 2026 | OccWAM: Occupancy World-Action Models with Joint Scene-to-Ego Flow Matching | [リンク](https://arxiv.org/abs/2610.17688) |
| 2610.16139 | 2026 | Directional Pullback Regularization for Long-Horizon Rollout of Latent World ... | [リンク](https://arxiv.org/abs/2610.16139) |
| 2610.14871 | 2026 | MORE: Learning Motion-Oriented Registers for Driving World Models and Planning | [リンク](https://arxiv.org/abs/2610.14871) |
| 2610.11060 | 2026 | AffordDrive3D: Affordance-Aware World-Action Modeling with Spatial Understanding | [リンク](https://arxiv.org/abs/2610.11060) |
| 2610.09438 | 2026 | Controllable Crowd Generation through World-Model Planning | [リンク](https://arxiv.org/abs/2610.09438) |
| 2610.09335 | 2026 | SearchWorld: Spatial Value-Grounded Imagination for UAV Object Search via Wor... | [リンク](https://arxiv.org/abs/2610.09335) |
| 2610.07381 | 2026 | GeoWM: Efficient Direct World Modeling in Explicit Geometry | [リンク](https://arxiv.org/abs/2610.07381) |
| 2610.07031 | 2026 | Artemis: Geometry-Grounded Multi-Agent Driving World Models with Shared 3D St... | [リンク](https://arxiv.org/abs/2610.07031) |
| 2610.06250 | 2026 | Generative World Models Enable Predictive Control of Laser Melt Pool Dynamics | [リンク](https://arxiv.org/abs/2610.06250) |
| 2609.39245 | 2026 | ReWAM: Reciprocal World Action Models for Interactive Autonomous Driving | [リンク](https://arxiv.org/abs/2609.39245) |

### 2026 年の増減（TSV 内カウント）
2026年 123 件 / 2025年 68 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
安全保証付きロールアウト、規制対応の検証可能予測、長期ドリフト定量化（TSV 上は identity drift 言及はあるが体系的手法は少ない印象）。

## ロボット操作・エンボディド操作の世界モデル（197 件）

### 解いている問題
操作に伴う視覚（触覚含む）未来を予測し、方策学習・データ効率・Real2Sim を改善する。

### 主要な手法の対立軸
RGB-D vs RGB / アクション条件 vs 言語条件 / Real2Sim 転移 vs 純シミュレーション

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.40401 | 2026 | Continuous-Action World Models: Learning Cross-Embodiment Spatiotemporal Dyna... | [リンク](https://arxiv.org/abs/2610.40401) |
| 2610.39528 | 2026 | PRIME W0: Physical Priors from World Models for Embodied Manipulation | [リンク](https://arxiv.org/abs/2610.39528) |
| 2610.37091 | 2026 | GAWM: A Compact Latent World-Action Model for Multi-Task Robot Manipulation | [リンク](https://arxiv.org/abs/2610.37091) |
| 2610.36011 | 2026 | E0.5: From Reconstructive to Future-Predictive 3D Foundations for Robotic Wor... | [リンク](https://arxiv.org/abs/2610.36011) |
| 2610.34593 | 2026 | What Does World Modeling Actually Improve in Robot Action Learning? | [リンク](https://arxiv.org/abs/2610.34593) |
| 2610.33807 | 2026 | RoboWorM: Evaluating Movement Realism, Consistency and Acceleration Affects i... | [リンク](https://arxiv.org/abs/2610.33807) |
| 2610.31474 | 2026 | Skeleton-Grounded Latent Action Model for Robot World Models | [リンク](https://arxiv.org/abs/2610.31474) |
| 2610.30781 | 2026 | DeXplicit: Making Physical State Explicit in Dexterous Manipulation World Models | [リンク](https://arxiv.org/abs/2610.30781) |
| 2610.29246 | 2026 | DepState-JEPA: Learning Depth-Grounded State Representation for Visual Percep... | [リンク](https://arxiv.org/abs/2610.29246) |
| 2610.26855 | 2026 | Ropedia W0: Scaling Loco-Manipulation World Models across Embodiments with Hu... | [リンク](https://arxiv.org/abs/2610.26855) |
| 2610.25600 | 2026 | Vector-Quantized World Model: Latent Feedback Motion Planning for Robot Manip... | [リンク](https://arxiv.org/abs/2610.25600) |
| 2610.24285 | 2026 | ACTS: Learning Visuo-Tactile World Models from Human Physical Interaction | [リンク](https://arxiv.org/abs/2610.24285) |
| 2610.23156 | 2026 | ORD-WM: Learning Object-Centric Rigid Dynamics for 3D World Modeling in Robot... | [リンク](https://arxiv.org/abs/2610.23156) |
| 2610.22364 | 2026 | T2-z: Test-Time Optimization of Environment Latents for Robotic World Models | [リンク](https://arxiv.org/abs/2610.22364) |
| 2610.21686 | 2026 | MAIA: Anticipating Interaction Anomalies in Contact-Rich Manipulation via Mul... | [リンク](https://arxiv.org/abs/2610.21686) |

### 2026 年の増減（TSV 内カウント）
2026年 151 件 / 2025年 36 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
長期操作 horizon での触覚統合、汎用ハンドの力制御連携（要約ベース）。

## VLA・World-Action・方策統合（126 件）

### 解いている問題
VLA の推論と世界予測を単一または緊結アーキテクチャで統合する。

### 主要な手法の対立軸
統合 WAM vs 分離 VLA+WM / 幾何 grounded vs 2D 生成

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.38508 | 2026 | SaiVLA-JEPA: Evaluating Future Latent Prediction in JEPA-Conditioned VLA Control | [リンク](https://arxiv.org/abs/2610.38508) |
| 2610.30814 | 2026 | DRILL: Training World Models to Improve Policies, Not Predict Pixels | [リンク](https://arxiv.org/abs/2610.30814) |
| 2610.23334 | 2026 | LAW: Unifying Language, Action, and World Modeling for Agentic Physical Intel... | [リンク](https://arxiv.org/abs/2610.23334) |
| 2610.21985 | 2026 | VeriVLA: Adaptive Test-Time Verification for Flow-Based VLAs with Latent Worl... | [リンク](https://arxiv.org/abs/2610.21985) |
| 2610.19825 | 2026 | What Matters for World Modeling in Vision-Language-Action Models? | [リンク](https://arxiv.org/abs/2610.19825) |
| 2610.18774 | 2026 | GreenWAM: A World Foundation Model for Robotics | [リンク](https://arxiv.org/abs/2610.18774) |
| 2610.18697 | 2026 | UniW(A)M: A Unified Mixture-of-Experts Framework for World and World-Action M... | [リンク](https://arxiv.org/abs/2610.18697) |
| 2610.17922 | 2026 | WoVR+: World Model as Reliable Simulator for Versatile VLA Policy Optimizatio... | [リンク](https://arxiv.org/abs/2610.17922) |
| 2610.16641 | 2026 | What Limits Cross-Task Generalization in World Action Models? | [リンク](https://arxiv.org/abs/2610.16641) |
| 2610.16558 | 2026 | G$^2$WAM: World Action Models for Efficient and Geometry Grounded Image-Goal ... | [リンク](https://arxiv.org/abs/2610.16558) |
| 2610.15585 | 2026 | StreamingWAM: Streaming World Action Modeling via Chunk-Wise Staircase Flow M... | [リンク](https://arxiv.org/abs/2610.15585) |
| 2610.12818 | 2026 | LeWAM: End-to-End World and Action Modeling with JEPAs | [リンク](https://arxiv.org/abs/2610.12818) |
| 2610.12407 | 2026 | LeWAM: A JEPA World Action Model with Diffusion-Steering-Based MPC | [リンク](https://arxiv.org/abs/2610.12407) |
| 2610.12285 | 2026 | PLaW-VLA: Predictive Latent World Modeling for Vision-Language-Action Policies | [リンク](https://arxiv.org/abs/2610.12285) |
| 2610.12194 | 2026 | MiniWAM: Learning Compact Future Targets for Efficient World-Action Modeling | [リンク](https://arxiv.org/abs/2610.12194) |

### 2026 年の増減（TSV 内カウント）
2026年 114 件 / 2025年 11 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
統合モデルの失敗時におけるモジュール分離 fallback の標準化（TSV 要約ベース）。

## 潜在ダイナミクス・MBRL (Dreamer 系)（305 件）

### 解いている問題
連続制御で想像ロールアウトから方策を学び、サンプル効率と長期安定性を両立する。

### 主要な手法の対立軸
拡散潜在 vs RSSM / IMLE・多峰性 vs 単峰 / Koopman 等スペクトル制約 vs 純 NN

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.40637 | 2026 | world2vec: Mechanistic world models through latent dynamics learning | [リンク](https://arxiv.org/abs/2610.40637) |
| 2610.39576 | 2026 | Bayesian Offline Multi-Agent Reinforcement Learning with Latent World Models | [リンク](https://arxiv.org/abs/2610.39576) |
| 2610.39258 | 2026 | Agentic LinkDreamer: Adaptive Neuro-Fuzzy World-Model Decision Making for Int... | [リンク](https://arxiv.org/abs/2610.39258) |
| 2610.39100 | 2026 | Generating Critic-Guided Synthetic Experience in Latent World Models | [リンク](https://arxiv.org/abs/2610.39100) |
| 2610.37588 | 2026 | Understanding the limits of latent world models | [リンク](https://arxiv.org/abs/2610.37588) |
| 2610.35636 | 2026 | Adapt for Planning, Not just Prediction: Optimistic Test-Time World Model Ada... | [リンク](https://arxiv.org/abs/2610.35636) |
| 2610.31617 | 2026 | DiffDreamer: Coupling World Models with Differentiable Simulation for Agile Q... | [リンク](https://arxiv.org/abs/2610.31617) |
| 2610.31194 | 2026 | Inside-JEPA: From Prediction to Relational Grounding in Latent World Models | [リンク](https://arxiv.org/abs/2610.31194) |
| 2610.29382 | 2026 | RadioDreamer: A World Model for Radio Map Forecasting and Imagination-Based O... | [リンク](https://arxiv.org/abs/2610.29382) |
| 2610.28779 | 2026 | Second Thoughts: Exploring and Planning through Comparative Imagination in Wo... | [リンク](https://arxiv.org/abs/2610.28779) |
| 2610.28483 | 2026 | Exploring Temporal Context-Aware Physical Grounding in Latent World Models | [リンク](https://arxiv.org/abs/2610.28483) |
| 2610.28074 | 2026 | Slot-JEPA: Object-Structured Prediction Interfaces for Latent World Models | [リンク](https://arxiv.org/abs/2610.28074) |
| 2610.27890 | 2026 | EndoWorld-JEPA: Motion-Guided Global-Local Latent World Modeling for Endoscop... | [リンク](https://arxiv.org/abs/2610.27890) |
| 2610.27851 | 2026 | LaLa-World: Scaling Latent World Models with Natural Language Actions | [リンク](https://arxiv.org/abs/2610.27851) |
| 2610.25781 | 2026 | See the Future, Classify the Present: Stochastic Latent World Modeling for Hy... | [リンク](https://arxiv.org/abs/2610.25781) |

### 2026 年の増減（TSV 内カウント）
2026年 209 件 / 2025年 43 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
実機 humanoid/legged への大規模検証記述が TSV サンプルでは限定的。

## 動画拡散・生成型世界基盤 (WFM / Cosmos / Genie)（228 件）

### 解いている問題
Physical AI 向けに大規模動画基盤で世界をモデル化し、生成・計画・評価を統合する。

### 主要な手法の対立軸
統合 WAM vs 分離 policy+WM / NVIDIA Cosmos 系 vs 学術拡散 / 合成データ生成 vs 方策学習

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.40191 | 2026 | Video Generation Meets Agent Harness: Agentic Video Generation, Agentic World... | [リンク](https://arxiv.org/abs/2610.40191) |
| 2610.39232 | 2026 | Seeing and Imagining as One: Unified Video Generation and 4D Perception for E... | [リンク](https://arxiv.org/abs/2610.39232) |
| 2610.37257 | 2026 | GameVerse: A Minute-Scale Gameplay Dataset for Long-Horizon Interactive World... | [リンク](https://arxiv.org/abs/2610.37257) |
| 2610.35529 | 2026 | WorldPager: Zero-Stall Tiered Memory for Long-Horizon World Models on a Singl... | [リンク](https://arxiv.org/abs/2610.35529) |
| 2610.33894 | 2026 | WMEval: Evaluating Interactive World Models Grounded on Physical Simulations | [リンク](https://arxiv.org/abs/2610.33894) |
| 2610.33589 | 2026 | Mix Forcing: Causal Pre-Training via Mixture Attention for Interactive World ... | [リンク](https://arxiv.org/abs/2610.33589) |
| 2610.32381 | 2026 | UniWorld: A Unified World Model for Real-Time Visual World Simulation | [リンク](https://arxiv.org/abs/2610.32381) |
| 2610.30129 | 2026 | Rethinking Video Autoencoders for Interactive World Models | [リンク](https://arxiv.org/abs/2610.30129) |
| 2610.29061 | 2026 | OccJEPA: Occlusion as Masking for Amodal Video Segmentation | [リンク](https://arxiv.org/abs/2610.29061) |
| 2610.28631 | 2026 | AEON: Unifying Video and 3D World Models | [リンク](https://arxiv.org/abs/2610.28631) |
| 2610.27387 | 2026 | Training Controllable World Models via Action Influence Maximization | [リンク](https://arxiv.org/abs/2610.27387) |
| 2610.25959 | 2026 | EmbodiedWorld-200K: Toward Embodied World Agents via Embodied-Planning Datase... | [リンク](https://arxiv.org/abs/2610.25959) |
| 2610.23913 | 2026 | UMI-WM: Interactive World Modeling for Bimanual Manipulation from Wrist Cameras | [リンク](https://arxiv.org/abs/2610.23913) |
| 2610.22355 | 2026 | OmniVerifier-C1: Decomposed Graded Verifier for Rule-Governed Generative Worl... | [リンク](https://arxiv.org/abs/2610.22355) |
| 2610.22311 | 2026 | Velox: Spatial Memory Makes World Models Efficient | [リンク](https://arxiv.org/abs/2610.22311) |

### 2026 年の増減（TSV 内カウント）
2026年 166 件 / 2025年 46 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
リアルタイム閉ループ制御との定量トレードオフ記述がまだ散発的。

## 自己教師あり動画表現 (JEPA 等) と予測（91 件）

### 解いている問題
観察のみから物理理解と予測表現を学び、計画可能な表現へ接続する。

### 主要な手法の対立軸
密な予測 vs グローバル表現 / 少量相互作用データ vs 大規模動画 / planning への接続 vs 理解のみ

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.37963 | 2026 | Self-Supervised Latent Action-Conditioned World Modeling for Time Series | [リンク](https://arxiv.org/abs/2610.37963) |
| 2610.36662 | 2026 | SWIM: Learning What Matters from Behaviors for JEPA World Models | [リンク](https://arxiv.org/abs/2610.36662) |
| 2610.34033 | 2026 | Fovea-JEPA: Overcoming Geometric Blind Spots in V-JEPA for Camera Motion Reco... | [リンク](https://arxiv.org/abs/2610.34033) |
| 2610.30160 | 2026 | V-JEPA 2 Meets AQA: Phase-Based Scoring and Reference-Based Feedback for Moun... | [リンク](https://arxiv.org/abs/2610.30160) |
| 2610.27921 | 2026 | Quantum-JEPA: Quantum Born Priors for Latent-Action JEPA World Models | [リンク](https://arxiv.org/abs/2610.27921) |
| 2610.26780 | 2026 | V-JEPA Hand: Simple, Accurate and Fast 3D Hand and Camera Trajectory Recovery... | [リンク](https://arxiv.org/abs/2610.26780) |
| 2610.23982 | 2026 | Time-JEPA: Grounding Video World Models with Physical Time Series | [リンク](https://arxiv.org/abs/2610.23982) |
| 2610.23896 | 2026 | InJePA: Intention-First Latent Planning with Coupled JEPA World Models for Vi... | [リンク](https://arxiv.org/abs/2610.23896) |
| 2610.23127 | 2026 | BeJEPA: A Goal-Conditioned Humanoid Behavior World Model via Unsupervised RL | [リンク](https://arxiv.org/abs/2610.23127) |
| 2610.17584 | 2026 | RAN-JEPA: An Action-Conditioned World Model for Energy-efficient Mobile Netwo... | [リンク](https://arxiv.org/abs/2610.17584) |
| 2610.15429 | 2026 | World Modeling through Spectral Alignment | [リンク](https://arxiv.org/abs/2610.15429) |
| 2610.14324 | 2026 | EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference | [リンク](https://arxiv.org/abs/2610.14324) |
| 2610.13956 | 2026 | MDN-VJEPA: Multimodal Probabilistic Joint-Embedding World Models | [リンク](https://arxiv.org/abs/2610.13956) |
| 2610.13912 | 2026 | RSI-Anything: Unlocking Recursive Self-Improvement with World Models | [リンク](https://arxiv.org/abs/2610.13912) |
| 2610.07540 | 2026 | Preserving Unstable Modes Through Inverse Dynamics in JEPA World Models | [リンク](https://arxiv.org/abs/2610.07540) |

### 2026 年の増減（TSV 内カウント）
2026年 83 件 / 2025年 4 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
操作タスクでの密表現の必須性の比較研究（要約上は V-JEPA 系が増加）。

## 触覚・マルチモーダル知覚世界モデル（13 件）

### 解いている問題
接触時の視覚限界を触覚で補い、接触豊かな相互作用を予測する。

### 主要な手法の対立軸
視覚のみ vs 視触融合 / 接触物理 vs 見た目予測

### 代表論文（13 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.28613 | 2026 | Physical Canvas: A Vision Tactile World Model For Robot Policy Evaluation And... | [リンク](https://arxiv.org/abs/2610.28613) |
| 2609.38444 | 2026 | Audible World Models: Spatially Aware Sound Generation for 3D Worlds | [リンク](https://arxiv.org/abs/2609.38444) |
| 2609.34286 | 2026 | Dexterous Tactile World Model | [リンク](https://arxiv.org/abs/2609.34286) |
| 2609.27656 | 2026 | InternW0: A Foundational Physical World Model for Efficient Real-World Intera... | [リンク](https://arxiv.org/abs/2609.27656) |
| 2609.06837 | 2026 | BinauralVAE: Spatial Audio Reconstruction For World Models | [リンク](https://arxiv.org/abs/2609.06837) |
| 2608.23189 | 2026 | EchoWM: Open and Enterable Omnimodal World Models | [リンク](https://arxiv.org/abs/2608.23189) |
| 2608.21075 | 2026 | AudioWorldSim: Realistic Binaural Audio Datasets For World Models | [リンク](https://arxiv.org/abs/2608.21075) |
| 2608.05891 | 2026 | AppDeltaWorld: Transition-Grounded Delta Code World Model for Mobile GUI Agents | [リンク](https://arxiv.org/abs/2608.05891) |
| 2605.19950 | 2026 | AffectVerse: Emotional World Models for Multimodal Affective Computing | [リンク](https://arxiv.org/abs/2605.19950) |
| 2512.00883 | 2025 | Audio-Visual World Models: Learning Physically Grounded Multisensory Dynamics | [リンク](https://arxiv.org/abs/2512.00883) |
| 2511.01310 | 2025 | From Pixels to Cooperation Multi Agent Reinforcement Learning based on Multim... | [リンク](https://arxiv.org/abs/2511.01310) |
| 2509.21574 | 2025 | X-Streamer: Unified Human World Modeling with Audiovisual Interaction | [リンク](https://arxiv.org/abs/2509.21574) |
| 2304.11193 | 2023 | Multi-Modal World Model for Physical Robot Interactions: Simultaneous Visual ... | [リンク](https://arxiv.org/abs/2304.11193) |

### 2026 年の増減（TSV 内カウント）
2026年 9 件 / 2025年 3 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
件数自体が少なく、標準ベンチマーク化は未確認。

## 3D・幾何一貫性・シーン理解（70 件）

### 解いている問題
深度・新視点・操作を一貫した 3D/物理表現で統合する。

### 主要な手法の対立軸
明示 3D vs 暗黙 / NeRF・GS vs 動画基盤 / 操作と認識の統合

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.39721 | 2026 | WorldProbe: When Video World Models Fall Apart under Long-Horizon Spatial Exp... | [リンク](https://arxiv.org/abs/2610.39721) |
| 2610.38903 | 2026 | Structural-Test Geometry as an Inductive Bias for Partially Observable World ... | [リンク](https://arxiv.org/abs/2610.38903) |
| 2610.22343 | 2026 | GeoState: Learning View-Decoupled Geometry States for 3D World Modeling | [リンク](https://arxiv.org/abs/2610.22343) |
| 2610.20625 | 2026 | Decoupling Appearance and Geometry in Diffusion World Models | [リンク](https://arxiv.org/abs/2610.20625) |
| 2610.19201 | 2026 | Into the LidarVerse: A Real-Time Unified LiDAR World Model Across Tasks and S... | [リンク](https://arxiv.org/abs/2610.19201) |
| 2610.18570 | 2026 | Order-Consistent Latent Geometry for Reliable Short-Horizon Planning in World... | [リンク](https://arxiv.org/abs/2610.18570) |
| 2610.15166 | 2026 | ExeWorldBench: Benchmarking Code-Based Executable 3D World Modeling | [リンク](https://arxiv.org/abs/2610.15166) |
| 2610.13706 | 2026 | GLIMPSE: Global-Local Indexing with Multi-Precision Spectral Encoding for Exp... | [リンク](https://arxiv.org/abs/2610.13706) |
| 2610.02860 | 2026 | Counterfactual Action Evaluation, Observation Bottlenecks, and Representation... | [リンク](https://arxiv.org/abs/2610.02860) |
| 2610.02160 | 2026 | 4Director: Controlling Video World Models with Rigid 3D Geometry | [リンク](https://arxiv.org/abs/2610.02160) |
| 2609.40003 | 2026 | DashVMC: Real-Time Discrete World Model Control in Geometry Dash | [リンク](https://arxiv.org/abs/2609.40003) |
| 2609.35311 | 2026 | RoGSW4RLD: Feed-Forward 4D Gaussian Lifting for Robot World Model Rollouts | [リンク](https://arxiv.org/abs/2609.35311) |
| 2609.32657 | 2026 | World Models with Predictable Long-Horizon Marginals | [リンク](https://arxiv.org/abs/2609.32657) |
| 2609.29092 | 2026 | DAWN: Noise-Robust Quadruped Parkour via Depth-Denoising World Models | [リンク](https://arxiv.org/abs/2609.29092) |
| 2609.21787 | 2026 | Compact but Moving: Intervention-Relevant Geometry in Recurrent World Models | [リンク](https://arxiv.org/abs/2609.21787) |

### 2026 年の増減（TSV 内カウント）
2026年 53 件 / 2025年 12 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
生成 WM と 3D 再構成の統一評価指標。

## 評価・ベンチマーク・シミュレーション用途（104 件）

### 解いている問題
WM ロールアウトの品質測定と、方策評価用の代替環境を提供する。

### 主要な手法の対立軸
学習済み WM を環境化 (WorldGym) vs 人手シミュ / VLM 自動評価 vs 人手

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.33565 | 2026 | WorldFailBench: Do World Models Understand Policy Failures? | [リンク](https://arxiv.org/abs/2610.33565) |
| 2610.33014 | 2026 | The Social World Model Evaluation Gap | [リンク](https://arxiv.org/abs/2610.33014) |
| 2610.31066 | 2026 | Dual Exam: Controlled Evaluation of Multimodal Agents and World Models | [リンク](https://arxiv.org/abs/2610.31066) |
| 2610.26903 | 2026 | Beckmann World Models: Direct Terminal-Map Learning for One-Step Action-Condi... | [リンク](https://arxiv.org/abs/2610.26903) |
| 2610.24519 | 2026 | Axiomatic World Modeling for Physics Reasoning | [リンク](https://arxiv.org/abs/2610.24519) |
| 2610.22708 | 2026 | GlobeBench: Evaluating Text-Based World Model Capabilities for Scalable Envir... | [リンク](https://arxiv.org/abs/2610.22708) |
| 2610.19063 | 2026 | WorldMemBench: A Comprehensive Benchmark for Memory of Video World Models | [リンク](https://arxiv.org/abs/2610.19063) |
| 2610.18826 | 2026 | WorldOracle: Benchmarking Action-Conditioned World Models against Real-World ... | [リンク](https://arxiv.org/abs/2610.18826) |
| 2610.16450 | 2026 | CivWorldBench: Evaluating Language World Models in Structured Multi-Agent San... | [リンク](https://arxiv.org/abs/2610.16450) |
| 2610.13372 | 2026 | Towards Safe World Models: Risks, Defenses, and Evaluation | [リンク](https://arxiv.org/abs/2610.13372) |
| 2610.09134 | 2026 | World Models Dream of Success: Diagnosing and Repairing Failure Insensitivity... | [リンク](https://arxiv.org/abs/2610.09134) |
| 2610.08791 | 2026 | World Models' Last Exam in Physics | [リンク](https://arxiv.org/abs/2610.08791) |
| 2610.03356 | 2026 | ReFract: Benchmarking Perspective Awareness in Language Model Agents with Tex... | [リンク](https://arxiv.org/abs/2610.03356) |
| 2610.02957 | 2026 | Understanding Trajectory Heterogeneity in Federated World Model Learning | [リンク](https://arxiv.org/abs/2610.02957) |
| 2610.02660 | 2026 | SpectralCache: Accelerating Diffusion-Based World Models via Spectral Feature... | [リンク](https://arxiv.org/abs/2610.02660) |

### 2026 年の増減（TSV 内カウント）
2026年 83 件 / 2025年 15 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
人手評価との相関の長期追跡。

## 計画・想像ロールアウトと方策学習（215 件）

### 解いている問題
想像軌道から方策を学び・計画し、モデル誤差の蓄積を抑える。

### 主要な手法の対立軸
長期 rollout vs 短 horizon / policy-aware 特徴選択 vs 全画素予測

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.37891 | 2026 | When More Planning Hurts: Learned Planners for World Models | [リンク](https://arxiv.org/abs/2610.37891) |
| 2610.34663 | 2026 | Video World Models Need Predictable Latents | [リンク](https://arxiv.org/abs/2610.34663) |
| 2610.29435 | 2026 | Events, Not Pixels: Where World Models Get the Return Wrong | [リンク](https://arxiv.org/abs/2610.29435) |
| 2610.28011 | 2026 | Knowing When to Stop Thinking: A Dissection of Expected Free Energy as a Test... | [リンク](https://arxiv.org/abs/2610.28011) |
| 2610.27914 | 2026 | World Models with Configurable Perception | [リンク](https://arxiv.org/abs/2610.27914) |
| 2610.27280 | 2026 | VPFlow: Value-Predictive Planning with Imperfect World Models for Offline Goa... | [リンク](https://arxiv.org/abs/2610.27280) |
| 2610.26923 | 2026 | CaMeWM: A Causal Medical World Model for Generative Tumor Evolution and Treat... | [リンク](https://arxiv.org/abs/2610.26923) |
| 2610.26844 | 2026 | AnyGoal: On World Model Generalization Beyond Expert Rollouts | [リンク](https://arxiv.org/abs/2610.26844) |
| 2610.25666 | 2026 | Frechet Forcing: Training Long-Horizon Streaming World Models from Short Clips | [リンク](https://arxiv.org/abs/2610.25666) |
| 2610.22041 | 2026 | Plans Are Not Executions: Adapting Frozen World-Model Planners to Controller-... | [リンク](https://arxiv.org/abs/2610.22041) |
| 2610.18135 | 2026 | SkipWorld: Latent Skip Planning with Distilled World Models for Efficient Vis... | [リンク](https://arxiv.org/abs/2610.18135) |
| 2610.17510 | 2026 | Rethinking World Models for Biosignals | [リンク](https://arxiv.org/abs/2610.17510) |
| 2610.12910 | 2026 | Sampling-based Kinodynamic Planning with World Models | [リンク](https://arxiv.org/abs/2610.12910) |
| 2610.10274 | 2026 | Sparse Planning in Visual World Models via Cost Gradients | [リンク](https://arxiv.org/abs/2610.10274) |
| 2610.09048 | 2026 | Towards Financial World Modeling | [リンク](https://arxiv.org/abs/2610.09048) |

### 2026 年の増減（TSV 内カウント）
2026年 151 件 / 2025年 41 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
未確認

## 動画・視覚未来予測（ドメイン非特化）（18 件）

### 解いている問題
ドメイン特化前段階として、フレーム列の物理 plausible な未来を予測する。

### 主要な手法の対立軸
ピクセル予測 vs 潜在予測 / 単ステップ vs 長系列

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.30724 | 2026 | Learning from Next-Frame Prediction: Towards Unified and Scalable Visual Worl... | [リンク](https://arxiv.org/abs/2610.30724) |
| 2610.19212 | 2026 | Decoupled Drift-Diffusion World Models for Consistent Future Frame Prediction | [リンク](https://arxiv.org/abs/2610.19212) |
| 2610.12468 | 2026 | DreamTrue: Action-Faithful Robot World Model with Counterfactual Post-Training | [リンク](https://arxiv.org/abs/2610.12468) |
| 2610.12417 | 2026 | WOVEN: Weaving Visual World Modeling into Multimodal LLMs | [リンク](https://arxiv.org/abs/2610.12417) |
| 2610.01215 | 2026 | AutoGUIWorld: Image Generators as Visual World Models for GUI Agent | [リンク](https://arxiv.org/abs/2610.01215) |
| 2609.04911 | 2026 | TourPhysics: Bringing Physics to World Models for Exploration and Manipulatio... | [リンク](https://arxiv.org/abs/2609.04911) |
| 2608.28491 | 2026 | AcrossVAM1.0: Particle World Modeling for Text-Assisted Robot Video Prediction | [リンク](https://arxiv.org/abs/2608.28491) |
| 2608.04653 | 2026 | Overcoming Statistical Bias in Action-Controllable World Models | [リンク](https://arxiv.org/abs/2608.04653) |
| 2608.03211 | 2026 | CrossScope: A Role-Asymmetric World Model for Joint Dual-Scope Surgical Video... | [リンク](https://arxiv.org/abs/2608.03211) |
| 2606.29059 | 2026 | Flow Matching in Feature Space for Stochastic World Modeling | [リンク](https://arxiv.org/abs/2606.29059) |
| 2606.08775 | 2026 | Unifying Object-Centric World Models and Diffusion Policy: A Hierarchical Fra... | [リンク](https://arxiv.org/abs/2606.08775) |
| 2605.07079 | 2026 | Learning Visual Feature-Based World Models via Residual Latent Action | [リンク](https://arxiv.org/abs/2605.07079) |
| 2602.03747 | 2026 | LIVE: Long-horizon Interactive Video World Modeling | [リンク](https://arxiv.org/abs/2602.03747) |
| 2511.03077 | 2025 | WorldPlanner: Monte Carlo Tree Search and MPC with Action-Conditioned Visual ... | [リンク](https://arxiv.org/abs/2511.03077) |
| 2508.06096 | 2025 | Bounding Distributional Shifts in World Modeling through Novelty Detection | [リンク](https://arxiv.org/abs/2508.06096) |

### 2026 年の増減（TSV 内カウント）
2026年 13 件 / 2025年 3 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
未確認

## エンボディド AI・Physical AI（横断）（41 件）

### 解いている問題
Physical AI 全般の世界モデル化・デジタルツイン。

### 主要な手法の対立軸
プラットフォーム (Cosmos 等) vs 単一論文手法

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.18447 | 2026 | Thinker-WM: A Unified World Model with Shared Multimodal Representations for ... | [リンク](https://arxiv.org/abs/2610.18447) |
| 2610.09285 | 2026 | LeCuration: A Tiny World Model as a Data Curation Multi-Tool | [リンク](https://arxiv.org/abs/2610.09285) |
| 2610.06349 | 2026 | KineWorld: Action-Induced Transport Fields for Embodied World Modeling | [リンク](https://arxiv.org/abs/2610.06349) |
| 2610.03374 | 2026 | EVEWorld: Physical Evolution Supervision for Embodied World Models | [リンク](https://arxiv.org/abs/2610.03374) |
| 2609.24313 | 2026 | NeuIDO: Neural Intrinsic Dynamics Operator for Physics-Informed 4D World Models | [リンク](https://arxiv.org/abs/2609.24313) |
| 2609.23184 | 2026 | CausalWM: Causal Chain-of-Thought Reasoning for Embodied World Model | [リンク](https://arxiv.org/abs/2609.23184) |
| 2609.16697 | 2026 | World Models for Embodied Intelligence: From Plausible to Controllable to Act... | [リンク](https://arxiv.org/abs/2609.16697) |
| 2609.05834 | 2026 | Learning Counterfactual World Models for Embodied Reasoning under Partial Obs... | [リンク](https://arxiv.org/abs/2609.05834) |
| 2608.13901 | 2026 | Ontology-Grounded World Models for Failure Diagnosis and Closed-Loop Repair i... | [リンク](https://arxiv.org/abs/2608.13901) |
| 2608.10618 | 2026 | Toward the Cognitive--Physical Limits of Embodied Intelligence through a Worl... | [リンク](https://arxiv.org/abs/2608.10618) |
| 2608.07809 | 2026 | CausalNav: Reliability-Certified Causal World Models for Control under Physic... | [リンク](https://arxiv.org/abs/2608.07809) |
| 2607.28251 | 2026 | Policy-Level Recursive Self-Improvement for Embodied AI with a Criticality Wo... | [リンク](https://arxiv.org/abs/2607.28251) |
| 2607.13560 | 2026 | Grounded world models in biological organisms and future embodied AI | [リンク](https://arxiv.org/abs/2607.13560) |
| 2607.02634 | 2026 | Metasurface embodied intelligence through electromagnetic world model | [リンク](https://arxiv.org/abs/2607.02634) |
| 2606.22449 | 2026 | Self-Evolving Cognitive Framework via Causal World Modeling for Embodied Scie... | [リンク](https://arxiv.org/abs/2606.22449) |

### 2026 年の増減（TSV 内カウント）
2026年 23 件 / 2025年 16 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
未確認

## 言語モデル・エージェント連携の世界モデル（16 件）

### 解いている問題
動的環境で LM エージェントが使う予測・推論用世界表現を構築する。

### 主要な手法の対立軸
LM 推論用 WM vs 物理予測 / test-time 混合 vs 単一 WM

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.19642 | 2026 | Model What Matters: Decision-Guided Selective World Modeling for Language Agents | [リンク](https://arxiv.org/abs/2610.19642) |
| 2609.31874 | 2026 | COUNTERMEM: World-Model Verified Counter-Factual Memory for Language Agents | [リンク](https://arxiv.org/abs/2609.31874) |
| 2607.08894 | 2026 | GATS: Graph-Augmented Tree Search with Layered World Models for Efficient Age... | [リンク](https://arxiv.org/abs/2607.08894) |
| 2606.31422 | 2026 | Ask the World Before Acting: Environment Probing for Calibrating Agent World ... | [リンク](https://arxiv.org/abs/2606.31422) |
| 2606.31399 | 2026 | World-Model Collapse as a Phase Transition | [リンク](https://arxiv.org/abs/2606.31399) |
| 2606.27806 | 2026 | Agentic vs. Parametric World Models: Hybrid Planning for Reliable Language Ag... | [リンク](https://arxiv.org/abs/2606.27806) |
| 2606.02388 | 2026 | Policy and World Modeling Co-Training for Language Agents | [リンク](https://arxiv.org/abs/2606.02388) |
| 2606.02372 | 2026 | CoMAP: Co-Evolving World Models and Agent Policies for LLM Agents | [リンク](https://arxiv.org/abs/2606.02372) |
| 2601.22647 | 2026 | Test-Time Mixture of World Models for Embodied Agents in Dynamic Environments | [リンク](https://arxiv.org/abs/2601.22647) |
| 2601.07964 | 2026 | Executable Ontologies in Game Development: From Algorithmic Control to Semant... | [リンク](https://arxiv.org/abs/2601.07964) |
| 2601.00755 | 2026 | A formal theory on problem space as a semantic world model in systems enginee... | [リンク](https://arxiv.org/abs/2601.00755) |
| hFiNgXOT8p | 2026 | Real-Time Text-Conditioned World Models for Interactive Prototyping | [リンク](https://openreview.net/forum?id=hFiNgXOT8p) |
| 2512.14014 | 2025 | MobileWorldBench: Towards Semantic World Modeling For Mobile Agents | [リンク](https://arxiv.org/abs/2512.14014) |
| 2512.07195 | 2025 | Multilingual Agent-Based World Modeling for Social Science | [リンク](https://arxiv.org/abs/2512.07195) |
| 2411.06559 | 2024 | Is Your LLM Secretly a World Model of the Internet? Model-Based Planning for ... | [リンク](https://arxiv.org/abs/2411.06559) |

### 2026 年の増減（TSV 内カウント）
2026年 12 件 / 2025年 2 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
物理 grounded と言語推論の失敗モード分類。

## 連続制御・汎用 MBRL 世界モデル（30 件）

### 解いている問題
操作・運転以外の連続制御やマルチタスクで想像学習を効率化する。

### 主要な手法の対立軸
多峰 IMLE vs 単峰 / latent action vs 低次元 / マルチタスク vs 単タスク

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.36791 | 2026 | RynnWorld-Latent: A Cross-Embodiment World Model Conditioned on Universal Lat... | [リンク](https://arxiv.org/abs/2610.36791) |
| 2610.10846 | 2026 | Cross-Embodiment Robot Foundation World Models with Latent Actions | [リンク](https://arxiv.org/abs/2610.10846) |
| 2609.31893 | 2026 | CyberWorld: World Models for Sample-Efficient Autonomous Cyber Defense | [リンク](https://arxiv.org/abs/2609.31893) |
| 2608.20936 | 2026 | Graph-Operator World Models for Morphology-Parameter Generalization in Contin... | [リンク](https://arxiv.org/abs/2608.20936) |
| 2608.17956 | 2026 | An Omitted Mode Is a Rare Rule: The Sampling-Verification Danger Law in Conti... | [リンク](https://arxiv.org/abs/2608.17956) |
| 2607.09185 | 2026 | Causally Debiased Latent Action Model for Embodied Action-Conditioned World M... | [リンク](https://arxiv.org/abs/2607.09185) |
| 2606.05015 | 2026 | Generalization of World Models under Environmental Variability for Vision-bas... | [リンク](https://arxiv.org/abs/2606.05015) |
| 2605.15725 | 2026 | DiLA: Disentangled Latent Action World Models | [リンク](https://arxiv.org/abs/2605.15725) |
| 2604.19734 | 2026 | UniT: Toward a Unified Physical Language for Human-to-Humanoid Policy Learnin... | [リンク](https://arxiv.org/abs/2604.19734) |
| 2604.08958 | 2026 | WOMBET: World Model-Based Experience Transfer for Robust and Sample-efficient... | [リンク](https://arxiv.org/abs/2604.08958) |
| 2603.21546 | 2026 | What Do World Models Learn in RL? Probing Latent Representations in Learned E... | [リンク](https://arxiv.org/abs/2603.21546) |
| 2603.11110 | 2026 | ResWM: Residual-Action World Model for Visual RL | [リンク](https://arxiv.org/abs/2603.11110) |
| 2602.16229 | 2026 | Factored Latent Action World Models | [リンク](https://arxiv.org/abs/2602.16229) |
| 2602.10104 | 2026 | Olaf-World: Orienting Latent Actions for Video World Modeling | [リンク](https://arxiv.org/abs/2602.10104) |
| ovaI8QU0gS | 2026 | FLAM: Scaling Latent Action World Models with Factorization | [リンク](https://openreview.net/forum?id=ovaI8QU0gS) |

### 2026 年の増減（TSV 内カウント）
2026年 17 件 / 2025年 8 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
実ロボット連続制御での不確実性校正の共通ベンチ。

## 離散・ゲーム・Atari 世界モデル（34 件）

### 解いている問題
離散状態空間での計画・サンプル効率を世界モデルで改善する。

### 主要な手法の対立軸
離散 latent vs 連続 / 古典 Atari vs 3D ゲーム

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.40607 | 2026 | Fight World Model: Customizable Combat through Visual Interaction Proxies | [リンク](https://arxiv.org/abs/2610.40607) |
| 2610.25861 | 2026 | ActionRoPE: Action as Coordinates for Spatially Consistent Control in Planar-... | [リンク](https://arxiv.org/abs/2610.25861) |
| 2609.25652 | 2026 | GameDirector: Decoupling Gameplay Logic from Rendering for Player-Configurabl... | [リンク](https://arxiv.org/abs/2609.25652) |
| 2608.30692 | 2026 | Can Video World Models Track Unobserved World States? | [リンク](https://arxiv.org/abs/2608.30692) |
| 2608.25518 | 2026 | Agentic Game Development as a Verifiable Trajectory Data Engine for Scaling W... | [リンク](https://arxiv.org/abs/2608.25518) |
| 2608.24680 | 2026 | Game2World Engine: Unlocking In-the-Wild Gameplay Videos for World Model Trai... | [リンク](https://arxiv.org/abs/2608.24680) |
| 2607.28287 | 2026 | Tycho: Active Abstraction with Programmatic World Models for ARC-AGI-3 | [リンク](https://arxiv.org/abs/2607.28287) |
| 2607.26754 | 2026 | StatePlay: State-Aware Game World Models for Mechanics-Consistent Generation | [リンク](https://arxiv.org/abs/2607.26754) |
| 2607.18367 | 2026 | AlayaWorld: Interactive Long-Horizon World Modeling -- Full Technical Report | [リンク](https://arxiv.org/abs/2607.18367) |
| 2607.14169 | 2026 | When a Verified World Model Still Loses: Play-Adequacy vs Prediction-Accuracy... | [リンク](https://arxiv.org/abs/2607.14169) |
| 2606.30292 | 2026 | DreamForge-World 0.1 Preview: A Low-Compute Real-Time Controllable World Model | [リンク](https://arxiv.org/abs/2606.30292) |
| 2605.24375 | 2026 | Distilling Game Code World Model Generation into Lightweight Large Language M... | [リンク](https://arxiv.org/abs/2605.24375) |
| 2605.15256 | 2026 | ReactiveGWM: Flexible Control and NPC Reactivity in Game World Models | [リンク](https://arxiv.org/abs/2605.15256) |
| 2605.13740 | 2026 | Learning POMDP World Models from Observations with Language-Model Priors | [リンク](https://arxiv.org/abs/2605.13740) |
| 2605.08578 | 2026 | Probing the Impact of Scale on Data-Efficient, Generalist Transformer World M... | [リンク](https://arxiv.org/abs/2605.08578) |

### 2026 年の増減（TSV 内カウント）
2026年 19 件 / 2025年 6 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
Physical AI への転移可能性の定量比較は TSV 上ほぼ未確認。

## 汎用・その他の世界モデル（888 件）

### 解いている問題
上記にまたがる一般的世界予測・モデル化。

### 主要な手法の対立軸
分野横断 vs 単一ドメイン

### 代表論文（15 本、ID 付き）

| ID | 年 | タイトル | 確認用 URL |
| --- | --- | --- | --- |
| 2610.40503 | 2026 | Algebraic World Model: From Exploration to Proofs | [リンク](https://arxiv.org/abs/2610.40503) |
| 2610.39812 | 2026 | GROME: GROunding Factorized MEmory into Video World Models | [リンク](https://arxiv.org/abs/2610.39812) |
| 2610.38980 | 2026 | Context Compaction for World Models | [リンク](https://arxiv.org/abs/2610.38980) |
| 2610.38289 | 2026 | PulmoWorld: An Asynchronous Multimodal Medical World Model for Longitudinal P... | [リンク](https://arxiv.org/abs/2610.38289) |
| 2610.37175 | 2026 | MLE-World: Predicting Machine Learning Experiment Outcomes with a Learned Wor... | [リンク](https://arxiv.org/abs/2610.37175) |
| 2610.36068 | 2026 | Rollback: Experience Backtracking in World Models for Policy Improvement | [リンク](https://arxiv.org/abs/2610.36068) |
| 2610.35877 | 2026 | Calibrated for Which Policy? Conformal Uncertainty for Fixed World Models Und... | [リンク](https://arxiv.org/abs/2610.35877) |
| 2610.35813 | 2026 | World Model for Energy Efficiency Maximization in Dynamic Metasurface Antennas | [リンク](https://arxiv.org/abs/2610.35813) |
| 2610.34797 | 2026 | TimeWorld: Towards Action-Conditioned Multimodal World Models for Time Series... | [リンク](https://arxiv.org/abs/2610.34797) |
| 2610.34564 | 2026 | FlockWorld: Toward Population-Scale Multi-Agent Video World Models through Ar... | [リンク](https://arxiv.org/abs/2610.34564) |
| 2610.33566 | 2026 | Distilling Dense Trajectory Teachers For Large-Motion Video World Models | [リンク](https://arxiv.org/abs/2610.33566) |
| 2610.33169 | 2026 | World-in-Context: Interactive Video World Modeling with In-Context Conditioning | [リンク](https://arxiv.org/abs/2610.33169) |
| 2610.33054 | 2026 | Saga: an in silico ontology for a multimodal patient world model | [リンク](https://arxiv.org/abs/2610.33054) |
| 2610.33033 | 2026 | Duration-Aware World Models for Sleep Staging with Dwell-Time Constraints | [リンク](https://arxiv.org/abs/2610.33033) |
| 2610.32977 | 2026 | UniAction: Unified Action Conditioning for World Models | [リンク](https://arxiv.org/abs/2610.32977) |

### 2026 年の増減（TSV 内カウント）
2026年 484 件 / 2025年 167 件（TSV 内）。2026 は年初 arXiv 月日表記が多い。

### 未開拓に見える方向
ドメイン横断転移の失敗境界。

## 除外サンプル（理由付き、最大 10 件）

- `IljH2Bt6jO` Training a Vision-Language Model for Diverse Exploration in … — タイトル/要約に世界モデル・WFM・Dreamer/JEPA/操作応用の中核語がない
- `hcuEdq6eKD` GDPval: Evaluating AI Model Performance on Real-World Econom… — タイトル/要約に世界モデル・WFM・Dreamer/JEPA/操作応用の中核語がない
- `Kk9t5empEf` Unified Surgical World Model for Structured Understanding, L… — Physical AI 中心の調査から外れる応用ドメイン（供給網・外科等）
- `NuGAhTDYTd` Scalable In-Context Q-Learning… — タイトル/要約に世界モデル・WFM・Dreamer/JEPA/操作応用の中核語がない
- `rbNOhbdQ0v` Making Offline Model-Based Reinforcement Learning Work on Re… — タイトル/要約に世界モデル・WFM・Dreamer/JEPA/操作応用の中核語がない
- `BjJ8yNgEMZ` GoalZero: Model-based Hierarchical Self-Play for Sequential … — タイトル/要約に世界モデル・WFM・Dreamer/JEPA/操作応用の中核語がない
- `UgFmrYcLOt` TOUCAN: Synthesizing 1.5M Tool-Agentic Data from Real-World … — タイトル/要約に世界モデル・WFM・Dreamer/JEPA/操作応用の中核語がない
- `OQRs4JYvuv` Accelerating Model-Based Reinforcement Learning Using Equiva… — タイトル/要約に世界モデル・WFM・Dreamer/JEPA/操作応用の中核語がない
- `sjxhk2vuo9` Long-Horizon Model-Based Offline Reinforcement Learning With… — タイトル/要約に世界モデル・WFM・Dreamer/JEPA/操作応用の中核語がない
- `TntCH2maP7` Model-Based Reinforcement Learning under Random Observation … — タイトル/要約に世界モデル・WFM・Dreamer/JEPA/操作応用の中核語がない