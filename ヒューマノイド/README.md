# ヒューマノイド資料集

調査日: 2026-10-31。ヒューマノイドの全身制御、歩行、操作、遠隔操作、言語指示による制御などの論文をまとめたフォルダです。

## 研究テーマの全体像

[awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) は、次のように分類しています。

- 歩行と操作の統合、全身制御
- 操作
- 遠隔操作
- 歩行
- ナビゲーション
- 状態推定
- Sim-to-Real
- ハードウェア設計
- シミュレーションベンチマーク
- 物理ベースのキャラクターアニメーション
- 人間動作の解析と生成

## 主要論文

| 年月 | 論文 | arXiv |
|---|---|---|
| 2024-03 | HumanoidBench | 2403.10506 |
| 2025-01 | Humanoid Locomotion and Manipulation (総説、IEEE/ASME T-Mech 2026) | 2501.02116 |
| 2025-06 | A Survey of Behavior Foundation Model | 2506.20487 |
| 2025-06 | LeVERB (言語指示の全身制御) | 2506.13751 |
| 2025-08 | BeyondMimic | 2508.08241 |
| 2025-11 | TWIST2 | 2511.02832 |
| 2025-11 | SONIC | 2511.07820 |

## 学習環境

- [Isaac Lab](https://docs.nvidia.com/isaaclab/3.0/isaac-lab): Isaac Sim と併用でき、Newton 物理バックエンドで単独でも動きます。
- [mjlab](https://arxiv.org/abs/2601.22074): Isaac Lab のマネージャ型 API を採用した、MuJoCo ベースの軽量な GPU シミュレーション環境です。
- [WBC-AGILE](https://github.com/nvidia-isaac/WBC-AGILE): Isaac Lab ベースの全身制御学習フレームワークで、Booster T1 と Unitree G1 での Sim-to-Real が報告されています。

## 産業動向

出典は報道と各社の発表です。独立した検証ではなく、数字の定義も各社で異なります。低品質なまとめサイトに、互いに矛盾する数字が多かったので、確認できたものだけを載せます。

- **Unitree**: 報道によると、目論見書では 2025 年のヒューマノイド出荷が 5,500 台超、売上は約 17 億元です。2026-08-19 に上海 STAR 市場へ上場しました (688836、調達額は約 61 億元)。出典は [SSE 掲載の China Daily](https://english.sse.com.cn/news/newsrelease/voice/c/c_20260811_10828578.shtml) などで、目論見書の原本は確認していません。2025 年の売上は、報道により 16.99 億元と 17.08 億元の 2 種類があり、原文を確認できていないのでどちらが正しいかは未確定です (`notes/hardware_industry_addendum.md`)。
- **Agility Robotics**: GXO と複数年契約を結び、[両社の発表](https://investors.gxo.com/news-releases/news-release-details/gxo-signs-industry-first-multi-year-agreement-agility-robotics) では業界初の商用展開としています。[DC Velocity](https://www.dcvelocity.com/material-handling/robotics/gxo-to-expand-use-of-humanoid-robots-from-agility) などが展開拡大を報じています。
- **その他**: [Interesting Engineering の Reality Check](https://interestingengineering.com/research/the-humanoid-robot-reality-check) (2026 年 7 月) は、発表と実稼働の差を検証した記事です。出荷予測などの数字は、記事ごとの幅が大きいので、計画に使う場合は一次資料で確認してください。

## 関連リソース

- [awesome-humanoid-learning](https://github.com/jonyzhang2023/awesome-humanoid-learning)
- [awesome-humanoid-manipulation](https://github.com/tsunami-kun/awesome-humanoid-manipulation)

## 詳細ノート

Sonnet、Codex、Cursor に分担して作成しました。出典と「未確認」の区別はノート内に記載しています。

- `notes/hardware_industry.md`: 主要機体の仕様比較表、オープンハードウェア、各社の実績、日本の動向
- `notes/hardware_industry_addendum.md`: 機体仕様の追補、Unitree の数字の検討、RSS 2025 と Humanoids 2025 の受賞
- `notes/venues.md`: 主要学会の論文と受賞
- `notes/themes.md`: 論文のテーマ別整理 (キーワード分類)

## 収集状況

- 候補論文: 1962 本 (`_catalog.csv`)
- 論文の本文 (.md): 247 本
- 手元に残した論文 PDF: 0 本
- フォルダ全体: 0.02 GB

## サーベイ、総説、チュートリアル

- 2025-06 [A Survey of Behavior Foundation Model: Next-Generation Whole-Body Control System of Humanoid Robots](https://arxiv.org/abs/2506.20487) (本文あり)
- 2025-04 [Dexterous Manipulation through Imitation Learning: A Survey](https://arxiv.org/abs/2504.03515) (本文あり)
- 2024-04 [Deep Reinforcement Learning for Bipedal Locomotion: A Brief Survey](https://arxiv.org/abs/2404.17070) (本文あり)
- 2024-03 [Humanoid Robots and Humanoid AI: Review, Perspectives and Directions](https://arxiv.org/abs/2405.15775) (本文あり)
- 2023-01 [Teleoperation of Humanoid Robots: A Survey](https://arxiv.org/abs/2301.04317) (本文あり)
- 2022-07 [Robot's Gendering Trouble: A Scoping Review of Gendering Humanoid Robots and its Effects on HRI](https://arxiv.org/abs/2207.01130) (本文あり)
