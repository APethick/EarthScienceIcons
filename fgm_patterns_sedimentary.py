"""FGM sedimentary and coal map patterns (ref/12) and coal seam symbols (FGM 5.6.2, ref/14-15)."""
import math
from functools import partial
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

from fgm_common import (
    ALLUVIUM, BROWN_COAL, CHERT, CLAY, COAL, COAL_DULL, CONGLOMERATE,
    DOLOMITE, FieldDrawing, GRID, HEAT, INK, LIMESTONE, MUDSTONE,
    OIL_SHALE, PAPER, QUARTZ, SAND, SANDSTONE, SHALE, SOIL, STEEL, TUFF,
    WHITE, block, ellipse_points, grid_points, irregular_polygon, rng,
    scatter, smooth, smooth_closed, swatch,
)
from icons_geophysics_expanded import Part

REF_MAP = 'FGM Patterns for geological maps - sedimentary rocks'
REF_COAL = 'FGM 5.6.2 Graphic representation of coal seams'


# --------------------------------------------------------- private helpers --

def _knockout_shape(d, geom, fill=WHITE, outline=False, width=.55):
    """Subtract ``geom`` from dark coal ink in mono and paint ``fill`` in colour."""
    ink = geom.boundary.buffer(width / 2, quad_segs=6, join_style=1) if outline else Polygon()
    d.parts.append(Part(ink, INK if outline else fill, geom, fill))


def _knockout_line(d, points, width=1.55, fill=WHITE, cap=1):
    """White/light line on dark coal ground that survives monochrome closing."""
    geom = LineString(points).buffer(width / 2, quad_segs=6, cap_style=cap, join_style=1)
    _knockout_shape(d, geom, fill=fill, outline=False)


def _dark_swatch(d, fill=COAL):
    """Solid dark map-pattern swatch (black in mono, ``fill`` in flat colour)."""
    d.rect(4, 8, 40, 32, fill, 1.2)
    d.solid(box(4, 8, 44, 40).buffer(-.45), fill)
    return box(4, 8, 44, 40).buffer(-1.15)


def _seam_frame(d, fill=PAPER):
    """Standard 40x18 horizontal coal seam bar with subtle roof/floor strata lines."""
    x, y, w, h = 4, 15, 40, 18
    d.dashed([(5, 11.2), (43, 11.2)], STEEL, width=.58, dash=3.2, gap=2.0)
    d.dashed([(5, 36.8), (43, 36.8)], STEEL, width=.58, dash=3.2, gap=2.0)
    d.shape(box(x, y, x + w, y + h), fill, INK, 1.0)
    return x, y, w, h


def _seam_bright_fraction(frac):
    """5.6.2 brightness classes: left ``frac`` solid bright coal, right dull coal."""
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, PAPER)
    bw = round(w * frac, 2)
    d.solid(box(x, y, x + bw, y + h), COAL)
    if bw < w - .5:
        d.line([(x + bw, y), (x + bw, y + h)], INK, .85)
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def _fibrous_mark(d, cx, cy, r=1.48, tick=3.1, width=.62):
    """Open circle with horizontal side ticks (5.6.2 no.9 fibrous coal)."""
    d.line([(cx - tick, cy), (cx - r, cy)], INK, width)
    d.line([(cx + r, cy), (cx + tick, cy)], INK, width)
    d.shape(Point(cx, cy).buffer(r, quad_segs=18), WHITE, INK, width)


# -------------------------------------------- 1-21, 36: Map pattern swatches --

def gl_conglomerate_pattern():
    d = FieldDrawing()
    region = swatch(d, CONGLOMERATE)
    r = rng(101)
    rows_y = [11.6, 17.0, 22.4, 27.8, 33.2, 37.6]
    with d.clipped(region):
        for r_idx, y in enumerate(rows_y):
            xs = [8.5, 16.25, 24.0, 31.75, 39.5] if r_idx % 2 == 0 else [12.4, 20.1, 27.9, 35.6]
            for c_idx, x in enumerate(xs):
                i = r_idx * 5 + c_idx
                rx = 2.35 + (i % 3 - 1) * .25
                ry = 1.38 + ((i // 2) % 2 - .5) * .18
                ang = r.uniform(-16, 16)
                pts = ellipse_points(x, y, rx, ry, steps=28, angle=ang)
                fill = SANDSTONE if (r_idx + c_idx) % 2 == 0 else '#C7AF83'
                d.shape(Polygon(pts), fill, INK, .8)
    return d


def gl_sandstone_pattern():
    d = FieldDrawing()
    region = swatch(d, SANDSTONE)
    with d.clipped(region):
        for x, y in scatter(202, 64, region, spacing=3.5, margin=1.3):
            d.circle(x, y, .65, INK, INK, True)
    return d


def gl_pebbly_sandstone():
    d = FieldDrawing()
    region = swatch(d, SANDSTONE)
    pebbles = [
        (11.0, 13.8, 2.6, 1.55, -12),
        (24.5, 13.4, 2.3, 1.42, 14),
        (36.8, 15.2, 2.5, 1.50, -8),
        (16.8, 23.6, 2.65, 1.58, 10),
        (30.8, 24.4, 2.35, 1.45, -16),
        (10.5, 33.2, 2.4, 1.48, 8),
        (23.2, 33.6, 2.55, 1.52, -10),
        (36.2, 33.0, 2.3, 1.42, 14),
    ]
    pebble_geoms = []
    with d.clipped(region):
        for px, py, rx, ry, ang in pebbles:
            pts = ellipse_points(px, py, rx, ry, steps=28, angle=ang)
            poly = Polygon(pts)
            pebble_geoms.append(poly.buffer(1.95))
            d.shape(poly, CONGLOMERATE, INK, .82)
        avoid = unary_union(pebble_geoms)
        for x, y in scatter(303, 60, region, spacing=3.35, margin=1.1):
            if not avoid.contains(Point(x, y)):
                d.circle(x, y, .62, INK, INK, True)
    return d


def gl_cross_bedded_sandstone():
    d = FieldDrawing()
    region = swatch(d, SANDSTONE)
    with d.clipped(region):
        # Gently curved set truncation surfaces (ref/12 bottom of sandstone col)
        s1 = smooth([(4, 16.2), (18, 14.8), (32, 16.4), (44, 15.0)], 3)
        s2 = smooth([(4, 25.0), (16, 26.4), (30, 24.5), (44, 25.8)], 3)
        s3 = smooth([(4, 33.4), (20, 32.2), (34, 33.8), (44, 32.6)], 3)
        lines = [LineString(s1), LineString(s2), LineString(s3)]
        for s in (s1, s2, s3):
            d.line(s, INK, .84)
        # Set 1 (y=8..16): tangential concave-up foresets dipping right
        for x0 in range(2, 40, 7):
            pts = smooth([(x0, 8.0), (x0 + 3.2, 12.8), (x0 + 8.5, 15.6)], 3)
            lines.append(LineString(pts))
            d.line(pts, INK, .68)
        # Set 2 (y=16..25.5): tangential concave-up foresets dipping left
        for x0 in range(9, 47, 7):
            pts = smooth([(x0, 15.6), (x0 - 3.4, 21.5), (x0 - 8.8, 25.2)], 3)
            lines.append(LineString(pts))
            d.line(pts, INK, .68)
        # Set 3 (y=25.5..33): tangential concave-up foresets dipping right
        for x0 in range(1, 40, 7):
            pts = smooth([(x0, 25.2), (x0 + 3.4, 30.0), (x0 + 8.6, 33.0)], 3)
            lines.append(LineString(pts))
            d.line(pts, INK, .68)
        # Set 4 (y=33..40): tangential foresets dipping right
        for x0 in range(4, 42, 7):
            pts = smooth([(x0, 33.0), (x0 + 3.0, 37.4), (x0 + 7.8, 39.8)], 3)
            lines.append(LineString(pts))
            d.line(pts, INK, .68)
        # Interstitial sand stipple grains clear of all laminae
        avoid = unary_union([ln.buffer(1.75) for ln in lines])
        for x, y in scatter(404, 48, region, spacing=3.2, margin=1.2):
            if not avoid.contains(Point(x, y)):
                d.circle(x, y, .58, INK, INK, True)
    return d


def gl_limestone_pattern():
    d = FieldDrawing()
    region = swatch(d, LIMESTONE)
    courses = [8.0, 14.4, 20.8, 27.2, 33.6, 40.0]
    with d.clipped(region):
        for y in courses[1:-1]:
            d.line([(4, y), (44, y)], INK, 1.05)
        for row, (y0, y1) in enumerate(zip(courses[:-1], courses[1:])):
            offset = 4.5 if row % 2 else 0.0
            x = 8.5 + offset
            while x < 42.5:
                d.line([(x, y0), (x, y1)], INK, 1.0)
                x += 9.0
    return d


def gl_dolomite_pattern():
    d = FieldDrawing()
    region = swatch(d, DOLOMITE)
    courses = [8.0, 14.4, 20.8, 27.2, 33.6, 40.0]
    with d.clipped(region):
        for y in courses[1:-1]:
            d.line([(4, y), (44, y)], INK, 1.05)
        for row, (y0, y1) in enumerate(zip(courses[:-1], courses[1:])):
            dy = y1 - y0
            shift = 4.5 if row % 2 else 0.0
            dx = dy * .72  # Consistent oblique rhomb joint angle across all courses (ref/12)
            x = 5.5 + shift
            while x < 41.5:
                d.line([(x, y0), (x + dx, y1)], INK, 1.0)
                x += 9.0
    return d


def gl_sandy_limestone():
    d = FieldDrawing()
    region = swatch(d, LIMESTONE)
    courses = [8.0, 14.4, 20.8, 27.2, 33.6, 40.0]
    with d.clipped(region):
        for y in courses[1:-1]:
            d.line([(4, y), (44, y)], INK, .76)
        for row, (y0, y1) in enumerate(zip(courses[:-1], courses[1:])):
            ym = (y0 + y1) / 2
            offset = 5.0 if row % 2 else 0.0
            x = 4.0 + offset
            while x < 44.0:
                if 5.5 < x < 42.5:
                    d.line([(x, y0), (x, y1)], INK, .72)
                for gx in (x + 3.3, x + 6.7):
                    if 6.2 < gx < 41.8:
                        d.circle(gx, ym, .58, INK, INK, True)
                x += 10.0
    return d


def gl_shale_pattern():
    d = FieldDrawing()
    region = swatch(d, SHALE)
    with d.clipped(region):
        for row, y in enumerate([11.2, 15.0, 18.8, 22.6, 26.4, 30.2, 34.0, 37.6]):
            x = 5.5 + (3.6 if row % 2 else 0.0)
            while x < 42.5:
                d.line([(x, y), (min(x + 4.4, 42.8), y)], INK, .72)
                x += 7.2
    return d


def gl_sandy_shale():
    d = FieldDrawing()
    region = swatch(d, SHALE)
    with d.clipped(region):
        dash_rows = [10.8, 18.2, 25.6, 33.0]
        dot_rows = [14.5, 21.9, 29.3, 36.7]
        for row, y in enumerate(dash_rows):
            x = 5.2 + (3.5 if row % 2 else 0.0)
            while x < 42.5:
                d.line([(x, y), (min(x + 4.5, 42.8), y)], INK, .72)
                x += 7.0
        for row, y in enumerate(dot_rows):
            x = 6.4 + (1.8 if row % 2 else 0.0)
            while x < 42.0:
                d.circle(x, y, .6, INK, INK, True)
                x += 3.8
    return d


def gl_bedded_chert():
    d = FieldDrawing()
    region = swatch(d, CHERT)
    with d.clipped(region):
        # Bedded chert: horizontal bed boundaries with oblique hachure bundles and dots (ref/12)
        for yb in (16.0, 24.0, 32.0):
            d.line([(4, yb), (44, yb)], INK, .64)
        rows = [12.0, 20.0, 28.0, 36.0]
        for r_idx, y in enumerate(rows):
            x = 7.5 + (4.5 if r_idx % 2 else 0.0)
            while x < 41.0:
                for k in (-1, 0, 1):
                    ox = x + k * 1.7
                    d.line([(ox - .85, y + 1.45), (ox + .85, y - 1.45)], INK, .62)
                if x + 4.6 < 41.5:
                    d.circle(x + 4.6, y, .54, INK, INK, True)
                x += 9.2
    return d


def gl_massive_chert():
    d = FieldDrawing()
    region = swatch(d, CHERT)
    with d.clipped(region):
        # Massive chert: interlocking 2D patchwork of ///, \\\ and === hachure packets (ref/12)
        rows_y = [12.0, 18.6, 25.2, 31.8, 37.8]
        xs = [8.2, 16.0, 23.8, 31.6, 39.4]
        for r_idx, y in enumerate(rows_y):
            for c_idx, x0 in enumerate(xs):
                x = x0 + (1.4 if r_idx % 2 else -1.0)
                if not (6.2 < x < 41.8):
                    continue
                mode = (r_idx * 2 + c_idx) % 3
                if mode == 0:
                    for k in (-1, 0, 1):
                        ox = x + k * 1.65
                        d.line([(ox - .85, y + 1.5), (ox + .85, y - 1.5)], INK, .62)
                elif mode == 1:
                    for k in (-1, 0, 1):
                        ox = x + k * 1.65
                        d.line([(ox + .85, y + 1.5), (ox - .85, y - 1.5)], INK, .62)
                else:
                    for dy in (-1.35, .0, 1.35):
                        d.line([(x - 2.3, y + dy), (x + 2.3, y + dy)], INK, .6)
    return d


def gl_coal_undifferentiated():
    d = FieldDrawing()
    _dark_swatch(d, COAL)
    return d


def gl_broken_coal():
    d = FieldDrawing()
    region = _dark_swatch(d, COAL)
    cracks = [
        [(4, 15), (13, 17), (21, 13), (31, 16), (44, 13)],
        [(4, 26), (14, 24), (24, 28), (34, 24), (44, 27)],
        [(4, 35), (16, 33), (27, 36), (37, 33), (44, 36)],
        [(13, 8), (13, 17), (14, 24), (11, 34), (13, 40)],
        [(24, 8), (21, 13), (24, 28), (27, 36), (25, 40)],
        [(35, 8), (31, 16), (34, 24), (37, 33), (35, 40)],
    ]
    with d.clipped(region):
        for pts in cracks:
            _knockout_line(d, pts, width=1.55, fill=WHITE)
    return d


def gl_coal_with_shale_bands():
    d = FieldDrawing()
    region = _dark_swatch(d, COAL)
    # Staggered light lenticular shale bands with internal fissile dash on black coal (ref/12)
    rows = [13.0, 20.4, 27.8, 35.0]
    with d.clipped(region):
        for r_idx, y in enumerate(rows):
            x = 10.5 + (6.8 if r_idx % 2 else 0.0)
            while x < 39.5:
                upper = []
                lower = []
                rx, ry = 5.6, 2.25
                for i in range(21):
                    u = (i / 20) * 2 - 1
                    env = max(0.0, 1 - u * u)
                    upper.append((x + u * rx, y - ry * env))
                    lower.append((x + u * rx, y + ry * env))
                lens = Polygon(upper + list(reversed(lower)))
                _knockout_shape(d, lens, fill=SHALE)
                d.line([(x - 2.1, y), (x + 2.1, y)], INK, .6)
                x += 13.6
    return d


def gl_shale_with_coal_bands():
    d = FieldDrawing()
    region = swatch(d, SHALE)
    with d.clipped(region):
        for idx, y0 in enumerate([13.5, 24.0, 34.5]):
            upper = []
            lower = []
            for i in range(25):
                t = i / 24
                x = 4 + 40 * t
                swell = 1.15 + .75 * math.sin(t * math.tau * 2 + idx * 1.4)
                wave_y = y0 + .5 * math.cos(t * math.tau * 1.5 + idx)
                upper.append((x, wave_y - swell))
                lower.append((x, wave_y + swell))
            band = Polygon(upper + list(reversed(lower)))
            d.solid(band, COAL)
        for y in (9.6, 18.8, 29.2):
            d.dashed([(5.5, y), (42.5, y)], INK, width=.65, dash=3.2, gap=2.2)
    return d


def gl_cannel_coal():
    d = FieldDrawing()
    region = _dark_swatch(d, COAL)
    with d.clipped(region):
        for x in [9.0, 14.0, 19.0, 24.0, 29.0, 34.0, 39.0]:
            _knockout_line(d, [(x, 8), (x, 40)], width=1.55, fill=WHITE, cap=2)
    return d


def gl_cannel_shale():
    d = FieldDrawing()
    region = _dark_swatch(d, COAL)
    with d.clipped(region):
        for x in [12.0, 20.0, 28.0, 36.0]:
            _knockout_line(d, [(x, 8), (x, 40)], width=1.55, fill=WHITE, cap=2)
        for y in [14.4, 20.8, 27.2, 33.6]:
            _knockout_line(d, [(4, y), (44, y)], width=1.55, fill=WHITE, cap=2)
    return d


def gl_carbonaceous_shale():
    d = FieldDrawing()
    region = _dark_swatch(d, COAL)
    with d.clipped(region):
        for y in [13.2, 18.6, 24.0, 29.4, 34.8]:
            _knockout_line(d, [(4, y), (44, y)], width=1.55, fill=WHITE, cap=2)
    return d


def gl_brown_coal():
    d = FieldDrawing()
    region = _dark_swatch(d, BROWN_COAL)
    with d.clipped(region):
        for r_idx, y in enumerate([13.5, 24.0, 34.5]):
            for cx in [11.0, 24.0, 37.0]:
                pts = [
                    (cx - 4.0, y + .6),
                    (cx - 1.5, y - 1.5),
                    (cx + 1.5, y + 1.5),
                    (cx + 4.0, y - .6),
                ]
                _knockout_line(d, smooth(pts, 3), width=1.6, fill=WHITE)
    return d


def gl_oil_shale():
    d = FieldDrawing()
    region = swatch(d, '#E6E1D3')
    with d.clipped(region):
        lenses = [
            (12.0, 12.2, 5.2, 1.15), (27.5, 11.8, 5.8, 1.2), (39.5, 13.0, 4.5, 1.0),
            (8.5, 18.0, 4.8, 1.1), (21.0, 18.2, 6.0, 1.25), (34.5, 17.8, 5.2, 1.15),
            (13.5, 24.0, 5.8, 1.25), (28.5, 24.2, 5.5, 1.2), (40.0, 23.6, 4.2, 1.0),
            (9.0, 30.0, 5.0, 1.15), (22.5, 30.2, 6.0, 1.25), (36.0, 29.8, 5.2, 1.15),
            (14.0, 35.8, 5.5, 1.2), (29.5, 35.5, 5.8, 1.2),
        ]
        for lx, ly, rx, ry in lenses:
            upper = []
            lower = []
            for i in range(17):
                u = (i / 16) * 2 - 1
                env = max(0.0, 1 - u * u)
                wy = .45 * math.sin(u * math.pi)
                upper.append((lx + u * rx, ly + wy - ry * env))
                lower.append((lx + u * rx, ly + wy + ry * env))
            d.solid(Polygon(upper + list(reversed(lower))), OIL_SHALE)
    return d


def gl_thin_seam():
    d = FieldDrawing()
    region = swatch(d, SANDSTONE)
    with d.clipped(region):
        seam = Polygon([(4, 24.5), (44, 17.5), (44, 23.0), (4, 30.0)])
        d.solid(seam, COAL)
        d.line([(4, 24.5), (44, 17.5)], INK, .85)
        d.line([(4, 30.0), (44, 23.0)], INK, .85)
        for dy in (-7.5, -4.0, 4.5, 8.0):
            d.dashed([(5, 27.2 + dy), (43, 20.2 + dy)], INK, width=.62, dash=3.6, gap=2.4)
    return d


# -------------------------------------- 22-35: FGM 5.6.2 Coal seam symbols --

gl_coal_bright = partial(_seam_bright_fraction, 0.93)
gl_coal_bright_dull_bands = partial(_seam_bright_fraction, 0.76)
gl_coal_interbanded = partial(_seam_bright_fraction, 0.50)
gl_coal_dull_bright_bands = partial(_seam_bright_fraction, 0.28)
gl_coal_dull_minor_bright = partial(_seam_bright_fraction, 0.09)


def gl_coal_dull():
    # No. 7: Dull coal (up to 1% bright) - two narrow vertical black bands at left
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, PAPER)
    d.solid(box(x, y, x + 2.4, y + h), COAL)
    d.solid(box(x + 4.1, y, x + 6.5, y + h), COAL)
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def gl_coal_canneloid():
    # No. 8: Dull conchoidal (canneloid) - cross-hatched end block on left
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, PAPER)
    end_w = 10.5
    end_box = box(x, y, x + end_w, y + h)
    d.shape(end_box, '#E2E5E4', INK, .85)
    d.hatch(end_box.buffer(-.3), angle=45, spacing=3.2, colour=INK, width=.64)
    d.hatch(end_box.buffer(-.3), angle=-45, spacing=3.2, colour=INK, width=.64)
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def gl_coal_fibrous():
    # No. 9: Fibrous coal - two rows of four small circles with horizontal ticks
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, PAPER)
    for ry in (y + 5.4, y + 12.6):
        for cx in (10.2, 19.4, 28.6, 37.8):
            _fibrous_mark(d, cx, ry, r=1.48, tick=3.1, width=.64)
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def gl_coal_weathered():
    # No. 10: Weathered coal - central solid black vertical band
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, PAPER)
    d.solid(box(20.0, y, 28.0, y + h), COAL)
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def gl_coal_heat_altered():
    # No. 11: Heat-altered coal - central vertical ruling band
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, PAPER)
    band = box(18.5, y, 29.5, y + h)
    d.shape(band, '#EED6C4', INK, .82)
    for vx in (20.7, 22.9, 25.1, 27.3):
        d.line([(vx, y), (vx, y + h)], INK, .64)
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def gl_non_coal():
    # No. 12: Non-coal undifferentiated - open unshaded seam bar
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, '#ECEEEB')
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def gl_coal_interlayered_non_coal():
    # No. 13: Coal interlayered with non-coal (Cr) - narrow white strip on left, black on right
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, PAPER)
    split = x + 9.0
    d.solid(box(split, y, x + w, y + h), COAL_DULL)
    d.line([(split, y), (split, y + h)], INK, .85)
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def gl_non_coal_interlayered_coal():
    # No. 14: Non-coal interlayered with coal (Rc) - wide white on left, narrow black strip on right
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, PAPER)
    split = x + w - 8.5
    d.solid(box(split, y, x + w, y + h), COAL)
    d.line([(split, y), (split, y + h)], INK, .85)
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def gl_stony_coal():
    # No. 15: Stony coal (Sc) - two thin vertical lines in centre of bar
    d = FieldDrawing()
    x, y, w, h = _seam_frame(d, '#E7E9E5')
    d.line([(21.5, y), (21.5, y + h)], INK, .78)
    d.line([(26.5, y), (26.5, y + h)], INK, .78)
    d.shape(box(x, y, x + w, y + h), None, INK, 1.0)
    return d


def gl_mudstone_pattern():
    # No. 17: Mudstone (Ms) - continuous bedding lines with dense double-dash rows
    d = FieldDrawing()
    region = swatch(d, MUDSTONE)
    with d.clipped(region):
        for y in (13.4, 21.4, 29.4, 37.4):
            d.line([(4, y), (44, y)], INK, .7)
        for row, y_base in enumerate([9.4, 17.4, 25.4, 33.4]):
            for dy in (-1.15, 1.15):
                y = y_base + dy
                x = 5.2 + (3.4 if row % 2 else 0.0)
                while x < 42.5:
                    d.line([(x, y), (min(x + 4.2, 42.8), y)], INK, .64)
                    x += 6.8
    return d


def gl_coal_seam_log():
    # Example graphic coal seam column (ref/15 right)
    d = FieldDrawing()
    x, w = 10, 24
    # 1. Weathered coal (W): y=4..8.5
    d.shape(box(x, 4.0, x + w, 8.5), PAPER, INK, .8)
    d.solid(box(x + 8.5, 4.0, x + 15.5, 8.5), COAL)
    # 2. Dull minor bright (Dmb): y=8.5..12.5
    d.shape(box(x, 8.5, x + w, 12.5), PAPER, INK, .8)
    d.solid(box(x, 8.5, x + 3.5, 12.5), COAL)
    # 3. Shale roof/parting (Sh): y=12.5..17.5
    d.shape(box(x, 12.5, x + w, 17.5), SHALE, INK, .8)
    for ry, ox in ((14.2, 2.2), (16.0, 5.2)):
        for dx in range(0, 20, 6):
            if ox + dx + 3.6 < w - 1.2:
                d.line([(x + ox + dx, ry), (x + ox + dx + 3.6, ry)], INK, .62)
    # 4. Bright coal (B): y=17.5..24.0
    d.solid(box(x, 17.5, x + w, 24.0), COAL)
    # 5. Fibrous coal (F): y=24.0..29.2
    d.shape(box(x, 24.0, x + w, 29.2), PAPER, INK, .8)
    for cx in (x + 5.5, x + 12.0, x + 18.5):
        _fibrous_mark(d, cx, 26.6, r=1.42, tick=2.55, width=.58)
    # 6. Sandstone band (Ss): y=29.2..33.2
    d.shape(box(x, 29.2, x + w, 33.2), SANDSTONE, INK, .8)
    for gx, gy in ((13.5, 31.0), (17.8, 31.5), (22.0, 30.8), (26.2, 31.6), (30.5, 31.0)):
        d.circle(gx, gy, .56, INK, INK, True)
    # 7. Interbanded coal (DB): y=33.2..38.6
    d.shape(box(x, 33.2, x + w, 38.6), PAPER, INK, .8)
    d.solid(box(x, 33.2, x + w * .5, 38.6), COAL)
    d.line([(x + w * .5, 33.2), (x + w * .5, 38.6)], INK, .75)
    # 8. Coal interlayered with non-coal (Cr): y=38.6..44.0
    d.shape(box(x, 38.6, x + w, 44.0), PAPER, INK, .8)
    d.solid(box(x + 5.5, 38.6, x + w, 44.0), COAL_DULL)
    d.line([(x + 5.5, 38.6), (x + 5.5, 44.0)], INK, .75)
    # Outer column frame and right-hand bed ticks (like ref/15)
    d.shape(box(x, 4.0, x + w, 44.0), None, INK, .95)
    for ty in (6.25, 10.5, 15.0, 20.75, 26.6, 31.2, 35.9, 41.3):
        d.line([(x + w, ty), (x + w + 4.2, ty)], INK, .72)
    return d


# -------------------------------------------------------------------- rows --

ROWS = [
    ('gl_conglomerate_pattern', 'Conglomerate Pattern',
     'Rounded pebble ellipses in staggered courses within a sandy conglomerate swatch.',
     REF_MAP, gl_conglomerate_pattern),
    ('gl_sandstone_pattern', 'Sandstone Pattern',
     'Evenly stippled quartz sand grains across a sandstone map swatch.',
     REF_MAP, gl_sandstone_pattern),
    ('gl_pebbly_sandstone', 'Pebbly Sandstone Pattern',
     'Scattered rounded pebbles set within a stippled sandstone matrix.',
     REF_MAP, gl_pebbly_sandstone),
    ('gl_cross_bedded_sandstone', 'Cross-Bedded Sandstone Pattern',
     'Tabular cross-bedded sets with curved tangential foreset laminae truncated by bedding surfaces.',
     REF_MAP, gl_cross_bedded_sandstone),
    ('gl_limestone_pattern', 'Limestone Pattern',
     'Regular courses of orthogonal masonry-style limestone blocks.',
     REF_MAP, gl_limestone_pattern),
    ('gl_dolomite_pattern', 'Dolomite Pattern',
     'Bedding courses cut by oblique rhombic cross-joints characteristic of dolomite.',
     REF_MAP, gl_dolomite_pattern),
    ('gl_sandy_limestone', 'Sandy Limestone Pattern',
     'Orthogonal limestone block pattern containing sand stipple grains within each course.',
     REF_MAP, gl_sandy_limestone),
    ('gl_shale_pattern', 'Shale Pattern',
     'Staggered horizontal rows of short parallel fissile shale dashes.',
     REF_MAP, gl_shale_pattern),
    ('gl_sandy_shale', 'Sandy Shale Pattern',
     'Alternating horizons of dashed shale laminae and stippled sand grains.',
     REF_MAP, gl_sandy_shale),
    ('gl_bedded_chert', 'Bedded Chert Pattern',
     'Stratified rows of oblique chalcedonic hachure bundles and silica dots separated by bedding planes.',
     REF_MAP, gl_bedded_chert),
    ('gl_massive_chert', 'Massive Chert Pattern',
     'Interlocking dashed horizons and alternating oblique hachure clusters across a massive chert swatch.',
     REF_MAP, gl_massive_chert),
    ('gl_coal_undifferentiated', 'Undifferentiated Coal Pattern',
     'Solid black map swatch representing undifferentiated coal seams.',
     REF_MAP, gl_coal_undifferentiated),
    ('gl_broken_coal', 'Broken Coal Pattern',
     'Solid dark coal swatch traversed by an irregular polygonal network of white fractures.',
     REF_MAP, gl_broken_coal),
    ('gl_coal_with_shale_bands', 'Coal with Shale Bands',
     'Solid dark coal swatch enclosing staggered rows of light lenticular shale bands.',
     REF_MAP, gl_coal_with_shale_bands),
    ('gl_shale_with_coal_bands', 'Shale with Coal Bands',
     'Light fissile shale swatch containing wavy pinch-and-swell black coal bands.',
     REF_MAP, gl_shale_with_coal_bands),
    ('gl_cannel_coal', 'Cannel Coal Pattern',
     'Solid dark coal swatch ruled by closely spaced vertical white lines.',
     REF_MAP, gl_cannel_coal),
    ('gl_cannel_shale', 'Cannel Shale Pattern',
     'Solid dark coal swatch divided by orthogonal vertical and horizontal white lines into a block grid.',
     REF_MAP, gl_cannel_shale),
    ('gl_carbonaceous_shale', 'Carbonaceous Shale Pattern',
     'Solid dark carbonaceous swatch ruled by parallel horizontal white bedding lines.',
     REF_MAP, gl_carbonaceous_shale),
    ('gl_brown_coal', 'Brown Coal Pattern',
     'Dark brown-black lignite swatch marked by rows of white wavy woody curls.',
     REF_MAP, gl_brown_coal),
    ('gl_oil_shale', 'Oil Shale Pattern',
     'Light kerogenous shale swatch with staggered dark wavy lenticular streaks.',
     REF_MAP, gl_oil_shale),
    ('gl_thin_seam', 'Thin Dipping Coal Seam',
     'Thin gently dipping solid black coal seam enclosed within bedded host rock.',
     REF_MAP, gl_thin_seam),
    ('gl_coal_bright', 'Bright Coal Seam (>90% Bright)',
     'Horizontal seam bar with over ninety percent solid black bright coal on the left and a thin dull margin on the right.',
     REF_COAL, gl_coal_bright),
    ('gl_coal_bright_dull_bands', 'Bright Coal with Dull Bands (60-90%)',
     'Horizontal seam bar partitioned into three-quarters black bright coal on the left and one-quarter dull coal on the right.',
     REF_COAL, gl_coal_bright_dull_bands),
    ('gl_coal_interbanded', 'Interbanded Dull and Bright Coal (40-60%)',
     'Horizontal seam bar split equally into black bright coal on the left and light dull coal on the right.',
     REF_COAL, gl_coal_interbanded),
    ('gl_coal_dull_bright_bands', 'Mainly Dull Coal with Bright Bands (10-40%)',
     'Horizontal seam bar with roughly one-quarter black bright coal on the left and three-quarters light dull coal on the right.',
     REF_COAL, gl_coal_dull_bright_bands),
    ('gl_coal_dull_minor_bright', 'Dull Coal with Minor Bright Bands (1-10%)',
     'Horizontal seam bar with a narrow black bright-coal stripe at the left edge and dominant light dull coal.',
     REF_COAL, gl_coal_dull_minor_bright),
    ('gl_coal_dull', 'Dull Coal (Up to 1% Bright)',
     'Horizontal dull-coal seam bar marked by two thin vertical black stripes at the left margin.',
     REF_COAL, gl_coal_dull),
    ('gl_coal_canneloid', 'Canneloid Dull Conchoidal Coal',
     'Horizontal dull-coal seam bar with a diagonally cross-hatched block at the left end.',
     REF_COAL, gl_coal_canneloid),
    ('gl_coal_fibrous', 'Fibrous Coal (Fusain)',
     'Horizontal seam bar containing two rows of small open circles with horizontal side ticks.',
     REF_COAL, gl_coal_fibrous),
    ('gl_coal_weathered', 'Weathered Coal Seam',
     'Horizontal seam bar marked by a central vertical solid black band.',
     REF_COAL, gl_coal_weathered),
    ('gl_coal_heat_altered', 'Heat-Altered (Cindered) Coal Seam',
     'Horizontal seam bar with a central vertical band of closely spaced parallel lines.',
     REF_COAL, gl_coal_heat_altered),
    ('gl_non_coal', 'Undifferentiated Non-Coal Seam Parting',
     'Unshaded horizontal seam bar bounded by roof and floor strata lines.',
     REF_COAL, gl_non_coal),
    ('gl_coal_interlayered_non_coal', 'Coal Interlayered with Non-Coal',
     'Horizontal seam bar with a narrow light non-coal strip on the left and dark coal across the right three-quarters.',
     REF_COAL, gl_coal_interlayered_non_coal),
    ('gl_non_coal_interlayered_coal', 'Non-Coal Interlayered with Coal',
     'Horizontal seam bar with dominant light non-coal on the left and a narrow black coal band at the right edge.',
     REF_COAL, gl_non_coal_interlayered_coal),
    ('gl_stony_coal', 'Stony Coal Seam',
     'Horizontal seam bar divided near its centre by two thin vertical parallel lines.',
     REF_COAL, gl_stony_coal),
    ('gl_mudstone_pattern', 'Mudstone Pattern',
     'Map swatch with continuous horizontal bedding lines alternating with dense double-dashed mudstone rows.',
     REF_COAL, gl_mudstone_pattern),
    ('gl_coal_seam_log', 'Graphic Coal Seam Column',
     'Vertical graphic coal-seam log combining weathered, bright, interbanded, fibrous, dull and clastic parting symbols.',
     REF_COAL, gl_coal_seam_log),
]
