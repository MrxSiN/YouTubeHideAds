<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · **繁體中文** · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**一個移除 YouTube 廣告的 Xposed 模組：所有判斷都用 Brainfuck 撰寫，其餘部分用 XAX。**

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](README.md#install)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-EA4AAA?logo=githubsponsors&logoColor=fff&style=for-the-badge)](https://github.com/sponsors/MrxSiN)

<img src="docs/images/settings-ads.png" width="240" alt="Ads and SponsorBlock settings">
<img src="docs/images/settings-player.png" width="240" alt="Player settings">
<img src="docs/images/settings-feed.png" width="240" alt="Feed and blacklist settings">

</div>

## 功能

- **廣告在顯示之前就被移除：** 影片和 Shorts 廣告、動態和搜尋廣告、Premium 和全螢幕推廣，不留空白位置。
- **內建 SponsorBlock**，進度列上有彩色片段，播放器中有按鈕，可手動略過、投票和提交。
- **播放器：** 預設速度和畫質、偏好的字幕語言、背景播放、原始音訊、記住直播位置、點按跳轉、循環、速度按鈕，以及 Return YouTube Dislike 的不喜歡數。
- **手勢：** 全螢幕時左側滑動調亮度、右側滑動調音量，不會作用於直播聊天室、面板或「更多影片」面板。
- **動態：** 隱藏 Shorts 區塊、貼文、預覽、Playables 和 AI 頻道，頻道和關鍵字黑名單，以及 DeArrow 縮圖。
- **Shorts：** 可單獨隱藏按鈕和面板，並略過直播 Shorts。
- **一個設定頁面**，位於 **你 → 設定 → YouTube Hide Ads**，使用 YouTube 的語言（10 種語言）。

新增的附加功能預設關閉。所有設定及其預設值見[文件](docs/README.md#settings-and-defaults)。

## 安裝

1. 從 [Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) 或 [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads) 取得 APK。
2. 在 [Vector](https://github.com/JingMatrix/Vector) 或 LSPosed（libxposed API 102）中啟用，作用範圍選擇 YouTube。
3. 強制停止 YouTube，然後重新開啟。

需要 Android 9 或更新版本、arm64，框架需要 root。模組本身不要求任何權限。

## 相容性

| YouTube | 模組 | 狀態 |
|---|---|---|
| 21.45.88 | 1.3.0 (build 157) | ✅ 正常 |
| 21.43.523 | 1.2.0 | ✅ 正常 |
| 21.42.243 | 1.1.0 | ✅ 正常 |

在執行 Android 17 和 Vector 2.2 的 Pixel 8 Pro 上測試。YouTube 在大多數更新中會重新命名其內部類別。模組會依結構重新找到目標，找不到時會關閉該功能，而不是去猜。歷史：[變更記錄](CHANGELOG.md) · 詳情：[相容性](docs/COMPATIBILITY.md)。

## 已知限制

- HTTPS 過濾應用程式（如 AdGuard）可能會封鎖 SponsorBlock、更新檢查、不喜歡數和 DeArrow；見[下文](README.md#sponsorblock-or-update-check-never-connects)。
- DeArrow 只替換縮圖，不替換標題。套用預設速度後，YouTube 自帶的速度選單仍顯示 1x。
- 行動數據下的預設畫質、直播 Shorts 和自動字幕封鎖尚未在手機上測試。
- 只在一支手機的深色主題下檢查過。1.3.0 的新文字為英文。

所有已測試和未測試的內容：[功能涵蓋範圍](docs/FEATURE_COVERAGE.md)。

## 疑難排解

| 問題 | 嘗試 |
|---|---|
| 框架記錄中沒有 `YouTubeHideAds:` 行 | 確認 YouTube 在作用範圍內，然後強制停止它。 |
| 某個動態開關似乎無效 | 重新載入動態。 |
| YouTube 更新後失效 | 使用 **關於 → 相容性與診斷 → 回報問題**。 |

### SponsorBlock 或更新檢查始終無法連線

這同樣適用於不喜歡數和 DeArrow。記錄中會出現 `NOT_ENOUGH_SCTS`。某個 HTTPS 過濾應用程式正在重新簽署連線，而 YouTube 的
憑證透明度檢查拒絕了它。在 AdGuard 中，將以下項目加入 **HTTPS 過濾 → 排除項目**：
`sponsor.ajay.app`、`github.com`、`returnyoutubedislikeapi.com`、`dearrow-thumb.ajay.app`。然後重新啟動 YouTube。

## 運作方式

Brainfuck 負責判斷，XAX 負責執行。九個 Brainfuck 策略負責判斷，例如某個元件是不是
廣告、某次跳轉能否略過片段、某次觸控是不是滑動。它們由 [BBC](https://github.com/MrxSiN/BBC) 預先編譯為
AArch64。Hook、探索、設定和網路都在一個
[XAX](https://github.com/MrxSiN/XAX) 儲存中，編譯為 DEX。本儲存庫沒有 Java、Kotlin 或 C
應用程式原始碼。

[架構](docs/ARCHITECTURE_BRAINFUCK_XAX.md) · [建置](docs/BUILD.md) · [所有文件](docs/README.md) · [證據](evidence/README.md)

## 支持

如果這個模組對你有用，可以[贊助它的開發](https://github.com/sponsors/MrxSiN)。

## 致謝和授權

[DexKit](https://github.com/LuckyPray/DexKit)、[libxposed](https://github.com/libxposed/api)、
[Vector](https://github.com/JingMatrix/Vector)、[SponsorBlock](https://sponsor.ajay.app)、
[Return YouTube Dislike](https://returnyoutubedislike.com)、[DeArrow](https://dearrow.ajay.app)、
[AiSList](https://github.com/Override92/AiSList)（CC BY-NC 4.0，未內附），以及
[Morphe Patches](https://github.com/MorpheApp/morphe-patches)，用作行為參考
（[聲明](LICENSES/Morphe-NOTICE.txt)）。

GPL-3.0-or-later。見 [NOTICE](NOTICE) 和[上游來源](docs/UPSTREAM_PROVENANCE.md)。
本專案與 Google 或 YouTube 無關聯。
