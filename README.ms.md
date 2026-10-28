<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · **Bahasa Melayu**

**Modul Xposed yang membuang iklan daripada YouTube, dengan setiap keputusan ditulis dalam Brainfuck dan selebihnya dalam XAX. Ya, betul.**

Iklan, Shorts tajaan dan promosi dibuang sebelum YouTube memaparkannya, dan segmen SponsorBlock dilangkau.

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#keperluan)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!NOTE]
> YouTube menukar nama kelas yang dikaburkan hampir setiap kali dikemas kini. Modul ini mencari semula sasarannya berdasarkan struktur setiap kali dimulakan. Jika sesuatu peranan tiada atau tidak jelas, ciri itu dibiarkan seperti asal dan tidak diteka. Lihat jadual [keserasian](#keserasian) untuk perkara yang benar-benar telah diuji.

## Kenapa Brainfuck? Dan apa itu XAX?

- **Brainfuck yang membuat keputusan.** Sama ada komponen ini iklan, sama ada pemasaran Premium boleh dibuang, sama ada pemain boleh melompat ke hujung segmen tajaan, sama ada leretan menukar kecerahan. Brainfuck tidak boleh memanggil Android, Xposed, DexKit atau JNI; ia hanya membaca dan menulis bait, dan hos hanya bertindak apabila jawapannya tepat dan berjaya.
- **XAX melakukan semua yang lain.** Hook, carian DexKit, refleksi, halaman tetapan serta HTTPS dan JSON untuk SponsorBlock berada dalam satu storan semantik [XAX](https://github.com/MrxSiN/XAX) yang kanonik. Pengkompil XAX luaran menukarkannya kepada DEX dan menandatangani APK. Tiada kod aplikasi Java, Kotlin, C, Python atau shell dalam repositori ini.

Ia juga tidak perlahan. Sembilan polisi dikompil lebih awal kepada pustaka kongsi AArch64 oleh [BBC](https://github.com/MrxSiN/BBC). Tiada penterjemah dalam APK.

|  | |
|---|---|
| 🧹 **Dibuang, bukan disorok** | Komponen iklan diganti sebelum YouTube menyusunnya, dan Shorts tajaan dikeluarkan daripada suapan sebelum pemain dibina, jadi tiada ruang kosong atau klip tersekat. |
| ⏭️ **SponsorBlock terbina dalam** | Carian awalan dengan cubaan semula dan cache terhad, mod dan warna setiap kategori, langkau dan buat asal secara manual, penciptaan segmen dan undian, pengecualian, statistik dan pemindahan tetapan. |
| 🔎 **Tahan pertukaran nama** | DexKit mencari setiap hook berdasarkan struktur setiap kali dimulakan. Peranan yang tiada atau tidak jelas tidak memasang apa-apa untuk ciri itu. |
| 🧠 **Polisi Brainfuck yang dikompil** | Sembilan atur cara yang ditulis sendiri, dikompil kepada kod asli; polisi dan kawalan SponsorBlock disemak setiap kali dimulakan. |
| 🛟 **Gagal dengan selamat** | Jika semakan kendiri gagal, ciri itu kekal dimatikan. Ralat rangkaian dan jenis main balik yang tidak dikenali tidak sekali-kali menyebabkan lompatan. |
| ⚙️ **Tetapan bergaya asli** | Bahagian **YouTubeHideAds** sendiri dalam **Anda → Tetapan**, di atas Akaun, menggunakan baris YouTube sendiri, dengan setiap suis berdiri sendiri dan halaman Keserasian & diagnostik. |
| 🎛️ **SponsorBlock dalam pemain** | Ikon SponsorBlock di sebelah automain membuka menu terapung yang sama seperti gear tetapan pemain; segmen diwarnakan pada bar carian. |
| 📱 **Shorts lebih kemas** | Sembunyikan butang dan panel Shorts satu demi satu, dan langkau strim langsung dalam suapan Shorts. |
| 👆 **Kawalan leret yang mudah dibaca** | Kecerahan di kiri, kelantangan di kanan, dipaparkan sebagai kapsul dengan ikon, aras dan nilai. |
| 🌐 **Bahasa anda** | Mengikut bahasa YouTube: English, 简体中文, 繁體中文, Español, Português, Русский, 日本語, 한국어, Bahasa Indonesia dan Bahasa Melayu. |

---

## Apa yang dibuang

| Kumpulan | Tetapan | Lalai |
|---|---|---|
| Iklan | Iklan video dan Shorts · Iklan suapan dan carian · Promosi Premium · Promosi skrin penuh | Hidup, di bawah suis utama **Sembunyikan iklan** |
| SponsorBlock | Penaja, promosi diri | Hidup |
| SponsorBlock | Peringatan interaksi, pengenalan, penutup, pratonton, pengisi, segmen bukan muzik | Mati |
| Kandungan | Playables (rak permainan, kad, entri Teroka) | Disembunyikan |
| Suapan | Video pratonton · Teroka lebih banyak topik · Siaran | Disembunyikan |
| Suapan | Shorts dalam suapan | Dipaparkan |
| Suapan | Saluran AI · Saluran yang mungkin AI ([AiSList](https://github.com/Override92/AiSList)) | Mati |
| Pemain | Leret untuk kecerahan (kiri) · Leret untuk kelantangan (kanan), skrin penuh sahaja | Hidup |
| Pemain | Paksa audio asal pada video berbilang bahasa | Hidup |
| Pemain | Main balik latar belakang, termasuk video untuk kanak-kanak | Hidup |
| Shorts | Suka, ulasan, kongsi, remiks, simpan, bunyi, langgan, tajuk, cadangan dan panel maklumat, butang semasa dijeda | Dipaparkan (setiap satu boleh disembunyikan) |
| Shorts | Langkau Shorts langsung | Mati |

Mematikan **Sembunyikan iklan** tidak mematikan ciri kandungan dan pemain. Muat semula suapan selepas menukar suisnya. Audio asal berkuat kuasa mulai senarai trek seterusnya dan menghormati pilihan manual. Jadual penuh: [tetapan dan nilai lalai](docs/README.md#settings-and-defaults). Main balik latar belakang tidak bergantung pada Sembunyikan iklan atau SponsorBlock; mulakan semula YouTube selepas menukarnya. [Pelaksanaan dan had yang diuji](docs/BACKGROUND_PLAYBACK.md).

<details open>
<summary><b>🧱 Di mana setiap pembuangan berlaku</b></summary>
<br>

| Bahagian | Di mana | Fungsinya |
|---|---|---|
| **Iklan video** | pengaktifan dan susun atur iklan pemain | Menahan slot iklan apabila Brainfuck mengesahkan tanda struktur iklan dan peralihan yang selamat. |
| **Iklan suapan, carian dan beli-belah** | penghurai komponen, ditemui oleh DexKit | Menggantikan komponen berbayar yang disahkan dengan komponen kosong milik YouTube. |
| **Shorts tajaan** | respons, sisipan dan data awal pemain Shorts | Membuang entri iklan video/imej bersama data penjejakannya sebelum pemain wujud. |
| **Premium, skrin penuh, panel** | paparan tawaran, dialog skrin penuh, panel interaksi mengikut pengecam bertaip | Menyembunyikan paparan pemasaran tanpa menyentuh hak atau pengurusan langganan. |
| **Bahagian suapan, Playables, saluran AI, komponen Shorts** | hook komponen yang sama | Hanya membuang bahagian, kad atau butang yang sepadan; baris saluran dan senarai main kekal. |
| **SponsorBlock** | jambatan lompat/tempoh pemain dan bar carian asli | Carian awalan terhad, mod kategori, tanda berwarna, kawalan manual dan tindakan komuniti yang jelas. |

</details>

---

## Status

**v1.1.0** (versionCode 153) ialah keluaran pertama sejak 1.0.0. Keluaran ini menambah main balik latar belakang, bahagian sendiri dalam Tetapan YouTube, halaman Keserasian & diagnostik, kawalan SponsorBlock bergaya YouTube, Sembunyikan komponen Shorts, Langkau Shorts langsung, kawalan leret yang direka semula dan sembilan lagi bahasa. Ia juga jauh lebih ringan pada telefon: panggilan dasar Brainfuck tidak lagi membuka semula APK, dan hasil DexKit disimpan dalam cache, jadi YouTube dibuka kira-kira 0.35 saat lebih cepat selepas pelancaran pertama. [Semakan peranti](evidence/device_perf_20261028/README.md).

Binaan pembangunan antara kedua-dua keluaran (111 hingga 153) disenaraikan dalam [log perubahan](CHANGELOG.md), dengan bukti setiap satu dalam [evidence](evidence/README.md).

### Keserasian

Diuji pada Pixel 8 Pro dengan Android 17 dan Vector 2.2 (libxposed API 102). Pernah mencuba persediaan lain? Sila buka pull request untuk menambah baris.

| YouTube | Modul | Status |
|---|---|---|
| 21.42.243 | 1.1.0 | ✅ Berfungsi |
| 21.41.525 | 1.0.0 | ✅ Berfungsi |

### Had yang diketahui

- Promosi Premium, skrin penuh dan panel penglibatan hanya dibuang dalam ujian hook terkawal; kes yang dihantar secara sebenar belum muncul.
- Rak video pratonton dan "Terokai lebih banyak topik" hanya dikenali melalui tajuk bahasa Inggeris.
- Senarai saluran AI diselenggara komuniti dan boleh tersalah kelaskan saluran, sebab itu ia dimatikan secara lalai.
- Main balik latar belakang memerlukan YouTube dimulakan semula selepas suisnya diubah dan membiarkan Shorts kepada YouTube. Kawalan Bluetooth dan panggilan masuk belum diuji.
- Penghantaran dan undian SponsorBlock belum dicuba pada pelayan sebenar. Lihat [ciri dan had](docs/SPONSORBLOCK_API_RESEARCH.md).
- Langkau Shorts langsung belum menemui Short langsung sebenar; ciri ini, pil leret dan penukaran bahasa YouTube disemak dengan probe pembangunan.
- Halaman modul hanya disemak dalam tema gelap. Tema cerah, tablet dan susun atur kanan-ke-kiri belum diuji.
- Pelancaran pertama selepas YouTube atau modul dikemas kini membina semula cache hook dan lebih perlahan kira-kira 0.4 saat.
- arm64-v8a sahaja. Hanya persediaan dan versi YouTube di atas yang pernah dicuba; LSPatch belum.

Butiran: [liputan ciri](docs/FEATURE_COVERAGE.md) dan [keserasian](docs/COMPATIBILITY.md).

## Keperluan

| | |
|---|---|
| **Android** | 9.0 (API 28) atau lebih baharu, arm64 |
| **Aplikasi** | YouTube (`com.google.android.youtube`) |
| **Rangka kerja** | [Vector](https://github.com/JingMatrix/Vector) atau LSPosed dengan libxposed API 102 |
| **Root** | Diperlukan oleh Vector/LSPosed; modul ini sendiri tidak meminta sebarang kebenaran |

## Pemasangan

```
1. Pasang APK daripada Releases atau repositori modul Xposed
2. Dayakan YouTubeHideAds dalam Vector atau LSPosed dengan skop YouTube
3. Paksa henti YouTube sekali, kemudian bukanya
```

Muat turun daripada [GitHub Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) atau [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads). Tetapan berada di **YouTube → Anda → Tetapan → YouTubeHideAds**. Pilihan dan cache AI disimpan dalam data YouTube sendiri, jadi mengosongkan data YouTube akan menetapkannya semula.

Log rangka kerja menunjukkan apa yang berlaku dalam baris yang bermula dengan `YouTubeHideAds:`:

```text
Ad policy self-check passed (70 cases)
SponsorBlock self-check passed (277 cases)
Ad component hook installed
Shorts feed removal hooks installed (paired, insert, response, restore, seed)
Video ad suppressed
```

---

## Cara ia berfungsi

```
YouTube process
  XAX module (DEX) ──────────────► Bfp1Bridge.run ──JNI──► lib<policy>.so
  hooks, DexKit roles               input bytes            nine AOT Brainfuck policies
  settings page, HTTPS/JSON              ▲                       │
  typed actions                          │   exact reply only    │
                                         └───────────────────────┘
```

Satu peraturan menentukan letak kod: **jika ia menyentuh YouTube, Android, rangkaian atau JNI, XAX yang melakukannya; jika ia memutuskan sama ada bertindak atas penemuan XAX, Brainfuck yang memutuskan.** Butiran pustaka polisi, susun atur bait dan carian hook ada dalam [`docs/BRAINFUCK_ABI.md`](docs/BRAINFUCK_ABI.md) dan [`docs/DEXKIT_RESOLUTION.md`](docs/DEXKIT_RESOLUTION.md).

Pengambilan segmen automatik hanya menghantar awalan SHA-256 empat digit perenambelasan daripada ID video. Saiz respons, bilangan rekod dan had masa adalah terhad, dan ubah hala dimatikan. Serahan dan undian manual menghantar data yang diperlukan serta identiti peribadi ke pelayan pilihan; laporan tontonan dimatikan secara lalai dan eksport tetapan tidak menyertakan ID peribadi secara lalai.

---

## Binaan

Repositori ini tiada skrip binaan. Keluaran dibina dengan alat luaran:

```text
BBC          source/**/*.bf  ->  lib<policy>.so (AArch64)
AAPT2        source/branding ->  branding.apk (static resources only)
XAX          source/xax/youtubehideads.xax + pinned inputs -> signed APK
```

Setiap input dipaku dengan BLAKE3 dalam storan, jadi input yang tidak sepadan menggagalkan binaan. Untuk membina semula, gunakan [XAX](https://github.com/MrxSiN/XAX) dengan profil Android libxposed (commit `3cca599` atau syot kilat branding-v2 yang serasi). Langkahnya ada dalam [`docs/BUILD.md`](docs/BUILD.md).

## Penyelesaian masalah

| Masalah | Cuba |
|---|---|
| Tiada baris log modul | Pastikan modul didayakan dengan skop YouTube, kemudian paksa henti YouTube. |
| `UnsatisfiedLinkError` sejurus selepas kemas kini | Tunggu pemasangan selesai, kemudian paksa henti dan buka semula YouTube. |
| Semakan kendiri melaporkan `false` | Ciri itu kekal dimatikan. Laporkan baris log `YouTubeHideAds:`. |
| Suis suapan seperti tidak berkesan | Muat semula suapan; pembuangan berkuat kuasa untuk komponen yang baru dimuatkan. |
| Rosak selepas kemas kini YouTube | YouTube mungkin menukar kelas dalamannya. Laporkan log bersama versi YouTube, atau salin laporan daripada Keserasian & diagnostik. |

## Penghargaan

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed API](https://github.com/libxposed/api), [Vector](https://github.com/JingMatrix/Vector), [LSPosed](https://github.com/LSPosed/LSPosed), [XAX](https://github.com/MrxSiN/XAX), [XAX-MCP](https://github.com/MrxSiN/XAX-MCP), [BBC](https://github.com/MrxSiN/BBC), [SponsorBlock](https://sponsor.ajay.app), [Override92/AiSList](https://github.com/Override92/AiSList) dan [Morphe Patches](https://github.com/MorpheApp/morphe-patches) ([notis yang dikekalkan](LICENSES/Morphe-NOTICE.txt)). Bahan projek yang baharu ditulis berlesen GPL-3.0-or-later; lihat [NOTICE](NOTICE) untuk terma pihak ketiga.

## Penafian

Tidak bergabung dengan, disokong atau ditaja oleh Google LLC atau YouTube. Disediakan untuk kegunaan pendidikan dan peribadi. Kemas kini YouTube boleh merosakkan hook tanpa notis.
