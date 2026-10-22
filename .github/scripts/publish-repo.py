"""
Builds the extension repo (apk/, icon/, index.json, index.min.json) from the build artifacts.

Replaces move-apks.sh + create-repo.sh (and the extensions inspector, aapt and jq they relied on).
Run it with the checked-out `repo` branch as the working directory:

    cd repo && python ../main/.github/scripts/publish-repo.py

Inputs:  ~/apk-artifacts/**/build/outputs/apk/release/*.apk   one APK per extension
         ~/apk-artifacts/**/build/source-info.json            written by Gradle next to every APK
Outputs: ./apk/<apk>, ./icon/<package>.png, ./index.json, ./index.min.json
Anything else in the repo branch (README.md, repo.json, .git, ...) is left untouched.
"""

import json
import shutil
import sys
from pathlib import Path

ARTIFACTS_DIR = Path.home() / "apk-artifacts"
REPO_DIR = Path.cwd()
SOURCE_DIR = Path(__file__).resolve().parents[2]  # checkout of `main`, used to find icons

# Same guard as the old move-apks.sh: refuse to replace the repo with (almost) nothing.
MIN_APKS = 2


def find_extensions() -> list[tuple[dict, Path]]:
    found = []
    for info_file in ARTIFACTS_DIR.glob("**/source-info.json"):
        info = json.loads(info_file.read_text(encoding="utf-8"))
        apks = list((info_file.parent / "outputs/apk/release").glob("*.apk"))
        if len(apks) != 1:
            sys.exit(f"{info['pkg']}: expected exactly one release APK next to {info_file}, found {len(apks)}")
        found.append((info, apks[0]))
    return sorted(found, key=lambda item: item[0]["pkg"])


def index_entry(info: dict) -> dict:
    lang = info["folderLang"]
    sources = info["sources"]

    # Fixes the language code without needing to rename the folders (same rule as the old create-repo.sh):
    # a single source with a more specific language (e.g. folder "pt", source "pt-BR") wins.
    if len(sources) == 1:
        source_lang = sources[0]["lang"]
        if source_lang != lang and "all" not in (source_lang, lang) and "other" not in (source_lang, lang):
            lang = source_lang

    return {
        "name": info["name"],
        "pkg": info["pkg"],
        "apk": info["apk"],
        "lang": lang,
        "code": info["code"],
        "version": info["version"],
        # legacy index only knows 0/1: SAFE -> 0, MIXED and NSFW -> 1
        "nsfw": 0 if info["contentWarning"] == 0 else 1,
        "sources": sources,
    }


def main() -> None:
    extensions = find_extensions()
    if len(extensions) < MIN_APKS:
        sys.exit(f"Insufficient amount of APKs found ({len(extensions)}). Please check the project configuration.")
    print(f"Publishing {len(extensions)} extensions")

    for folder in ("apk", "icon"):
        shutil.rmtree(REPO_DIR / folder, ignore_errors=True)
        (REPO_DIR / folder).mkdir()

    index = []
    for info, apk in extensions:
        shutil.copy2(apk, REPO_DIR / "apk" / info["apk"])
        shutil.copy2(SOURCE_DIR / info["icon"], REPO_DIR / "icon" / f"{info['pkg']}.png")
        index.append(index_entry(info))

    (REPO_DIR / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (REPO_DIR / "index.min.json").write_text(
        json.dumps(index, separators=(",", ":"), ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
