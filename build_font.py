"""
Compiler for the GeoScience Icons TrueType Font (.ttf), WOFF, SVG set, CSS, JSON catalog,
HTML interactive specimen, and FreeType-rendered PNG verification sheet.
"""

import json
import os
import argparse
from html import escape
from pathlib import Path
from typing import Dict, Any, List
from shapely.geometry import Polygon
from shapely.geometry import box
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from PIL import Image, ImageDraw, ImageFont

from geom_utils import clean_for_ttf, rect_outline, line, union_all
from icons_geophysical import GEOPHYSICAL_ICONS
from icons_geotechnical import GEOTECHNICAL_ICONS
from icons_geological import GEOLOGICAL_ICONS
from icons_geochemical import GEOCHEMICAL_ICONS
from icons_opus_geology import OPUS_GEOLOGY_ICONS
from icons_geochemical_expanded import EXPANDED_GEOCHEMISTRY_ICONS
from icons_mineralis_inversion import MINERALIS_INVERSION_ICONS
from icon_artwork import artwork, svg_document, build_recipes
from font_artwork import detailed_font_geometry
from icon_specimen import build_catalog, render_flat_sheet, render_style_preview, render_material_preview

UPM = 1000
ASCENT = 880
DESCENT = -120
Y_OFFSET = -120  # Maps canvas [0, 1000] -> font Y [-120, 880]

# 193+ printable fallback characters across ASCII, Latin-1 Supplement, and Latin Extended-A
printable_chars = [chr(c) for c in range(0x0021, 0x007F)] + [
    chr(c) for c in range(0x00A1, 0x0100)
] + [chr(c) for c in range(0x0100, 0x0180)]
ASCII_KEYS = printable_chars[:193]


def polygons_to_ttglyph(polys: List[Polygon]):
    """Convert oriented Shapely polygons into a TrueType Glyph via TTGlyphPen."""
    pen = TTGlyphPen(None)
    for poly in polys:
        rings = [poly.exterior] + list(poly.interiors)
        for ring in rings:
            coords = list(ring.coords)[:-1]
            if len(coords) < 3:
                continue
            pts = [(int(round(x)), int(round(y + Y_OFFSET))) for x, y in coords]
            # Remove consecutive duplicate integer points
            dedup = [pts[0]]
            for pt in pts[1:]:
                if pt != dedup[-1]:
                    dedup.append(pt)
            if len(dedup) > 1 and dedup[0] == dedup[-1]:
                dedup.pop()
            if len(dedup) < 3:
                continue
            pen.moveTo(dedup[0])
            for pt in dedup[1:]:
                pen.lineTo(pt)
            pen.closePath()
    return pen.glyph()


def polygons_to_svg_path(polys: List[Polygon]) -> str:
    """Convert oriented Shapely polygons into an SVG path d-string (canvas 1000x1000, Y flipped)."""
    cmds = []
    for poly in polys:
        rings = [poly.exterior] + list(poly.interiors)
        for ring in rings:
            coords = list(ring.coords)[:-1]
            if len(coords) < 3:
                continue
            x0, y0 = coords[0]
            cmds.append(f"M{x0:.1f} {1000.0 - y0:.1f}")
            for x, y in coords[1:]:
                cmds.append(f"L{x:.1f} {1000.0 - y:.1f}")
            cmds.append("Z")
    return " ".join(cmds)


def make_notdef_glyph():
    """Standard .notdef glyph (box with X)."""
    g = union_all(
        [
            rect_outline(150, 100, 850, 900, 40),
            line(170, 120, 830, 880, 32),
            line(170, 880, 830, 120, 32),
        ]
    )
    return polygons_to_ttglyph(clean_for_ttf(g))


def build_all(install_opus: bool = False):
    root_dir = Path(__file__).resolve().parent
    dist_dir = root_dir / "dist"
    svg_dir = dist_dir / "svg"
    mono_dir = dist_dir / "svg-mono"
    dist_dir.mkdir(parents=True, exist_ok=True)
    svg_dir.mkdir(parents=True, exist_ok=True)
    mono_dir.mkdir(parents=True, exist_ok=True)

    all_icons: List[Dict[str, Any]] = (
        GEOPHYSICAL_ICONS
        + GEOTECHNICAL_ICONS
        + GEOLOGICAL_ICONS
        + GEOCHEMICAL_ICONS
        + OPUS_GEOLOGY_ICONS
        + EXPANDED_GEOCHEMISTRY_ICONS
        + MINERALIS_INVERSION_ICONS
    )
    assert len(all_icons) == 193, f"Expected 193 icons, got {len(all_icons)}"
    expected_ids = {icon["id"] for icon in all_icons}
    if set(build_recipes()) != expected_ids:
        raise ValueError(f"Artwork IDs differ: missing={expected_ids - set(build_recipes())}, extra={set(build_recipes()) - expected_ids}")

    glyph_order = [".notdef", "space"]
    cmap: Dict[int, str] = {0x0020: "space", 0x00A0: "space"}
    glyf_table = {
        ".notdef": make_notdef_glyph(),
        "space": TTGlyphPen(None).glyph(),
    }
    hmtx_table = {
        ".notdef": (UPM, 100),
        "space": (500, 0),
    }

    catalog_entries = []

    print(f"Building {len(all_icons)} geoscience icons...")
    for idx, icon in enumerate(all_icons):
        glyph_name = icon["id"]
        codepoint = icon["codepoint"]
        ascii_char = ASCII_KEYS[idx]

        layers = artwork(icon)
        raw_geom = detailed_font_geometry(icon)
        if raw_geom.is_empty or not raw_geom.is_valid or not box(0, 0, UPM, UPM).covers(raw_geom):
            raise ValueError(f"Invalid or clipped glyph: {glyph_name} {raw_geom.bounds}")
        polys = clean_for_ttf(raw_geom, simplify_tol=0.6)
        tt_glyph = polygons_to_ttglyph(polys)
        svg_path_d = polygons_to_svg_path(polys)

        # Compute left side bearing from actual polygon bounds
        min_x = min((p.bounds[0] for p in polys), default=60.0)
        lsb = int(round(min_x))

        glyph_order.append(glyph_name)
        glyf_table[glyph_name] = tt_glyph
        hmtx_table[glyph_name] = (UPM, lsb)

        # Map both PUA codepoint and ASCII key
        cmap[codepoint] = glyph_name
        cmap[ord(ascii_char)] = glyph_name

        # Write standalone SVG file
        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="100%" height="100%">
  <title>{escape(icon["name"])} ({icon["domain"]} - {icon["category"]})</title>
  <desc>{escape(icon["description"])}</desc>
  <path fill="currentColor" d="{svg_path_d}"/>
</svg>
"""
        (mono_dir / f"{glyph_name}.svg").write_text(svg_content, encoding="utf-8")
        (svg_dir / f"{glyph_name}.svg").write_text(svg_document(icon, layers, polygons_to_svg_path), encoding="utf-8")

        catalog_entries.append(
            {
                "index": idx + 1,
                "id": glyph_name,
                "css_class": f"gi-{glyph_name.replace('_', '-')}",
                "name": icon["name"],
                "domain": icon["domain"],
                "category": icon["category"],
                "codepoint_int": codepoint,
                "codepoint_hex": f"U+{codepoint:04X}",
                "css_content": f"\\{codepoint:04x}",
                "html_entity": f"&#x{codepoint:04X};",
                "ascii_key": ascii_char,
                "description": icon["description"],
                "keywords": icon["keywords"],
                "svg_file": f"svg/{glyph_name}.svg",
                "svg_mono_file": f"svg-mono/{glyph_name}.svg",
            }
        )

    # Build TrueType Font (.ttf)
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyf_table)
    fb.setupHorizontalMetrics(hmtx_table)
    fb.setupHorizontalHeader(ascent=ASCENT, descent=DESCENT, lineGap=0)
    fb.setupNameTable(
        {
            "familyName": "GeoScience Icons",
            "styleName": "Regular",
            "uniqueFontIdentifier": "GeoScienceIcons-Regular-2.1",
            "fullName": "GeoScience Icons Regular",
            "psName": "GeoScienceIcons-Regular",
            "version": "Version 2.100",
            "copyright": "Copyright (c) 2026 GeoScience Icon Set. Open License.",
            "description": "Comprehensive TrueType icon font covering Geophysical, Geotechnical, Geological, and Geochemical methods, earth model types, and processes.",
        }
    )
    fb.setupOS2(
        sTypoAscender=ASCENT,
        sTypoDescender=DESCENT,
        sTypoLineGap=0,
        usWinAscent=ASCENT,
        usWinDescent=abs(DESCENT),
        sxHeight=520,
        sCapHeight=760,
        fsType=0,  # Installable embedding allowed
    )
    fb.setupPost(isFixedPitch=1)
    fb.font["head"].fontRevision = 2.1

    ttf_dist_path = dist_dir / "GeoScienceIcons.ttf"
    ttf_root_path = root_dir / "GeoScienceIcons.ttf"
    fb.save(str(ttf_dist_path))
    fb.save(str(ttf_root_path))

    # Also save WOFF webfont
    fb.font.flavor = "woff"
    woff_dist_path = dist_dir / "GeoScienceIcons.woff"
    fb.save(str(woff_dist_path))
    print(f"Saved TTF to: {ttf_root_path} ({ttf_root_path.stat().st_size:,} bytes)")
    print(f"Saved WOFF to: {woff_dist_path} ({woff_dist_path.stat().st_size:,} bytes)")

    # Write JSON metadata catalog
    json_path = dist_dir / "geoscience-icons.json"
    json_data = {
        "fontFamily": "GeoScience Icons",
        "postScriptName": "GeoScienceIcons-Regular",
        "version": "2.1.0",
        "svgStyle": "detailed-flat-natural-materials",
        "fontStyle": "detailed-technical-line",
        "unitsPerEm": UPM,
        "ascent": ASCENT,
        "descent": DESCENT,
        "totalIcons": len(catalog_entries),
        "domains": ["Geophysical", "Geotechnical", "Geological", "Geochemical"],
        "categories": ["Methods", "Earth Model Types", "Processes"],
        "icons": catalog_entries,
    }
    json_path.write_text(json.dumps(json_data, indent=2), encoding="utf-8")

    # Write CSS stylesheet
    css_lines = [
        "/**",
        " * GeoScience Icons v2.1.0",
        " * Domains: Geophysical, Geotechnical, Geological, Geochemical",
        " * Categories: Methods, Earth Model Types, Processes",
        " */",
        "@font-face {",
        "  font-family: 'GeoScience Icons';",
        "  src: url('GeoScienceIcons.woff') format('woff'),",
        "       url('GeoScienceIcons.ttf') format('truetype');",
        "  font-weight: normal;",
        "  font-style: normal;",
        "  font-display: block;",
        "}",
        "",
        ".gi {",
        "  font-family: 'GeoScience Icons' !important;",
        "  speak: never;",
        "  font-style: normal;",
        "  font-weight: normal;",
        "  font-variant: normal;",
        "  text-transform: none;",
        "  line-height: 1;",
        "  display: inline-block;",
        "  -webkit-font-smoothing: antialiased;",
        "  -moz-osx-font-smoothing: grayscale;",
        "}",
        "",
    ]
    for item in catalog_entries:
        css_lines.append(
            f".{item['css_class']}::before {{ content: \"{item['css_content']}\"; }} /* {item['name']} ({item['codepoint_hex']}) */"
        )
    (dist_dir / "geoscience-icons.css").write_text("\n".join(css_lines) + "\n", encoding="utf-8")

    # Build HTML interactive specimen page
    build_catalog(dist_dir / "index.html", catalog_entries)

    # Render PNG verification sheet directly from the compiled TTF font using Pillow/FreeType
    render_specimen_png(ttf_dist_path, dist_dir / "specimen_sheet.png", catalog_entries)
    render_flat_sheet(dist_dir / "flat_specimen_sheet.png", all_icons)
    render_style_preview(dist_dir / "style_preview.png", all_icons, ttf_dist_path)
    render_material_preview(dist_dir / "natural_colour_preview.png", all_icons)

    # Generate Java GlyphFont class for Opus
    java_code = build_java_glyph_class(catalog_entries)
    (dist_dir / "GeoScienceIcons.java").write_text(java_code, encoding="utf-8")
    print(f"Generated Java GlyphFont class: {dist_dir / 'GeoScienceIcons.java'}")

    # Copy font & java class into C:\projects\opus\opus.base if directory exists
    opus_fonts_dir = Path(r"C:\projects\opus\opus.base\resources\fonts")
    opus_icons_dir = Path(r"C:\projects\opus\opus.base\src\opus\base\icons")
    if install_opus and opus_fonts_dir.exists():
        import shutil
        shutil.copy2(str(ttf_dist_path), str(opus_fonts_dir / "GeoScienceIcons.ttf"))
        print(f"Copied TTF to Opus resources: {opus_fonts_dir / 'GeoScienceIcons.ttf'}")
    if install_opus and opus_icons_dir.exists():
        import shutil
        shutil.copy2(str(ttf_dist_path), str(opus_icons_dir / "GeoScienceIcons.ttf"))
        (opus_icons_dir / "GeoScienceIcons.java").write_text(java_code, encoding="utf-8")
        print(f"Copied TTF & Java class to Opus icons: {opus_icons_dir / 'GeoScienceIcons.java'}")


def build_java_glyph_class(catalog: List[Dict[str, Any]]) -> str:
    glyph_enums = []
    lookup_cases = []
    for item in catalog:
        enum_const = item["id"].upper()
        ch_hex = f"\\u{item['codepoint_int']:04x}"
        glyph_enums.append(f"\t\t{enum_const}('{ch_hex}'), // {item['name']} ({item['domain']} - {item['category']})")
        lookup_cases.append(f"\t\t\tcase \"{item['id']}\" -> Glyph.{enum_const};")

    code = f"""package opus.base.icons;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Arrays;

import org.controlsfx.glyphfont.GlyphFont;
import org.controlsfx.glyphfont.GlyphFontRegistry;
import org.controlsfx.glyphfont.INamedCharacter;

import opus.base.properties.OpusProperty;
import opus.base.resources.OpusResources;

/**
 * GeoScienceIcons TrueType glyph font (193 icons) covering Geophysical, Geotechnical,
 * Geological, and Geochemical methods, earth model types, and processes.
 * Includes dedicated suites for Inversion, Thermodynamics, Petrophysics, and Geochemistry,
 * aligned with opus.geo.geochemistry, opus.geo.petrophysics, and opus.geo.geotechnical.
 */
public class GeoScienceIcons extends GlyphFont {{

    private static final Logger logger = LogManager.getLogger(GeoScienceIcons.class.getName());
    public static final String FONT_NAME = "GeoScience Icons";

    public enum Glyph implements INamedCharacter {{
{chr(10).join(glyph_enums)}
        ;

        private final char ch;

        Glyph(char ch) {{
            this.ch = ch;
        }}

        @Override
        public char getChar() {{
            return ch;
        }}
    }}

    public GeoScienceIcons() {{
        super(FONT_NAME, 14, getBufferedStream(), true);
        GlyphFontRegistry.register(FONT_NAME, getBufferedStream(), 14);
        registerAll(Arrays.asList(Glyph.values()));
    }}

    @Override
    public org.controlsfx.glyphfont.Glyph create(String glyphName) {{
        GlyphFont font = GlyphFontRegistry.font(FONT_NAME);
        char c = getCharacter(glyphName);
        return font.create(c);
    }}

    private static InputStream getBufferedStream() {{
        try {{
            return new BufferedInputStream(new FileInputStream(new File(OpusResources.getResourcePath("fonts/GeoScienceIcons.ttf"))));
        }} catch (Exception e) {{
            logger.error("Failed to load GeoScienceIcons.ttf", e);
        }}
        return null;
    }}

    public static Glyph forIconId(String iconId) {{
        if (iconId == null) return null;
        return switch (iconId.toLowerCase().trim()) {{
{chr(10).join(lookup_cases)}
            default -> null;
        }};
    }}

    public static org.controlsfx.glyphfont.Glyph createGlyph(Glyph glyph, double size) {{
        GlyphFont font = GlyphFontRegistry.font(FONT_NAME);
        return font.create(glyph).size(size);
    }}
}}
"""
    return code


def render_specimen_png(ttf_path: Path, png_path: Path, catalog: List[Dict[str, Any]]):
    """Render all glyphs directly from the compiled TTF file into a grid contact sheet."""
    import math
    cols = 20
    rows = int(math.ceil(len(catalog) / cols))
    cell_w, cell_h = 160, 185
    header_h = 90
    img_w = cols * cell_w + 40
    img_h = rows * cell_h + header_h + 30

    img = Image.new("RGB", (img_w, img_h), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    icon_font = ImageFont.truetype(str(ttf_path), 76)
    try:
        label_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
        title_font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
        sub_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
    except Exception:
        label_font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    draw.text((28, 18), f"GeoScienceIcons.ttf — TrueType Font Contact Sheet ({len(catalog)} Icons)", fill=(248, 250, 252), font=title_font)
    draw.text(
        (28, 52),
        "Geophysical (39) • Geotechnical (22) • Geological (59) • Geochemical (73) — Methods (59), Earth Models (85), Processes (49)",
        fill=(148, 163, 184),
        font=sub_font,
    )

    domain_palette = {
        "Geophysical": (56, 189, 248),
        "Geotechnical": (251, 191, 36),
        "Geological": (52, 211, 153),
        "Geochemical": (192, 132, 252),
    }

    for idx, item in enumerate(catalog):
        c = idx % cols
        r = idx // cols
        x0 = 20 + c * cell_w
        y0 = header_h + r * cell_h

        # Card box
        draw.rounded_rectangle(
            [x0 + 4, y0 + 4, x0 + cell_w - 4, y0 + cell_h - 4],
            radius=8,
            fill=(30, 41, 59),
            outline=(51, 65, 85),
            width=1,
        )

        # Domain & Category header
        dom_color = domain_palette.get(item["domain"], (200, 200, 200))
        cat_abbr = {"Methods": "Method", "Earth Model Types": "Model", "Processes": "Process"}[item["category"]]
        draw.text((x0 + 8, y0 + 8), f"{item['domain'][:6]} • {cat_abbr}", fill=dom_color, font=label_font)
        draw.text((x0 + cell_w - 54, y0 + 8), item["codepoint_hex"], fill=(148, 163, 184), font=label_font)

        # Render actual TTF glyph
        ch = chr(item["codepoint_int"])
        draw.text((x0 + 42, y0 + 34), ch, fill=(248, 250, 252), font=icon_font)

        # Short label at bottom
        short_name = item["name"]
        if len(short_name) > 19:
            short_name = short_name[:17] + ".."
        draw.text((x0 + 8, y0 + cell_h - 22), short_name, fill=(226, 232, 240), font=label_font)

    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()
    try:
        if png_path.exists():
            os.remove(png_path)
        png_path.write_bytes(png_bytes)
        print(f"Saved FreeType PNG specimen sheet to: {png_path}")
    except OSError:
        alt_path = png_path.with_name("specimen_sheet_v2.png")
        alt_path.write_bytes(png_bytes)
        print(f"Saved FreeType PNG specimen sheet to: {alt_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the flat SVG collection and matching line icon font.")
    parser.add_argument("--install-opus", action="store_true", help="Also copy the font and Java binding into the existing Opus checkout.")
    build_all(install_opus=parser.parse_args().install_opus)
