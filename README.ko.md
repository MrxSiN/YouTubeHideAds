<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · **한국어** · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**YouTube 광고를 없애는 Xposed 모듈입니다. 모든 판단은 Brainfuck으로, 나머지는 XAX로 작성했습니다. 진짜입니다.**

광고, 스폰서 Shorts, 프로모션은 YouTube가 표시하기 전에 제거되고 SponsorBlock 세그먼트는 건너뜁니다.

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#요구-사항)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!NOTE]
> YouTube는 거의 매 업데이트마다 난독화된 클래스 이름을 바꿉니다. 모듈은 시작할 때마다 구조를 보고 대상을 다시 찾습니다. 역할을 찾지 못하거나 하나로 정해지지 않으면 추측하지 않고 해당 기능을 그대로 둡니다. 실제로 테스트한 환경은 [호환성](#호환성) 표를 보세요.

## 왜 Brainfuck인가요? XAX는 무엇인가요?

- **판단은 Brainfuck이 합니다.** 이 구성요소가 광고인지, Premium 마케팅을 없애도 되는지, 플레이어가 스폰서 세그먼트 끝으로 이동해도 되는지, 스와이프가 밝기 조절인지. Brainfuck은 Android, Xposed, DexKit, JNI를 호출할 수 없고 바이트를 읽고 쓸 뿐입니다. 호스트는 정확히 성공한 응답을 받을 때만 동작합니다.
- **나머지는 모두 XAX가 합니다.** 후크, DexKit 탐색, 리플렉션, 설정 페이지, SponsorBlock의 HTTPS와 JSON은 하나의 표준 [XAX](https://github.com/MrxSiN/XAX) 시맨틱 저장소에 있습니다. 외부 XAX 컴파일러가 이를 DEX로 바꾸고 APK에 서명합니다. 이 저장소에는 Java, Kotlin, C, Python, 셸 앱 소스가 없습니다.

느리지도 않습니다. 9개의 정책은 [BrainfuckCC](https://github.com/MrxSiN/BrainfuckCC)로 미리 AArch64 공유 라이브러리로 컴파일됩니다. APK에는 인터프리터가 없습니다.

|  | |
|---|---|
| 🧹 **숨기지 않고 제거** | 광고 구성요소는 YouTube가 배치하기 전에 교체되고, 스폰서 Shorts는 플레이어가 만들어지기 전에 피드에서 빠지므로 빈 칸이나 멈춘 영상이 없습니다. |
| ⏭️ **SponsorBlock 내장** | 재시도와 캐시가 제한된 접두사 조회, 카테고리별 동작과 색상, 수동 건너뛰기와 취소, 세그먼트 생성과 투표, 제외, 통계, 설정 이전. |
| 🔎 **이름이 바뀌어도 동작** | DexKit이 시작할 때마다 구조로 모든 후크를 찾습니다. 역할이 없거나 모호하면 해당 기능은 아무것도 설치하지 않습니다. |
| 🧠 **Brainfuck 정책, 컴파일됨** | 직접 작성한 9개 프로그램을 네이티브 코드로 컴파일했습니다. 정책과 SponsorBlock 컨트롤은 시작할 때마다 검사합니다. |
| 🛟 **실패하면 꺼짐** | 자체 점검에 실패한 기능은 꺼진 상태로 남습니다. 네트워크 오류나 알 수 없는 재생 유형에서는 이동하지 않습니다. |
| ⚙️ **네이티브 느낌의 설정** | **나 → 설정**의 '계정' 위에 전용 **YouTubeHideAds** 섹션이 있고, YouTube 자체 행 스타일을 사용합니다. 모든 스위치는 독립적이며 '호환성 및 진단' 페이지도 있습니다. |
| 🎛️ **플레이어에 녹아든 SponsorBlock** | 자동재생 옆 SponsorBlock 아이콘은 설정 톱니바퀴와 같은 플로팅 메뉴를 엽니다. 세그먼트는 탐색 막대에 색상으로 표시됩니다. |
| 📱 **깔끔한 Shorts** | Shorts의 버튼과 패널을 하나씩 숨기고, Shorts 피드의 실시간 스트림을 건너뛸 수 있습니다. |
| 👆 **한눈에 보이는 스와이프 컨트롤** | 왼쪽은 밝기, 오른쪽은 볼륨. 아이콘, 레벨, 값이 담긴 알약 모양으로 표시합니다. |
| 🌐 **내 언어로** | YouTube 언어를 따릅니다: English, 简体中文, 繁體中文, Español, Português, Русский, 日本語, 한국어, Bahasa Indonesia, Bahasa Melayu. |

---

## 제거하는 항목

| 그룹 | 설정 | 기본값 |
|---|---|---|
| 광고 | 동영상 및 Shorts 광고 · 피드 및 검색 광고 · Premium 프로모션 · 전체 화면 프로모션 | 켜짐(**광고 숨기기** 기본 스위치에 따름) |
| SponsorBlock | 스폰서, 자체 홍보 | 켜짐 |
| SponsorBlock | 상호작용 알림, 인트로, 아웃트로, 미리보기, 채우기 콘텐츠, 음악 외 구간 | 꺼짐 |
| 콘텐츠 | Playables(게임 섹션, 카드, 탐색 항목) | 숨김 |
| 피드 | 미리보기 동영상 · 다른 주제 탐색 · 게시물 | 숨김 |
| 피드 | 피드의 Shorts | 표시 |
| 피드 | AI 채널 · AI로 의심되는 채널([AiSList](https://github.com/Override92/AiSList)) | 꺼짐 |
| 플레이어 | 스와이프로 밝기(왼쪽) · 스와이프로 볼륨(오른쪽), 전체 화면 전용 | 켜짐 |
| 플레이어 | 다국어 동영상에서 원본 오디오 사용 | 켜짐 |
| 플레이어 | 백그라운드 재생(아동용 동영상 포함) | 켜짐 |
| Shorts | 좋아요, 댓글, 공유, 리믹스, 저장, 사운드, 구독, 제목, 추천 및 정보 패널, 일시중지 시 버튼 | 표시(각각 숨길 수 있음) |
| Shorts | 실시간 Shorts 건너뛰기 | 꺼짐 |

**광고 숨기기**를 꺼도 콘텐츠와 플레이어 기능은 꺼지지 않습니다. 피드 스위치를 바꾼 뒤에는 피드를 새로고침하세요. 원본 오디오는 다음 트랙 목록부터 적용되며 수동 선택을 존중합니다. 전체 표: [설정 및 기본값](docs/README.md#settings-and-defaults). 백그라운드 재생은 '광고 숨기기'와 SponsorBlock과 별개이며, 바꾼 뒤에는 YouTube를 다시 시작하세요. [구현 및 테스트 한계](docs/BACKGROUND_PLAYBACK.md).

<details open>
<summary><b>🧱 각 항목이 제거되는 위치</b></summary>
<br>

| 영역 | 위치 | 하는 일 |
|---|---|---|
| **동영상 광고** | 플레이어 광고 활성화와 광고 레이아웃 | Brainfuck이 구조적 광고 특징과 안전한 전환을 확인하면 광고 슬롯을 막습니다. |
| **피드, 검색, 쇼핑 광고** | DexKit으로 찾은 구성요소 파서 | 확인된 유료 구성요소를 YouTube 자체의 빈 구성요소로 바꿉니다. |
| **스폰서 Shorts** | Shorts 응답, 삽입, 플레이어 초기 데이터 | 플레이어가 생기기 전에 동영상/이미지 광고 항목을 추적 데이터와 함께 제거합니다. |
| **Premium, 전체 화면, 패널** | 제안 화면, 전체 화면 대화상자, 형식 식별자로 찾은 참여 패널 | 혜택이나 구독 관리는 건드리지 않고 마케팅 화면만 숨깁니다. |
| **피드 섹션, Playables, AI 채널, Shorts 구성요소** | 같은 구성요소 후크 | 일치한 섹션, 카드, 버튼만 제거하고 채널 행과 재생목록은 남깁니다. |
| **SponsorBlock** | 플레이어 이동/길이 브리지와 네이티브 탐색 막대 | 제한된 접두사 조회, 카테고리 동작, 색상 표시, 수동 컨트롤, 명시적인 커뮤니티 작업. |

</details>

---

## 상태

**v1.1.0**(versionCode 153)은 1.0.0 이후 첫 릴리스입니다. 백그라운드 재생, YouTube 설정의 전용 섹션, '호환성 및 진단' 페이지, YouTube 스타일 SponsorBlock 컨트롤, Shorts 구성요소 숨기기, 실시간 Shorts 건너뛰기, 새로 디자인한 스와이프 컨트롤, 9개 언어를 추가합니다. 휴대전화 부담도 크게 줄었습니다. Brainfuck 정책 호출이 더 이상 APK를 다시 열지 않고 DexKit 결과를 캐시하므로, 처음 실행한 뒤에는 YouTube가 약 0.35초 더 빨리 열립니다. [기기 점검](evidence/device_perf_20261028/README.md).

두 릴리스 사이의 개발 빌드(111~153)는 [변경 기록](CHANGELOG.md)에, 각 빌드의 증거는 [evidence](evidence/README.md)에 있습니다.

### 호환성

각 행은 누군가 실제로 실행해 본 환경입니다. 다른 환경을 시도했다면 행을 추가하는 pull request를 보내 주세요.

| 기기 | Android | 프레임워크 | YouTube | 모듈 | 결과 | 테스터 | 날짜 |
|---|---|---|---|---|---|---|---|
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.42.243 | 1.1.0 | 광고, Shorts 광고 제거, SponsorBlock, 원본 오디오, 피드와 링크에서 연 동영상의 백그라운드 재생(홈, 화면 꺼짐, 스위치 끔), 시작 11개 점검 | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.42.243 | dev 132 | 설정 섹션, 진단, Shorts 구성요소, SponsorBlock 아이콘/메뉴, 실제 건너뛰기, 시작 11개 + UI 64개 점검 | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.42.243 | dev 127 | 새 슬라이더, 다크/라이트, 터치, 키보드, 저장/다시 열기, 636 + 64개 점검 | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.42.243 | dev 123 | 네이티브 SponsorBlock UI, 색상 선택기, 636 + 28개 점검 | @MrxSiN | 2026-10 |

### 알려진 한계

- Premium, 전체 화면, 패널 프로모션은 통제된 후크 테스트를 통과했지만 실제로 전달된 사례는 아직 보지 못했습니다.
- 미리보기 동영상과 '다른 주제 탐색' 제목은 영어로만 인식합니다.
- AI 목록은 커뮤니티가 관리하며 잘못 분류할 수 있어 기본으로 꺼져 있습니다.
- SponsorBlock 컨트롤은 플레이어 상단의 SponsorBlock 아이콘과 모듈 설정에서 쓸 수 있습니다. [기능과 한계](docs/SPONSORBLOCK_API_RESEARCH.md)를 보세요.
- 실시간 Shorts 건너뛰기는 테스트 휴대전화에서 아직 실제 실시간 Short를 만나지 못했습니다. 페이지 판정은 개발용 프로브로 확인했습니다.
- arm64-v8a만 지원합니다. 다른 YouTube 버전, 기기, LSPatch는 테스트하지 않았습니다.

자세히: [기능 범위](docs/FEATURE_COVERAGE.md), [호환성](docs/COMPATIBILITY.md).

## 요구 사항

| | |
|---|---|
| **Android** | 9.0(API 28) 이상, arm64 |
| **앱** | YouTube(`com.google.android.youtube`) |
| **프레임워크** | [Vector](https://github.com/JingMatrix/Vector) 또는 libxposed API 102를 지원하는 LSPosed |
| **Root** | Vector/LSPosed에 필요하며, 모듈 자체는 권한을 요청하지 않습니다 |

## 설치

```
1. Releases 또는 Xposed 모듈 저장소에서 APK 설치
2. Vector 또는 LSPosed에서 YouTubeHideAds를 사용 설정하고 범위를 YouTube로 지정
3. YouTube를 한 번 강제 종료한 뒤 실행
```

[GitHub Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) 또는 [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads)에서 받을 수 있습니다. 설정은 **YouTube → 나 → 설정 → YouTubeHideAds**에 있습니다. 설정과 AI 캐시는 YouTube 자체 데이터에 저장되므로 YouTube 데이터를 지우면 초기화됩니다.

프레임워크 로그에서 `YouTubeHideAds:`로 시작하는 줄로 동작을 확인할 수 있습니다.

```text
Ad policy self-check passed (70 cases)
SponsorBlock self-check passed (277 cases)
Ad component hook installed
Shorts feed removal hooks installed (paired, insert, response, restore, seed)
Video ad suppressed
```

---

## 동작 방식

```
YouTube process
  XAX module (DEX) ──────────────► Bfp1Bridge.run ──JNI──► lib<policy>.so
  hooks, DexKit roles               input bytes            nine AOT Brainfuck policies
  settings page, HTTPS/JSON              ▲                       │
  typed actions                          │   exact reply only    │
                                         └───────────────────────┘
```

코드 위치를 정하는 규칙은 하나입니다: **YouTube, Android, 네트워크, JNI를 다루면 XAX가 하고, XAX가 찾은 것에 대해 행동할지는 Brainfuck이 정합니다.** 정책 라이브러리, 바이트 배치, 후크 탐색의 자세한 내용은 [`docs/BRAINFUCK_ABI.md`](docs/BRAINFUCK_ABI.md)와 [`docs/DEXKIT_RESOLUTION.md`](docs/DEXKIT_RESOLUTION.md)에 있습니다.

세그먼트 자동 조회는 동영상 ID의 SHA-256 앞 네 자리(16진수)만 보냅니다. 응답 크기, 레코드 수, 시간 제한에 상한이 있고 리디렉션은 꺼져 있습니다. 수동 제출과 투표는 선택한 서버에 필요한 데이터와 비공개 ID를 보냅니다. 시청 보고는 기본으로 꺼져 있고, 설정 내보내기는 기본으로 비공개 ID를 제외합니다.

---

## 빌드

이 저장소에는 빌드 스크립트가 없습니다. 릴리스는 외부 도구로 빌드합니다.

```text
BrainfuckCC  source/**/*.bf  ->  lib<policy>.so (AArch64)
AAPT2        source/branding ->  branding.apk (static resources only)
XAX          source/xax/youtubehideads.xax + pinned inputs -> signed APK
```

모든 입력은 저장소에 BLAKE3로 고정되어 있어, 입력이 다르면 빌드가 실패합니다. 다시 빌드하려면 Android libxposed 프로필이 있는 [XAX](https://github.com/MrxSiN/XAX)(커밋 `3cca599` 또는 호환되는 branding-v2 스냅샷)가 필요합니다. 절차는 [`docs/BUILD.md`](docs/BUILD.md)에 있습니다.

## 문제 해결

| 문제 | 해결 방법 |
|---|---|
| 모듈 로그가 없음 | 모듈이 YouTube 범위로 켜져 있는지 확인한 뒤 YouTube를 강제 종료하세요. |
| 업데이트 직후 `UnsatisfiedLinkError` | 설치가 끝날 때까지 기다린 뒤 YouTube를 강제 종료하고 다시 여세요. |
| 자체 점검이 `false` | 해당 기능은 꺼진 상태로 남습니다. `YouTubeHideAds:` 로그를 알려 주세요. |
| 피드 스위치가 적용되지 않는 것 같음 | 피드를 새로고침하세요. 새로 불러온 구성요소에 적용됩니다. |
| YouTube 업데이트 후 동작하지 않음 | 내부 클래스가 바뀌었을 수 있습니다. YouTube 버전과 함께 로그를 알려 주거나 '호환성 및 진단'의 보고서를 복사해 주세요. |

## 크레딧

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed API](https://github.com/libxposed/api), [Vector](https://github.com/JingMatrix/Vector), [LSPosed](https://github.com/LSPosed/LSPosed), [XAX](https://github.com/MrxSiN/XAX), [XAX-MCP](https://github.com/MrxSiN/XAX-MCP), [BrainfuckCC](https://github.com/MrxSiN/BrainfuckCC), [SponsorBlock](https://sponsor.ajay.app), [Override92/AiSList](https://github.com/Override92/AiSList), [Morphe Patches](https://github.com/MorpheApp/morphe-patches)([보존한 고지](LICENSES/Morphe-NOTICE.txt)). 새로 작성한 프로젝트 자료는 GPL-3.0-or-later이며, 제3자 조건은 [NOTICE](NOTICE)를 보세요.

## 면책 조항

Google LLC 또는 YouTube와 관련이 없으며 승인이나 후원을 받지 않았습니다. 교육 및 개인 용도로 제공됩니다. YouTube 업데이트로 예고 없이 후크가 동작하지 않을 수 있습니다.
