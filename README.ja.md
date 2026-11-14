<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · **日本語** · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**YouTube の広告を取り除く Xposed モジュール。判断はすべて Brainfuck で書かれ、残りは XAX です。**

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](README.md#install)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-EA4AAA?logo=githubsponsors&logoColor=fff&style=for-the-badge)](https://github.com/sponsors/MrxSiN)

<img src="docs/images/settings-ads.png" width="240" alt="Ads and SponsorBlock settings">
<img src="docs/images/settings-player.png" width="240" alt="Player settings">
<img src="docs/images/settings-feed.png" width="240" alt="Feed and blacklist settings">

</div>

## 機能

- **広告は表示される前に取り除かれます:** 動画とショートの広告、フィードと検索の広告、Premium やフルスクリーンのプロモーション。空白の枠は残りません。
- **SponsorBlock を内蔵**。シークバーに色付きのセグメントを表示し、プレーヤーのボタンから手動スキップ、投票、送信ができます。
- **プレーヤー:** 既定の速度と画質、優先する字幕言語、バックグラウンド再生、オリジナル音声、ライブの再生位置の記憶、タップでシーク、ループ、速度ボタン、Return YouTube Dislike の低評価数。
- **ジェスチャー:** フルスクリーンで左側のスワイプは明るさ、右側は音量。ライブチャット、パネル、「その他の動画」シートの上では動作しません。
- **フィード:** ショートの棚、投稿、プレビュー、Playables、AI チャンネルの非表示、チャンネルとキーワードのブラックリスト、DeArrow のサムネイル。
- **ショート:** 個々のボタンやパネルを非表示にでき、ライブのショートをスキップします。
- **設定ページは 1 つ。** **マイページ → 設定 → YouTube Hide Ads** にあり、YouTube の言語で表示されます（10 言語）。

新しい追加機能は既定でオフです。すべての設定と既定値は[ドキュメント](docs/README.md#settings-and-defaults)に載っています。

## インストール

1. [Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) または [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads) から APK を入手します。
2. [Vector](https://github.com/JingMatrix/Vector) または LSPosed（libxposed API 102）で有効にし、スコープに YouTube を指定します。
3. YouTube を強制停止してから、もう一度開きます。

arm64 の Android 9 以降と、フレームワーク用の root が必要です。モジュール自体は権限を一切要求しません。

## 互換性

| YouTube | モジュール | 状態 |
|---|---|---|
| 21.45.88 | 1.3.0 (build 157) | ✅ 動作 |
| 21.43.523 | 1.2.0 | ✅ 動作 |
| 21.42.243 | 1.1.0 | ✅ 動作 |

Android 17 と Vector 2.2 の Pixel 8 Pro で確認しています。YouTube はほとんどの
アップデートで内部クラス名を変えます。モジュールは構造からもう一度対象を見つけ、見つからないときは
推測せずにその機能をオフにします。履歴: [変更履歴](CHANGELOG.md) · 詳細: [互換性](docs/COMPATIBILITY.md)。

## 既知の制限

- AdGuard など HTTPS をフィルタリングするアプリは、SponsorBlock、更新チェック、低評価数、DeArrow をブロックすることがあります。[下記](README.md#sponsorblock-or-update-check-never-connects)を参照してください。
- DeArrow が置き換えるのはサムネイルで、タイトルではありません。既定の速度を適用しても、YouTube 自身の速度メニューは 1x のままです。
- モバイルデータでの既定画質、ライブのショート、自動字幕のブロックは、実機では未確認です。
- 確認したのはダークテーマで、1 台のスマートフォンだけです。1.3.0 の新しい文言は英語です。

確認済みの内容と未確認の内容のすべて: [機能の確認範囲](docs/FEATURE_COVERAGE.md)。

## トラブルシューティング

| 問題 | 対処 |
|---|---|
| フレームワークのログに `YouTubeHideAds:` の行がない | YouTube がスコープに入っているか確認し、強制停止してください。 |
| フィードのスイッチが効いていないようだ | フィードを再読み込みしてください。 |
| YouTube の更新後に動かない | **概要 → 互換性と診断 → 問題を報告** を使ってください。 |

### SponsorBlock や更新チェックがいつまでも接続できない

低評価数と DeArrow にも当てはまります。ログに `NOT_ENOUGH_SCTS` が出ます。HTTPS をフィルタリングするアプリが接続に再署名していて、YouTube の
証明書の透明性チェックがそれを拒否しています。AdGuard では、**HTTPS フィルタリング → 除外** に次を追加してください:
`sponsor.ajay.app`、`github.com`、`returnyoutubedislikeapi.com`、`dearrow-thumb.ajay.app`。その後、YouTube を再起動します。

## 仕組み

判断するのが Brainfuck、実行するのが XAX です。9 つの Brainfuck ポリシーが、たとえばコンポーネントが
広告かどうか、シークでセグメントをスキップしてよいか、タッチがスワイプかどうかを判断します。これらは
[BBC](https://github.com/MrxSiN/BBC) で事前に AArch64 にコンパイルされます。フック、探索、設定、ネットワークは 1 つの
[XAX](https://github.com/MrxSiN/XAX) ストアにまとまっていて、DEX にコンパイルされます。リポジトリには Java、Kotlin、C のアプリケーションソースはありません。

[アーキテクチャ](docs/ARCHITECTURE_BRAINFUCK_XAX.md) · [ビルド](docs/BUILD.md) · [すべてのドキュメント](docs/README.md) · [エビデンス](evidence/README.md)

## サポート

このモジュールが役に立ったら、[開発を支援](https://github.com/sponsors/MrxSiN)できます。

## クレジットとライセンス

[DexKit](https://github.com/LuckyPray/DexKit)、[libxposed](https://github.com/libxposed/api)、
[Vector](https://github.com/JingMatrix/Vector)、[SponsorBlock](https://sponsor.ajay.app)、
[Return YouTube Dislike](https://returnyoutubedislike.com)、[DeArrow](https://dearrow.ajay.app)、
[AiSList](https://github.com/Override92/AiSList)（CC BY-NC 4.0、同梱なし）、
動作の参考にした [Morphe Patches](https://github.com/MorpheApp/morphe-patches)
（[通知](LICENSES/Morphe-NOTICE.txt)）。

GPL-3.0-or-later。[NOTICE](NOTICE) と[アップストリームの出典](docs/UPSTREAM_PROVENANCE.md)を参照してください。
このプロジェクトは Google や YouTube とは関係ありません。
