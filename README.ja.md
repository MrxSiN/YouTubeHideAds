<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · **日本語** · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**YouTube の広告を取り除く Xposed モジュールです。判断はすべて Brainfuck、それ以外は XAX で書かれています。本当です。**

広告、スポンサー付きショート、プロモーションは YouTube が表示する前に取り除かれ、SponsorBlock のセグメントはスキップされます。

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#必要環境)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!NOTE]
> YouTube はほぼ毎回のアップデートで難読化されたクラスの名前を変えます。モジュールは起動のたびに構造から対象を見つけ直します。役割が見つからない、または一意に決まらない場合は、推測せずにその機能を何も変更しません。実際に試した環境は[互換性](#互換性)の表をご覧ください。

## なぜ Brainfuck？ XAX とは？

- **判断は Brainfuck。** このコンポーネントは広告か、Premium の宣伝を消してよいか、プレーヤーをスポンサー部分の終わりまで進めてよいか、スワイプは明るさの変更か。Brainfuck は Android、Xposed、DexKit、JNI を呼び出せず、バイトを読んで書くだけです。ホストは完全に正しい応答を受け取ったときだけ動作します。
- **それ以外はすべて XAX。** フック、DexKit による探索、リフレクション、設定ページ、SponsorBlock の HTTPS と JSON は、1 つの正規の [XAX](https://github.com/MrxSiN/XAX) セマンティック ストアにまとまっています。外部の XAX コンパイラが DEX に変換し、APK に署名します。このリポジトリには Java、Kotlin、C、Python、シェルのアプリ ソースはありません。

遅くもありません。9 つのポリシーは [BBC](https://github.com/MrxSiN/BBC) で事前に AArch64 共有ライブラリへコンパイルされます。APK にインタプリタはありません。

|  | |
|---|---|
| 🧹 **隠すのではなく取り除く** | 広告コンポーネントは YouTube が配置する前に置き換えられ、スポンサー付きショートはプレーヤーが作られる前にフィードから外れるので、空白や止まった動画が残りません。 |
| ⏭️ **SponsorBlock を内蔵** | 再試行とキャッシュを制限したプレフィックス検索、カテゴリごとの動作と色、手動スキップと取り消し、セグメントの作成と投票、除外、統計、設定の移行。 |
| 🔎 **名前の変更に強い** | DexKit が起動のたびに構造からすべてのフックを探します。役割が欠けているか一意でなければ、その機能には何もインストールしません。 |
| 🧠 **ポリシーは Brainfuck、しかもコンパイル済み** | 手書きの 9 つのプログラムをネイティブ コードにコンパイル。ポリシーと SponsorBlock の操作は起動のたびにチェックされます。 |
| 🛟 **失敗したら止める** | セルフチェックに失敗した機能はオフのまま。ネットワーク エラーや不明な再生タイプではシークしません。 |
| ⚙️ **ネイティブな見た目の設定** | **マイページ → 設定** の「アカウント」の上に専用の **YouTubeHideAds** セクション。YouTube 自身の行を使い、スイッチはすべて独立。「互換性と診断」ページもあります。 |
| 🎛️ **プレーヤーになじむ SponsorBlock** | 自動再生の横の SponsorBlock アイコンから、設定の歯車と同じフローティング メニューが開きます。セグメントはシークバーに色付きで表示されます。 |
| 📱 **すっきりしたショート** | ショートのボタンやパネルを個別に非表示にでき、ショート フィードのライブ配信を飛ばせます。 |
| 👆 **ひと目でわかるスワイプ操作** | 左で明るさ、右で音量。アイコン、レベル、数値の入ったピルで表示します。 |
| 🌐 **あなたの言語で** | YouTube の言語に従います：English、简体中文、繁體中文、Español、Português、Русский、日本語、한국어、Bahasa Indonesia、Bahasa Melayu。 |

---

## 取り除くもの

| グループ | 設定 | 既定 |
|---|---|---|
| 広告 | 動画とショートの広告 · フィードと検索の広告 · Premium のプロモーション · 全画面のプロモーション | オン（**広告を非表示** のマスタースイッチ配下） |
| SponsorBlock | スポンサー、自己宣伝 | オン |
| SponsorBlock | アクションの呼びかけ、イントロ、エンディング、予告、フィラー、音楽以外の部分 | オフ |
| コンテンツ | Playables（ゲームの棚、カード、探索の入口） | 非表示 |
| フィード | プレビュー動画 · 他のトピックを見る · 投稿 | 非表示 |
| フィード | フィードのショート | 表示 |
| フィード | AI チャンネル · AI の可能性があるチャンネル（[AiSList](https://github.com/Override92/AiSList)） | オフ |
| プレーヤー | スワイプで明るさ（左）· スワイプで音量（右）、全画面のみ | オン |
| プレーヤー | 多言語の動画で元の音声を優先 | オン |
| プレーヤー | バックグラウンド再生（子ども向け動画を含む） | オン |
| ショート | 高評価、コメント、共有、リミックス、保存、サウンド、登録、タイトル、おすすめと情報パネル、一時停止中のボタン | 表示（それぞれ非表示にできます） |
| ショート | ライブのショートをスキップ | オフ |

**広告を非表示** をオフにしてもコンテンツやプレーヤーの機能はオフになりません。フィードのスイッチを変えたらフィードを再読み込みしてください。元の音声は次のトラック リストから適用され、手動の選択を尊重します。全項目は[設定と既定値](docs/README.md#settings-and-defaults)。バックグラウンド再生は「広告を非表示」や SponsorBlock とは独立しています。変更後は YouTube を再起動してください。[実装とテスト済みの制限](docs/BACKGROUND_PLAYBACK.md)。

<details open>
<summary><b>🧱 どこで取り除くか</b></summary>
<br>

| 対象 | 場所 | 内容 |
|---|---|---|
| **動画広告** | プレーヤーの広告開始と広告レイアウト | Brainfuck が構造上の広告の特徴と安全な遷移を確認したときに広告枠を抑止します。 |
| **フィード、検索、ショッピングの広告** | DexKit で見つけたコンポーネント パーサー | 確認された有料コンポーネントを YouTube 自身の空のコンポーネントに置き換えます。 |
| **スポンサー付きショート** | ショートの応答、挿入、プレーヤーの初期データ | プレーヤーができる前に、動画・画像の広告項目をトラッキング データごと取り除きます。 |
| **Premium、全画面、パネル** | オファー表示、全画面ダイアログ、型付き識別子によるエンゲージメント パネル | 特典や定期購入の管理には触れずに宣伝面を非表示にします。 |
| **フィードのセクション、Playables、AI チャンネル、ショートの要素** | 同じコンポーネント フック | 一致したセクション、カード、ボタンだけを取り除きます。チャンネルの行や再生リストは残ります。 |
| **SponsorBlock** | プレーヤーのシーク/再生時間のブリッジとネイティブのシークバー | 制限付きのプレフィックス検索、カテゴリの動作、色付きマーク、手動操作、明示的なコミュニティ操作。 |

</details>

---

## 状況

**v1.1.0**（versionCode 153）は 1.0.0 以来の最初のリリースです。バックグラウンド再生、YouTube の設定内の専用セクション、「互換性と診断」ページ、YouTube 風の SponsorBlock 操作、ショートの要素の非表示、ライブのショートのスキップ、新しいスワイプ操作、さらに 9 言語を追加しました。スマートフォンでの負荷も大きく下がりました。Brainfuck のポリシー呼び出しは APK を開き直さなくなり、DexKit の結果はキャッシュされるため、初回以降は YouTube が約 0.35 秒早く開きます。[端末での確認](evidence/device_perf_20261028/README.md)。

2 つのリリースの間の開発ビルド（111〜153）は[変更履歴](CHANGELOG.md)に、それぞれの証拠は [evidence](evidence/README.md) にあります。

### 互換性

Pixel 8 Pro（Android 17、Vector 2.2、libxposed API 102）で確認しています。ほかの構成で試したら、行を追加する pull request をお願いします。

| YouTube | モジュール | 状態 |
|---|---|---|
| 21.42.243 | 1.1.0 | ✅ 動作 |
| 21.41.525 | 1.0.0 | ✅ 動作 |

### 既知の制限

- Premium、全画面、エンゲージメント パネルのプロモーションは、制御したフック テストでしか除去を確認していません。実際の配信例はまだ見ていません。
- プレビュー動画と「他のトピックを見る」の棚は英語の見出しでのみ判定します。
- AI チャンネルのリストはコミュニティが管理しており誤判定がありうるため、既定でオフです。
- バックグラウンド再生はスイッチを変えたあと YouTube の再起動が必要で、ショートは YouTube の動作のままです。Bluetooth 操作と着信による中断は未確認です。
- SponsorBlock の送信と投票は本番サーバーでは試していません。[機能と制限](docs/SPONSORBLOCK_API_RESEARCH.md)をご覧ください。
- ライブのショートのスキップはまだ実際のライブ ショートに出会っていません。この機能、スワイプのピル、YouTube の言語切り替えは開発用プローブで確認しました。
- モジュールのページはダーク テーマでのみ確認しました。ライト テーマ、タブレット、右から左のレイアウトは未確認です。
- YouTube またはモジュールの更新後の最初の起動ではフックのキャッシュを作り直すため、約 0.4 秒遅くなります。
- arm64-v8a のみ。上の構成と YouTube バージョン以外は試していません。LSPatch も未確認です。

詳細：[機能の対応範囲](docs/FEATURE_COVERAGE.md)と[互換性](docs/COMPATIBILITY.md)。

## 必要環境

| | |
|---|---|
| **Android** | 9.0（API 28）以降、arm64 |
| **アプリ** | YouTube（`com.google.android.youtube`） |
| **フレームワーク** | [Vector](https://github.com/JingMatrix/Vector) または libxposed API 102 対応の LSPosed |
| **Root** | Vector/LSPosed に必要。モジュール自体は権限を要求しません |

## インストール

```
1. Releases または Xposed モジュール リポジトリから APK をインストール
2. Vector または LSPosed で YouTubeHideAds を有効にし、スコープを YouTube に
3. YouTube を一度強制停止してから開く
```

[GitHub Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) または [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads) から入手できます。設定は **YouTube → マイページ → 設定 → YouTubeHideAds** にあります。設定と AI のキャッシュは YouTube 自身のデータに保存されるため、YouTube のデータを消去するとリセットされます。

フレームワークのログでは `YouTubeHideAds:` で始まる行で動作を確認できます。

```text
Ad policy self-check passed (70 cases)
SponsorBlock self-check passed (277 cases)
Ad component hook installed
Shorts feed removal hooks installed (paired, insert, response, restore, seed)
Video ad suppressed
```

---

## 仕組み

```
YouTube process
  XAX module (DEX) ──────────────► Bfp1Bridge.run ──JNI──► lib<policy>.so
  hooks, DexKit roles               input bytes            nine AOT Brainfuck policies
  settings page, HTTPS/JSON              ▲                       │
  typed actions                          │   exact reply only    │
                                         └───────────────────────┘
```

コードの置き場所を決めるルールは 1 つです：**YouTube、Android、ネットワーク、JNI に触れるものは XAX が行い、XAX が見つけたものに対して動くかどうかは Brainfuck が決める。** ポリシー ライブラリ、バイト配置、フック探索の詳細は [`docs/BRAINFUCK_ABI.md`](docs/BRAINFUCK_ABI.md) と [`docs/DEXKIT_RESOLUTION.md`](docs/DEXKIT_RESOLUTION.md) にあります。

セグメントの自動取得では、動画 ID の SHA-256 の先頭 4 桁（16 進数）だけを送ります。応答サイズ、レコード数、タイムアウトには上限があり、リダイレクトは無効です。手動の送信や投票では、選んだサーバーに必要なデータとプライベート ID を送ります。視聴の報告は既定でオフ、設定のエクスポートは既定でプライベート ID を含みません。

---

## ビルド

このリポジトリにビルド スクリプトはありません。リリースは外部ツールでビルドします。

```text
BBC          source/**/*.bf  ->  lib<policy>.so (AArch64)
AAPT2        source/branding ->  branding.apk (static resources only)
XAX          source/xax/youtubehideads.xax + pinned inputs -> signed APK
```

すべての入力はストア内で BLAKE3 により固定されているため、入力が一致しなければビルドは失敗します。再ビルドには Android libxposed プロファイル付きの [XAX](https://github.com/MrxSiN/XAX)（コミット `3cca599` または互換の branding-v2 スナップショット）を使います。手順は [`docs/BUILD.md`](docs/BUILD.md) にあります。

## トラブルシューティング

| 問題 | 対処 |
|---|---|
| モジュールのログが出ない | モジュールが YouTube をスコープにして有効か確認し、YouTube を強制停止します。 |
| 更新直後の `UnsatisfiedLinkError` | インストールの完了を待ってから YouTube を強制停止し、開き直します。 |
| セルフチェックが `false` | その機能はオフのままです。`YouTubeHideAds:` のログ行を報告してください。 |
| フィードのスイッチが効かない | フィードを再読み込みしてください。新しく読み込まれたコンポーネントに適用されます。 |
| YouTube の更新後に動かない | 内部クラスが変わった可能性があります。YouTube のバージョンと一緒にログを報告するか、「互換性と診断」のレポートをコピーしてください。 |

## クレジット

[DexKit](https://github.com/LuckyPray/DexKit)、[libxposed API](https://github.com/libxposed/api)、[Vector](https://github.com/JingMatrix/Vector)、[LSPosed](https://github.com/LSPosed/LSPosed)、[XAX](https://github.com/MrxSiN/XAX)、[XAX-MCP](https://github.com/MrxSiN/XAX-MCP)、[BBC](https://github.com/MrxSiN/BBC)、[SponsorBlock](https://sponsor.ajay.app)、[Override92/AiSList](https://github.com/Override92/AiSList)、[Morphe Patches](https://github.com/MorpheApp/morphe-patches)（[保持している通知](LICENSES/Morphe-NOTICE.txt)）。新たに書かれたプロジェクト素材は GPL-3.0-or-later です。第三者の条件は [NOTICE](NOTICE) をご覧ください。

## 免責事項

Google LLC や YouTube とは関係がなく、承認や後援も受けていません。教育および個人利用のために提供しています。YouTube の更新により、予告なくフックが動かなくなることがあります。
