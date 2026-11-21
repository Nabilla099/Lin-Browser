#!/usr/bin/env bash
# Mencetak fakta penting dari source Android agar patch bisa dicocokkan dengan tepat.
cd "${1:-src}"
sec() { printf '\n===== %s =====\n' "$*"; }
F=mobile/android/fenix

sec "mobile/android";            ls mobile/android | head -60
sec "fenix";                     ls "$F" "$F/app/src" 2>&1 | head -40
sec "minSdk";                    grep -rnEs "minSdk(Version)?\s*[=:]?\s*[0-9]+" mobile/android --include=*.gradle --include=*.kts --include=*.kt --include=*.toml | grep -v "/test" | head -20
sec "configure min sdk";         grep -rns "min.sdk" build/moz.configure mobile/android/moz.configure 2>/dev/null | head
sec "applicationId";             grep -rn "applicationId" "$F"/app/build.gradle* 2>/dev/null | head -20
sec "app_name";                  grep -rn "app_name" "$F"/app/build.gradle* "$F"/app/src/main/res/values/strings.xml 2>/dev/null | head -10
sec "launcher icons";            find "$F/app/src" -name 'ic_launcher*' 2>/dev/null | sort | head -60
sec "channel gates (addons)";    grep -rnE "Config\.channel\.is(NightlyOrDebug|Debug|Nightly)" "$F/app/src/main/java" 2>/dev/null | grep -iE "addon|extension|\bamo\b" | head -40
sec "addon source files";        find "$F/app/src/main/java" -iname '*addon*' 2>/dev/null | head -40
sec "install from file";         grep -rniE "installAddonFromFile|install.?from.?file|InstallFromFile" "$F/app/src/main" 2>/dev/null | head -20
sec "custom collection";         grep -rniE "override_amo_collection|customAddonsCollection|amoCollection" "$F/app/src/main" 2>/dev/null | head -20
sec "prefs files";               find mobile/android -maxdepth 3 \( -name 'geckoview-prefs.js' -o -name 'mobile.js' \) 2>/dev/null
sec "mozboot android versions";  grep -nE "_VERSION|def ensure_android" python/mozboot/mozboot/android.py 2>/dev/null | head -30
sec "gradle files";              ls gradle* mobile/android/gradle* 2>&1 | head -20

sec "FeatureFlags.kt";           sed -n 1,40p "$F/app/src/main/java/org/mozilla/fenix/FeatureFlags.kt" 2>/dev/null
sec "SettingsFragment add-on";   S="$F/app/src/main/java/org/mozilla/fenix/settings/SettingsFragment.kt"; sed -n 625,655p "$S" 2>/dev/null; echo ...; sed -n 762,790p "$S" 2>/dev/null
sec "build.gradle flavors";      grep -nE "flavorDimensions|productFlavors|buildTypes|^\s+(debug|nightly|beta|release|benchmark|fenix)\s*\{" "$F"/app/build.gradle 2>/dev/null | head -30
sec "gradle projects";           grep -nE "include|project\(" mobile/android/settings.gradle "$F"/settings.gradle 2>/dev/null | head -20
sec "ensure_android signature";  sed -n 339,352p python/mozboot/mozboot/android.py 2>/dev/null
