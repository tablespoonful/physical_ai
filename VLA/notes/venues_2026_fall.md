# CoRL 2026 / NeurIPS 2026 の VLA・ヒューマノイド・世界モデル論文

調査基準日: 2026-10-31。候補の全リストは `venues_2026_fall_candidates.tsv` (181 行)。既存の `venues.md` は読むだけで、変更していない。

## 1. CoRL 2026: 公式の採択一覧を確認できた

- 公式の採択一覧: https://www.corl.org/program/accepted-papers (2026-10-19 公開。出典: https://www.corl.org/ のお知らせ欄)
- 件数 (一覧ページ冒頭と公式 X の告知): 採択 687 件、oral 21、spotlight 72。応募 2,094 件 (active)、採択率 32.8%。出典: https://x.com/corl_conf/status/2095971635593404733 (検索結果のスニペットで確認。ページ本体は HTTP 402 で未取得)。
- 会期: 本会議 2026-11-09〜11、ワークショップ 11-12、テキサス州オースティン (https://www.corl.org/)。
- 確認方法: 一覧ページはサイト内の埋め込み表示で、ページ内検索ボックスに "VLA" / "humanoid" / "world" を入力し、表示された題名を目視で書き起こした。一括取得はしていない。各題名は OpenReview へのリンクになっているが、OpenReview 本体 (https://openreview.net/group?id=robot-learning.org/CoRL/2026/Conference) は読み込み前の画面で、内容は確認できなかった。
- 検索ヒット数 (重複を含む): "VLA" 76 件 (うち spotlight 8 件の重複を除くと 68 件)、"humanoid" 74 件、"world" 91 件。TSV はこれらから、世界モデルでも VLA でもない題名 (real-world / open-world だけで当たったもの) を除いた 178 件。
- TSV の内訳 (CoRL 分 178 件): VLA 71、humanoid 61、worldmodel 46。NeurIPS 3 件を含めた合計は VLA 73、humanoid 61、worldmodel 47。VLA 検索に当たった題名のうち世界モデルを題名に含むもの (PLaW-VLA、WoVR など) は topic を VLA にした。
- 取りこぼしの可能性: 題名に VLA / humanoid / world を含まない論文 (例: 題名が "Vision-Language-Action" だけの論文は "VLA" 検索に当たらない可能性、"whole-body"、"WAM" だけの題名) は拾えていない。humanoid は表示が長く、各セッションを連続して確認したが、画面外の行の見落としがありうる。
- 題名は CoRL の採択一覧のとおり。arXiv の題名と異なる場合がある。

### 代表的な論文 (すべて公式一覧で確認)
- oral: "World Action Models are Zero-shot Policies" と "Memory-augmented Action-conditioned World Model for Robot Manipulation" (Oral O2 世界モデル枠)、"GRAIL: Generating Humanoid Loco-Manipulation from World Models"、"RoboNaldo"、"SuperMimic" (Oral O7 ヒューマノイド枠)。
- spotlight (VLA): "Learning What to Say to Your VLA"、"ZETA"、"BitVLA"、"EagleVLA"、"REACT"、"Never Too Late for Force"、"Demystifying When and Why VLAs Fail in Contact-Rich Tasks"、"MolmoAct2: Action Reasoning Models for Real-World Deployment" ほか。
- spotlight (ヒューマノイド): "Humanoid Navigation in Cluttered Environments with a Whole-Body Vision-Language-Action Model"、"LadderMan"、"OpenHLM"、"PHUMA"、"ResSafe"、"TactileStep" (Spotlight S7)。
- 傾向 (一覧からの観察): VLA の推論高速化・非同期実行 (FlashVLA、AsyncVLA ほか)、力・触覚を VLA に入れる論文、世界モデルと行動を一体で扱う "World Action Model (WAM)" 系 (20 件以上)、ヒューマノイドの全身制御・ロコマニピュレーションが目立つ。

### arXiv で確認できたもの (arXiv ページで "Accepted at CoRL 2026" を確認)
| 論文 | arXiv | 出典 |
|---|---|---|
| HuRo: Robotizing Human Videos for Scalable VLA Pretraining (RLWRLD、630K エピソード) | 2609.10706 (comments: Accepted at CoRL 2026) | https://arxiv.org/abs/2609.10706 |
| SuperMimic (Oral) | 2610.28480 (comments: Accepted at CoRL 2026 (Oral)) | https://arxiv.org/abs/2610.28480 |
| Intercepting the Future: Latent-Space Predictive World Model for Dynamic VLA Manipulation | 2606.02486 (CoRL 2026 採択と記載) | https://arxiv.org/abs/2606.02486 |

- FlowVLA: 公式一覧に "FlowVLA: Enabling World Dynamics Understanding through Pluggable 3D Flow Learning" がある。検索では arXiv 2508.18269 が CoRL 2026 採択と紹介されたが、arXiv の最新題名は "FlowVLA: Visual Chain of Thought-based Motion Reasoning for Vision-Language-Action Models" (v3, 2025-10-07) で、題名が異なる。同一論文か未確認のため TSV の arxiv_id は空欄 (https://arxiv.org/abs/2508.18269)。
- RLWRLD の告知 (二次情報、https://digg.com/ai/y7iy3i1r) に、HuRo のほか "Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models"、"Robot-Factored World Models via Robot Rendering" (公式一覧にも題名あり)、"AutoDex"、"Learning Unions of Convex Sets..." があった。Modular Sensory Stream は VLA 検索の画面では確認していない (未確認)。
- 上記以外の arxiv_id は未確認で、TSV では空欄。

## 2. NeurIPS 2026: 公式の採択一覧は未確認

- 採択通知日 2026-09-24 (https://neurips.cc/Conferences/2026/Dates の取得結果、https://neurips.cc/Conferences/2026/CallForPapers でも AoE の通知日を確認)。
- 開催: シドニー 12 月 6〜12 日、アトランタ 12 月 9〜13 日、パリ 12 月 9〜13 日 (https://neurips.cc/Conferences/2026/Dates の取得結果。日付は要再確認)。
- 公式の採択論文ページ https://neurips.cc/virtual/2026/papers.html は、ブラウザで開いても「Loading...」のままで、論文は表示されなかった (基準日時点で未公開か、読み込みできない状態。どちらかは未確認)。
- 公開予定日: camera-ready 期限と、OpenReview / proceedings での公開日を示すページは見つけられなかった (未確認)。例年の proceedings は会期の直前に公開されるが、2026 年の日程としては未確認。
- 確認方法の代替: arXiv のコメント欄で "accepted at NeurIPS 2026" と書かれた論文を、検索で見つけた GitHub の日次まとめ (二次情報: https://github.com/guoyue0412/DailyArxiv/issues/100) から拾い、各 arXiv ページで直接確認した。3 件のみで、網羅的ではない。

| 論文 | topic | arXiv (コメント欄を確認) | コード |
|---|---|---|---|
| NestedVLA: Learning to Consolidate and Generate Skills for VLA Models | VLA | https://arxiv.org/abs/2610.23271 ("accepted at NeurIPS 2026"、camera-ready 版) | https://github.com/WanyuGroup/NeurIPS2026-NestedVLA |
| CondenseVLA: Learnable History Condensation for Efficient Multi-Frame VLA | VLA | https://arxiv.org/abs/2610.25927 ("Accepted at NeurIPS 2026") | https://github.com/FeiyangHong/CondenseVLA |
| AEON: Unifying Video and 3D World Models | worldmodel | https://arxiv.org/abs/2610.28631 ("Accepted to NeurIPS 2026") | (arXiv ページに明記なし。project: https://weiqi-zhang.github.io/AEON) |

- 注意: ある検索結果の要約は DreamVLA、ThinkAct、CogVLA などを「NeurIPS 2026 採択」と書いていたが、これらは NeurIPS 2025 の論文と思われ (既存の venues.md にも NeurIPS 2025 として DreamVLA、ThinkAct がある)、採用していない。
- 検索で出た他の論文 (UniWALM、EMMA など) は、NeurIPS 2026 採択の根拠が二次情報の要約だけで、arXiv ページを確認していないため採用していない。

## 3. 残った未確認事項
- NeurIPS 2026 の公式採択一覧 (VLA・ヒューマノイド・世界モデルの全数) と、公開予定日。
- CoRL 2026 の proceedings (PMLR) の公開時期 (基準日時点で PMLR 掲載なし。例年は会期後。2026 年の予定は未確認)。
- CoRL 論文の arXiv ID (上記 3 件以外)。公式一覧の各題名は OpenReview へのリンクだが、内容は未確認。
- CoRL 2026 の Best Paper 等の受賞 (一覧ページと公式サイトの取得範囲では見つからず、未確認)。
