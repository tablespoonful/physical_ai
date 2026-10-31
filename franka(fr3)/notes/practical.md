# Franka Research 3（FR3）実務調査

調査基準日：2026-10-31。対象は購入・モデル選定・制御環境構築・データ収集。以下の「推奨」は出典に基づく調査者の判断であり、実機評価結果ではない。Web の main／latest は可変で、日付のない変更履歴について基準日時点のリリース日を遡及確定したものではない。PDF の新規取得、実機接続、ソフトウェアのインストール・動作試験は実施していない。

## 1. 最初に押さえること

- **Panda＝旧 Franka Emika Robot（FER）と、FR3 は別製品として扱う。** FCI 文書は両者を明確に分け、libfranka の互換範囲も異なる。Panda 用 wheel／URDF を、FR3 用だと名前だけで判断しない。[公式 FCI](https://frankarobotics.github.io/docs/)・[公式互換表](https://franka.de/fr3-compatibility-matrix)
- **Arm 世代、Control 世代、System Image、FCI サーバープロトコル、libfranka、Python パッケージを別々に記録する。** ハードウェアは銘板、System Image は Desk の Settings → Dashboard で確認する。互換性と安全認証・性能確認は公式表でも別区分である。[確認方法と区分](https://franka.de/fr3-compatibility-matrix)
- **現在は公式 FR3 パラメータが公開されている。** Panda の古い同定論文の「メーカー非公開」という記述を、そのまま現在の FR3 に適用しない。FR3 各世代の質量・重心・慣性は公式 YAML にある。[fr3](https://github.com/frankarobotics/franka_description/blob/main/robots/fr3/inertials.yaml)・[fr3v2](https://github.com/frankarobotics/franka_description/blob/main/robots/fr3v2/inertials.yaml)・[fr3v2_1](https://github.com/frankarobotics/franka_description/blob/main/robots/fr3v2_1/inertials.yaml)
- **FCI のライセンスとクライアントの OSS ライセンスを分ける。** libfranka が Apache-2.0 でも、実機には FCI ライセンス・Feature の導入・FCI モード有効化が必要。[libfranka ライセンス](https://frankarobotics.github.io/libfranka/0.15.0/)・[FCI 導入条件](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html#installing-the-fci-feature)

## 2. Panda と FR3、Arm 世代の違い

### 2.1 制御ソフトから見た違い

| 観点 | Panda／FER | FR3 | 実務上の意味・出典 |
|---|---|---|---|
| ライブラリ世代 | System ≥4.2.1 の行は libfranka ≥0.9.1, <0.10.0 | System ≥5.2.0 以降は 0.10 系以降を、Image の範囲別に選ぶ | 「最新を入れる」より先にサーバー版を照合。[公式表](https://franka.de/fr3-compatibility-matrix) |
| 関節・軌道の制限 | FER 専用表 | FR3 専用表。位置・運動方向で変わる速度上限もある | Panda の固定定数を移植しない。`getUpperJointVelocityLimits`／`getLowerJointVelocityLimits` を参照。[制御仕様](https://frankarobotics.github.io/docs/robot_specifications.html) |
| モデル | `fer`、既存 Panda 記述 | `fr3`／`fr3v2`／`fr3v2_1` | 世代選択を省略しない。[公式 description](https://github.com/frankarobotics/franka_description) |
| 製品の位置付け | 公式資料ポータルでは End of Life | FR3 の世代別マニュアル・データシートを掲載 | 中古 Panda の導入判断では保守と更新範囲を別途照会。[公式資料一覧](https://franka.de/documents) |

FCI 文書の FR3 並進速度上限は 3.0 m/s、FER は 1.7 m/s だが、手元の FR3 データシート R02212/2.6（July 2026）p.2 は TCP 最大 2 m/s と記載する。**FCI 軌道制約表と製品の動作仕様を同一の速度保証と解釈しない。** 設計では Image・安全設定・用途に適用される上限をメーカーへ確認する。いずれもメーカー公表値で、今回の実測値ではない。[FCI 制御仕様](https://frankarobotics.github.io/docs/robot_specifications.html)・[データシート掲載元](https://franka.de/documents)

### 2.2 Arm v1／v2.0／v2.1／v2.2

| Arm 世代 | 確認できた差・モデル | 未確認／注意点 | 出典 |
|---|---|---|---|
| v1 | 公式モデル `fr3`。Desk 表示対応は `Arm3R`。手元の v1 Hardware Manual R02210/1.3 には重量約17.8 kg の記述がある | v1 内の全ハードウェア改訂差は未確認。旧 Product Manual はハード・操作説明の一体形式 | [description README](https://github.com/frankarobotics/franka_description)・[公式資料一覧](https://franka.de/documents) |
| v2.0 | `fr3v2`／`Arm3Rv2`。独立した inertials と kinematics を持つ。手元の v2.0 Hardware Manual R02210/1.3 は約17.8 kg と記載 | 「v2 は v1 の外装だけ変更」とは判断できない。GELLO Duo の説明も v2.0 以降と従来世代の運動学差に言及 | [公式モデル](https://github.com/frankarobotics/franka_description/tree/main/robots/fr3v2)・[資料一覧：R02210／R62040](https://franka.de/documents) |
| v2.1 | `fr3v2_1`／`Arm3Rv2.1`。手元の Hardware Manual R02210/1.3 p.2 は重量更新・ラベル改訂・停止時間／停止距離仕様の改訂を変更内容として記載。R02212/2.6 は約18.3 kg | リンク重心・一部質量にも v2.0 と異なる値がある。停止特性を旧版の表で評価しない | [公式 inertials](https://github.com/frankarobotics/franka_description/blob/main/robots/fr3v2_1/inertials.yaml)・[R02210／R02212 掲載元](https://franka.de/documents) |
| v2.2 | 公式ポータルは v2.1／v2.2 を共通のマニュアル・データシート項目にまとめている。手元の R02212/2.6 p.2 も両者を併記し約18.3 kg と記載 | **内部部品・センサー・配線・性能上の v2.1 との差は未確認。** 調べた description README に `fr3v2_2` は列挙されていない。v2.1 モデルで完全に代替できるという保証も未確認 | [公式資料一覧](https://franka.de/documents)・[公式 description](https://github.com/frankarobotics/franka_description) |

`Arm v2.2`、データシートの**文書版 2.2.2**、Control の版、System Image 5.x は別の識別子である。手元の `Datasheet ... R02212_2.2.2_EN_June 2026.pdf` は本文では Arm v2.0 用である。ファイル名の数字だけでハードウェアを選定しない。また、description README は古い Image（5.9.1 未満）では Desk の Arm 表示が正しくない場合があるとする。[資料一覧](https://franka.de/documents)・[description の Arm 判別表](https://github.com/frankarobotics/franka_description#troubleshooting)

**調査者の推奨：** 見積書・実機銘板・Desk・使用モデル ID を一組で残す。v2.2 のモデル指定は販売店から書面で確認する。根拠は世代別モデルの存在と、公式がハードウェア／Image の互換性を別々に管理していることである。[モデル一覧](https://github.com/frankarobotics/franka_description)・[互換性管理](https://franka.de/fr3-compatibility-matrix)

## 3. 動力学パラメータと同定

### 3.1 公式に取れるもの

| 情報 | 所在・取得方法 | 解釈 |
|---|---|---|
| リンク質量・重心・慣性テンソル | `robots/<model>/inertials.yaml`。比較例：link1 の質量は `fr3` が2.9274653454 kg、`fr3v2` と `fr3v2_1` が2.437700 kg | 公式配布モデルの値。対象個体の測定値と同一という保証は未確認。[fr3](https://github.com/frankarobotics/franka_description/blob/main/robots/fr3/inertials.yaml)・[fr3v2](https://github.com/frankarobotics/franka_description/blob/main/robots/fr3v2/inertials.yaml)・[fr3v2_1](https://github.com/frankarobotics/franka_description/blob/main/robots/fr3v2_1/inertials.yaml) |
| 世代差の具体例 | link2 の重心 xyz は v2.0 で `(0.004541, -0.180691, -0.010479)` m、v2.1 で `(-0.010630, -0.184739, -0.010479)` m | 質量が同じでも重心位置が変わるため、ファイル一式を世代で揃える。[v2.0](https://github.com/frankarobotics/franka_description/blob/main/robots/fr3v2/inertials.yaml)・[v2.1](https://github.com/frankarobotics/franka_description/blob/main/robots/fr3v2_1/inertials.yaml) |
| 運動学・関節限界・形状 | 同じ `robots/<model>/` の記述と meshes。生成スクリプトで URDF 化 | 動力学だけ更新してフレームや形状を旧版のままにしない。[公式 description](https://github.com/frankarobotics/franka_description) |
| 実機側モデルの計算 API | `Robot::loadModel()`、`Model::mass`／`coriolis`／`gravity`、pose／Jacobian。現行 Model コンストラクターはロボット由来 URDF 文字列を受ける | 公開 YAML と実機供給モデルを同一物と仮定しない。設定した工具と実機状態も含めて照合する。[Model API](https://github.com/frankarobotics/libfranka/blob/main/include/franka/model.h) |
| モデル実装の変更 | libfranka 0.14.0 の変更履歴に Pinocchio による動力学計算への変更を記載 | 古い「実機からバイナリモデルライブラリを取得する」前提だけで現行実装を説明しない。[変更履歴](https://github.com/frankarobotics/libfranka/blob/main/CHANGELOG.md) |

粘性摩擦・静止摩擦・減速機弾性・モーター遅延を含む、**全 Arm 世代に対応する公式の完全同定データセット／誤差保証**は今回確認できなかった。上の公開 inertials だけから完全な実機再現性を主張しない。[公開データの確認先](https://github.com/frankarobotics/franka_description)・[公式モデル案内](https://franka.de/models-and-simulation)

### 3.2 第三者の同定・コード

| 資料 | 対象と確認内容 | コード・利用判断 |
|---|---|---|
| Gaz ほか, “Dynamic Identification of the Franka Emika Panda Robot With Retrieval of Feasible Parameters Using Penalty-Based Optimization” | **Panda**。IEEE RA-L 2019。OLS による基底パラメータ推定と物理整合制約付きのリンクパラメータ復元、摩擦モデル。FR3 の同定結果ではない。[出版社](https://doi.org/10.1109/LRA.2019.2931248) | [著者コード](https://github.com/marcocognetti/FrankaEmikaPandaDynModel)：MATLAB、データ、C++、V-REP、補足資料。GPL-3.0。FR3 へは手法を参考にし、数値は流用しない |
| HIRO-group `panda-dynamics-model` | **Panda** の動力学モデル実装。[リポジトリ](https://github.com/HIRO-group/panda-dynamics-model) | Python から利用する候補。独立した FR3 同定コードと誤認しない。FR3 対応・現行環境での動作は未確認 |
| “Application of a modified DREM algorithm for the identification of payload parameters for a Franka Emika cobot” | 出版社抄録は **FR3 のペイロード慣性のオンライン同定**と記載。IFAC-PapersOnLine 59(14), 2025。アーム全リンクの完全同定とは区別。[出版社](https://www.sciencedirect.com/science/article/pii/S2405896325028393) | 公開コードと arXiv ID は未確認。出版社の検索抽出を確認したが、本文ページの直接取得は403。性能の独立再検証なし |
| FrankaTwin | 開発者が FR3＋Franka Hand での同定を報告。Isaac Lab 上で armature、静的／動的／粘性摩擦、遅延を最適化。リンク慣性全体の復元ではない。[同定手順とパラメータ表](https://tsrobcvai.github.io/frankatwin/sysid.html) | [コード](https://github.com/tsrobcvai/frankatwin)。開発者自身が個体差・パラメータの非一意性を注意。掲載値は第三者開発者の自己申告でありメーカー公式値ではない |
| FrankaTwin に関連する “Visual Sim-to-Real Learning for Robotic Insertion under Geometric Variations: Application to Rebar Installation” | 2026年の arXiv 論文。FrankaTwin 文書が関連論文として引用。**同定専用論文として扱わない**。[arXiv で実在確認](https://arxiv.org/abs/2609.20477)・[開発者の引用案内](https://tsrobcvai.github.io/frankatwin/index.html) | FrankaTwin の公開実装と研究文脈を追う候補。査読採択先は未確認 |

**調査者の推奨：** まず実機の工具質量・重心・慣性と TCP を正しく設定し、公式モデルを基準にする。その後、対象動作で励起・同定し、学習に使わない別軌道で検証する。FrankaTwin は保持した別軌道による検証を説明しており、Polymetis の文書も工具の慣性設定不足を追従誤差の原因として挙げる。[同定・検証](https://tsrobcvai.github.io/frankatwin/sysid.html)・[工具設定](https://github.com/facebookresearch/fairo/blob/main/polymetis/docs/source/troubleshooting.md#end-effector-configuration)

## 4. シミュレーションモデルの所在と FR3 対応

「モデルファイルがある」「エンジンが読める」「実機と一致する」「FCI のネットワークを模擬する」は別の確認項目として扱う。以下はファイル／文書の確認であり、今回ロード試験は行っていない。

| 環境・資産 | 所在 | FR3 対応の確認結果 | 導入時の注意 |
|---|---|---|---|
| 公式 URDF／xacro | [franka_description](https://github.com/frankarobotics/franka_description) | **あり**。`fr3`、`fr3v2`、`fr3v2_1`、Duo／Mobile Duo を選択可能 | `./scripts/create_urdf.sh <robot_type>`。工具、自己衝突形状、prefix を明示。v2.2 専用 ID は未確認 |
| Gazebo／ROS 2 | [franka_ros2](https://github.com/frankarobotics/franka_ros2)・[公式モデル案内](https://franka.de/models-and-simulation) | **あり**。公式が FR3 と Duo 等のドキュメントへ誘導 | Gazebo 起動と実機 FCI 接続を区別。使用する branch、ROS、Image を揃える |
| MuJoCo Menagerie：FR3 v1 | [franka_fr3 README](https://github.com/google-deepmind/mujoco_menagerie/blob/main/franka_fr3/README.md) | **あり**。公式 description の `fr3` から派生。MuJoCo ≥3.1.3、Apache-2.0 | 簡略 MJCF で、position actuator を追加している。FCI トルク入力そのものと同じ制御契約ではない |
| MuJoCo Menagerie：FR3 v2 | [franka_fr3_v2 README](https://github.com/google-deepmind/mujoco_menagerie/blob/main/franka_fr3_v2/README.md) | **あり**。README は公式 description 1.0.1 由来と記載。公式も `franka_fr3_v2` を案内 | README の生成コマンドには `fr3` とあるため、README の記述だけで対象世代・最新版への追従を保証しない。XML のフレーム／inertial を照合する。[公式案内](https://franka.de/models-and-simulation) |
| Menagerie：Panda | [franka_emika_panda](https://github.com/google-deepmind/mujoco_menagerie/tree/main/franka_emika_panda) | **Panda 用**。FR3 とは別ディレクトリ | 見た目が似ていても置換扱いしない。[モデル一覧](https://github.com/google-deepmind/mujoco_menagerie) |
| Isaac Lab 標準 Franka 設定 | [robots/franka.py](https://github.com/isaac-sim/IsaacLab/blob/main/source/isaaclab_assets/isaaclab_assets/robots/franka.py) | 確認した標準設定は `FRANKA_PANDA_CFG` と Panda 資産。**このファイルだけでは FR3 専用標準設定を確認できない** | `Franka` の名前を FR3 保証と解釈しない。Isaac Lab 全体に FR3 が存在しないとの断定ではない |
| Franka 公式 Isaac Sim USD | [franka_simulation](https://github.com/frankarobotics/franka_simulation)・[Releases](https://github.com/frankarobotics/franka_simulation/releases) | **FR3 v2.1、Duo、Mobile Duo の資産あり** | README は Isaac Sim `6.0.0-rc.59` 対応と記載。Isaac Lab の ArticulationCfg・actuator・sensor への接続と動作検証は別途必要。安定性試験済みという記述はメーカー自己申告 |
| Isaac Lab の第三者同定環境 | [FrankaTwin 導入](https://tsrobcvai.github.io/frankatwin/installation.html) | FR3 実機に対応する同定／replay ワークフローを開発者が提供 | 文書の試験環境は Isaac Lab 2.3.0。`franka_mimic.usd` 等を導入する方式であり、公式 FR3 世代別 USD と同一とは未確認 |
| Genesis 標準例 | [Control your robot](https://genesis-world.readthedocs.io/en/latest/user_guide/getting_started/control_your_robot.html) | 例は `xml/franka_emika_panda/panda.xml`。**標準例は Panda** | FR3 の MJCF／URDF 読み込み可否と、アクチュエータ／摩擦／接触の同等性は別途検証 |
| Genesis／MuJoCo＋FCI 模擬 | [BarisYazici/libfranka-sim](https://github.com/BarisYazici/libfranka-sim) | README はデフォルトで hand なし FR3 URDF、server protocol 10 を提供。Genesis は任意バックエンド | **第三者の自己申告対応**。旧 protocol 9 以下非対応と記載。「全 wrapper に無条件対応」ではない。物理バックエンドのモデルとクライアント供給 URDF の一致も確認対象 |
| 別の FCI 模擬実装 | [TimSchneider42/franky-sim](https://github.com/TimSchneider42/franky-sim) | FR3 向け server、MuJoCo／Genesis 対応を開発者が説明 | 上の `franka-sim` と別リポジトリ・別パッケージ。API 模擬と実機同等精度を区別する。精度は今回未検証 |
| Drake の共有モデル | [RobotLocomotion/models/franka_description](https://github.com/RobotLocomotion/models/blob/master/franka_description/README.md) | README は **Panda モデル**と明記。一方、反映ローター慣性は FR3 由来、加速度制限は旧 Panda 由来と説明 | 「FR3 由来値を含む」ことは FR3 完全モデルの証拠ではない。link5 分割・独立指駆動等の変更もある |
| Drake 実機ドライバー | [drake-franka-driver](https://github.com/RobotLocomotion/drake-franka-driver) | FR3／firmware 5.x、libfranka 0.10.0 の利用記載あり | ドライバー対応とシミュレーションモデル対応は別。新しい Image の動作は未確認 |

**変換時の確認項目（調査者の推奨）：** 同一の関節角で、ベース→フランジ→TCP の FK、可動域、重力トルク、質量行列、工具を含む慣性、初期姿勢、衝突形状、重力補償の有無、位置／トルク駆動を比較する。Menagerie の FR3 は position actuator を持ち、Drake モデルも原モデルとの差を説明しているため、変換成功だけで同等性を判断しない。[Menagerie の変換手順](https://github.com/google-deepmind/mujoco_menagerie/blob/main/franka_fr3/README.md)・[Drake の差分説明](https://github.com/RobotLocomotion/models/blob/master/franka_description/README.md)

## 5. FCI ライセンス・購入条件

| 項目 | 確認結果・購入時に残す質問 | 出典 |
|---|---|---|
| OSS クライアント | libfranka は Apache-2.0。これは実機側 Feature 利用権とは別 | [公式 API のライセンス記載](https://frankarobotics.github.io/libfranka/0.15.0/) |
| 実機に必要な権利と導入 | FCI ライセンスと、Franka World アカウントに登録済みの Control が必要。Feature を同期し、Desk の Installed Features で確認 | [公式手順](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html#installing-the-fci-feature) |
| 毎回の使用条件 | ブレーキ解除後、Desk で Activate FCI。制御 PC は Arm 底部ではなく **Control の LAN** に接続 | [公式手順](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html) |
| 価格・同梱・更新費 | 日本向け現行価格、FCI が標準同梱か別売か、永続／期間契約か、更新・移管費は**未確認**。見積で本体、Hand／Robotiq、FCI、PC、架台、設置、教育、保守を分けて確認する | [メーカー問い合わせ](https://franka.de/contact)・[日本販売店の確認先](https://franka.de/partners) |
| 商用利用 | 現行 FR3 の個別 FCI 契約について、企業の研究利用・製品運用への利用範囲は**未確認**。旧 Panda の非商用記述を現行 FR3 の契約に外挿しない | [現行 FCI 導入条件](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html)・[メーカー契約条件への入口](https://franka.de/documents) |
| 中古・複数台 | Control の登録先変更、FCI ライセンス移管、Arm／Control の組合せ、Duo の各 Control に必要な権利を見積で確認。公開資料だけでは一括保証を確認できない | [Franka World マニュアル](https://download.franka.de/franka-world-manual/)・[ハード互換表](https://franka.de/fr3-compatibility-matrix) |
| 購買契約 | 手元の `New_GTC_EN_FrankaRobotics_040226.pdf` §10 はソフトウェアライセンス条件の遵守と OSS 条項を区別。これをもって FCI の価格・用途制限を確定できない | [公式 GTC へのリンクを含むページ](https://franka.de/documents) |

**調査者の推奨：** 発注仕様書に「納入 Image・対応 libfranka・FCI ライセンスの名義／用途／期間／再登録可否・公式モデル ID・検収時の状態取得と制御確認」を含める。これは公開条件の不足を埋める調達上の提案であり、メーカーが必須として列挙した仕様ではない。[条件の根拠](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html)・[互換表](https://franka.de/fr3-compatibility-matrix)

### Image と libfranka の照合表

次は公式互換表の範囲を整理したもの。Arm v2.1 等のハードウェア版とは別である。ROS の対応 OS は同ページ内でも組合せが複雑なため、ここから OS まで推定しない。[公式互換表](https://franka.de/fr3-compatibility-matrix)

| ロボット／System Image | libfranka | Robot／Gripper server |
|---|---|---|
| FR3 ≥5.9.0 | ≥0.18.0 | 10／3 |
| FR3 ≥5.7.2, <5.9.0 | ≥0.15.0, <0.18.0 | 9／3 |
| FR3 ≥5.7.0, <5.7.2 | ≥0.14.1, <0.15.0 | 8／3 |
| FR3 ≥5.5.0, <5.7.0 | ≥0.13.3, <0.14.1 | 7／3 |
| FR3 ≥5.2.0, <5.5.0 | ≥0.10.0, <0.13.3 | 6／3 |
| FER ≥4.2.1, <5.2.0（公式表の表記） | ≥0.9.1, <0.10.0 | 5／3 |

手元の `docs/fci/libfranka/docs/compatibility_matrix.rst.txt` は各行の下限中心の表記である。一方、メーカー Web 表には上限もあるため、下限だけ見て新しい libfranka を選ばない。とくに DROID の旧手順の `FR3 → 0.10.0` は全 FR3 Image をカバーしない。[手元資料の上流](https://frankarobotics.github.io/docs/doc/libfranka/docs/compatibility_matrix.html)・[上限付き公式表](https://franka.de/fr3-compatibility-matrix)・[DROID 手順](https://github.com/droid-dataset/droid/blob/main/docs/software-setup/host-installation.md)

## 6. Python 制御の比較・保守状況

保守状況は「確認した更新証拠」と「未確認」を分ける。GitHub API で最終 commit 日の取得を試みたが取得できず、deoxys／Polymetis の最終更新日や保守終了は確定していない。issue が残っていることだけを保守終了の根拠にしない。

| 選択肢 | 実行構成・用途 | FR3 と版選択 | 保守の証拠・留意点 |
|---|---|---|---|
| **pylibfranka（公式）** | libfranka の Python バインディング。外部 read/write 制御、状態取得、関節／直交制御、グリッパー例を提供 | libfranka と Image を照合。Python の重い推論を同期制御ループに混ぜる構成は避けることを推奨 | 公式変更履歴で0.16.0（2025-09-15）に導入、0.17.0 に直交姿勢制御追加。参照した履歴は0.21.3 まであり、終了処理の例外修正や型 stub を記載。ただし日付なし版の公開日は未確認。[導入](https://github.com/frankarobotics/libfranka/blob/main/pylibfranka/README.md)・[履歴](https://github.com/frankarobotics/libfranka/blob/main/CHANGELOG.md) |
| **panda-py**（配布名 `panda-python`） | C++ 側の制御スレッドと Python API。ROS なしの実験・既存 controller 利用の候補 | デフォルト PyPI 版は libfranka 0.9.2 を同梱すると README に記載。FR3 はサーバー版に合う別 wheel を選ぶ。名前が Panda でも FR3 用 build はある | **1.1.1、2026-10-01** の PyPI 公開と変更履歴を確認。停止 deadlock とログ取得による制御停止を修正。旧い0.8系しかないという判断は誤り。[README](https://github.com/JeanElsner/panda-py)・[PyPI](https://pypi.org/project/panda-python/1.1.1/)・[履歴](https://github.com/JeanElsner/panda-py/blob/main/CHANGELOG.md) |
| **deoxys_control** | Python desktop＋C++ 制御 PC／NUC。robosuite と実機の制御 API を接続する研究向け構成 | README の主対象は Panda。FR3 利用報告はあるが Image 別の公式保証表は今回未確認 | FR3 が例で動かない報告と追従誤差報告を確認。最終 commit 日・最新 FR3 Image の試験状況は未確認。既存 deoxys 実験の再現では採用候補、新規 FR3 の無検証導入は推奨しない。[README](https://github.com/UT-Austin-RPL/deoxys_control)・[#20](https://github.com/UT-Austin-RPL/deoxys_control/issues/20)・[#36](https://github.com/UT-Austin-RPL/deoxys_control/issues/36) |
| **Polymetis** | Python／PyTorch で controller を記述し、制御 server に渡す。TorchControl、Pinocchio、通信 client/server を持つ | 上流 README は Panda を説明。**DROID 上流手順が FR3 設定を提供**。最新 upstream を入れるだけで DROID と一致するとは限らない | MIT。公開 README・文書の存在、DROID での利用を確認。上流 Polymetis の直近最終更新日と保守終了は未確認。DROID 指定 submodule・libfranka・モデルを固定して評価。[上流](https://github.com/facebookresearch/fairo/blob/main/polymetis/README.md)・[DROID](https://github.com/droid-dataset/droid/blob/main/docs/software-setup/host-installation.md) |
| **FrankaPy＋franka-interface** | Python が ROS／protobuf で C++ 側の skill 実行へ指示。既存研究環境の再現候補 | 参照 README は Panda、ROS Melodic／Noetic、Ubuntu 18.04／20.04 を説明。現行 FR3 Image での標準対応は未確認 | 2020年のソフトウェア論文あり。新規 FR3 の第一候補とするには追加検証が必要。最終保守日は未確認。[README](https://github.com/iamlab-cmu/frankapy)・[論文](https://arxiv.org/abs/2011.02398) |
| **franky（追加候補）** | 高水準 Python／C++ 動作 API。非同期 motion 更新や reaction を提供 | README に0.18.0 までを含む libfranka の試験版一覧あり。自機との一致確認が必要 | frankx からの派生だが別実装として進展している。利用条件は独自記述を含むため採用時に LICENSE と商用条件を確認。直近最終保守日は未確認。[上流](https://github.com/TimSchneider42/franky) |

**調査者の選択案：** 新規 FR3 で公式 API を直接使うなら pylibfranka、C++ controller と扱いやすい Python API なら適合 build の panda-py、DROID 再現なら DROID に固定された Polymetis、既存 robosuite 系実験なら deoxys を評価する。これは機能・保守証拠からの比較判断であり、性能順位ではない。[公式 Python](https://github.com/frankarobotics/libfranka/blob/main/pylibfranka/README.md)・[panda-py](https://github.com/JeanElsner/panda-py)・[DROID](https://github.com/droid-dataset/droid)・[deoxys](https://github.com/UT-Austin-RPL/deoxys_control)

実時間部分と画像／VLA 推論部分を分ける構成を推奨する。公式 troubleshooting は1 kHz 制御での読出し→書込みの時間制約と、ループ中のモデルロードを避けることを説明する。Python バインディングの存在だけでは Python／GPU 処理全体の実時間性は保証されない。[公式 troubleshooting](https://frankarobotics.github.io/docs/troubleshooting.html)・[Polymetis の PC 分離案](https://github.com/facebookresearch/fairo/blob/main/polymetis/docs/source/prereq.md)

## 7. GitHub issue に繰り返し現れる不具合と対処

issue 全件の集計や発生率は**未確認**。ここでは通信系の複数報告と、実務上影響が大きい個別報告を挙げる。報告者の環境依存の対処を一般保証として扱わない。

| 症状・証拠 | 切り分け・対処 | 確認の強さ |
|---|---|---|
| `communication_constraints_violation`：libfranka [#60](https://github.com/frankarobotics/libfranka/issues/60)、[#186](https://github.com/frankarobotics/libfranka/issues/186)、franka_ros2 [#108](https://github.com/frankarobotics/franka_ros2/issues/108) 等 | まず同じ PC で公式 libfranka の例／`communication_test` と ROS 2 経由を比較。Control 直結、RT kernel、Release build、CPU governor、packet loss／jitter を確認 | **複数報告＋公式対処**。通信試験にはロボットを動かす例が含まれるので、読取り専用試験と区別。[公式](https://frankarobotics.github.io/docs/troubleshooting.html) |
| ROS 2 の時だけ同エラー：[#108](https://github.com/frankarobotics/franka_ros2/issues/108)、[#201](https://github.com/frankarobotics/franka_ros2/issues/201) | controller manager の overrun 管理、該当 branch の patch／設定、DDS 負荷を確認。`overruns.manage`／`enable_overrun` 等は版依存。設定名を別版へ無条件コピーしない | #108 には無効化しても改善しない報告もあり、**万能対処ではない** |
| controller 切替時の `UDP receive: Timeout`：libfranka [#241](https://github.com/frankarobotics/libfranka/issues/241) | UDP firewall、NIC／ネットワーク、スケジューリングを確認。controller manager 周波数増加を FR3 の FCI 周期変更だと解釈しない | メンテナーは libfranka が1 kHz feedback に同期すると説明。閉じた issue でも全環境で解決した保証ではない |
| `Incompatible Library Version` | Desk の Image と報告された server version、**実際にリンク／同梱した** libfranka を照合。Python wheel／Conda／ROS 依存の混在に注意 | **公式対処**。[troubleshooting](https://frankarobotics.github.io/docs/troubleshooting.html)・[panda-py の別 build 選択](https://github.com/JeanElsner/panda-py) |
| Connection timeout／FCI に入れない | FCI Feature・ライセンス、Activate FCI、Control 側 LAN、IP／route、SPoC 状態を確認 | **公式手順**。Arm 側ポートで Desk が見えることと FCI 制御 PC の正しい配線は別。[導入](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html)・[troubleshooting](https://frankarobotics.github.io/docs/troubleshooting.html) |
| jerk／velocity／acceleration discontinuity、`start_pose_invalid` | 最初の指令を実機の初期状態へ合わせ、速度・加速度を連続化。FR3 の位置依存速度上限と補間器を確認 | **公式仕様**。通信 packet loss も不連続を生むため、軌道側だけで原因確定しない。[仕様](https://frankarobotics.github.io/docs/robot_specifications.html)・[対処](https://frankarobotics.github.io/docs/troubleshooting.html) |
| panda-py の動作開始 segfault／停止 deadlock／ログ中断 | motion 呼出しの1.0.0 不具合は1.1.0、停止とログの不具合は1.1.1 の修正履歴を参照。適合 libfranka build を選んで更新する | **開発者が修正を記載**。頻発率は未確認。[変更履歴](https://github.com/JeanElsner/panda-py/blob/main/CHANGELOG.md) |
| pylibfranka の例外後にプロセスが落ちる | 参照した0.21.3 履歴に `ActiveControl` destructor からの例外による `std::terminate` 修正あり。Image 互換と該当変更の配布有無を確認 | **公式修正履歴**。0.21.3 の公開日は履歴に記載がなく未確認。[変更履歴](https://github.com/frankarobotics/libfranka/blob/main/CHANGELOG.md) |
| deoxys の新 FR3 が動かない：[#20](https://github.com/UT-Austin-RPL/deoxys_control/issues/20) | まず単体 libfranka 接続を確認し、NUC↔desktop の遅延や送信条件を追う。counter を増やす提案はあるが、検証済み一般解ではない | **複数ユーザー報告、確定解は未確認** |
| deoxys の末端到達誤差：[#36](https://github.com/UT-Austin-RPL/deoxys_control/issues/36) | TCP／IK モデル／工具慣性／controller gain／settling を個別に確認することを推奨。記載された誤差を FR3 の絶対精度として引用しない | **個別報告**。原因や解決の実機検証は未確認。[工具設定の根拠](https://github.com/facebookresearch/fairo/blob/main/polymetis/docs/source/troubleshooting.md) |
| シミュレーション初期姿勢が関節制限外：description [#33](https://github.com/frankarobotics/franka_description/issues/33) | 関節ゼロを home と仮定しない。reset 姿勢をモデルの limits と比較し、有効な keyframe を明示 | **個別の静的設定報告**。同 issue は Menagerie FR3 の home は影響を受けないと説明 |

安全機能の拒否を通信不良と混同しない。手元の R02212/2.6 の脚注は、Image <5.10 で SLP-C／SLS-C 設定時の FCI 制約に言及する。設定変更を行う際は対象 Image の操作マニュアルと安全設計を確認し、エラー回避だけを目的に監視機能を無効化しない。[データシート・操作マニュアル掲載元](https://franka.de/documents)・[公式 troubleshooting](https://frankarobotics.github.io/docs/troubleshooting.html)

## 8. GELLO・DROID・ALOHA 系の構成例

| 構成 | 一次情報で確認した実装 | FR3 導入に使う部分・境界 |
|---|---|---|
| GELLO 原論文 | 同じ運動学構造の小型 leader を使う方式。著者サイトの Franka 実演は Panda と表示 | 原論文の結果を FR3 v2 の実証と読み替えない。[論文](https://arxiv.org/abs/2309.13037)・[著者サイト](https://wuphilipp.github.io/gello_site/) |
| Franka GELLO Single | 上流 `gello_software/ros2` に FR3＋ROS 2 Humble、Franka Hand 用設定と起動手順あり | GELLO publisher → FR3 controller、gripper は別ノード。`com_port`、`robot_ip`、sign／offset を設定。[ROS 2 手順](https://github.com/wuphilipp/gello_software/blob/main/ros2/README.md) |
| Franka GELLO Duo＋FR3 Duo | 同じ上流に Duo 用設定と Robotiq controller 手順。メーカーは単腕／双腕の試作機を案内 | 双腕 leader と左右 FR3 の対応・同期初期姿勢を確認。手元の R62040/1.2 は v2.0 以降の運動学に対応し、従来世代は少し異なると記載。製品案内は **prototype**。[メーカー](https://franka.de/gello)・[資料 R62040](https://franka.de/documents) |
| FR3 Duo の視覚構成 | 公式 reference setup は Robotiq 2F-85 ×2、RealSense D405 wrist ×2、ZED Mini と Head Bracket | 同一名の bare Duo と視覚・把持 kit 付き構成を区別。[公式モデル・構成説明](https://franka.de/models-and-simulation) |
| DROID＋FR3 | 上流 host-installation に FR3 用 libfranka／設定ファイル、`robot_type=fr3`、Polymetis server、Quest、Robotiq 工具設定の説明あり | **実在する上流 FR3 対応**。古い Image 向け0.10.0 記載を現行機へ固定しない。pinned `fairo` submodule、RobotModel、工具、Image を一組で検証。[上流手順](https://github.com/droid-dataset/droid/blob/main/docs/software-setup/host-installation.md)・[コード](https://github.com/droid-dataset/droid) |
| ALOHA／ACT | 著者が公開する双腕 imitation learning のハードウェア・ACT。ALOHA 2 のサイトは Trossen の WidowX／ViperX 系を案内 | **原版は FR3 標準構成ではない**。今回、原版 ALOHA／ALOHA 2 上流で検証済みの FR3 置換構成は未確認。ACT の利用と ALOHA ハードウェア互換性を分ける。[ALOHA](https://github.com/tonyzhaozh/aloha)・[原論文](https://arxiv.org/abs/2304.13705)・[ALOHA 2](https://aloha-2.github.io/) |

**調査者の推奨する FR3 双腕構成案：** 実装根拠がある FR3 Duo＋GELLO Duo＋上記の視覚・把持 kit を基準に、データ記録と学習系を追加する。これを「公式 ALOHA-FR3」と呼ばず、GELLO／FR3 Duo に ACT 等を組み合わせる独自構成として記録する。画像時刻・左右関節・gripper・action の同期、左右ベース変換、TCP、左右の安全領域は別途検証項目とする。[Duo 構成](https://franka.de/models-and-simulation)・[GELLO の実装](https://github.com/wuphilipp/gello_software/blob/main/ros2/README.md)・[ACT の出典](https://arxiv.org/abs/2304.13705)

## 9. 日本の販売代理店・日本語資料

| 窓口・資料 | 確認結果と利用先 | 出典 |
|---|---|---|
| 国内販売窓口 | メーカー公式 partner 一覧の JAPAN は **RYOSAN CO. LTD.** と `ryosan.co.jp` を掲載 | [メーカー一覧](https://franka.de/partners) |
| 日本側の現行表記 | リョーサン菱洋テクラボは「リョーサンが日本唯一の正規代理店」と説明。**唯一という表現は販売店側の自己申告**。問い合わせ先法人・契約名義は現行窓口で確認 | [販売店自身の解説](https://techlabo.rers-grp.com/article/25080517_1254.html) |
| メーカー日本語製品説明 | FR3 と FCI の概要を日本語で確認できる。宣伝上の性能表現はメーカー自己申告 | [日本語製品ページ](https://franka.de/ja/franka-research-3) |
| メーカー日本語 Hardware Manual | 手元の `Hardware Manual Franka Research 3_Armv2.0_R02210_1.0_JA.pdf` は本文で Arm v2.0、2025年11月の初回版と確認。公式一覧にも v2.0 の JA がある | [公式資料一覧の JA](https://franka.de/documents) |
| v2.1／v2.2 の日本語版 | 確認した公式一覧の v2.1／v2.2 ハードウェア資料の言語列には JA がない。日本語最新版の入手可否は**未確認**。v2.0 翻訳だけで新世代を運用しない | [公式一覧](https://franka.de/documents) |
| 国内向け技術資料 | リョーサンによる FR3 の日本語ホワイトペーパー所在を確認。今回 PDF の新規取得はしていない | [販売店資料 URL](https://techlabo.ryosan.co.jp/article/Item/CK000341_FRANKA%20RESEARCH3_WP.pdf) |

**調査者の照会案：** Arm v2.2 の変更点とモデル指定、国内納入 Image、FCI の利用範囲と移管、日本語版の適用世代、RT PC の推奨構成、Robotiq／カメラ込みの工具パラメータ、検収・故障時の国内対応をまとめて問い合わせる。価格や納期を未確認の Web 数値で埋めない。[国内窓口の確認元](https://franka.de/partners)・[仕様と互換性](https://franka.de/fr3-compatibility-matrix)

## 10. 利用した手元資料と調査の限界

以下は既存ファイルを読み取りのみ利用した。上流 URL を併記するが、取得済みファイルの hash と Web 版の同一性までは照合していない。

| 手元の相対パス（`franka(fr3)/` 基準） | 今回の利用内容 | 上流 URL |
|---|---|---|
| `docs/fci/overview.rst.txt`、`robot_specifications.rst.txt`、`troubleshooting.rst.txt`、`compatibility.rst.txt` | FER／FR3 の区分、制御制限、FCI とネットワークの切り分け | [FCI](https://frankarobotics.github.io/docs/) |
| `docs/fci/libfranka/docs/compatibility_matrix.rst.txt` | 下限中心の表記と Web 表の上限付き範囲の照合 | [互換文書](https://frankarobotics.github.io/docs/doc/libfranka/docs/compatibility_matrix.html) |
| `docs/repos/franka_description_README.md`、`franka_description_CHANGELOG.rst` | 世代 ID、Desk 表示、v2 の inertials、v2.1 追加 | [公式 description](https://github.com/frankarobotics/franka_description) |
| `docs/repos/libfranka_CHANGELOG.md` | Python 導入、Pinocchio、0.21.3 までの修正内容 | [公式履歴](https://github.com/frankarobotics/libfranka/blob/main/CHANGELOG.md) |
| `docs/official_pdf/Hardware Manual Franka Research 3_Arm_v1_R02210_1.3_EN.pdf` | v1 対象・重量記述・文書分離 | [公式掲載元](https://franka.de/documents) |
| `docs/official_pdf/Hardware Manual Franka Research 3_Arm v2.0_R02210_1.3_EN.pdf` | v2.0 対象・重量記述 | [公式掲載元](https://franka.de/documents) |
| `docs/official_pdf/Hardware Manual Franka Research 3_Arm v2.1_R02210_1.3_EN.pdf` | p.2 の v2.1 変更概要 | [公式掲載元](https://franka.de/documents) |
| `docs/official_pdf/Datasheet Franka Research 3_R02212_2.2.2_EN_June 2026.pdf`、`..._2.6_EN_July 2026.pdf` | 文書版と Arm 世代の区別、v2.1／v2.2 共通仕様、FCI 制約脚注 | [公式掲載元](https://franka.de/documents) |
| `docs/official_pdf/Operating Manual Franka Research 3_5.10_R02216_1.3_EN.pdf` | FCI、モデル・工具設定の説明を確認 | [公式掲載元](https://franka.de/documents) |
| `docs/official_pdf/Quick Guide for Installation Franka GELLO DUO_0.5_R62040_1.2_EN.pdf` | v2.0 以降の運動学、prototype の位置付け、上流リポジトリ | [公式掲載元](https://franka.de/documents) |
| `docs/official_pdf/Hardware Manual Franka Research 3_Armv2.0_R02210_1.0_JA.pdf` | 日本語版の対象ハードウェア・版 | [公式掲載元](https://franka.de/documents) |
| `docs/official_pdf/New_GTC_EN_FrankaRobotics_040226.pdf` | ソフトウェア契約条項を読み、FCI 個別条件の確定とは分けた | [公式 GTC リンクの入口](https://franka.de/documents) |

論文候補は同じディレクトリの `candidates.tsv` に記載した。`year` は原則として最初の公開年、出版社で確認した雑誌論文は掲載年。`status` に FR3 の直接性、査読先未確認、コード未確認等を残す。arXiv ID は個別 abstract ページで確認したものだけを記載し、確認できない項目は「未確認」とした。PDF URL は参照先の記録であり、PDF はダウンロードしていない。
