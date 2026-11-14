<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · **简体中文** · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**一个移除 YouTube 广告的 Xposed 模块：所有判断都用 Brainfuck 编写，其余部分用 XAX。**

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](README.md#install)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-EA4AAA?logo=githubsponsors&logoColor=fff&style=for-the-badge)](https://github.com/sponsors/MrxSiN)

<img src="docs/images/settings-ads.png" width="240" alt="Ads and SponsorBlock settings">
<img src="docs/images/settings-player.png" width="240" alt="Player settings">
<img src="docs/images/settings-feed.png" width="240" alt="Feed and blacklist settings">

</div>

## 功能

- **广告在显示之前就被移除：** 视频和 Shorts 广告、动态和搜索广告、Premium 和全屏推广，不留空白位置。
- **内置 SponsorBlock**，进度条上有彩色片段，播放器中有按钮，可手动跳过、投票和提交。
- **播放器：** 默认速度和画质、首选字幕语言、后台播放、原始音轨、记住直播位置、点按跳转、循环、速度按钮，以及 Return YouTube Dislike 的踩数。
- **手势：** 全屏时左侧滑动调亮度、右侧滑动调音量，不会作用于直播聊天、面板或“更多视频”面板。
- **动态：** 隐藏 Shorts 栏、帖子、预览、Playables 和 AI 频道，频道和关键词黑名单，以及 DeArrow 缩略图。
- **Shorts：** 可单独隐藏按钮和面板，并跳过直播 Shorts。
- **一个设置页面**，位于 **你 → 设置 → YouTube Hide Ads**，使用 YouTube 的语言（10 种语言）。

新增的附加功能默认关闭。所有设置及其默认值见[文档](docs/README.md#settings-and-defaults)。

## 安装

1. 从 [Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) 或 [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads) 获取 APK。
2. 在 [Vector](https://github.com/JingMatrix/Vector) 或 LSPosed（libxposed API 102）中启用，作用域选择 YouTube。
3. 强制停止 YouTube，然后重新打开。

需要 Android 9 或更高版本、arm64，框架需要 root。模块本身不申请任何权限。

## 兼容性

| YouTube | 模块 | 状态 |
|---|---|---|
| 21.45.88 | 1.3.0 (build 157) | ✅ 正常 |
| 21.43.523 | 1.2.0 | ✅ 正常 |
| 21.42.243 | 1.1.0 | ✅ 正常 |

在运行 Android 17 和 Vector 2.2 的 Pixel 8 Pro 上测试。YouTube 在大多数更新中会重命名其内部类。模块会按结构重新找到目标，找不到时会关闭该功能，而不是去猜。历史：[更新日志](CHANGELOG.md) · 详情：[兼容性](docs/COMPATIBILITY.md)。

## 已知限制

- HTTPS 过滤应用（如 AdGuard）可能会拦截 SponsorBlock、更新检查、踩数和 DeArrow；见[下文](README.md#sponsorblock-or-update-check-never-connects)。
- DeArrow 只替换缩略图，不替换标题。应用默认速度后，YouTube 自带的速度菜单仍显示 1x。
- 移动数据下的默认画质、直播 Shorts 和自动字幕屏蔽尚未在手机上测试。
- 只在一台手机的深色主题下检查过。1.3.0 的新文字为英文。

所有已测试和未测试的内容：[功能覆盖](docs/FEATURE_COVERAGE.md)。

## 故障排除

| 问题 | 尝试 |
|---|---|
| 框架日志中没有 `YouTubeHideAds:` 行 | 确认 YouTube 在作用域内，然后强制停止它。 |
| 某个动态开关似乎无效 | 重新加载动态。 |
| YouTube 更新后失效 | 使用 **关于 → 兼容性与诊断 → 报告问题**。 |

### SponsorBlock 或更新检查始终无法连接

这同样适用于踩数和 DeArrow。日志中会出现 `NOT_ENOUGH_SCTS`。某个 HTTPS 过滤应用正在重新签署连接，而 YouTube 的
证书透明度检查拒绝了它。在 AdGuard 中，将以下内容添加到 **HTTPS 过滤 → 排除项**：
`sponsor.ajay.app`、`github.com`、`returnyoutubedislikeapi.com`、`dearrow-thumb.ajay.app`。然后重启 YouTube。

## 工作原理

Brainfuck 负责判断，XAX 负责执行。九个 Brainfuck 策略负责判断，例如某个组件是不是
广告、某次跳转能否跳过片段、某次触摸是不是滑动。它们由 [BBC](https://github.com/MrxSiN/BBC) 预先编译为
AArch64。Hook、查找、设置和网络都在一个
[XAX](https://github.com/MrxSiN/XAX) 存储中，编译为 DEX。本仓库没有 Java、Kotlin 或 C
应用源码。

[架构](docs/ARCHITECTURE_BRAINFUCK_XAX.md) · [构建](docs/BUILD.md) · [全部文档](docs/README.md) · [证据](evidence/README.md)

## 支持

如果这个模块对你有用，可以[赞助它的开发](https://github.com/sponsors/MrxSiN)。

## 致谢和许可证

[DexKit](https://github.com/LuckyPray/DexKit)、[libxposed](https://github.com/libxposed/api)、
[Vector](https://github.com/JingMatrix/Vector)、[SponsorBlock](https://sponsor.ajay.app)、
[Return YouTube Dislike](https://returnyoutubedislike.com)、[DeArrow](https://dearrow.ajay.app)、
[AiSList](https://github.com/Override92/AiSList)（CC BY-NC 4.0，未打包），以及
[Morphe Patches](https://github.com/MorpheApp/morphe-patches)，用作行为参考
（[声明](LICENSES/Morphe-NOTICE.txt)）。

GPL-3.0-or-later。见 [NOTICE](NOTICE) 和[上游来源](docs/UPSTREAM_PROVENANCE.md)。
本项目与 Google 或 YouTube 无关联。
