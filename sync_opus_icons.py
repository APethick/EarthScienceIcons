"""Merge generated icon mappings into Opus while preserving its local helpers."""
import argparse
import json
import re
import shutil
from pathlib import Path

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parent
DEFAULT_OPUS = Path(r"C:\projects\opus\opus.base")
ENUM_START = "    public enum Glyph implements INamedCharacter {"
ENUM_END = "        private final char ch;"
LOOKUP_START = "    public static Glyph forIconId(String iconId) {"
LOOKUP_END = "    /** Resolve an Opus quantity"


def section(text, start, end):
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"Cannot locate unique Java section: {start}")
    first = text.index(start)
    last = text.index(end, first)
    return text[first:last]


def mappings(text):
    entries = re.findall(r"\b([A-Z][A-Z0-9_]+)\('\\u([0-9a-fA-F]{4})'\)", text)
    lookup = re.findall(r'case "([^"]+)" -> Glyph\.([A-Z][A-Z0-9_]+);', text)
    if len(dict(entries)) != len(entries) or len(dict(lookup)) != len(lookup):
        raise ValueError("Duplicate glyph or lookup key in Java binding")
    return dict(entries), dict(lookup)


def sync(opus):
    target = opus / "src/opus/base/icons/GeoScienceIcons.java"
    fonts = [opus / "resources/fonts/GeoScienceIcons.ttf", target.with_suffix(".ttf")]
    source = ROOT / "dist/GeoScienceIcons.java"
    font_path = ROOT / "dist/GeoScienceIcons.ttf"
    for path in [target, *fonts, source, font_path, ROOT / "dist/geoscience-icons.json"]:
        if not path.is_file():
            raise FileNotFoundError(f"Required file does not exist: {path}")

    original = target.read_text(encoding="utf-8")
    generated = source.read_text(encoding="utf-8")
    old_entries, old_lookup = mappings(original)
    new_entries, new_lookup = mappings(generated)
    for key, value in old_entries.items():
        if new_entries.get(key) != value:
            raise ValueError(f"Generated binding changes or removes existing glyph {key}")
    for key, value in old_lookup.items():
        if new_lookup.get(key) != value:
            raise ValueError(f"Generated binding changes or removes existing lookup {key}")
    catalog = json.loads((ROOT / "dist/geoscience-icons.json").read_text(encoding="utf-8"))
    if len(new_entries) != catalog["totalIcons"]:
        raise ValueError("Generated Java glyph count does not match the manifest")
    with TTFont(font_path) as font:
        cmap = font.getBestCmap()
        for key, code in new_entries.items():
            if cmap.get(int(code, 16)) != key.lower():
                raise ValueError(f"Font and Java mapping differ: {key}")

    updated = original
    for start, end in ((ENUM_START, ENUM_END), (LOOKUP_START, LOOKUP_END)):
        updated = updated.replace(section(updated, start, end), section(generated, start, end), 1)
    updated = re.sub(r"glyph font \(\d+ icons\)", f"glyph font ({len(new_entries)} icons)", updated, count=1)
    if updated != original:
        target.write_bytes(updated.encode("utf-8"))
    for destination in fonts:
        shutil.copy2(font_path, destination)
    print(f"Updated {target} and both Opus fonts with {len(new_entries)} glyphs.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opus-root", type=Path, default=DEFAULT_OPUS)
    args = parser.parse_args()
    sync(args.opus_root)
