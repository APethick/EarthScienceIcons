"""Flat material-colour rendering of the detailed technical compositions.

Record primitive geometry from the same callable builders used by the font.
Restore module globals immediately after each call. Underpaint selected closed
surfaces, then colour only visible geometry so boolean cutouts and all original
scientific linework survive. No gradients, shadows or raster assets are used.
"""

from dataclasses import dataclass
from functools import lru_cache

from shapely import affinity
from shapely.geometry import Polygon

from font_artwork import OVERRIDES, detailed_font_geometry
from geom_utils import union_all
from icon_materials import ICON_MATERIALS, MATERIALS

INK = MATERIALS['ink']
BLUE = '#3478F6'
RED = '#E35D65'
YELLOW = '#F2C94C'


@dataclass
class FlatLayer:
    surface: object
    color: str


PRIMITIVES = {
    'circle', 'ring', 'disk_ring', 'rect', 'rect_outline', 'rounded_rect',
    'rounded_rect_outline', 'poly', 'regular_poly', 'stroke', 'line',
    'dashed_line', 'arc', 'sector', 'ellipse', 'ellipse_outline',
    'arrow_head', 'arrow', 'curved_arrow', 'sine_wave',
}
FILLED = {'circle', 'rect', 'rounded_rect', 'poly', 'regular_poly', 'sector'}
PLOT_IDS = {
    'gp_velocity_model', 'gp_density_model', 'gp_susceptibility_model',
    'gp_resistivity_section', 'gp_seismic_cube_3d', 'gl_block_model_3d',
    'gl_wireframe_mesh', 'gc_alteration_zonation', 'gc_geochem_anomaly_contours',
    'gl_composition_category', 'gc_major_element_oxides',
}
FIELD_IDS = {
    'gp_magnetic_survey', 'gp_electromagnetic_em', 'gp_ert_ip',
    'gp_wave_propagation', 'gp_magnetotellurics_mt', 'gp_ground_penetrating_radar',
    'gp_acoustics_sonar', 'gc_isotope_ratio_analysis', 'gc_chemical_elements',
    'gc_hydrothermal_circulation',
}
WATER_IDS = {
    'gt_piezometer_well', 'gt_soil_liquefaction', 'gt_seepage_flownet',
    'gp_pore_fluid_archie', 'gp_gassmann_fluid_sub', 'gp_permeability_kozeny',
    'gl_fluvial_point_bar_channel', 'gc_hydrothermal_circulation',
    'gc_supergene_leaching', 'gc_hydrothermal_boiling_immiscibility',
    'gc_water_activity_ah2o', 'gp_specific_gravity_balance',
}


def polygons(geometry):
    if geometry.geom_type == 'Polygon':
        return [geometry]
    if hasattr(geometry, 'geoms'):
        return [part for part in geometry.geoms if part.geom_type == 'Polygon']
    return []


def holes(geometry, minimum=1800):
    return [Polygon(ring) for polygon in polygons(geometry)
            for ring in polygon.interiors if Polygon(ring).area >= minimum]


def trace(builder):
    records, originals = [], {}
    namespace = builder.__globals__
    for name in PRIMITIVES:
        if name not in namespace or not callable(namespace[name]):
            continue
        original = namespace[name]
        originals[name] = original

        def record(*args, _name=name, _original=original, **kwargs):
            geometry = _original(*args, **kwargs)
            records.append((_name, args, kwargs, geometry))
            return geometry

        namespace[name] = record
    try:
        geometry = builder().buffer(0)
    finally:
        namespace.update(originals)
    return geometry, records


def to_canvas(geometry, bounds):
    x0, y0, x1, y1 = bounds
    factor = 880 / max(x1 - x0, y1 - y0)
    geometry = affinity.translate(geometry, xoff=-(x0 + x1) / 2, yoff=-(y0 + y1) / 2)
    geometry = affinity.scale(geometry, xfact=factor, yfact=factor, origin=(0, 0))
    return affinity.translate(geometry, xoff=500, yoff=500)


def layer(geometry, colour):
    # Shared SVG/PNG renderers use a 24-unit, Y-down canvas.
    geometry = affinity.scale(geometry, xfact=24 / 1000, yfact=-24 / 1000, origin=(0, 0))
    return FlatLayer(affinity.translate(geometry, yoff=24), colour)


def colour_for(identifier, name, args, geometry, accent):
    if identifier == 'gp_magnetic_survey':
        return RED if name in {'ellipse_outline', 'arrow_head'} else MATERIALS['steel'] if name == 'rounded_rect' else INK
    if identifier == 'gp_electromagnetic_em':
        if name == 'ellipse_outline' and args[1] > 600:
            return BLUE if args[0] < 500 else INK
        return BLUE if name in {'curved_arrow', 'arrow_head', 'ellipse_outline'} else MATERIALS['steel']
    if identifier == 'gp_magnetotellurics_mt':
        if name in {'sine_wave', 'arrow'}:
            return BLUE
        if name == 'line' and len(args) >= 4 and args[0] == args[2] == 500:
            return RED
        if name == 'line' and len(args) >= 4 and args[1] == args[3] == 320:
            return BLUE
        return YELLOW if name == 'circle' else INK
    if identifier in {'gp_susceptibility_model', 'gp_koenigsberger_remanence'} and name in {'arrow', 'arrow_head'}:
        return RED
    if identifier in {'gc_temperature_thermo', 'gp_thermal_geothermal'} and name in {'circle', 'rect'}:
        return MATERIALS['heat']
    if identifier == 'gc_biogeochem_vegetation' and name in FILLED:
        return MATERIALS['leaf']
    if identifier == 'gc_aqua_regia_partial_digest' and name == 'regular_poly':
        return MATERIALS['quartz']
    if identifier == 'gl_minerals_specimen':
        return MATERIALS['steel'] if name == 'stroke' else INK
    if identifier in {'gl_style_veined_stringer', 'gl_ptygmatic_vein_fold'} and name in {'line', 'stroke'}:
        return MATERIALS['quartz']
    if identifier in WATER_IDS and name in {'sine_wave', 'curved_arrow', 'arrow'}:
        return MATERIALS['water']
    if identifier in {'gp_ground_penetrating_radar', 'gp_wave_propagation', 'gp_ert_ip'} and name in {'arc', 'curved_arrow'}:
        return BLUE
    if identifier == 'gp_radiometrics_gamma' and name in {'sector', 'circle'}:
        return YELLOW
    if identifier.startswith('gc_') and any(word in identifier for word in ('laser', 'libs')) and name in {'poly', 'arrow'}:
        return RED
    return MATERIALS[accent] if name in FILLED else INK


@lru_cache(maxsize=256)
def _artwork(identifier, builder):
    accent, body = ICON_MATERIALS[identifier]
    raw, records = trace(OVERRIDES.get(identifier, builder))
    cleaned = raw.buffer(.65, quad_segs=4, join_style=1).buffer(-.65, quad_segs=4, join_style=1)
    bounds = cleaned.bounds
    ink_geometry = detailed_font_geometry({'id': identifier, 'builder': builder})
    underpaint, painted = [], []
    abstract = accent == 'ink' and body == 'paper'
    for index, (name, args, kwargs, primitive) in enumerate(records):
        # Fill housing and rock surfaces, but keep field/orbital paths open.
        outline = name in {'rect_outline', 'rounded_rect_outline'}
        closed = name == 'stroke' and (kwargs.get('closed', False) or (len(args[0]) > 2 and args[0][0] == args[0][-1]))
        ring_body = name in {'ring', 'disk_ring'} and identifier not in FIELD_IDS
        if not abstract and (outline or closed or ring_body):
            fill_colour = MATERIALS[body]
            if identifier == 'gl_minerals_specimen':
                fill_colour = MATERIALS['basalt'] if index == 0 else MATERIALS['quartz']
            for pocket in holes(primitive):
                underpaint.append(layer(to_canvas(pocket, bounds), fill_colour))
        colour = colour_for(identifier, name, args, primitive, accent)
        visible = to_canvas(primitive, bounds).intersection(ink_geometry)
        # A solid primitive may only be a temporary construction mask used to
        # derive an outline. Do not let it recolour every internal feature.
        occupied = primitive.intersection(raw).area / max(primitive.area, 1)
        construction_mask = name in FILLED and occupied < .45
        if not construction_mask and not visible.is_empty and visible.area > 12 and colour != INK:
            painted.append(layer(visible, colour))
    if identifier == 'gc_water_activity_ah2o':
        underpaint = [layer(pocket, MATERIALS['water']) for pocket in holes(ink_geometry, 6000)]
    if identifier == 'gc_fluid_inclusion_microtherm':
        underpaint = [layer(pocket, MATERIALS['glass']) for pocket in holes(ink_geometry, 3500)]
    if identifier == 'gc_aqua_regia_partial_digest':
        for pocket in holes(raw):
            if pocket.centroid.y < 300:
                underpaint.append(layer(to_canvas(pocket, bounds), '#E8CD82'))
    if identifier == 'gt_soil_profile_log':
        for pocket in holes(raw):
            height = pocket.centroid.y
            material = 'soil' if height > 700 else 'clay' if height > 500 else 'sand' if height > 300 else 'limestone'
            underpaint.append(layer(to_canvas(pocket, bounds), MATERIALS[material]))
    if identifier == 'gl_stratigraphic_logging':
        for pocket in holes(raw):
            height = pocket.centroid.y
            material = 'limestone' if height > 690 else 'slate' if height > 490 else 'sand' if height > 280 else 'soil'
            underpaint.append(layer(to_canvas(pocket, bounds), MATERIALS[material]))
    layers = underpaint + [layer(ink_geometry, INK)] + painted
    # Geophones and EM receiver loops retain the yellow/black convention.
    for name, args, kwargs, primitive in records:
        receiver = identifier == 'gp_seismic_reflection' and name == 'poly' and primitive.centroid.y > 700
        receiver = receiver or (identifier == 'gp_electromagnetic_em' and name == 'ellipse_outline' and args[0] > 500 and args[1] > 600)
        receiver = receiver or (identifier == 'gp_magnetotellurics_mt' and name == 'circle')
        if receiver:
            geometry = to_canvas(primitive, bounds)
            filled = union_all([Polygon(polygon.exterior) for polygon in polygons(geometry)])
            layers.append(layer(filled, YELLOW))
            layers.append(layer(filled.boundary.buffer(10, quad_segs=4), '#111111'))
    return layers


def artwork(icon):
    from icons_alteration import GEOCHEM_IDS, flat_artwork as geochem_artwork
    if icon["id"] in GEOCHEM_IDS:
        return geochem_artwork(icon["id"])
    from icons_mt import MT_IDS, flat_artwork as mt_artwork
    if icon["id"] in MT_IDS:
        return mt_artwork(icon["id"])
    from icons_geophysics_expanded import EXPANDED_IDS, flat_artwork
    if icon['id'] in EXPANDED_IDS:
        return flat_artwork(icon)
    return _artwork(icon['id'], icon['builder'])
