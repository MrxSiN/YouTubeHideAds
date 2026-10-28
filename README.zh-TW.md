<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · **繁體中文** · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**一個移除 YouTube 廣告的 Xposed 模組：所有判斷都以 Brainfuck 撰寫，其餘部分使用 XAX。沒錯，是真的。**

廣告、贊助 Shorts 和宣傳內容會在 YouTube 顯示之前被移除，SponsorBlock 片段會自動略過。

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#系統需求)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!NOTE]
> YouTube 幾乎每次更新都會重新命名混淆後的類別。模組會在每次啟動時依結構重新尋找目標；如果某個角色缺失或不唯一，就不啟用該功能，而不是去猜測。實際測試過的環境請見[相容性](#相容性)表。

## 為什麼用 Brainfuck？XAX 又是什麼？

- **Brainfuck 負責判斷。** 這個元件是不是廣告、Premium 行銷能否移除、播放器能否跳到贊助片段結尾、某次滑動是否在調整亮度。Brainfuck 無法呼叫 Android、Xposed、DexKit 或 JNI，只能讀寫位元組；只有收到完全正確的回覆時，主程式才會執行動作。
- **其餘一切由 XAX 完成。** Hook、DexKit 搜尋、反射、設定頁面、SponsorBlock 的 HTTPS 和 JSON 都在一個標準的 [XAX](https://github.com/MrxSiN/XAX) 語意儲存區中。外部 XAX 編譯器將其編譯為 DEX 並簽署 APK。本存放區沒有 Java、Kotlin、C、Python 或 shell 應用程式原始碼。

它也不慢。九個策略由 [BBC](https://github.com/MrxSiN/BBC) 預先編譯為 AArch64 共用程式庫，APK 中沒有直譯器。

|  | |
|---|---|
| 🧹 **移除，而非隱藏** | 廣告元件在 YouTube 排版前就被取代，贊助 Shorts 在播放頁面建立前就被移出動態，因此不會留下空白或卡住的片段。 |
| ⏭️ **內建 SponsorBlock** | 前綴查詢（有限重試和快取）、類別模式和顏色、手動略過/復原、建立片段和投票、排除頻道、統計和設定轉移。 |
| 🔎 **不怕重新命名** | DexKit 每次啟動都依結構尋找所有 Hook。角色缺失或不唯一時，該功能不會安裝任何東西。 |
| 🧠 **策略以 Brainfuck 撰寫並編譯** | 九個手寫程式編譯為原生程式碼；每次啟動都會檢查封裝的策略和 SponsorBlock 控制項。 |
| 🛟 **失敗即關閉** | 自我檢查失敗時，該功能維持關閉。網路錯誤和未知播放類型絕不會跳轉。 |
| ⚙️ **原生風格的設定** | 在 **你 → 設定** 中擁有獨立的 **YouTubeHideAds** 區段，位於「帳戶」上方，使用 YouTube 自己的列樣式；每個開關各自獨立，另有「相容性與診斷」頁面。 |
| 🎛️ **融入播放器的 SponsorBlock** | 自動播放旁的 SponsorBlock 圖示會開啟與播放器設定齒輪相同的浮動選單；片段會在進度列上以顏色標示。 |
| 📱 **更清爽的 Shorts** | 可逐一隱藏 Shorts 的按鈕和面板，並略過 Shorts 動態中的直播。 |
| 👆 **一眼就懂的滑動控制** | 左側調整亮度，右側調整音量，以含圖示、進度和數值的膠囊顯示。 |
| 🌐 **你的語言** | 跟隨 YouTube 的語言：English、简体中文、繁體中文、Español、Português、Русский、日本語、한국어、Bahasa Indonesia 和 Bahasa Melayu。 |

---

## 移除內容

| 分組 | 設定 | 預設 |
|---|---|---|
| 廣告 | 影片和 Shorts 廣告 · 動態和搜尋廣告 · Premium 宣傳 · 全螢幕宣傳 | 開啟，受 **隱藏廣告** 總開關控制 |
| SponsorBlock | 贊助、自我宣傳 | 開啟 |
| SponsorBlock | 互動提醒、片頭、片尾、預告、填充內容、非音樂片段 | 關閉 |
| 內容 | Playables（遊戲區塊、卡片、探索入口） | 隱藏 |
| 動態 | 預覽影片 · 探索更多主題 · 貼文 | 隱藏 |
| 動態 | 動態中的 Shorts | 顯示 |
| 動態 | AI 頻道 · 疑似 AI 頻道（[AiSList](https://github.com/Override92/AiSList)） | 關閉 |
| 播放器 | 滑動調整亮度（左側）· 滑動調整音量（右側），僅限全螢幕 | 開啟 |
| 播放器 | 多語言影片強制使用原始音軌 | 開啟 |
| 播放器 | 背景播放，包括兒童專屬影片 | 開啟 |
| Shorts | 喜歡、留言、分享、混音、儲存、音訊、訂閱、標題、建議和資訊面板、暫停時的疊加按鈕 | 顯示（可逐項隱藏） |
| Shorts | 略過直播 Shorts | 關閉 |

關閉 **隱藏廣告** 不會停用內容和播放器功能。變更動態相關開關後請重新載入動態。原始音軌從下一個音軌清單開始生效，並尊重你的手動選擇。完整表格：[設定和預設值](docs/README.md#settings-and-defaults)。背景播放獨立於「隱藏廣告」和 SponsorBlock；變更該開關後請重新啟動 YouTube。[實作和測試限制](docs/BACKGROUND_PLAYBACK.md)。

<details open>
<summary><b>🧱 每項移除發生在哪裡</b></summary>
<br>

| 介面 | 位置 | 作用 |
|---|---|---|
| **影片廣告** | 播放器廣告啟動和廣告版面 | 當 Brainfuck 確認結構性廣告特徵且轉換安全時，抑制廣告位。 |
| **動態、搜尋和購物廣告** | 由 DexKit 找到的元件剖析器 | 以 YouTube 自己的空元件取代已確認的付費元件。 |
| **贊助 Shorts** | Shorts 回應、插入和播放頁初始資料 | 在播放頁存在之前，連同追蹤資料一起移除影片/圖片廣告項目。 |
| **Premium、全螢幕、面板** | 宣傳檢視、全螢幕對話框、依類型識別的互動面板 | 隱藏行銷介面，不影響權益或訂閱管理。 |
| **動態區塊、Playables、AI 頻道、Shorts 元件** | 同一個元件 Hook | 只移除符合的區塊、卡片或按鈕；頻道列和播放清單保留。 |
| **SponsorBlock** | 播放器跳轉/長度橋接和原生進度列 | 有限的前綴擷取、類別模式、彩色標記、手動控制和明確的社群操作。 |

</details>

---

## 狀態

**v1.1.0**（versionCode 153）是 1.0.0 之後的第一個正式版本。它加入背景播放、YouTube 設定中的獨立區段、「相容性與診斷」頁面、YouTube 風格的 SponsorBlock 控制項、隱藏 Shorts 元件、略過直播 Shorts、重新設計的滑動控制，以及另外九種語言。它在手機上也輕快得多：Brainfuck 策略呼叫不再重複開啟 APK，DexKit 結果會被快取，因此首次啟動之後 YouTube 開啟快約 0.35 秒。[裝置檢查](evidence/device_perf_20261028/README.md)。

兩個正式版本之間的開發版本（111 至 153）請見[更新記錄](CHANGELOG.md)，各自的證據請見 [evidence](evidence/README.md)。

### 相容性

在 Pixel 8 Pro（Android 17、Vector 2.2，libxposed API 102）上測試。試過其他環境？歡迎提交 PR 新增一列。

| YouTube | 模組 | 狀態 |
|---|---|---|
| 21.42.243 | 1.1.0 | ✅ 正常 |
| 21.41.525 | 1.0.0 | ✅ 正常 |

### 已知限制

- Premium、全螢幕和互動面板推廣只在受控 Hook 測試中移除過，尚未見到真實推送的案例。
- 預覽影片和「探索更多主題」欄目僅依英文標題比對。
- AI 頻道清單由社群維護，可能誤判頻道，因此預設關閉。
- 背景播放的開關變更後需要重新啟動 YouTube，Shorts 仍由 YouTube 自行處理。藍牙控制和來電中斷尚未測試。
- SponsorBlock 的提交和投票尚未在正式伺服器上試過。請見[功能和限制](docs/SPONSORBLOCK_API_RESEARCH.md)。
- 略過直播 Shorts 尚未遇到真實的直播 Short；它、滑動膠囊和 YouTube 語言切換都是用開發探針檢查的。
- 模組頁面只在深色主題下檢查過。淺色主題、平板和由右至左版面尚未測試。
- YouTube 或模組更新後的第一次啟動會重建 Hook 快取，大約慢 0.4 秒。
- 僅支援 arm64-v8a。只試過上面的環境和 YouTube 版本，尚未試過 LSPatch。

詳情：[功能涵蓋範圍](docs/FEATURE_COVERAGE.md)和[相容性](docs/COMPATIBILITY.md)。

## 系統需求

| | |
|---|---|
| **Android** | 9.0（API 28）或以上，arm64 |
| **應用程式** | YouTube（`com.google.android.youtube`） |
| **框架** | [Vector](https://github.com/JingMatrix/Vector) 或支援 libxposed API 102 的 LSPosed |
| **Root** | Vector/LSPosed 需要；模組本身不要求任何權限 |

## 安裝

```
1. 從 Releases 或 Xposed 模組存放區安裝 APK
2. 在 Vector 或 LSPosed 中啟用 YouTubeHideAds，作用範圍為 YouTube
3. 強制停止 YouTube 一次，然後開啟
```

可從 [GitHub Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) 或 [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads) 取得。設定位於 **YouTube → 你 → 設定 → YouTubeHideAds**。偏好設定和 AI 快取儲存在 YouTube 自己的資料中，清除 YouTube 資料會重設它們。

框架記錄中以 `YouTubeHideAds:` 開頭的行會說明發生了什麼：

```text
Ad policy self-check passed (70 cases)
SponsorBlock self-check passed (277 cases)
Ad component hook installed
Shorts feed removal hooks installed (paired, insert, response, restore, seed)
Video ad suppressed
```

---

## 運作方式

```
YouTube process
  XAX module (DEX) ──────────────► Bfp1Bridge.run ──JNI──► lib<policy>.so
  hooks, DexKit roles               input bytes            nine AOT Brainfuck policies
  settings page, HTTPS/JSON              ▲                       │
  typed actions                          │   exact reply only    │
                                         └───────────────────────┘
```

只有一條規則決定程式碼放在哪裡：**凡是涉及 YouTube、Android、網路或 JNI 的，由 XAX 處理；凡是決定是否對 XAX 找到的內容採取行動的，由 Brainfuck 決定。**策略程式庫、位元組配置和 Hook 搜尋的細節請見 [`docs/BRAINFUCK_ABI.md`](docs/BRAINFUCK_ABI.md) 和 [`docs/DEXKIT_RESOLUTION.md`](docs/DEXKIT_RESOLUTION.md)。

自動片段擷取只傳送影片 ID 的 SHA-256 前四位十六進位前綴。回應大小、記錄數和逾時都有上限，並停用重新導向。手動提交和投票會向所選伺服器傳送必要的資料和私人身分；觀看回報預設關閉，設定匯出預設不含私人 ID。

---

## 建置

本存放區沒有建置指令碼，發行版本使用外部工具建置：

```text
BBC          source/**/*.bf  ->  lib<policy>.so (AArch64)
AAPT2        source/branding ->  branding.apk (static resources only)
XAX          source/xax/youtubehideads.xax + pinned inputs -> signed APK
```

所有輸入都以 BLAKE3 固定在儲存區中，輸入不符會導致建置失敗。重新建置需要含 Android libxposed 設定檔的 [XAX](https://github.com/MrxSiN/XAX)（提交 `3cca599` 或相容的 branding-v2 快照）。步驟請見 [`docs/BUILD.md`](docs/BUILD.md)。

## 疑難排解

| 問題 | 嘗試 |
|---|---|
| 沒有模組記錄 | 確認模組已啟用且作用範圍包含 YouTube，然後強制停止 YouTube。 |
| 更新後立即出現 `UnsatisfiedLinkError` | 等待安裝完成後強制停止並重新開啟 YouTube。 |
| 自我檢查回報 `false` | 該功能維持關閉。請提交 `YouTubeHideAds:` 記錄行。 |
| 動態開關似乎無效 | 重新載入動態；移除僅對新載入的元件生效。 |
| YouTube 更新後失效 | YouTube 可能變更了內部類別。請連同 YouTube 版本提交記錄，或複製「相容性與診斷」中的報告。 |

## 致謝

[DexKit](https://github.com/LuckyPray/DexKit)、[libxposed API](https://github.com/libxposed/api)、[Vector](https://github.com/JingMatrix/Vector)、[LSPosed](https://github.com/LSPosed/LSPosed)、[XAX](https://github.com/MrxSiN/XAX)、[XAX-MCP](https://github.com/MrxSiN/XAX-MCP)、[BBC](https://github.com/MrxSiN/BBC)、[SponsorBlock](https://sponsor.ajay.app)、[Override92/AiSList](https://github.com/Override92/AiSList)、[Morphe Patches](https://github.com/MorpheApp/morphe-patches)（[保留的聲明](LICENSES/Morphe-NOTICE.txt)）。新撰寫的專案材料採用 GPL-3.0-or-later，第三方條款請見 [NOTICE](NOTICE)。

## 免責聲明

本專案與 Google LLC 或 YouTube 無關，也未獲其認可或贊助。僅供學習和個人使用。YouTube 更新可能隨時導致 Hook 失效。
