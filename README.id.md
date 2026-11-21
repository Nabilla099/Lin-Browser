<p align="center">
  <img src="assets/lin-browser.gif" alt="Lin Browser" width="320">
</p>

<h1 align="center">Lin Browser</h1>

<p align="center">
  Browser web untuk Android yang cepat, ringan, dan menjaga privasi, ditenagai oleh <b>Gecko</b>.
</p>

<p align="center">
  <img alt="Mesin: Gecko" src="https://img.shields.io/badge/mesin-Gecko-000000?style=flat-square&labelColor=ffd400">
  <img alt="Android 6.0+" src="https://img.shields.io/badge/android-6.0%2B-000000?style=flat-square&labelColor=ffd400">
  <img alt="ARM 32/64-bit" src="https://img.shields.io/badge/arm-32%20%2F%2064--bit-000000?style=flat-square&labelColor=ffd400">
  <img alt="Lisensi: MPL 2.0" src="https://img.shields.io/badge/lisensi-MPL--2.0-000000?style=flat-square&labelColor=ffd400">
</p>

<p align="center">
  <a href="README.md">English</a> &nbsp;·&nbsp; <b>Bahasa Indonesia</b>
</p>

---

## Ringkasan

Lin Browser membawa mesin Gecko ke Android dalam kemasan yang lebih ramping. Standar web dan performa JavaScript Gecko tetap utuh, aktivitas latar belakang dikurangi, dan ekosistem add-on dibuka sehingga Anda bisa memasang ekstensi yang Anda butuhkan.

## Fitur

| | |
|---|---|
| **Mesin Gecko** | Dukungan standar web penuh dengan mesin render dan JavaScript yang sama seperti Firefox. |
| **Add-on terbuka** | Telusuri dan pasang add-on dari addons.mozilla.org, atau impor berkas add-on (`.xpi`) dari perangkat Anda. |
| **Memori lebih hemat** | Proses konten lebih sedikit dan cache maju/mundur lebih kecil. |
| **Privat secara bawaan** | Telemetri dan studi dimatikan sejak awal. |
| **Tenang di latar belakang** | Tanpa prefetch jaringan spekulatif dan tanpa crash reporter. |
| **Jalan di perangkat lama** | Mendukung Android 6.0 ke atas. Satu APK berjalan di ponsel ARM 32-bit maupun 64-bit. |

## Instalasi

1. Buka halaman [**Releases**](../../releases) di ponsel Anda dan unduh `lin-browser-<versi>.apk`.
2. Izinkan browser atau pengelola berkas Anda **memasang aplikasi dari sumber tidak dikenal** saat Android meminta.
3. Buka APK yang sudah diunduh lalu ketuk **Pasang**.

Satu APK untuk semua perangkat yang didukung, jadi tidak perlu memilih antara versi 32-bit dan 64-bit. Sebagian kecil ponsel terbaru sudah tidak mendukung aplikasi 32-bit; jika Android menyatakan aplikasi tidak kompatibel, berarti perangkat Anda tidak didukung.

## Add-on

- **Unduh:** buka pengelola add-on dari menu utama, atau kunjungi [addons.mozilla.org](https://addons.mozilla.org/android/) dan pasang add-on dari halamannya.
- **Impor:** pilih berkas `.xpi` dari penyimpanan perangkat di pengelola add-on.

Add-on ditandatangani dan diverifikasi oleh Mozilla. Pasang ekstensi hanya dari sumber yang Anda percaya.

## Pembaruan

Lin Browser tidak memperbarui dirinya sendiri. Unduh APK baru dari [Releases](../../releases) lalu pasang di atas versi lama; data Anda tetap aman.

## Struktur repo

| Jalur | Fungsi |
|---|---|
| `mozconfig.android` | Konfigurasi mesin |
| `prefs/` | Pengaturan bawaan |
| `android/` | Kustomisasi aplikasi |
| `assets/` | Logo dan ikon peluncur |

## Atribusi

Lin Browser dibangun dari source code Gecko dan Firefox for Android yang dirilis bersama Firefox 143, berlisensi [Mozilla Public License 2.0](https://www.mozilla.org/MPL/2.0/).
Firefox dan Gecko adalah merek dagang atau proyek Mozilla Foundation dan Mozilla Corporation. Lin Browser adalah proyek independen dan tidak berafiliasi dengan maupun didukung oleh Mozilla.
