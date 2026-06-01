#!/usr/bin/env python3
"""Apply the Brazilian Portuguese (pt-BR) translation onto a freshly cloned
Dantotsu source tree before building.

It does two things:

1. Writes the translated strings as ``values-pt-rBR/strings.xml`` so devices
   set to Brazilian Portuguese pick it up automatically (standard Android).
2. Optionally overrides the default ``values/strings.xml`` so the app is in
   Portuguese for everyone, regardless of device locale. Only string names
   that exist in the translation are replaced; any new upstream strings stay
   in English, so the build never breaks when upstream adds strings.

Usage:
    python3 scripts/apply_translation.py <dantotsu_source_dir> [--no-default]
"""
import argparse
import copy
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRANSLATION_FILE = REPO_ROOT / "translation" / "values-pt-rBR" / "strings.xml"


def load_translation():
    tree = ET.parse(TRANSLATION_FILE)
    root = tree.getroot()
    mapping = {}
    for tag in ("string", "string-array"):
        for elem in root.findall(tag):
            mapping[(tag, elem.get("name"))] = elem
    return mapping


def override_default(default_path: Path, translation):
    """Replace values of matching names in the default strings.xml in place."""
    ET.register_namespace("tools", "http://schemas.android.com/tools")
    tree = ET.parse(default_path)
    root = tree.getroot()
    replaced = 0
    for child in list(root):
        key = (child.tag, child.get("name"))
        if key in translation:
            src = translation[key]
            # Copy translated text and any child nodes (<u>, <b>, <item> ...)
            child.text = src.text
            for sub in list(child):
                child.remove(sub)
            for sub in list(src):
                child.append(copy.deepcopy(sub))
            replaced += 1
    tree.write(default_path, encoding="utf-8", xml_declaration=False)
    return replaced


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to the cloned Dantotsu source tree")
    parser.add_argument(
        "--no-default",
        action="store_true",
        help="Only add the pt-BR locale, do not override the default strings.",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    res_dir = source / "app" / "src" / "main" / "res"
    default_strings = res_dir / "values" / "strings.xml"
    if not default_strings.is_file():
        sys.exit(f"error: default strings not found at {default_strings}")

    if not TRANSLATION_FILE.is_file():
        sys.exit(f"error: translation file not found at {TRANSLATION_FILE}")

    # 1. Install the pt-BR locale resource.
    target_dir = res_dir / "values-pt-rBR"
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TRANSLATION_FILE, target_dir / "strings.xml")
    print(f"Installed pt-BR locale -> {target_dir / 'strings.xml'}")

    # 2. Optionally force pt-BR as the default language.
    if not args.no_default:
        translation = load_translation()
        replaced = override_default(default_strings, translation)
        print(f"Overrode {replaced} default strings with pt-BR -> {default_strings}")
    else:
        print("Skipped overriding default strings (--no-default).")


if __name__ == "__main__":
    main()
