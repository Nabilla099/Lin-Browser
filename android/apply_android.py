#!/usr/bin/env python3
"""Menerapkan kustomisasi Lin Browser ke source Gecko/Fenix (Firefox for Android).

Pemakaian: python3 android/apply_android.py <src> [--dry-run] [--strict]

Setiap aturan bersifat 'fail-soft': kalau pola tidak ditemukan, aturan itu
dilaporkan [WARN] dan build lanjut. Dengan --strict, ada WARN => exit 1.
"""
import glob
import os
import re
import sys

SRC = os.path.abspath(sys.argv[1])
DRY = "--dry-run" in sys.argv
STRICT = "--strict" in sys.argv
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FENIX = os.path.join(SRC, "mobile", "android", "fenix")
APP = os.path.join(FENIX, "app")
NAME = "Lin Browser"
APP_ID = "app.lin.browser"
warns = 0


def ok(msg):
    print("[ok]  ", ("(dry) " if DRY else "") + msg)


def warn(msg):
    global warns
    warns += 1
    print("[WARN]", msg)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, text):
    if not DRY:
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)


def rel(p):
    return os.path.relpath(p, SRC)


# 1) Preferensi bawaan ----------------------------------------------------
def rule_prefs():
    marker = "// ---- Lin Browser prefs ----"
    for c in ("mobile/android/app/geckoview-prefs.js", "mobile/android/app/mobile.js"):
        p = os.path.join(SRC, c)
        if not os.path.exists(p):
            continue
        text = read(p)
        if marker in text:
            ok(f"prefs sudah ada di {c}")
            return
        add = read(os.path.join(REPO, "prefs", "android.js"))
        write(p, text.rstrip("\n") + f"\n\n{marker}\n{add}")
        ok(f"prefs ditambahkan ke {c}")
        return
    warn("file prefs (geckoview-prefs.js / mobile.js) tidak ditemukan")


# 2) Add-on: aktifkan koleksi kustom + "install dari file" di semua channel ------
def find_function_body(text, name):
    """Kembalikan (awal, akhir) isi fungsi Kotlin `name` (di dalam kurung kurawalnya)."""
    m = re.search(r"fun\s+" + re.escape(name) + r"\s*\(", text)
    if not m:
        return None
    i = text.find("{", m.end())
    if i < 0:
        return None
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return i + 1, j
    return None


CHANNEL = re.compile(r"Config\.channel\.is\w+")
SECRET = re.compile(r"settings\.showSecretDebugMenuThisSession|showSecretDebugMenuThisSession")


def rule_addon_features():
    # a) FeatureFlags.customExtensionCollectionFeature -> true
    ff = os.path.join(APP, "src", "main", "java", "org", "mozilla", "fenix", "FeatureFlags.kt")
    if os.path.exists(ff):
        t = read(ff)
        new, c = re.subn(r"(val\s+customExtensionCollectionFeature\s*=\s*)[^\n]+", r"\1true", t)
        if c:
            write(ff, new)
            ok("FeatureFlags.customExtensionCollectionFeature = true")
        else:
            warn("customExtensionCollectionFeature tidak ditemukan di FeatureFlags.kt")
    else:
        warn("FeatureFlags.kt tidak ada")

    # b) pengaturan 'koleksi add-on kustom' & 'install add-on dari file' selalu terlihat
    sf = os.path.join(APP, "src", "main", "java", "org", "mozilla", "fenix", "settings", "SettingsFragment.kt")
    if not os.path.exists(sf):
        warn("SettingsFragment.kt tidak ada")
        return
    text = read(sf)
    for fn in ("setupInstallAddonFromFilePreference", "setupAmoCollectionOverridePreference"):
        span = find_function_body(text, fn)
        if not span:
            warn(f"fungsi {fn} tidak ditemukan")
            continue
        body = text[span[0]:span[1]]
        new_body = SECRET.sub("true", CHANNEL.sub("true", body))
        text = text[:span[0]] + new_body + text[span[1]:]
        ok(f"{fn}: {'diubah' if new_body != body else 'TIDAK ada pembatas yang cocok'}")
        if new_body == body:
            warn(f"{fn} tidak punya pembatas channel/secret-menu yang dikenali; isi fungsi:")
        for ln in new_body.strip("\n").split("\n")[:30]:
            print("        |", ln)
    write(sf, text)


# 3) Nama aplikasi ------------------------------------------------------------
def rule_app_name():
    n = 0
    for g in glob.glob(os.path.join(APP, "build.gradle*")):
        text = read(g)
        new, c = re.subn(r"""(resValue\s*\(?\s*["']string["']\s*,\s*["']app_name["']\s*,\s*["'])([^"']*)(["'])""",
                         lambda m: m.group(1) + NAME + m.group(3), text)
        if c:
            write(g, new)
            n += c
    for x in glob.glob(os.path.join(APP, "src", "**", "res", "values*", "*.xml"), recursive=True):
        text = read(x)
        new, c = re.subn(r"""(<string\s+name="app_name"[^>]*>)([^<]*)(</string>)""",
                         lambda m: m.group(1) + NAME + m.group(3), text)
        if c:
            write(x, new)
            n += c
    ok(f"app_name -> {NAME} ({n} tempat)") if n else warn("app_name tidak ditemukan")


# 4) Application ID ------------------------------------------------------------
def rule_app_id():
    n = 0
    for g in glob.glob(os.path.join(APP, "build.gradle*")):
        lines = read(g).split("\n")
        for i, line in enumerate(lines):
            if "applicationId" in line and "Suffix" not in line and re.search(r'"org\.mozilla[\w.]*"', line):
                lines[i] = re.sub(r'"org\.mozilla[\w.]*"', f'"{APP_ID}"', line)
                print(f"        {rel(g)}:{i + 1}: {line.strip()}  ->  {lines[i].strip()}")
                n += 1
        if n:
            write(g, "\n".join(lines))
    # release memakai akhiran ".firefox" -> kosongkan supaya ID akhir = app.lin.browser
    for g in glob.glob(os.path.join(APP, "build.gradle*")):
        text = read(g)
        new, c = re.subn(r'(applicationIdSuffix\s*=?\s*)"\.firefox"', r'\1""', text)
        if c:
            write(g, new)
            print(f"        applicationIdSuffix \".firefox\" -> \"\" ({c}x)")
    ok(f"applicationId -> {APP_ID}") if n else warn("applicationId org.mozilla* tidak ditemukan")


# 5) Ikon peluncur -------------------------------------------------------------
DENSITY = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
VECTORS = ("ic_launcher_foreground.xml", "ic_launcher_background.xml", "ic_launcher_monochrome.xml")
BITMAP = re.compile(r"^ic_launcher(_round)?\.(png|webp)$")
STORE = re.compile(r"^ic_launcher-(web|playstore)\.(png|webp)$")


def rule_icons():
    bitmaps = vectors = 0
    for r in glob.glob(os.path.join(APP, "src", "*", "res")) + glob.glob(os.path.join(APP, "src", "*")):
        for f in glob.glob(os.path.join(r, "**", "ic_launcher*"), recursive=True):
            base = os.path.basename(f)
            if base in VECTORS:
                if not DRY:
                    with open(os.path.join(REPO, "assets", "android", base), "rb") as s_, open(f, "wb") as d_:
                        d_.write(s_.read())
                vectors += 1
            elif BITMAP.match(base) or STORE.match(base):
                if not DRY:
                    from PIL import Image
                    dens = re.search(r"mipmap-(x*hdpi|mdpi)", f)
                    size = 512 if STORE.match(base) else DENSITY.get(dens.group(1) if dens else "", None)
                    src = Image.open(os.path.join(REPO, "assets", "icons", "lin-512.png")).convert("RGBA")
                    if size is None:
                        with Image.open(f) as cur:
                            size = cur.size[0]
                    src.resize((size, size), Image.LANCZOS).save(f)
                bitmaps += 1
    if bitmaps or vectors:
        ok(f"ikon diganti: {bitmaps} bitmap, {vectors} vektor adaptif/monokrom")
    else:
        warn("ic_launcher* tidak ditemukan")


if not os.path.isdir(FENIX):
    warn(f"{rel(FENIX)} tidak ada - ini bukan source Firefox for Android?")
for rule in (rule_prefs, rule_addon_features, rule_app_name, rule_app_id, rule_icons):
    print(f"\n--- {rule.__name__} ---")
    rule()
print(f"\nSelesai: {warns} peringatan")
sys.exit(1 if (STRICT and warns) else 0)
