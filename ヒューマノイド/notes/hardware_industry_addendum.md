# ヒューマノイド 追補: 未確認項目の調査結果 (調査基準日 2026-10-31)

hardware_industry.md と venues.md で「未確認」だった項目の追補。[公式] = 公式ページを今回直接取得。[二次] = ニュース・販売店・まとめサイト (ベンダー自己申告を含む)。

## 1. Unitree 売上: 17.08 億元と 16.99 億元の差
- 2025 年売上高の数字は報道で 2 系統ある (原文の目論見書 PDF は今回も取得できず、一次確認は未了)。
  - 17.08 億元 (170,820.87 万元、前年比 +335.36%)、純利益 2.88 億元、扣非 6 億元 (+674.29%): 華爾街見聞 https://wallstreetcn.com/articles/3768005 [二次、IPO 受理時の報道]
  - 16.99 億元 (2023-2025 年: 1.59、3.93、16.99 億元)、純利益 -1,114.51 万、9,547.47 万、2.78 億元: 新華網 https://www.news.cn/tech/20260602/8463deaf5c1d4c748fdf73157a5befeb/c.html [二次、2026-06-02、「招股説明書によると」と記載]
  - 財聯社 https://www.cls.cn/detail/2319719 は 2025 年 1-9 月の売上が「10 億元超」、通期は「17 億元超の見込み」と記載 (初期段階の申報稿ベース)。
- 筆者の解釈 (推測): 前年 3.93 億元に +335.36% を掛けると約 17.1 億元で 17.08 と整合する。16.99 は同じ前年比と整合しない (約 +332%)。純利益も 2.88 億と 2.78 億で食い違う。よって、17.08/2.88 は申報時点の数字、16.99/2.78 は問い合わせ回答後の修正または上場時の数字 (監査・会計処理の調整) である可能性が高い。ただし原文で未確認。上場時点 (SSE/China Daily) の数字は約 17.0 億元・純利益 2.78 億元で後者と一致する (既存 notes の記載)。引用するなら 16.99 億元 (上場時点)、17.08 億元 (申報時点) と版を明記するのが安全。
- 出荷台数: 2025 年のヒューマノイド出荷は 5,500 台超 (複数報道で一致)。財聯社の「累計ほぼ 4,000 台」は申報稿時点 (2025 年 9 月末まで) の累計と読め、SSE/China Daily の 3 年累計 5,632 台とは基準時点が異なる。四足は累計 3 万台超。
- 1-9 月の売上構成: ヒューマノイド 5.95 億元 (主営業収入の 51.53%)、四足 4.88 億元 (42.25%) (華爾街見聞、cls.cn の検索要約と一致)。
- 資金使途 (モデル 20.22 億、機体 11.1 億、新型製品 4.45 億、製造拠点 6.24 億元) は検索結果の要約で再確認。原文は未確認。

## 2. 機体仕様の補完
| 機体 | 身長 | 重量 | 自由度 | バッテリー | 備考 | 出典 |
|---|---|---|---|---|---|---|
| Unitree H1 | 約 180cm | 約 47kg | 23 (脚 10x2、腕 8 ほか、拡張可) | 15Ah (0.864kWh)、最大 67.2V | 価格・SDK 記載なし。オプションで Intel i5/i7、Orin NX | [公式] https://www.unitree.com/h1 (小文字 URL で取得可。前回の大文字 URL は 404) |
| UBTECH Walker S2 | 176cm | 70kg (73kg の記載もあり) | 52 (手 11 DoF の第 4 世代手) | 2.3kWh、48V 二重、自動交換 3 分以内、稼働約 2h | 歩行 2m/s、片手把持 7.5kg。販売店経由 | [二次] 検索要約 (robotshop https://www.robotshop.com/products/ubtech-walker-s2-industrial-humanoid-robot 、SDK 文書 https://a.storyblok.com/f/298593/x/1329253096/ubtech-walker-s2-sdk-secondary-development-document-external.pdf)。公式 PDF は画像で読めず |
| AgiBot X2 | 約 1.31m | Ultra 約 39kg、EDU 約 33kg | Ultra 30 (新版 31)、EDU 29、片腕 7 | 約 421Wh、歩行約 2h (0.5m/s) | 最大 1.8m/s、ピークトルク 120N·m、ペイロード全域 1kg 以下 | [公式] https://x2-aimdk.agibot.com/en/latest/about_agibot_X2/robot_specifications.html |
| AgiBot A2 | 169cm | 55-69kg | 40+ | 未確認 | | [二次] 検索要約 https://community.robotshop.com/blog/show/choosing-an-agibot-humanoid-robot-a-buyers-guide-to-the-a2-x2-and-g2-lineups |
| AgiBot G2 (車輪型) | 1225-1795mm (可変) | 185kg | 26 | 未確認 | 腕 7DoF x2、腰 3 | [二次] 同上と販売店 PDF https://cdn.robotshop.com/media/A/Agb/RB-Agb-09/pdf/AgiBot-G2-Specification.pdf (本文未確認) |
| Xiaomi 新世代 CyberOne | 約 1.70m | 66kg | 66 (両手で 33) | 未確認 | 2026-08-19 WRC で公開。自動車工場の実習 4 か月 | [二次] 36Kr https://eu.36kr.com/en/p/3947315943472512 |
| Apptronik Apollo | 1.73m | 72.6kg | 34 | 最長約 4h、交換式 | ペイロード 25kg | [二次のみ] 販売・まとめサイトの検索要約 (https://qviro.com/product/apptronik/apollo/specifications 等)。公式ページは再度 404 (apptronik.com/apollo)。自己申告値に準じる |
| Tesla Optimus | 約 5'8" (172cm) | 57kg (Gen 3 の報道) | 体 28 + 手 22x2 とされる | 未確認 | 目標価格 US$2-3 万 | [二次] 検索要約 (https://humanoid.guide/product/optimus-gen-3/ ほか)。tesla.com は 403。V3 の公式発表・量産開始の事実は未確認 (「2026 年 7-8 月に前倒し」の報道のみ、https://optimusk.blog/blog/tesla-optimus-gen-3/ は個人ブログで信頼度低) |

Xiaomi の工場試験の数値 (36Kr): 自タッピングナット装着ステーションで両手作業の成功率 90.2% から 98%、中央コンソールのサイドカバー装着と材料箱の折りたたみ 90%、同ステーションで 3 時間連続稼働、ライン節拍 76 秒を満たした。すべて同社発表値 (自己申告)。

## 3. Figure の公式発表 (公式ニュース再取得)
[公式] https://www.figure.ai/news の一覧で次を確認 (本文個別記事は未取得):
- 2025-09-16 Series C 10 億ドル超、ポストマネー評価額 390 億ドル
- 2025-10-09 Figure 03 発表、2026-04-29 に生産増強の発表
- 2025-11-19 F.02 が BMW で 3 万台の生産に貢献、2026-06-30 F.03 が BMW に到着
- 2026-01-27 Helix 02、2026-03-09 居間の片付け、2026-05-08 寝室の片付け、2026-09-17 Helix 2.5 (30 軒でゼロショット汎化)
- 2026-08-25 Index (「世界最大・最多様の物理データセット」とされる)、2026-09-03 Nscale と最大 10 万 GPU (NVIDIA Vera Rubin) の提携、2026-09-30 F.02 退役
- 既存 notes の記載は一覧ページの見出しで裏付けられた。BMW 貢献台数の詳細は個別記事で未確認。
- Tesla の実績の公式発表は取得できず未確認 (tesla.com は 403)。

## 4. 日本 (東大 JSK・産総研)
- 東大 JSK の最新論文リスト: 一次ページを今回も取得できず未確認。確認できたのは次の間接情報のみ。
  - 川原圭博ではなく河原塚健人 (東大 情報理工、講師、2026 年時点) の KAKEN 課題: 「ロボットによるロボットのための逐次的技能訓練・拡張」(2026-2029、挑戦的研究 (開拓))、「可変身体と適応知能システムを備えた高出力ギアレス・ワイヤ拮抗駆動ロボット」(2024-2026) など。筋骨格ヒューマノイド、ワイヤ駆動が中心。 https://nrid.nii.ac.jp/ja/nrid/1000090964677
  - IEEE-RAS Humanoids 2025 で東大の論文が受賞候補 (下記)。
- 産総研の最近の公式発表: プレスリリースの一覧 URL (https://www.aist.go.jp/aist_j/press_release/pr2026/) は 404 で取得できず、未確認。

## 5. 学会の受賞 (公式ページ確認)
### RSS 2025 (公式 https://roboticsconference.org/2025/program/awards/)
- Outstanding Paper: "FEAST: A Flexible Mealtime-Assistance System Tackling In-the-Wild Personalization" (Jenamani et al.)。finalist は "FAST: Efficient Action Tokenization for Vision-Language-Action Models" (Pertsch et al.) と "Solving Multi-Agent Safe Optimal Control with Distributed Epigraph Form MARL" (Zhang et al.)。
- Outstanding Student Paper: "Solving Multi-Agent Safe Optimal Control with Distributed Epigraph Form MARL" (Zhang et al.)。finalist は Doppler Correspondence、Reactive Diffusion Policy。
- Outstanding Systems Paper: "Building Rome with Convex Optimization" (Han & Yang)。finalist に **"Learning Humanoid Standing-up Control across Diverse Postures" (Huang et al.)** (ヒューマノイド関連。arXiv ID は今回未確認)。
- Outstanding Demo Paper: "Demonstrating MuJoCo Playground" (Zakka et al.)。
- 結論: RSS 2025 の主要受賞にヒューマノイド論文の受賞はなく、systems paper の finalist のみ。前回 venues.md の Berkeley Humanoid Lite と ASAP は受賞ではない。

### IEEE-RAS Humanoids 2025 (ソウル、公式 https://2025humanoids.org/awards/)
- Best Oral Paper: "Design of a 3-DOF Hopping Robot with an Optimized Gearbox" (Choe et al., KAIST)。finalist: "Physically Consistent Humanoid Loco-Manipulation Using Latent Diffusion Models" (Taouil et al., TUM)、"Geometry-Aware Predictive Safety Filters on Humanoids" (Bena et al., Caltech)。
- Mike Stilman Award: "From Screen to Stage: Kid Cosmo, a Life-Like, Torque-Controlled Humanoid for Entertainment Robotics" (Liu et al., UCLA)。finalist: 東大 Hirai et al. "Development of a Transformable Robot with Wire-Differential Steering Ankle Joints"、CMU "Walking, Rolling, and Beyond..."。
- Best Interactive Paper: "Design and Experiment of Hydraulic Driven Deformable Wheeled Biped Robot" (Li et al., HIT)。finalist は東大 2 件 (Arai et al. "Motion Generation and Burden Evaluation of Sitting-Up Assistance by Humanoid Robot"、Hattori et al. "Design and Development of a Remotely Wire-Driven Walking Robot")。
- 論文 ID (Paper 番号) は会議内番号で arXiv ID ではない。Humanoids 2024 は未確認。

### IROS 2025 (杭州)
- [二次] 検索要約: Best Conference Paper は中国科学院瀋陽自動化研究所の生体融合ロボット電極の論文、Best Student Paper は Neural MP (Dalal et al., CMU)、"Unified Whole-Body Policy" が finalist との記述。公式の受賞者ページは取得できず未確認。出典 https://newshub.sustech.edu.cn/en/?p=47545 、https://ramagazine.ieee.org/2026/06/29/advancing-the-human-robot-frontiers-through-global-collaboration-a-recap-of-iros-2025-in-hangzhou-china-conference-highlights/ (本文に受賞者なし)。IROS 2024・2026 は未調査。

## 6. 残る未確認
- Unitree 目論見書の原文 (上交所/巨潮資訊網) と 17.08/16.99 の版の特定。
- Apptronik Apollo と Tesla Optimus の公式仕様 (公式サイトが 404/403)、Optimus V3 の実際の発表。
- AIST と東大 JSK の 2025-2026 年の論文・発表。
- Humanoids 2024、IROS 2024・2026、RSS/CoRL 2026 の受賞。
