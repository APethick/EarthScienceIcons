"""Field Geologists' Manual map patterns: tectonic igneous, metamorphic and surface units.

Covers FGM 19.4-19.6 tectonic map symbols for orogenic granites, felsic volcanics
and cratonic igneous rocks, plus FGM black-and-white geological map patterns for
metamorphic rocks, volcanic/plutonic textures and regolith cover.
"""
import math
from shapely.geometry import LineString, Point, Polygon, box

from fgm_common import (
    ALLUVIUM, BASALT, BASALT_MAP, CONGLOMERATE, DOLERITE_MAP, FELDSPAR,
    FieldDrawing, GNEISS, GOSSAN, GRANITE, GRANITE_LIGHT, HORNFELS, INK,
    OLIVINE, PAPER, PLAGIOCLASE, PYROXENE, QUARTZ, ROCK, SAND, SANDSTONE,
    SCHIST, SHALE, SLATE, SOIL, SOIL_DARK, TUFF, VOLCANIC, WHITE,
    grid_points, irregular_polygon, rng, scatter, smooth, swatch,
)

# High-contrast pigment tones for coloured map patterns drawn on white paper.
PURPLE_INK = '#6A4C93'
RED_INK = '#B84A3E'
ORANGE_INK = '#C86D22'
GREEN_INK = '#467A44'


def _cross(d, x, y, arm=1.85, colour=WHITE, width=.8, angle=0):
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    d.line([(x - arm * ca, y - arm * sa), (x + arm * ca, y + arm * sa)], colour, width)
    d.line([(x + arm * sa, y - arm * ca), (x - arm * sa, y + arm * ca)], colour, width)


def _v_tick(d, x, y, size=1.85, angle=0, colour=PURPLE_INK, width=.78):
    """Open V/chevron tick centred near (x, y); angle=0 points up (^)."""
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    pts = [(-size * .88, size * .55), (0, -size * .65), (size * .88, size * .55)]
    rot = [(x + u * ca - v * sa, y + u * sa + v * ca) for u, v in pts]
    d.line(rot, colour, width)


def _rounded_inner(x=4, y=8, width=40, height=32, radius=1.2, inset=.35):
    """Clip region matching the rounded swatch corners without protruding at vertices."""
    return box(x + radius, y + radius, x + width - radius, y + height - radius).buffer(radius - inset, quad_segs=6)


def _star4(d, x, y, arm=3.0, core=1.12, colour=INK, angle=16):
    """Four-pointed star with crisp ray tips and prominent diamond core."""
    _cross(d, x, y, arm=arm, colour=colour, width=.68, angle=angle)
    a = math.radians(angle)
    pts = []
    for i in range(8):
        r = arm * .92 if i % 2 == 0 else core
        t = a + i * math.pi / 4
        pts.append((x + r * math.cos(t), y + r * math.sin(t)))
    d.solid(Polygon(pts), colour)


def build_granite_post_kinematic():
    """FGM 19.4.1: Regular dense orthogonal grid of white crosses on red ground."""
    d = FieldDrawing()
    region = swatch(d, GRANITE)
    with d.clipped(region):
        for r in range(4):
            y = 12.5 + r * 7.6
            for c in range(5):
                x = 8.8 + c * 7.6
                _cross(d, x, y, arm=1.95, colour=WHITE, width=.82)
    return d


def build_granite_late_post_kinematic():
    """FGM 19.4.2: Sparse staggered white crosses on red ground."""
    d = FieldDrawing()
    region = swatch(d, GRANITE)
    with d.clipped(region):
        coords = [
            (11.5, 13.5), (24.0, 13.5), (36.5, 13.5),
            (17.8, 24.0), (30.2, 24.0),
            (11.5, 34.5), (24.0, 34.5), (36.5, 34.5),
        ]
        for x, y in coords:
            _cross(d, x, y, arm=2.15, colour=WHITE, width=.85)
    return d


def build_granite_syn_late_kinematic():
    """FGM 19.4.3: Staggered small white crosses alternating with dots on red ground."""
    d = FieldDrawing()
    region = swatch(d, GRANITE)
    with d.clipped(region):
        for r in range(4):
            y = 12.4 + r * 7.7
            for c in range(5):
                x = 8.4 + c * 7.4 + (1.8 if r % 2 else -1.0)
                if x < 7.0 or x > 41.0:
                    continue
                if (r + c) % 2 == 0:
                    _cross(d, x, y, arm=1.48, colour=WHITE, width=.76)
                else:
                    d.circle(x, y, .74, WHITE, WHITE, True)
    return d


def build_granite_syn_kinematic_foliated():
    """FGM 19.4.4: Bold white sigmoidal S-shaped foliation marks on red ground."""
    d = FieldDrawing()
    region = swatch(d, GRANITE)
    with d.clipped(region):
        centres = [(15.2, 17.5), (31.8, 17.5), (16.2, 30.8), (32.8, 30.8)]
        for cx, cy in centres:
            # S-curve spine with spindle-tapered thickness (thick centre, pointed tips)
            spine = smooth([
                (cx - 6.0, cy + 3.4),
                (cx - 2.6, cy + 3.1),
                (cx, cy),
                (cx + 2.6, cy - 3.1),
                (cx + 6.0, cy - 3.4),
            ], 3)
            left_side, right_side = [], []
            n = len(spine)
            for i, (px, py) in enumerate(spine):
                t = i / (n - 1)
                half_w = 1.05 * math.sin(math.pi * t) ** 0.85
                p_prev = spine[max(0, i - 1)]
                p_next = spine[min(n - 1, i + 1)]
                dx, dy = p_next[0] - p_prev[0], p_next[1] - p_prev[1]
                length = math.hypot(dx, dy) or 1.0
                nx, ny = -dy / length, dx / length
                left_side.append((px + nx * half_w, py + ny * half_w))
                right_side.append((px - nx * half_w, py - ny * half_w))
            d.solid(Polygon(left_side + right_side[::-1]), WHITE)
    return d


def build_granite_gneissic_anatectic():
    """FGM 19.4.5: Four-pointed black stars on red granite ground."""
    d = FieldDrawing()
    region = swatch(d, GRANITE)
    with d.clipped(region):
        stars = [
            (12.0, 14.8, 14), (25.0, 14.0, 20), (36.5, 16.2, 12),
            (16.0, 25.5, 18), (30.0, 25.0, 15),
            (11.2, 34.8, 12), (23.8, 34.5, 18), (36.0, 34.0, 15),
        ]
        for x, y, ang in stars:
            _star4(d, x, y, arm=3.05, core=1.12, colour=INK, angle=ang)
    return d


def build_gabbro_diorite_orogenic():
    """FGM 19.4.6: Staggered diagonal white x-marks on red ground."""
    d = FieldDrawing()
    region = swatch(d, GRANITE)
    with d.clipped(region):
        for r in range(4):
            y = 12.5 + r * 7.6
            shift = 3.8 if r % 2 else 0.0
            for c in range(5):
                x = 8.8 + c * 7.6 + shift
                if x > 40.5:
                    continue
                _cross(d, x, y, arm=1.65, colour=WHITE, width=.78, angle=45)
    return d


def build_porphyry_pattern():
    """FGM 19.4.7: Random short white phenocryst dashes on red ground."""
    d = FieldDrawing()
    region = swatch(d, GRANITE)
    r = rng(1947)
    with d.clipped(region):
        for r_idx in range(4):
            for c_idx in range(6):
                x = 8.2 + c_idx * 6.2 + r.uniform(-1.0, 1.0)
                y = 12.0 + r_idx * 7.8 + r.uniform(-1.0, 1.0)
                ang = math.radians(r.choice([0, 28, 55, 85, 118, 148]))
                half = 1.75
                dx, dy = half * math.cos(ang), half * math.sin(ang)
                d.line([(x - dx, y - dy), (x + dx, y + dy)], WHITE, .8)
    return d


def build_island_arc_volcanics():
    """FGM 19.5.1: Dense nested rows of upward purple chevrons on white ground."""
    d = FieldDrawing()
    region = swatch(d, PAPER)
    with d.clipped(region):
        for r in range(5):
            y = 12.0 + r * 6.0
            shift = 3.0 if r % 2 else 0.0
            x = 7.4 + shift
            while x <= 41.0:
                _v_tick(d, x, y, size=2.2, angle=0, colour=PURPLE_INK, width=.8)
                x += 6.0
    return d


def build_felsic_volcanics_rare_basics():
    """FGM 19.5.2: Alternating rows of ^ < and < v red angle marks on white ground."""
    d = FieldDrawing()
    region = swatch(d, PAPER)
    with d.clipped(region):
        for r in range(4):
            y = 12.4 + r * 7.6
            for c in range(5):
                x = 8.8 + c * 7.6
                if r % 2 == 0:
                    ang = 0 if c % 2 == 0 else -90
                else:
                    ang = -90 if c % 2 == 0 else 180
                _v_tick(d, x, y, size=1.95, angle=ang, colour=RED_INK, width=.8)
    return d


def build_rhyolite_dacite_volcanics():
    """FGM 19.5.3: Sparse variously oriented purple V-ticks on white ground."""
    d = FieldDrawing()
    region = swatch(d, PAPER)
    ticks = [
        (10.5, 13.5, -55), (21.5, 13.0, 180), (34.5, 13.2, -90),
        (15.5, 20.2, 65),  (27.0, 19.8, -35), (37.5, 21.2, 55),
        (9.8, 26.8, -90),  (21.0, 27.5, 140), (31.5, 27.2, 0),
        (13.5, 34.5, 45),  (24.5, 34.8, 0),   (35.8, 34.2, -80),
    ]
    with d.clipped(region):
        for x, y, ang in ticks:
            _v_tick(d, x, y, size=2.1, angle=ang, colour=PURPLE_INK, width=.82)
    return d


def build_felsic_volcanics_with_granite():
    """FGM 19.5.4: Dense rotated purple V-ticks interspersed with dots on white ground."""
    d = FieldDrawing()
    region = swatch(d, PAPER)
    r = rng(1954)
    angles = [0, 50, 105, 155, 210, 265, 315]
    with d.clipped(region):
        idx = 0
        for r_idx in range(4):
            y = 12.2 + r_idx * 7.7
            for c_idx in range(6):
                x = 7.8 + c_idx * 6.4 + (1.4 if r_idx % 2 else 0.0)
                if x > 41.0:
                    continue
                jx = x + r.uniform(-.4, .4)
                jy = y + r.uniform(-.4, .4)
                if (r_idx + c_idx) % 2 == 0:
                    ang = angles[idx % len(angles)]
                    idx += 1
                    _v_tick(d, jx, jy, size=1.75, angle=ang, colour=PURPLE_INK, width=.76)
                else:
                    d.circle(jx, jy, .72, PURPLE_INK, PURPLE_INK, True)
    return d


def build_flood_basalt():
    """FGM 19.6.1: Staggered right-pointing orange chevrons and dots on white ground."""
    d = FieldDrawing()
    region = swatch(d, PAPER)
    with d.clipped(region):
        for r in range(4):
            y = 12.2 + r * 7.8
            for c in range(5):
                x = 8.6 + c * 7.6 + (1.8 if r % 2 else 0)
                if x > 41.2:
                    continue
                if (r + c) % 2 == 0:
                    _v_tick(d, x, y, size=1.85, angle=90, colour=ORANGE_INK, width=.8)
                else:
                    d.circle(x, y, .74, ORANGE_INK, ORANGE_INK, True)
    return d


def build_dolerite_granophyre():
    """FGM 19.6.2: Scattered green double-bar (= and //) marks on white ground."""
    d = FieldDrawing()
    region = swatch(d, PAPER)
    # Parallel bars separated by 2.16 units centre-to-centre so mono closing keeps them distinct
    pairs = [
        (10.5, 13.5, -35), (23.5, 13.2, 12),  (36.0, 13.8, -55),
        (16.5, 20.8, 35),  (29.5, 20.2, -15), (39.0, 21.5, 75),
        (10.2, 27.8, -50), (22.5, 27.5, 40),  (34.5, 27.8, -25),
        (15.0, 34.8, -18), (27.5, 34.8, 18),  (38.5, 34.5, -45),
    ]
    with d.clipped(region):
        for x, y, deg in pairs:
            a = math.radians(deg)
            ux, uy = math.cos(a) * 1.75, math.sin(a) * 1.75
            nx, ny = -math.sin(a) * 1.08, math.cos(a) * 1.08
            d.line([(x - ux + nx, y - uy + ny), (x + ux + nx, y + uy + ny)], GREEN_INK, .7)
            d.line([(x - ux - nx, y - uy - ny), (x + ux - nx, y + uy - ny)], GREEN_INK, .7)
    return d


def build_keratophyre():
    """FGM 19.6.3: Grid of rotated purple T-bar ticks with corner barbs on white ground."""
    d = FieldDrawing()
    region = swatch(d, PAPER)
    angles = [
        -15, 165, -105, 75,
        155, -25, 85, -95,
        -10, 170, -100, 80,
    ]
    with d.clipped(region):
        idx = 0
        for r in range(3):
            y = 13.8 + r * 10.2
            for c in range(4):
                x = 10.2 + c * 9.2
                a = math.radians(angles[idx])
                idx += 1
                ca, sa = math.cos(a), math.sin(a)
                p0 = (x - 2.1 * ca, y - 2.1 * sa)
                p1 = (x + 2.1 * ca, y + 2.1 * sa)
                p2 = (x - 2.4 * sa, y + 2.4 * ca)
                d.line([p0, p1], PURPLE_INK, .8)
                d.line([(x, y), p2], PURPLE_INK, .8)
                barb = Polygon([
                    (x, y),
                    (x + 1.55 * ca, y + 1.55 * sa),
                    (x - 1.55 * sa, y + 1.55 * ca),
                ])
                d.solid(barb, PURPLE_INK)
    return d


def build_granite_intruding_craton():
    """FGM 19.6.5: Red crosses surrounded by stipple dot trails on white ground."""
    d = FieldDrawing()
    region = swatch(d, PAPER)
    crosses = [
        (13.5, 13.5), (34.5, 13.5),
        (24.0, 20.0), (14.5, 26.5), (32.5, 26.5),
        (10.5, 34.0), (23.0, 34.5), (36.5, 34.5),
    ]
    dots = [
        (8.5, 12.5), (19.5, 12.5), (28.5, 13.0), (39.5, 16.5),
        (9.2, 18.8), (18.8, 17.5), (29.2, 18.8), (36.5, 20.5),
        (8.8, 25.0), (20.5, 25.2), (26.8, 25.2), (38.2, 25.5),
        (14.8, 31.8), (19.0, 30.2), (28.0, 31.0), (39.2, 30.5),
        (16.8, 35.5), (29.8, 35.2),
    ]
    with d.clipped(region):
        for x, y in crosses:
            _cross(d, x, y, arm=1.85, colour=RED_INK, width=.8)
        for x, y in dots:
            d.circle(x, y, .68, RED_INK, RED_INK, True)
    return d


def build_layered_intrusion():
    """FGM 19.6.6: Rhythmic gabbro-peridotite cumulate layering with settled olivine and laths."""
    d = FieldDrawing()
    swatch(d, PLAGIOCLASE)
    inner = _rounded_inner()
    with d.clipped(inner):
        bands = [
            (8.0, 16.0, PLAGIOCLASE),
            (16.0, 24.0, OLIVINE),
            (24.0, 32.0, PLAGIOCLASE),
            (32.0, 40.0, PYROXENE),
        ]
        for y0, y1, fill in bands:
            d.poly([(4, y0), (44, y0), (44, y1), (4, y1)], fill, INK)
        # Igneous lamination (tabular plagioclase lath lines) in leucogabbro layers
        for y0 in (8.0, 24.0):
            for x in (9.5, 19.0, 28.5, 38.0):
                d.line([(x - 2.3, y0 + 2.7), (x + 2.3, y0 + 2.7)], INK, .78)
            for x in (14.2, 23.8, 33.2):
                d.line([(x - 2.3, y0 + 5.3), (x + 2.3, y0 + 5.3)], INK, .78)
        # Settled equant cumulate olivine/pyroxene grains in ultramafic layers
        for y0, col in ((16.0, PYROXENE), (32.0, OLIVINE)):
            yc = y0 + 4.0
            for idx, x in enumerate((8.8, 14.9, 21.0, 27.1, 33.2, 39.3)):
                if idx % 2 == 0:
                    d.circle(x, yc, 1.5, col, INK)
                else:
                    d.circle(x, yc, .85, INK, INK, True)
    d.rect(4, 8, 40, 32, None, 1.2)
    return d


def build_alkaline_intrusive():
    """FGM 19.6.7: Euhedral nepheline hexagons and acicular aegirine needles on purple ground."""
    d = FieldDrawing()
    region = swatch(d, VOLCANIC)
    hex_centres = [
        (12.2, 15.2, 3.8, 10), (26.5, 14.5, 3.6, -12), (37.8, 17.5, 3.3, 20),
        (19.0, 26.2, 3.9, -8), (32.2, 28.2, 3.6, 15),
        (10.5, 33.8, 3.3, 25), (24.2, 35.2, 3.2, 5),
    ]
    needles = [
        (19.5, 15.8, 40), (10.0, 24.0, -35), (26.0, 21.2, 65),
        (38.5, 26.0, -55), (16.8, 34.8, 25), (37.2, 35.2, -25),
    ]
    with d.clipped(region):
        for cx, cy, rad, rot in hex_centres:
            a0 = math.radians(rot)
            outer = [(cx + rad * math.cos(a0 + i * math.tau / 6),
                      cy + rad * math.sin(a0 + i * math.tau / 6)) for i in range(6)]
            d.poly(outer, PLAGIOCLASE, INK)
            d.circle(cx, cy, .78, INK, INK, True)
        for x, y, deg in needles:
            a = math.radians(deg)
            dx, dy = 2.0 * math.cos(a), 2.0 * math.sin(a)
            d.line([(x - dx, y - dy), (x + dx, y + dy)], INK, .82)
    return d


def build_kimberlite_lamproite():
    """FGM 19.6.8: Carrot-shaped purple diatreme pipe cutting wall rock with breccia xenoliths."""
    d = FieldDrawing()
    swatch(d, SANDSTONE)
    inner = _rounded_inner()
    with d.clipped(inner):
        # Horizontal country-rock bedding cut by pipe
        for y, fill in ((8, SANDSTONE), (16, SHALE), (24, SANDSTONE), (32, SHALE)):
            d.poly([(4, y), (44, y), (44, y + 8), (4, y + 8)], fill, INK)
        # Downward-tapering carrot-shaped diatreme pipe
        pipe = [
            (9.5, 8.0), (38.5, 8.0),
            (34.0, 18.5), (30.5, 29.5), (27.8, 40.0),
            (20.2, 40.0), (17.5, 29.5), (14.0, 18.5),
        ]
        d.poly(pipe, VOLCANIC, INK)
        # Euhedral diamond octahedron near the top of the diatreme
        cx, cy, r = 24.0, 14.5, 3.1
        d.poly([(cx, cy - r), (cx + r * .82, cy), (cx, cy + r), (cx - r * .82, cy)], WHITE, INK)
        # Well-spaced mantle nodules and angular xenoliths inside the pipe
        clasts = [
            (16.2, 13.2, 2.0, 5, OLIVINE),
            (31.8, 13.2, 2.0, 4, PLAGIOCLASE),
            (20.2, 23.2, 2.1, 5, OLIVINE),
            (28.0, 24.5, 2.0, 4, SANDSTONE),
            (24.0, 33.0, 2.2, 5, OLIVINE),
        ]
        for idx, (x, y, rad, sides, col) in enumerate(clasts):
            d.poly(irregular_polygon(1968 + idx, x, y, rad, sides=sides, jitter=.25), col, INK)
        for x, y in ((18.5, 18.2), (29.2, 18.5), (24.2, 27.8), (22.5, 37.5)):
            d.circle(x, y, .65, INK, INK, True)
    d.rect(4, 8, 40, 32, None, 1.2)
    return d


def build_carbonatite():
    """FGM 19.6.9: Staggered solid black diamond symbols on purple carbonatite ground."""
    d = FieldDrawing()
    region = swatch(d, VOLCANIC)
    with d.clipped(region):
        for r in range(3):
            y = 14.0 + r * 10.0
            for c in range(4):
                x = 10.0 + c * 9.2 + (2.3 if r % 2 else -1.2)
                if x > 40.5 or x < 7.5:
                    continue
                rx, ry = 1.95, 3.05
                diamond = Polygon([(x, y - ry), (x + rx, y), (x, y + ry), (x - rx, y)])
                d.solid(diamond, INK)
    return d


def build_slate_phyllite():
    """FGM metamorphic pattern: Close fine parallel horizontal cleavage lines on slate ground."""
    d = FieldDrawing()
    region = swatch(d, SLATE)
    with d.clipped(region):
        for group_y in (11.2, 21.4, 31.6):
            d.line([(5.8, group_y), (42.2, group_y)], INK, .92)
            d.line([(5.8, group_y + 2.6), (42.2, group_y + 2.6)], INK, .78)
            d.line([(5.8, group_y + 5.2), (42.2, group_y + 5.2)], INK, .78)
    return d


def build_schist_gneiss_high_grade():
    """FGM metamorphic pattern: Staggered wavy crenulated foliation dashes on schist ground."""
    d = FieldDrawing()
    region = swatch(d, SCHIST)
    with d.clipped(region):
        for r in range(5):
            y = 11.5 + r * 6.2
            shift = 4.6 if r % 2 else 0.0
            for c in range(4):
                x0 = 6.5 + c * 9.5 + shift
                if x0 + 5.8 > 42.8:
                    continue
                pts = [(x0 + i * 6.0 / 24, y + 1.0 * math.sin(i / 24 * math.tau * 2.0))
                       for i in range(25)]
                d.line(pts, INK, .78)
    return d


def build_sandy_slate_interbedded():
    """FGM metamorphic pattern: Parallel cleavage lines alternating with dotted sandy beds."""
    d = FieldDrawing()
    swatch(d, SLATE)
    inner = _rounded_inner()
    with d.clipped(inner):
        # Two well-proportioned sandy interbeds with central dot rows
        for y0 in (12.2, 26.2):
            d.poly([(4, y0), (44, y0), (44, y0 + 6.6), (4, y0 + 6.6)], SANDSTONE, INK)
            for x in (8.5, 14.0, 19.5, 25.0, 30.5, 36.0, 40.5):
                d.circle(x, y0 + 3.3, .7, INK, INK, True)
        # Cleavage lines in the alternating slate beds
        for y in (10.1, 21.3, 23.7, 35.2, 37.6):
            d.line([(5.8, y), (42.2, y)], INK, .78)
    d.rect(4, 8, 40, 32, None, 1.2)
    return d


def build_hornfels_massive():
    """FGM metamorphic pattern: Staggered solid black squares on massive hornfels ground."""
    d = FieldDrawing()
    region = swatch(d, HORNFELS)
    with d.clipped(region):
        for r in range(4):
            y = 12.2 + r * 7.6
            shift = 3.8 if r % 2 else 0.0
            for c in range(5):
                x = 8.6 + c * 7.6 + shift
                if x > 40.2:
                    continue
                s = 1.5
                d.solid(box(x - s, y - s, x + s, y + s), INK)
    return d


def build_basic_plutonic_hypabyssal():
    """FGM igneous pattern: Dense ophitic triplet-dash clusters on basic rock ground."""
    d = FieldDrawing()
    region = swatch(d, '#8D9B91')
    # 3x3 + 2 staggered clusters with 2.05-unit line spacing so triplets never fuse in mono
    clusters = [
        (10.5, 13.5, -35), (24.0, 13.2, 40), (37.0, 13.8, -55),
        (17.0, 23.8, 60),  (30.8, 23.8, -25),
        (10.5, 34.0, 22),  (24.0, 34.2, -60), (37.0, 33.8, 35),
    ]
    with d.clipped(region):
        for x, y, deg in clusters:
            a = math.radians(deg)
            ux, uy = math.cos(a) * 2.1, math.sin(a) * 2.1
            nx, ny = -math.sin(a) * 2.05, math.cos(a) * 2.05
            for k in (-1, 0, 1):
                L = 1.0 if k == 0 else .82
                d.line([(x - ux * L + nx * k, y - uy * L + ny * k),
                        (x + ux * L + nx * k, y + uy * L + ny * k)], INK, .68)
    return d


def build_bedded_lavas():
    """FGM igneous pattern: Sub-parallel wavy lava flow lines with directional arrow barbs."""
    d = FieldDrawing()
    region = swatch(d, '#C7967B')
    with d.clipped(region):
        for r in range(4):
            y = 12.2 + r * 7.8
            pts = [(5.0 + i * 38.0 / 40, y + .65 * math.sin(i / 40 * math.tau * 2.5 + r))
                   for i in range(41)]
            d.line(pts, INK, .76)
            barb_xs = [12.5, 25.0, 36.5] if r % 2 == 0 else [18.5, 31.0]
            for bx in barb_xs:
                by = y + .65 * math.sin((bx - 5.0) / 38.0 * math.tau * 2.5 + r)
                barb = Polygon([
                    (bx + 1.8, by),
                    (bx - 1.5, by - 1.65),
                    (bx - .6, by),
                    (bx - 1.5, by + 1.65),
                ])
                d.solid(barb, INK)
    return d


def build_tuff_tuffaceous_sandstone():
    """FGM miscellaneous pattern: Random shard dashes and stipple dots on tuff ground."""
    d = FieldDrawing()
    region = swatch(d, TUFF)
    r = rng(2601)
    angles = [12, 48, 82, 128, 162]
    with d.clipped(region):
        idx = 0
        for r_idx in range(4):
            y = 12.2 + r_idx * 7.7
            for c_idx in range(6):
                x = 7.8 + c_idx * 6.4 + (1.4 if r_idx % 2 else 0.0)
                if x > 41.0:
                    continue
                jx = x + r.uniform(-.45, .45)
                jy = y + r.uniform(-.45, .45)
                if (r_idx + c_idx) % 2 == 0:
                    ang = math.radians(angles[idx % len(angles)])
                    idx += 1
                    dx, dy = 1.75 * math.cos(ang), 1.75 * math.sin(ang)
                    d.line([(jx - dx, jy - dy), (jx + dx, jy + dy)], INK, .78)
                else:
                    d.circle(jx, jy, .72, INK, INK, True)
    return d


def build_bedded_tuff():
    """FGM miscellaneous pattern: Horizontal bedding lines punctuated by downward V-ticks."""
    d = FieldDrawing()
    region = swatch(d, TUFF)
    with d.clipped(region):
        for r in range(4):
            y = 12.0 + r * 7.8
            v_xs = [12.5, 24.0, 35.5] if r % 2 == 0 else [18.2, 29.8]
            pts = [(5.8, y)]
            for vx in v_xs:
                pts.extend([(vx - 2.1, y), (vx, y + 2.6), (vx + 2.1, y)])
            pts.append((42.2, y))
            d.line(pts, INK, .88)
    return d


def build_breccia_pattern():
    """FGM miscellaneous pattern: Angular solid black triangle clasts on clean ground."""
    d = FieldDrawing()
    region = swatch(d, CONGLOMERATE)
    tris = [
        (10.0, 13.0, 2.5, 15),  (20.0, 12.5, 2.3, 75),  (30.5, 13.2, 2.5, 140), (39.0, 13.5, 2.2, 35),
        (14.5, 20.2, 2.4, 110), (25.0, 20.5, 2.6, 20),  (35.0, 20.0, 2.3, 85),
        (9.5, 27.8, 2.3, 55),   (19.5, 27.5, 2.5, 160), (30.0, 28.0, 2.4, 40),  (39.2, 27.5, 2.3, 125),
        (14.0, 35.0, 2.5, 25),  (24.8, 34.8, 2.3, 95),  (35.2, 35.0, 2.5, 170),
    ]
    with d.clipped(region):
        for x, y, rad, deg in tris:
            a = math.radians(deg)
            pts = [
                (x + rad * math.cos(a), y + rad * math.sin(a)),
                (x + rad * .95 * math.cos(a + 2.2), y + rad * .95 * math.sin(a + 2.2)),
                (x + rad * .85 * math.cos(a + 4.3), y + rad * .85 * math.sin(a + 4.3)),
            ]
            d.solid(Polygon(pts), INK)
    return d


def build_scree_brecciated_rock():
    """FGM miscellaneous pattern: Angular triangles mixed with dense stipple dots."""
    d = FieldDrawing()
    region = swatch(d, SAND)
    tris = [
        (11.5, 14.0, 2.7, 20, True),   (24.5, 13.5, 2.8, 85, False), (36.5, 14.5, 2.6, 145, True),
        (17.5, 24.0, 2.8, 130, False), (30.5, 23.8, 2.7, 35, True),
        (11.0, 33.8, 2.7, 65, False),  (23.5, 34.2, 2.7, 15, True),  (36.0, 33.5, 2.8, 110, False),
    ]
    with d.clipped(region):
        tri_polys = []
        for x, y, rad, deg, is_solid in tris:
            a = math.radians(deg)
            pts = [
                (x + rad * math.cos(a), y + rad * math.sin(a)),
                (x + rad * .95 * math.cos(a + 2.15), y + rad * .95 * math.sin(a + 2.15)),
                (x + rad * .88 * math.cos(a + 4.25), y + rad * .88 * math.sin(a + 4.25)),
            ]
            poly = Polygon(pts)
            tri_polys.append(poly)
            if is_solid:
                d.solid(poly, INK)
            else:
                d.poly(pts, PAPER, INK)
        for x, y in scatter(2902, 32, region, spacing=4.2, margin=1.8):
            pt = Point(x, y)
            if all(pt.distance(poly) > 2.3 for poly in tri_polys):
                d.circle(x, y, .68, INK, INK, True)
    return d


def build_soil_cover():
    """FGM miscellaneous pattern: Sparse stipple dots and small open granules on soil ground."""
    d = FieldDrawing()
    region = swatch(d, SOIL)
    circles = [
        (11.5, 13.5), (23.8, 13.2), (35.8, 13.8),
        (17.5, 23.8), (30.2, 23.5),
        (11.2, 34.0), (23.5, 34.2), (35.5, 33.5),
    ]
    dots = [
        (17.6, 13.5), (30.0, 13.5),
        (8.8, 18.8), (23.8, 18.8), (38.2, 19.2),
        (11.2, 24.2), (23.8, 24.2), (36.2, 24.0),
        (17.0, 29.2), (29.8, 29.2), (39.0, 29.0),
        (17.2, 34.5), (29.8, 34.2),
    ]
    with d.clipped(region):
        for x, y in circles:
            d.ellipse(x, y, 1.55, 1.18, SAND, INK)
        for x, y in dots:
            d.circle(x, y, .68, INK, INK, True)
    return d


def build_alluvium():
    """FGM miscellaneous pattern: Staggered gull-wing double-arc marks on alluvium ground."""
    d = FieldDrawing()
    region = swatch(d, ALLUVIUM)
    with d.clipped(region):
        rows = [
            (14.5, [11.5, 24.0, 36.5]),
            (24.2, [17.8, 30.2]),
            (34.0, [11.5, 24.0, 36.5]),
        ]
        for y, xs in rows:
            for cx in xs:
                left_arc = [(cx - 3.9 + 3.9 * i / 16, y - 1.75 * math.sin(math.pi * i / 16))
                            for i in range(17)]
                right_arc = [(cx + 3.9 * i / 16, y - 1.75 * math.sin(math.pi * i / 16))
                             for i in range(17)]
                d.line(left_arc, INK, .82)
                d.line(right_arc, INK, .82)
    return d


def build_gossan_ore():
    """FGM miscellaneous pattern: Cellular diagonal cross-hatch with boxwork dots on gossan ground."""
    d = FieldDrawing()
    region = swatch(d, GOSSAN)
    spacing = 5.8
    d.hatch(region, angle=45, spacing=spacing, colour=INK, width=.7)
    d.hatch(region, angle=135, spacing=spacing, colour=INK, width=.7)
    with d.clipped(region):
        cx, cy = 24.0, 24.0
        step = spacing / math.sqrt(2)
        for r in range(-5, 6):
            for c in range(-6, 7):
                if (r + c) % 2 == 0:
                    x = cx + c * step
                    y = cy + r * step
                    if 6.5 <= x <= 41.5 and 10.5 <= y <= 37.5:
                        d.circle(x, y, .62, INK, INK, True)
    return d


ROWS = [
    ('gl_granite_post_kinematic', 'Post-Kinematic Granite',
     'Regular grid of upright crosses in a map swatch representing post-kinematic discordant granite.',
     'FGM 19.4.1 Orogenic granites (tectonic map symbols)', build_granite_post_kinematic),
    ('gl_granite_late_post_kinematic', 'Late- to Post-Kinematic Granite',
     'Widely spaced staggered crosses in a map swatch representing late- to post-kinematic granite.',
     'FGM 19.4.2 Orogenic granites (tectonic map symbols)', build_granite_late_post_kinematic),
    ('gl_granite_syn_late_kinematic', 'Syn- to Late-Kinematic Granite',
     'Staggered small crosses alternating with dots in a map swatch representing syn- to late-kinematic granite.',
     'FGM 19.4.3 Orogenic granites (tectonic map symbols)', build_granite_syn_late_kinematic),
    ('gl_granite_syn_kinematic_foliated', 'Syn-Kinematic Foliated Granite',
     'Bold sigmoidal S-shaped foliation marks in a map swatch representing foliated syn-kinematic granite.',
     'FGM 19.4.4 Orogenic granites (tectonic map symbols)', build_granite_syn_kinematic_foliated),
    ('gl_granite_gneissic_anatectic', 'Gneissic Anatectic Granite',
     'Tilted four-pointed stars in a map swatch representing gneissic anatectic granite.',
     'FGM 19.4.5 Orogenic granites (tectonic map symbols)', build_granite_gneissic_anatectic),
    ('gl_gabbro_diorite_orogenic', 'Orogenic Gabbro-Diorite',
     'Staggered diagonal x-marks in a map swatch representing volcanic-arc gabbro and diorite.',
     'FGM 19.4.6 Orogenic granites (tectonic map symbols)', build_gabbro_diorite_orogenic),
    ('gl_porphyry_pattern', 'Porphyry Pattern',
     'Randomly oriented short phenocryst dashes in a map swatch representing porphyry intrusions.',
     'FGM 19.4.7 Orogenic granites (tectonic map symbols)', build_porphyry_pattern),
    ('gl_island_arc_volcanics', 'Island-Arc Volcanics',
     'Closely nested rows of upward-pointing chevrons in a map swatch representing island-arc extrusives.',
     'FGM 19.5.1 Orogenic felsic volcanics (tectonic map symbols)', build_island_arc_volcanics),
    ('gl_felsic_volcanics_rare_basics', 'Rift Felsic Volcanics with Rare Basics',
     'Alternating rows of directional chevron ticks in a map swatch representing volcanic-rift felsic extrusives.',
     'FGM 19.5.2 Orogenic felsic volcanics (tectonic map symbols)', build_felsic_volcanics_rare_basics),
    ('gl_rhyolite_dacite_volcanics', 'Rhyolite and Dacite Volcanics',
     'Sparsely scattered open angle ticks at varied orientations in a map swatch representing rhyolite and dacite.',
     'FGM 19.5.3 Orogenic felsic volcanics (tectonic map symbols)', build_rhyolite_dacite_volcanics),
    ('gl_felsic_volcanics_with_granite', 'Felsic Volcanics Associated with Granite',
     'Dense rotated angle ticks interspersed with dots in a map swatch representing granite-coupled felsic volcanics.',
     'FGM 19.5.4 Orogenic felsic volcanics (tectonic map symbols)', build_felsic_volcanics_with_granite),
    ('gl_flood_basalt', 'Flood Basalt and Trap',
     'Staggered right-pointing chevrons and dots in a map swatch representing cratonic flood basalt.',
     'FGM 19.6.1 Cratonic igneous rocks (tectonic map symbols)', build_flood_basalt),
    ('gl_dolerite_granophyre', 'Dolerite-Granophyre',
     'Scattered paired parallel bars at varied angles in a map swatch representing dolerite and granophyre.',
     'FGM 19.6.2 Cratonic igneous rocks (tectonic map symbols)', build_dolerite_granophyre),
    ('gl_keratophyre', 'Keratophyre',
     'Rotated T-bar ticks with corner barbs in a map swatch representing keratophyre extrusives.',
     'FGM 19.6.3 Cratonic igneous rocks (tectonic map symbols)', build_keratophyre),
    ('gl_granite_intruding_craton', 'Granite Intruding Craton',
     'Upright crosses surrounded by stipple dot trails in a map swatch representing craton-intruding granite.',
     'FGM 19.6.5 Cratonic igneous rocks (tectonic map symbols)', build_granite_intruding_craton),
    ('gl_layered_intrusion', 'Layered Mafic-Ultramafic Intrusion',
     'Rhythmic cumulate layers of settled olivine grains and tabular plagioclase laths in a map swatch.',
     'FGM 19.6.6 Cratonic igneous rocks (tectonic map symbols)', build_layered_intrusion),
    ('gl_alkaline_intrusive', 'Alkaline Intrusive',
     'Euhedral zoned nepheline hexagons and acicular pyroxene needles in a map swatch.',
     'FGM 19.6.7 Cratonic igneous rocks (tectonic map symbols)', build_alkaline_intrusive),
    ('gl_kimberlite_lamproite', 'Kimberlite and Lamproite',
     'Downward-tapering carrot-shaped diatreme pipe cutting bedded wall rock and packed with mantle xenoliths.',
     'FGM 19.6.8 Cratonic igneous rocks (tectonic map symbols)', build_kimberlite_lamproite),
    ('gl_carbonatite', 'Carbonatite',
     'Staggered solid diamond symbols in a map swatch representing carbonatite intrusions.',
     'FGM 19.6.9 Cratonic igneous rocks (tectonic map symbols)', build_carbonatite),
    ('gl_slate_phyllite', 'Slate and Phyllite Pattern',
     'Closely spaced parallel horizontal cleavage lines in a map swatch representing slate and phyllite.',
     'FGM Patterns for geological maps - metamorphic rocks', build_slate_phyllite),
    ('gl_schist_gneiss_high_grade', 'High-Grade Schist and Gneiss Pattern',
     'Staggered wavy crenulated foliation segments in a map swatch representing high-grade schist and gneiss.',
     'FGM Patterns for geological maps - metamorphic rocks', build_schist_gneiss_high_grade),
    ('gl_sandy_slate_interbedded', 'Sandy Slate and Interbedded Sediments',
     'Parallel cleavage lines alternating with dotted sandy interbeds in a map swatch.',
     'FGM Patterns for geological maps - metamorphic rocks', build_sandy_slate_interbedded),
    ('gl_hornfels_massive', 'Massive Hornfels Pattern',
     'Brick-staggered solid squares in a map swatch representing massive contact-metamorphic hornfels.',
     'FGM Patterns for geological maps - metamorphic rocks', build_hornfels_massive),
    ('gl_basic_plutonic_hypabyssal', 'Basic Plutonic and Hypabyssal Pattern',
     'Dense ophitic clusters of parallel lath dashes in a map swatch representing basic plutonic rock.',
     'FGM Patterns for geological maps - igneous rocks', build_basic_plutonic_hypabyssal),
    ('gl_bedded_lavas', 'Bedded Lavas Pattern',
     'Layered wavy flow lines with directional arrow-like barbs in a map swatch representing bedded lavas.',
     'FGM Patterns for geological maps - igneous rocks', build_bedded_lavas),
    ('gl_tuff_tuffaceous_sandstone', 'Tuff and Tuffaceous Sandstone',
     'Randomly oriented shard dashes mixed with stipple dots in a map swatch representing tuffaceous rock.',
     'FGM Patterns for geological maps - miscellaneous', build_tuff_tuffaceous_sandstone),
    ('gl_bedded_tuff', 'Bedded Tuff and Tuffaceous Shale',
     'Horizontal bedding lines punctuated by staggered V-notches in a map swatch representing bedded tuff.',
     'FGM Patterns for geological maps - miscellaneous', build_bedded_tuff),
    ('gl_breccia_pattern', 'Breccia Pattern',
     'Scattered solid angular triangle clasts at varied orientations in a map swatch representing breccia.',
     'FGM Patterns for geological maps - miscellaneous', build_breccia_pattern),
    ('gl_scree_brecciated_rock', 'Brecciated Rock and Scree',
     'Solid and outlined angular triangle clasts amidst dense stipple dots in a map swatch.',
     'FGM Patterns for geological maps - miscellaneous', build_scree_brecciated_rock),
    ('gl_soil_cover', 'Soil Cover Pattern',
     'Small open granules and sparse stipple dots in a map swatch representing residual soil cover.',
     'FGM Patterns for geological maps - miscellaneous', build_soil_cover),
    ('gl_alluvium', 'Alluvium Pattern',
     'Staggered gull-wing double-arc marks in a map swatch representing alluvial deposits.',
     'FGM Patterns for geological maps - miscellaneous', build_alluvium),
    ('gl_gossan_ore', 'Gossan and Ore Outcrop Pattern',
     'Diagonal cross-hatching with central boxwork dots in a map swatch representing gossan and ore.',
     'FGM Patterns for geological maps - miscellaneous', build_gossan_ore),
]
