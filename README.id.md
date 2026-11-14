<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Bahasa Indonesia** · [Bahasa Melayu](README.ms.md)

**Modul Xposed yang menghapus iklan dari YouTube, dengan setiap keputusan ditulis dalam Brainfuck dan sisanya dalam XAX.**

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](README.md#install)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-EA4AAA?logo=githubsponsors&logoColor=fff&style=for-the-badge)](https://github.com/sponsors/MrxSiN)

<img src="docs/images/settings-ads.png" width="240" alt="Ads and SponsorBlock settings">
<img src="docs/images/settings-player.png" width="240" alt="Player settings">
<img src="docs/images/settings-feed.png" width="240" alt="Feed and blacklist settings">

</div>

## Fitur

- **Iklan dihapus sebelum tampil:** iklan video dan Shorts, iklan di beranda dan pencarian, promosi Premium dan layar penuh. Tanpa ruang kosong.
- **SponsorBlock bawaan**, dengan segmen berwarna di bilah geser dan tombol di pemutar untuk lompat manual, memberi suara, dan mengirim segmen.
- **Pemutar:** kecepatan dan kualitas default, bahasa teks pilihan, putar di latar belakang, audio asli, ingat posisi siaran langsung, ketuk untuk mencari, ulang, tombol kecepatan, dan jumlah Return YouTube Dislike.
- **Gestur:** geser untuk kecerahan di kiri dan volume di kanan saat layar penuh, tidak pernah di atas live chat, panel, atau lembar Video lainnya.
- **Beranda:** sembunyikan rak Shorts, postingan, pratinjau, Playables, dan kanal AI, daftar hitam kanal dan kata kunci, serta thumbnail DeArrow.
- **Shorts:** sembunyikan tombol dan panel tertentu, dan lewati Shorts siaran langsung.
- **Satu halaman setelan** di **Anda → Setelan → YouTube Hide Ads**, dalam bahasa YouTube (10 bahasa).

Tambahan baru nonaktif secara default. Semua setelan dan nilai defaultnya tercantum di [dokumentasi](docs/README.md#settings-and-defaults).

## Pemasangan

1. Unduh APK dari [Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) atau [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads).
2. Aktifkan di [Vector](https://github.com/JingMatrix/Vector) atau LSPosed (libxposed API 102) dengan YouTube dalam cakupan.
3. Paksa berhenti YouTube lalu buka lagi.

Membutuhkan Android 9 atau lebih baru di arm64, dan root untuk framework. Modulnya sendiri tidak meminta izin apa pun.

## Kompatibilitas

| YouTube | Modul | Status |
|---|---|---|
| 21.45.88 | 1.3.0 (build 157) | ✅ Berfungsi |
| 21.43.523 | 1.2.0 | ✅ Berfungsi |
| 21.42.243 | 1.1.0 | ✅ Berfungsi |

Diuji di Pixel 8 Pro dengan Android 17 dan Vector 2.2. YouTube mengganti nama kelas internalnya di sebagian besar
pembaruan. Modul menemukan lagi targetnya berdasarkan strukturnya, dan mematikan fitur daripada menebak
saat tidak bisa. Riwayat: [catatan perubahan](CHANGELOG.md) · detail: [kompatibilitas](docs/COMPATIBILITY.md).

## Batasan yang diketahui

- Aplikasi penyaring HTTPS seperti AdGuard dapat memblokir SponsorBlock, pemeriksaan pembaruan, jumlah dislike, dan DeArrow; lihat [di bawah](README.md#sponsorblock-or-update-check-never-connects).
- DeArrow mengganti thumbnail, bukan judul. Menu kecepatan bawaan YouTube tetap menampilkan 1x setelah kecepatan default diterapkan.
- Kualitas default di data seluler, Shorts siaran langsung, dan pemblokiran teks otomatis belum diuji di ponsel.
- Diperiksa hanya di tema gelap pada satu ponsel. Teks baru 1.3.0 dalam bahasa Inggris.

Semua yang sudah dan belum diuji: [cakupan fitur](docs/FEATURE_COVERAGE.md).

## Pemecahan masalah

| Masalah | Coba |
|---|---|
| Tidak ada baris `YouTubeHideAds:` di log framework | Pastikan YouTube ada dalam cakupan, lalu paksa berhenti. |
| Tombol beranda sepertinya diabaikan | Muat ulang beranda. |
| Rusak setelah pembaruan YouTube | Gunakan **Tentang → Kompatibilitas & diagnostik → Laporkan masalah**. |

### SponsorBlock atau pemeriksaan pembaruan tidak pernah tersambung

Ini juga berlaku untuk jumlah dislike dan DeArrow. Log menampilkan `NOT_ENOUGH_SCTS`. Aplikasi penyaring HTTPS menandatangani ulang koneksi, dan
pemeriksaan certificate transparency milik YouTube menolaknya. Di AdGuard, tambahkan ini ke **Penyaringan HTTPS → Pengecualian**:
`sponsor.ajay.app`, `github.com`, `returnyoutubedislikeapi.com`, `dearrow-thumb.ajay.app`. Lalu mulai ulang YouTube.

## Cara kerja

Brainfuck memutuskan dan XAX bertindak. Sembilan kebijakan Brainfuck memutuskan, misalnya, apakah sebuah komponen adalah
iklan, apakah sebuah lompatan boleh melewati segmen, atau apakah sebuah sentuhan adalah gesekan. Kebijakan itu dikompilasi lebih dulu ke
AArch64 oleh [BBC](https://github.com/MrxSiN/BBC). Hook, penemuan, setelan, dan jaringan adalah satu
store [XAX](https://github.com/MrxSiN/XAX), dikompilasi ke DEX. Repositori ini tidak punya kode sumber aplikasi Java, Kotlin, atau C.

[Arsitektur](docs/ARCHITECTURE_BRAINFUCK_XAX.md) · [build](docs/BUILD.md) · [semua dokumentasi](docs/README.md) · [bukti](evidence/README.md)

## Dukungan

Kalau modul ini berguna untuk Anda, Anda bisa [mensponsori pengembangannya](https://github.com/sponsors/MrxSiN).

## Kredit dan lisensi

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed](https://github.com/libxposed/api),
[Vector](https://github.com/JingMatrix/Vector), [SponsorBlock](https://sponsor.ajay.app),
[Return YouTube Dislike](https://returnyoutubedislike.com), [DeArrow](https://dearrow.ajay.app),
[AiSList](https://github.com/Override92/AiSList) (CC BY-NC 4.0, tidak disertakan), dan
[Morphe Patches](https://github.com/MorpheApp/morphe-patches), dipakai sebagai acuan perilaku
([pemberitahuan](LICENSES/Morphe-NOTICE.txt)).

GPL-3.0-or-later. Lihat [NOTICE](NOTICE) dan [asal-usul upstream](docs/UPSTREAM_PROVENANCE.md).
Proyek ini tidak berafiliasi dengan Google atau YouTube.
