# IEEE 系 (ICRA / IROS / RA-L / T-RO) の VLA・ロボット基盤モデル論文 補遺 (2024-2026)

調査基準日: 2026-10-31。候補は `venues_ieee_candidates.tsv` (28 件)。既存の venues.md / venues_candidates.tsv と重複するものは除いた。

## 1. 結論
- 公式の採択一覧 (IEEE Xplore, PaperPlaza, dblp) は取得できなかった (dblp は Anubis により 403、IEEE Xplore は 418)。ICRA/IROS/RA-L/T-RO の網羅的な一覧は作れていない。
- 代わりに Semantic Scholar の検索 API (https://api.semanticscholar.org/graph/v1/paper/search, venue と year で絞り込み) を使った。ICRA 100 件 (2024: 28, 2025: 54, 2026: 18)、IROS 183 件、T-RO 100 件を取得し、タイトルで VLA・基盤モデル・汎用ポリシーに該当するものを手で選んだ。検索結果は上位に偏り、網羅的ではない。RA-L は venue 名の指定で 0 件だった (未取得)。
- 年の判定は DOI 接頭辞による。10.1109/ICRA55743.2025 は ICRA 2025、10.1109/ICRA57385.2026 は ICRA 2026、10.1109/ICRA57147.2024 は ICRA 2024、10.1109/IROS60139.2025 は IROS 2025、10.1109/IROS58592.2024 は IROS 2024。これは Semantic Scholar 上の書誌情報であり、IEEE 公式一覧との突き合わせはしていない。
- 重要: 論文の arXiv 投稿年と学会年は一致しない。例えば FP3 は arXiv 2025-03 だが、DOI は ICRA 2026 (https://www.semanticscholar.org/ で確認、取得 URL は TSV の verify_url)。

## 2. arXiv の comments 欄で学会名を確認できたもの (個別ページ)
- DAM-VLA: comments 欄に "Accepted to ICRA2026" https://arxiv.org/abs/2603.00926
- Dexora: comments 欄に "Accepted by ICRA 2026" https://arxiv.org/abs/2605.18722 。ICRA 2026 の Best Paper finalist (Robot Manipulation and Locomotion 部門) でもあると二次情報 (bohrium) が述べる。公式は未確認。
- 確認できなかったもの (comments 欄に学会名なし): TinyVLA https://arxiv.org/abs/2409.12514 (RA-L 2025 は awesome-list と検索結果のみ)、Developing VLA from Egocentric Videos https://arxiv.org/abs/2509.21986 (ICRA 2026 は検索結果上の著者 LinkedIn のみ)、FP3 https://arxiv.org/abs/2503.08950、Octo https://arxiv.org/abs/2405.12213 (RSS 2024 のはずで、awesome-list の "ICRA 2024" 表記は誤りの疑い)、Open X-Embodiment https://arxiv.org/abs/2310.08864 (ICRA 2024 Best Conference Paper という検索結果の二次情報のみ)。

## 3. ICRA 2026 (ウィーン, 2026-06-01〜05, 約 1,800 件採択 / 5,088 投稿は二次情報)
Semantic Scholar の DOI (10.1109/ICRA57385.2026) で確認 (書誌のみ): OmniVLA (ナビゲーション VLA, 2509.19480)、Goal-VLA (2506.23919)、FP3 (3D 基盤ポリシー, 2503.08950)、IVRA (2601.16207)、Scalable VLA Pretraining with Real-Life Human Activity Videos (2510.21571)、GRAPE (2411.19309)、SINGER (2509.18610)、The One Ring (2412.14401)、DemoDiffusion (2506.20668)、COMPASS (2502.16372)、Learning Generalizable Robot Policy with Human Demonstration Video as a Prompt (2505.20795)、SOE、AnchorDream、Embodiment-Aware Generalist Specialist Distillation ほか。
注: 2024 年や 2025 年の arXiv 論文が ICRA 2026 に載っている (GRAPE は 2024-11 投稿)。

受賞 (二次情報 https://www.bohrium.com/en/blog/icra-2026-papers-to-read/、公式未確認): Best Paper finalist 12 件のうち、VLA・基盤モデル関連は FP3 (Robot Learning 部門)、Dexora (Manipulation and Locomotion 部門)、Uncertainty Comes for Free (拡散ポリシーの HIL)。FindAnything と IMR-LLM は VLM/LLM 系。

ワークショップ: "From Data to Decisions: VLA Pipelines for Real Robots", 2026-06-05 ウィーン。主催は AIRoA (Kris Wu, Kei Ota)、Oxford/Amazon Robotics の Jun Yamada と Ingmar Posner、東大の Tatsuya Matsushima、早大の Tetsuya Ogata、USC の Ishika Singh。採択論文の一覧はページ上になし (発表日 2026-05-01 とのみ記載) https://icra2026vlapipeline.github.io 。vla-eval (arXiv 2603.13966) がこのワークショップに採択されたとの検索結果があるが、arXiv の comments 欄には記載なく未確認。

## 4. ICRA 2025 / 2024
- ICRA 2025 (DOI 10.1109/ICRA55743.2025、書誌のみ): Robot Utility Models (2409.05865)、KALIE (2409.14066)、FLaRe (2409.16578)、Robot Policy Transfer with Online Demonstrations (2503.12993)。既存ノート掲載分は除外。
- ICRA 2024: 今回の検索では VLA・基盤モデルに該当するものは Open X-Embodiment のみ (上記)。

## 5. IROS
- IROS 2025 (DOI 10.1109/IROS60139.2025): 検索で 107 件取得 (2024 年扱い含む)。VLA・基盤モデルに該当する新規は少なく、既存ノートの PD-VLA, CLAP, RoboNurse-VLA, Refined Policy Distillation が再確認できた程度。
- IROS 2024: GenCHiP (2404.06645, コードによるポリシー生成)。
- IROS 2026 (2026-10): 採択一覧は取得できず未確認。検索結果は CLAM (連続潜在行動モデル) が IROS 2026 採択と述べるが、arXiv ページ未確認のため TSV には入れていない。

## 6. RA-L / T-RO
- T-RO (DOI 10.1109/TRO.2026): FlowVLA (2508.18269、既存ノート掲載、DOI で確認)、Embodied Robot Manipulation in the Era of Foundation Models (サーベイ, 2512.22983)、From Ill-Posed to Well-Posed (基盤モデル利用のロボット学習フレームワーク)。TaF-VLA (2601.20321) は書誌の DOI が arXiv のもので、T-RO 掲載は書誌の venue 欄のみ (弱い根拠)。
- RA-L: VLA-Touch が RA-L vol.11 no.7 pp.8487-8494 (2026-07) https://researchr.org/publication/BiMHSS26/bibtex 。TinyVLA の RA-L 2025 は未確認。RA-L の網羅的な一覧は取得できなかった。

## 7. 注意点・未確認
- awesome-list (https://github.com/Psi-Robot/Awesome-VLA-Papers の取得結果、要約ツール経由) は ICRA/IROS/RA-L タグを持つが、Octo の誤りの疑いがあり、arXiv コメントと突き合わせるまで根拠としない。
- 取得 API の venue 絞り込みは名称ゆれ (例: IROS の綴り "IEEE/RJS ...") があり、取りこぼしがある。ICRA の「vision-language-action」クエリ自体は大量ヒットしても 100 件単位の上位のみ。
- 本ファイルの venue は、DAM-VLA と Dexora を除きすべて二次書誌 (Semantic Scholar、検索結果) であり、公式採択一覧での確認ではない。
