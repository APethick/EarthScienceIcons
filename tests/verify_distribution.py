"""Check shipped assets and compatibility with the published 193-icon font.

Run after build_font.py and build_site.py: python tests/verify_distribution.py
The fixture records the original published glyph outlines, not regenerated ones.
"""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

from fontTools.ttLib import TTFont


def verify():
    root = Path(__file__).resolve().parents[1]
    dist = root / 'dist'
    assets = root / 'docs' / 'assets'
    catalog = json.loads((dist / 'geoscience-icons.json').read_text(encoding='utf-8'))
    icons = catalog['icons']
    assert len(icons) == catalog['totalIcons'] == 484
    assert len({icon['id'] for icon in icons}) == len(icons)
    assert len({icon['codepoint_int'] for icon in icons}) == len(icons)
    assert len({icon['ascii_key'] for icon in icons}) == len(icons)
    assert sum(icon['domain'] == 'Geophysical' for icon in icons) == 152
    assert sum(icon['domain'] == 'Geological' for icon in icons) == 207
    assert sum(icon['category'] == 'Petrophysical Quantities' for icon in icons) == 12
    original = json.loads((root / 'tests' / 'compatibility-193.json').read_text(encoding='utf-8'))
    redraws = json.loads((root / 'tests' / 'redraws-2.8.json').read_text(encoding='utf-8'))
    published = json.loads((root / 'tests' / 'compatibility-471-mappings.json').read_text(encoding='utf-8'))
    assert set(published).issubset({icon['id'] for icon in icons})
    font = TTFont(dist / 'GeoScienceIcons.ttf')
    webfont = TTFont(dist / 'GeoScienceIcons.woff')
    cmap = font.getBestCmap()
    assert cmap == webfont.getBestCmap()
    added_hashes = set()
    for icon in icons:
        identifier = icon['id']
        codepoint = icon['codepoint_int']
        if identifier in published:
            assert [codepoint, icon['ascii_key']] == published[identifier], identifier
        name = cmap[codepoint]
        assert cmap[ord(icon['ascii_key'])] == name, identifier
        glyph = font['glyf'][name]
        assert glyph.numberOfContours > 0, identifier
        assert 0 <= glyph.xMin < glyph.xMax <= 1000, identifier
        assert -120 <= glyph.yMin < glyph.yMax <= 880, identifier
        outline = hashlib.sha256(glyph.compile(font['glyf'])).hexdigest()
        if identifier in original:
            saved = original[identifier]
            assert codepoint == saved['codepoint'], identifier
            assert icon['ascii_key'] == saved['fallback'], identifier
            # MT was deliberately redrawn from the user reference in 2.5.
            if identifier in redraws:
                assert outline == redraws[identifier]["outline_sha256"], identifier
            elif identifier != "gp_magnetotellurics_mt":
                assert outline == saved['outline_sha256'], identifier
        else:
            assert outline not in added_hashes, identifier
            added_hashes.add(outline)
        for field in ('svg_file', 'svg_mono_file'):
            path = dist / icon[field]
            svg = ET.fromstring(path.read_text(encoding='utf-8'))
            assert svg.tag == '{http://www.w3.org/2000/svg}svg', identifier
            assert svg.findall('.//{http://www.w3.org/2000/svg}path'), identifier
            assert path.read_bytes() == (assets / icon[field]).read_bytes(), identifier
    assert len(original) == 193 and len(added_hashes) == 291
    for name in ('GeoScienceIcons.ttf', 'GeoScienceIcons.woff', 'geoscience-icons.css', 'geoscience-icons.json'):
        assert (dist / name).read_bytes() == (assets / name).read_bytes(), name
    assert (root / 'GeoScienceIcons.ttf').read_bytes() == (dist / 'GeoScienceIcons.ttf').read_bytes()
    with zipfile.ZipFile(assets / 'EarthScienceIcons.zip') as archive:
        assert archive.testzip() is None
        for path in dist.rglob('*'):
            if path.is_file():
                assert archive.read(path.relative_to(dist).as_posix()) == path.read_bytes(), str(path)
    print('PASS: 484 glyphs, 968 SVGs, webfont, Pages assets and ZIP; 189 original outlines preserved; MT and three 2.8 icons intentionally redrawn; all published mappings preserved.')


if __name__ == '__main__':
    verify()
