"""GeoScience visual system: bespoke flat SVG artwork and matching line glyphs.

Artwork is drawn on a 24-unit grid, with 1.5-unit rounded strokes and a
two-unit optical margin. Flat and monochrome forms share the same geometry;
large colour surfaces become outlines in the font. No bitmap dependencies.
"""

import math
from functools import lru_cache
from dataclasses import dataclass
from html import escape

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

INK = "#26354D"
BLUE = "#3478F6"
RED = "#E35D65"
YELLOW = "#F2C94C"
TEAL = "#239D88"
PURPLE = "#8A63CF"
PALE = "#E5ECF4"
WHITE = "#FFFFFF"
STROKE = 1.5


@dataclass
class Layer:
    surface: object
    color: str
    glyph: object
    knockout: object = None


def shape(geometry, color="a", solid=False):
    """A coloured surface whose font counterpart is a clean outline."""
    outline = geometry if solid else geometry.boundary.buffer(STROKE / 2, quad_segs=8, join_style=1)
    return Layer(geometry, color, outline, geometry if not solid else None)


def R(x, y, w, h, color="a", radius=0.7, solid=False):
    radius = min(radius, w / 2, h / 2)
    geometry = box(x + radius, y + radius, x + w - radius, y + h - radius).buffer(radius, quad_segs=8) if radius else box(x, y, x + w, y + h)
    return shape(geometry, color, solid)


def C(x, y, radius, color="a", solid=False):
    return shape(Point(x, y).buffer(radius, quad_segs=20), color, solid)


def P(points, color="a", solid=False):
    return shape(Polygon(points), color, solid)


def E(x, y, rx, ry, color="a", angle=0):
    geometry = affinity.scale(Point(x, y).buffer(1, quad_segs=24), rx, ry, origin=(x, y))
    return shape(affinity.rotate(geometry, angle, origin=(x, y)), color)


def L(points, color=INK, width=STROKE):
    geometry = LineString(points).buffer(width / 2, quad_segs=8, cap_style=1, join_style=1)
    return Layer(geometry, color, geometry)


def A(x0, y0, x1, y1, color=INK):
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    head = Polygon([(x1, y1), (x1 - ux * 2.5 - uy * 1.65, y1 - uy * 2.5 + ux * 1.65), (x1 - ux * 2.5 + uy * 1.65, y1 - uy * 2.5 - ux * 1.65)])
    geometry = unary_union([LineString([(x0, y0), (x1 - ux * 1.4, y1 - uy * 1.4)]).buffer(STROKE / 2, cap_style=1), head])
    return Layer(geometry, color, geometry)


def arc(x, y, radius, start, stop, color=INK):
    return L([(x + radius * math.cos(math.radians(start + (stop - start) * i / 40)), y + radius * math.sin(math.radians(start + (stop - start) * i / 40))) for i in range(41)], color)


def wave(y=12, color="a", amplitude=2, cycles=2, x0=3, x1=21):
    return L([(x0 + (x1 - x0) * i / 80, y + amplitude * math.sin(i / 80 * cycles * 2 * math.pi)) for i in range(81)], color)


def dots(points, color="a", radius=0.85):
    return [C(x, y, radius, color, True) for x, y in points]


def axes():
    return [L([(3, 3), (3, 21), (21, 21)])]


def chart(points, extra=()):
    return axes() + [L(points, "a")] + list(extra)


def crystal(x=12, y=12, scale=1, color="a"):
    points = [(x, y - 9 * scale), (x + 5 * scale, y - 5 * scale), (x + 5 * scale, y + 6 * scale), (x, y + 9 * scale), (x - 5 * scale, y + 6 * scale), (x - 5 * scale, y - 5 * scale)]
    return [P(points, color), L([(x, y - 9 * scale), (x, y + 9 * scale)], WHITE, 1), L([(x - 5 * scale, y - 5 * scale), (x, y - 2 * scale), (x + 5 * scale, y - 5 * scale)], WHITE, 1)]


def cube():
    return [P([(12, 2.5), (21, 7.5), (12, 12.5), (3, 7.5)], "a"), P([(3, 7.5), (12, 12.5), (12, 22), (3, 17)], "p"), P([(12, 12.5), (21, 7.5), (21, 17), (12, 22)], INK)]


def strata():
    return [R(3, 3, 18, 18, "p"), R(3, 3, 18, 6, "a", 0), L([(3, 9), (21, 9)]), L([(3, 15), (21, 15)])]


def rock():
    return [P([(3, 17), (6, 6), (14, 3), (21, 11), (18, 21), (7, 21)], "p")]


def flask():
    return [P([(9, 3), (15, 3), (15, 10), (21, 20), (20, 21), (4, 21), (3, 20), (9, 10)], "p"), P([(6, 16), (18, 16), (20, 20), (4, 20)], "a"), L([(8, 3), (16, 3)])]


def drop(x=12, y=12, size=8, color="a"):
    # Rounded teardrop constructed from a circle and tangent shoulders.
    geometry = unary_union([Point(x, y + size * .35).buffer(size * .55, quad_segs=20), Polygon([(x, y - size), (x + size * .49, y + size * .1), (x - size * .49, y + size * .1)])]).convex_hull
    return shape(geometry, color)


def tunnel():
    return [R(3, 3, 18, 18, "p"), C(12, 13, 6, "a"), R(6, 13, 12, 8, "a", 0), L([(3, 21), (21, 21)])]


def cycle():
    return [arc(12, 12, 8, 205, 370, "a"), arc(12, 12, 8, 25, 190, INK), P([(20, 7), (20, 13), (15, 10)], "a", True), P([(4, 17), (4, 11), (9, 14)], INK, True)]


def bars(values=(8, 15, 11)):
    return [R(4 + i * 6, 21 - height, 4, height, "a" if i != 1 else INK, 0.8) for i, height in enumerate(values)]


def receiver(x, y):
    geometry = Point(x, y).buffer(1.55, quad_segs=16)
    return [shape(geometry.buffer(.38), "#111111", True), shape(geometry, YELLOW)]


def lattice():
    return [R(3, 3, 18, 18, "p"), L([(3, 9), (21, 9)]), L([(3, 15), (21, 15)]), L([(9, 3), (9, 21)]), L([(15, 3), (15, 21)])]


def thermometer():
    return [R(9, 3, 6, 13, "p", 3), C(12, 17, 4, "a"), L([(12, 7), (12, 17)], "a", 2)]


def magnet():
    return [L([(5, 4), (5, 13), (6, 17), (9, 20), (15, 20), (18, 17), (19, 13), (19, 4)], RED, 4), R(3, 3, 4, 5, INK, .4, True), R(17, 3, 4, 5, INK, .4, True)]


def atom():
    return [E(12, 12, 10, 4, "p", 0), E(12, 12, 10, 4, "a", 60), E(12, 12, 10, 4, "p", -60), C(12, 12, 2, INK, True)]


@lru_cache(maxsize=1)
def build_recipes():
    """Every ID has a deliberate composition; no name-hash or generic fallback."""
    return {
        "gp_seismic_reflection": [R(3, 15, 18, 6, "p"), L([(3, 9), (21, 9)]), L([(5, 9), (12, 18), (19, 9)], BLUE), C(5, 6, 1.6, BLUE, True)] + receiver(19, 7),
        "gp_gravity_survey": [R(4, 3, 10, 14, "p"), L([(9, 5), (7, 7), (11, 9), (7, 11), (9, 13)]), R(6, 13, 6, 3, "a"), A(19, 4, 19, 19), L([(3, 21), (21, 21)])],
        "gp_magnetic_survey": magnet(),
        "gp_electromagnetic_em": [E(7, 6, 4, 2, BLUE), E(17, 6, 4, 2, RED), L([(7, 8), (7, 12), (17, 12), (17, 8)], INK), arc(12, 12, 5, 15, 165, BLUE), arc(12, 12, 9, 20, 160, BLUE)],
        "gp_ert_ip": [L([(3, 8), (21, 8)], BLUE), L([(5, 5), (5, 12)]), L([(19, 5), (19, 12)]), arc(12, 10, 5, 10, 170, BLUE), arc(12, 10, 9, 10, 170, BLUE)] + receiver(9, 8) + receiver(15, 8),
        "gp_velocity_model": strata() + [L([(5, 7), (9, 5), (13, 7), (18, 5)], WHITE, 1.2)],
        "gp_density_model": lattice() + [R(9, 9, 6, 6, INK, 0), R(15, 15, 6, 6, "a", 0)],
        "gp_susceptibility_model": [R(3, 3, 18, 18, "p")] + [A(x, y + 2, x + 2, y - 1, RED) for x, y in [(6, 7), (14, 7), (6, 16), (14, 16)]],
        "gp_resistivity_section": [P([(3, 5), (21, 5), (17, 21), (7, 21)], "p"), P([(7, 10), (17, 10), (15, 17), (9, 17)], BLUE), L([(3, 5), (21, 5)])] + receiver(6, 4) + receiver(12, 4) + receiver(18, 4),
        "gp_seismic_cube_3d": cube() + [L([(4, 12), (12, 17), (20, 12)], WHITE, 1.1), L([(4, 16), (12, 21), (20, 16)], WHITE, 1.1)],
        "gp_wave_propagation": [C(5, 12, 1.5, "a", True), arc(5, 12, 5, -70, 70, BLUE), arc(5, 12, 10, -60, 60, BLUE), arc(5, 12, 15, -40, 40, BLUE)],
        "gp_ray_refraction_snell": [R(3, 12, 18, 9, "p"), L([(3, 12), (21, 12)]), A(5, 4, 12, 12, BLUE), A(12, 12, 21, 17, BLUE)],
        "gp_geophysical_inversion": cycle() + [R(8, 8, 8, 8, "p"), L([(8, 12), (16, 12)])],
        "gp_signal_deconvolution": [wave(7, BLUE, 2, 2, 3, 10), A(12, 12, 19, 12), L([(15, 21), (15, 17), (17, 17), (17, 4)], "a")],
        "gp_nmo_stacking": [L([(3, 4), (6, 4), (8, 8), (10, 4), (12, 4)], "p"), L([(3, 10), (8, 10), (10, 14), (12, 10), (14, 10)], "a"), L([(3, 16), (10, 16), (12, 20), (14, 16), (17, 16)], INK), A(19, 4, 19, 21)],
        "gt_spt_test": [R(9, 2.5, 6, 6, "a"), L([(12, 9), (12, 21)], INK, 2), R(8, 15, 8, 6, "p"), A(5, 4, 5, 12), L([(3, 14), (7, 14)]), L([(17, 14), (21, 14)])],
        "gt_cpt_cone": [R(10, 3, 4, 13, "a"), P([(8, 16), (16, 16), (12, 22)], INK), L([(3, 12), (7, 12)]), L([(17, 12), (21, 12)])],
        "gt_triaxial_shear": [R(6, 5, 12, 14, "p", 2), R(9, 8, 6, 8, "a"), A(12, 2, 12, 7), A(12, 22, 12, 17), A(2, 12, 7, 12), A(22, 12, 17, 12)],
        "gt_piezometer_well": [R(3, 12, 18, 9, "p"), R(10, 3, 4, 18, INK, 0), R(11, 12, 2, 8, BLUE, 0, True), wave(14, BLUE, .8, 2)],
        "gt_inclinometer_casing": [R(8, 3, 8, 18, "p"), L([(11, 20), (11, 13), (14, 7), (14, 3)], "a"), L([(3, 12), (5, 12)]), L([(19, 12), (21, 12)])],
        "gt_mohr_coulomb": chart([(4, 18), (21, 7)], [arc(12, 20, 6, 180, 360, INK)]),
        "gt_rock_mass_rmr_gsi": rock() + [L([(6, 6), (15, 12), (7, 21)]), L([(3, 17), (15, 12), (21, 11)])],
        "gt_slope_stability_grid": [P([(3, 5), (9, 5), (15, 15), (21, 17), (21, 21), (3, 21)], "p"), arc(7, 7, 11, 0, 90, "a"), A(16, 8, 21, 13)],
        "gt_soil_profile_log": strata() + dots([(6, 12), (12, 12), (18, 12)], INK, .7),
        "gt_fe_mesh_tunnel": tunnel() + [L([(3, 3), (8, 8)]), L([(21, 3), (16, 8)]), L([(3, 12), (6, 13)]), L([(21, 12), (18, 13)])],
        "gt_consolidation_settlement": [R(3, 15, 18, 6, "p"), R(5, 11, 14, 3, "a"), A(8, 3, 8, 9), A(16, 3, 16, 9), L([(3, 18), (21, 18)])],
        "gt_soil_liquefaction": [R(3, 15, 18, 6, "p"), wave(18, BLUE, 1, 2), R(8, 7, 8, 5, "a"), A(5, 14, 5, 5, BLUE), A(19, 14, 19, 5, BLUE)],
        "gt_slope_landslide": [P([(3, 4), (7, 5), (14, 16), (21, 19), (21, 21), (3, 21)], "p"), P([(8, 6), (16, 12), (13, 16)], "a"), A(15, 5, 21, 11)],
        "gt_seepage_flownet": [R(9, 3, 6, 12, INK, .4), L([(3, 12), (7, 18), (12, 21), (17, 18), (21, 12)], BLUE), L([(3, 6), (4, 15), (9, 21)], "a"), A(19, 9, 21, 5, BLUE)],
        "gt_rock_burst_spalling": tunnel() + [P([(12, 5), (10, 10), (13, 9), (11, 15), (16, 8), (13, 9)], INK, True)],
        "gl_strike_dip_mapping": [C(12, 12, 9, "p"), L([(7, 18), (17, 6)]), L([(12, 12), (17, 16)], "a", 2), P([(12, 2), (10, 5), (14, 5)], "a", True)],
        "gl_diamond_core_drilling": [R(7, 3, 10, 13, "p"), R(9, 4, 6, 12, "a"), P([(8, 16), (16, 16), (14, 20), (10, 20)], INK), L([(10, 8), (14, 10)], WHITE, 1.2)],
        "gl_thin_section_petrography": [C(12, 12, 9, "p"), P([(7, 7), (13, 5), (15, 12), (10, 17), (6, 13)], "a"), L([(15, 12), (20, 14)]), L([(10, 17), (11, 21)])],
        "gl_stratigraphic_logging": strata() + [L([(7, 3), (7, 21)]), L([(9, 12), (18, 12)], WHITE, 1.2)],
        "gl_structural_stereonet": [C(12, 12, 9, "p"), E(12, 12, 4, 9, "a"), L([(3, 12), (21, 12)], WHITE, 1.2)] + dots([(14, 8), (16, 15)], INK),
        "gl_block_model_3d": cube() + [L([(7.5, 10), (7.5, 19.5)], WHITE, 1), L([(16.5, 10), (16.5, 19.5)], WHITE, 1), L([(3, 12.5), (12, 17.5), (21, 12.5)], WHITE, 1)],
        "gl_wireframe_mesh": [P([(12, 2.5), (21, 9), (18, 21), (5, 20), (3, 8)], "p"), L([(12, 2.5), (9, 12), (18, 21), (21, 9), (9, 12), (5, 20), (3, 8), (9, 12)], "a")],
        "gl_faulted_stratigraphy": [P([(3, 4), (11, 4), (7, 20), (3, 20)], "a"), P([(14, 7), (21, 7), (21, 21), (10, 21)], "p"), L([(3, 11), (9, 11)]), L([(12, 14), (21, 14)]), L([(12, 3), (8, 21)])],
        "gl_folded_anticline_model": [wave(8, "a", 3, 1), wave(13, INK, 3, 1), wave(18, "a", 3, 1)],
        "gl_intrusive_pluton_model": strata() + [P([(6, 21), (7, 16), (11, 13), (11, 5), (14, 5), (14, 13), (18, 16), (19, 21)], INK)],
        "gl_plate_subduction": [P([(3, 8), (11, 8), (21, 19), (18, 21), (9, 12), (3, 12)], "a"), P([(14, 8), (21, 8), (21, 12), (17, 12)], "p"), A(4, 4, 10, 4), A(21, 4, 15, 4)],
        "gl_fault_slip_tectonics": [P([(3, 5), (11, 5), (7, 18), (3, 18)], "a"), P([(15, 8), (21, 8), (21, 21), (11, 21)], "p"), A(8, 12, 10, 4), A(14, 12, 12, 20)],
        "gl_sedimentation_deposition": [R(3, 16, 18, 5, "p"), L([(3, 18.5), (21, 18.5)]), A(6, 4, 6, 13, "a"), A(12, 3, 12, 13, "a"), A(18, 4, 18, 13, "a")],
        "gl_metamorphism_pt": crystal(12, 12, .75) + [A(2, 12, 6, 12), A(22, 12, 18, 12), A(12, 2, 12, 6), A(12, 22, 12, 18)],
        "gl_weathering_erosion": [P([(3, 21), (5, 7), (12, 4), (16, 12), (12, 21)], "p"), L([(6, 8), (10, 13), (6, 17)])] + dots([(18, 8), (20, 14), (17, 20)], "a", 1.3),
        "gc_soil_stream_sampling": [wave(16, BLUE, 2, 1), R(15, 11, 5, 9, "a"), L([(6, 3), (6, 13)]), P([(3, 11), (9, 11), (8, 16), (6, 18), (4, 16)], INK)],
        "gc_pxrf_analyzer": [P([(3, 5), (16, 5), (16, 11), (11, 11), (9, 21), (4, 20), (6, 11), (3, 11)], "a"), R(6, 7, 6, 2, "p", .2), A(18, 8, 22, 8)],
        "gc_icp_ms_spectrometry": chart([(4, 19), (7, 19), (8, 10), (10, 19), (13, 19), (15, 4), (17, 19), (21, 19)]),
        "gc_fire_assay": [P([(5, 3), (19, 3), (17, 13), (7, 13)], "p"), R(7, 11, 10, 3, "a"), drop(12, 19, 3, RED), L([(3, 16), (7, 16)]), L([(17, 16), (21, 16)])],
        "gc_isotope_ratio_analysis": atom() + dots([(20, 12), (7, 5)], INK, 1.3),
        "gc_alteration_zonation": [C(12, 12, 10, "p"), C(12, 12, 6.5, "a"), C(12, 12, 3, INK, True)],
        "gc_geochem_anomaly_contours": [E(12, 12, 9, 7, "p", -25), E(12, 12, 6, 4.5, "a", -25), E(12, 12, 2.5, 2, INK, -25)],
        "gc_ternary_classification": [P([(12, 3), (22, 21), (2, 21)], "p"), L([(7, 12), (17, 12)]), L([(7, 21), (14.5, 7.5)], WHITE, 1.1)] + dots([(13, 16)], "a", 1.7),
        "gc_eh_ph_pourbaix": axes() + [P([(4, 4), (20, 4), (20, 12), (4, 8)], "p"), P([(4, 9), (20, 13), (20, 20), (4, 20)], "a"), L([(4, 9), (20, 13)])],
        "gc_downhole_geochem_log": [R(3, 3, 5, 18, INK), L([(11, 3), (11, 21)], "p", 2), L([(13, 4), (19, 7), (14, 11), (21, 15), (16, 20)], "a")],
        "gc_hydrothermal_circulation": cycle() + [drop(12, 12, 3, RED)],
        "gc_supergene_leaching": [R(3, 3, 18, 6, "p"), R(3, 17, 18, 4, "a"), A(7, 10, 7, 15), A(17, 10, 17, 15)],
        "gc_redox_front_roll": [R(3, 3, 18, 18, "p"), L([(5, 5), (13, 6), (17, 12), (13, 18), (5, 19)], "a", 3), A(3, 12, 11, 12)],
        "gc_magmatic_differentiation": [R(5, 3, 14, 18, "p", 5), R(6, 16, 12, 4, "a"), A(9, 14, 9, 6), A(15, 14, 15, 6)] + dots([(9, 18), (15, 18)], INK),
        "gc_element_dispersion_halo": [R(3, 9, 4, 12, INK), A(9, 7, 20, 4, "a"), A(9, 12, 21, 12, "a"), A(9, 17, 20, 20, "a")],
        "gp_self_potential": [C(12, 7, 4, "p"), L([(10, 6), (12, 9), (14, 6)], BLUE), L([(8, 7), (4, 7), (4, 16)]), L([(16, 7), (20, 7), (20, 16)]), P([(8, 21), (12, 13), (16, 21)], "a")],
        "gp_magnetotellurics_mt": [wave(5, BLUE, 1.5, 2), L([(3, 11), (21, 11)]), A(5, 17, 19, 17, BLUE), A(12, 21, 12, 13, RED)] + receiver(5, 17),
        "gp_ground_penetrating_radar": [R(7, 3, 10, 4, BLUE), C(8, 8, 1, INK, True), C(16, 8, 1, INK, True), L([(3, 10), (21, 10)]), arc(12, 10, 5, 25, 155, BLUE), arc(12, 10, 9, 25, 155, BLUE), C(12, 20, 1.5, INK, True)],
        "gp_radiometrics_gamma": [C(12, 12, 2, INK, True)] + [P([(12 + 4 * math.cos(math.radians(a)), 12 + 4 * math.sin(math.radians(a))), (12 + 9 * math.cos(math.radians(a - 25)), 12 + 9 * math.sin(math.radians(a - 25))), (12 + 9 * math.cos(math.radians(a + 25)), 12 + 9 * math.sin(math.radians(a + 25)))], YELLOW) for a in [-90, 30, 150]],
        "gp_nmr_sounding": [E(9, 12, 6, 9, "p"), L([(9, 4), (9, 20)], RED), A(9, 14, 14, 7, BLUE), wave(12, BLUE, 2, 1, 16, 22)],
        "gp_thermal_geothermal": thermometer() + [A(20, 20, 20, 5, RED), L([(3, 12), (6, 12)])],
        "gp_acoustics_sonar": [P([(3, 6), (7, 6), (10, 11), (3, 11)], "a"), arc(7, 9, 7, 5, 85, BLUE), arc(7, 9, 12, 5, 85, BLUE), L([(3, 21), (8, 18), (14, 21), (21, 18)], INK)],
        "gp_geodesy_insar_gnss": [R(9, 4, 6, 6, "a"), R(2, 4, 5, 6, "p"), R(17, 4, 5, 6, "p"), A(12, 12, 12, 19), E(12, 20, 7, 2, INK)],
        "gp_remote_sensing_hyperspectral": [P([(3, 4), (12, 8), (21, 4), (12, 2)], "a"), P([(3, 9), (12, 13), (21, 9), (12, 7)], "p"), P([(3, 14), (12, 18), (21, 14), (12, 12)], INK), A(12, 19, 12, 22)],
        "gp_matrix_mixing_bounds": chart([(4, 19), (9, 17), (14, 12), (20, 4)], [L([(4, 19), (11, 9), (20, 4)], INK)]),
        "gp_pore_fluid_archie": [R(3, 3, 18, 18, "p")] + [C(x, y, 2.4, BLUE) for x, y in [(7, 7), (17, 7), (7, 17), (17, 17)]] + [L([(5, 12), (19, 12)], INK)],
        "gp_ip_cole_cole": chart([(4, 19), (5, 14), (8, 10), (12, 8), (16, 10), (19, 14), (20, 19)]),
        "gp_dielectric_permittivity": [R(4, 3, 4, 18, BLUE), R(16, 3, 4, 18, RED), A(10, 8, 14, 8), A(10, 16, 14, 16)],
        "gp_koenigsberger_remanence": [R(4, 4, 16, 16, "p"), A(7, 17, 17, 7, RED), A(7, 17, 7, 7, BLUE)],
        "gp_gassmann_fluid_sub": [R(2.5, 4, 7, 16, "p"), R(14.5, 4, 7, 16, "a"), C(6, 12, 2, BLUE), drop(18, 12, 3, WHITE), A(10, 12, 14, 12)],
        "gp_permeability_kozeny": [C(6, 6, 3, "p"), C(18, 6, 3, "p"), C(6, 18, 3, "p"), C(18, 18, 3, "p"), A(3, 12, 21, 12, BLUE)],
        "gt_deere_rqd": [R(3, 8, 5, 9, "a"), R(10, 8, 9, 9, "p"), R(21, 8, 1, 9, INK, .3, True), L([(3, 4), (21, 4)]), L([(3, 3), (3, 5)]), L([(21, 3), (21, 5)])],
        "gt_barton_q_tunnel": tunnel() + [L([(5, 10), (8, 12)], WHITE), L([(19, 10), (16, 12)], WHITE), L([(12, 4), (12, 8)], WHITE)],
        "gt_bieniawski_rmr": [R(4, 3, 16, 18, "p")] + [R(7, y, width, 2, "a", .5, True) for y, width in [(6, 10), (11, 7), (16, 9)]],
        "gt_hoek_brown_criterion": chart([(4, 19), (7, 13), (11, 9), (15, 6), (20, 4)], [L([(4, 19), (20, 9)], INK)]),
        "gt_ucs_from_velocity": [R(8, 6, 8, 12, "p"), wave(12, "a", 2, 1, 3, 21), A(12, 2, 12, 5), A(12, 22, 12, 19)],
        "gt_brittleness_index": rock() + [L([(12, 4), (9, 10), (14, 13), (10, 21)], INK), A(2, 12, 6, 12), A(22, 12, 18, 12)],
        "gl_rock_type_igneous": [P([(2.5, 21), (9, 7), (15, 7), (21.5, 21)], "a"), L([(9, 7), (12, 10), (15, 7)], WHITE), L([(10, 4), (12, 2), (14, 4)], INK)] + dots([(7, 18), (13, 16), (17, 19)], INK),
        "gl_rock_type_sedimentary": strata() + dots([(6, 18), (12, 18), (18, 18)], INK),
        "gl_rock_type_metamorphic": [R(3, 3, 18, 18, "p"), wave(8, "a", 1.5, 1), wave(13, INK, 1.5, 1), wave(18, "a", 1.5, 1)],
        "gl_composition_category": [R(3, 3, 8, 8, "a"), R(13, 3, 8, 8, "p"), P([(12, 13), (20, 21), (4, 21)], INK)],
        "gl_genetic_category": cycle() + [P([(10, 9), (15, 10), (14, 15), (9, 15)], "a")],
        "gl_metamorphic_facies_pt": axes() + [P([(5, 19), (9, 10), (14, 5), (20, 4), (18, 13)], "p"), L([(5, 19), (14, 12), (20, 4)], "a"), L([(9, 10), (18, 13)], INK)],
        "gl_consolidation_degree": dots([(4, 5), (4, 12), (4, 19)], "a", 1.5) + [A(8, 12, 13, 12), R(16, 4, 5, 16, INK)],
        "gl_deformation_brittle_ductile": [L([(3, 4), (8, 10), (4, 15), (9, 21)], INK), wave(12, "a", 3, 1, 13, 21)],
        "gl_unit_morphology": [E(7, 7, 4, 2, "a"), E(17, 7, 4, 2, "a"), P([(3, 21), (6, 16), (12, 13), (18, 16), (21, 21)], "p")],
        "gl_style_disseminated": [R(3, 3, 18, 18, "p")] + dots([(7, 7), (15, 6), (11, 12), (18, 14), (6, 17), (14, 19)], "a", 1.1),
        "gl_style_net_textured": [R(3, 3, 18, 18, "a")] + [C(x, y, 3, "p") for x, y in [(7, 7), (17, 7), (12, 16)]],
        "gl_style_massive_sulfide": [R(3, 3, 18, 18, "a"), L([(5, 18), (18, 5)], WHITE, 2)] + dots([(7, 7), (17, 17)], INK, 1.5),
        "gl_style_veined_stringer": [R(3, 3, 18, 18, "p"), L([(4, 6), (12, 12), (20, 17)], "a", 2), L([(12, 12), (18, 4)], "a", 2), L([(12, 12), (6, 20)], "a", 2)],
        "gl_particle_shape_roundness": [P([(4, 4), (10, 3), (11, 10), (3, 11)], "a"), C(18, 7, 3, INK), E(12, 18, 9, 3, "p")],
        "gl_contact_unconformity": [R(3, 3, 18, 18, "p"), L([(3, 11), (6, 9), (10, 12), (15, 9), (21, 11)], "a", 2), L([(6, 13), (3, 21)]), L([(13, 13), (10, 21)]), L([(20, 13), (17, 21)])],
        "gl_foliation_lineation": [P([(8, 3), (22, 7), (16, 21), (2, 17)], "p"), L([(10, 6), (5, 17)], "a"), L([(15, 7), (10, 18)], "a"), A(19, 8, 14, 19)],
        "gl_borehole_drilling_methods": [L([(12, 3), (12, 17)], INK, 3), P([(7, 17), (17, 17), (12, 22)], "a"), L([(8, 6), (16, 9), (8, 12), (16, 15)], "a")],
        "gl_planar_polarity_overturned": [L([(5, 3), (5, 21)]), L([(5, 9), (10, 9)], "a"), L([(16, 3), (16, 21)]), arc(16, 12, 4, 90, 270, "a"), A(16, 16, 21, 16)],
        "gm_acid_rock_drainage": rock() + [drop(16, 16, 5, YELLOW), L([(13, 16), (19, 16)], INK), L([(16, 13), (16, 19)], INK)],
        "gm_comminution_work_index": [P([(3, 3), (10, 3), (8, 11)], INK), P([(14, 3), (21, 3), (16, 11)], INK), A(12, 8, 12, 15)] + dots([(7, 18), (12, 21), (17, 18)], "a", 1.8),
        "gm_flotation_recovery": [R(3, 8, 18, 13, "p"), wave(14, BLUE, 1, 2), C(8, 10, 2, "a"), C(16, 6, 2, "a"), C(12, 3, 1, "a", True)],
        "gc_melt_chemistry_f02": flask() + [C(12, 12, 1.5, RED, True)],
        "gc_carbon_mineralisation": crystal(12, 14, .7) + [A(12, 2, 12, 8), L([(3, 13), (5, 13)]), L([(19, 13), (21, 13)])],
        "gl_lithology_tensor_anisotropy": [E(12, 12, 10, 5, "p", -30), L([(5, 16), (19, 8)], "a"), L([(9, 5), (15, 19)], INK)],
        "gl_fault_normal_graben": [P([(3, 5), (8, 5), (12, 17), (3, 17)], "a"), P([(16, 5), (21, 5), (21, 17), (12, 17)], "a"), P([(9, 10), (15, 10), (12, 19)], "p"), A(3, 2, 7, 2), A(21, 2, 17, 2)],
        "gl_fault_thrust_ramp": [P([(3, 16), (8, 16), (15, 7), (21, 7), (21, 12), (17, 12), (10, 21), (3, 21)], "a"), L([(3, 12), (7, 12), (14, 3), (21, 3)], INK), A(4, 7, 10, 7)],
        "gl_fault_strike_slip_dextral": [R(3, 3, 8, 18, "p"), R(14, 3, 7, 18, "a"), A(7, 17, 7, 7), A(17, 7, 17, 17)],
        "gl_shear_zone_sigmoidal": [L([(3, 4), (21, 4)]), L([(3, 20), (21, 20)]), E(12, 12, 7, 3, "a", -30), A(3, 2, 10, 2), A(21, 22, 14, 22)],
        "gl_chevron_kink_fold": [L([(3, 18), (7, 6), (12, 17), (17, 6), (21, 18)], "a", 2), L([(3, 12), (7, 2), (12, 12), (17, 2), (21, 12)], INK)],
        "gl_ptygmatic_vein_fold": [R(3, 3, 18, 18, "p"), L([(5, 5), (17, 6), (7, 11), (18, 15), (7, 18), (17, 20)], "a", 2)],
        "gl_columnar_jointing": [P([(3, 8), (6, 5), (9, 8), (9, 19), (6, 22), (3, 19)], "p"), P([(9, 5), (12, 2), (15, 5), (15, 19), (12, 22), (9, 19)], "a"), P([(15, 8), (18, 5), (21, 8), (21, 19), (18, 22), (15, 19)], INK)],
        "gl_spinifex_texture": [R(3, 3, 18, 18, "p"), P([(5, 20), (11, 4), (10, 17)], "a"), P([(9, 20), (19, 5), (14, 18)], INK), L([(5, 6), (20, 17)], "a")],
        "gl_pillow_lava": [E(8, 8, 5, 4, "a", -20), E(17, 9, 4, 5, "p", 30), E(11, 18, 7, 3.5, INK)],
        "gl_fiamme_ignimbrite": [R(3, 3, 18, 18, "p"), E(10, 7, 6, 1.5, "a"), E(15, 12, 5, 1.5, INK), E(9, 17, 5, 1.5, "a")],
        "gl_banded_iron_formation": [R(3, 3, 18, 18, "p")] + [R(3, y, 18, 2.5, INK if y == 10 else "a", 0, True) for y in [4, 10, 16]],
        "gl_hydrothermal_breccia": [P([(4, 3), (12, 4), (9, 12), (3, 10)], "a"), P([(16, 4), (21, 6), (20, 14), (12, 11)], "p"), P([(6, 15), (13, 14), (11, 21), (3, 21)], INK), P([(16, 16), (20, 17), (21, 21), (15, 21)], "a")],
        "gl_potassic_alteration": [R(3, 3, 18, 18, "p"), R(8, 3, 3, 18, "a", 0), R(14, 3, 4, 18, INK, 0)] + dots([(5, 8), (20, 16)], "a"),
        "gl_phyllic_sericitic_alteration": [R(3, 3, 18, 18, "p")] + [P([(x, y), (x + 4, y - 1), (x + 3, y + 2), (x - 1, y + 3)], "a") for x, y in [(6, 6), (15, 7), (8, 15), (16, 16)]],
        "gl_advanced_argillic": [R(3, 3, 18, 18, "a")] + [C(x, y, r, "p") for x, y, r in [(7, 8, 2.2), (16, 7, 3), (11, 16, 3.5), (19, 18, 1.5)]],
        "gl_propylitic_chlorite_epidote": [P([(4, 20), (7, 4), (10, 3), (9, 19)], "a"), P([(11, 20), (15, 4), (18, 5), (15, 21)], "p"), P([(18, 21), (20, 12), (22, 13), (21, 21)], INK)],
        "gl_serpentinite_mesh": lattice() + dots([(6, 6), (12, 12), (18, 18)], "a", 1.4),
        "gl_skarn_calc_silicate": [R(3, 3, 7, 18, "p"), R(14, 3, 7, 18, "a"), P([(10, 7), (14, 12), (10, 17)], INK), A(3, 12, 8, 12), A(21, 12, 16, 12)],
        "gl_greisen_cassiterite": [P([(4, 4), (8, 4), (16, 20), (12, 20)], "a"), P([(16, 4), (20, 4), (12, 20), (8, 20)], INK)],
        "gl_tourmaline_sun_rosette": [C(12, 12, 2, "a", True)] + [L([(12 + 3 * math.cos(i * math.pi / 6), 12 + 3 * math.sin(i * math.pi / 6)), (12 + 9 * math.cos(i * math.pi / 6), 12 + 9 * math.sin(i * math.pi / 6))], "a" if i % 2 else INK) for i in range(12)],
        "gl_turbidite_bouma_sequence": strata() + [L([(4, 5), (20, 5)], WHITE, 1), wave(12, "a", .7, 2)] + dots([(6, 18), (12, 18), (18, 18)], INK),
        "gl_fluvial_point_bar_channel": [R(3, 3, 18, 18, "p"), L([(8, 3), (6, 7), (15, 12), (18, 17), (14, 21)], BLUE, 4), E(12, 14, 3, 1.8, "a", 30)],
        "gc_la_icp_ms_laser": [R(9, 3, 6, 5, INK), P([(10, 8), (14, 8), (12, 16)], RED, True), R(3, 18, 18, 3, "p"), A(5, 15, 9, 15, "a"), A(15, 15, 20, 15, "a")],
        "gc_epma_wds_microprobe": [R(4, 3, 6, 7, INK), A(7, 11, 7, 18, "a"), R(3, 19, 12, 2, "p"), arc(12, 12, 8, -80, 50, "a"), R(17, 9, 4, 5, "a")],
        "gc_xrd_diffractometer": [R(3, 4, 5, 5, "a"), R(16, 4, 5, 5, INK), L([(6, 10), (12, 19), (18, 10)], "a"), R(8, 19, 8, 2, "p"), arc(12, 16, 10, 210, 330, INK)],
        "gc_xanes_synchrotron": [C(9, 10, 6, "p"), C(9, 10, 3, "a"), A(14, 13, 21, 20), L([(15, 8), (17, 8), (18, 3), (21, 3)], INK)],
        "gc_libs_laser_plasma": [R(3, 18, 18, 3, "p"), R(9, 3, 6, 5, INK), A(12, 8, 12, 14, RED), C(12, 16, 2.5, "a"), L([(5, 12), (7, 14)], "a"), L([(19, 12), (17, 14)], "a")],
        "gc_ftir_raman_spectroscopy": [wave(6, "a", 1, 3), L([(3, 21), (7, 21), (9, 11), (11, 21), (14, 21), (17, 8), (20, 21)], INK)],
        "gc_four_acid_total_digest": [R(6, 3, 12, 18, "p", 2), R(7, 13, 10, 7, "a"), wave(15, WHITE, .7, 1, 8, 16)] + dots([(9, 6), (15, 6)], INK),
        "gc_aqua_regia_partial_digest": flask() + dots([(10, 17), (15, 19)], INK, .8),
        "gc_cyanide_bottle_roll": [R(4, 4, 16, 13, "p", 3), R(4, 11, 16, 5, "a"), C(7, 21, 1.5, INK, True), C(17, 21, 1.5, INK, True), L([(10, 7), (14, 7)], INK)],
        "gc_sequential_extraction": [R(3, 5, 4, 16, "p", 2), R(10, 5, 4, 16, "p", 2), R(17, 5, 4, 16, "p", 2), R(3, 15, 4, 6, "a", 1), R(10, 11, 4, 10, "a", 1), R(17, 8, 4, 13, "a", 1), L([(3, 3), (21, 3)])],
        "gc_gas_chromatography_ms": [E(7, 8, 4, 5, "p"), E(7, 14, 4, 5, "a"), L([(13, 21), (15, 21), (16, 10), (18, 21), (20, 5), (22, 21)], INK)],
        "gc_sims_shrimp_microprobe": [A(3, 4, 10, 15, "a"), R(5, 18, 14, 3, "p"), A(13, 15, 20, 5), C(20, 5, 2, "a")],
        "gc_tims_thermal_ionization": [R(3, 3, 18, 18, "p"), R(6, 16, 12, 2, INK), L([(9, 14), (9, 9)], RED), L([(15, 14), (15, 9)], RED), A(12, 9, 12, 4, "a")],
        "gc_stable_isotope_gas_irms": [R(3, 5, 7, 5, "a"), L([(10, 7), (14, 7), (19, 15)], INK), L([(10, 7), (13, 7), (13, 18)], "a"), C(13, 20, 1.5, INK, True), C(20, 17, 1.5, INK, True)],
        "gc_fluid_inclusion_microtherm": crystal() + [C(12, 13, 2.8, "p"), C(13, 12, .9, INK, True)],
        "gc_radon_emanometry": [R(9, 3, 6, 6, "a"), L([(12, 9), (12, 21)], INK, 2), L([(3, 15), (9, 15)]), L([(15, 15), (21, 15)]), A(5, 21, 5, 17), A(19, 21, 19, 17)],
        "gc_biogeochem_vegetation": [L([(12, 21), (12, 8)], INK), E(7, 9, 5, 2.8, TEAL, 30), E(17, 6, 5, 2.8, TEAL, -30), L([(8, 22), (12, 19), (16, 22)], "a")],
        "gc_ree_chondrite_spidergram": chart([(4, 5), (7, 8), (10, 7), (13, 15), (16, 13), (20, 18)], dots([(4, 5), (10, 7), (16, 13), (20, 18)], INK)),
        "gc_primitive_mantle_spidergram": chart([(4, 8), (7, 14), (10, 5), (13, 17), (16, 12), (20, 16)], dots([(4, 8), (10, 5), (16, 12)], INK)),
        "gc_tas_volcanic_diagram": axes() + [P([(4, 20), (4, 12), (12, 8), (20, 4), (20, 20)], "p"), L([(4, 12), (20, 4)], "a"), L([(11, 10), (11, 20)]), L([(16, 6), (16, 20)])],
        "gc_qapf_ternary_double": [P([(12, 2.5), (21.5, 12), (12, 21.5), (2.5, 12)], "p"), P([(12, 2.5), (21.5, 12), (2.5, 12)], "a"), L([(3, 12), (21, 12)]), L([(12, 3), (12, 21)], WHITE, 1.2)],
        "gc_pearce_tectonic_discrimination": axes() + [P([(4, 20), (12, 12), (20, 14), (20, 20)], "p"), L([(5, 4), (12, 12), (20, 14)], "a"), L([(12, 12), (20, 5)], "a")] + dots([(8, 9), (16, 17)], INK),
        "gc_activity_activity_diagram": axes() + [P([(4, 20), (10, 13), (15, 13), (20, 4), (20, 20)], "p"), L([(4, 20), (10, 13), (15, 13), (20, 4)], "a"), L([(10, 13), (10, 4)]), L([(15, 13), (15, 20)])],
        "gc_zircon_upb_concordia": chart([(4, 19), (8, 18), (12, 15), (16, 10), (20, 3)], [L([(4, 19), (20, 3)], INK)]),
        "gc_rb_sr_isochron_diagram": chart([(4, 19), (20, 4)], dots([(7, 16), (12, 12), (18, 6)], INK, 1.3)),
        "gc_sulfur_isotope_delta34s": [L([(3, 12), (21, 12)]), L([(12, 3), (12, 21)]), R(8, 6, 8, 3, "a", .4), R(10, 15, 9, 3, INK, .4)],
        "gc_swir_mineral_spectral_trough": chart([(4, 7), (9, 8), (12, 18), (15, 8), (20, 7)], [A(12, 3, 12, 9)]),
        "gc_campbell_vectoring_ratio": chart([(4, 19), (9, 18), (13, 14), (17, 8), (20, 3)], [C(20, 3, 1.2, INK, True)]),
        "gc_alumina_saturation_asi": axes() + [R(4, 4, 8, 8, "p", 0), R(12, 4, 8, 16, "a", 0), L([(12, 4), (12, 20)]), L([(4, 12), (20, 12)])] + dots([(8, 8), (16, 16)], INK),
        "gc_harker_variation_diagram": chart([(4, 5), (20, 19)], dots([(6, 8), (10, 9), (14, 15), (18, 16)], INK)),
        "gc_water_solubility_melt": chart([(4, 19), (7, 13), (11, 9), (15, 6), (20, 4)], [drop(17, 15, 4, "p")]),
        "gc_oxygen_isotope_delta18o": chart([(4, 19), (20, 4)], [A(11, 12, 19, 12), C(11, 12, 1.2, INK, True)]),
        "gc_hydrothermal_boiling_immiscibility": [drop(7, 15, 5, "a"), drop(18, 8, 4, "p"), A(14, 14, 20, 20)] + dots([(4, 4), (10, 3)], INK, 1.1),
        "gc_sulfide_melt_immiscibility": [R(3, 3, 18, 18, "p")] + [drop(8, 10, 3, "a"), drop(16, 16, 4, INK)],
        "gc_fluid_rock_metasomatism": [P([(13, 3), (21, 3), (21, 21), (13, 21), (16, 16), (11, 12), (16, 7)], "p"), A(3, 7, 11, 7, "a"), A(3, 17, 11, 17, "a")],
        "gc_bacterial_sulfate_reduction": [R(3, 7, 8, 10, "a", 4), A(12, 12, 16, 12), C(19, 12, 3, "p")] + dots([(18, 11), (20, 13)], INK, .7),
        "gc_heavy_mineral_placer": [P([(3, 8), (8, 8), (11, 15), (15, 15), (18, 8), (21, 8), (21, 21), (3, 21)], "p"), L([(3, 8), (8, 8), (11, 15), (15, 15), (18, 8), (21, 8)], BLUE)] + dots([(12, 18), (15, 18)], "a", 1.2),
        "gc_gossan_boxwork_weathering": lattice() + [L([(3, 3), (21, 21)], "a"), L([(3, 21), (21, 3)], "a")],
        "gc_fumarolic_gas_exsolution": [P([(3, 21), (9, 12), (15, 12), (21, 21)], "p"), L([(9, 9), (7, 6), (9, 3)], "a"), L([(15, 9), (17, 6), (15, 3)], "a")],
        "gc_clay_adsorption_cec": [R(3, 4, 18, 4, INK), R(3, 16, 18, 4, "a")] + dots([(7, 12), (12, 12), (17, 12)], "a", 1.4),
        "gc_metal_chloride_complexation": [C(12, 12, 3, "a")] + [L([(12, 12), point], INK) for point in [(12, 3), (21, 12), (12, 21), (3, 12)]] + dots([(12, 3), (21, 12), (12, 21), (3, 12)], "a", 1.7),
        "gc_hydrocarbon_catagenesis": [A(5, 19, 5, 5), A(12, 19, 12, 5), A(19, 19, 19, 5)] + dots([(5, 21), (12, 21), (19, 21)], "a", 1),
        "gc_colloid_flocculation": dots([(4, 5), (7, 9), (3, 14), (8, 18)], "a", 1) + [A(10, 12, 14, 12)] + dots([(18, 10), (21, 12), (18, 15)], INK, 1.7),
        "gc_gibbs_free_energy": chart([(4, 5), (7, 13), (10, 18), (13, 19), (16, 16), (20, 7)], [C(13, 16, 1.5, INK, True)]),
        "gc_chemical_elements": atom(),
        "gl_minerals_specimen": crystal(7, 15, .65, "p") + crystal(16, 12, 1, "a"),
        "gc_element_diff_wtpct": [R(3, 3, 18, 18, "p"), L([(8, 17), (16, 7)], "a", 2), C(8, 7, 1.7, INK), C(16, 17, 1.7, INK)],
        "gc_temperature_thermo": thermometer() + [L([(18, 6), (21, 6)]), L([(18, 10), (20, 10)])],
        "gc_pressure_gauge": [C(12, 12, 9, "p"), arc(12, 12, 6, 200, 340, "a"), A(12, 12, 17, 7), C(12, 12, 1.4, INK, True)],
        "gc_gradient_perturbation_factor": chart([(4, 18), (20, 6)], [A(12, 12, 12, 6), L([(9, 6), (15, 6)], "a")]),
        "gc_l1_norm_regularization": [P([(12, 3), (21, 12), (12, 21), (3, 12)], "p"), L([(12, 3), (12, 21)]), L([(3, 12), (21, 12)], "a")],
        "gc_n_iterations_loop": cycle() + [L([(9, 16), (9, 9), (13, 8), (15, 10), (15, 16)], "a")],
        "gc_thermodynamics_system": [R(5, 5, 14, 14, "p"), drop(12, 12, 5, RED), A(12, 2, 12, 5), A(12, 22, 12, 19), L([(2, 12), (5, 12)]), L([(19, 12), (22, 12)])],
        "gp_petrophysics_core_matrix": [R(5, 5, 14, 16, "p", 3), E(12, 5, 7, 3, "a")] + dots([(9, 11), (15, 14), (10, 18)], BLUE, 1.3),
        "gl_positions_spatial_coords": [A(4, 20, 4, 3), A(4, 20, 21, 20), A(4, 20, 17, 7), C(14, 11, 2, "a")],
        "gc_volatiles_degassing": [P([(3, 14), (8, 16), (15, 13), (21, 15), (21, 21), (3, 21)], "p")] + dots([(7, 10), (16, 7), (12, 3)], "a", 1.6),
        "gc_water_activity_ah2o": [drop(), L([(8, 16), (10, 18), (16, 12)], WHITE, 1.5)],
        "gc_fluid_xco2_mole_fraction": [C(12, 12, 9, "p"), P([(12, 12), (12, 3), (18.4, 5.6), (21, 12)], "a"), L([(6, 15), (18, 15)]), C(12, 15, 2, INK)],
        "gc_oxygen_fugacity_fo2": [L([(4, 7), (20, 7)]), L([(12, 3), (12, 21)]), C(5, 13, 3, "p"), C(19, 13, 3, "a"), L([(5, 7), (5, 11)]), L([(19, 7), (19, 11)]), L([(8, 21), (16, 21)])],
        "gc_major_element_oxides": [P([(12, 3), (21, 16), (4, 18)], "p"), L([(12, 3), (12, 12), (21, 16)]), L([(12, 12), (4, 18)])] + dots([(12, 3), (21, 16), (4, 18), (12, 12)], "a", 1.6),
        "gc_gradient_initial_step": chart([(4, 4), (7, 12), (11, 17), (16, 19), (21, 20)], [A(7, 5, 10, 13), C(4, 4, 1.3, INK, True)]),
        "gc_sensitivity_jacobian": [L([(6, 3), (3, 3), (3, 21), (6, 21)]), L([(18, 3), (21, 3), (21, 21), (18, 21)])] + [R(x, y, 3, 3, "a" if (x + y) % 2 else INK, .5) for x, y in [(7, 5), (14, 5), (7, 11), (14, 11), (7, 17), (14, 17)]],
        "gp_specific_gravity_balance": [L([(12, 3), (12, 21)]), L([(4, 6), (20, 6)]), L([(8, 21), (16, 21)]), R(3, 13, 6, 7, "p"), R(17, 10, 4, 5, "a"), L([(6, 6), (6, 16)]), L([(19, 6), (19, 10)]), wave(17, BLUE, .5, 1, 3, 9)],
        "gc_log_error_residuals": chart([(4, 4), (6, 11), (9, 16), (13, 18), (20, 19)], dots([(7, 9), (12, 17), (18, 18)], INK)),
        "gl_geological_tagging_domain": [P([(8, 3), (16, 3), (21, 8), (21, 21), (3, 21), (3, 8)], "p"), C(12, 7, 1, INK, True), R(6, 11, 12, 3, "a"), R(6, 16, 12, 3, INK)],
    }


PALETTES = {
    "Geophysical": (BLUE, "#DDEAFF"),
    "Geotechnical": ("#D79A36", "#F6E9CE"),
    "Geological": (TEAL, "#D5EEE7"),
    "Geochemical": (PURPLE, "#EAE1F6"),
}


def artwork(icon):
    layers = build_recipes()[icon["id"]]
    accent, pale = PALETTES[icon["domain"]]
    for layer in layers:
        layer.color = {"a": accent, "p": pale}.get(layer.color, layer.color)
    return layers


def font_geometry(layers):
    geometry = Polygon()
    for layer in layers:
        if layer.knockout is not None:
            geometry = geometry.difference(layer.knockout)
        geometry = geometry.union(layer.glyph)
    # Match the existing 1000-unit Y-up font canvas and its baseline metrics.
    geometry = affinity.scale(geometry, xfact=1000 / 24, yfact=-1000 / 24, origin=(0, 0))
    return affinity.translate(geometry, yoff=1000)


def svg_document(icon, layers, path_converter):
    from geom_utils import clean_for_ttf
    paths = []
    for layer in layers:
        geometry = affinity.scale(layer.surface, xfact=1000 / 24, yfact=-1000 / 24, origin=(0, 0))
        geometry = affinity.translate(geometry, yoff=1000)
        data = path_converter(clean_for_ttf(geometry, simplify_tol=.2))
        paths.append(f'  <path fill="{layer.color}" d="{data}"/>')
    title = escape(icon["name"])
    description = escape(icon["description"])
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-labelledby="title desc">\n  <title id="title">{title}</title>\n  <desc id="desc">{description}</desc>\n' + "\n".join(paths) + "\n</svg>\n"
