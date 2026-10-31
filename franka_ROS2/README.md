# franka_ros2 資料集

調査日: 2026-10-31。FR3 を ROS 2 で動かすための公式ドキュメントと、ROS 2 の実時間性などに関する論文をまとめたフォルダです。

## 現在のバージョン

| 系列 | 最新 | OS | 必要な依存 |
|---|---|---|---|
| Jazzy | v3.6.1 (2026-10-27) | Ubuntu 24.04 | libfranka >= 0.20.4、franka_description >= 2.9.0 |
| Humble | v2.7.1 (2026-09-01) | Ubuntu 22.04 | `docs/humble/repo_CHANGELOG.rst` を参照 |

注: 公式の互換性表 (`docs/jazzy/franka_ros2/doc/compatibility_matrix.rst.txt`) は v3.4.0 までの記載で止まっています。v3.5 以降の要件は `docs/jazzy/repo_CHANGELOG.rst` の各リリース見出しで確認してください。

## 使い始める前に

- 公式 README は Docker での利用を推奨しています。ローカルビルドでは多数の依存が入り、競合の原因になるためです。
- Windows は公式サポート外です。
- README は「開発が速く、破壊的変更がありうる」と明記しています。更新前に CHANGELOG を確認してください。
- 1 kHz の通信要件は FCI と同じです。詳しくは `../franka(fr3)/README.md` の「FCI の要点」を参照してください。

## 最近の変更で注意する点

v3.6.1 の CHANGELOG から、既存のコードに影響しうるものを抜き出しました。

- `FrankaRobotState` の配列サイズが、説明ファイル全体の回転関節数ではなく、対象アームの関節から決まるようになりました。7 個を超える回転関節がある構成では、それまで範囲外のデータを読んでいました。
- `FrankaRobotState` のフレーム ID の解決方法が変わりました。単腕の標準起動では、ベース座標系のフレーム ID が `base` から `<arm>_link0` に変わります。`~/current_pose` などの簡易トピックにも影響します。
- `FrankaHardwareInterface::read()/write()` は、コマンドモード切り替え中にブロックせず、そのサイクルをスキップするようになりました。
- 説明ファイルに必要な関節やリンクが無い場合、コンポーネントの生成時などに拒否されるようになりました。

## 保存した資料

- `docs/jazzy/`、`docs/humble/`: 公式ドキュメントのソースと、リポジトリの README、CHANGELOG。bringup、example controllers、MoveIt 設定、Gazebo、gripper、hardware などの各パッケージを含みます。
- `*.pdf`: ROS 2 の実時間性や遅延解析、ros2_control、MoveIt、マニピュレータ統合に関する論文。
- `_catalog.csv`: 論文の全候補。

## 関連リソース

- [franka_ros2 リポジトリ](https://github.com/frankarobotics/franka_ros2) と [リリース一覧](https://github.com/frankarobotics/franka_ros2/releases)
- [FCI ドキュメント](https://frankarobotics.github.io/docs/) と [トラブルシューティング](https://frankarobotics.github.io/docs/troubleshooting.html)
- [FR3 互換性表](https://franka.de/FR3-compatibility-matrix)
- [NVIDIA Isaac ROS の franka_fr3_ros2_control](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_robots/franka_fr3_ros2_control/index.html): 専用の SCHED_FIFO スレッドで 1 kHz ループを回し、PREEMPT_RT なしで動かす構成の説明です。Franka 公式の要件とは異なるので、利用する場合は通信品質を実測してください。

## 詳細ノート

Sonnet、Codex、Cursor に分担して作成しました。出典と「未確認」の区別はノート内に記載しています。

- `notes/practical.md`: Jazzy と Humble の選択、実機接続、コントローラ、MoveIt、実時間調整、既知の不具合、GELLO や VLA との接続。実機と Docker での動作は未検証

## 収集状況

- 候補論文: 114 本 (`_catalog.csv`)
- 論文の本文 (.md): 39 本
- 手元に残した論文 PDF: 0 本
- フォルダ全体: 0.00 GB

## サーベイ、総説、チュートリアル

- 2025-12 [A Survey of Real-Time Support, Analysis, and Advancements in ROS 2](https://arxiv.org/abs/2601.10722) (本文あり)
