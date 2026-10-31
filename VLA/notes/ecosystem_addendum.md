# VLA エコシステム追補：未確認事項の追加調査

調査基準日：2026-10-31。対象は既存 `ecosystem.md` で未確認だった事項。既存資料を修正せず、本ファイルだけを新規作成した。PDF の本文取得・ダウンロード、arXiv API、OpenAlex API は使用していない。PDF URL は公式 HTML のリンクから記録し、一部は HEAD リクエストで応答だけを確認した。

## 1. Open X-Embodiment と DROID の公式ライセンス

| 対象 | 今回確認できた内容 | 一次出典 |
|---|---|---|
| Open X-Embodiment | 公式リポジトリの「License and Disclaimer」は、ソフトウェアを Apache-2.0、それ以外の資料を CC BY 4.0 International と明記している。 | [公式 README](https://github.com/google-deepmind/open_x_embodiment#license-and-disclaimer) |
| Open X-Embodiment の構成データ | 公式 README は、収録データのメタデータと個別引用を別の一覧に委ねている。今回取得した一覧ではライセンス列を確認できなかった。上記のリポジトリの声明を、元の全データセットの個別条件を精査済みという意味には使わない。個別データの条件との照合は未確認。 | [公式 README](https://github.com/google-deepmind/open_x_embodiment)、[公式収録一覧](https://docs.google.com/spreadsheets/d/1rPBD77tk60AEIGZrGSODwyyzs5FgCU9Uz3h-3_t2A9g/edit) |
| DROID データ本体 | 著者の論文本文の Introduction と III「DROID Data Collection Setup」に、データ全体を **CC BY 4.0** で公開すると明記されている。論文ページ上部の論文自身のライセンス表示だけから判断したものではない。 | [著者論文 HTML・v2](https://arxiv.org/html/2403.12945v2) |

DROID の既存メモにある再配布版の Apache-2.0 表示を、データ本体の公式条件として採用する必要はなくなった。データ本体の確認根拠は上記の著者声明である。コードと学習済み重みの条件は、この声明だけでは確定しない。[出典：DROID 論文](https://arxiv.org/html/2403.12945v2)

## 2. リーダーボードの現在値

### RoboArena：公式表示のフィルタまで確認

公式サイトが読み込む JavaScript から公開 API を特定し、JSON を取得した。以下は API の `last_updated = 2026-10-31T04:19:46.259378Z` 時点の値で、JST では同日 13:19:46。`score`、`std`、`num_evals` をそのまま記録している。[公開 API](https://roboarena-api-domain-name.online/api/leaderboard)、[配信 JavaScript](https://robo-arena.github.io/assets/index-FWyWX4NQ.js)

公式画面の初期表示「Official」は **100 件以上の A/B 評価**があるポリシーに限定する。`dreaming_zebra` は画面上で `DreamZero` に置換される。画面はスコアを Elo、誤差を標準偏差として表示するため、以下の `std` を成功率や 95% 信頼区間として読まない。[公式画面ソース](https://github.com/robo-arena/robo-arena.github.io/blob/main/src/pages/Leaderboard.jsx)、[表示名変換](https://github.com/robo-arena/robo-arena.github.io/blob/main/src/api.js)

以下は Official 条件に合致する全行を API 順に掲載したもの。**出典は表全体について [公式公開 API](https://roboarena-api-domain-name.online/api/leaderboard)**。

| 順位 | 表示名／API 名 | score | std | A/B 評価件数 |
|---|---|---:|---:|---:|
| 1 | DreamZero / `dreaming_zebra` | 1735 | 42.6 | 190 |
| 2 | `pi05_droid` | 1608 | 30.7 | 745 |
| 3 | `pi0_fast_droid` | 1582 | 29.6 | 941 |
| 4 | `paligemma_vq_droid` | 1546 | 29.9 | 952 |
| 5 | `paligemma_diffusion_droid` | 1533 | 29.7 | 949 |
| 6 | `paligemma_fast_specialist_droid` | 1531 | 29.8 | 1057 |
| 7 | `paligemma_fast_droid` | 1516 | 29.9 | 1062 |
| 8 | `pi0_droid` | 1461 | 29.8 | 1120 |
| 9 | `paligemma_binning_droid` | 786 | 50.0 | 629 |

全ポリシー表示では `j2-vla`（画面名 Spirit v1.6）が score 1788、std 106.0、25 件で最上位だが、Official 条件を満たさない。Apricot も score 1661、std 61.0、63 件で Official 対象外。「現在の首位」を記す際は対象フィルタを併記する必要がある。[API](https://roboarena-api-domain-name.online/api/leaderboard)、[閾値と画面名の実装](https://robo-arena.github.io/assets/index-FWyWX4NQ.js)

### Meta-World、ManiSkill、Isaac Lab-Arena

| 対象 | 今回の確認結果 | 現在値の扱い・出典 |
|---|---|---|
| Meta-World | 公式プロジェクトと Farama 文書を確認したが、更新日時を伴う公式のモデル横断順位表は特定できなかった。 | **未確認**。論文比較表や第三者サイトの SOTA 表を「現在の公式順位」として代用しない。[公式プロジェクト](https://meta-world.github.io/)、[公式文書](https://metaworld.farama.org/) |
| ManiSkill2 継続チャレンジ | SAPIEN の公式案内は、CVPR 2023 の大会終了後も継続リーダーボードを維持すると説明し、`ms2-ongoing` に案内する。しかし、リンク先の現在表は取得タイムアウトで読めなかった。 | **現在値は未確認**。リーダーボードが存在しないとは結論しない。[公式案内](https://sapien.ucsd.edu/challenges/maniskill/2022/)、[継続チャレンジ](https://sapien.ucsd.edu/challenges/maniskill/challenges/ms2-ongoing) |
| ManiSkill-ViTac 2026 | 別の実機・言語指示・双腕視触覚チャレンジについては、主催者の最終表を確認できた。下表に掲載。 | ManiSkill3 の汎用 VLA 順位表との同一視はしない。[主催者ページ](https://callmeray.github.io/Mani_ViTac_Challenge_2026_page/) |
| Isaac Lab-Arena | 公式製品ページと文書は、ベンチマークの作成・実行・分析を支える共通基盤として説明する。今回、モデル名・評価条件・更新日時を揃えた公開順位表を特定できなかった。 | **現在値は未確認**。公式説明図の「GR00T 51%」「π0 50%」を実測リーダーボード値として転載しない。これらは固定タスク評価の問題を説明する文脈の図である。[公式製品ページ](https://developer.nvidia.com/isaac/lab-arena)、[公式説明文書](https://isaac-sim.github.io/IsaacLab-Arena/main/pages/motivation/motivation.html) |

ManiSkill-ViTac 2026 の掲載表は以下のとおり。主催者ページは最終順位の公表日を 2026-06-01 と記載する。数値は成功率ではなく、同ページの Task 1 / Task 2 / Total の**スコア表記をそのまま転記**したもの。得点式の詳細は未確認。[表・日程の一次出典](https://callmeray.github.io/Mani_ViTac_Challenge_2026_page/#leaderboard)

| 順位 | チーム | Task 1 | Task 2 | Total |
|---|---|---:|---:|---:|
| 1 | BIT IN²Bot | 420 | 280 | 700 |
| 2 | Baymax | 200 | 40 | 240 |
| 3 | NPU-EAI | 140 | 60 | 200 |
| 4 | ZTE&BUPT | 0 | 180 | 180 |
| 5 | ResTac | 160 | 0 | 160 |
| 6 | RoboReach | 0 | 60 | 60 |
| 比較用 | Official Baseline | 200 | 140 | 340 |

## 3. Gemini Robotics 2：公式ブログとレポートの所在

公式ブログ **“Gemini Robotics 2 brings whole body intelligence to robots”** を確認した。ページの公表日は **2026-07-30**、著者は Carolina Parada。VLA 本体の公式製品ページも存在し、early access の待機リストへ案内している。[DeepMind 公式ブログ](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)、[VLA 公式ページ](https://deepmind.google/models/gemini-robotics/vla/)

既存メモで報道由来だった Apollo 2 の全身制御、SharpaWave の 22 自由度の手は、この公式ブログ本文にも記載されている。ただし、いずれも **DeepMind 自己申告**であり、本調査による外部再現結果ではない。[公式ブログ](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)

同ブログの多指操作の図には、電球の取り付け 36%、取り外し 92%、ごみ袋の結束 44%、ちりとり 32%、Ziplock 40% と記載される。これにより既存メモの一部の二次情報数値を一次情報に置き換えられる。これらは Apollo / Sharpa の**個別タスク結果**で、VLA 全体の総合成功率ではない。試行数と誤差算出法の詳細は今回未確認。[公式ブログの “Multi-finger dexterity” 図](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)

レポートは、公式ブログから **“Gemini Robotics 2: Safety Technical Report”** としてリンクされている次の URL を確認した。

- [公式の安全性技術レポート PDF URL](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-2-Safety.pdf)。HEAD 応答は HTTP 200 / `application/pdf`。本文はダウンロードせず未読。
- 公式ブログはこのレポートを、安全なツール呼び出し、人への介入要求、人の接近時の停止などの評価を補足する資料として案内する。**モデル全体の学習手順・データ・性能を網羅する別の技術レポートや arXiv ID は未確認**。[リンク元と説明](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)

利用形態については、公式ブログが VLA 本体と On-Device を early-access partners 向けと明記する。一般配布される重みの URL は今回確認できなかった。「一般向け公開重みは未確認」と「パートナー提供がある」を併記する方が正確である。[公式ブログ](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)

## 4. openpi の最新タグと π*0.6 / π0.7 の重み

| 項目 | 追加確認の結論 | 一次出典 |
|---|---|---|
| openpi 最新タグ | GitHub REST API の tags 一覧が HTTP 200、空配列 `[]`。**確認時点でタグなし。したがって最新タグ名はない**。`main` をリリースタグと呼ばない。 | [公式 GitHub tags API](https://api.github.com/repos/Physical-Intelligence/openpi/tags?per_page=100) |
| openpi 最新 Release | releases API も HTTP 200、`[]`。GitHub の画面も “There aren’t any releases here” と表示する。タグと Release を別々に確認した。 | [releases API](https://api.github.com/repos/Physical-Intelligence/openpi/releases?per_page=100)、[公式 Releases 画面](https://github.com/Physical-Intelligence/openpi/releases) |
| π*0.6 | 公式ブログには論文と π0.6 のモデルカードへのリンクがある。一方、公式 openpi の現行 README のチェックポイント一覧には該当する重み配布先がない。**公式の公開重み・配布ライセンスは未確認**。「openpi で公開済み」という二次情報は採用しない。 | [公式発表](https://www.pi.website/blog/pistar06)、[現行 README 原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md) |
| π0.7 | 公式発表に論文へのリンクはあるが、現行 openpi のチェックポイント一覧では重み配布先を確認できない。**公式の公開重み・配布ライセンスは未確認**。公開されていないという絶対的な断定にも広げない。 | [公式発表](https://www.pi.website/blog/pi07)、[現行 README 原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md) |

上記は README の年表だけでなく、確認時点の raw 本文にある配布一覧との照合結果である。論文の公表、モデルの発表、実行可能な重みの一般公開を別の状態として扱う。[公式 openpi](https://github.com/Physical-Intelligence/openpi)

## 5. 日本：PFN、東大、産総研

### Preferred Networks（PFN）

PFN と Preferred Robotics は **2026-09-09**、屋内移動ロボット向け **PLaMo-SemGround** の共同開発開始を発表した。自然言語・RGB 画像・深度から走行可能／禁止領域や作業条件を理解する、2B パラメータ級以下のモデルを計画し、GENIAC のロボット基盤モデル研究開発に採択されたと説明する。これは**企業自身の開発計画の発表**である。[PFN 公式発表](https://www.preferred.jp/ja/news/1731)

同発表は PFR 製品への 2028 年度中の先行実装と、モデルライセンス・SDK 等の段階的な商用販売を計画する。完成済みのオープン VLA として数えない。行動出力を含む VLA の公開重み・技術論文・現時点の実測成績は、この発表では未確認。[PFN 公式発表](https://www.preferred.jp/ja/news/1731)

関連する公開モデルとして、PFN は **2026-04-03** に PLaMo-VL を発表している。ただし公式分類は視覚言語モデル（VLM）であり、VLA の公開実績に読み替えない。[PFN の PLaMo-VL 発表](https://www.preferred.jp/ja/news/pr20260403)

### 東京大学

松尾・岩澤研究室と AIRoA は **Physical AI Robot Challenge 2026（PARC2026）** を実施し、VLA の汎化能力向上を目的としている。公式ページは、同一タスク・同一ドメイン、同一タスク・未知ドメイン、既知スキルの新規組合せ・未知ドメインの評価 Track を示し、成功率以外になめらかさ、実行時間、安全性も評価対象とする。[研究室公式ページ](https://weblab.t.u-tokyo.ac.jp/physical-ai-competition/)

研究論文の具体例は **VLATest**。著者欄で Yuheng Huang と Lei Ma の東京大学所属を確認でき、ManiSkill2 上で視覚条件や指示等を変えるテスト場面を生成して VLA の頑健性を調べる共同研究である。新規汎用 VLA の重み公開とは別種の、**評価・品質保証の取り組み**として整理できる。[著者所属・手法の一次情報](https://arxiv.org/html/2409.12894v2)、[著者リポジトリ](https://github.com/ma-labo/VLATest)

### 産業技術総合研究所（産総研）

産総研の **2026-05-13** の公式記事は、実体知能研究チームの取り組みとして、複数の身体感覚を統合し、既存 VLA の「身体性」を補うロボット基盤モデルの開発を説明する。また双腕ロボットデータセットの無償公開、学習フレームワークの提供、AIRoA への参画も記載する。研究方針・活動の一次確認ができた段階であり、具体的な新 VLA モデル名や公開重みの確認とは区別する。[産総研公式記事](https://www.aist.go.jp/aist_j/magazine/20260513.html)

さらに **2026-01-14** の公式調達公告は、「自律移動ロボットためのVLA基盤モデルの技術調査およびスクリプト試作」を対象とし、オープンソース／API 利用可能な VLA の調査と、自律移動ロボットへのカスタマイズの試作を明記している。公告は研究需要の根拠にはなるが、納品完了・成果公開・性能達成の根拠にはしない。それらは未確認。[産総研公式調達公告](https://www.aist.go.jp/aist_j/procure/supplyinfo/pub/detail/WM50AL29)

## 6. 論文候補：転記用 TSV

TSV の出力先パスが指定されておらず、書込み許可は本 Markdown のみのため、別ファイルを作らず以下にタブ区切りで収録した。既存メモで実在確認済みの論文は再列挙していない。year は出版年とし、VLATest の初回 arXiv 投稿年は 2024、改訂は 2025 と区別する。出版先と DOI は論文 HTML の書誌欄、ID と版履歴は abstract ページで確認した。PDF URL はリンクと HEAD のみ確認し、本文未取得。[書誌情報](https://arxiv.org/html/2409.12894v2)、[版履歴](https://arxiv.org/abs/2409.12894)

```tsv
title	year	venue	status	arxiv_id	pdf_url	code_url	topic	verify_url
VLATest: Testing and Evaluating Vision-Language-Action Models for Robotic Manipulation	2025	PACMSE 2 FSE; DOI:10.1145/3729343	出版情報・所属・HTML確認済み; PDF本文未取得	2409.12894	https://arxiv.org/pdf/2409.12894	https://github.com/ma-labo/VLATest	VLA評価・頑健性; 東京大学との共同研究	https://arxiv.org/html/2409.12894v2
```

## 7. 残る未確認事項

- Meta-World の公式の現在順位表、ManiSkill2 継続チャレンジの現在スコア、ManiSkill3 の汎用 VLA 順位、Isaac Lab-Arena の実測公開順位表。[確認先：Meta-World](https://metaworld.farama.org/)、[ManiSkill2](https://sapien.ucsd.edu/challenges/maniskill/challenges/ms2-ongoing)、[ManiSkill](https://www.maniskill.ai/)、[Isaac Lab-Arena](https://developer.nvidia.com/isaac/lab-arena)
- Gemini Robotics 2 の安全性レポート本文、モデル全体を説明する別の技術レポートの所在・arXiv ID、ブログ数値の試行数・誤差算出法。今回確認したのは公式ブログと安全性レポートへのリンクである。[確認先：DeepMind 公式ブログ](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)
- π*0.6 / π0.7 の公式公開重みと適用ライセンス。公式の配布先を確認するまでは公開済みに分類しない。[確認先：openpi](https://github.com/Physical-Intelligence/openpi)、[π*0.6](https://www.pi.website/blog/pistar06)、[π0.7](https://www.pi.website/blog/pi07)
