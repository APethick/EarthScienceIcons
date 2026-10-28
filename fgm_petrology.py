"""FGM petrology, sedimentology, stratigraphy and seismology icons.

Covers:
- Classification of gabbroic rocks (IUGS ternary diagrams, FGM ref 02)
- Grain roundness and sphericity classes (Powers scale, FGM ref 04)
- Visual percentage estimation charts for grains (1% to 50%, FGM ref 06-07)
- Lithostratigraphic unit and chronostratigraphic boundary stratotypes (FGM ref 16)
- Earthquake magnitude vs released energy spheres (FGM ref 27)
"""
import math
from functools import lru_cache, partial

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

from fgm_common import (
    ALLUVIUM, BASALT, CONGLOMERATE, DOLOMITE, FELDSPAR, FieldDrawing,
    GRANITE, GRANITE_LIGHT, HORNBLENDE, HORNFELS, INK, LIMESTONE, MUDSTONE,
    OLIVINE, PAPER, PLAGIOCLASE, PYROXENE, QUARTZ, SAND, SANDSTONE, SCHIST,
    SHALE, SKY, SLATE, VOLCANIC, WATER, WHITE, ellipse_points,
    irregular_polygon, rng, smooth, smooth_closed,
)
from icons_geophysics_expanded import Part


# ---------------------------------------------------------------------------
# 1. Gabbroic rock classification ternaries (ref 02)
# ---------------------------------------------------------------------------

_T = (24.0, 12.8)
_L = (11.2, 35.0)
_R = (36.8, 35.0)


def _bary(p, a, b):
    """Barycentric coordinates (Plag, Left-apex, Right-apex) -> (x, y)."""
    return (
        p * _T[0] + a * _L[0] + b * _R[0],
        p * _T[1] + a * _L[1] + b * _R[1],
    )


def _glyph_plagioclase(d, cx=24.0, cy=7.0):
    """White/pale tabular lath with polysynthetic twin lines."""
    pts = [
        (cx - 5.4, cy - 2.6),
        (cx + 5.8, cy - 2.6),
        (cx + 5.4, cy + 2.6),
        (cx - 5.8, cy + 2.6),
    ]
    d.poly(pts, WHITE, INK)
    # Alternating albite twin lamella
    lam = [
        (cx - 1.8, cy - 2.6),
        (cx + 1.9, cy - 2.6),
        (cx + 1.5, cy + 2.6),
        (cx - 2.2, cy + 2.6),
    ]
    d.poly(lam, PLAGIOCLASE, INK)
    for dx in (-3.6, -1.8, 1.8, 3.6):
        d.line([(cx + dx + 0.2, cy - 2.5), (cx + dx - 0.2, cy + 2.5)], INK, 0.6)


def _glyph_pyroxene(d, cx, cy, is_opx=False, is_cpx=False):
    """Dark green stubby octagonal prism with ~90-degree intersecting cleavage."""
    rx, ry = 4.2, 3.8
    c = 0.48
    pts = [
        (cx - rx * c, cy - ry),
        (cx + rx * c, cy - ry),
        (cx + rx, cy - ry * c),
        (cx + rx, cy + ry * c),
        (cx + rx * c, cy + ry),
        (cx - rx * c, cy + ry),
        (cx - rx, cy + ry * c),
        (cx - rx, cy - ry * c),
    ]
    fill = '#748254' if is_opx else PYROXENE
    d.poly(pts, fill, INK)
    if is_cpx:
        # Diagonal ~87/93 deg cleavage network in clinopyroxene
        for off in (-1.3, 1.3):
            d.line([(cx - 2.6, cy - 2.4 + off), (cx + 2.6, cy + 2.4 + off)], INK, 0.6)
            d.line([(cx - 2.6, cy + 2.4 + off), (cx + 2.6, cy - 2.4 + off)], INK, 0.6)
    else:
        # Orthogonal 90 deg cleavage grid
        for off in (-1.3, 1.3):
            d.line([(cx - 3.6, cy + off), (cx + 3.6, cy + off)], INK, 0.6)
            d.line([(cx + off, cy - 3.3), (cx + off, cy + 3.3)], INK, 0.6)


def _glyph_olivine(d, cx, cy):
    """Olive-green equant rounded grain with characteristic curved fractures."""
    pts = smooth_closed([
        (cx - 3.8, cy - 2.4),
        (cx - 1.2, cy - 3.9),
        (cx + 2.2, cy - 3.6),
        (cx + 4.2, cy - 1.2),
        (cx + 3.9, cy + 2.2),
        (cx + 1.0, cy + 3.8),
        (cx - 2.6, cy + 3.4),
        (cx - 4.3, cy + 0.8),
    ], iterations=2)
    d.poly(pts, OLIVINE, INK)
    d.line([(cx - 2.8, cy - 1.6), (cx - 0.3, cy + 0.2), (cx + 2.9, cy - 1.4)], INK, 0.65)
    d.line([(cx - 0.3, cy + 0.2), (cx + 0.8, cy + 3.2)], INK, 0.65)


def _glyph_hornblende(d, cx, cy):
    """Near-black elongate pseudo-hexagonal prism with 120/60-degree diamond cleavage."""
    rx, ry = 5.0, 3.5
    pts = [
        (cx - rx, cy),
        (cx - rx * 0.42, cy - ry),
        (cx + rx * 0.42, cy - ry),
        (cx + rx, cy),
        (cx + rx * 0.42, cy + ry),
        (cx - rx * 0.42, cy + ry),
    ]
    d.poly(pts, HORNBLENDE, INK)
    # Central 120-degree cleavage rhomb highlighted slightly for flat-colour contrast
    inner_rhomb = [
        (cx - 2.6, cy),
        (cx, cy - 1.6),
        (cx + 2.6, cy),
        (cx, cy + 1.6),
    ]
    d.poly(inner_rhomb, '#5A6D63', INK)
    d.line([(cx - 3.2, cy - 1.9), (cx + 3.2, cy + 1.9)], INK, 0.6)
    d.line([(cx - 3.2, cy + 1.9), (cx + 3.2, cy - 1.9)], INK, 0.6)


def gabbroic_ternary(kind):
    d = FieldDrawing()
    # Outer ternary triangle
    d.poly([_T, _L, _R], PAPER, INK)

    p_hi = 0.84
    p_lo = 0.14

    if kind == 'plag_px_ol':
        # Central olivine gabbronorite field shaded subtly
        central = [
            _bary(p_hi, 0.08, 0.08),
            _bary(p_lo, 0.78, 0.08),
            _bary(p_lo, 0.08, 0.78),
        ]
        d.poly(central, '#D3DEC4', INK)
        # 90 and 10 plagioclase horizontal lines
        d.line([_bary(p_hi, 0.16, 0.0), _bary(p_hi, 0.0, 0.16)], INK, 0.75)
        d.line([_bary(p_lo, 0.86, 0.0), _bary(p_lo, 0.0, 0.86)], INK, 0.75)
        # 50% tick on bottom edge
        mid_base = _bary(0.0, 0.5, 0.5)
        d.line([mid_base, (mid_base[0], mid_base[1] - 1.6)], INK, 0.65)
        # Mineral glyphs at apices
        _glyph_plagioclase(d, 24.0, 7.0)
        _glyph_pyroxene(d, 7.8, 40.2)
        _glyph_olivine(d, 40.2, 40.2)

    elif kind == 'plag_px_hbl':
        # Central pyroxene-hornblende gabbronorite field
        central = [
            _bary(p_hi, 0.08, 0.08),
            _bary(p_lo, 0.78, 0.08),
            _bary(p_lo, 0.08, 0.78),
        ]
        d.poly(central, '#C2D3CB', INK)
        # 90 and 10 plagioclase lines
        d.line([_bary(p_hi, 0.16, 0.0), _bary(p_hi, 0.0, 0.16)], INK, 0.75)
        d.line([_bary(p_lo, 0.86, 0.0), _bary(p_lo, 0.0, 0.86)], INK, 0.75)
        # Bottom strip divisions: pyroxenite, hbl pyroxenite, px hornblendite, hornblendite
        d.line([_bary(p_lo, 0.78, 0.08), _bary(0.0, 0.90, 0.10)], INK, 0.75)
        d.line([_bary(p_lo, 0.08, 0.78), _bary(0.0, 0.10, 0.90)], INK, 0.75)
        d.line([_bary(p_lo, 0.43, 0.43), _bary(0.0, 0.50, 0.50)], INK, 0.75)
        # Mineral glyphs at apices
        _glyph_plagioclase(d, 24.0, 7.0)
        _glyph_pyroxene(d, 7.8, 40.2)
        _glyph_hornblende(d, 40.0, 40.2)

    elif kind == 'plag_opx_cpx':
        # Central gabbronorite trapezoid (cpx norite + opx gabbro)
        m = 0.06
        central = [
            _bary(p_hi, 1.0 - p_hi - m, m),
            _bary(p_hi, m, 1.0 - p_hi - m),
            _bary(p_lo, m, 1.0 - p_lo - m),
            _bary(p_lo, 1.0 - p_lo - m, m),
        ]
        d.poly(central, '#CAD6C6', INK)
        # 90 and 10 plagioclase lines
        d.line([_bary(p_hi, 0.16, 0.0), _bary(p_hi, 0.0, 0.16)], INK, 0.75)
        d.line([_bary(p_lo, 0.86, 0.0), _bary(p_lo, 0.0, 0.86)], INK, 0.75)
        # Dashed median boundary dividing cpx norite from opx gabbro
        d.dashed(
            [_bary(p_hi, 0.08, 0.08), _bary(p_lo, 0.43, 0.43)],
            INK, width=0.75, dash=2.0, gap=1.3,
        )
        # Mineral glyphs at apices: Plag, Opx, Cpx
        _glyph_plagioclase(d, 24.0, 7.0)
        _glyph_pyroxene(d, 7.8, 40.2, is_opx=True)
        _glyph_pyroxene(d, 40.2, 40.2, is_cpx=True)

    else:
        raise ValueError(kind)
    return d


# ---------------------------------------------------------------------------
# 2. Grain roundness and sphericity classes (ref 04)
# ---------------------------------------------------------------------------

def _roundness_scale_bar(d, active_step):
    """Consistent 6-step scale bar at the bottom with ``active_step`` (0..5) filled."""
    y0, w, h = 38.2, 5.3, 4.2
    step_dx = 6.45
    x_start = 24.0 - (5 * step_dx + w) / 2.0
    for i in range(6):
        x = x_start + i * step_dx
        if i == active_step:
            d.solid(box(x, y0, x + w, y0 + h), INK)
        else:
            d.rect(x, y0, w, h, PAPER, 0.25, INK)


def roundness_class(step):
    """Draw the high-sphericity (left) and low-sphericity (right) grains for step 0..5."""
    d = FieldDrawing()
    hx, hy = 14.2, 18.8
    lx, ly = 34.6, 18.8

    if step == 0:  # Very angular
        high_pts = [
            (hx - 6.8, hy - 6.5), (hx - 3.6, hy - 6.8), (hx - 2.0, hy - 8.4),
            (hx + 0.5, hy - 7.0), (hx + 1.8, hy - 8.0), (hx + 3.4, hy - 6.2),
            (hx + 5.2, hy - 7.2), (hx + 7.4, hy - 4.4), (hx + 6.4, hy + 0.5),
            (hx + 7.2, hy + 2.4), (hx + 5.4, hy + 3.2), (hx + 4.4, hy + 6.8),
            (hx + 1.8, hy + 6.4), (hx + 0.2, hy + 7.8), (hx - 3.8, hy + 6.8),
            (hx - 6.2, hy + 4.4), (hx - 8.0, hy + 0.6), (hx - 7.8, hy - 2.2),
            (hx - 6.4, hy - 3.8),
        ]
        low_pts = [
            (lx - 3.2, ly - 10.5), (lx - 1.2, ly - 11.6), (lx + 0.4, ly - 10.6),
            (lx + 2.4, ly - 11.4), (lx + 3.0, ly - 6.8), (lx + 4.2, ly - 4.0),
            (lx + 3.8, ly - 1.2), (lx + 5.2, ly + 2.2), (lx + 4.2, ly + 5.6),
            (lx + 5.0, ly + 8.2), (lx + 1.2, ly + 11.8), (lx - 4.6, ly + 8.6),
            (lx - 4.2, ly + 5.8), (lx - 5.4, ly + 3.2), (lx - 4.4, ly + 0.6),
            (lx - 5.2, ly - 2.8), (lx - 3.8, ly - 6.4),
        ]
        d.poly(high_pts, SANDSTONE, INK)
        d.line([(hx - 3.8, hy - 3.2), (hx + 0.8, hy + 0.5), (hx + 4.2, hy - 1.8)], INK, 0.6)
        d.line([(hx + 0.8, hy + 0.5), (hx - 1.2, hy + 4.8)], INK, 0.6)

        d.poly(low_pts, QUARTZ, INK)
        d.line([(lx - 1.2, ly - 7.5), (lx + 1.0, ly - 0.5), (lx - 1.4, ly + 7.2)], INK, 0.6)

    elif step == 1:  # Angular
        high_pts = [
            (hx - 4.2, hy - 6.4), (hx + 0.6, hy - 8.0), (hx + 5.4, hy - 7.6),
            (hx + 6.0, hy - 4.6), (hx + 8.2, hy - 0.8), (hx + 5.8, hy + 4.2),
            (hx + 2.6, hy + 6.6), (hx - 0.8, hy + 8.4), (hx - 4.4, hy + 6.6),
            (hx - 5.2, hy + 2.4), (hx - 7.6, hy - 1.0), (hx - 6.8, hy - 4.4),
        ]
        low_pts = [
            (lx + 0.2, ly - 11.6), (lx + 1.6, ly - 10.2), (lx + 1.4, ly - 7.8),
            (lx + 4.4, ly - 5.6), (lx + 3.8, ly + 3.8), (lx + 2.2, ly + 10.6),
            (lx - 0.4, ly + 11.8), (lx - 2.6, ly + 11.2), (lx - 4.4, ly - 2.2),
            (lx - 2.8, ly - 8.4),
        ]
        d.poly(high_pts, SANDSTONE, INK)
        d.line([(hx - 3.6, hy - 2.4), (hx + 1.6, hy + 0.6), (hx + 5.0, hy - 2.0)], INK, 0.6)
        d.line([(hx + 1.6, hy + 0.6), (hx - 0.4, hy + 5.4)], INK, 0.6)

        d.poly(low_pts, QUARTZ, INK)
        d.line([(lx + 0.2, ly - 7.2), (lx - 0.6, ly + 7.8)], INK, 0.6)

    elif step == 2:  # Subangular
        high_raw = [
            (hx - 7.4, hy - 4.6), (hx - 2.4, hy - 7.8), (hx + 4.6, hy - 7.4),
            (hx + 7.8, hy - 3.2), (hx + 6.2, hy + 4.2), (hx + 3.2, hy + 6.8),
            (hx - 4.8, hy + 5.4), (hx - 7.2, hy + 1.2),
        ]
        low_raw = [
            (lx - 3.8, ly - 10.6), (lx - 0.6, ly - 11.2), (lx + 3.2, ly - 7.8),
            (lx + 5.6, ly - 1.8), (lx + 5.8, ly + 6.2), (lx + 3.6, ly + 9.8),
            (lx - 2.4, ly + 10.6), (lx - 4.8, ly + 8.0), (lx - 4.4, ly + 2.8),
            (lx - 2.4, ly - 0.8), (lx - 4.6, ly - 6.8),
        ]
        d.poly(smooth_closed(high_raw, 1), SANDSTONE, INK)
        d.line([(hx - 3.2, hy - 2.2), (hx + 2.4, hy + 1.2)], INK, 0.6)

        d.poly(smooth_closed(low_raw, 1), QUARTZ, INK)
        d.line([(lx - 0.4, ly - 6.2), (lx + 1.8, ly + 5.4)], INK, 0.6)

    elif step == 3:  # Subrounded
        high_raw = [
            (hx - 5.2, hy - 6.4), (hx + 2.6, hy - 8.2), (hx + 5.8, hy - 5.6),
            (hx + 8.0, hy + 1.0), (hx + 5.4, hy + 3.4), (hx + 6.2, hy + 6.6),
            (hx + 0.8, hy + 7.8), (hx - 5.6, hy + 6.2), (hx - 7.8, hy - 1.2),
        ]
        low_raw = [
            (lx - 0.4, ly - 11.6), (lx + 4.6, ly - 5.8), (lx + 3.8, ly + 0.6),
            (lx + 4.8, ly + 5.6), (lx + 2.2, ly + 10.8), (lx - 4.2, ly + 10.2),
            (lx - 4.6, ly - 4.2), (lx - 3.2, ly - 9.8),
        ]
        d.poly(smooth_closed(high_raw, 2), SANDSTONE, INK)
        d.arc(hx + 0.8, hy + 0.5, 4.4, 20, 115, INK)

        d.poly(smooth_closed(low_raw, 2), QUARTZ, INK)
        d.line([(lx + 0.4, ly - 5.5), (lx + 0.8, ly + 5.5)], INK, 0.6)

    elif step == 4:  # Rounded
        high_raw = [
            (hx - 4.2, hy - 6.8), (hx + 1.6, hy - 7.8), (hx + 6.2, hy - 4.2),
            (hx + 7.8, hy + 1.8), (hx + 5.6, hy + 6.8), (hx - 0.4, hy + 8.0),
            (hx - 6.2, hy + 5.8), (hx - 7.4, hy - 0.8),
        ]
        low_raw = [
            (lx + 1.8, ly - 10.2), (lx + 4.6, ly - 6.8), (lx + 4.6, ly + 5.2),
            (lx + 2.2, ly + 10.2), (lx - 2.8, ly + 10.8), (lx - 4.0, ly + 3.6),
            (lx - 4.8, ly - 4.8), (lx - 1.8, ly - 8.2),
        ]
        d.poly(smooth_closed(high_raw, 3), SANDSTONE, INK)
        d.arc(hx, hy + 0.5, 4.6, 30, 120, INK)

        d.poly(smooth_closed(low_raw, 3), QUARTZ, INK)
        d.arc(lx, ly + 3.0, 2.6, 25, 145, INK)

    elif step == 5:  # Well-rounded
        high_pts = ellipse_points(hx, hy, 8.2, 7.4, angle=-18)
        low_raw = [
            (lx, ly - 11.4), (lx + 4.2, ly - 8.6), (lx + 4.8, ly),
            (lx + 4.2, ly + 8.6), (lx, ly + 11.4), (lx - 4.2, ly + 8.6),
            (lx - 4.8, ly), (lx - 4.2, ly - 8.6),
        ]
        d.poly(high_pts, SANDSTONE, INK)
        d.arc(hx, hy, 5.2, 25, 115, INK)

        d.poly(smooth_closed(low_raw, 3), QUARTZ, INK)
        d.arc(lx, ly + 4.0, 2.8, 25, 155, INK)

    else:
        raise ValueError(step)

    _roundness_scale_bar(d, step)
    return d


# ---------------------------------------------------------------------------
# 3. Grain percentage visual estimation charts (ref 06 & 07)
# ---------------------------------------------------------------------------

_GRAIN_COUNTS = {
    1: 4,
    2: 6,
    3: 9,
    5: 13,
    7: 17,
    10: 22,
    15: 30,
    20: 38,
    25: 44,
    30: 50,
    40: 62,
    50: 74,
}

_GAUGE_ANGLES = {
    1: 14,
    2: 20,
    3: 27,
    5: 36,
    7: 45,
    10: 56,
    15: 68,
    20: 79,
    25: 90,
    30: 108,
    40: 144,
    50: 180,
}


@lru_cache(maxsize=16)
def _compute_grains(pct, cx=20.0, cy=23.0, radius=16.6):
    """Compute non-overlapping angular grains whose exact area is ``pct``% of the circle."""
    circle_poly = Point(cx, cy).buffer(radius, quad_segs=32)
    target_area = (pct / 100.0) * circle_poly.area
    count = _GRAIN_COUNTS[pct]
    inner = circle_poly.buffer(-0.9)

    r = rng(700 + pct * 41)
    x0, y0, x1, y1 = inner.bounds

    # Sample well-spaced grain centres inside inner circle
    centers = []
    spacing = 2.4 * radius / math.sqrt(count)
    for _ in range(18):
        for _ in range(400):
            if len(centers) >= count:
                break
            x, y = r.uniform(x0, x1), r.uniform(y0, y1)
            if not inner.contains(Point(x, y)):
                continue
            if all((x - px) ** 2 + (y - py) ** 2 >= spacing ** 2 for px, py in centers):
                centers.append((x, y))
        if len(centers) >= count:
            break
        spacing *= 0.88

    # Generate unit angular grain templates around each centre
    templates = []
    for i, (gx, gy) in enumerate(centers):
        sides = 5 + (i % 3)
        rel_r = 0.82 + 0.38 * ((i * 7 + 3) % 11) / 10.0
        stretch = 0.72 + 0.56 * ((i * 5 + 2) % 9) / 8.0
        angle = (i * 47 + pct * 19) % 180
        pts = irregular_polygon(
            seed=3000 + pct * 100 + i,
            x=gx, y=gy,
            radius=rel_r,
            sides=sides,
            jitter=0.33,
            stretch=stretch,
            angle=angle,
        )
        templates.append((gx, gy, Polygon(pts)))

    gap = 0.36 if pct <= 30 else 0.28

    def build_at_scale(s):
        placed = []
        occupied = Polygon()
        for gx, gy, poly in templates:
            scaled = affinity.scale(poly, xfact=s, yfact=s, origin=(gx, gy))
            clipped = scaled.intersection(inner)
            if not occupied.is_empty:
                clipped = clipped.difference(occupied.buffer(gap, quad_segs=4))
            if not clipped.is_empty and clipped.area > 0.15:
                if clipped.geom_type == 'MultiPolygon':
                    clipped = max(clipped.geoms, key=lambda g: g.area)
                if clipped.geom_type == 'Polygon':
                    placed.append(clipped)
                    occupied = occupied.union(clipped)
        return placed, occupied.area

    # Binary search on scale factor s so total grain area == target_area
    lo, hi = 0.2, 6.0
    best_grains = []
    for _ in range(15):
        mid = 0.5 * (lo + hi)
        grains, area = build_at_scale(mid)
        best_grains = grains
        if area < target_area:
            lo = mid
        else:
            hi = mid

    return tuple(best_grains)


def _pie_gauge(d, pct, gx=39.4, gy=38.4, r_g=5.2):
    """Small circular pie-gauge showing the grain fraction at lower-right."""
    d.circle(gx, gy, r_g, QUARTZ, INK)
    # Reference ticks at 0%, 25%, 50%, 75%
    for deg in (-90, 0, 90, 180):
        a = math.radians(deg)
        d.line([
            (gx + (r_g - 1.1) * math.cos(a), gy + (r_g - 1.1) * math.sin(a)),
            (gx + r_g * math.cos(a), gy + r_g * math.sin(a)),
        ], INK, 0.55)
    # Filled pie wedge clockwise from 12 o'clock (-90 deg)
    span = _GAUGE_ANGLES[pct]
    steps = max(8, int(span / 4))
    wedge_pts = [(gx, gy)] + [
        (
            gx + r_g * math.cos(math.radians(-90 + span * i / steps)),
            gy + r_g * math.sin(math.radians(-90 + span * i / steps)),
        )
        for i in range(steps + 1)
    ]
    d.solid(Polygon(wedge_pts), INK)


def grain_percent_chart(pct):
    d = FieldDrawing()
    cx, cy, radius = 20.0, 23.0, 16.6
    d.circle(cx, cy, radius, PAPER, INK)
    for grain in _compute_grains(pct, cx, cy, radius):
        d.solid(grain, INK)
    _pie_gauge(d, pct)
    return d


# ---------------------------------------------------------------------------
# 4. Unit and boundary stratotypes (ref 16)
# ---------------------------------------------------------------------------

def unit_stratotype():
    """Landscape cross-section with dipping beds and bracketed Formation B unit stratotype."""
    d = FieldDrawing()

    # Dipping beds in the subsurface/outcrop profile (dipping left at ~32 deg)
    # Base clip polygon bounded by top topographic profile and flat bottom y=42
    topo = [
        (3.5, 31.0),
        (9.5, 24.5),    # Formation C cuesta crest
        (11.5, 25.8),
        (14.0, 24.8),   # Second cuesta ledge of Formation C
        (15.5, 27.5),   # <-- Upper Boundary Stratotype contact!
        (19.0, 27.8),
        (21.5, 29.2),   # Covered valley floor
        (26.5, 29.2),
        (29.0, 27.8),
        (33.5, 27.5),   # <-- Lower Boundary Stratotype contact!
        (37.5, 23.8),   # Formation A hogback ridge 1
        (39.2, 25.0),
        (41.5, 24.0),   # Formation A hogback ridge 2
        (44.5, 26.5),
    ]
    section_region = Polygon(topo + [(44.5, 42.0), (3.5, 42.0)])

    # Dipping stratigraphic units from left (youngest, Formation C) to right (oldest, Formation A)
    # All contacts dip left: dx = -15, dy = +15 (45 deg on screen)
    # Contact X positions at y = 27.5:
    # Formation C: x < 15.5 (divided into 2 limestone beds at x = 11.2)
    # Formation B (Unit Stratotype): 15.5 <= x <= 33.5 (divided at 20.0, 24.5, 29.0)
    # Formation A: x > 33.5 (divided at 38.2)
    def dip_band(x_left_top, x_right_top):
        y_top = 20.0
        y_bot = 43.0
        shift_top = -(y_top - 27.5) * 1.05
        shift_bot = -(y_bot - 27.5) * 1.05
        raw = Polygon([
            (x_left_top + shift_top, y_top),
            (x_right_top + shift_top, y_top),
            (x_right_top + shift_bot, y_bot),
            (x_left_top + shift_bot, y_bot),
        ]).intersection(section_region)
        polys = [g for g in getattr(raw, 'geoms', [raw]) if g.geom_type == 'Polygon' and g.area > 0.2]
        return max(polys, key=lambda g: g.area) if polys else Polygon()

    bands = [
        (-5.0, 11.2, LIMESTONE, 'limestone'),
        (11.2, 15.5, LIMESTONE, 'limestone'),
        (15.5, 20.0, SHALE, 'shale'),
        (20.0, 24.5, SANDSTONE, 'sandstone'),
        (24.5, 29.0, DOLOMITE, 'shale'),
        (29.0, 33.5, SANDSTONE, 'sandstone'),
        (33.5, 39.5, CONGLOMERATE, 'sandstone'),
        (39.5, 58.0, '#C8B289', 'sandstone'),
    ]

    for x0, x1, fill, kind in bands:
        poly = dip_band(x0, x1)
        if poly.is_empty:
            continue
        d.shape(poly, fill, INK)
        with d.clipped(poly.buffer(-0.35)):
            if kind == 'limestone':
                # Cross-joints perpendicular to bedding
                for t in range(-2, 10):
                    by = 24.0 + t * 2.4
                    bx = 0.5 * (x0 + x1) - (by - 27.5) * 1.05
                    d.line([(bx - 1.8, by - 1.6), (bx + 1.8, by + 1.6)], INK, 0.55)
            elif kind == 'shale':
                xm = 0.5 * (x0 + x1)
                d.dashed(
                    [(xm - (20.0 - 27.5) * 1.05, 20.0), (xm - (43.0 - 27.5) * 1.05, 43.0)],
                    INK, width=0.55, dash=1.8, gap=1.2,
                )
            elif kind == 'sandstone':
                xm = 0.5 * (x0 + x1)
                for k in range(8):
                    py = 24.0 + k * 2.2
                    px = xm - (py - 27.5) * 1.05 + ((k % 2) - 0.5) * 1.1
                    d.circle(px, py, 0.45, INK, INK, True)

    # Alluvial covered pocket in the middle of Formation B valley
    covered = Polygon([
        (20.2, 28.3), (24.0, 28.6), (27.8, 28.3),
        (26.5, 30.2), (21.5, 30.2),
    ])
    d.shape(covered, ALLUVIUM, INK)

    # Emphasise the two boundary contacts of Formation B
    for x_contact in (15.5, 33.5):
        d.line([
            (x_contact, 27.5),
            (x_contact - (42.0 - 27.5) * 1.05, 42.0),
        ], INK, 1.15)

    # Left and right Boundary Stratotype vertical flag markers
    # Left boundary at x = 15.5
    d.line([(11.5, 7.0), (15.5, 7.0), (15.5, 24.5)], INK, 0.95)
    d.text_free_arrow(15.5, 19.0, 15.5, 26.8, INK, width=0.95, head=2.8)

    # Right boundary at x = 33.5
    d.line([(37.5, 7.0), (33.5, 7.0), (33.5, 24.5)], INK, 0.95)
    d.text_free_arrow(33.5, 19.0, 33.5, 26.8, INK, width=0.95, head=2.8)

    # Double-headed horizontal arrow spanning the Unit Stratotype (Formation B)
    ym = 15.0
    d.line([(18.0, ym), (31.0, ym)], INK, 0.95)
    d.text_free_arrow(24.5, ym, 16.0, ym, INK, width=0.95, head=2.7)
    d.text_free_arrow(24.5, ym, 33.0, ym, INK, width=0.95, head=2.7)

    return d


def boundary_stratotype():
    """Stepped dipping succession with a single boundary marker arrow at the Stage A / Stage B contact."""
    d = FieldDrawing()

    # Beds dip to the lower-right with slope k = 0.28 (dy = 0.28 * dx)
    k = 0.28

    def bed_poly(x_left_top, y_left_top, x_left_bot, y_left_bot, x_right_top, x_right_bot):
        y_rt = y_left_top + k * (x_right_top - x_left_top)
        y_rb = y_left_bot + k * (x_right_bot - x_left_bot)
        return Polygon([
            (x_left_top, y_left_top),
            (x_right_top, y_rt),
            (x_right_bot, y_rb),
            (x_left_bot, y_left_bot),
        ])

    # 6 dipping beds from bottom (Stage A) to top (Stage B)
    # Stage A / Stage B boundary is between bed 2 (top of Stage A) and bed 3 (base of Stage B)
    # at left outcrop point (15.5, 25.0)!
    beds = [
        # Stage A (lower 3 beds)
        (11.0, 32.5, 8.0, 36.5, 31.0, 27.0, SHALE, 'shale'),
        (13.2, 28.8, 11.0, 32.5, 33.5, 31.0, DOLOMITE, 'limestone'),
        (15.5, 25.0, 13.2, 28.8, 36.0, 33.5, MUDSTONE, 'shale'),
        # Stage B (upper 3 beds)
        (17.5, 20.5, 15.5, 25.0, 38.5, 36.0, SANDSTONE, 'sandstone'),
        (20.8, 15.0, 17.5, 20.5, 41.2, 38.5, SHALE, 'shale'),
        (24.5, 8.5, 20.8, 15.0, 44.0, 41.2, LIMESTONE, 'limestone'),
    ]

    for xlt, ylt, xlb, ylb, xrt, xrb, fill, kind in beds:
        poly = bed_poly(xlt, ylt, xlb, ylb, xrt, xrb)
        d.shape(poly, fill, INK)
        with d.clipped(poly.buffer(-0.35)):
            if kind == 'shale':
                xm = 0.5 * (xlt + xlb)
                ym = 0.5 * (ylt + ylb)
                d.dashed(
                    [(xm - 1.0, ym - 0.28), (xrt, ym + k * (xrt - xm))],
                    INK, width=0.55, dash=2.0, gap=1.2,
                )
            elif kind == 'limestone':
                for step in range(1, 6):
                    t = step / 6.0
                    xt = xlt + t * (xrt - xlt)
                    yt = ylt + t * k * (xrt - xlt)
                    xb = xlb + t * (xrb - xlb)
                    yb = ylb + t * k * (xrb - xlb)
                    d.line([(xt, yt), (xb, yb)], INK, 0.6)
            elif kind == 'sandstone':
                for step in range(1, 7):
                    t = step / 7.5
                    px = 0.5 * (xlt + xlb) + t * (xrt - xlt)
                    py = 0.5 * (ylt + ylb) + t * k * (xrt - xlt)
                    d.circle(px, py, 0.48, INK, INK, True)

    # Prominent Stage A / Stage B boundary horizon line extending down-dip to the right
    bx0, by0 = 15.5, 25.0
    bx1 = 43.5
    by1 = by0 + k * (bx1 - bx0)
    d.line([(bx0, by0), (bx1, by1)], INK, 1.35)

    # Single Boundary Stratotype marker arrow on the left pointing at (15.5, 25.0)
    d.line([(8.0, 14.5), (14.2, 14.5), (14.2, 22.0)], INK, 1.05)
    d.text_free_arrow(14.2, 17.5, 14.2, 24.4, INK, width=1.05, head=3.0)

    return d


# ---------------------------------------------------------------------------
# 5. Earthquake magnitude vs energy spheres (ref 27)
# ---------------------------------------------------------------------------

def _shaded_sphere(d, cx, cy, r):
    """Sphere with concentric radial colour bands and monochrome highlight/shadow arcs."""
    bands = [
        (1.00, 0.00, 0.00, '#4E5B62'),
        (0.82, -0.05, -0.05, '#6C7C85'),
        (0.64, -0.10, -0.10, '#93A4AE'),
        (0.45, -0.14, -0.14, '#C1CFD6'),
        (0.25, -0.18, -0.18, SKY),
    ]
    for scale, ox, oy, fill in bands:
        disc = Point(cx + ox * r, cy + oy * r).buffer(r * scale, quad_segs=28)
        d.parts.append(Part(Polygon(), INK, disc, fill))

    # Crisp outer INK boundary
    d.circle(cx, cy, r, None, INK)

    # Concentric 3D crescent shading and highlight arcs so monochrome reads as a shaded sphere
    if r >= 12.0:
        d.arc(cx, cy, r * 0.85, -38, 128, INK)
        d.arc(cx, cy, r * 0.70, -22, 112, INK)
        d.arc(cx, cy, r * 0.55, -5, 95, INK)
        d.arc(cx - 0.14 * r, cy - 0.14 * r, r * 0.34, 195, 260, INK)
    elif r >= 5.0:
        d.arc(cx, cy, r * 0.80, -32, 122, INK)
        d.arc(cx, cy, r * 0.58, -12, 102, INK)
        d.arc(cx - 0.12 * r, cy - 0.12 * r, r * 0.34, 200, 255, INK)
    else:
        d.arc(cx, cy, r * 0.68, -25, 115, INK)


def earthquake_magnitude_energy():
    """Three shaded spheres of exponentially increasing volume for earthquake magnitude vs energy."""
    d = FieldDrawing()
    _shaded_sphere(d, 6.6, 39.2, 3.0)
    _shaded_sphere(d, 15.8, 34.6, 6.2)
    _shaded_sphere(d, 30.8, 19.2, 14.2)
    return d


# ---------------------------------------------------------------------------
# 6. QAPF plutonic rock classification & 2.4.1 Metamorphic facies (ref 01, 03)
# ---------------------------------------------------------------------------

def qapf_plutonic_diagram():
    """IUGS QAPF double-triangle diagram for plutonic rocks with modal field subdivisions."""
    d = FieldDrawing()
    qv, av, pv, fv = (24.0, 4.5), (7.5, 24.0), (40.5, 24.0), (24.0, 43.5)

    def qap(q, p_ratio):
        """Point in upper Q-A-P triangle at modal quartz fraction q and P/(A+P) = p_ratio."""
        y = 24.0 - q * (24.0 - 4.5)
        xl = 7.5 + q * (24.0 - 7.5)
        xr = 40.5 - q * (40.5 - 24.0)
        return (xl + p_ratio * (xr - xl), y)

    def fap(f, p_ratio):
        """Point in lower F-A-P triangle at modal foid fraction f and P/(A+P) = p_ratio."""
        y = 24.0 + f * (43.5 - 24.0)
        xl = 7.5 + f * (24.0 - 7.5)
        xr = 40.5 - f * (40.5 - 24.0)
        return (xl + p_ratio * (xr - xl), y)

    # Filled compositional zones inside the QAPF diamond
    # Quartzolite & quartz-rich granitoids (Q > 60%)
    d.poly([qv, qap(0.60, 0.0), qap(0.60, 1.0)], QUARTZ, INK)
    # Granite / granodiorite / tonalite belt (20% < Q < 60%)
    d.poly([qap(0.60, 0.0), qap(0.20, 0.0), qap(0.20, 0.65), qap(0.60, 0.65)], GRANITE_LIGHT, INK)
    d.poly([qap(0.60, 0.65), qap(0.20, 0.65), qap(0.20, 1.0), qap(0.60, 1.0)], PLAGIOCLASE, INK)
    # Syenite / monzonite / monzodiorite / gabbro-diorite belt (0 < Q < 20% and 0 < F < 10%)
    d.poly([qap(0.20, 0.0), av, fap(0.10, 0.0), fap(0.10, 0.65), qap(0.0, 0.65), qap(0.20, 0.65)], FELDSPAR, INK)
    d.poly([qap(0.20, 0.65), qap(0.0, 0.65), fap(0.10, 0.65), fap(0.10, 1.0), pv, qap(0.20, 1.0)], SANDSTONE, INK)
    # Foid syenite / foid monzosyenite / foid monzodiorite / foid gabbro belt (10% < F < 60%)
    d.poly([fap(0.10, 0.0), fap(0.60, 0.0), fap(0.60, 0.50), fap(0.10, 0.50)], '#C7B6D8', INK)
    d.poly([fap(0.10, 0.50), fap(0.60, 0.50), fap(0.60, 1.0), fap(0.10, 1.0)], LIMESTONE, INK)
    # Foidolites (F > 60%)
    d.poly([fap(0.60, 0.0), fv, fap(0.60, 1.0)], VOLCANIC, INK)

    # Dashed Q=90 line (quartzolite) and Q=5 line (quartz-bearing prefix)
    d.dashed([qap(0.88, 0.0), qap(0.88, 1.0)], INK, width=0.6, dash=1.4, gap=1.0)
    # Solid horizontal Q=60, Q=20, Q=0/F=0, F=10, F=60 boundaries
    for q in (0.60, 0.20, 0.0):
        d.line([qap(q, 0.0), qap(q, 1.0)], INK, 0.8)
    for f in (0.10, 0.60):
        d.line([fap(f, 0.0), fap(f, 1.0)], INK, 0.8)

    # Radial plagioclase-ratio dividers in upper triangle (10, 35, 65, 90)
    for p_ratio in (0.10, 0.35, 0.65, 0.90):
        q_top = 0.60 if p_ratio in (0.10, 0.65, 0.90) else 0.20
        d.line([qap(q_top, p_ratio), qap(0.0, p_ratio)], INK, 0.7)
        d.line([qap(0.0, p_ratio), fap(0.10, p_ratio)], INK, 0.7)

    # Radial dividers in lower foid triangle (10, 50, 90 from F=10 to F=60)
    for p_ratio in (0.10, 0.50, 0.90):
        d.line([fap(0.10, p_ratio), fap(0.60, p_ratio)], INK, 0.7)

    # Crisp outer QAPF diamond border
    d.poly([qv, pv, fv, av], None, INK)
    return d


def metamorphic_facies_diagram():
    """FGM 2.4.1 Pressure-Temperature metamorphic facies diagram with closed facies fields."""
    d = FieldDrawing()
    # Rectangular P-T plot frame (x: 6..43, y: 6..41)
    frame = box(6.0, 6.0, 43.0, 41.0)
    d.shape(frame, PAPER, INK, width=0.95)

    with d.clipped(frame.buffer(-0.2)):
        # Upper bounding geotherm / high-P limit and eclogite cap
        eclogite = Polygon([(13.0, 6.5), (41.0, 6.5), (41.0, 11.5), (34.0, 15.8), (23.0, 16.5), (13.0, 6.5)])
        d.shape(eclogite, '#C9877C', INK, width=0.75)

        # Dashed lower limit of metamorphism on the left
        lower_lim = smooth([(12.5, 8.5), (9.5, 22.0), (8.6, 33.5), (12.0, 38.8), (24.0, 40.4)], 2)
        d.dashed(lower_lim, INK, width=0.7, dash=2.0, gap=1.3)

        # Zeolite field (bottom-left corner along lower limit)
        zeolite = Polygon(smooth_closed([
            (8.8, 31.2), (11.5, 33.5), (12.2, 39.2), (9.2, 37.5)
        ], 2))
        d.shape(zeolite, QUARTZ, INK, width=0.7)

        # Prehnite-pumpellyite lobe ('A')
        prehnite = Polygon(smooth_closed([
            (11.0, 29.0), (14.5, 26.5), (15.8, 29.5), (13.8, 34.8), (11.2, 33.0)
        ], 2))
        d.shape(prehnite, LIMESTONE, INK, width=0.7)

        # Glaucophane-lawsonite schist (Blueschist) lobe (high-P, low-T upper-left)
        blueschist = Polygon(smooth_closed([
            (12.2, 10.2), (18.0, 15.0), (18.4, 21.0), (13.5, 26.0), (9.6, 28.2), (10.5, 19.0)
        ], 2))
        d.shape(blueschist, '#8CAEC4', INK, width=0.75)

        # Greenschist lobe (central-left)
        greenschist = Polygon(smooth_closed([
            (15.2, 35.8), (16.5, 26.5), (20.5, 17.5), (22.8, 19.0), (21.5, 33.0), (18.0, 36.8)
        ], 2))
        d.shape(greenschist, '#8FB08B', INK, width=0.75)

        # Amphibolite lobe (large central field)
        amphibolite = Polygon(smooth_closed([
            (22.5, 33.5), (23.8, 18.2), (28.5, 16.5), (32.5, 18.5), (30.5, 32.8), (26.0, 34.8)
        ], 2))
        d.shape(amphibolite, SCHIST, INK, width=0.75)

        # Granulite lobe (high-T right field)
        granulite = Polygon(smooth_closed([
            (31.2, 33.5), (34.5, 17.0), (37.8, 16.2), (36.0, 32.5), (33.5, 34.2)
        ], 2))
        d.shape(granulite, SANDSTONE, INK, width=0.75)

        # Low-P contact hornfels & sanidinite fields along the base (y ~ 35.5..41)
        hornfels = Polygon(smooth([(16.0, 40.8), (21.5, 36.8), (29.2, 36.0), (27.0, 40.8)], 2) + [(16.0, 40.8)])
        d.shape(hornfels, HORNFELS, INK, width=0.7)
        pyx_hornfels = Polygon(smooth([(27.8, 40.8), (31.0, 36.5), (38.0, 39.2), (42.8, 39.0), (42.8, 40.8)], 2))
        d.shape(pyx_hornfels, FELDSPAR, INK, width=0.7)

        # Minimum melting Qu-Or-Ab curve sweeping down from top-centre to bottom-right
        melting_curve = smooth([(27.5, 13.5), (28.8, 25.5), (31.5, 35.0), (36.5, 39.5), (42.5, 40.5)], 2)
        d.dashed(melting_curve, INK, width=0.85, dash=1.4, gap=1.0)

    # Re-stroke frame and exterior ticks on left (kb), bottom (T C) and right (Depth km)
    d.poly([(6.0, 6.0), (43.0, 6.0), (43.0, 41.0), (6.0, 41.0)], None, INK)
    for y in (11.5, 17.0, 22.5, 28.0, 33.5):
        d.line([(6.0, y), (7.4, y)], INK, 0.65)
        d.line([(41.6, y), (43.0, y)], INK, 0.65)
    for x in (11.5, 17.5, 23.5, 29.5, 35.5):
        d.line([(x, 41.0), (x, 39.6)], INK, 0.65)
        d.line([(x, 6.0), (x, 7.4)], INK, 0.65)
    return d


# ---------------------------------------------------------------------------
# Module contract: ROWS
# ---------------------------------------------------------------------------

ROWS = [
    (
        'gl_qapf_plutonic_diagram',
        'QAPF Plutonic Rock Diagram',
        'IUGS QAPF double-triangle diagram for plutonic rocks with modal quartz, alkali feldspar, plagioclase and feldspathoid field boundaries.',
        'FGM Classification of plutonic rocks (IUGS QAPF)',
        qapf_plutonic_diagram,
    ),
    (
        'gl_gabbroic_plag_px_ol',
        'Gabbroic Rocks (Plag-Px-Ol)',
        'IUGS ternary diagram for plagioclase, pyroxene and olivine with mineral glyphs at each apex and a shaded central olivine gabbronorite field.',
        'FGM Classification of gabbroic rocks (IUGS)',
        partial(gabbroic_ternary, 'plag_px_ol'),
    ),
    (
        'gl_gabbroic_plag_px_hbl',
        'Gabbroic Rocks (Plag-Px-Hbl)',
        'IUGS ternary diagram for plagioclase, pyroxene and hornblende with apex mineral glyphs and subdivided ultramafic base fields.',
        'FGM Classification of gabbroic rocks (IUGS)',
        partial(gabbroic_ternary, 'plag_px_hbl'),
    ),
    (
        'gl_gabbroic_plag_opx_cpx',
        'Gabbroic Rocks (Plag-Opx-Cpx)',
        'IUGS ternary diagram for plagioclase, orthopyroxene and clinopyroxene with a dashed median boundary separating norite and gabbro fields.',
        'FGM Classification of gabbroic rocks (IUGS)',
        partial(gabbroic_ternary, 'plag_opx_cpx'),
    ),
    (
        'gl_metamorphic_facies_diagram',
        'Metamorphic Facies Diagram (P-T)',
        'Pressure-temperature diagram showing closed zeolite, blueschist, greenschist, amphibolite, granulite, eclogite and hornfels facies fields with the minimum melting curve.',
        'FGM 2.4.1 Metamorphic facies diagram',
        metamorphic_facies_diagram,
    ),
    (
        'gl_roundness_very_angular',
        'Roundness: Very Angular',
        'High-sphericity and low-sphericity clasts with jagged, serrated edges and sharp fracture points above a six-step roundness bar.',
        'FGM Roundness and sphericity',
        partial(roundness_class, 0),
    ),
    (
        'gl_roundness_angular',
        'Roundness: Angular',
        'High-sphericity and low-sphericity clasts bounded by planar fracture facets and sharp vertices above a six-step roundness bar.',
        'FGM Roundness and sphericity',
        partial(roundness_class, 1),
    ),
    (
        'gl_roundness_subangular',
        'Roundness: Subangular',
        'High-sphericity and low-sphericity clasts with flat faces and slightly blunted corners above a six-step roundness bar.',
        'FGM Roundness and sphericity',
        partial(roundness_class, 2),
    ),
    (
        'gl_roundness_subrounded',
        'Roundness: Subrounded',
        'High-sphericity and low-sphericity clasts with smoothed edges and remnants of flat faces above a six-step roundness bar.',
        'FGM Roundness and sphericity',
        partial(roundness_class, 3),
    ),
    (
        'gl_roundness_rounded',
        'Roundness: Rounded',
        'High-sphericity and low-sphericity pebbles with smooth convex outlines above a six-step roundness bar.',
        'FGM Roundness and sphericity',
        partial(roundness_class, 4),
    ),
    (
        'gl_roundness_well_rounded',
        'Roundness: Well-Rounded',
        'High-sphericity oval and low-sphericity capsule pebbles with completely smooth, symmetrical curves above a six-step roundness bar.',
        'FGM Roundness and sphericity',
        partial(roundness_class, 5),
    ),
    (
        'gl_grain_percent_01',
        'Grain Percentage: 1%',
        'Circular petrographic field of view containing angular grains covering 1% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 1),
    ),
    (
        'gl_grain_percent_02',
        'Grain Percentage: 2%',
        'Circular petrographic field of view containing angular grains covering 2% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 2),
    ),
    (
        'gl_grain_percent_03',
        'Grain Percentage: 3%',
        'Circular petrographic field of view containing angular grains covering 3% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 3),
    ),
    (
        'gl_grain_percent_05',
        'Grain Percentage: 5%',
        'Circular petrographic field of view containing angular grains covering 5% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 5),
    ),
    (
        'gl_grain_percent_07',
        'Grain Percentage: 7%',
        'Circular petrographic field of view containing angular grains covering 7% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 7),
    ),
    (
        'gl_grain_percent_10',
        'Grain Percentage: 10%',
        'Circular petrographic field of view containing angular grains covering 10% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 10),
    ),
    (
        'gl_grain_percent_15',
        'Grain Percentage: 15%',
        'Circular petrographic field of view containing angular grains covering 15% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 15),
    ),
    (
        'gl_grain_percent_20',
        'Grain Percentage: 20%',
        'Circular petrographic field of view containing angular grains covering 20% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 20),
    ),
    (
        'gl_grain_percent_25',
        'Grain Percentage: 25%',
        'Circular petrographic field of view containing angular grains covering 25% of the area with a quarter-circle sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 25),
    ),
    (
        'gl_grain_percent_30',
        'Grain Percentage: 30%',
        'Circular petrographic field of view containing angular grains covering 30% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 30),
    ),
    (
        'gl_grain_percent_40',
        'Grain Percentage: 40%',
        'Circular petrographic field of view containing angular grains covering 40% of the area with a fractional sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 40),
    ),
    (
        'gl_grain_percent_50',
        'Grain Percentage: 50%',
        'Circular petrographic field of view containing angular grains covering 50% of the area with a half-circle sector gauge.',
        'FGM 2.6 Diagrams representing percentages of grains',
        partial(grain_percent_chart, 50),
    ),
    (
        'gl_unit_stratotype',
        'Unit Stratotype',
        'Dipping sedimentary landscape section where a lithostratigraphic formation is bracketed between two boundary marker arrows.',
        'FGM Stratotypes',
        unit_stratotype,
    ),
    (
        'gl_boundary_stratotype',
        'Boundary Stratotype',
        'Stepped outcrop succession of dipping beds with a boundary marker arrow pointing to the contact horizon between two stages.',
        'FGM Stratotypes',
        boundary_stratotype,
    ),
    (
        'gl_earthquake_magnitude_energy',
        'Earthquake Magnitude vs Energy',
        'Three radially shaded spheres of exponentially increasing volume comparing seismic energy release across successive magnitudes.',
        'FGM 9.9 Earthquake magnitude and intensity',
        earthquake_magnitude_energy,
    ),
]
