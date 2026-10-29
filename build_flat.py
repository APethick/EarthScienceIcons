"""Refresh flat SVG colours and previews without modifying detailed font assets."""
import json
from pathlib import Path

from build_font import polygons_to_svg_path
from icon_catalog import ALL_ICONS
from icons_geophysics_expanded import EXPANDED_IDS
from icons_mt import MT_IDS
from icons_alteration import GEOCHEM_IDS
from icons_field_manual import FGM_IDS
from icon_artwork import artwork, svg_document
from icon_materials import ICON_MATERIALS
from icon_specimen import build_catalog, render_flat_sheet, render_style_preview, render_material_preview, render_em_preview, render_petrophysics_preview, render_logging_preview


def build_flat():
    dist = Path(__file__).resolve().parent / 'dist'
    from build_font import ASCII_KEYS
    from icon_identity import validate_sources
    icons = ALL_ICONS
    validate_sources(icons, ASCII_KEYS)
    expected = {icon['id'] for icon in icons}
    from icons_spectroscopy import SPECTROSCOPY_IDS
    from icons_field_instruments import IDS as FIELD_IDS
    from icons_seismic_equipment import IDS as SEISMIC_IDS
    available = SEISMIC_IDS | FIELD_IDS | SPECTROSCOPY_IDS | set(ICON_MATERIALS) | EXPANDED_IDS | MT_IDS | GEOCHEM_IDS | FGM_IDS
    if expected != available:
        raise ValueError(f'Material assignments differ: {expected ^ available}')
    for icon in icons:
        (dist / 'svg' / f"{icon['id']}.svg").write_text(
            svg_document(icon, artwork(icon), polygons_to_svg_path), encoding='utf-8')
    manifest = dist / 'geoscience-icons.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    data['svgStyle'] = 'detailed-flat-natural-materials'
    manifest.write_text(json.dumps(data, indent=2), encoding='utf-8')
    build_catalog(dist / 'index.html', data['icons'])
    render_flat_sheet(dist / 'flat_specimen_sheet.png', icons)
    render_style_preview(dist / 'style_preview.png', icons, dist / 'GeoScienceIcons.ttf')
    render_material_preview(dist / 'natural_colour_preview.png', icons)
    render_em_preview(dist / 'em_equipment_preview.png', icons, dist / 'GeoScienceIcons.ttf')
    render_petrophysics_preview(dist / 'petrophysics_preview.png', icons, dist / 'GeoScienceIcons.ttf')
    render_logging_preview(dist / 'petrophysics_logging_preview.png', icons, dist / 'GeoScienceIcons.ttf')
    from icon_specimen import render_category_sheets, render_individual_pngs
    render_category_sheets(dist, icons, dist / 'GeoScienceIcons.ttf')
    render_individual_pngs(dist, icons, dist / 'GeoScienceIcons.ttf')
    print(f'Updated {len(icons)} flat SVGs with object/material colours. Detailed fonts and monochrome SVGs were not rebuilt.')


if __name__ == '__main__':
    build_flat()
