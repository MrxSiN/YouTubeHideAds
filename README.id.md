<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Bahasa Indonesia** · [Bahasa Melayu](README.ms.md)

**Modul Xposed yang menghapus iklan dari YouTube, dengan setiap keputusan ditulis dalam Brainfuck dan sisanya dalam XAX. Ya, sungguhan.**

Iklan, Shorts bersponsor, dan promosi dihapus sebelum YouTube menampilkannya, dan segmen SponsorBlock dilewati.

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#persyaratan)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!NOTE]
> YouTube mengganti nama kelas yang diobfuskasi hampir di setiap pembaruan. Modul menemukan kembali targetnya berdasarkan struktur setiap kali dimulai. Jika sebuah peran tidak ada atau ambigu, fitur itu dibiarkan apa adanya, bukan ditebak. Lihat tabel [kompatibilitas](#kompatibilitas) untuk yang benar-benar sudah diuji.

## Kenapa Brainfuck? Dan apa itu XAX?

- **Brainfuck yang memutuskan.** Apakah komponen ini iklan, apakah pemasaran Premium boleh dihapus, apakah pemutar boleh melompat ke akhir segmen sponsor, apakah usapan mengubah kecerahan. Brainfuck tidak bisa memanggil Android, Xposed, DexKit, atau JNI; ia hanya membaca dan menulis byte, dan host hanya bertindak jika jawabannya tepat dan berhasil.
- **XAX mengerjakan semua yang lain.** Hook, pencarian DexKit, refleksi, halaman setelan, serta HTTPS dan JSON untuk SponsorBlock ada dalam satu penyimpanan semantik [XAX](https://github.com/MrxSiN/XAX) yang kanonis. Compiler XAX eksternal mengubahnya menjadi DEX dan menandatangani APK. Tidak ada kode aplikasi Java, Kotlin, C, Python, atau shell di repositori ini.

Ini juga tidak lambat. Sembilan kebijakan dikompilasi lebih dulu menjadi pustaka bersama AArch64 oleh [BBC](https://github.com/MrxSiN/BBC). Tidak ada interpreter di APK.

|  | |
|---|---|
| 🧹 **Dihapus, bukan disembunyikan** | Komponen iklan diganti sebelum YouTube menatanya, dan Shorts bersponsor keluar dari feed sebelum pemutar dibuat, jadi tidak ada ruang kosong atau klip macet. |
| ⏭️ **SponsorBlock bawaan** | Pencarian prefiks dengan percobaan ulang dan cache terbatas, mode dan warna per kategori, lewati dan batalkan manual, pembuatan segmen dan pemungutan suara, pengecualian, statistik, dan pemindahan setelan. |
| 🔎 **Tahan perubahan nama** | DexKit menemukan setiap hook berdasarkan struktur setiap kali dimulai. Peran yang hilang atau ambigu tidak memasang apa pun untuk fitur itu. |
| 🧠 **Kebijakan Brainfuck yang dikompilasi** | Sembilan program yang ditulis tangan, dikompilasi ke kode native; kebijakan dan kontrol SponsorBlock diperiksa setiap kali dimulai. |
| 🛟 **Gagal dengan aman** | Jika pemeriksaan mandiri gagal, fitur itu tetap mati. Kesalahan jaringan dan jenis pemutaran yang tidak dikenal tidak pernah memicu lompatan. |
| ⚙️ **Setelan bergaya asli** | Bagian **YouTubeHideAds** sendiri di **Anda → Setelan**, di atas Akun, memakai baris YouTube sendiri, dengan setiap tombol berdiri sendiri dan halaman Kompatibilitas & diagnostik. |
| 🎛️ **SponsorBlock menyatu dengan pemutar** | Ikon SponsorBlock di samping putar otomatis membuka menu mengambang yang sama dengan roda gigi setelan pemutar; segmen diberi warna di bilah progres. |
| 📱 **Shorts lebih bersih** | Sembunyikan tombol dan panel Shorts satu per satu, dan lewati siaran langsung di feed Shorts. |
| 👆 **Kontrol geser yang mudah dibaca** | Kecerahan di kiri, volume di kanan, ditampilkan sebagai kapsul dengan ikon, level, dan nilai. |
| 🌐 **Bahasa Anda** | Mengikuti bahasa YouTube: English, 简体中文, 繁體中文, Español, Português, Русский, 日本語, 한국어, Bahasa Indonesia, dan Bahasa Melayu. |

---

## Yang dihapus

| Grup | Setelan | Default |
|---|---|---|
| Iklan | Iklan video dan Shorts · Iklan feed dan penelusuran · Promosi Premium · Promosi layar penuh | Aktif, di bawah tombol utama **Sembunyikan iklan** |
| SponsorBlock | Sponsor, promosi diri | Aktif |
| SponsorBlock | Pengingat interaksi, intro, penutup, cuplikan, pengisi, segmen non-musik | Nonaktif |
| Konten | Playables (rak game, kartu, entri Jelajahi) | Disembunyikan |
| Feed | Video pratinjau · Jelajahi topik lainnya · Postingan | Disembunyikan |
| Feed | Shorts di feed | Ditampilkan |
| Feed | Channel AI · Channel yang kemungkinan AI ([AiSList](https://github.com/Override92/AiSList)) | Nonaktif |
| Pemutar | Geser untuk kecerahan (kiri) · Geser untuk volume (kanan), hanya layar penuh | Aktif |
| Pemutar | Paksa audio asli pada video multibahasa | Aktif |
| Pemutar | Pemutaran di latar belakang, termasuk video untuk anak | Aktif |
| Shorts | Suka, komentar, bagikan, remix, simpan, suara, subscribe, judul, saran dan panel info, tombol saat dijeda | Ditampilkan (masing-masing bisa disembunyikan) |
| Shorts | Lewati Shorts live | Nonaktif |

Menonaktifkan **Sembunyikan iklan** tidak mematikan fitur konten dan pemutar. Muat ulang feed setelah mengubah tombolnya. Audio asli berlaku mulai daftar trek berikutnya dan menghormati pilihan manual. Tabel lengkap: [setelan dan default](docs/README.md#settings-and-defaults). Pemutaran di latar belakang tidak bergantung pada Sembunyikan iklan atau SponsorBlock; mulai ulang YouTube setelah mengubahnya. [Implementasi dan batas yang diuji](docs/BACKGROUND_PLAYBACK.md).

<details open>
<summary><b>🧱 Di mana setiap penghapusan terjadi</b></summary>
<br>

| Bagian | Di mana | Fungsinya |
|---|---|---|
| **Iklan video** | aktivasi dan tata letak iklan pemutar | Menekan slot iklan saat Brainfuck memastikan tanda struktural iklan dan transisi yang aman. |
| **Iklan feed, penelusuran, dan belanja** | parser komponen, ditemukan oleh DexKit | Mengganti komponen berbayar yang terkonfirmasi dengan komponen kosong milik YouTube. |
| **Shorts bersponsor** | respons, penyisipan, dan data awal pemutar Shorts | Menghapus entri iklan video/gambar beserta data pelacakannya sebelum pemutar ada. |
| **Premium, layar penuh, panel** | tampilan penawaran, dialog layar penuh, panel interaksi menurut pengenal bertipe | Menyembunyikan tampilan pemasaran tanpa menyentuh hak atau pengelolaan langganan. |
| **Bagian feed, Playables, channel AI, komponen Shorts** | hook komponen yang sama | Hanya menghapus bagian, kartu, atau tombol yang cocok; baris channel dan playlist tetap ada. |
| **SponsorBlock** | jembatan lompat/durasi pemutar dan bilah progres asli | Pencarian prefiks terbatas, mode kategori, tanda berwarna, kontrol manual, dan tindakan komunitas yang eksplisit. |

</details>

---

## Status

**v1.1.0** (versionCode 153) adalah rilis pertama sejak 1.0.0. Rilis ini menambahkan pemutaran di latar belakang, bagian sendiri di Setelan YouTube, halaman Kompatibilitas & diagnostik, kontrol SponsorBlock bergaya YouTube, Sembunyikan komponen Shorts, Lewati Shorts live, kontrol geser yang didesain ulang, dan sembilan bahasa lagi. Modul ini juga jauh lebih ringan di ponsel: panggilan kebijakan Brainfuck tidak lagi membuka ulang APK, dan hasil DexKit disimpan dalam cache, sehingga YouTube terbuka sekitar 0,35 detik lebih cepat setelah peluncuran pertama. [Pemeriksaan perangkat](evidence/device_perf_20261028/README.md).

Build pengembangan di antara kedua rilis (111 sampai 153) tercantum di [log perubahan](CHANGELOG.md), dengan bukti masing-masing di [evidence](evidence/README.md).

### Kompatibilitas

Diuji pada Pixel 8 Pro dengan Android 17 dan Vector 2.2 (libxposed API 102). Pernah mencoba pengaturan lain? Silakan buka pull request untuk menambahkan baris.

| YouTube | Modul | Status |
|---|---|---|
| 21.42.243 | 1.1.0 | ✅ Berfungsi |
| 21.41.525 | 1.0.0 | ✅ Berfungsi |

### Batasan yang diketahui

- Promosi Premium, layar penuh, dan panel interaksi baru dihapus dalam uji hook terkendali; kasus yang dikirim secara nyata belum muncul.
- Rak video pratinjau dan "Jelajahi topik lainnya" hanya dikenali dari judul berbahasa Inggris.
- Daftar saluran AI dikelola komunitas dan bisa salah menggolongkan saluran, karena itu nonaktif secara default.
- Pemutaran di latar belakang memerlukan mulai ulang YouTube setelah sakelarnya diubah dan membiarkan Shorts ditangani YouTube. Kontrol Bluetooth dan panggilan masuk belum diuji.
- Pengiriman dan pemungutan suara SponsorBlock belum dicoba di server sungguhan. Lihat [fitur dan batasan](docs/SPONSORBLOCK_API_RESEARCH.md).
- Lewati Shorts live belum menemui Short live sungguhan; fitur ini, pil geser, dan penggantian bahasa YouTube diperiksa dengan probe pengembangan.
- Halaman modul hanya diperiksa dalam tema gelap. Tema terang, tablet, dan tata letak kanan-ke-kiri belum diuji.
- Peluncuran pertama setelah YouTube atau modul diperbarui membangun ulang cache hook dan sekitar 0,4 detik lebih lambat.
- Hanya arm64-v8a. Hanya pengaturan dan versi YouTube di atas yang pernah dicoba; LSPatch belum.

Rincian: [cakupan fitur](docs/FEATURE_COVERAGE.md) dan [kompatibilitas](docs/COMPATIBILITY.md).

## Persyaratan

| | |
|---|---|
| **Android** | 9.0 (API 28) atau lebih baru, arm64 |
| **Aplikasi** | YouTube (`com.google.android.youtube`) |
| **Framework** | [Vector](https://github.com/JingMatrix/Vector) atau LSPosed dengan libxposed API 102 |
| **Root** | Dibutuhkan Vector/LSPosed; modul sendiri tidak meminta izin apa pun |

## Pemasangan

```
1. Pasang APK dari Releases atau repositori modul Xposed
2. Aktifkan YouTubeHideAds di Vector atau LSPosed dengan cakupan YouTube
3. Paksa berhenti YouTube sekali, lalu buka
```

Unduh dari [GitHub Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) atau [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads). Setelan ada di **YouTube → Anda → Setelan → YouTubeHideAds**. Preferensi dan cache AI tersimpan di data YouTube sendiri, jadi menghapus data YouTube akan mengatur ulangnya.

Log framework menampilkan apa yang terjadi pada baris yang diawali `YouTubeHideAds:`:

```text
Ad policy self-check passed (70 cases)
SponsorBlock self-check passed (277 cases)
Ad component hook installed
Shorts feed removal hooks installed (paired, insert, response, restore, seed)
Video ad suppressed
```

---

## Cara kerja

```
YouTube process
  XAX module (DEX) ──────────────► Bfp1Bridge.run ──JNI──► lib<policy>.so
  hooks, DexKit roles               input bytes            nine AOT Brainfuck policies
  settings page, HTTPS/JSON              ▲                       │
  typed actions                          │   exact reply only    │
                                         └───────────────────────┘
```

Satu aturan menentukan letak kode: **jika menyentuh YouTube, Android, jaringan, atau JNI, XAX yang mengerjakan; jika memutuskan apakah bertindak atas temuan XAX, Brainfuck yang memutuskan.** Rincian pustaka kebijakan, tata letak byte, dan pencarian hook ada di [`docs/BRAINFUCK_ABI.md`](docs/BRAINFUCK_ABI.md) dan [`docs/DEXKIT_RESOLUTION.md`](docs/DEXKIT_RESOLUTION.md).

Pengambilan segmen otomatis hanya mengirim prefiks SHA-256 empat digit heksadesimal dari ID video. Ukuran respons, jumlah rekaman, dan batas waktu dibatasi, dan pengalihan dinonaktifkan. Pengiriman dan suara manual mengirim data yang diperlukan dan identitas pribadi ke server pilihan; pelaporan tontonan nonaktif secara default dan ekspor setelan tidak menyertakan ID pribadi secara default.

---

## Build

Repositori ini tidak memiliki skrip build. Rilis dibuat dengan alat eksternal:

```text
BBC          source/**/*.bf  ->  lib<policy>.so (AArch64)
AAPT2        source/branding ->  branding.apk (static resources only)
XAX          source/xax/youtubehideads.xax + pinned inputs -> signed APK
```

Setiap input dipatok dengan BLAKE3 di penyimpanan, jadi input yang tidak cocok menggagalkan build. Untuk build ulang, gunakan [XAX](https://github.com/MrxSiN/XAX) dengan profil Android libxposed (commit `3cca599` atau snapshot branding-v2 yang kompatibel). Langkahnya ada di [`docs/BUILD.md`](docs/BUILD.md).

## Pemecahan masalah

| Masalah | Coba |
|---|---|
| Tidak ada baris log modul | Pastikan modul aktif dengan cakupan YouTube, lalu paksa berhenti YouTube. |
| `UnsatisfiedLinkError` tepat setelah pembaruan | Tunggu pemasangan selesai, lalu paksa berhenti dan buka lagi YouTube. |
| Pemeriksaan mandiri melaporkan `false` | Fitur itu tetap mati. Laporkan baris log `YouTubeHideAds:`. |
| Tombol feed seperti diabaikan | Muat ulang feed; penghapusan berlaku untuk komponen yang baru dimuat. |
| Rusak setelah pembaruan YouTube | YouTube mungkin mengubah kelas internalnya. Laporkan log beserta versi YouTube, atau salin laporan dari Kompatibilitas & diagnostik. |

## Kredit

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed API](https://github.com/libxposed/api), [Vector](https://github.com/JingMatrix/Vector), [LSPosed](https://github.com/LSPosed/LSPosed), [XAX](https://github.com/MrxSiN/XAX), [XAX-MCP](https://github.com/MrxSiN/XAX-MCP), [BBC](https://github.com/MrxSiN/BBC), [SponsorBlock](https://sponsor.ajay.app), [Override92/AiSList](https://github.com/Override92/AiSList), dan [Morphe Patches](https://github.com/MorpheApp/morphe-patches) ([pemberitahuan yang dipertahankan](LICENSES/Morphe-NOTICE.txt)). Materi proyek yang baru ditulis berlisensi GPL-3.0-or-later; lihat [NOTICE](NOTICE) untuk ketentuan pihak ketiga.

## Penafian

Tidak berafiliasi dengan, didukung, atau disponsori oleh Google LLC atau YouTube. Disediakan untuk penggunaan edukasi dan pribadi. Pembaruan YouTube dapat merusak hook tanpa pemberitahuan.
