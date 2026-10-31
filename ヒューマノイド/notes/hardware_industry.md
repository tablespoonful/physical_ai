# ヒューマノイド 機体・企業・日本の動向 (調査基準日 2026-10-31)

凡例: [公式] = 当該社の公式ページを直接取得。[二次] = ニュース、販売店、まとめサイト経由 (ベンダー自己申告を含む)。「未確認」= 取得できなかった。

## 1. 機体仕様の比較表

| 機体 | 身長 | 重量 | 自由度 | 手 | バッテリー | 価格 | SDK / 研究用途 | 出典 |
|---|---|---|---|---|---|---|---|---|
| Unitree G1 | 1320mm (折畳み690mm) | 約35kg | 23 (EDU は 23-43) | 標準は手なし。EDU は Dex3-1 (3 本指、7DoF) を選択可 | 9000mAh、約2h | 標準 US$13.5K (税・送料別)。EDU は問い合わせ | EDU が二次開発対応 | [公式] https://www.unitree.com/g1 |
| Unitree H1 | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | https://www.unitree.com/H1 は 404 で取得できず |
| Unitree H2 | 1820mm | 約70kg | 31 | 標準は手なし。EDU で複数選択 | 15Ah、最大75.6V、約3h | 標準 US$29,900。EDU は問い合わせ | EDU が二次開発対応 | [公式] https://www.unitree.com/H2 |
| Unitree R1 | 1230mm | 27kg (AIR) / 29kg (R1, EDU) | 20 (AIR) / 26 (R1, EDU) | 未確認 | 約1h | AIR US$4,900、R1 US$5,900、EDU は問い合わせ | EDU あり (詳細未確認) | [公式] https://www.unitree.com/R1 |
| Booster T1 | 約1.18m | 約30kg | 23 (グリッパー版31、手版41) | オプション (6DoF 手) | 未確認 | US$51,800-75,000 (販売店表示) | ROS 2、オープン API (販売店記載) | [二次] https://www.generationrobots.com/en/404278-booster-t1-humanoid-robot.html 、https://www.robotshop.com/products/booster-t1-humanoid-robot-dextrous-hands 。公式 https://www.booster.tech/booster-t1/ は T2/K1 を掲載し T1 の数値なし。公式ドキュメント https://docs.booster.tech/zh-CN |
| Fourier GR-3 | 165cm | 71kg | 55+ | 多指手 | 約3h (ホットスワップ) | US$119,995 (販売店表示) | 未確認 | [二次] https://rbtx.de/en-GB/components/humanoid/fourier-gr3-humanoid-robot-care-bot 。公式ドキュメント https://support.fftai.com/en/docs/GR-X-Humanoid-Robot/GR3/GR-3_Introduction/ は本文未取得 |
| Figure 03 | 168cm | 60kg | 42 (手に20) | 多指手 | 2.3kWh、ピーク約5h、無線充電 | 非公開 | 研究用販売は未確認 | [二次] 検索結果の要約 (https://humanoid.guide/product/figure-03/ ほか)。公式 figure-03 ページは 404 で未取得 |
| Tesla Optimus | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 外部販売なし | tesla.com/optimus は 403 で取得不可 |
| 1X NEO | 5'6" (約168cm) | 66 lbs (約30kg) | 手22x2、腕7x2、首3、背骨2、脚6x2 | 22DoF/手 | 842Wh、約4h | US$20,000 (Early Access) または US$499/月。デポジット US$200 | 家庭向け。研究用 SDK は未確認 | [公式] https://www.1x.tech/neo (仕様、デポジット)。価格は [二次] https://www.eweek.com/news/1x-neo-humanoid-home-robot-2026/ |
| Agility Digit | 175cm | 65kg | 未確認 | グリッパー交換式 | 4-8h (二次情報) | 非公開 | 法人向け。研究用は未確認 | 公式 https://agilityrobotics.com/solutions/digit は Digit 5 を「開発中」とし、ペイロード23kg、到達2.2m、20h/24h 稼働を掲載。身長・重量・バッテリーは [二次] https://qviro.com/product/agility-robotics/digit/specifications |
| Apptronik Apollo | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 非公開 | 未確認 | apptronik.com/apollo は 404。資金調達は下記 |
| Boston Dynamics Atlas (製品版) | 1.9m | 90kg | 56 | 公式ページに詳細なし | 4h、自己交換式 | 非公開 | 少数の早期導入先のみ。研究用販売は未確認 | [公式] https://bostondynamics.com/products/atlas/ |
| AgiBot | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 仕様は未取得。出荷実績は下記 |
| UBTECH Walker S2 | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 非公開 | 産業向け | 仕様は未取得。受注は下記 |
| Xiaomi | 未確認 | 未確認 | 未確認 | 未確認 | 未確認 | 非売品 | なし | 仕様は未取得。工場試験は下記 |

注意:
- Unitree、Atlas、1X の数値は公式ページ取得。Booster、Fourier、Figure、Digit の一部は販売店や集約サイト経由で、ベンダー自己申告に準じる。
- 研究用途で買えるか: Unitree (G1 は標準で購入可、EDU で二次開発) と Booster T1 (販売店で購入可) は確認。Figure、Atlas、Digit、Optimus、Apollo は研究用の一般販売を確認できなかった。

## 2. オープンハードウェア
- Berkeley Humanoid Lite: 3D プリント、部品は EC で入手、総額 US$5,000 未満、ハード設計・組込みコード・学習環境を公開、RSS 2025。論文 https://arxiv.org/abs/2504.17249 、プロジェクト https://lite.berkeley-humanoid.org
- ToddlerBot: 高さ0.56m、3.4kg、3D プリント+市販部品、総額 US$6,000 未満、オープンソース。論文 https://arxiv.org/abs/2502.00893 、https://toddlerbot.github.io/
- Berkeley Humanoid (中型の研究用機体): https://arxiv.org/abs/2407.21781 (オープン度は未確認)
- Open Duck Mini、Roboto Origin など: 一次ページを確認できず、未確認。

## 3. 各社の直近の実績

### Unitree (目論見書・上場)
- 上場: 2026-08-19 に上海証券取引所 STAR 市場で取引開始 (688836)。公募価格150.80元、約40.45百万株 (上場後株式の10%)、調達額約61億元。初値は1,100元 (公募価格比+629%)。出典 https://www.caixinglobal.com/2026-08-19/chinese-robot-maker-unitree-soars-629-in-shanghai-debut-102475578.html (検索結果の要約のみ、本文未取得)、https://english.sse.com.cn/news/newsrelease/voice/c/c_20260811_10828578.shtml (SSE 英語版が掲載した China Daily 記事)、https://autonews.gasgoo.com/articles/news/unitree-launches-star-market-ipo-issuance-process-subscriptions-open-august-10-2083181368883253248
- 主幹事は CITIC Securities。申込は2026-08-10 開始 (gasgoo)。
- 目論見書由来の数値 (二次報道経由。目論見書原文は取得できず「未確認」):
  - 2025年売上高: 約17億元 (SSE/China Daily は 1.70 billion yuan、gasgoo は 1.699 billion yuan)。中国語報道 (cls.cn など) の「17.08億元、前年比+335.36%」は末尾が合わないため要確認。
  - 2025年のヒューマノイド出荷は5,500台超、2023-2025年累計5,632台 (SSE/China Daily)。中国語報道は「報告期間の累計ほぼ4000台」と記述しており、期間の定義が異なる可能性。
  - 2025年 純利益2.78億元、非経常損益控除後の親会社帰属で5.91億元、海外売上7.32億元 (主営業収入の43.65%)。(SSE/China Daily)
  - 2025年1-9月にヒューマノイド収入 (5.95億元) が四足 (4.88億元) を初めて上回った (51.53%)。(https://www.kucoin.com/news/flash/analysis-of-unitree-s-ipo-filing-reveals-robot-market-realities と中国語検索結果 cls.cn、10jqka)
  - 資金使途: モデル研究開発20.22億元、機体研究開発11.1億元、新型製品4.45億元、製造拠点6.24億元 (中国語検索結果の要約、原文未確認)。
- 一次情報の探索結果: SSE 英語版ニュースは取得できたが、目論見書 PDF (上交所 科創板の公告) には到達できなかった。次は上交所の科創板「宇树科技」公告ページか巨潮資訊網で原文を取得する必要がある。

### AgiBot
- 2026-03-30 に累計10,000台目のヒューマノイドを発表 (二次報道。例 https://www.roboticstomorrow.com/story/2026/03/agibot-reaches-10000-units-as-real-world-demand-for-robots-accelerates/26331/)。2025年出荷5,100台超でシェア39%は分析会社由来の二次情報。公式プレスリリース原文は未確認。

### UBTECH
- Walker S2 は量産・納入開始、受注8億元超 (Kyodo PR Wire 配信 https://kyodonewsprwire.jp/index.php/release/202511179261 、2025年11月、検索結果のタイトルで確認)。2025年の人型ロボット受注合計14億元は [二次] 報道。Airbus 案件は https://www.bloomberg.com/news/articles/2026-01-19/airbus-humanoid-order-sends-chinese-robot-maker-s-shares-surging (見出しのみ)。年内の生産目標は二次情報で未確認。

### Figure
- 公式ニュース https://www.figure.ai/news の要約: 2025-09-16 に Series C で10億ドル超、ポストマネー評価額390億ドル。2025-10-09 に Figure 03 発表。2025-11-19 に BMW で F.02 が車両3万台の製造に貢献。2026-06-30 に F.03 が BMW に到着。2026-01-27 に Helix 02。2026-09-17 に Helix 2.5 (30軒の家で zero-shot)。小型モデル経由の要約なので原文確認が望ましい。

### Apptronik
- 2026-02-11 に Series A-X 拡張で5.2億ドル、Series A 合計9.35億ドル超、総調達額は約10億ドル、評価額55億ドル超と報じられた (プレスリリース https://apptronik.com/news-collection/apptronik-closes-over-935-million-series-a は検索結果で確認、本文未取得。二次 https://www.therobotreport.com/apptronik-brings-in-another-520m-to-ramp-up-apollo-production/)。2026年内に新型ロボット発表予定と報じられた。

### 1X
- Hayward 工場が2026-04-30 に本格生産開始 (二次: https://www.eweek.com/news/news-1x-california-factory-neo-humanoid-robot/)。初年度1万台分が5日で売り切れたという記述あり。顧客出荷は2026年内予定で、実際の出荷は未確認。

### Tesla Optimus
- Q1 2026 決算説明会で V3 の発表を量産開始に合わせて2026年7-8月に前倒しとの報道 (二次)。実際の発表と量産状況は未確認。

### Boston Dynamics
- Atlas 製品版を少数の早期導入先に提供。Hyundai が最初の顧客パイロット (公式 https://bostondynamics.com/products/atlas/)。

### Xiaomi
- 自動車工場で人型ロボットの試験運用を開始、5年以内の大規模導入を目標 (https://technode.com/2026/03/03/xiaomi-says-humanoid-robots-begin-factory-trials-targets-large-scale-deployment-within-five-years/)。2026-08-19 の WRC で新世代機を公開 (二次)。「98% 成功率」は同社自己申告 (TechRepublic の検索結果)。

### その他
- Humanoid (英国): 2026-07-24 に Series A 1.52億ドル、ポストマネー13.5億ドル、総調達2.7億ドル、2026年第4四半期にベータ展開予定 (https://kyodonewsprwire.jp/release/202607243051)。

## 4. 日本の研究と企業
- 産総研 HRP-5P: 身長182cm、体重101kg、37自由度、石膏ボード施工を想定 (検索結果の要約。出典 https://monoist.itmedia.co.jp/mn/articles/1810/23/news039.html は2018年の記事)。最近の AIST 公式発表は未確認。
- 川崎重工 Kaleido: 東大との共同開発、2017年の国際ロボット展で初公開。2025年国際ロボット展 (2025-12-03〜06) で第9世代を公開、30kg の棚を移動、HMD で遠隔操作 (https://news.mynavi.jp/techplus/article/20251205-3764371/ ほか検索結果、本文未取得)。2026年5月に米サンノゼに Kawasaki Physical AI Center を設立、Foxconn と看護補助ロボット Nurabot を共同開発 (検索結果の要約、一次ページ未確認)。2018年記事 https://newswitch.jp/p/15337 は Kaleido と HRP-5P の制御基盤整備を報じている。
- 東大 JSK: 最近の一次情報を取得できず「未確認」。
- Honda: 2026年4月に P2 を展示、4本指ロボットハンドの実演 (二次 https://www.eweek.com/fr/news/apac-chinese-humanoids-japan-robotics-race/)。
- トヨタ: CUE7 (身長2m超) の展示 (同上、二次)。
- 政策: 経産省と NEDO が205億円のフィジカル AI 開発プログラム。ハードはヒューマノイドに限定しない (https://newswitch.jp/ の検索結果、個別記事 URL は未確認)。
- GITAI: 2024年11月に Series B 拡張で1,550万ドル (https://thebridge.jp/2024/11/gitai-series-b4-round-funding)、ISS 向け S2 アームの船外実証を計画。ヒューマノイドではなく宇宙作業ロボット。2026年の最新情報は未確認。
- 日本語資料: monoist の 2025 国際ロボット展レポート https://monoist.itmedia.co.jp/mn/articles/2512/23/news026.html 、Humanoids Summit Tokyo 2026 https://www.businesswire.com/news/home/20260408592677/en/Global-Robotics-Industry-Converges-on-Japan-for-Humanoids-Summit-Tokyo-2026 。
