"""FGM structural geology icons: fold attitudes, vergence, dip isogons, stereonets.

Reference: Berkman, D. A. (ed.) Field Geologists' Manual, 4th edition,
Australasian Institute of Mining and Metallurgy (AusIMM) Monograph 9,
Sections 5.1, 5.10, 5.14.21, 5.15, 6.10.
"""
import math
from functools import partial
from shapely.geometry import LineString, Point, Polygon, box

from fgm_common import (
    FieldDrawing, INK, STEEL, ALU, GRID, PAPER, WHITE,
    QUARTZ, LIMESTONE, DOLOMITE, SANDSTONE, CONGLOMERATE,
    SHALE, MUDSTONE, SLATE, SCHIST, COAL, GOSSAN, WATER, GLASS,
    LOESS, TUFF, ellipse_points, smooth, smooth_closed, swatch,
)


# ---------------------------------------------------------------------------
# 1-8. Fold Attitude Block Diagrams (FGM 5.1, ref/08.png)
# ---------------------------------------------------------------------------

def _box_point(u, v, w):
    """Map normalized 3D block coordinates (u, v, w) in [0, 1]^3 to 2D canvas.

    u: 0..1 along front-right cross-section face (from front vertical edge to right edge)
    v: 0..1 along front-left face (from front vertical edge to back-left edge)
    w: 0..1 vertically from bottom (0) to top (1)
    """
    x = 21.0 + 22.0 * u - 16.0 * v
    y = 41.0 - 7.0 * u - 7.0 * v - 22.0 * w
    return (x, y)


def _draw_box_back(d):
    """Subtle block background and rear wireframe edges."""
    p000 = _box_point(0, 0, 0)
    p100 = _box_point(1, 0, 0)
    p101 = _box_point(1, 0, 1)
    p111 = _box_point(1, 1, 1)
    p011 = _box_point(0, 1, 1)
    p010 = _box_point(0, 1, 0)
    p110 = _box_point(1, 1, 0)
    hull = [p000, p100, p101, p111, p011, p010]
    d.poly(hull, PAPER, STEEL)
    d.line([p010, p110, p100], GRID, .55)
    d.line([p110, p111], GRID, .55)


def _draw_box_front(d):
    """Foreground wireframe edges of the reference block."""
    p000 = _box_point(0, 0, 0)
    p001 = _box_point(0, 0, 1)
    p100 = _box_point(1, 0, 0)
    p101 = _box_point(1, 0, 1)
    p111 = _box_point(1, 1, 1)
    p011 = _box_point(0, 1, 1)
    p010 = _box_point(0, 1, 0)
    d.line([p011, p001, p101], STEEL, .7)
    d.line([p001, p000], STEEL, .7)
    d.line([p010, p011, p111, p101, p100, p000, p010], INK, .85)


def _axial_plane(d, points, angle=90, spacing=1.85):
    """Draw a hatched axial surface polygon."""
    poly = Polygon(points).buffer(0)
    d.shape(poly, QUARTZ, INK, width=.8)
    d.hatch(poly.buffer(-.25), angle=angle, spacing=spacing, colour=INK, width=.52)


def _bold_band(d, outer_pts, inner_pts=None, fill=COAL, width=2.2):
    """Draw the bold folded marker bed cut edge on the block faces."""
    if inner_pts is not None:
        poly = Polygon(list(outer_pts) + list(reversed(inner_pts))).buffer(0)
    else:
        poly = LineString(outer_pts).buffer(width / 2, cap_style=2, join_style=2)
    d.shape(poly, fill, INK)


def fold_attitude(kind):
    d = FieldDrawing()
    _draw_box_back(d)
    P = _box_point

    if kind == 'upright_horizontal':
        # Right 3D limb surface (behind crest)
        d.poly([P(.48, 0, .95), P(.48, 1, .95), P(1, 1, 0), P(1, 0, 0)], LIMESTONE, INK)
        # Core under arch on front-right face: vertical hatched axial surface
        _axial_plane(d, [P(.48, 0, .92), P(.48, 0, 0), P(.88, 0, 0), P(.88, 0, .22)], angle=90)
        d.line([P(.48, 0, .92), P(.48, 0, 0)], INK, .95)
        # Left 3D limb surface (SANDSTONE) extending horizontally from front to back
        d.poly([P(0, 0, 0), P(.48, 0, .95), P(.48, 1, .95), P(0, 1, 0)], SANDSTONE, INK)
        # Bold marker bed cross-section on front-right face
        _bold_band(
            d,
            [P(0, 0, 0), P(.48, 0, .95), P(1, 0, 0)],
            [P(.09, 0, 0), P(.48, 0, .77), P(.91, 0, 0)],
        )

    elif kind == 'upright_plunging':
        # Vertical axial plane protruding above plunging hinge in back-left
        _axial_plane(d, [P(.48, .22, .94), P(.48, 1, .94), P(.48, 1, .32), P(.48, .22, .94)], angle=90)
        # Right 3D limb surface
        d.poly([P(.48, .22, .94), P(.82, .22, .90), P(1, 0, 0), P(.48, 0, .86)], LIMESTONE, INK)
        # Vertical hatched axial plane inside the front-right arch
        _axial_plane(d, [P(.48, 0, .84), P(.48, 0, 0), P(.90, 0, 0), P(.78, 0, .84)], angle=90)
        d.line([P(.48, 0, .86), P(.48, 0, 0)], INK, .95)
        # Left plunging 3D limb surface (SANDSTONE)
        d.poly([P(0, 0, 0), P(.48, 0, .86), P(.48, .22, .94), P(.48, 1, .32), P(0, 1, 0)], SANDSTONE, INK)
        # Bold marker bed cut edge on front-right and top faces
        _bold_band(
            d,
            [P(0, 0, 0), P(.48, 0, .86), P(.48, .22, .94), P(.82, .22, .90), P(1, 0, 0)],
            [P(.09, 0, 0), P(.48, 0, .68), P(.53, .16, .82), P(.75, .16, .79), P(.91, 0, 0)],
        )

    elif kind == 'vertical':
        # Back-right limb inner wall
        d.poly([P(.32, .35, 1), P(.48, 1, 1), P(1, 0, 1), P(1, 0, 0), P(.32, .35, 0)], LIMESTONE, INK)
        # Vertical axial plane with vertical hinge and vertical hatching
        _axial_plane(d, [P(.32, .35, 1), P(.82, .35, 1), P(.82, .35, 0), P(.32, .35, 0)], angle=90)
        # Front-left limb vertical wall (SANDSTONE) closing at vertical hinge
        d.poly([P(.32, .35, 1), P(.32, .35, 0), P(0, 1, .35), P(0, 1, 1)], SANDSTONE, INK)
        # Bold marker bed on top face (horizontal V-closure) + vertical hinge column + right vertical edge
        _bold_band(
            d,
            [P(.48, 1, 1), P(.24, .32, 1), P(1, 0, 1)],
            [P(.58, 1, 1), P(.37, .36, 1), P(.90, 0, 1)],
        )
        _bold_band(
            d,
            [P(.24, .32, 1), P(.24, .32, 0)],
            [P(.35, .32, 1), P(.35, .32, 0)],
        )
        _bold_band(
            d,
            [P(.92, 0, 1), P(.92, 0, 0)],
            [P(1.0, 0, 1), P(1.0, 0, 0)],
        )

    elif kind == 'inclined_plunging':
        # Inclined axial plane sticking up above plunging limb (tilted hatching angle=62)
        _axial_plane(
            d,
            [P(.56, .20, .94), P(.56, 1, .94), P(.22, 1, .18), P(.22, .20, .38)],
            angle=62,
        )
        # Steep right limb 3D surface
        d.poly([P(.56, .20, .94), P(.82, .20, .88), P(1, 0, 0), P(.56, 0, .84)], LIMESTONE, INK)
        # Inclined hatched axial plane inside the front-right arch
        _axial_plane(
            d,
            [P(.56, 0, .84), P(.22, 0, 0), P(.90, 0, 0), P(.78, 0, .80)],
            angle=62,
        )
        d.line([P(.56, 0, .84), P(.22, 0, 0)], INK, .95)
        # Asymmetric gently-dipping plunging left limb (SANDSTONE)
        d.poly(
            [P(0, 0, .12), P(.35, 0, .32), P(.56, 0, .84), P(.56, .20, .94), P(.22, 1, .18), P(0, .75, .12)],
            SANDSTONE, INK,
        )
        # Bold marker bed cut edge
        _bold_band(
            d,
            [P(0, 0, .12), P(.35, 0, .32), P(.56, 0, .84), P(.56, .20, .94), P(.82, .20, .88), P(1, 0, 0)],
            [P(.06, 0, .04), P(.41, 0, .24), P(.58, 0, .68), P(.60, .14, .81), P(.76, .14, .77), P(.91, 0, 0)],
        )

    elif kind == 'overturned_horizontal':
        # Overturned lower limb in background
        d.poly([P(.96, 0, .74), P(.76, 0, 0), P(.76, 1, 0), P(.96, 1, .74)], LIMESTONE, INK)
        # Moderately inclined hatched axial plane (dipping ~35 deg to left)
        _axial_plane(
            d,
            [P(.96, 0, .74), P(0, 0, .12), P(.38, 0, 0), P(.76, 0, 0)],
            angle=36,
        )
        d.line([P(.96, 0, .74), P(0, 0, .12)], INK, .95)
        # Upper normal limb 3D surface (SANDSTONE) dipping gently left, hinge horizontal
        d.poly([P(0, 0, .42), P(.96, 0, .74), P(.96, 1, .74), P(0, 1, .42)], SANDSTONE, INK)
        # Bold overturned marker bed on front-right and front-left faces (both limbs dip left!)
        _bold_band(
            d,
            [P(0, 1, .42), P(0, 0, .42), P(.96, 0, .74), P(.76, 0, 0)],
            [P(0, 1, .32), P(0, 0, .32), P(.84, 0, .60), P(.66, 0, 0)],
        )

    elif kind == 'overturned_plunging':
        # Inclined axial plane above the plunging upper limb
        _axial_plane(
            d,
            [P(.58, .22, .94), P(.58, 1, .94), P(.15, 1, .16), P(.15, .22, .35)],
            angle=45,
        )
        # Steep overturned right limb (dipping left, same direction as left limb!)
        d.poly([P(.58, .22, .94), P(.94, .22, .90), P(.76, 0, 0), P(.58, 0, .82)], LIMESTONE, INK)
        # Inclined hatched axial plane inside the overturned arch
        _axial_plane(
            d,
            [P(.58, 0, .82), P(0, 0, 0), P(.76, 0, 0), P(.86, .15, .80)],
            angle=45,
        )
        d.line([P(.58, 0, .82), P(0, 0, 0)], INK, .95)
        # Plunging upper limb surface (SANDSTONE)
        d.poly(
            [P(0, 0, .10), P(.38, 0, .35), P(.58, 0, .82), P(.58, .22, .94), P(.15, 1, .16), P(0, .72, .10)],
            SANDSTONE, INK,
        )
        # Bold marker bed edge (both limbs dip left + plunging S-hook at top)
        _bold_band(
            d,
            [P(0, 0, .10), P(.38, 0, .35), P(.58, 0, .82), P(.58, .22, .94), P(.94, .22, .90), P(.76, 0, 0)],
            [P(.06, 0, .02), P(.44, 0, .27), P(.62, 0, .68), P(.64, .16, .82), P(.84, .16, .79), P(.66, 0, 0)],
        )

    elif kind == 'recumbent':
        # Lower inverted limb surface
        d.poly([P(0, 0, 0), P(.98, 0, .50), P(.98, 1, .50), P(0, 1, 0)], LIMESTONE, INK)
        # Horizontal hatched axial plane slicing across the middle of the recumbent fold
        _axial_plane(
            d,
            [P(0, 0, .50), P(.98, 0, .50), P(.98, 1, .50), P(0, 1, .50)],
            angle=22,
        )
        # Upper horizontal limb surface (SANDSTONE) at the top of the front-left/right faces
        d.shape(Polygon([P(0, 0, .92), P(.98, 0, .50), P(.98, 1, .50), P(0, 1, .92)]).buffer(0), SANDSTONE, INK)
        # Bold recumbent marker bed closing sideways at the right edge
        _bold_band(
            d,
            [P(0, 1, .92), P(0, 0, .92), P(.98, 0, .50), P(0, 0, 0), P(0, 1, 0)],
            [P(0, 1, .82), P(0, 0, .82), P(.84, 0, .50), P(0, 0, .11), P(0, 1, .11)],
        )

    elif kind == 'reclined':
        # Lower/right inclined limb surface from front-bottom up to top-right
        d.poly([P(0, 0, 0), P(.98, 0, .94), P(.28, .28, .85), P(0, 1, .45)], LIMESTONE, INK)
        # Moderately dipping axial surface hatched along strike/dip, hinge pitching 90 deg down dip
        _axial_plane(
            d,
            [P(.98, 0, .94), P(.28, .28, .85), P(0, 1, .45), P(0, 0, 0)],
            angle=24,
        )
        # Upper back limb surface
        d.poly([P(.98, 0, .94), P(.45, 1, .96), P(.28, .28, .85)], SANDSTONE, INK)
        # Bold marker bed tracing the reclined sideways closure and down-dip limbs
        _bold_band(
            d,
            [P(.98, 0, .94), P(.28, .28, .85), P(0, 1, .45), P(0, 0, 0), P(.98, 0, .94)],
            [P(.86, 0, .84), P(.35, .24, .75), P(.08, .86, .42), P(.08, 0, .12), P(.86, 0, .84)],
        )

    _draw_box_front(d)
    return d


# ---------------------------------------------------------------------------
# 9. Monocline (FGM 5.1, ref/08.png)
# ---------------------------------------------------------------------------

def gl_monocline():
    """Oblique block diagram of a monocline: local steepening of horizontal strata."""
    d = FieldDrawing()
    ox, oy = 9.0, -7.0

    def front_curve(y_left, y_right):
        pts = []
        for i in range(33):
            t = i / 32.0
            x = 5.0 + 30.0 * t
            # Smooth local steepening between t=0.35 and t=0.65
            s = 0.5 * (1.0 + math.tanh((t - 0.5) * 7.5))
            y = y_left + (y_right - y_left) * s
            pts.append((x, y))
        return pts

    top_bed = front_curve(16.0, 26.5)
    mid_bed = front_curve(21.5, 32.0)
    bot_bed = front_curve(27.5, 38.0)
    base_line = [(35.0, 42.0), (5.0, 42.0)]

    # 3D upper surface of the top bed (receding by ox, oy)
    top_back = [(x + ox, y + oy) for x, y in top_bed]
    d.poly(top_bed + list(reversed(top_back)), LIMESTONE, INK)
    # Dip-slope flexure ruling on the monoclinal ramp of the top face
    for idx in (12, 15, 18, 21):
        x0, y0 = top_bed[idx]
        d.line([(x0, y0), (x0 + ox, y0 + oy)], STEEL, .55)

    # Right side face of the 3D block
    r_top = top_bed[-1]
    r_mid = mid_bed[-1]
    r_bot = bot_bed[-1]
    r_base = (35.0, 42.0)
    d.poly([r_top, (r_top[0] + ox, r_top[1] + oy), (r_mid[0] + ox, r_mid[1] + oy), r_mid], DOLOMITE, INK)
    d.poly([r_mid, (r_mid[0] + ox, r_mid[1] + oy), (r_bot[0] + ox, r_bot[1] + oy), r_bot], LOESS, INK)
    d.poly([r_bot, (r_bot[0] + ox, r_bot[1] + oy), (r_base[0] + ox, r_base[1] + oy), r_base], MUDSTONE, INK)

    # Front cross-section strata layers
    d.poly(top_bed + list(reversed(mid_bed)), LIMESTONE, INK)
    d.poly(mid_bed + list(reversed(bot_bed)), SANDSTONE, INK)
    d.poly(bot_bed + base_line, SHALE, INK)

    # Dashed monoclinal axial traces at upper and lower knees + upward-facing arrow
    d.dashed([(15.5, 11.0), (19.5, 42.0)], INK, .65, dash=1.8, gap=1.2)
    d.dashed([(21.0, 14.0), (25.0, 42.0)], INK, .65, dash=1.8, gap=1.2)
    d.text_free_arrow(9.5, 21.0, 9.5, 11.5, INK, .85, head=2.4)
    return d


# ---------------------------------------------------------------------------
# 10. Fold Vergence (FGM 5.15, ref/09.png)
# ---------------------------------------------------------------------------

def gl_fold_vergence():
    """Antiform with Z, M and S parasitic minor folds, axial trace and vergence arrows."""
    d = FieldDrawing()

    # Construct parasitic minor folds along a major antiform arch
    # Left limb: Z-fold; Hinge crest: symmetric M-fold; Right limb: S-fold
    outer_ctrl = [
        (6.0, 41.0), (8.5, 31.0),
        # Left Z-parasitic fold
        (10.5, 23.0), (14.5, 26.5), (15.0, 16.5),
        # Central M-parasitic fold at hinge
        (19.5, 10.5), (21.8, 14.5), (24.0, 9.5), (26.2, 14.5), (28.5, 10.5),
        # Right S-parasitic fold
        (33.0, 16.5), (33.5, 26.5), (37.5, 23.0),
        (39.5, 31.0), (42.0, 41.0),
    ]
    inner_ctrl = [
        (11.0, 41.0), (13.0, 33.0),
        # Left Z-parasitic fold inner
        (14.2, 27.5), (18.0, 30.8), (18.5, 21.0),
        # Central M-parasitic fold inner
        (21.2, 16.2), (22.6, 19.2), (24.0, 15.2), (25.4, 19.2), (26.8, 16.2),
        # Right S-parasitic fold inner
        (29.5, 21.0), (30.0, 30.8), (33.8, 27.5),
        (35.0, 33.0), (37.0, 41.0),
    ]
    outer = smooth(outer_ctrl, iterations=2)
    inner = smooth(inner_ctrl, iterations=2)

    # Core fill below the inner arc
    d.poly(inner + [(11.0, 41.0)], LIMESTONE, INK)
    # Folded marker bed with Z / M / S parasitic folds
    d.poly(outer + list(reversed(inner)), SANDSTONE, INK)
    d.line([(4.5, 41.0), (43.5, 41.0)], INK, .85)

    # Axial trace down the centre with upward arrowhead at top (FGM 5.15)
    d.line([(24.0, 42.5), (24.0, 7.0)], INK, .85)
    d.text_free_arrow(24.0, 9.0, 24.0, 4.5, INK, .85, head=2.5)

    # Vergence arrows on left and right limbs pointing toward the antiform closure
    d.text_free_arrow(14.5, 37.5, 19.5, 26.5, INK, .9, head=2.5)
    d.text_free_arrow(33.5, 37.5, 28.5, 26.5, INK, .9, head=2.5)
    return d


# ---------------------------------------------------------------------------
# 11. Superposed Folds (FGM 5.14.21 & 5.15, ref/09.png)
# ---------------------------------------------------------------------------

def gl_superposed_folds():
    """Map swatch showing boomerang/crescent fold interference of a stippled marker bed."""
    d = FieldDrawing()
    region = swatch(d, LIMESTONE, x=4, y=7, width=40, height=34, radius=1.5)

    with d.clipped(region):
        # Classic Ramsay Type 2 boomerang / mushroom refolded marker bed (ref/09.png)
        outer_loop = smooth_closed([
            (9.0, 14.0), (17.0, 10.5), (28.0, 12.5), (37.5, 19.0),
            (39.0, 28.0), (33.0, 31.5), (27.5, 25.5), (20.5, 22.0),
            (16.5, 25.5), (22.0, 32.5), (17.5, 37.5), (10.0, 33.5),
            (7.5, 24.0),
        ], iterations=3)
        inner_core = smooth_closed([
            (13.0, 16.5), (18.5, 14.0), (27.0, 15.8), (34.2, 20.5),
            (35.0, 26.2), (31.8, 27.5), (26.5, 21.5), (19.5, 18.2),
            (13.2, 22.5), (17.5, 31.5), (15.2, 33.8), (12.0, 30.5),
            (10.8, 23.0),
        ], iterations=3)
        d.poly(outer_loop, SANDSTONE, INK)
        d.poly(inner_core, SHALE, INK)

        # Stipple dots inside the SANDSTONE marker bed (matching FGM 5.15 "Marker bed")
        marker_ring = Polygon(outer_loop).difference(Polygon(inner_core))
        for gx in range(8, 40, 3):
            for gy in range(10, 39, 3):
                pt = Point(gx + (1.2 if (gy // 3) % 2 else 0), gy)
                if marker_ring.buffer(-.6).contains(pt):
                    d.circle(pt.x, pt.y, .38, INK, INK, True)

        # Early F1 curved axial trace + late F2 straight dashed axial trace
        f1_trace = smooth([(14.0, 35.5), (11.5, 23.5), (17.5, 14.8), (28.0, 16.5), (35.5, 25.0)], 2)
        d.dashed(f1_trace, INK, .65, dash=2.0, gap=1.3)
        d.dashed([(7.0, 36.0), (41.0, 12.0)], INK, .85, dash=2.2, gap=1.4)
        # Opposing synform/antiform ticks across F2 axial trace
        d.text_free_arrow(24.5, 18.0, 27.2, 21.8, INK, .75, head=2.0)
        d.text_free_arrow(31.5, 27.8, 28.8, 24.0, INK, .75, head=2.0)

    return d


# ---------------------------------------------------------------------------
# 12-16. Classification of Folds by Dip Isogons (FGM 5.10, ref/17.png)
# ---------------------------------------------------------------------------

def _parabola_arch(x_crest, y_crest, half_width, y_base=41.0, power=2.0, steps=48):
    pts = []
    for i in range(steps + 1):
        u = -1.0 + 2.0 * i / steps
        x = x_crest + half_width * u
        y = y_crest + (y_base - y_crest) * (abs(u) ** power)
        pts.append((x, y))
    return pts


def fold_isogon_class(cls):
    d = FieldDrawing()
    y_base = 41.0
    cx = 24.0

    if cls == '1a':
        # Class 1A (Strongly convergent): thin hinge, thick flaring limbs; isogons strongly convergent
        outer = _parabola_arch(cx, 8.0, 18.5, y_base, power=1.85)
        inner = _parabola_arch(cx, 13.8, 7.8, y_base, power=1.75)
        d.poly(inner + [(cx - 7.8, y_base)], QUARTZ, INK)
        d.poly(outer + list(reversed(inner)), SANDSTONE, INK)
        pairs = [
            ((20.8, 9.0), (23.0, 14.2)),
            ((17.5, 11.5), (21.8, 15.8)),
            ((14.0, 16.0), (20.4, 18.8)),
            ((10.2, 22.8), (18.8, 24.8)),
        ]

    elif cls == '1b':
        # Class 1B (Parallel / concentric): constant orthogonal thickness, radial normal isogons
        yc = 24.5
        r_out, r_in = 16.5, 8.0
        outer, inner = [], []
        for i in range(49):
            ang = math.radians(-168 + 156 * i / 48)
            outer.append((cx + r_out * math.cos(ang), yc + r_out * math.sin(ang)))
            inner.append((cx + r_in * math.cos(ang), yc + r_in * math.sin(ang)))
        outer = [(5.8, y_base)] + outer + [(42.2, y_base)]
        inner = [(14.5, y_base)] + inner + [(33.5, y_base)]
        d.poly(inner + [(14.5, y_base)], QUARTZ, INK)
        d.poly(outer + list(reversed(inner)), SANDSTONE, INK)
        pairs = []
        for deg in (16, 33, 50, 67):
            rad = math.radians(deg)
            p_out = (cx - r_out * math.sin(rad), yc - r_out * math.cos(rad))
            p_in = (cx - r_in * math.sin(rad), yc - r_in * math.cos(rad))
            pairs.append((p_out, p_in))
        # Subtle dashed radii inside core converging to the centre of curvature
        for deg in (-50, -16, 16, 50):
            rad = math.radians(deg)
            d.dashed([(cx - r_in * math.sin(rad), yc - r_in * math.cos(rad)), (cx, yc)], STEEL, .48, 1.4, 1.1)
        d.circle(cx, yc, .85, INK, INK, True)

    elif cls == '1c':
        # Class 1C (Weakly convergent): moderately thickened hinge, weakly convergent isogons
        outer = _parabola_arch(cx, 7.5, 15.5, y_base, power=2.0)
        inner = _parabola_arch(cx, 17.5, 9.5, y_base, power=2.0)
        d.poly(inner + [(cx - 9.5, y_base)], QUARTZ, INK)
        d.poly(outer + list(reversed(inner)), SANDSTONE, INK)
        pairs = [
            ((21.5, 8.4), (22.3, 18.3)),
            ((19.0, 11.0), (20.5, 20.8)),
            ((16.2, 15.5), (18.5, 25.0)),
            ((13.2, 21.8), (16.4, 30.8)),
        ]

    elif cls == '2':
        # Class 2 (Similar): identical curves shifted vertically, strictly vertical parallel isogons
        shift = 11.5
        outer = _parabola_arch(cx, 7.0, 14.5, y_base, power=2.0)
        inner = []
        for i in range(49):
            u = -1.0 + 2.0 * i / 48
            x = cx + 10.9 * u
            y = (7.0 + shift) + (y_base - 7.0) * ((abs(x - cx) / 14.5) ** 2.0)
            inner.append((x, y))
        d.poly(inner + [(cx - 10.9, y_base)], QUARTZ, INK)
        d.poly(outer + list(reversed(inner)), SANDSTONE, INK)
        pairs = []
        for dx in (2.2, 4.5, 6.8, 9.2):
            y_o = 7.0 + (y_base - 7.0) * ((dx / 14.5) ** 2.0)
            y_i = y_o + shift
            pairs.append(((cx - dx, y_o), (cx - dx, y_i)))

    elif cls == '3':
        # Class 3 (Divergent): very thick hinge, thin pinched limbs; isogons diverge downward
        outer = _parabola_arch(cx, 6.8, 12.8, y_base, power=2.1)
        inner = _parabola_arch(cx, 20.5, 11.0, y_base, power=1.7)
        d.poly(inner + [(cx - 11.0, y_base)], QUARTZ, INK)
        d.poly(outer + list(reversed(inner)), SANDSTONE, INK)
        pairs = [
            ((22.4, 7.3), (21.2, 21.8)),
            ((20.8, 8.8), (18.4, 24.5)),
            ((19.0, 11.6), (15.6, 28.5)),
            ((17.0, 15.8), (13.2, 33.5)),
        ]

    # Draw the symmetric pairs of dip isogons across the layer
    for (x0, y0), (x1, y1) in pairs:
        d.line([(x0, y0), (x1, y1)], INK, .68)
        d.line([(2 * cx - x0, y0), (2 * cx - x1, y1)], INK, .68)

    # Vertical axial trace and horizontal baseline (ref/17.png)
    d.line([(cx, outer[len(outer) // 2][1]), (cx, y_base)], INK, .75)
    d.line([(4.5, y_base), (43.5, y_base)], INK, .85)
    return d


# ---------------------------------------------------------------------------
# 17. Construction of Dip Isogons (FGM 5.10, ref/17.png top)
# ---------------------------------------------------------------------------

def gl_dip_isogon_construction():
    """Inclined fold with equal-dip tangent lines, joined dip isogon and protractor."""
    d = FieldDrawing()

    # Horizontal reference datum line across the diagram
    d.line([(4.0, 26.0), (44.0, 26.0)], STEEL, .65)

    # Tilted half-circle protractor on the left (ref/17.png 'a')
    px, py, pr = 19.0, 26.0, 14.0
    tilt = 80.0  # protractor base tilted at 80 deg
    arc_pts = ellipse_points(px, py, pr, pr, start=tilt + 90, stop=tilt + 270, steps=36)
    prot_poly = Polygon(arc_pts)
    d.shape(prot_poly, GLASS, INK, width=.85)
    # Degree tick marks along inside rim of protractor
    for ang in range(int(tilt + 105), int(tilt + 260), 15):
        rad = math.radians(ang)
        d.line([
            (px + pr * math.cos(rad), py + pr * math.sin(rad)),
            (px + (pr - 1.8) * math.cos(rad), py + (pr - 1.8) * math.sin(rad)),
        ], INK, .55)

    # Inclined folded layer on the right (SANDSTONE)
    outer_fold = smooth([
        (17.8, 20.5), (27.5, 13.5), (37.5, 8.5), (42.5, 10.0), (40.5, 22.0), (33.5, 42.0),
    ], 3)
    inner_fold = smooth([
        (18.6, 24.5), (27.5, 18.2), (34.2, 16.5), (36.8, 19.5), (34.8, 28.0), (29.0, 42.0),
    ], 3)
    d.poly(outer_fold + list(reversed(inner_fold)), SANDSTONE, INK)

    # Protractor radial angle line + two parallel tangent lines of equal dip (-20 deg)
    slope_ang = math.radians(-18.0)
    ux, uy = math.cos(slope_ang), math.sin(slope_ang)
    # Protractor ray at -18 deg (showing dip measurement from horizontal)
    d.line([(px, py), (px - pr * ux, py - pr * uy)], INK, .7)
    d.arc(px, py, 9.5, 162, 180, INK)

    # Outer tangent line touching outer arc at (34.5, 9.4) and inner tangent touching (31.5, 16.9)
    t_out = (34.8, 9.3)
    t_in = (31.6, 17.0)
    d.line([(t_out[0] - 15 * ux, t_out[1] - 15 * uy), (t_out[0] + 9 * ux, t_out[1] + 9 * uy)], STEEL, .65)
    d.line([(t_in[0] - 13 * ux, t_in[1] - 13 * uy), (t_in[0] + 11 * ux, t_in[1] + 11 * uy)], STEEL, .65)

    # Constructed dip isogon connecting the two tangent points + hinge isogon fan
    d.line([t_out, t_in], INK, 1.05)
    d.circle(t_out[0], t_out[1], .9, INK, INK, True)
    d.circle(t_in[0], t_in[1], .9, INK, INK, True)
    for (x0, y0), (x1, y1) in [
        ((37.5, 8.8), (33.6, 16.6)),
        ((40.2, 9.2), (35.4, 17.4)),
        ((41.8, 11.2), (36.4, 19.2)),
    ]:
        d.line([(x0, y0), (x1, y1)], INK, .6)

    return d


# ---------------------------------------------------------------------------
# 18-19. Triangular Grid & Classification for Fold Attitudes (FGM 5.10, ref/18.png)
# ---------------------------------------------------------------------------

def _tri_point(s_left, s_right, u):
    """Interpolate across the fold-attitude triangle (top=(24,5), bl=(5,41), br=(43,41)).

    s_left: fraction up the left edge from bottom-left (0) to top (1)
    s_right: fraction up the right edge from bottom-right (0) to top (1)
    u: horizontal parameter across the triangle from left edge (0) to right edge (1)
    """
    xl = 5.0 + (24.0 - 5.0) * s_left
    yl = 41.0 + (5.0 - 41.0) * s_left
    xr = 43.0 + (24.0 - 43.0) * s_right
    yr = 41.0 + (5.0 - 41.0) * s_right
    return (xl + (xr - xl) * u, yl + (yr - yl) * u)


def _plunge_curve(frac, steps=32):
    """Curved iso-plunge line connecting fraction `frac` on left and right edges (bowing down)."""
    pts = []
    for i in range(steps + 1):
        u = i / steps
        x, y = _tri_point(frac, frac, u)
        # Downward bow proportional to frac * (1 - frac * 0.3) * 4*u*(1-u)
        bow = 12.5 * frac * (1.0 - 0.35 * frac) * 4.0 * u * (1.0 - u)
        pts.append((x, y + bow))
    return pts


def _pitch_curve(frac_left, steps=28, stop_u=0.92):
    """Curved iso-pitch ray from `frac_left` on left edge to bottom-right vertex (43, 41)."""
    pts = []
    for i in range(steps + 1):
        u = stop_u * i / steps
        x, y = _tri_point(frac_left, 0.0, u)
        bow = 5.5 * frac_left * (1.0 - frac_left) * 4.0 * u * (1.0 - u)
        pts.append((x, y + bow))
    return pts


def gl_fold_attitude_grid():
    """Fleuty/Rickard triangular coordinate grid for plotting fold attitudes."""
    d = FieldDrawing()
    v_top, v_bl, v_br = (24.0, 5.0), (5.0, 41.0), (43.0, 41.0)
    tri = Polygon([v_top, v_bl, v_br])
    d.shape(tri, PAPER, INK, width=.95)

    with d.clipped(tri.buffer(-.3)):
        # 1. Iso-Dip lines: straight lines parallel to the left edge
        for f in (0.18, 0.36, 0.54, 0.72, 0.86):
            x_bot = 43.0 - 38.0 * f
            x_right = 43.0 + (24.0 - 43.0) * f
            y_right = 41.0 + (5.0 - 41.0) * f
            d.line([(x_bot, 41.0), (x_right, y_right)], STEEL, .55)

        # 2. Iso-Plunge curves: downward-bowing curves between left and right edges
        for f in (0.18, 0.36, 0.54, 0.72, 0.86):
            d.line(_plunge_curve(f), INK, .58)

        # 3. Iso-Pitch curves: sweeping from left edge toward bottom-right corner
        for f in (0.18, 0.36, 0.54, 0.72, 0.86):
            d.line(_pitch_curve(f, stop_u=0.92), INK, .58)

    # Re-stroke outer triangle frame and exterior graduation ticks
    d.poly([v_top, v_bl, v_br], None, INK)
    for f in (0.18, 0.36, 0.54, 0.72, 0.86):
        # Left edge ticks
        xl, yl = _tri_point(f, 0, 0)
        d.line([(xl, yl), (xl - 1.3, yl - 0.6)], INK, .6)
        # Right edge ticks
        xr, yr = _tri_point(0, f, 1)
        d.line([(xr, yr), (xr + 1.3, yr - 0.6)], INK, .6)
        # Bottom edge ticks
        xb = 5.0 + 38.0 * f
        d.line([(xb, 41.0), (xb, 42.5)], INK, .6)
    return d


def gl_fold_attitude_classification():
    """Fold-attitude classification triangle with shaded corner fields and marginal bands."""
    d = FieldDrawing()
    v_top, v_bl, v_br = (24.0, 5.0), (5.0, 41.0), (43.0, 41.0)
    tri = Polygon([v_top, v_bl, v_br])
    d.shape(tri, PAPER, INK, width=.95)

    # Marginal bands (Upright on left, Horizontal at bottom, Reclined on right)
    f_edge = 0.84
    plunge_low = _plunge_curve(0.14)
    plunge_high = _plunge_curve(0.82)
    pitch_high = _pitch_curve(0.82, stop_u=1.0)

    with d.clipped(tri):
        # Marginal bands tinted QUARTZ
        upright_band = Polygon([
            v_bl, v_top,
            (43.0 + (24.0 - 43.0) * f_edge, 41.0 + (5.0 - 41.0) * f_edge),
            (43.0 - 38.0 * f_edge, 41.0),
        ])
        horiz_band = Polygon(plunge_low + [v_br, v_bl])
        reclined_band = Polygon(pitch_high + [v_top])
        for band in (upright_band, horiz_band, reclined_band):
            d.shape(band.intersection(tri), QUARTZ, INK, width=.7)

        # Three shaded corner fields (Vertical folds, Horizontal upright folds, Recumbent folds)
        vert_cap = Polygon([v_top] + plunge_high).intersection(tri)
        horiz_upright_corner = upright_band.intersection(horiz_band).intersection(tri)
        recumbent_corner = Polygon([
            (43.0 - 38.0 * 0.15, 41.0),
            (43.0 + (24.0 - 43.0) * 0.15, 41.0 + (5.0 - 41.0) * 0.15),
            v_br,
        ]).intersection(tri)

        for corner in (vert_cap, horiz_upright_corner, recumbent_corner):
            d.shape(corner, SANDSTONE, INK, width=.8)

        # Redraw main internal classification boundary lines crisp on top
        d.line([
            (43.0 - 38.0 * f_edge, 41.0),
            (43.0 + (24.0 - 43.0) * f_edge, 41.0 + (5.0 - 41.0) * f_edge),
        ], INK, .75)
        d.line(plunge_low, INK, .75)
        d.line(plunge_high, INK, .75)
        d.line(pitch_high, INK, .75)
        d.line([
            (43.0 - 38.0 * 0.15, 41.0),
            (43.0 + (24.0 - 43.0) * 0.15, 41.0 + (5.0 - 41.0) * 0.15),
        ], INK, .75)

    d.poly([v_top, v_bl, v_br], None, INK)
    # Three directional axis arrows outside the triangle edges (ref/18.png bottom)
    d.text_free_arrow(9.0, 25.0, 13.0, 17.5, INK, .7, head=2.0)
    d.text_free_arrow(39.0, 25.0, 35.0, 17.5, INK, .7, head=2.0)
    d.text_free_arrow(28.5, 44.0, 19.5, 44.0, INK, .7, head=2.0)
    return d


# ---------------------------------------------------------------------------
# 20-22. Stereonets and Contouring Device (FGM 6.10, ref/19, 20, 22.png)
# ---------------------------------------------------------------------------

def gl_orthographic_net():
    """Orthographic stereonet with graduated rim, straight horizontal parallels and elliptical meridians."""
    d = FieldDrawing()
    cx, cy = 24.0, 24.0
    r_outer, r_prim = 19.5, 17.6

    # Graduated outer degree ring (ref/19.png)
    d.circle(cx, cy, r_outer, QUARTZ, INK)
    d.circle(cx, cy, r_prim, PAPER, INK)
    for deg in range(0, 360, 10):
        rad = math.radians(deg)
        r0 = r_prim if deg % 30 == 0 else r_prim + 0.55
        d.line([
            (cx + r0 * math.cos(rad), cy + r0 * math.sin(rad)),
            (cx + r_outer * math.cos(rad), cy + r_outer * math.sin(rad)),
        ], INK if deg % 30 == 0 else STEEL, .65 if deg % 30 == 0 else .48)

    prim_clip = Point(cx, cy).buffer(r_prim - .2)
    with d.clipped(prim_clip):
        # Small circles (parallels of latitude): straight horizontal lines y = cy +/- R*sin(lat)
        # Spaced at 20, 40, 60, 76 deg -> crowding near the N and S poles!
        for lat in (20, 40, 60, 76):
            dy = r_prim * math.sin(math.radians(lat))
            hw = r_prim * math.cos(math.radians(lat))
            for sign in (-1, 1):
                d.line([(cx - hw, cy + sign * dy), (cx + hw, cy + sign * dy)], STEEL, .55)

        # Great circles (meridians of longitude): semi-ellipses rx = R*sin(lon), ry = R
        # Spaced at 20, 40, 60, 76 deg -> crowding densely near the E/W rim!
        for lon in (20, 40, 60, 76):
            rx = r_prim * math.sin(math.radians(lon))
            for start, stop in ((-90, 90), (90, 270)):
                pts = ellipse_points(cx, cy, rx, r_prim, start=start, stop=stop, steps=40)
                d.line(pts, INK if lon == 60 else STEEL, .62 if lon == 60 else .55)

        # Principal N-S and E-W axes
        d.line([(cx - r_prim, cy), (cx + r_prim, cy)], INK, .8)
        d.line([(cx, cy - r_prim), (cx, cy + r_prim)], INK, .8)

    d.circle(cx, cy, r_prim, None, INK)
    d.circle(cx, cy, r_outer, None, INK)
    return d


def gl_wulff_net():
    """Wulff equal-angle stereonet with circular-arc great and small circles and polar caps."""
    d = FieldDrawing()
    cx, cy, r = 24.0, 24.0, 18.5
    d.circle(cx, cy, r, PAPER, INK)

    prim_clip = Point(cx, cy).buffer(r - .25)
    # Polar caps around N and S poles where minor meridians terminate (ref/20.png)
    cap_rad = r * math.tan(math.radians(15))
    cap_dist = r / math.cos(math.radians(15))
    n_cap = Point(cx, cy - cap_dist).buffer(cap_rad)
    s_cap = Point(cx, cy + cap_dist).buffer(cap_rad)
    inner_clip = prim_clip.difference(n_cap).difference(s_cap)

    with d.clipped(prim_clip):
        # Small circles (parallels): circular arcs orthogonal to the primitive circle
        for beta in (15, 32, 50, 68):
            rad = math.radians(beta)
            rc = r * math.tan(rad)
            yc_off = r / math.cos(rad)
            for sign in (-1, 1):
                pts = ellipse_points(cx, cy + sign * yc_off, rc, rc, start=0, stop=360, steps=64)
                d.line(pts, INK if beta == 15 else STEEL, .68 if beta == 15 else .55)

    with d.clipped(inner_clip):
        # Great circles (meridians): circular arcs passing through N and S poles
        for alpha in (18, 36, 54, 72):
            rad = math.radians(alpha)
            rg = r / math.cos(rad)
            xc_off = r * math.tan(rad)
            for sign in (-1, 1):
                pts = ellipse_points(cx + sign * xc_off, cy, rg, rg, start=0, stop=360, steps=64)
                d.line(pts, INK if alpha == 54 else STEEL, .62 if alpha == 54 else .55)

    # Principal N-S and E-W diameters + N/S external ticks
    d.line([(cx - r, cy), (cx + r, cy)], INK, .8)
    d.line([(cx, cy - r - 2.2), (cx, cy + r + 2.2)], INK, .85)
    d.circle(cx, cy, r, None, INK)
    return d


def gl_schmidt_net():
    """Schmidt equal-area stereonet with Lambert equal-area meridian and parallel spacing and polar caps."""
    d = FieldDrawing()
    cx, cy, r = 24.0, 24.0, 18.5
    d.circle(cx, cy, r, PAPER, INK)

    prim_clip = Point(cx, cy).buffer(r - .25)
    # Polar caps around N and S poles where intermediate meridians terminate (ref/21.png)
    cap_rad = r * math.sqrt(2.0) * math.sin(math.radians(15.0 / 2.0))
    n_cap = Point(cx, cy - r).buffer(cap_rad * 1.45)
    s_cap = Point(cx, cy + r).buffer(cap_rad * 1.45)
    inner_clip = prim_clip.difference(n_cap).difference(s_cap)

    with d.clipped(prim_clip):
        # Small circles (parallels) in Lambert azimuthal equal-area projection:
        # equatorial intercept y_eq = R * sqrt(2) * sin(lat / 2), rim intercept y_rim = R * sin(lat)
        for lat in (18, 36, 54, 72):
            rad = math.radians(lat)
            y_eq = r * math.sqrt(2.0) * math.sin(rad / 2.0)
            y_rim = r * math.sin(rad)
            x_rim = r * math.cos(rad)
            for sign in (-1, 1):
                pts = []
                for i in range(41):
                    u = -1.0 + 2.0 * i / 40.0
                    x = x_rim * u
                    y = sign * (y_eq + (y_rim - y_eq) * (u * u))
                    pts.append((cx + x, cy + y))
                d.line(pts, INK if lat == 72 else STEEL, .68 if lat == 72 else .55)

    with d.clipped(inner_clip):
        # Great circles (meridians) in Lambert equal-area projection:
        # equatorial intercept x_eq = R * sqrt(2) * sin(lon / 2), passing through N and S poles
        for lon in (18, 36, 54, 72):
            rad = math.radians(lon)
            x_eq = r * math.sqrt(2.0) * math.sin(rad / 2.0)
            for sign in (-1, 1):
                pts = []
                for i in range(49):
                    t = -math.pi / 2.0 + math.pi * i / 48.0
                    # Equal-area meridian curve from N pole to S pole through (cx + sign*x_eq, cy)
                    x = sign * x_eq * math.cos(t)
                    y = r * math.sin(t)
                    pts.append((cx + x, cy + y))
                d.line(pts, INK if lon == 54 else STEEL, .62 if lon == 54 else .55)

    # Principal N-S and E-W diameters + primitive circle
    d.line([(cx - r, cy), (cx + r, cy)], INK, .8)
    d.line([(cx, cy - r), (cx, cy + r)], INK, .8)
    d.circle(cx, cy, r, None, INK)
    return d


def gl_stereonet_contouring_device():
    """Equal-area stereonet 1% counting device with tick-marked rim and orthogonal ellipse chains."""
    d = FieldDrawing()
    cx, cy, r = 24.0, 24.0, 17.5
    d.circle(cx, cy, r, PAPER, INK)

    # Exterior degree tick marks protruding from the primitive circle rim (ref/22.png)
    for deg in range(0, 360, 10):
        rad = math.radians(deg)
        tick_len = 2.4 if deg % 90 == 0 else 1.45
        d.line([
            (cx + r * math.cos(rad), cy + r * math.sin(rad)),
            (cx + (r + tick_len) * math.cos(rad), cy + (r + tick_len) * math.sin(rad)),
        ], INK, .8 if deg % 90 == 0 else .55)

    prim_clip = Point(cx, cy).buffer(r - .15)
    with d.clipped(prim_clip):
        # Orthogonal counting-ellipse chains along vertical and horizontal axes (ref/22.png)
        # Along vertical axis: ellipses widen horizontally toward N/S rim
        for offset, rx, ry in [
            (3.1, 2.2, 2.1),
            (7.3, 2.35, 2.05),
            (11.4, 2.55, 1.95),
            (15.3, 2.85, 1.80),
        ]:
            for sign in (-1, 1):
                yc = cy + sign * offset
                d.ellipse(cx, yc, rx, ry, GLASS, INK)
                d.line([(cx - .8, yc), (cx + .8, yc)], INK, .55)

        # Along horizontal axis: ellipses elongate vertically toward E/W rim + rim half-ellipses
        for offset, rx, ry in [
            (3.1, 2.1, 2.2),
            (7.3, 2.05, 2.35),
            (11.4, 1.95, 2.55),
            (15.3, 1.80, 2.85),
            (18.2, 1.55, 3.20),
        ]:
            for sign in (-1, 1):
                xc = cx + sign * offset
                d.ellipse(xc, cy, rx, ry, GLASS, INK)
                if offset < 17.0:
                    d.line([(xc, cy - .8), (xc, cy + .8)], INK, .55)

        # Full N-S and E-W crosshairs across the primitive circle
        d.line([(cx - r, cy), (cx + r, cy)], INK, .75)
        d.line([(cx, cy - r), (cx, cy + r)], INK, .75)

    d.circle(cx, cy, r, None, INK)
    return d


# ---------------------------------------------------------------------------
# Exported ROWS
# ---------------------------------------------------------------------------

ROWS = [
    (
        'gl_fold_upright_horizontal',
        'Upright Horizontal Fold',
        'Oblique block diagram of a symmetric antiform with a vertical hatched axial surface and a horizontal hinge line.',
        'FGM 5.1 Fold definitions and attitudes',
        partial(fold_attitude, 'upright_horizontal'),
    ),
    (
        'gl_fold_upright_plunging',
        'Upright Plunging Fold',
        'Oblique block diagram of an antiform with a vertical hatched axial surface and a forward-plunging hinge line.',
        'FGM 5.1 Fold definitions and attitudes',
        partial(fold_attitude, 'upright_plunging'),
    ),
    (
        'gl_fold_vertical',
        'Vertical Fold',
        'Oblique block diagram of a fold closing horizontally on the top surface with a vertical hinge and vertical hatched axial surface.',
        'FGM 5.1 Fold definitions and attitudes',
        partial(fold_attitude, 'vertical'),
    ),
    (
        'gl_fold_inclined_plunging',
        'Inclined Plunging Fold',
        'Oblique block diagram of an asymmetrical plunging fold with a moderately dipping hatched axial surface and unequal limb dips.',
        'FGM 5.1 Fold definitions and attitudes',
        partial(fold_attitude, 'inclined_plunging'),
    ),
    (
        'gl_fold_overturned_horizontal',
        'Overturned Horizontal Fold',
        'Oblique block diagram of an overturned fold with both limbs dipping in the same direction, a moderately inclined axial surface and a horizontal hinge.',
        'FGM 5.1 Fold definitions and attitudes',
        partial(fold_attitude, 'overturned_horizontal'),
    ),
    (
        'gl_fold_overturned_plunging',
        'Overturned Plunging Fold',
        'Oblique block diagram of an overturned plunging fold with same-direction dipping limbs, a tilted hatched axial surface and a plunging hinge.',
        'FGM 5.1 Fold definitions and attitudes',
        partial(fold_attitude, 'overturned_plunging'),
    ),
    (
        'gl_fold_recumbent',
        'Recumbent Fold',
        'Oblique block diagram of a sideways-closing fold with a horizontal hatched axial surface and an inverted lower limb.',
        'FGM 5.1 Fold definitions and attitudes',
        partial(fold_attitude, 'recumbent'),
    ),
    (
        'gl_fold_reclined',
        'Reclined Fold',
        'Oblique block diagram of a reclined fold whose hinge plunges directly down the dip of an inclined hatched axial surface.',
        'FGM 5.1 Fold definitions and attitudes',
        partial(fold_attitude, 'reclined'),
    ),
    (
        'gl_monocline',
        'Monocline',
        'Oblique block diagram showing a local steep flexure stepping horizontal strata down to a lower level.',
        'FGM 5.1 Fold definitions and attitudes',
        gl_monocline,
    ),
    (
        'gl_fold_vergence',
        'Fold Vergence',
        'Major antiform with asymmetric Z and S limb folds, a symmetric M hinge fold, axial trace and inward vergence arrows.',
        'FGM 5.15 Vergence and superposed folds',
        gl_fold_vergence,
    ),
    (
        'gl_superposed_folds',
        'Superposed Folds',
        'Map swatch showing a refolded crescent-and-mushroom stippled marker bed cut by early curved and late straight axial traces.',
        'FGM 5.14.21 & 5.15 Superposed folds',
        gl_superposed_folds,
    ),
    (
        'gl_fold_class_1a',
        'Fold Class 1A (Strongly Convergent)',
        'Folded layer with a thinned hinge, thickened limbs and dip isogons converging strongly inward toward the core.',
        'FGM 5.10 Classification of folds by dip isogons',
        partial(fold_isogon_class, '1a'),
    ),
    (
        'gl_fold_class_1b',
        'Fold Class 1B (Parallel)',
        'Concentric folded layer of constant orthogonal thickness with dip isogons radiating perpendicular to the arcs from a common centre.',
        'FGM 5.10 Classification of folds by dip isogons',
        partial(fold_isogon_class, '1b'),
    ),
    (
        'gl_fold_class_1c',
        'Fold Class 1C (Weakly Convergent)',
        'Folded layer with slightly attenuated limbs and dip isogons converging weakly toward the inner arc.',
        'FGM 5.10 Classification of folds by dip isogons',
        partial(fold_isogon_class, '1c'),
    ),
    (
        'gl_fold_class_2',
        'Fold Class 2 (Similar)',
        'Similar fold with identical outer and inner bounding curves and strictly vertical dip isogons parallel to the axial trace.',
        'FGM 5.10 Classification of folds by dip isogons',
        partial(fold_isogon_class, '2'),
    ),
    (
        'gl_fold_class_3',
        'Fold Class 3 (Divergent)',
        'Folded layer with a thickened crest, thinned limbs and dip isogons diverging downward away from the outer arc.',
        'FGM 5.10 Classification of folds by dip isogons',
        partial(fold_isogon_class, '3'),
    ),
    (
        'gl_dip_isogon_construction',
        'Dip Isogon Construction',
        'Inclined folded layer with parallel equal-dip tangent lines joined by a dip isogon alongside a tilted half-circle protractor.',
        'FGM 5.10 Classification of folds by dip isogons',
        gl_dip_isogon_construction,
    ),
    (
        'gl_fold_attitude_grid',
        'Fold Attitude Triangular Grid',
        'Equilateral plotting triangle ruled with intersecting iso-dip lines, curved iso-plunge arcs and sweeping iso-pitch rays.',
        'FGM 5.10 Triangular grid for fold attitudes',
        gl_fold_attitude_grid,
    ),
    (
        'gl_fold_attitude_classification',
        'Fold Attitude Classification Triangle',
        'Triangular fold-attitude diagram subdivided into shaded vertical, horizontal-upright and recumbent corners with upright, reclined, horizontal and inclined fields.',
        'FGM 5.10 Classification of fold attitudes',
        gl_fold_attitude_classification,
    ),
    (
        'gl_orthographic_net',
        'Orthographic Stereonet',
        'Equatorial orthographic projection net with a graduated degree rim, straight horizontal latitude parallels and rim-crowded elliptical meridians.',
        'FGM 6.10 Stereonets and contouring device',
        gl_orthographic_net,
    ),
    (
        'gl_wulff_net',
        'Wulff Equal-Angle Stereonet',
        'Equal-angle stereographic net with circular-arc great and small circles terminating at north and south polar caps.',
        'FGM 6.10 Stereonets and contouring device',
        gl_wulff_net,
    ),
    (
        'gl_schmidt_net',
        'Schmidt Equal-Area Stereonet',
        'Equal-area Lambert stereonet with area-preserving meridian and parallel curves and polar caps.',
        'FGM 6.10 Stereonets and contouring device',
        gl_schmidt_net,
    ),
    (
        'gl_stereonet_contouring_device',
        'Stereonet Contouring Device',
        'Equal-area counting circle with exterior rim ticks and orthogonal crosshairs of 1-percent area counting ellipses.',
        'FGM 6.10 Stereonets and contouring device',
        gl_stereonet_contouring_device,
    ),
]
