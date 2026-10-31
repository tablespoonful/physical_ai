# 世界モデル (World Model) 資料集

調査日: 2026-10-31。環境の変化を予測するモデルの論文を、ロボット、自動運転、Physical AI を中心にまとめたフォルダです。GUI エージェントなど実世界と関係の薄い応用は、PDF の取得対象から外しています (`_catalog.csv` には残っています)。

## 手法の分類

Chef Robotics の [サーベイ記事](https://chefrobotics.ai/post/world-models-and-world-action-models-an-accessible-and-comprehensive-survey) は、次の 6 つに分類しています。

1. 潜在再帰状態空間モデル (Dreamer 系)
2. 価値等価プランニングモデル (MuZero、TD-MPC 系)
3. 自己回帰トークン Transformer
4. 拡散、生成フレームモデル
5. Joint-Embedding Predictive Architecture (JEPA 系)
6. 動画生成の基盤モデル (Cosmos 系)

## 主要論文

| 年月 | 論文 | arXiv |
|---|---|---|
| 2018-03 | World Models | 1803.10122 |
| 2022-06 | DayDreamer | 2206.14176 |
| 2023-01 | DreamerV3 | 2301.04104 |
| 2025-01 | Cosmos World Foundation Model Platform | 2501.03575 |
| 2025-04 | Unified World Models | 2504.02792 |
| 2025-06 | V-JEPA 2 | 2506.09985 |
| 2026-01 | Cosmos Policy | 2601.16163 |
| 2026-03 | V-JEPA 2.1 | 2603.14482 |
| 2026-06 | Cosmos 3 | 2606.02800 |

## 2026 年の動き

- **World Action Model (WAM)** が新しい区分として定着しつつあります。予測と行動生成を一つのモデルに統合する考え方で、サーベイが複数出ています ([Awesome-WAM](https://github.com/OpenMOSS/Awesome-WAM))。
- [NVIDIA Cosmos](https://github.com/nvidia/cosmos) の現行版は Cosmos 3 です。README は「見る、推論する、シミュレーションする、行動する」を一つのモデルファミリーで担うと説明しています。技術レポートは `docs/Cosmos 3 Technical Report.pdf` に保存しました。
- 世界モデルを方策の学習や評価に使う研究が VLA 側でも増えています。`../VLA/` の WMPO、VLA-RFT、Gemini Robotics の Veo シミュレータでの評価 (arXiv 2512.10675) が関連します。

## 関連リソース

- [Awesome-World-Models (leofan90)](https://github.com/leofan90/Awesome-World-Models)
- [Awesome-World-Models (knightnemo)](https://github.com/knightnemo/Awesome-World-Models)
- [AwesomeWorldModels (Li-Zn-H)](https://github.com/Li-Zn-H/AwesomeWorldModels)
- [Awesome-WAM (OpenMOSS)](https://github.com/OpenMOSS/Awesome-WAM)

## 詳細ノート

Sonnet、Codex、Cursor に分担して作成しました。出典と「未確認」の区別はノート内に記載しています。

- `notes/practical_addendum.md`: 学習設備、実機評価、重みとライセンス、2026 年の学会論文の追補
- `notes/practical.md`: 公開実装と重み、ライセンス、必要 GPU、評価指標、企業動向、日本語資料
- `notes/venues.md`: 主要学会の論文と受賞
- `notes/themes.md`: 論文のテーマ別整理 (キーワード分類)

## 収集状況

- 候補論文: 3681 本 (`_catalog.csv`)
- 論文の本文 (.md): 276 本
- 手元に残した論文 PDF: 2 本
- フォルダ全体: 0.08 GB

## サーベイ、総説、チュートリアル

- 2026-09 [World-Action Models for Robot Learning and Control: A Survey](https://arxiv.org/abs/2609.16074) (本文あり)
- 2026-08 [Do World Models Make Better Robots? A Survey of Evaluation Benchmarks for Predictive Embodied Intelligence](https://arxiv.org/abs/2609.29669) (本文あり)
- 2026-08 [Surgical Video Generation From Diffusion to World Models: A Survey](https://arxiv.org/abs/2608.26214) (本文あり)
- 2026-07 [A Review Of Robotic World Models For Dynamic Environments Based On Factor And Scene Graphs](https://arxiv.org/abs/2610.08800) (本文あり)
- 2026-07 [From World Action Models to Embodied Brains: A Roadmap for Open-World Physical Intelligence](https://arxiv.org/abs/2607.11689) (本文あり)
- 2026-07 [A Definition and Roadmap for World Models](https://arxiv.org/abs/2607.06401) (本文あり)
- 2026-07 [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) (本文あり)
- 2026-07 [From World Models to World Action Models: A Concise Tutorial for Robotics](https://arxiv.org/abs/2607.00836) (本文あり)
- 2026-06 [World Action Models: A Survey](https://arxiv.org/abs/2606.20781) (本文あり)
- 2026-06 [A Tutorial on World Models and Physical AI](https://arxiv.org/abs/2606.12783) (本文あり)
- 2026-05 [World Models: A Comprehensive Survey of Architectures, Methodologies, Reasoning Paradigms, and Applications](https://arxiv.org/abs/2606.00133) (本文あり)
- 2026-05 [World Models for Robotic Manipulation: A Survey](https://arxiv.org/abs/2606.00113) (本文あり)
- 2026-05 [GE-Sim 2.0: A Roadmap Towards Comprehensive Closed-loop Video World Simulators for Robotic Manipulation](https://arxiv.org/abs/2605.27491) (本文あり)
- 2026-04 [World Model for Robot Learning: A Comprehensive Survey](https://arxiv.org/abs/2605.00080) (本文あり)
- 2026-04 [Beyond the Autoregressive Horizon: A Comprehensive Survey of Diffusion Models, World Modelling, and State Space Models for Code](https://arxiv.org/abs/2606.23690)
- 2026-03 [Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses](https://arxiv.org/abs/2605.02900) (本文あり)
- 2026-01 [Robotic Video World Models: A Survey of Applications, Research Challenges, Future Directions](https://arxiv.org/abs/2601.07823) (本文あり)
- 2025-12 [Modeling the Mental World for Embodied AI: A Comprehensive Review](https://arxiv.org/abs/2601.02378) (本文あり)
- 2025-11 [Simulating the Visual World with Artificial Intelligence: A Roadmap](https://arxiv.org/abs/2511.08585) (本文あり)
- 2025-10 [A Step Toward World Models: A Survey on Robotic Manipulation](https://arxiv.org/abs/2511.02097) (本文あり)
- 2025-10 [A Comprehensive Survey on World Models for Embodied AI](https://arxiv.org/abs/2510.16732) (本文あり)
- 2025-10 [The Safety Challenge of World Models for Embodied AI Agents: A Review](https://arxiv.org/abs/2510.05865) (本文あり)
- 2025-09 [3D and 4D World Modeling: A Survey](https://arxiv.org/abs/2509.07996)
- 2025-07 [A Survey: Learning Embodied Intelligence from Physical Simulators and World Models](https://arxiv.org/abs/2507.00917) (本文あり)
- 2025-06 [From 2D to 3D Cognition: A Brief Survey of General World Models](https://arxiv.org/abs/2506.20134) (本文あり)
- 2025-06 [A Survey on World Models Grounded in Acoustic Physical Information](https://arxiv.org/abs/2506.13833) (本文あり)
- 2025-03 [Exploring the Evolution of Physics Cognition in Video Generation: A Survey](https://arxiv.org/abs/2503.21765)
- 2025-03 [Simulating the Real World: A Unified Survey of Multimodal Generative Models](https://arxiv.org/abs/2503.04641)
- 2025-02 [The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey](https://arxiv.org/abs/2502.10498) (本文あり)
- 2025-01 [A Survey of World Models for Autonomous Driving](https://arxiv.org/abs/2501.11260) (本文あり)
