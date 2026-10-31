# 世界モデル論文：学会・採択・受賞の確認

調査基準日：2026-10-31。以下は確認できた代表論文の選集であり、全採択論文の網羅一覧ではない。学会名・年・採択は公式proceedings／公式プログラムを優先し、プレプリントは別扱いにした。PDFはダウンロードしていない。

## 年の読み方と採録基準

- `candidates.tsv`の`year`は、採択確認済み論文では会議開催年／雑誌掲載年、会議未確認のものではプレプリント公開年。CoRL 2024のPMLR刊行年は2025なので、会議年と刊行年を混同しない。[PMLR 270巻](https://proceedings.mlr.press/v270/)
- `status`の「本会議採択」「公式プログラム掲載」「プレプリント」「ワークショップ受賞」は異なる証拠の強さを表す。「公式プログラム掲載」は個別proceedingsや受賞まで確認したという意味ではない。
- arXiv IDは個別の論文ページまたは原著者の書誌情報で実在を確認した値だけを記録。`未確認`のID／PDF URL／code URLを類似タイトルやURL規則から補っていない。PDF URLはリンクの存在までの確認で、ファイルの到達性・内容・checksumは未検証。

## 指定6学会：2024〜2026年の代表論文

| 会議 | 年 | 確認済みの代表論文・研究上の位置づけ | 採択・受賞の確認範囲 |
|---|---|---|---|
| CoRL | 2024 | [Dreamitate: Real-World Visuomotor Policy Learning via Video Generation](https://proceedings.mlr.press/v270/liang25b.html)：生成した実行動画から実機を制御。[Multi-Task Interactive Robot Fleet Learning with Visual World Models](https://proceedings.mlr.press/v270/liu25g.html)：未来の行動結果から異常を予測し、人の介入を組み込む。 | PMLR本会議論文。刊行年は2025、会議年は2024。[巻情報](https://proceedings.mlr.press/v270/) |
| CoRL | 2025 | [LaDi-WM: A Latent Diffusion-Based World Model for Predictive Manipulation](https://proceedings.mlr.press/v305/huang25a.html)：DINO／CLIP系潜在表現を予測。[DreamGen: Unlocking Generalization in Robot Learning through Video World Models](https://proceedings.mlr.press/v305/jang25a.html)：動画世界モデルによるデータ生成。 | PMLR本会議採択。受賞は本調査では未確認。DreamGenはarXiv版と会議版で副題が異なる。[arXiv版](https://arxiv.org/abs/2505.12705) |
| CoRL | 2026 | 公式サイトに10月19日の採択一覧公開告知あり。ただし取得した[採択一覧ページ](https://2026.corl.org/program/accepted-papers)では一覧本文が取得できず、個別の世界モデル論文は未確認。 | 会議は11月9〜12日で基準日より後。採択未発表とは書かないが、受賞済みとも書かない。[開催日・告知](https://2026.corl.org/) |
| RSS | 2024 | [Advancing Humanoid Locomotion: Mastering Challenging Terrains with Denoising World Model Learning](https://www.roboticsproceedings.org/rss20/p058.html)：人型の歩行制御。[World Models for General Surgical Grasping](https://roboticsproceedings.org/rss20/p041.html)：手術環境の視覚運動制御。 | 公式proceedingsで本会議採択。双方とも実機評価を原著者が報告。受賞は未確認。 |
| RSS | 2025 | [Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets](https://www.roboticsproceedings.org/rss21/p015.html)：動画・行動の拡散を統合。 | RSS本会議採択。ICML 2025ワークショップのBest Paper Awardは別の賞であり、RSS Best Paperとしない。[著者ページ](https://weirdlabuw.github.io/uwm/) |
| RSS | 2026 | [Self-Improving Robot Policy with Compositional World Model](https://www.roboticsproceedings.org/rss22/p012.html)：RISE、未来生成とprogress valueによる想像内の方策改善。ほかにAct2Goal、Causal World Modeling、Simulation Distillation等が[公式目次](https://www.roboticsproceedings.org/rss22/)に掲載。 | RISEは本会議採択。目次だけ確認した他論文の実装・数値・賞は未確認。 |
| ICRA | 2024 | [TWIST: Teacher-Student World Model Distillation for Sim-to-Real Transfer](https://ori.ox.ac.uk/people/jack-collins)：特権状態のteacherから視覚studentへ世界モデルを蒸留。 | 著者所属研究所の書誌情報でICRA 2024を確認。IEEE個別ページはJavaScript検証画面で本文未取得。[IEEEページ](https://ieeexplore.ieee.org/document/10610450)。arXiv版には題名中にEfficientが入る。[arXiv](https://arxiv.org/abs/2311.03622) |
| ICRA | 2025 | [LUMOS: Language-Conditioned Imitation Learning with World Models](https://ora.ox.ac.uk/objects/uuid%3A121d6c46-74e3-48b4-9130-048a4e0a599d)：言語条件の技能学習を世界モデル内で行い実機へ移行。 | 大学の機関リポジトリでICRA 2025掲載を確認。受賞は未確認。 |
| ICRA | 2026 | [WorldPlanner: Monte Carlo Tree Search and MPC with Action-Conditioned Visual World Models](https://ieeexplore.ieee.org/abstract/document/11697238)：世界モデルとaction samplerを用いたMCTS／MPC。 | IEEEの掲載情報で本会議を確認。原著者は実機3タスクの検証を報告。受賞は未確認。 |
| CVPR | 2024 | [Generalized Predictive Model for Autonomous Driving（GenAD）](https://openaccess.thecvf.com/content/CVPR2024/papers/Yang_Generalized_Predictive_Model_for_Autonomous_Driving_CVPR_2024_paper.pdf)：運転動画の一般化予測。 | CVFの本会議論文情報を確認。受賞は未確認。リンクは既存公開PDFの出典表示のみで、ダウンロードしていない。 |
| CVPR | 2025 | [Navigation World Models](https://openaccess.thecvf.com/content/CVPR2025/html/Bar_Navigation_World_Models_CVPR_2025_paper.html)：行動条件付き未来動画によるnavigation planning。[GEM](https://openaccess.thecvf.com/content/CVPR2025/html/Hassan_GEM_A_Generalizable_Ego-Vision_Multimodal_World_Model_for_Fine-Grained_Ego-Motion_CVPR_2025_paper.html)、[MaskGWM](https://openaccess.thecvf.com/content/CVPR2025/html/Ni_MaskGWM_A_Generalizable_Driving_World_Model_with_Video_Mask_Reconstruction_CVPR_2025_paper.html)も本会議。 | Navigation World ModelsはBest Paper **Honorable Mention**。Best Paper本賞と混同しない。[公式受賞発表](https://cvpr.thecvf.com/Conferences/2025/News/Awards_Press) |
| CVPR | 2026 | [GeoWorld: Geometric World Models](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_GeoWorld_Geometric_World_Models_CVPR_2026_paper.html)：双曲潜在空間の予測・計画。[Physical Object Understanding with a Physically Controllable World Model](https://openaccess.thecvf.com/content/CVPR2026/html/Venkatesh_Physical_Object_Understanding_with_a_Physically_Controllable_World_Model_CVPR_2026_paper.html)：物理的操作が可能なモデルと物体理解。 | CVF本会議採択を確認。これらの受賞は未確認。[公式受賞発表](https://cvpr.thecvf.com/Conferences/2026/News/Best_Papers)とは分けて照合。 |
| NeurIPS | 2024 | [Diffusion Forcing: Next-token Prediction Meets Full-Sequence Diffusion](https://proceedings.neurips.cc/paper_files/paper/2024/hash/2aee1c4159e48407d68fe16ae8e6e49e-Abstract-Conference.html)：トークンごとの独立noise levelで予測と系列生成を統合。世界モデル生成・計画の基盤手法として採録。 | 公式proceedingsのMain Conference Track。受賞は未確認。 |
| NeurIPS | 2025 | [Video World Models with Long-term Spatial Memory](https://proceedings.neurips.cc/paper_files/paper/2025/hash/467655d26fcc207bca08915dc91964c6-Abstract-Conference.html)：3Dに根ざした記憶で再訪時の一貫性を扱う。 | 公式proceedingsのMain Conference Track。受賞は未確認。[公式Best Paper一覧](https://blog.neurips.cc/2025/11/26/announcing-the-neurips-2025-best-paper-awards/)を世界モデル論文の受賞根拠へ転用しない。 |
| NeurIPS | 2026 | DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning、DRILL: Training World Models to Improve Policies, Not Predict Pixelsが[公式Downloads一覧](https://neurips.cc/Downloads/2026)に掲載。 | 公式掲載まで確認。個別decision／proceedings／受賞は未確認。会議本体は12月で基準日より後。[公式日程](https://neurips.cc/Conferences/2026/Dates) |
| ICML | 2024 | [Genie: Generative Interactive Environments](https://proceedings.mlr.press/v235/bruce24a.html)：ラベルなし動画から潜在行動付き対話環境を生成。 | PMLR本会議採択。受賞は未確認。 |
| ICML | 2025 | [DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning](https://proceedings.mlr.press/v267/zhou25t.html)：DINOv2特徴の未来予測と行動列最適化。 | PMLR本会議採択。古いICLR投稿版の表記を最終会議としない。UWMのICML関連受賞はワークショップ。[UWM](https://weirdlabuw.github.io/uwm/) |
| ICML | 2026 | [DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos](https://proceedings.mlr.press/v306/gao26q.html)：人間動画からlatent actionを介してロボット世界モデルを学習。 | PMLR本会議採択。公式DownloadsではReal-Timeを含む題名もあるため、書誌タイトルはPMLRを採用。[公式一覧](https://icml.cc/Downloads/2026)。受賞は未確認。 |

## 受賞論文：確認できたものと関連範囲

| 論文 | 正確な賞・根拠 | 世界モデルとの関係 |
|---|---|---|
| Navigation World Models | CVPR 2025 Best Paper Honorable Mention。[学会公式発表](https://cvpr.thecvf.com/Conferences/2025/News/Awards_Press) | 世界モデルが中心の論文。[原論文](https://openaccess.thecvf.com/content/CVPR2025/html/Bar_Navigation_World_Models_CVPR_2025_paper.html) |
| Unified World Models | ICML 2025 Workshop on Building Physically Plausible World Models、Best Paper Award。著者プロジェクトページの申告を確認。主催者による別の受賞一覧との二重照合は未確認。[著者ページ](https://weirdlabuw.github.io/uwm/) | RSS 2025本会議論文でもあるが、RSS／ICML本会議のBest Paperという意味ではない。[RSS論文](https://www.roboticsproceedings.org/rss21/p015.html) |
| One Model to Drift Them All: Physics-Informed Conditional Diffusion Model for Driving at the Limits | CoRL 2024 Outstanding Paper Award。[学会公式一覧](https://2024.corl.org/program/awards) | 物理モデルのパラメータ分布とMPCを用いる実車制御の隣接研究。動画生成型世界モデルと同一分類にしない。Toyota Supra／Lexus LC 500での実験を報告。[原論文](https://proceedings.mlr.press/v270/djeumou25a.html) |
| NeuralActuator: Neural Actuation Modeling for Robot Dynamics and External Force Perception | RSS 2026 Outstanding Systems Paper in Memory of Seth Teller Award。[学会公式一覧](https://roboticsconference.org/2026/program/awards/) | dynamics modelingの隣接研究として読む候補。汎用世界モデルの受賞と呼び替えない。 |

ICML 2026の公式受賞一覧は確認したが、本メモのDreamDojoを受賞論文とする根拠は確認できない。「採択」「spotlight」「award」を同義にしない。[公式受賞発表](https://blog.icml.cc/2026/07/05/announcing-the-icml-2026-awards/)

## 指定学会以外でも実務上参照する論文

| 論文 | 位置づけ・出典 |
|---|---|
| DreamerV3 | 最終雑誌論文はNature 2025「Mastering diverse control tasks through world models」。上記6学会への採択と書き換えない。[Nature](https://doi.org/10.1038/s41586-025-08744-2) |
| TD-MPC2 | ICLR 2024。上記6学会には含まれないが実装比較の重要候補。[著者実装・書誌](https://github.com/nicklashansen/tdmpc2)、[arXiv](https://arxiv.org/abs/2310.16828) |
| Dreamer 4 | 2025年公開プレプリントを確認。会議採択は本調査では未確認。[arXiv](https://arxiv.org/abs/2509.24527) |
| V-JEPA 2 | Metaの研究公開・arXiv論文を確認。会議採択は未確認。[Meta](https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/)、[arXiv](https://arxiv.org/abs/2506.09985) |
| Cosmos 3 | 2026年技術報告。会議採択は未確認。[arXiv](https://arxiv.org/abs/2606.02800) |
| DreamZero | 「World Action Models are Zero-shot Policies」、2026年プレプリント。会議採択は未確認。[arXiv](https://arxiv.org/abs/2602.15922) |
| WorldScore | ICCV 2025本会議。CVPR 2025ではない。[CVF](https://openaccess.thecvf.com/content/ICCV2025/html/Duan_WorldScore_A_Unified_Evaluation_Benchmark_for_World_Generation_ICCV_2025_paper.html) |
| VP² | 「A Control-Centric Benchmark for Video Prediction」、ICLR 2023。対象期間外の評価基盤。[著者ページ](https://s-tian.github.io/projects/vp2/) |
| 日本語研究 | JSAI 2025の[階層世界モデルと実機制御](https://www.jstage.jst.go.jp/article/pjsai/JSAI2025/0/JSAI2025_1B3OS41a01/_article/-char/ja)、JSAI 2026の[マルチモーダル階層世界モデル](https://www.jstage.jst.go.jp/article/pjsai/JSAI2026/0/JSAI2026_1E3OS39a02/_article/-char/ja)。国際6学会の採択とは分けて記録。 |

## 後続の収集処理に渡す際の注意

`candidates.tsv`は指定の9列を持つタブ区切り。`未確認`は空欄の代わりの明示値であり、ダウンロード対象URLではない。`verify_url`を最初に確認し、会議年と刊行年、会議版とarXiv版の題名差、重みとコードのライセンスを保持する。本調査ではPDF、README.md、_catalog.csv、docs/を変更していない。
