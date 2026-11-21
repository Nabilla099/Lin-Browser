<p align="center">
  <img src="assets/lin-browser.gif" alt="Lin Browser" width="320">
</p>

<h1 align="center">Lin Browser</h1>

<p align="center">
  A fast, lightweight, privacy-minded web browser for Android, powered by <b>Gecko</b>.
</p>

<p align="center">
  <img alt="Engine: Gecko" src="https://img.shields.io/badge/engine-Gecko-000000?style=flat-square&labelColor=ffd400">
  <img alt="Android 6.0+" src="https://img.shields.io/badge/android-6.0%2B-000000?style=flat-square&labelColor=ffd400">
  <img alt="ARM 32/64-bit" src="https://img.shields.io/badge/arm-32%20%2F%2064--bit-000000?style=flat-square&labelColor=ffd400">
  <img alt="License: MPL 2.0" src="https://img.shields.io/badge/license-MPL--2.0-000000?style=flat-square&labelColor=ffd400">
</p>

<p align="center">
  <b>English</b> &nbsp;·&nbsp; <a href="README.id.md">Bahasa Indonesia</a>
</p>

---

## Overview

Lin Browser brings the Gecko engine to Android in a leaner package. It keeps Gecko's standards-compliant rendering and JavaScript performance, trims background activity, and opens up the add-on ecosystem so you can install the extensions you want.

## Features

| | |
|---|---|
| **Gecko engine** | Full web-standards support with the same rendering and JavaScript engine used by Firefox. |
| **Open add-ons** | Browse and install add-ons from addons.mozilla.org, or import an add-on file (`.xpi`) from your device. |
| **Lower memory use** | Fewer content processes and a smaller back/forward cache. |
| **Private by default** | Telemetry and studies are disabled out of the box. |
| **Quiet in the background** | No speculative network prefetching and no crash reporter. |
| **Works on older devices** | Supports Android 6.0 and newer. A single APK runs on both 32-bit and 64-bit ARM phones. |

## Installation

1. Open the [**Releases**](../../releases) page on your phone and download `lin-browser-<version>.apk`.
2. Allow your browser or file manager to **install unknown apps** when Android asks.
3. Open the downloaded APK and tap **Install**.

One APK covers every supported device, so there is no need to choose between 32-bit and 64-bit versions. A small number of very recent phones have dropped support for 32-bit apps; if Android reports that the app is not compatible, your device is not supported.

## Add-ons

- **Download:** open the add-ons manager from the main menu, or visit [addons.mozilla.org](https://addons.mozilla.org/android/) and install any add-on from its page.
- **Import:** choose an `.xpi` file from your device storage in the add-ons manager.

Add-ons are signed and verified by Mozilla. Only install extensions from sources you trust.

## Updates

Lin Browser does not update itself. Download the new APK from [Releases](../../releases) and install it over the old version; your data is kept.

## Repository layout

| Path | Purpose |
|---|---|
| `mozconfig.android` | Engine configuration |
| `prefs/` | Default preferences |
| `android/` | App customisation |
| `assets/` | Logo and launcher icons |

## Attribution

Lin Browser is built from the Gecko and Firefox for Android source code released with Firefox 143, which is licensed under the [Mozilla Public License 2.0](https://www.mozilla.org/MPL/2.0/).
Firefox and Gecko are trademarks or projects of the Mozilla Foundation and Mozilla Corporation. Lin Browser is an independent project and is not affiliated with or endorsed by Mozilla.
