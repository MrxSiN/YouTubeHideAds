<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · **Bahasa Melayu**

**Modul Xposed yang membuang iklan daripada YouTube, dengan setiap keputusan ditulis dalam Brainfuck dan selebihnya dalam XAX.**

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](README.md#install)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-EA4AAA?logo=githubsponsors&logoColor=fff&style=for-the-badge)](https://github.com/sponsors/MrxSiN)

<img src="docs/images/settings-ads.png" width="240" alt="Ads and SponsorBlock settings">
<img src="docs/images/settings-player.png" width="240" alt="Player settings">
<img src="docs/images/settings-feed.png" width="240" alt="Feed and blacklist settings">

</div>

## Ciri

- **Iklan dibuang sebelum dipaparkan:** iklan video dan Shorts, iklan suapan dan carian, promosi Premium dan skrin penuh. Tiada ruang kosong.
- **SponsorBlock terbina dalam**, dengan segmen berwarna pada bar carian dan butang dalam pemain untuk langkau manual, mengundi dan menghantar segmen.
- **Pemain:** kelajuan dan kualiti lalai, bahasa sari kata pilihan, main di latar belakang, audio asal, ingat kedudukan siaran langsung, ketik untuk mencari, ulang, butang kelajuan, dan kiraan Return YouTube Dislike.
- **Gerak isyarat:** leret untuk kecerahan di kiri dan kelantangan di kanan dalam skrin penuh, tidak pernah di atas sembang langsung, panel atau helaian Video lagi.
- **Suapan:** sembunyikan rak Shorts, siaran, pratonton, Playables dan saluran AI, senarai hitam saluran dan kata kunci, serta imej kecil DeArrow.
- **Shorts:** sembunyikan butang dan panel tertentu, dan langkau Shorts siaran langsung.
- **Satu halaman tetapan** di bawah **Anda → Tetapan → YouTube Hide Ads**, dalam bahasa YouTube (10 bahasa).

Tambahan baharu dimatikan secara lalai. Semua tetapan dan nilai lalainya disenaraikan dalam [dokumentasi](docs/README.md#settings-and-defaults).

## Pemasangan

1. Dapatkan APK daripada [Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) atau [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads).
2. Dayakan dalam [Vector](https://github.com/JingMatrix/Vector) atau LSPosed (libxposed API 102) dengan YouTube dalam skop.
3. Paksa henti YouTube dan buka semula.

Memerlukan Android 9 atau lebih baharu pada arm64, dan root untuk rangka kerja. Modul itu sendiri tidak meminta sebarang kebenaran.

## Keserasian

| YouTube | Modul | Status |
|---|---|---|
| 21.45.88 | 1.3.0 (build 157) | ✅ Berfungsi |
| 21.43.523 | 1.2.0 | ✅ Berfungsi |
| 21.42.243 | 1.1.0 | ✅ Berfungsi |

Diuji pada Pixel 8 Pro dengan Android 17 dan Vector 2.2. YouTube menukar nama kelas dalamannya dalam kebanyakan
kemas kini. Modul menemui semula sasarannya mengikut strukturnya, dan mematikan sesuatu ciri daripada meneka
apabila tidak dapat. Sejarah: [log perubahan](CHANGELOG.md) · butiran: [keserasian](docs/COMPATIBILITY.md).

## Had yang diketahui

- Aplikasi penapis HTTPS seperti AdGuard boleh menyekat SponsorBlock, semakan kemas kini, kiraan dislike dan DeArrow; lihat [di bawah](README.md#sponsorblock-or-update-check-never-connects).
- DeArrow menggantikan imej kecil, bukan tajuk. Menu kelajuan YouTube sendiri masih menunjukkan 1x selepas kelajuan lalai dikenakan.
- Kualiti lalai pada data mudah alih, Shorts siaran langsung dan sekatan sari kata automatik belum diuji pada telefon.
- Disemak dalam tema gelap pada satu telefon sahaja. Teks baharu 1.3.0 dalam bahasa Inggeris.

Semua yang diuji dan belum diuji: [liputan ciri](docs/FEATURE_COVERAGE.md).

## Penyelesaian masalah

| Masalah | Cuba |
|---|---|
| Tiada baris `YouTubeHideAds:` dalam log rangka kerja | Pastikan YouTube berada dalam skop, kemudian paksa hentikannya. |
| Suis suapan nampaknya diabaikan | Muat semula suapan. |
| Rosak selepas kemas kini YouTube | Gunakan **Perihal → Keserasian & diagnostik → Laporkan masalah**. |

### SponsorBlock atau semakan kemas kini tidak pernah bersambung

Ini juga meliputi kiraan dislike dan DeArrow. Log menunjukkan `NOT_ENOUGH_SCTS`. Aplikasi penapis HTTPS menandatangani semula sambungan, dan
semakan ketelusan sijil YouTube menolaknya. Dalam AdGuard, tambahkan ini pada **Penapisan HTTPS → Pengecualian**:
`sponsor.ajay.app`, `github.com`, `returnyoutubedislikeapi.com`, `dearrow-thumb.ajay.app`. Kemudian mulakan semula YouTube.

## Cara ia berfungsi

Brainfuck memutuskan dan XAX bertindak. Sembilan dasar Brainfuck memutuskan, sebagai contoh, sama ada sesuatu komponen ialah
iklan, sama ada sesuatu pencarian boleh melangkau segmen, atau sama ada sesuatu sentuhan ialah leretan. Dasar itu dikompil lebih awal ke
AArch64 oleh [BBC](https://github.com/MrxSiN/BBC). Cangkuk, penemuan, tetapan dan rangkaian ialah satu
stor [XAX](https://github.com/MrxSiN/XAX), dikompil ke DEX. Repositori ini tiada kod sumber aplikasi Java, Kotlin atau C.

[Seni bina](docs/ARCHITECTURE_BRAINFUCK_XAX.md) · [binaan](docs/BUILD.md) · [semua dokumentasi](docs/README.md) · [bukti](evidence/README.md)

## Sokongan

Jika modul ini berguna kepada anda, anda boleh [menaja pembangunannya](https://github.com/sponsors/MrxSiN).

## Penghargaan dan lesen

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed](https://github.com/libxposed/api),
[Vector](https://github.com/JingMatrix/Vector), [SponsorBlock](https://sponsor.ajay.app),
[Return YouTube Dislike](https://returnyoutubedislike.com), [DeArrow](https://dearrow.ajay.app),
[AiSList](https://github.com/Override92/AiSList) (CC BY-NC 4.0, tidak disertakan), dan
[Morphe Patches](https://github.com/MorpheApp/morphe-patches), digunakan sebagai rujukan tingkah laku
([notis](LICENSES/Morphe-NOTICE.txt)).

GPL-3.0-or-later. Lihat [NOTICE](NOTICE) dan [asal usul upstream](docs/UPSTREAM_PROVENANCE.md).
Projek ini tidak berkaitan dengan Google atau YouTube.
