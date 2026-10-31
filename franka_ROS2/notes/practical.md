# franka_ros2 実践メモ

調査基準日: **2026-10-31**。対象は FR3 を中心とする実機制御と、その周辺の ROS 2・学習系接続。以下の「推奨」「設計案」は調査結果からの判断であり、実機動作の確認結果ではない。ローカルの `docs/humble/`、`docs/jazzy/` の README、CHANGELOG、bringup、hardware、semantic components、example controllers、MoveIt、Gazebo 資料を読んで使用した。実機、Docker、ROS 2、シミュレータでの実行は**未検証**。

## 1. Jazzy と Humble の選び方

| 条件 | 選択案と根拠 |
|---|---|
| 新規 FR3 環境 | Ubuntu 24.04 + Jazzy を第一候補にする。公式 Jazzy 互換資料がこの組合せを強く推奨する。[Jazzy 互換表][compat-j] |
| Ubuntu 22.04 の既存実験、Humble 専用コードの再現 | Humble ブランチを固定して継続する。公式 Humble 互換資料の基盤 OS は Ubuntu 22.04。[Humble 互換表][compat-h] |
| GELLO の公開 ROS 2 実装をそのまま再現 | `wuphilipp/gello_software/ros2` は Humble 向け。Jazzy への移植済みとは扱わない。[GELLO ROS 2][gello] |
| 旧 Panda を含む複数腕、MuJoCo と同じ制御器の利用 | `multipanda_ros2` の専用環境を検討する。公式 FR3 最新スタックと、Panda・旧 libfranka を対象とする派生スタックの依存を混在させない。[論文対応リポジトリ][multi] |

基準日前に確認できた Jazzy リリースは **v3.6.1（2026-10-27）**で、要求は **libfranka >= 0.20.4、franka_description >= 2.9.0**。ローカルの Jazzy 互換表は v3.4.0 / description >=2.8.0 までの記載なので、最新の最小依存条件にはリリースと CHANGELOG を併用する。Humble のローカル CHANGELOG は **v2.7.1（2026-09-01）**を先頭に持つ。番号の大小だけでブランチを取り替えず、**ロボット System Image → libfranka → franka_ros2 → description → ros2_control** の組合せを記録する。[Jazzy リリース][release-j]、[Humble リリース][release-h]、[公式機体互換表][robot-compat]

推奨する再現記録は OS、カーネル、ROS distribution、各リポジトリの SHA、依存取り込み結果、実行時にロードされた libfranka の場所、機体 System Image、設定 YAML。公式 README 自体が破壊的変更を予告し、Issue #218 には upstream libfranka と ROS 配布バイナリのパッケージ競合が報告されているため、この単位で固定するのが妥当。[README][readme]、[#218][i218]

## 2. Docker と実機への接続

### 準備と構築

公式は Docker を推奨するが、**実機用ホストは Linux + PREEMPT_RT + Docker Engine を選ぶ**。Windows は公式サポート対象外で、README は UDP timeout 時に Docker Desktop を避けるよう案内している。コンテナを使ってもホスト側カーネルの実時間要件は残る。[README][readme]、[実時間カーネル][rt]

以下は公式手順を基にした **Linux 上の別の作業用チェックアウト**での実行例。本資料を置く収集フォルダで実行する指示ではない。依存を取り込む前にタグを固定し、対応する `dependency.repos` を使う。[README][readme]、[v3.6.1][release-j]

```bash
git clone --branch v3.6.1 https://github.com/frankarobotics/franka_ros2.git franka_runtime
cd franka_runtime
# .env に USER_UID、USER_GID、CONTAINER_NAME を設定する
docker compose build
docker compose up -d
docker compose exec franka_ros2_jazzy bash
```

コンテナでは workspace のルートで依存を取り込み、Release ビルドし、`install/setup.bash` を source する。公式構成はホストのチェックアウトを `/ros2_ws/src` にマウントするため、ホスト側リポジトリ直下とコンテナ側 workspace 直下は異なる。[README][readme]、[Compose][compose]

```bash
cd /ros2_ws
vcs import src --recursive --skip-existing < src/dependency.repos
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --symlink-install
source install/setup.bash
```

公式 Compose の確認点は `network_mode: host`、`SYS_NICE`、`rtprio`、`rttime`、`memlock`、`limits.conf`、デバイスの共有。提示構成は `privileged: true` も使う。これらの設定があることと、起動したプロセスに実際に RT 権限が付いたことは別なので、コンテナ内でも `ulimit -r` / `ulimit -l` を確認する、というのが本メモの運用提案。GUI には DISPLAY と X11 socket の共有も確認する。[Compose][compose]、[RT 権限設定][rt]

### 接続と起動の順序

1. 機体の互換表を確認し、PC を **Control の LAN** に直接つなぐ。Arm の LAN とは区別する。機体のネットワーク設定に合わせて固定 IP と到達経路を設定する。[FCI ネットワーク要件][net]
2. Desk の **Activate FCI** と FCI feature の状態を確認する。単に ping が通るだけでは FCI 制御が可能とは判定しない。[接続トラブルシュート][trouble]
3. `ping` と libfranka の `communication_test` を行う。平均 RTT だけでなく最大遅延、損失、制御時の成功率を見る。[診断手順][trouble]、[ネットワーク要件][net]
4. まず fake hardware でモデル、TF、MoveIt の設定を確認する。その後、実機 bringup で状態を読み、最後に目的の command controller を有効化する。[MoveIt 設定][moveit]、[bringup][bringup]

公式 launch の最小例。IP は実際の FCI IP に置換する。下段は実機に接続する。[MoveIt][moveit]、[bringup][bringup]

```bash
ros2 launch franka_fr3_moveit_config moveit.launch.py use_fake_hardware:=true robot_ip:=dont-care
ros2 launch franka_bringup franka.launch.py robot_ip:=<FCI_IP> robot_type:=fr3
```

`example.launch.py` は `franka.config.yaml` を読むため、実機 IP、namespace、gripper の有無をそこで合わせる。単腕の引数は `controller_names`。FR3 Duo は専用 launch と **`controller_name`（単数）**を使い、現在の公式 Duo 経路は腕の effort command のみを対象とする。[bringup][bringup]

## 3. ros2_control の制御器とインターフェース

### 公式 example controllers の分類

以下は Jazzy 資料と `controllers.yaml` の登録名。全てが同じ環境で動くという意味ではなく、実機・fake・Gazebo ごとの export interface の照合が必要。[examples][examples]、[登録 YAML][controllers]

| 分類 | 登録名 | 用途・注意 |
|---|---|---|
| 状態表示 | `joint_state_broadcaster`、`franka_robot_state_broadcaster` | 標準関節状態と Franka 固有状態を配信する。指令制御器とは区別。[hardware][hardware] |
| 読み取り例 | `model_example_controller` | コリオリ、重力、姿勢、Jacobian の取得例。[examples][examples] |
| トルク基礎 | `gravity_compensation_example_controller` | ゼロの関節トルク指令。実機側の自重補償を利用する。[examples][examples] |
| 初期姿勢移動 | `move_to_start_example_controller` | ホーム姿勢への移動例。任意の外部目標を受ける汎用制御器とは扱わない。[examples][examples] |
| 関節インピーダンス | `joint_impedance_example_controller`、`joint_impedance_with_ik_example_controller` | 前者は周期運動、後者は MoveIt の IK service で求めた関節目標を利用。[examples][examples] |
| 関節 motion generator | `joint_position_example_controller`、`joint_velocity_example_controller` | 関節位置・速度の周期指令例。[examples][examples] |
| Cartesian motion generator | `cartesian_pose_example_controller`、`cartesian_orientation_example_controller`、`cartesian_velocity_example_controller` | Cartesian pose、orientation、velocity の指令例。[examples][examples] |
| 冗長自由度 | `cartesian_elbow_example_controller`、`cartesian_pose_elbow_example_controller`、`elbow_example_controller` | YAML の前二者は同じ `CartesianElbowExampleController` 型の登録。elbow の指定と pose/velocity の組合せを確認する。[登録 YAML][controllers] |
| Cartesian インピーダンス | `cartesian_impedance_example_controller` | 平衡姿勢と剛性を外部更新できるトルク制御例。[コード][cart-code] |
| グリッパ | `gripper_example_controller` | Franka Hand の action goal を送る例。[examples][examples] |
| 複数腕・移動体 | `fr3_duo_joint_impedance_example_controller`、`mobile_fr3_duo_joint_impedance_example_controller` | 腕の effort 制御。mobile 版は台車も統合。`swerve_drive_controller` は `franka_mobile` 所属。[examples][examples]、[登録 YAML][controllers] |

**資料の不整合**: examples 冒頭には「位置 interface は使えずトルクのみ」という古い説明が残る一方、同資料の後段、hardware 資料、実装は position / velocity / Cartesian の例を持つ。単腕の対応判断は hardware と使用タグのコードを優先する。また hardware 資料には `initial_position` が列挙されるが、過去の CHANGELOG には初期状態 interface の削除があるため、実際の `list_hardware_interfaces` を確認する。[examples][examples]、[hardware][hardware]、[CHANGELOG][changes]

### トルク、関節インピーダンス、Cartesian を混同しない

- **effort command** は重力を除く所望関節トルク。hardware は position / velocity / effort の state と、単腕の position / velocity / effort command を提供する。重力を二重加算しない。[hardware][hardware]
- **外部関節インピーダンス**は関節目標との差・速度からトルクを作る。**外部 Cartesian インピーダンス**は手先誤差と Jacobian 等から関節トルクを作る。公式 Cartesian 例は task 成分、nullspace 成分、コリオリ補償を組み合わせる。[関節例][joint-code]、[Cartesian 例][cart-code]
- **Cartesian pose / velocity command** は Franka semantic component を通じて motion generator に送る経路。Cartesian インピーダンスの effort command とは異なる。内部剛性の設定が期待通り効かないという #53 の報告もあり、内部制御モードと外部制御器側の剛性を分けて確認する。[semantic components][semantic]、[#53][i53]
- 公式 Cartesian インピーダンス例の入力は `~/equilibrium_pose`（`geometry_msgs/msg/PoseStamped`）と `~/set_cartesian_stiffness`（`franka_msgs/srv/SetCartesianStiffness`）。この service と hardware の内部パラメータ設定 service は同名末尾でも別の対象。namespace を含む完全名を確認する。[コード][cart-code]

### 自作コントローラの作り方

1. `ament_cmake` パッケージに `controller_interface::ControllerInterface` 派生クラスを作る。`on_init`、`on_configure`、`on_activate`、`on_deactivate`、`update` と interface configuration を実装する。[ros2_control 作成ガイド][custom]
2. 使用する joint と `position` / `velocity` / `effort` の名前を列挙する。型だけでなく URDF の joint 名・prefix を一致させる。model/state の特殊 interface は直接キャストせず `FrankaRobotModel` / `FrankaRobotState` を使う。[作成ガイド][custom]、[semantic][semantic]
3. `on_configure` までにパラメータ、メモリ、非 RT 通信を準備する。`on_activate` で loaned interfaces を関連付け、現在値から目標を初期化する。`on_activate` も更新スレッドで呼ばれるので、重い処理を持ち込まない。[作成ガイド][custom]、[Cartesian 例][cart-code]
4. 非 RT の購読 callback と RT の `update` は realtime buffer/box 等で橋渡しする。推論・HTTP・IK service 待ち・毎周期ログ・動的確保を制御ループ内で実行しない。[Cartesian 例][cart-code]、[FCI の RT 注意事項][trouble]
5. pluginlib export、plugin XML、共有ライブラリと CMake export を設定し、controller manager の YAML に `type: package/Class` を登録する。ビルド後に型が見えること、load/configure/activate が進むことを順に確認する。[作成ガイド][custom]
6. 最初は状態読み取り、次に現在姿勢保持、最後に小さな目標変化で確認する、というのが本メモの実装提案。指令の時間切れ、有限値検査、速度・トルク変化制限を実装対象にする。FCI は不連続指令でも停止し得るため、通信問題だけを疑わない。[FCI troubleshooting][trouble]

運用時は `ros2 control list_controllers`、`list_controller_types`、`list_hardware_components`、`list_hardware_interfaces` で、登録、ライフサイクル、利用可能・claim 済み interface を確認する。対象 namespace の controller manager を指定する。[ros2_control CLI][cli]

## 4. MoveIt 2 / Servo / Gazebo / Isaac Sim

| 経路 | 実践上の要点 |
|---|---|
| MoveIt 2 → 実機 | 公式 `franka_fr3_moveit_config moveit.launch.py` を使用。planning group は選んだ `robot_type` の arm。Hand の有無で TCP が変わるので、学習データの TCP と一致させる。[MoveIt 資料][moveit] |
| MoveIt Servo → 実機 | Servo は関節目標を出す上位処理。URDF/SRDF、関節状態、位置または速度を受ける controller が必要。直接 FCI の 1 kHz トルクループとして使う構成ではない。[Servo][servo] |
| Gazebo → ros2_control | 公式 Gazebo bringup を利用。position / velocity / joint impedance の起動例がある。gripper の velocity 制御には既知の問題があり、公式資料は position interface を案内する。[Gazebo 資料][gazebo] |
| Isaac Sim → MoveIt 2 | NVIDIA の Franka MoveIt scene と `isaac_moveit` の例を再現してからモデルを差し替える。標準例の planning group は `panda_arm` なので FR3 の名前をそのまま混用しない。[NVIDIA tutorial][isaac] |
| Isaac Sim → ros2_control | NVIDIA 6.2 資料には in-process ControllerManager と SystemInterface を提供する `isaacsim.ros2.control` がある。これを Franka 実機用 hardware plugin と同一視しない。[NVIDIA API][isaac-api] |

Servo 接続の設計案は「入力 device / VLA → Twist・JointJog 等 → Servo → JointTrajectory 等 → 対応 controller → franka_hardware」。`command_out_type` と `command_out_topic` を受け側に合わせ、planning frame、EE frame、joint 名、timeout、collision/singularity status、smoothing を確認する。参照した現行 main 資料は PoseStamped 入力も説明するが、**Humble/Jazzy のインストール済み版が同じ API を持つかは未確認**。Humble では専用版の資料も参照する。[現行 Servo][servo]、[Humble Servo][servo-h]

Gazebo の入口は例えば次の二つ。fake hardware はモデル表示・コマンド経路の確認、Gazebo は物理シミュレーションという目的で使い分ける、というのが本メモの検証方針。[Gazebo][gazebo]、[fake hardware の公式例][readme]

```bash
ros2 launch franka_gazebo_bringup visualize_franka_robot.launch.py
ros2 launch franka_gazebo_bringup gazebo_franka_arm_example_controller.launch.py controller:=joint_impedance_example_controller
```

Jazzy の v3.4.0 では Gazebo の構成が `franka_gazebo_bringup` と `franka_gazebo_hardware` に整理され、モデル計算による重力補償 plugin が導入された。古い `franka_ign_ros2_control` の共有ライブラリ名を新しい環境へコピーする前に、同じ版の xacro と plugin 登録を使う。Gazebo Classic 用 `gazebo_ros2_control` は Jazzy にリリースされていない。[CHANGELOG][changes]、[Classic の公式注意][classic]

Isaac Sim の公式 Franka USD 配布は `franka_simulation`。README は **Isaac Sim 6.0.0-rc.59** を対応 runtime と記し、FR3 v2.1、Duo 等のモデルを列挙する。これは asset 配布の対応条件で、別版の Isaac Sim や franka_ros2 の全 semantic interfaces がそのまま動く保証ではない。NVIDIA 6.0 tutorial は Humble の断続的 timeout を既知の制限として記し、Jazzy を案内するが、**ベンダーの説明であり本調査での性能比較ではない**。[Franka USD][usd]、[NVIDIA tutorial][isaac]

## 5. 実時間性の調整

### PREEMPT_RT とスケジューリング

公式要件は PREEMPT_RT 上での実時間優先度実行。Ubuntu 22.04 / 24.04 には Ubuntu Pro の RT kernel が推奨され、手動パッチの案内もある。起動後は `uname -a` と `/sys/kernel/realtime`（値 1）で確認し、realtime group と rtprio/memlock の limits を設定して再ログインする。一般ユーザーを sudo 実行することだけを解決策にしない。[RT 設定][rt]

現行の公式 `controllers.yaml` は `update_rate: 1000`、`thread_priority: 97`、`overruns.manage: false` を持つ。これらは当該構成の値で、別版 ros2_control に無条件で移植する推奨値ではない。libfranka はロボットからの feedback を待つため、controller manager の周波数を上げれば通信要件が解決するとはいえない。[設定 YAML][controllers]、[libfranka #241 の議論][lib-i241]

### NIC と CPU

| 調整項目 | 手順・判定 |
|---|---|
| 配線と経路 | 専用の有線 NIC から Control へ直接接続し、スイッチ等を減らす。RTT・制御計算・機体処理の合計で周期条件を満たす必要がある。[要件][net] |
| NIC の診断 | `ethtool -i <NIC>`、`ethtool -S <NIC>`、`ethtool -c <NIC>` で driver、drop/error、coalescing を調べる。[ethtool manual][ethtool] |
| 割込み抑制 | 対応 NIC で adaptive coalescing を無効にし `rx-usecs` / `tx-usecs` を減らす比較を行う。Intel i40e の公式 driver 資料は低遅延向けに双方 0 の例を示す。全 NIC 共通の Franka 指定ではなく、割込み増加と CPU 負荷も実測する。[Linux i40e 資料][nic] |
| EEE / offload | `ethtool --show-eee <NIC>` と `ethtool -k <NIC>` で現状を保存する。EEE 無効化や offload 一括無効化が Franka 全構成に必要という根拠は**未確認**。変更するなら個別比較にする。[ethtool manual][ethtool] |
| CPU 周波数 | `cpufreq-info` で governor を確認し、公式案内に従って performance に変更する。推論負荷を載せた状態でも遅延を測る。[Franka troubleshooting][trouble] |
| affinity / IRQ | RT loop と GPU 推論・画像処理・記録処理の競合を減らす設計を検討する。NIC IRQ と CPU の固定方法は driver と NUMA 構成依存。コア番号や C-state/SMT の一律設定値は本調査では**未確認**。[Linux i40e][nic] |

診断は `communication_test`、制御周期の最大遅延、NIC counters、`control_command_success_rate` を組み合わせる。公式要件は 1 kHz 通信と合計 1 ms 未満を説明するが、平均 ping が小さいことだけでは制御ループの最悪遅延を保証しない。[要件][net]、[診断][trouble]

VLA 用 GPU と RT 用ホストの分離は本メモの設計提案。公式 RT 文書も NVIDIA driver の PREEMPT_RT 上のサポートに注意を記しているので、RT ホストに推論環境を追加する場合は事前検証する。[RT 文書][rt]

## 6. Issue で繰り返し現れる問題と対処

以下は公式 Issue、README、CHANGELOG を突き合わせた**症状別の整理**。Issue 全件の集計は行っておらず、発生件数・頻度の順位は**未確認**。Issue の Open/Closed は閲覧時の表示であり、Closed だけを修正済みの根拠にしない。[Issue 一覧][issues]

| 症状・根拠 | 切り分けと対処 | 確認範囲 |
|---|---|---|
| System 更新後の Incompatible library version（#103） | System Image と libfranka の互換を確認。別の場所の `.so` をロードしていないか、依存も含めて再構築されたか確認する。[#103][i103] | 個別報告。全機体に共通の単一バージョンへの更新は勧めない。 |
| APT 競合（#218） | upstream `libfranka` と `ros-humble-libfranka` を混在させない。必要な版が ROS binary にない場合は依存を揃えた source workspace を使う。[#218][i218] | Closed。パッケージ制約が全て撤廃されたとは確認できない。 |
| UDP timeout / communication constraints | FCI 有効化、Control LAN、firewall の UDP、RT kernel・権限、CPU governor、Release build を順に調べる。[公式診断][trouble] | 同じ timeout でも接続失敗・周期超過・例外処理は別問題。 |
| Humble の `read()` から NetworkException が漏れて process abort（#249） | 報告された deployed binary の SHA は不明。使用ソースの catch 範囲を確認し、例外を hardware error に変換する修正の適用状況を調べる。[#249][i249] | Open。報告中の修正案をリリース済み対処とは扱わない。 |
| command mode switch で RT thread が block（#243） | 使用版と切替周期を記録する。v3.6.1 には read/write の block 回避等が記載されるが、mode switch 自体の全問題解決とは断定しない。[#243][i243]、[CHANGELOG][changes] | Issue は Open。Jazzy の修正を Humble 適用済みとみなさない。 |
| 書込失敗なのに `write()` が OK（#250） | action の成功に加え、実測 joint state、robot mode、error を確認する。例外を握り潰す経路を調べる。[#250][i250] | Open。投稿者自身も実機の無動作事象との因果関係は未立証としている。 |
| fake hardware の Cartesian velocity configure timeout（#248） | mock が当該 Cartesian interface を export するか確認する。RViz 表示成功を FCI 固有制御器の動作成功と扱わない。[#248][i248] | Humble v2.2.0 の個別報告。解決確認は未確認。 |
| 剛性値が効かない（#53） | 内部 stiffness service と外部 effort controller のゲインを区別し、使用モードと実際の受信先を確認する。[#53][i53]、[公式 Cartesian 例][cart-code] | Open。全版に対する原因・修正版は未確認。 |
| 多関節 URDF で robot state の joint 名・frame が誤る | v3.6.1 は対象腕の joint/frame を名前で選ぶ修正を記載。既存データと TF の frame 解釈も再確認する。[CHANGELOG][changes] | 公式修正記載。実験ログの再評価要否は利用者側で判断。 |
| move-to-start 中の通信 reflex | v3.6.1 は RT loop 内の parameter 更新を外す修正を記載。RT 内の ROS parameter/service 操作を見直す。[CHANGELOG][changes] | 公式修正記載。本環境で再現試験は未実施。 |

### 破壊的変更の移行チェック

| 変更 | 影響と移行 |
|---|---|
| 旧 `panda/robot_model` / `panda/robot_state` 固定名 | robot_type と arm_prefix に対応する interface 名を使う。公開 joint interface の命名変更とは別。[hardware][hardware] |
| 初期 pose/elbow accessor の置換 | 古い `getInitial*` 使用箇所を検索し、現行 `getCurrent*` と state の意味を確認して移植する。[CHANGELOG][changes] |
| `arm_id` → `robot_type`、単腕 `controller_name` → `controller_names` | 自作 YAML、launch、コントローラを合わせて更新する。ただし Duo 専用 launch の単数引数は維持されている。[CHANGELOG][changes]、[bringup][bringup] |
| MoveIt group / TCP | 旧 manipulator group 前提のコードを見直す。現行 arm group と Hand 有無に応じた TCP を確認する。[MoveIt][moveit]、[CHANGELOG][changes] |
| v3.3.0 の ros2_control ABI 整合 | 古い build/install を再利用せず、新規 workspace で依存一式を再構築する。hardware_interface だけ別系統から重ねない。[CHANGELOG][changes] |
| v3.3.0 の convenience topics の QoS | `current_pose`、wrench 等の購読を best_effort に対応させる。デフォルト reliable の購読では届かなくなる。[CHANGELOG][changes] |
| v3.4.0 の `collision_detected` QoS | 購読側を SensorDataQoS / best_effort にする。Duo の collision monitor が受信できているか確認する。[CHANGELOG][changes]、[examples][examples] |
| state interface の内部格納方式 | RealtimeBuffer から RealtimeThreadSafeBox への変更あり。特殊 state を直接解釈する自作コードを避け semantic component 経由にする。[CHANGELOG][changes] |
| v3.6.1 の Cartesian impedance の設定名 | 残った `arm_id` override を `robot_type` に更新する。既定 fr3 以外・prefix 付き構成で特に確認する。[CHANGELOG][changes] |

現行 Jazzy hardware 資料の ControlException 復帰は「機体 error recovery action → hardware component active → command controller active」の順。NetworkException は別扱いで error となり broadcaster も停止し得る。古い版・Humble が同じ復帰仕様を持つかは使用ソースで確認する。[hardware 復帰手順][hardware]

## 7. コミュニティパッケージの保守状況

最終更新は、閲覧できた default branch の commit history の先頭日付。今後の保守保証、サポート契約、Jazzy 対応保証を意味しない。

| パッケージ | 公開根拠と評価 |
|---|---|
| `matthias-mayr/Cartesian-Impedance-Controller` | ROS 2/1 binding と独立 C++ library を持ち、ROS 2 の FR3 実機・sim 利用を作者が説明する。ROS 2 の型は `cartesian_impedance_controller/CartesianImpedanceController`。history 先頭は **2026-10-12**、2026-05-20 に colcon test 対応等があるため保守の形跡あり。現在の Jazzy v3.6.1 との組合せは未確認。[README][community]、[履歴][community-log] |
| `LucasG2001/cartesian_impedance_control` | Humble、libfranka >=0.13.0 を前提とする README があり、古い `franka_ros2 v0.13.1` 表記は検証済み公式タグとして採用しない。型は `cartesian_impedance_control/CartesianImpedanceController` で上記と異なる。`CurdinDeplazes` の旧 URL はこの repository に redirect した。history 先頭は **2025-10-22**、Jazzy 移行は未確認。[README][lucas]、[履歴][lucas-log] |
| `tenfoldpaper/multipanda_ros2` | 論文の arXiv ページがリンクするコード。Humble branch の history 先頭は **2026-10-28**で、実機向け position/velocity controller と multi-hardware interface の変更がある。継続更新の形跡はあるが、README の手動構築例は Panda/旧 libfranka 前提なので FR3 最新構成への互換は未確認。[論文][multi-paper]、[README][multi]、[履歴][multi-log] |
| `hucebot/multipanda_ros2` | 上記と同じ名前の派生。history 先頭は **2026-03-26**。Panda + Humble + MuJoCo の構成を記載し、`custom_cartesian_impedance_controller` は `/cartesian_impedance/equilibrium_pose` を受ける。simulation の Cartesian command interface は未対応と記載。外部 Cartesian impedance が effort を使う経路とは区別する。[README][hucebot]、[履歴][hucebot-log] |

採用案は、まず公式 Cartesian impedance 例で目的を満たせるか確認し、追加の wrench、trajectory、複数腕・sim 共用が必要なら community 実装を比較すること。repository 名だけで選ばず、plugin type、入力 topic、動力学補償、依存・機体世代、更新履歴を比較する。[公式例][cart-code]、[community][community]、[multipanda][multi]

## 8. GELLO / VLA 推論との接続例

### GELLO: 公開された ROS 2 の接続

`wuphilipp/gello_software/ros2` は **GELLO → `/gello/joint_states`（JointState）→ `franka_fr3_arm_controllers` の JointImpedanceController → トルク指令**という構成を説明する。Hand/Robotiq の制御は別 manager。serial port、joint signs、assembly offsets、namespace、robot IP を設定し、publisher、gripper、腕の順に起動する。起動時に follower が GELLO 姿勢へ同期するため、初期姿勢と入力の急変を確認する。[GELLO ROS 2][gello]

```bash
ros2 launch franka_gello_state_publisher main.launch.py config_file:=franka_gello_single.yaml
ros2 launch franka_gripper_manager franka_gripper_client.launch.py config_file:=example_fr3_config_franka_hand.yaml
ros2 launch franka_fr3_arm_controllers franka_fr3_arm_controllers.launch.py robot_config_file:=example_fr3_config.yaml
```

上記は同 README の起動経路であり実行未検証。Dev Container はリポジトリ全体ではなく **`ros2` サブフォルダ**を開く。USB latency timer と serial 接続は FCI Ethernet とは別の遅延要因として切り分ける。[GELLO ROS 2][gello]

Jazzy での収集基盤例には Franka 公式 **LABS** があり、FR3 Duo、GELLO、カメラを統合し、MCAP 記録から LeRobot v2.1 へ export する。README は prototype と破壊的変更を明記する。これを完成済み VLA 推論・実機実行システムとは扱わない。[LABS][labs]

### VLA: 公開シミュレーション例と実機への設計案

`kalaiselvan-t/openvla-fr3` は **ROS 2 Humble + Gazebo + MoveIt + Servo + OpenVLA** の統合を公開し、`ros2 launch franka_openvla fr3.launch.py` を入口とする。README は VLA-Servo bridge と推論 node を列挙する。**作者が説明するシミュレーション統合例**であり、本調査での再現、実機 franka_ros2 接続、成功率、推論速度は未確認。LIBERO 用モデルの正規化・camera・action 分布が実機にも適合するとは判断しない。[公開例][vla-example]

OpenVLA 本体には REST API serving の実装があるため、推論を別 PC に置く接続経路は用意できる。ただし、これ自体は franka_ros2 adapter ではない。[OpenVLA][openvla]、[deploy.py][deploy]

実機接続の設計案は次のいずれか。全体の動作実績を示すものではない。[OpenVLA serving][deploy]、[Servo][servo]、[公式 Cartesian impedance][cart-code]

1. **VLA → action adapter → Servo → 関節 controller → FCI**。差分位置と速度の区別、action 継続時間、基準 frame、回転表現、gripper 値を明示する。Servo の status と入力 timeout に応じて停止する設計にする。
2. **VLA → action adapter → 平衡姿勢 → Cartesian impedance → effort → FCI**。モデル出力を robot base に変換し、目標の更新量を制限する。外部入力で動く設定と demo の周期運動を区別し、入力断時の動作を実装・試験する。

両案とも、モデル推論を RT `update()` に入れず、時刻付き command と期限切れ判定を備えた非 RT / RT 間の受け渡しを作る。観測には joint state、EE pose、画像時刻を揃え、action の単位、絶対/相対、座標系、正規化キー、control period を実験記録に残す。この部分は本メモの設計提案であり、VLA 一般の標準化済み interface ではない。[公式 RT 注意事項][trouble]、[OpenVLA][openvla]

## 9. 論文候補と未確認事項

`candidates.tsv` は **ページで実在・ID を確認した 3 件**を収録する。`year` は arXiv 初回公開年、venue は確認できたものだけを記載する。PDF URL は閲覧ページのリンク先として記録し、ローカル PDF は保存していない。GELLO と OpenVLA の会議採録先はこの調査では未確認のため推測しない。[multipanda 論文][multi-paper]、[GELLO 論文][gello-paper]、[OpenVLA 論文][openvla-paper]

未確認: 全 Issue の頻度統計、各 community package と最新 Jazzy の完全互換、Isaac Sim と Franka 固有 semantic interfaces の網羅的互換、VLA 実機推論の遅延・成功率、対象機の NIC/CPU 最適値。本メモは一次情報の照合結果であり、実機受入試験の代替ではない。

## 出典 URL

[readme]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/README.md
[compat-j]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_ros2/doc/compatibility_matrix.rst
[compat-h]: https://github.com/frankarobotics/franka_ros2/blob/humble/franka_ros2/doc/compatibility_matrix.rst
[release-j]: https://github.com/frankarobotics/franka_ros2/releases/tag/v3.6.1
[release-h]: https://github.com/frankarobotics/franka_ros2/releases/tag/v2.7.1
[robot-compat]: https://franka.de/fr3-compatibility-matrix
[compose]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/docker-compose.yml
[bringup]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_bringup/doc/index.rst
[hardware]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_hardware/doc/index.rst
[semantic]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_semantic_components/doc/index.rst
[examples]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_example_controllers/doc/index.rst
[controllers]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_bringup/config/controllers.yaml
[cart-code]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_example_controllers/src/fr3/cartesian_impedance_example_controller.cpp
[joint-code]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_example_controllers/src/fr3/joint_impedance_example_controller.cpp
[changes]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/CHANGELOG.rst
[custom]: https://control.ros.org/jazzy/doc/ros2_controllers/doc/writing_new_controller.html
[cli]: https://control.ros.org/jazzy/doc/ros2_control/ros2controlcli/doc/userdoc.html
[moveit]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_fr3_moveit_config/doc/index.rst
[servo]: https://moveit.picknik.ai/main/doc/examples/realtime_servo/realtime_servo_tutorial.html
[servo-h]: https://moveit.picknik.ai/humble/doc/examples/realtime_servo/realtime_servo_tutorial.html
[gazebo]: https://github.com/frankarobotics/franka_ros2/blob/jazzy/franka_gazebo/franka_gazebo_bringup/doc/index.rst
[classic]: https://github.com/ros-controls/gazebo_ros2_control/blob/master/doc/index.rst
[isaac]: https://docs.isaacsim.omniverse.nvidia.com/6.0.0/ros2_tutorials/tutorial_ros2_moveit.html
[isaac-api]: https://docs.isaacsim.omniverse.nvidia.com/6.2.0/py/index.html
[usd]: https://github.com/frankarobotics/franka_simulation
[rt]: https://frankarobotics.github.io/docs/doc/libfranka/docs/real_time_kernel.html
[net]: https://frankarobotics.github.io/docs/doc/libfranka/docs/system_requirements.html
[trouble]: https://frankarobotics.github.io/docs/troubleshooting.html
[nic]: https://cdn.kernel.org/doc/html/latest/networking/device_drivers/ethernet/intel/i40e.html
[ethtool]: https://man.archlinux.org/man/ethtool.8
[issues]: https://github.com/frankarobotics/franka_ros2/issues
[i103]: https://github.com/frankarobotics/franka_ros2/issues/103
[i218]: https://github.com/frankarobotics/franka_ros2/issues/218
[i243]: https://github.com/frankarobotics/franka_ros2/issues/243
[i248]: https://github.com/frankarobotics/franka_ros2/issues/248
[i249]: https://github.com/frankarobotics/franka_ros2/issues/249
[i250]: https://github.com/frankarobotics/franka_ros2/issues/250
[i53]: https://github.com/frankarobotics/franka_ros2/issues/53
[lib-i241]: https://github.com/frankarobotics/libfranka/issues/241
[community]: https://github.com/matthias-mayr/Cartesian-Impedance-Controller
[community-log]: https://github.com/matthias-mayr/Cartesian-Impedance-Controller/commits
[lucas]: https://github.com/LucasG2001/cartesian_impedance_control
[lucas-log]: https://github.com/LucasG2001/cartesian_impedance_control/commits
[multi]: https://github.com/tenfoldpaper/multipanda_ros2
[multi-log]: https://github.com/tenfoldpaper/multipanda_ros2/commits
[hucebot]: https://github.com/hucebot/multipanda_ros2
[hucebot-log]: https://github.com/hucebot/multipanda_ros2/commits
[gello]: https://github.com/wuphilipp/gello_software/blob/main/ros2/README.md
[labs]: https://github.com/frankarobotics/labs
[vla-example]: https://github.com/kalaiselvan-t/openvla-fr3
[openvla]: https://github.com/openvla/openvla
[deploy]: https://github.com/openvla/openvla/blob/main/vla-scripts/deploy.py
[multi-paper]: https://arxiv.org/abs/2602.02269
[gello-paper]: https://arxiv.org/abs/2309.13037
[openvla-paper]: https://arxiv.org/abs/2406.09246
