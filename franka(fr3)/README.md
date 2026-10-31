# Franka Research 3 (FR3) 資料集

調査日: 2026-10-31。Franka Robotics の Research 3 と、その研究利用に関する資料をまとめたフォルダです。

## 主な仕様

出典はデータシート R02212 v2.6 (2026 年 7 月、Arm v2.1 / v2.2、Control v5.1) です。データシートは Arm の版ごとに分かれているので、手元の機体の版と合わせて確認してください。

| 項目 | 値 |
|---|---|
| 自由度 | 7 |
| 定格可搬重量 | 3 kg |
| 最大リーチ | 855 mm |
| 力覚 | 全 7 軸にリンク側トルクセンサ |
| 関節可動範囲 (deg) | A1 ±166 / A2 ±105 / A3 ±166 / A4 -176〜-7 / A5 ±165 / A6 25〜265 / A7 ±175 |
| 関節トルク上限 | A1-A4 ±87 Nm / A5-A7 ±12 Nm |
| 関節速度上限 | A1-A4 150 deg/s / A5-A7 301 deg/s (FCI 利用時の A6 は 239 deg/s) |
| TCP 速度 | 最大 2 m/s |
| 繰り返し位置精度 | ±0.1 mm 未満 (ISO 9283) |
| アーム重量 | 約 18.3 kg |
| 外部制御 | Franka Control Interface (FCI)、1 kHz |

注: 実験に使う前に、Product Manual と `docs/fci/robot_specifications.rst.txt` の制限値も確認してください。データシートの脚注には「System Image 5.10 未満では SLP-C / SLS-C 設定中は FCI で制御できない」とあります。

## FCI の要点

出典は `docs/fci/libfranka/docs/system_requirements.rst.txt` です。

- ワークステーションは PREEMPT_RT カーネルの Linux が最低要件です。
- PC は Control の LAN ポートへ接続します。Arm の LAN ポートには接続しません。スイッチを挟まない直結が推奨です。
- RTT、制御ループの実行時間、ロボット側の処理時間の合計を 1 ms 未満に収める必要があります。
- 1 ms を超えたパケットは破棄され、20 回連続で破棄されると `communication_constraints_violation` で停止します。
- NVIDIA ドライバは PREEMPT_RT カーネルでは公式サポート外です。GPU で方策を推論する場合は、制御 PC と推論 PC を分ける構成を検討してください (同文書 `real_time_kernel.rst.txt`)。

## 互換性

| libfranka | ロボットのシステムバージョン | Robot / Gripper Server |
|---|---|---|
| >= 0.18.0 | >= 5.9.0 | 10 / 3 |
| >= 0.15.0 | >= 5.7.2 | 9 / 3 |
| >= 0.14.1 | >= 5.7.0 | 8 / 3 |
| >= 0.13.3 | >= 5.5.0 | 7 / 3 |

最新の libfranka は 0.21.3 (2026-07-30) です。詳しくは `docs/fci/libfranka/docs/compatibility_matrix.rst.txt` と [公式の互換性表](https://franka.de/FR3-compatibility-matrix) を参照してください。

## AI Companion について

Franka AI Companion (Jetson Orin NX 搭載の小型コンピュータ) は、[公式の資料一覧](https://franka.de/documents) で **End of Life** と表記されています (2026-10-31 確認)。製品ページには見積フォームが残っていますが、新規購入や保守の継続は保証されません。導入を検討する場合は、先に Franka か代理店へ確認してください。OS の記載はマニュアル (Ubuntu 20.04) と MATLAB Toolbox の対応表 (22.04) で異なり、現行の配布版は未確認です。

## 保存した資料

- `docs/official_pdf/`: 公式 PDF 31 本。データシート、Product / Hardware / Operating Manual、Franka Hand、FR3 Duo、GELLO、ESD、穴あけ図面など。**日本語版は `Hardware Manual Franka Research 3_Armv2.0_R02210_1.0_JA.pdf`** です。
- `docs/fci/`: FCI と libfranka の公式ドキュメントのソース。
- `docs/repos/`: libfranka と franka_description の README と CHANGELOG。
- `*.pdf`: Franka を主題にした論文、または Franka の同定や制御に踏み込んだ論文。
- `_catalog.csv`: 論文の全候補。

## 出典

- [Franka 公式ドキュメント配布ページ](https://franka.de/documents)
- [FCI ドキュメント](https://frankarobotics.github.io/docs/)
- [libfranka リポジトリ](https://github.com/frankarobotics/libfranka)
- 動力学同定の定番論文: Gaz et al., "Dynamic Identification of the Franka Emika Panda Robot With Retrieval of Feasible Parameters Using Penalty-Based Optimization", IEEE RA-L 2019 ([著者稿 PDF](https://iris.uniroma1.it/bitstream/11573/1356777/2/Gaz_Postprint_Dynamic-Identification_2019.pdf))。対象は FR3 ではなく Panda なので、FR3 にそのまま流用できるとは限りません。

## 詳細ノート

Sonnet、Codex、Cursor に分担して作成しました。出典と「未確認」の区別はノート内に記載しています。

- `notes/practical_addendum.md`: Arm v2.2、FCI の契約条件、AI Companion の製品状態と OS、国内の見積窓口
- `notes/practical.md`: Panda との違い、動力学、シミュレーションモデル、Python 制御の比較、不具合と対処、構成例、国内窓口

## 収集状況

- 候補論文: 548 本 (`_catalog.csv`)
- 論文の本文 (.md): 30 本
- 手元に残した論文 PDF: 0 本
- フォルダ全体: 0.19 GB
