<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · **简体中文** · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**一个移除 YouTube 广告的 Xposed 模块：所有判断都用 Brainfuck 编写，其余部分用 XAX。没错，是真的。**

广告、赞助 Shorts 和推广内容会在 YouTube 显示之前被移除，SponsorBlock 片段会被自动跳过。

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#系统要求)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!NOTE]
> YouTube 几乎每次更新都会重命名混淆后的类。模块会在每次启动时按结构重新查找目标；如果某个角色缺失或不唯一，就不启用该功能，而不是去猜。实际测试过的环境见[兼容性](#兼容性)表。

## 为什么用 Brainfuck？XAX 又是什么？

- **Brainfuck 负责判断。** 这个组件是不是广告、Premium 营销能否移除、播放器能否跳到赞助片段末尾、某次滑动是否在调节亮度。Brainfuck 不能调用 Android、Xposed、DexKit 或 JNI，它只读写字节；只有收到完全正确的回复时，宿主才会执行操作。
- **其余一切由 XAX 完成。** Hook、DexKit 查找、反射、设置页面、SponsorBlock 的 HTTPS 和 JSON 都在一个标准的 [XAX](https://github.com/MrxSiN/XAX) 语义存储中。外部 XAX 编译器将其编译为 DEX 并签名 APK。本仓库没有 Java、Kotlin、C、Python 或 shell 应用源码。

它也不慢。九个策略由 [BBC](https://github.com/MrxSiN/BBC) 预先编译为 AArch64 共享库，APK 中没有解释器。

|  | |
|---|---|
| 🧹 **移除，而非隐藏** | 广告组件在 YouTube 排版之前就被替换，赞助 Shorts 在播放页面构建前就被移出动态，所以不会有空白位置或卡住的片段。 |
| ⏭️ **内置 SponsorBlock** | 前缀查询（有限重试和缓存）、类别模式和颜色、手动跳过/撤销、创建片段和投票、排除频道、统计和设置迁移。 |
| 🔎 **不怕重命名** | DexKit 每次启动都按结构查找所有 Hook。角色缺失或不唯一时，该功能不会安装任何东西。 |
| 🧠 **策略用 Brainfuck 编写并编译** | 九个手写程序编译为原生代码；每次启动都会检查打包的策略和 SponsorBlock 控件。 |
| 🛟 **失败即关闭** | 自检失败时，该功能保持关闭。网络错误和未知播放类型绝不会跳转。 |
| ⚙️ **原生风格的设置** | 在 **你 → 设置** 中拥有独立的 **YouTube Hide Ads** 分区，位于“账号”上方，使用 YouTube 自己的行样式；每个开关相互独立，还有“兼容性与诊断”页面。 |
| 🎛️ **融入播放器的 SponsorBlock** | 自动播放旁的 SponsorBlock 图标会打开与播放器设置齿轮相同的浮动菜单；片段会在进度条上着色显示。 |
| 📱 **更清爽的 Shorts** | 可单独隐藏 Shorts 的按钮和面板，并跳过 Shorts 动态中的直播。 |
| 👆 **一目了然的滑动控制** | 左侧调亮度，右侧调音量，以带图标、进度和数值的胶囊显示。 |
| 🌐 **你的语言** | 跟随 YouTube 的语言：English、简体中文、繁體中文、Español、Português、Русский、日本語、한국어、Bahasa Indonesia 和 Bahasa Melayu。 |

---

## 移除内容

| 分组 | 设置 | 默认 |
|---|---|---|
| 广告 | 视频和 Shorts 广告 · 动态和搜索广告 · Premium 推销 · 全屏推广 | 开启，受 **隐藏广告** 总开关控制 |
| SponsorBlock | 赞助、自我推广 | 开启 |
| SponsorBlock | 互动提醒、片头、片尾、预告、填充内容、非音乐片段 | 关闭 |
| 内容 | Playables（游戏栏、卡片、探索入口） | 隐藏 |
| 动态 | 预览视频 · 探索更多主题 · 帖子 | 隐藏 |
| 动态 | 动态中的 Shorts | 显示 |
| 动态 | AI 频道 · 疑似 AI 频道（[AiSList](https://github.com/Override92/AiSList)） | 关闭 |
| 播放器 | 滑动调节亮度（左侧）· 滑动调节音量（右侧），仅限全屏 | 开启 |
| 播放器 | 多语言视频强制使用原始音轨 | 开启 |
| 播放器 | 后台播放，包括面向儿童的视频 | 开启 |
| Shorts | 点赞、评论、分享、混剪、保存、音频、订阅、标题、建议和信息面板、暂停时的叠加按钮 | 显示（可逐项隐藏） |
| Shorts | 跳过直播 Shorts | 关闭 |

关闭 **隐藏广告** 不会停用内容和播放器功能。修改动态相关开关后请重新加载动态。原始音轨从下一个音轨列表开始生效，并尊重你的手动选择。完整表格：[设置和默认值](docs/README.md#settings-and-defaults)。后台播放独立于“隐藏广告”和 SponsorBlock；修改该开关后请重启 YouTube。[实现和测试限制](docs/BACKGROUND_PLAYBACK.md)。

<details open>
<summary><b>🧱 每项移除发生在哪里</b></summary>
<br>

| 界面 | 位置 | 作用 |
|---|---|---|
| **视频广告** | 播放器广告激活和广告布局 | 当 Brainfuck 确认结构性广告特征且过渡安全时，抑制广告位。 |
| **动态、搜索和购物广告** | 由 DexKit 找到的组件解析器 | 用 YouTube 自己的空组件替换已确认的付费组件。 |
| **赞助 Shorts** | Shorts 响应、插入和播放页初始数据 | 在播放页存在之前，连同跟踪数据一起移除视频/图片广告条目。 |
| **Premium、全屏、面板** | 推销视图、全屏对话框、按类型标识的互动面板 | 隐藏营销界面，不影响权益或订阅管理。 |
| **动态分区、Playables、AI 频道、Shorts 组件** | 同一个组件 Hook | 只移除匹配的分区、卡片或按钮；频道行和播放列表保留。 |
| **SponsorBlock** | 播放器跳转/时长桥接和原生进度条 | 有限的前缀检索、类别模式、彩色标记、手动控制和明确的社区操作。 |

</details>

---

## 状态

**v1.2.0**（versionCode 155）支持 YouTube 21.43.523：后台播放和 SponsorBlock 跳过重新可用。新增以 YouTube 风格对话框提示的更新检查（默认开启，位于“关于”）和 **报告问题** 按钮，可打开已填好内容的 GitHub issue。模块现名为 **YouTube Hide Ads**。[更新日志](CHANGELOG.md)。

**v1.1.0**（versionCode 153）是 1.0.0 之后的第一个正式版本。它加入了后台播放、YouTube 设置中的独立分区、“兼容性与诊断”页面、YouTube 风格的 SponsorBlock 控件、隐藏 Shorts 组件、跳过直播 Shorts、重新设计的滑动控制以及另外九种语言。它在手机上也轻快得多：Brainfuck 策略调用不再重复打开 APK，DexKit 结果会被缓存，因此首次启动之后 YouTube 打开快约 0.35 秒。[设备检查](evidence/device_perf_20261028/README.md)。

两个正式版本之间的开发版本（111 至 153）见[更新日志](CHANGELOG.md)，各自的证据见 [evidence](evidence/README.md)。

### 兼容性

在 Pixel 8 Pro（Android 17、Vector 2.2，libxposed API 102）上测试。试过其他环境？欢迎提交 PR 添加一行。

| YouTube | 模块 | 状态 |
|---|---|---|
| 21.43.523 | 1.2.0 | ✅ 正常 |
| 21.42.243 | 1.1.0 | ✅ 正常 |
| 21.41.525 | 1.0.0 | ✅ 正常 |

### 已知限制

- HTTPS 过滤应用（如 AdGuard）会让 SponsorBlock 和更新检查无法连接。请将 `sponsor.ajay.app` 和 `github.com` 加入 HTTPS 过滤的排除列表（[详情](README.md#sponsorblock-or-update-check-never-connects)）。
- Premium、全屏和互动面板推广只在受控 Hook 测试中移除过，尚未见到真实推送的案例。
- 预览视频和“探索更多主题”栏目仅按英文标题匹配。
- AI 频道列表由社区维护，可能误判频道，因此默认关闭。
- 后台播放的开关改动后需要重启 YouTube，Shorts 仍由 YouTube 自行处理。蓝牙控制和来电打断尚未测试。
- SponsorBlock 的提交和投票尚未在正式服务器上试过。见[功能和限制](docs/SPONSORBLOCK_API_RESEARCH.md)。
- 跳过直播 Shorts 尚未遇到真实的直播 Short；它、滑动胶囊和 YouTube 语言切换都是用开发探针检查的。
- 模块页面只在深色主题下检查过。浅色主题、平板和从右到左布局尚未测试。
- YouTube 或模块更新后的第一次启动会重建 Hook 缓存，大约慢 0.4 秒。
- 仅支持 arm64-v8a。只试过上面的环境和 YouTube 版本，尚未试过 LSPatch。

详情：[功能覆盖](docs/FEATURE_COVERAGE.md)和[兼容性](docs/COMPATIBILITY.md)。

## 系统要求

| | |
|---|---|
| **Android** | 9.0（API 28）或更高，arm64 |
| **应用** | YouTube（`com.google.android.youtube`） |
| **框架** | [Vector](https://github.com/JingMatrix/Vector) 或支持 libxposed API 102 的 LSPosed |
| **Root** | Vector/LSPosed 需要；模块本身不申请任何权限 |

## 安装

```
1. 从 Releases 或 Xposed 模块仓库安装 APK
2. 在 Vector 或 LSPosed 中启用 YouTubeHideAds，作用域为 YouTube
3. 强制停止 YouTube 一次，然后打开
```

可从 [GitHub Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) 或 [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads) 获取。设置位于 **YouTube → 你 → 设置 → YouTube Hide Ads**。偏好设置和 AI 缓存保存在 YouTube 自己的数据中，清除 YouTube 数据会重置它们。

框架日志中以 `YouTubeHideAds:` 开头的行会说明发生了什么：

```text
Ad policy self-check passed (70 cases)
SponsorBlock self-check passed (277 cases)
Ad component hook installed
Shorts feed removal hooks installed (paired, insert, response, restore, seed)
Video ad suppressed
```

---

## 工作原理

```
YouTube process
  XAX module (DEX) ──────────────► Bfp1Bridge.run ──JNI──► lib<policy>.so
  hooks, DexKit roles               input bytes            nine AOT Brainfuck policies
  settings page, HTTPS/JSON              ▲                       │
  typed actions                          │   exact reply only    │
                                         └───────────────────────┘
```

只有一条规则决定代码放在哪里：**凡是涉及 YouTube、Android、网络或 JNI 的，由 XAX 完成；凡是决定是否对 XAX 发现的内容采取行动的，由 Brainfuck 决定。**策略库、字节布局和 Hook 查找的细节见 [`docs/BRAINFUCK_ABI.md`](docs/BRAINFUCK_ABI.md) 和 [`docs/DEXKIT_RESOLUTION.md`](docs/DEXKIT_RESOLUTION.md)。

自动片段检索只发送视频 ID 的 SHA-256 前四位十六进制前缀。响应大小、记录数和超时都有上限，并禁用重定向。手动提交和投票会向所选服务器发送必要的数据和私有身份；观看报告默认关闭，设置导出默认不包含私有 ID。

---

## 构建

本仓库没有构建脚本，发布版本使用外部工具构建：

```text
BBC          source/**/*.bf  ->  lib<policy>.so (AArch64)
AAPT2        source/branding ->  branding.apk (static resources only)
XAX          source/xax/youtubehideads.xax + pinned inputs -> signed APK
```

所有输入都以 BLAKE3 固定在存储中，输入不匹配会导致构建失败。重新构建需要带 Android libxposed 配置的 [XAX](https://github.com/MrxSiN/XAX)（提交 `3cca599` 或兼容的 branding-v2 快照）。步骤见 [`docs/BUILD.md`](docs/BUILD.md)。

## 故障排除

| 问题 | 尝试 |
|---|---|
| 没有模块日志 | 确认模块已启用且作用域包含 YouTube，然后强制停止 YouTube。 |
| 更新后立即出现 `UnsatisfiedLinkError` | 等安装完成后强制停止并重新打开 YouTube。 |
| 自检报告 `false` | 该功能保持关闭。请提交 `YouTubeHideAds:` 日志行。 |
| 动态开关似乎无效 | 重新加载动态；移除仅对新加载的组件生效。 |
| YouTube 更新后失效 | YouTube 可能修改了内部类。请连同 YouTube 版本提交日志，或复制“兼容性与诊断”中的报告。 |

## 致谢

[DexKit](https://github.com/LuckyPray/DexKit)、[libxposed API](https://github.com/libxposed/api)、[Vector](https://github.com/JingMatrix/Vector)、[LSPosed](https://github.com/LSPosed/LSPosed)、[XAX](https://github.com/MrxSiN/XAX)、[XAX-MCP](https://github.com/MrxSiN/XAX-MCP)、[BBC](https://github.com/MrxSiN/BBC)、[SponsorBlock](https://sponsor.ajay.app)、[Override92/AiSList](https://github.com/Override92/AiSList)、[Morphe Patches](https://github.com/MorpheApp/morphe-patches)（[保留的声明](LICENSES/Morphe-NOTICE.txt)）。新编写的项目材料采用 GPL-3.0-or-later，第三方条款见 [NOTICE](NOTICE)。

## 免责声明

本项目与 Google LLC 或 YouTube 无关，也未获其认可或赞助。仅供学习和个人使用。YouTube 更新可能随时导致 Hook 失效。
