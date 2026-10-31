# Franka 未確認事項の追補

調査基準日：2026-10-31。既存の `franka(fr3)/notes/practical.md` と `franka_ROS2/notes/practical.md` を読み、残っていた購入条件・Arm v2.2・AI Companion に限定して追加調査した。Web の現行ページには後から更新されるものがあり、日付のない記述を基準日の確定履歴とは扱わない。

調査方法：公式 HTML、公式 GitHub の issue、既存 PDF のテキストを照合。PDF のダウンロード、arXiv API、OpenAlex API、deep research、実機試験は実施していない。新規論文候補は追加せず、TSV は作成・変更していない。書き込み先は本ファイルのみ。

## 1. 今回埋まった点と、残る点

| 論点 | 追加確認の結果 |
|---|---|
| AI Companion の製品状態 | **公式資料一覧で End of Life と明記。** 製品紹介ページには見積フォームが残っているが、新規供給・在庫・保守終了日を保証するものとは判断できない。[資料一覧][documents]・[製品ページ][companion] |
| 現行 OS | マニュアルは Ubuntu 20.04、現行 MATLAB Toolbox の対応表は AI Companion／Jetson Orin 向けに Ubuntu 22.04。**現行のメーカー配布 Base OS の版は未確認**で、両者を同じ意味の記述として統合できない。[マニュアル][companion-manual]・[Toolbox 対応表][matlab-os] |
| ROS 2／franka_ros2 の実績 | 公式 issue に AI Companion を示唆するホスト名の起動ログがあり、ROS 2 Humble 利用者が更新後の動作を報告。**利用者報告という限定付きで実績あり**。ホスト名以外のハードウェア証明と、現行 Jazzy の実績は未確認。[issue #145][issue145] |
| FCI の利用期間 | 一般 GTC に契約目的に限定された非独占・永続利用権の記載あり。ただし **FCI 個別契約の期間・更新料金を確定する証拠ではない**。[公式 GTC 掲載元][documents] |
| ライセンスの移行 | 現行操作マニュアルに、故障 Control から新 Control へ feature／app のライセンスを移す手順あり。**中古売買による名義変更の許諾とは別**。[操作マニュアル掲載元][documents] |
| Arm v2.2 の内部差分 | 今回も **未確認**。共通マニュアル掲載や専用モデル ID の不在だけで、v2.1 との内部同一性・代替性は確定できない。[資料一覧][documents]・[公式モデル][description] |

## 2. Arm v2.2：公開資料でどこまで分かるか

既存メモの「v2.1 と v2.2 は共通資料」という確認から一歩進めるため、手元の `Hardware Manual Franka Research 3_Arm v2.1_R02210_1.3_EN.pdf` の表紙情報と変更履歴も読んだ。p.2 の対象表記は **Arm v2.1**、変更履歴は v2.1 の重量・ラベル・停止仕様変更、その後の安全記述・参照・LED 表示の文書改訂を記載するが、v2.2 固有の改訂理由は記載していない。この取得済み版だけでは v2.2 の部品変更を埋められない。現行ポータルの共通掲載と、取得済みファイル本文の対象表記は分けて記録する。[公式資料一覧][documents]

公式 `franka_description` の生成コマンドの accepted values と Arm 対応表には `fr3v2_1` があり、`fr3v2_2` は列挙されていない。**これは v2.2 が v2.1 の URDF・慣性値をそのまま使えるとの保証ではない**。内部部品、トルクセンサー、配線、減速機、校正、運動学・慣性パラメータの各差分と、v2.2 に使う正式なモデル指定は未確認のままとする。[公式 README のモデル一覧・判別表][description]

追加で注意したい点は、公式互換表の HTML 抽出では色による互換性区分が落ち、Arm の数値リビジョンと商品名の対応も自明ではないことである。抽出テキストの空欄を「非互換」や「同一仕様」と読み替えず、Arm／Control の銘板と System Image を指定して確認する必要がある。これは調査者の判断であり、v2.2 の新しい制限を発見したという意味ではない。[公式互換表と凡例][compat]

## 3. FCI：一般条件と個別条件を分けた追加確認

以下は既存 `New_GTC_EN_FrankaRobotics_040226.pdf`（February 2026、§10、pp.6–7）と `Operating Manual Franka Research 3_5.10_R02216_1.3_EN.pdf` を読み取った結果。契約への適用は見積・注文確認書・個別ライセンス条件との照合が必要である。[公式掲載元][documents]

| 項目 | 新たに確認できた文書記載 | 未確認・適用上の限界 |
|---|---|---|
| 永続性 | GTC §10 は、供給ソフトウェアについて契約目的に限定した非独占・永続利用権と、合意した料金による対価を規定。バックアップコピーにも言及する。[GTC 掲載元][documents] | FCI を名指しした料金・期間条項、更新版の取得権、保守料金、個別条件の優先関係は未確認。「FCI は無料・永久更新」とは言えない。 |
| 譲渡・第三者提供 | 同じ §10 は、強行法や該当 OSS ライセンスで認められる場合を除き、ソフトウェアの第三者への譲渡・販売・貸与・ライセンス等を制限する。[GTC 掲載元][documents] | 中古機の譲渡時や関連会社での共用が自動的に認められるとは確認できない。 |
| 商用利用 | GTC には契約目的での利用と、第三者へのソフトウェア提供・商業的利用等に関する制限がある。[GTC 掲載元][documents] | **企業内 R&D、販売製品の試験、生産稼働の各用途に FCI を使えるかは未確認**。一般条項から全面許可／全面禁止を導かず、用途を明記した個別回答を要する。 |
| 初期インストール | 操作マニュアル §10.3 は、FCI feature は通常、初期設定時に自動インストールされ、未導入なら Franka World から導入できると記載。[操作マニュアル掲載元][documents] | 自動インストールの記述は、全販売構成における無償同梱・価格内包の証明ではない。FCI 文書は別途ライセンスを前提にする。[FCI 導入条件][fci-start] |
| 故障 Control の交換 | 操作マニュアル §14.4.1：旧 Control が起動・同期できれば Franka World で feature／app を解除し、新 Control を既存アカウントにリンクして同期する。起動・同期不能なら Support にライセンス解放を依頼する。[操作マニュアル掲載元][documents] | これは故障交換の手順。別組織への名義移管、Duo の複数 Control での共有、移管料金は未確認。 |
| 手動更新と移行の違い | 同 §14.4.1 は、Standard UI から更新や安全設定を手動インポートしても feature／app／license は移らないと明記する。[操作マニュアル掲載元][documents] | バックアップ復元だけで権利も復元されるという想定は避ける。 |

## 4. AI Companion の OS：確定できる版と確定できない版

| 情報の範囲 | 確認できた内容 | 読み方 |
|---|---|---|
| 製品マニュアル | 手元の R82010、版1.1（May 2025）の §6「Technical Specifications」p.25 は **Ubuntu Linux 20.04**。§5.7.2 は NVIDIA L4T、PREEMPT 実時間カーネル、Base OS の CUDA／ドライバー管理と、利用者に Base OS の管理者権限がないことを記載。[公式 PDF URL][companion-manual] | マニュアル記載値として確認済み。最新納入個体／最新更新ファイルがこの版という保証は未確認。本文フッターには1.0の表記も残るため、表紙版と本文位置を併記した。 |
| 現行 Toolbox 対応表 | Franka Toolbox **4.0.0** の AI Companion／Jetson Orin Platform 欄は **Ubuntu 22.04 LTS**。[公式対応表][matlab-os] | Toolbox の対象環境であり、AI Companion の Base OS が全機一斉に22.04へ更新されたことを示すリリースノートではない。 |
| 開発環境の構造 | マニュアルは Base OS／Application／User の層と Docker を説明。§8.1 は Franka が提供する更新ファイルを WebUI にアップロードする方式を説明する。[公式 PDF URL][companion-manual] | ROS コンテナ内の OS とホスト OS は個別に確認する。コンテナのディストリビューションだけからホストの L4T／JetPack／カーネルを推定しない。 |
| 現行配布イメージ | **未確認**：配布イメージ名・公開日・checksum、L4T／JetPack／CUDA の正確な版、カーネル版、22.04への公式更新手順、更新提供期限。[製品マニュアル][companion-manual]・[EOL 表記][documents] | 「現行 OS は22.04」と単一の断定に置き換えられない。 |

調達・保守時には、メーカーから現行イメージの版情報を取得し、対象個体のホスト `/etc/os-release`、`/etc/nv_tegra_release`、`uname -a` と、ROS コンテナ内の OS／ROS ディストリビューションを別々に残すことを推奨する。これは上記の資料差と Docker 構成に基づく調査者の提案であり、本調査では実行していない。[構成と更新方式][companion-manual]・[Toolbox 対象 OS][matlab-os]

## 5. AI Companion 上の ROS 2／franka_ros2：動作報告の具体性

公式 `franka_ros2` issue **#145** は2025-06-17に投稿され、投稿者は **ROS 2 Humble、libfranka 0.15.0、Robot Control 5.8.0、franka_ros2 v1.0.0** と記載する。ログのホスト名は `franka-ai-companion` を含み、実ロボット IP への接続成功を出力する一方、当初は起動エラーが発生している。2025-06-27には投稿者が新しいリリースを使って動いたと報告し、2025-08-01に completed として閉じられた。[投稿・ログ・改善報告][issue145]

この証拠は **AI Companion とみられる環境からの Humble／franka_ros2 利用と、更新後の改善を示す利用者の一次報告**として採用する。ただし、最終的に動いたパッケージのタグ／commit、ホスト OS、コンテナイメージ、JetPack、長時間の制御周期達成率、推論同時実行負荷は未確認。ホスト名だけで Orin NX 製品の型番・構成を独立検証したわけでもない。MoveIt 2＋Cartesian impedance の完成報告や、現行 Jazzy の AI Companion 上での検証済み構成とも扱わない。[issue の確認範囲][issue145]

名前の取り違えにも注意する。手元の Mobile FR3 Duo／TMR マニュアル §5.10 は、DNS 名 `companion` の User PC に **Jetson AGX Orin Developer Kit 64GB、Ubuntu 22.04、ROS 2 Humble、franka_ros2 humble branch** を記載する。これは Orin NX 16GB の「Franka AI Companion」製品そのものを示す証拠ではない。[Mobile FR3 Duo マニュアル][mobile-manual]・[AI Companion 製品仕様][companion]

## 6. Orin NX の推論性能：参考値と製品実測を分ける

**AI Companion 実機上での VLA／LLM の推論遅延、action chunk 生成時間、制御成功率、画像処理と FCI の同時負荷を測った公開結果は、今回確認できなかった。** メーカーの2024年発表には Isaac Manipulator／6D pose estimation・tracking のデモ説明があるが、FPS・レイテンシー・VLA モデル名を伴う製品ベンチマークではない。[メーカー発表][launch]

比較に使える一次資料として、NVIDIA の **MLPerf Inference v3.1 提出値**には Orin NX 16GB の結果がある。下表は **NVIDIA 自身の提出・掲載値**で、Franka AI Companion の実測ではない。対象ソフトウェアは JetPack 5.1.1、TensorRT 8.5.2、CUDA 11.4。[NVIDIA の条件・表・再現コード案内][nvbench]

| モデル | Orin NX の Offline throughput（samples/s） |
|---|---:|
| ResNet | 2640.51 |
| RetinaNet | 66.5 |
| BERT | 194.5 |

出典はすべて同じ [NVIDIA MLPerf v3.1 表][nvbench]。これらは Offline スループットであり、単一カメラ入力の end-to-end FPS、単発推論レイテンシー、VLA の制御 Hz に変換しない。AI Companion の電力モード・冷却・ソフトウェアとの一致も未確認である。[ベンチマーク条件][nvbench]・[AI Companion マニュアル][companion-manual]

調査者の受入試験案：対象モデルと精度・量子化方式、画像解像度／枚数、batch、action chunk 長、電力モード、CUDA／TensorRT／PyTorch を固定し、カメラ取得から指令到達までの遅延分布と、推論中の FCI 通信品質を同時記録する。これは未公開部分を埋める提案で、今回の測定結果ではない。[比較条件の根拠][nvbench]・[FCI 通信要件と診断][trouble]

## 7. 価格・国内入手経路の追加確認

| 対象 | 新たに確認できた購入情報 | 残る未確認事項 |
|---|---|---|
| FR3 の国内価格・納期 | 販売元名義のイプロス掲載では、現行の企業名は **リョーサン菱洋株式会社**、価格帯・納期とも「詳細はお問い合わせください」。日本向け公開定価は、この掲載では確認できない。[販売元掲載][jp-sales] | 税・送料・設置・FCI・工具・PC・保守を含む総額、在庫、納期は未確認。 |
| 国内技術窓口 | 販売店自身が FR3＋Jetson AGX Orin の障害物回避デモと、Ubuntu 22.04／JetPack 6.2／ROS 2 Humble の構成を公開し、ロボット相談フォームへ誘導する。[国内構築記事][jp-demo]・[問い合わせフォーム][jp-contact] | 販売店自身の実績説明。AI Companion NX の在庫・保守や、franka_ros2 の特定版の検証を保証する資料ではない。 |
| AI Companion の価格・供給 | メーカー製品ページは定価を示さず見積方式。別の公式資料一覧は EOL と表示する。[製品ページ][companion]・[資料一覧][documents] | 国内在庫、残品販売、代替品、修理受付終了日、OS 更新期限、買切価格は未確認。見積フォームの存在だけで新規購入可能とは断定できない。 |
| FCI 費用 | 一般 GTC は合意料金によるソフトウェア利用権を記載するが、FCI の個別金額を列挙しない。[GTC 掲載元][documents] | FCI 単価、本体への内包、更新・移管・再発行費用は未確認。 |

依頼するなら、国内の [ロボット相談フォーム][jp-contact] から、次の内容を一括で書面確認するのが実務的である。これは調査者の照会案であり、問い合わせ送信はしていない。

1. Arm v2.2 と v2.1 の変更通知、正式な URDF／慣性モデル指定、納入 Control／Image の組合せ。[公開情報の不足箇所][description]・[互換表][compat]
2. FCI の用途（企業内研究／製品試験／生産運用）、利用期間、台数・Control への紐付け、他組織への移管と故障時の再発行費。[条件・手順の掲載元][documents]
3. AI Companion の EOL 日・販売可否・保守期限・最終 OS イメージ。代替 Jetson を提案する場合は、NX と AGX を区別した型番と、推論を同時実行した FCI 検証結果。[EOL 表記][documents]・[国内 AGX 構成例][jp-demo]
4. 本体、FCI、工具、計算機、架台、設置・教育、輸送、保守、税を分けた円建て見積と納期。[国内価格案内][jp-sales]

## 8. 証拠と検証の限界

本追補が追加できたのは、EOL の公式表示、OS 記載の不一致、Humble の具体的な利用者報告、一般 GTC の永続性・第三者提供条件、故障時ライセンス移行、国内販売元の価格問い合わせ方式である。**v2.2 内部差分、FCI 個別用途・料金、最新 AI Companion Base OS、同製品上の VLA 推論性能は未確認**。資料の記載確認を、実機検証や契約上の利用許諾取得とは表現しない。[資料一覧][documents]・[Toolbox OS 表][matlab-os]・[利用者報告][issue145]・[国内販売案内][jp-sales]

既存 PDF は以下を読み取りのみ使用した。URL は公式掲載元または確認済みの公式リンク先であり、Web 版とのハッシュ一致は未検証。

| 既存ファイル（`franka(fr3)/docs/official_pdf/` 以下） | 使用箇所 | 出典 URL |
|---|---|---|
| `Product Manual AI Companion_R82010_1.1_EN.pdf` | 表紙版、§5.7–5.8、§6、§8.1 | [公式マニュアル][companion-manual] |
| `New_GTC_EN_FrankaRobotics_040226.pdf` | February 2026、§10、pp.6–7 | [公式 GTC 掲載元][documents] |
| `Operating Manual Franka Research 3_5.10_R02216_1.3_EN.pdf` | §10.3、§14.4.1 | [公式操作マニュアル掲載元][documents] |
| `Hardware Manual Franka Research 3_Arm v2.1_R02210_1.3_EN.pdf` | p.2 対象ハードウェアと変更履歴 | [公式ハードウェア資料掲載元][documents] |
| `Prototype Manual and Datasheets _Mobile FR3 Duo_R04245_EN.pdf` | §5.10、User PC と humble branch | [公式マニュアル][mobile-manual] |

[documents]: https://franka.de/documents
[companion]: https://franka.de/franka-ai-companion
[companion-manual]: https://franka.de/hubfs/Product%20Manual%20AI%20Companion_R82010_1.1_EN.pdf?hsLang=en
[matlab-os]: https://frankarobotics.github.io/docs/doc/franka_toolbox_for_matlab/docs/franka_matlab/system_requirements.html
[issue145]: https://github.com/frankarobotics/franka_ros2/issues/145
[description]: https://github.com/frankarobotics/franka_description#troubleshooting
[compat]: https://franka.de/fr3-compatibility-matrix
[fci-start]: https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html
[mobile-manual]: https://franka.de/hubfs/Prototype%20Manual%20and%20Datasheets%20_Mobile%20FR3%20Duo_R04245_EN.pdf?hsLang=en
[launch]: https://franka.de/news/franka-robotics-launches-franka-ai-companion
[nvbench]: https://developer.nvidia.com/embedded/jetson-benchmarks
[trouble]: https://frankarobotics.github.io/docs/troubleshooting.html
[jp-sales]: https://mono.ipros.com/product/detail/2000878517/
[jp-demo]: https://techlabo.rers-grp.com/article/25070200_1244.html
[jp-contact]: https://page.ryosan.co.jp/contact/general01
