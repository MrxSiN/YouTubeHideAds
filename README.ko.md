<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · **한국어** · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**YouTube 광고를 없애는 Xposed 모듈입니다. 모든 판단은 Brainfuck으로 작성했고, 나머지는 XAX로 작성했습니다.**

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](README.md#install)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-EA4AAA?logo=githubsponsors&logoColor=fff&style=for-the-badge)](https://github.com/sponsors/MrxSiN)

<img src="docs/images/settings-ads.png" width="240" alt="Ads and SponsorBlock settings">
<img src="docs/images/settings-player.png" width="240" alt="Player settings">
<img src="docs/images/settings-feed.png" width="240" alt="Feed and blacklist settings">

</div>

## 기능

- **광고는 표시되기 전에 제거됩니다:** 동영상과 Shorts 광고, 피드와 검색 광고, Premium 및 전체 화면 프로모션. 빈 자리가 남지 않습니다.
- **SponsorBlock 내장.** 탐색 막대에 색깔 구간이 표시되고, 플레이어 버튼으로 수동 건너뛰기, 투표, 제출을 할 수 있습니다.
- **플레이어:** 기본 재생 속도와 화질, 선호 자막 언어, 백그라운드 재생, 원본 오디오, 라이브 재생 위치 기억, 탭하여 이동, 반복, 속도 버튼, Return YouTube Dislike 수.
- **제스처:** 전체 화면에서 왼쪽은 밝기, 오른쪽은 볼륨을 스와이프로 조절합니다. 라이브 채팅, 패널, 더 많은 동영상 시트 위에서는 동작하지 않습니다.
- **피드:** Shorts 선반, 게시물, 미리보기, Playables, AI 채널 숨기기, 채널 및 키워드 블랙리스트, DeArrow 썸네일.
- **Shorts:** 개별 버튼과 패널을 숨기고, 라이브 Shorts를 건너뜁니다.
- **하나의 설정 페이지**가 **나 → 설정 → YouTube Hide Ads**에 있으며, YouTube 언어로 표시됩니다(10개 언어).

새 부가 기능은 기본적으로 꺼져 있습니다. 모든 설정과 기본값은 [문서](docs/README.md#settings-and-defaults)에 나와 있습니다.

## 설치

1. [Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) 또는 [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads)에서 APK를 받습니다.
2. [Vector](https://github.com/JingMatrix/Vector) 또는 LSPosed(libxposed API 102)에서 모듈을 켜고, 범위에 YouTube를 포함합니다.
3. YouTube를 강제 종료한 뒤 다시 엽니다.

arm64 기기의 Android 9 이상과 프레임워크용 root가 필요합니다. 모듈 자체는 어떤 권한도 요청하지 않습니다.

## 호환성

| YouTube | 모듈 | 상태 |
|---|---|---|
| 21.45.88 | 1.3.0 (build 157) | ✅ 작동 |
| 21.43.523 | 1.2.0 | ✅ 작동 |
| 21.42.243 | 1.1.0 | ✅ 작동 |

Android 17과 Vector 2.2가 있는 Pixel 8 Pro에서 테스트했습니다. YouTube는 대부분의 업데이트에서
내부 클래스 이름을 바꿉니다. 모듈은 구조를 보고 대상을 다시 찾으며, 찾지 못하면 추측하지 않고
해당 기능을 끕니다. 기록: [변경 내역](CHANGELOG.md) · 자세한 내용: [호환성](docs/COMPATIBILITY.md).

## 알려진 제한

- AdGuard 같은 HTTPS 필터링 앱은 SponsorBlock, 업데이트 확인, 싫어요 수, DeArrow를 막을 수 있습니다. [아래](README.md#sponsorblock-or-update-check-never-connects)를 참고하세요.
- DeArrow는 썸네일만 바꾸고 제목은 바꾸지 않습니다. 기본 속도를 적용해도 YouTube 자체 속도 메뉴에는 계속 1x로 표시됩니다.
- 모바일 데이터에서의 기본 화질, 라이브 Shorts, 자동 자막 차단은 휴대폰에서 테스트하지 않았습니다.
- 휴대폰 한 대에서 다크 테마만 확인했습니다. 1.3.0의 새 문구는 영어입니다.

테스트한 것과 하지 않은 것 전체: [기능 검증 범위](docs/FEATURE_COVERAGE.md).

## 문제 해결

| 문제 | 해결 방법 |
|---|---|
| 프레임워크 로그에 `YouTubeHideAds:` 줄이 없음 | YouTube가 범위에 포함되어 있는지 확인한 뒤 강제 종료하세요. |
| 피드 스위치가 무시되는 것 같음 | 피드를 새로고침하세요. |
| YouTube 업데이트 후 작동하지 않음 | **정보 → 호환성 및 진단 → 문제 신고**를 사용하세요. |

### SponsorBlock이나 업데이트 확인이 계속 연결되지 않음

싫어요 수와 DeArrow도 마찬가지입니다. 로그에 `NOT_ENOUGH_SCTS`가 나타납니다. HTTPS 필터링 앱이 연결에 다시 서명하고 있고, YouTube의
인증서 투명성 검사가 이를 거부합니다. AdGuard에서는 **HTTPS 필터링 → 제외 항목**에 다음을 추가하세요:
`sponsor.ajay.app`, `github.com`, `returnyoutubedislikeapi.com`, `dearrow-thumb.ajay.app`. 그런 다음 YouTube를 다시 시작하세요.

## 동작 방식

Brainfuck이 판단하고 XAX가 실행합니다. 아홉 개의 Brainfuck 정책이 예를 들어 구성 요소가
광고인지, 탐색으로 구간을 건너뛰어도 되는지, 터치가 스와이프인지를 판단합니다. 이 정책은
[BBC](https://github.com/MrxSiN/BBC)가 AArch64로 미리 컴파일합니다. 후크, 탐색, 설정, 네트워킹은 하나의
[XAX](https://github.com/MrxSiN/XAX) 저장소에 있으며 DEX로 컴파일됩니다. 저장소에는 Java, Kotlin, C 애플리케이션 소스가 없습니다.

[아키텍처](docs/ARCHITECTURE_BRAINFUCK_XAX.md) · [빌드](docs/BUILD.md) · [모든 문서](docs/README.md) · [증거](evidence/README.md)

## 후원

모듈이 도움이 되었다면 [개발을 후원](https://github.com/sponsors/MrxSiN)할 수 있습니다.

## 크레딧과 라이선스

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed](https://github.com/libxposed/api),
[Vector](https://github.com/JingMatrix/Vector), [SponsorBlock](https://sponsor.ajay.app),
[Return YouTube Dislike](https://returnyoutubedislike.com), [DeArrow](https://dearrow.ajay.app),
[AiSList](https://github.com/Override92/AiSList)(CC BY-NC 4.0, 포함하지 않음),
그리고 동작 참고용으로 사용한 [Morphe Patches](https://github.com/MorpheApp/morphe-patches)
([고지](LICENSES/Morphe-NOTICE.txt)).

GPL-3.0-or-later. [NOTICE](NOTICE)와 [업스트림 출처](docs/UPSTREAM_PROVENANCE.md)를 참고하세요.
이 프로젝트는 Google 또는 YouTube와 관련이 없습니다.
