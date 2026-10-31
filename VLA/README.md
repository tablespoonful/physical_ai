# VLA (Vision-Language-Action) 資料集

調査日: 2026-10-31。画像と言語指示からロボットの行動を出力するモデルの論文をまとめたフォルダです。元の 35 本 (ICLR 2026 投稿) に、基礎論文、後続の ICLR 2026 投稿、2026 年の arXiv 論文を加えました。

## ICLR 2026 の状況

OpenReview の ICLR 2026 投稿を、タイトルまたは概要に VLA を含むもので絞ると 166 本でした。[Moritz Reuss 氏のブログ](https://mbreuss.github.io/blog_post_iclr_26_vla.html) の「164 本」とほぼ一致します。

| OpenReview の表示 | 本数 |
|---|---|
| ICLR 2026 Poster | 58 |
| Submitted to ICLR 2026 | 59 |
| Withdrawn | 44 |
| Desk Rejected | 5 |

「Submitted to ICLR 2026」は採択表示が付いていないものです。OpenReview の表示だけで判定しているため、公式の採択リストとの照合はしていません。元の 35 本の表示は `_catalog.csv` の `venue` 列にあります。取り下げや Desk Reject の論文は、新規には取得していません。

## 系譜の主要論文

いずれも arXiv の日付です。

| 年月 | 論文 | arXiv |
|---|---|---|
| 2022-12 | RT-1 | 2212.06817 |
| 2023-03 | Diffusion Policy | 2303.04137 |
| 2023-03 | PaLM-E | 2303.03378 |
| 2023-04 | ACT / ALOHA | 2304.13705 |
| 2023-07 | RT-2 | 2307.15818 |
| 2024-05 | Octo | 2405.12213 |
| 2024-06 | OpenVLA | 2406.09246 |
| 2024-10 | π0 | 2410.24164 |
| 2025-01 | FAST | 2501.09747 |
| 2025-03 | GR00T N1 | 2503.14734 |
| 2025-03 | Gemini Robotics | 2503.20020 |
| 2025-04 | π0.5 | 2504.16054 |
| 2025-06 | SmolVLA | 2506.01844 |
| 2025-10 | Gemini Robotics 1.5 | 2510.03342 |
| 2025-11 | π*0.6 | 2511.14759 |
| 2026-04 | π0.7 | 2604.15483 |

## 実装を始めるときの情報

- [openpi](https://github.com/Physical-Intelligence/openpi): 公開されているのは π0、π0-FAST、π0.5 です。README の必要 GPU メモリは、推論 8 GB 超、LoRA ファインチューニング 22.5 GB 超、全体のファインチューニング 70 GB 超です。π0.6 と π0.7 はこの一覧にありません。
- [Isaac GR00T](https://github.com/NVIDIA/Isaac-GR00T): README の現行版は GR00T N1.7 で、LeRobot との連携手順があります。
- FR3 で使う場合、openpi の README は DROID データセットでの学習手順を案内しています。ただし DROID の標準構成は Panda です (`notes/ecosystem.md`)。
- LIBERO は成功率 99% 超で飽和しており、LIBERO-Plus や LIBERO-PRO では大きく低下します。性能比較には実機評価の併用が必要です (`notes/ecosystem.md`)。

## 2026 年の動き

- π0.7 は、言語指示に加えて、タスクの達成度メタデータやサブゴール画像でも方策を操縦する設計を提案しています。失敗を含むデータや、ロボット以外のデータも学習に使えるとしています (概要より)。
- Google DeepMind は 2026-07-30 に Gemini Robotics 2 を発表しました。モデルカードで確認できたのは ER 2 と On-Device 2 で、VLA 本体はパートナー限定、重みは非公開です。技術レポートは未確認です (`notes/ecosystem.md`)。
- サーベイの対象が、データとベンチマーク、人間動画からの学習、産業利用の準備度、ドローンなどへ広がっています。下の一覧を参照してください。

## 詳細ノート

Sonnet、Codex、Cursor に分担して作成しました。出典と「未確認」の区別はノート内に記載しています。

- `notes/ecosystem_addendum.md`: ライセンス、リーダーボード、Gemini Robotics 2、重みの公開状況の追補
- `notes/ecosystem.md`: 公開モデル、ツール、データセット、ベンチマーク、批判的検討、日本の動向
- `notes/venues_2026_fall.md`: CoRL 2026 の採択論文 (VLA、ヒューマノイド、世界モデル) と NeurIPS 2026 の確認状況
- `notes/venues.md`: CoRL、RSS、CVPR、ICML などの学会別論文と受賞、ワークショップ
- `notes/venues_candidates.tsv`: 学会別の論文候補
- `notes/themes.md`: 論文のテーマ別整理 (キーワード分類)

## 収集状況

- 候補論文: 3360 本 (`_catalog.csv`)
- 論文の本文 (.md): 574 本
- 手元に残した論文 PDF: 15 本
- フォルダ全体: 0.14 GB

## サーベイ、総説、チュートリアル

- 2026-10 [From Sliding Windows to Self-evolving Lifelong Memory: A Dual-perspective Survey of Memory Paradigms for Long-Horizon Robotics VLA Models](https://arxiv.org/abs/2610.23319) (本文あり)
- 2026-07 [Vision Language Action (VLA) Models for Unmanned Aerial Robotics and Bimanual Manipulation: A Review](https://arxiv.org/abs/2607.06706) (本文あり)
- 2026-05 [From Human Videos to Robot Manipulation: A Survey on Scalable Vision-Language-Action Learning with Human-Centric Data](https://arxiv.org/abs/2606.00054) (本文あり)
- 2026-04 [Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines](https://arxiv.org/abs/2604.23001) (本文あり)
- 2026-03 [Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses](https://arxiv.org/abs/2605.02900) (本文あり)
- 2026-03 [Robotic Foundation Models for Industrial Control: A Comprehensive Survey and Readiness Assessment Framework](https://arxiv.org/abs/2603.06749) (本文あり)
- 2025-10 [A Survey on Efficient Vision-Language-Action Models](https://arxiv.org/abs/2510.24795) (本文あり)
- 2025-10 [Efficient Vision-Language-Action Models for Embodied Manipulation: A Systematic Survey](https://arxiv.org/abs/2510.17111) (本文あり)
- 2025-10 [Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications](https://arxiv.org/abs/2510.07077) (本文あり)
- 2025-09 [Pure Vision Language Action (VLA) Models: A Comprehensive Survey](https://arxiv.org/abs/2509.19012) (本文あり)
- 2025-08 [Survey of Vision-Language-Action Models for Embodied Manipulation](https://arxiv.org/abs/2508.15201) (本文あり)
- 2025-08 [Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey](https://arxiv.org/abs/2508.13073) (本文あり)
- 2025-08 [A tutorial note on collecting simulated data for vision-language-action models](https://arxiv.org/abs/2508.06547) (本文あり)
- 2025-07 [Vision Language Action Models in Robotic Manipulation: A Systematic Review](https://arxiv.org/abs/2507.10672) (本文あり)
- 2025-07 [A Survey on Vision-Language-Action Models: An Action Tokenization Perspective](https://arxiv.org/abs/2507.01925) (本文あり)
- 2025-06 [A Survey on Vision-Language-Action Models for Autonomous Driving](https://arxiv.org/abs/2506.24044) (本文あり)
- 2025-05 [OpenHelix: A Short Survey, Empirical Analysis, and Open-Source Dual-System VLA Model for Robotic Manipulation](https://arxiv.org/abs/2505.03912) (本文あり)
- 2025-04 [Towards Forceful Robotic Foundation Models: a Literature Survey](https://arxiv.org/abs/2504.11827) (本文あり)
- 2025-03 [Generative Artificial Intelligence in Robotic Manipulation: A Survey](https://arxiv.org/abs/2503.03464) (本文あり)
- 2025-02 [Survey on Vision-Language-Action Models](https://arxiv.org/abs/2502.06851)
- 2024-10 [Neural Fields in Robotics: A Survey](https://arxiv.org/abs/2410.20220) (本文あり)
- 2024-07 [Aligning Cyber Space with Physical World: A Comprehensive Survey on Embodied AI](https://arxiv.org/abs/2407.06886) (本文あり)
- 2024-05 [A Survey on Vision-Language-Action Models for Embodied AI](https://arxiv.org/abs/2405.14093) (本文あり)
- 2024-05 [Is Sora a World Simulator? A Comprehensive Survey on General World Models and Beyond](https://arxiv.org/abs/2405.03520) (本文あり)
- 2024-04 [What Foundation Models can Bring for Robot Learning in Manipulation : A Survey](https://arxiv.org/abs/2404.18201) (本文あり)
- 2024-04 [A Survey on Integration of Large Language Models with Intelligent Robots](https://arxiv.org/abs/2404.09228) (本文あり)
- 2024-02 [Real-World Robot Applications of Foundation Models: A Review](https://arxiv.org/abs/2402.05741) (本文あり)
- 2024-02 [Understanding the planning of LLM agents: A survey](https://arxiv.org/abs/2402.02716) (本文あり)
- 2024-02 [A Survey on Robotics with Foundation Models: toward Embodied AI](https://arxiv.org/abs/2402.02385) (本文あり)
- 2023-12 [Toward General-Purpose Robots via Foundation Models: A Survey and Meta-Analysis](https://arxiv.org/abs/2312.08782) (本文あり)
