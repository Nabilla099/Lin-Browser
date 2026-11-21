#!/usr/bin/env bash
# Unduh + verifikasi source Gecko dari rilis Firefox, ekstrak ke ./src
set -euo pipefail
V="${1:?usage: fetch-source.sh <version>}"
base="https://archive.mozilla.org/pub/firefox/releases/${V}"
name="firefox-${V}.source.tar.xz"
curl -fL --retry 3 -o "$name" "$base/source/$name"
curl -fL --retry 3 -o SHA256SUMS "$base/SHA256SUMS"
grep -F "source/$name" SHA256SUMS | awk -v n="$name" '{print $1"  "n}' | sha256sum -c -
mkdir -p src
tar -xf "$name" -C src --strip-components=1
rm -f "$name"
