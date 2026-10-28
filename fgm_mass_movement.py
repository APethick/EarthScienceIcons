"""Field Geologists' Manual — Mass movement (landslide classification after Varnes).

Reference: Berkman, D. A. (ed.) Field Geologists' Manual, 4th edition,
AusIMM Monograph 9 — Landslide classification after Varnes (1978).
All 29 icons are 48-unit text-free geological cross-sections and oblique block
diagrams built with FieldDrawing.
"""
import math
from shapely.geometry import LineString, Point, Polygon

from fgm_common import (
    ALLUVIUM, BASALT, CLAY, CONGLOMERATE, DOLOMITE, FieldDrawing, GRANITE,
    INK, LIMESTONE, LOESS, MUDSTONE, PLAGIOCLASE, QUARTZ, ROCK, SAND,
    SANDSTONE, SCHIST, SHALE, SKY, SOIL, SOIL_DARK, STEEL, TUFF, VEGETATION,
    WATER, WHITE, ellipse_points, irregular_polygon, rng, scatter, smooth,
    smooth_closed,
)


# --------------------------------------------------------- texture helpers --

def _curved_arrow(d, points, colour=INK, width=.95, head=2.6):
    """Draw a smooth curved trajectory ending in a text_free_arrow head."""
    pts = smooth(points, 2) if len(points) > 2 else list(points)
    x0, y0 = pts[-2]
    x1, y1 = pts[-1]
    dx, dy = x1 - x0, y1 - y0
    dist = math.hypot(dx, dy) or 1.0
    ux, uy = dx / dist, dy / dist
    neck = (x1 - ux * head * .7, y1 - uy * head * .7)
    d.line(pts[:-1] + [neck], colour, width)
    d.text_free_arrow(x1 - ux * head * 1.15, y1 - uy * head * 1.15, x1, y1,
                      colour=colour, width=width, head=head)


def _bedrock_joints(d, poly, angle=-12, spacing=4.2, cross_spacing=6.5, width=.58):
    """Clipped bedding planes and orthogonal block joints inside a rock polygon."""
    x0, y0, x1, y1 = poly.bounds
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    reach = math.hypot(x1 - x0, y1 - y0)
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    with d.clipped(poly.buffer(-.35)):
        idx = 0
        offset = -reach
        while offset <= reach:
            px, py = cx + nx * offset, cy + ny * offset
            d.line([(px - ux * reach, py - uy * reach),
                    (px + ux * reach, py + uy * reach)], INK, width)
            if cross_spacing:
                shift = (idx % 2) * (cross_spacing * .5)
                t = -reach + shift
                while t <= reach:
                    jx0, jy0 = px + ux * t, py + uy * t
                    jx1, jy1 = jx0 + nx * spacing, jy0 + ny * spacing
                    d.line([(jx0, jy0), (jx1, jy1)], INK, width * .92)
                    t += cross_spacing
            offset += spacing
            idx += 1


def _shale_laminae(d, poly, angle=0, spacing=2.8, dash=3.4, gap=2.0, width=.55):
    """Clipped dashed fissile shale lamination inside ``poly``."""
    x0, y0, x1, y1 = poly.bounds
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    reach = math.hypot(x1 - x0, y1 - y0)
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    row = 0
    with d.clipped(poly.buffer(-.4)):
        offset = -reach
        while offset <= reach:
            px, py = cx + nx * offset, cy + ny * offset
            shift = (row % 2) * ((dash + gap) * .5)
            t = -reach + shift
            while t < reach:
                p0 = (px + ux * t, py + uy * t)
                p1 = (px + ux * (t + dash), py + uy * (t + dash))
                d.line([p0, p1], INK, width)
                t += dash + gap
            offset += spacing
            row += 1


def _debris_clasts(d, poly, seed=10, count=14, min_r=1.35, max_r=2.15, spacing=3.1):
    """Fill a debris region with bold angular clasts in contrasting rock tones."""
    colours = (ROCK, SANDSTONE, LIMESTONE, BASALT, QUARTZ)
    r = rng(seed)
    pts = scatter(seed, count, poly, spacing=spacing, margin=1.45)
    for idx, (x, y) in enumerate(pts):
        rad = r.uniform(min_r, max_r)
        ang = r.uniform(0, 180)
        c = colours[idx % len(colours)]
        clast = irregular_polygon(seed * 31 + idx, x, y, rad, sides=5, jitter=.28,
                                  stretch=r.uniform(1.0, 1.35), angle=ang)
        d.shape(Polygon(clast), c, INK, width=.65)


def _earth_texture(d, poly, seed=20, count=12, angle=0):
    """Subtle dispersed soil/clay dashes and fine granules."""
    pts = scatter(seed, count, poly, spacing=3.4, margin=1.5)
    a = math.radians(angle)
    ux, uy = math.cos(a) * 1.1, math.sin(a) * 1.1
    for idx, (x, y) in enumerate(pts):
        if idx % 3 == 0:
            d.circle(x, y, .52, INK, INK, True)
        else:
            d.line([(x - ux, y - uy), (x + ux, y + uy)], INK, .55)


def _oblique_slope(d, slope_fill=TUFF, side_fill=ROCK, front_fill=SOIL,
                   jointed_side=True):
    """Standard perspective hillslope block for 3D flow/avalanche diagrams."""
    side = Polygon([(5, 16), (5, 31), (25, 42), (25, 35)])
    front = Polygon([(25, 35), (25, 42), (43, 33), (43, 27)])
    slope = Polygon([(5, 16), (22, 7), (43, 27), (25, 35)])
    d.shape(side, side_fill, INK)
    if jointed_side:
        _bedrock_joints(d, side, angle=26, spacing=4.2, cross_spacing=6.0, width=.52)
    d.shape(front, front_fill, INK)
    d.shape(slope, slope_fill, INK)
    return slope, side, front


# --------------------------------------------------------- 1-6: Bedrock -----

def build_rock_fall():
    d = FieldDrawing()
    # Steep jointed bedrock cliff on left with upper detachment scar and basal platform
    cliff = Polygon([(5, 7), (19, 7), (20, 14), (17, 15), (18, 23),
                     (16, 30), (21, 38), (43, 38), (43, 42), (5, 42)])
    d.shape(cliff, ROCK, INK)
    _bedrock_joints(d, Polygon([(5, 7), (20, 7), (21, 42), (5, 42)]),
                    angle=8, spacing=4.8, cross_spacing=6.5, width=.58)
    # Dashed scar notch at cliff brow
    d.dashed([(19, 7), (22, 11), (18, 15)], INK, .65, 1.8, 1.2)
    # Coarse angular talus wedge at cliff base
    talus = Polygon([(17, 30), (23, 33), (31, 38), (16, 38)])
    d.shape(talus, DOLOMITE, INK)
    for pts, col in [
        ([(18, 34), (21, 33), (22, 36), (18, 37)], SANDSTONE),
        ([(23, 35), (26, 34), (27, 37), (23, 37.5)], LIMESTONE),
        ([(27, 36), (30, 35.5), (31, 38), (27, 38)], ROCK),
    ]:
        d.shape(Polygon(pts), col, INK, width=.7)
    # Free-falling and bouncing angular rock blocks + dashed trajectories
    d.dashed([(21, 10), (25, 16), (27, 25), (27, 33)], INK, .72, 2.0, 1.3)
    d.dashed([(27, 33), (31, 28), (36, 31), (39, 35)], INK, .72, 1.8, 1.2)
    # Falling block in air
    b1 = [(22, 16), (26.5, 15), (27.5, 19), (23, 20)]
    d.poly(b1, SANDSTONE, INK)
    d.line([(23, 17.5), (27, 16.8)], INK, .55)
    # Bouncing/rolling block near toe
    b2 = [(35, 32), (39.5, 31), (41, 35), (36.5, 36)]
    d.poly(b2, SANDSTONE, INK)
    d.line([(36, 33.8), (40, 33)], INK, .55)
    # Clear movement arrow
    d.text_free_arrow(29, 11, 34, 24, INK, .95, 2.7)
    return d


def build_rock_topple():
    d = FieldDrawing()
    # Sloping bedrock base with steeply dipping joints
    base = Polygon([(5, 27), (16, 30), (28, 34), (43, 38), (43, 42), (5, 42)])
    d.shape(base, ROCK, INK)
    with d.clipped(base.buffer(-.3)):
        for x in (9, 14, 19, 24, 29, 35):
            d.line([(x, 26), (x - 3, 43)], INK, .58)
    # Column 1 (left, intact steeply dipping column)
    c1 = [(5, 11), (11, 12), (9, 28.5), (5, 27)]
    d.poly(c1, LIMESTONE, INK)
    d.line([(5.3, 17), (10.3, 18)], INK, .58)
    d.line([(5.2, 22.5), (9.6, 23.5)], INK, .58)
    # Column 2 (slightly tilted forward, tension gap behind)
    c2 = [(13, 12.5), (18.5, 14), (15, 30), (10, 28.5)]
    d.poly(c2, SANDSTONE, INK)
    d.line([(12, 18.5), (17.2, 20)], INK, .58)
    d.line([(11, 24), (16, 25.5)], INK, .58)
    # Column 3 (strongly rotating forward about pivot at toe)
    c3 = [(22.5, 15), (27.8, 17.8), (21, 31.8), (16, 30.2)]
    d.poly(c3, LIMESTONE, INK)
    d.line([(20.2, 20.5), (25.4, 23)], INK, .58)
    d.line([(18.2, 25.5), (23.2, 28)], INK, .58)
    # Column 4 (actively toppling slab leaning steeply right)
    c4 = [(31, 20.5), (35.2, 24.5), (26.5, 33.8), (22, 32)]
    d.poly(c4, SANDSTONE, INK)
    d.line([(27.8, 25), (31.8, 28.5)], INK, .58)
    # Overturned fallen column block on toe platform
    c5 = [(29, 33), (41, 34.5), (40.5, 38), (28.5, 36.5)]
    d.poly(c5, LIMESTONE, INK)
    d.line([(33, 33.5), (32.5, 37)], INK, .58)
    d.line([(37, 34), (36.5, 37.5)], INK, .58)
    # Forward overturning trajectory arrow above rotating columns
    _curved_arrow(d, [(15, 8), (24, 9), (33, 14), (39, 22)], INK, .95, 2.7)
    return d


def build_rock_slump():
    d = FieldDrawing()
    # Unslumped bedrock footwall on left: upper Sandstone cap over lower Shale
    # (After Varnes Fig III.A: Rock Slump — stepped back-tilted sandstone-over-shale blocks)
    shale_base = Polygon([(5, 16.5), (12.5, 16.5), (15, 25.5), (22.5, 33),
                          (33, 37), (43, 37), (43, 42), (5, 42)])
    d.shape(shale_base, SHALE, INK)
    _shale_laminae(d, shale_base, angle=0, spacing=3.0)
    ss_cap = Polygon([(5, 8), (13, 8), (12.5, 16.5), (5, 16.5)])
    d.shape(ss_cap, SANDSTONE, INK)
    _bedrock_joints(d, ss_cap, angle=0, spacing=4.2, cross_spacing=4.8, width=.58)

    # Rotational Block 1 (dropped down main scarp and back-tilted ~14 deg toward scarp)
    b1_shale = Polygon([(13.8, 19.5), (25, 16.8), (26.5, 34.5), (22.5, 33), (15, 25.5)])
    d.shape(b1_shale, SHALE, INK)
    _shale_laminae(d, b1_shale, angle=-14, spacing=2.8)
    b1_ss = Polygon([(13.5, 14.0), (24.5, 11.2), (25, 16.8), (13.8, 19.5)])
    d.shape(b1_ss, SANDSTONE, INK)
    _bedrock_joints(d, b1_ss, angle=-14, spacing=3.8, cross_spacing=4.8, width=.55)

    # Rotational Block 2 (stepped lower, back-tilted ~16 deg, with fractured bulging toe on right)
    b2_shale = Polygon([(25.5, 23.2), (35.5, 20.5), (42, 33), (40, 37), (33, 37), (26.5, 34.5)])
    d.shape(b2_shale, MUDSTONE, INK)
    _shale_laminae(d, b2_shale, angle=-16, spacing=2.8)
    b2_ss = Polygon([(25.2, 18.2), (35, 15.5), (35.5, 20.5), (25.5, 23.2)])
    d.shape(b2_ss, SANDSTONE, INK)
    _bedrock_joints(d, b2_ss, angle=-16, spacing=3.6, cross_spacing=4.5, width=.55)

    # Bold concave-upward listric rotational slip surface + secondary internal shear
    slip = smooth([(13, 8), (14.5, 24), (22.5, 33), (33, 37), (40, 37), (42, 33)], 3)
    d.line(slip, INK, 1.25)
    d.dashed([(24.5, 11.2), (25.5, 24), (27.5, 35)], INK, .7, 2.0, 1.2)
    # Rotational movement arrow
    _curved_arrow(d, [(18, 6.8), (28, 7.8), (37.5, 12.5), (42, 20.5)], INK, .95, 2.6)
    return d


def build_rock_block_slide():
    d = FieldDrawing()
    # Dip-slope bedded bedrock footwall dipping ~28 deg right (after Varnes Rock Block Slide)
    footwall = Polygon([(5, 14), (38, 33), (43, 33), (43, 42), (5, 42)])
    d.shape(footwall, LIMESTONE, INK)
    _bedrock_joints(d, footwall, angle=29.8, spacing=3.8, cross_spacing=7.5, width=.58)

    # Upper intact cap bed at left crown (leaving open tension scarp gap)
    upper_bed = Polygon([(5, 8.2), (12, 12.2), (10, 16.8), (5, 14)])
    d.shape(upper_bed, SANDSTONE, INK)
    _bedrock_joints(d, upper_bed, angle=29.8, spacing=4.5, cross_spacing=4.5, width=.58)

    # Coherent sliding rock block translating down the planar bedding plane
    slab = Polygon([(16.5, 14.8), (33.5, 24.6), (31.2, 29.0), (14.2, 19.2)])
    d.shape(slab, SANDSTONE, INK)
    _bedrock_joints(d, slab, angle=29.8, spacing=4.5, cross_spacing=4.8, width=.58)

    # Overriding/buckled rock slabs ramping at the toe
    for pts, col in [
        ([(31.2, 29.0), (36.5, 26.5), (38, 30.2), (33, 31.5)], SANDSTONE),
        ([(35.5, 29.5), (41.5, 28.8), (42, 32.8), (36, 33)], DOLOMITE),
    ]:
        d.shape(Polygon(pts), col, INK, width=.75)

    # Bold planar slide surface line & parallel movement arrow
    d.line([(10, 16.8), (38, 33)], INK, 1.2)
    d.text_free_arrow(19, 10.5, 34, 19.2, INK, .95, 2.7)
    return d


def build_rock_lateral_spread():
    d = FieldDrawing()
    # Basal firm stratum
    firm_base = Polygon([(5, 36), (43, 36), (43, 42), (5, 42)])
    d.shape(firm_base, ROCK, INK)
    _bedrock_joints(d, firm_base, angle=0, spacing=5.5, cross_spacing=8.0, width=.52)

    # Ductile/plastic shale layer squeezing out toward right escarpment
    ductile = Polygon([(5, 26), (37, 26), (41, 31), (42, 36), (5, 36)])
    d.shape(ductile, SHALE, INK)
    # Wavy plastic squeeze lines and upward diapiric folds into fissures
    for y in (29.5, 33):
        pts = [(6 + i * 1.4, y - 1.1 * math.sin(i * .9)) for i in range(25)]
        d.line(pts, INK, .58)

    # Fractured competent bedrock cap blocks separating laterally with open grabens/fissures
    blocks = [
        ([(5, 14), (12.5, 14), (12, 26), (5, 26)], SANDSTONE, 0),
        ([(13.2, 16.5), (17.5, 16.8), (16.8, 26.5), (12.8, 26.2)], LIMESTONE, 3),
        ([(18.5, 14.2), (25, 14.6), (24.5, 26), (18, 26)], SANDSTONE, 4),
        ([(26.5, 15.2), (32.5, 16.2), (31.5, 26.2), (25.8, 26)], LIMESTONE, 8),
        ([(34.2, 17), (39.5, 18.8), (38, 27.5), (33, 26.5)], SANDSTONE, 14),
    ]
    for pts, col, ang in blocks:
        poly = Polygon(pts)
        d.shape(poly, col, INK)
        _bedrock_joints(d, poly, angle=ang, spacing=4.2, cross_spacing=5.5, width=.55)

    # Lateral extension arrow above separating rock blocks
    d.text_free_arrow(16, 9.5, 36, 9.5, INK, .95, 2.7)
    return d


def build_rock_creep_sackung():
    d = FieldDrawing()
    # Mountain ridge with double-crested sagging graben (Sackung), stepped uphill-facing
    # antislope scarplets, and convex lower-slope gravitational bulge (after Varnes Fig V.1-3)
    slope = Polygon([
        (5, 15), (9, 9.5), (12.5, 14), (16, 10),        # Double-crested summit graben trough
        (20.5, 15.5), (22, 13.8),                       # Antislope scarplet 1
        (26.5, 19.5), (28, 18),                         # Antislope scarplet 2
        (35, 24), (41, 31), (43, 38),                   # Convex lower-slope rock bulge
        (43, 42), (5, 42),
    ])
    d.shape(slope, SCHIST, INK)

    # Steeply dipping foliation/bedding planes flexing and bending downslope without brittle basal plane
    with d.clipped(slope.buffer(-.4)):
        for x_base in range(6, 44, 4):
            pts = [
                (x_base - 3, 43),
                (x_base - 1.5, 33),
                (x_base + .8, 25),
                (x_base + 5.0, 17),
                (x_base + 9.0, 9),
            ]
            d.line(smooth(pts, 2), INK, .6)

    # Steep normal fault / sackung scarplet lines under summit graben and antislope scarps
    d.dashed([(9, 9.5), (12.5, 23), (16, 32)], INK, .78, 2.2, 1.3)
    d.dashed([(16, 10), (14, 21)], INK, .78, 2.2, 1.3)
    d.dashed([(22, 13.8), (19.5, 25)], INK, .72, 2.0, 1.3)
    d.dashed([(28, 18), (25, 28)], INK, .72, 2.0, 1.3)

    # Sagging arrow at ridge-top graben + slow flexing arrow above bulging slope
    d.text_free_arrow(12.5, 4.5, 12.5, 12.2, INK, .95, 2.4)
    _curved_arrow(d, [(25, 10.5), (34, 14.5), (41.5, 23)], INK, .95, 2.6)
    return d


# --------------------------------------------------- 7-9: Bedrock Complex ---

def build_rock_fall_debris_flow():
    d = FieldDrawing()
    # Left steep mountain peak with rock-fall scar, long valley floor, right opposing valley wall
    # (After Varnes Fig VI: Rock Fall-Debris Flow / Rock-Fall Avalanche)
    mountain = Polygon([
        (4, 10), (11, 6), (14, 14), (18, 23), (24, 31),
        (35, 32), (40, 23), (44, 25), (44, 42), (4, 42)
    ])
    d.shape(mountain, ROCK, INK)
    _bedrock_joints(d, mountain, angle=-16, spacing=4.6, cross_spacing=6.5, width=.55)

    # Steep concave rock-fall headwall scar at peak
    scar = Polygon([(11, 6), (16.5, 9), (18, 17.5), (14, 14)])
    d.shape(scar, GRANITE, INK)
    # Falling blocks from upper cliff
    d.dashed([(14.5, 9), (18.5, 15), (21, 23)], INK, .72, 1.8, 1.2)
    d.poly([(16, 12), (19.2, 11.5), (19.8, 14.5), (16.5, 15)], SANDSTONE, INK)

    # Long rapid debris-avalanche / debris-flow runout tongue sweeping across valley & banking up right wall
    lobe = Polygon(smooth_closed([
        (16, 22), (23, 25.5), (32, 27), (39.5, 23.5), (41.5, 27),
        (37, 34.5), (27, 36), (18, 31.5), (15, 26)
    ], 2))
    d.shape(lobe, CONGLOMERATE, INK)
    _debris_clasts(d, lobe, seed=71, count=14, min_r=1.25, max_r=1.95, spacing=2.8)

    # Two-stage trajectory arrow: steep rock fall transitioning into long horizontal debris runout
    _curved_arrow(d, [(20, 7.5), (23, 17.5), (30, 21), (39, 19)], INK, .95, 2.7)
    return d


def build_slump_topple():
    d = FieldDrawing()
    # Lower slope shale base with deep rotational slump + upper jointed caprock toppling forward
    # (After Varnes Fig VI: Slump and Topple)
    base = Polygon([(5, 20), (13.5, 20), (16.5, 28), (26, 35), (43, 37), (43, 42), (5, 42)])
    d.shape(base, SHALE, INK)
    _shale_laminae(d, base, angle=0, spacing=3.0)

    # Intact vertically-jointed caprock cliff on left crown
    cliff = Polygon([(5, 8), (12, 8), (12, 20), (5, 20)])
    d.shape(cliff, SANDSTONE, INK)
    d.line([(8.5, 8), (8.5, 20)], INK, .6)
    d.line([(5, 14), (12, 14)], INK, .6)

    # Large back-tilted rotational slump block in mid-lower slope
    slump_shale = Polygon([(15, 22.5), (26.5, 19), (33, 27), (40, 35),
                           (38, 37), (26, 35), (16.5, 28)])
    d.shape(slump_shale, MUDSTONE, INK)
    _shale_laminae(d, slump_shale, angle=-18, spacing=2.8)
    slump_cap = Polygon([(18, 17), (26, 14.2), (26.5, 19), (17.5, 21.8)])
    d.shape(slump_cap, SANDSTONE, INK)
    _bedrock_joints(d, slump_cap, angle=-18, spacing=3.8, cross_spacing=4.2, width=.55)

    # Tall vertically-jointed columns toppling forward at the brow of the slump block!
    col1 = [(27.2, 14.8), (30.8, 16.5), (27.5, 26.5), (24.2, 25)]
    d.poly(col1, SANDSTONE, INK)
    d.line([(25.8, 20), (29.2, 21.5)], INK, .58)
    col2 = [(32, 18.2), (35.5, 21.2), (29.8, 29.5), (26.8, 27.2)]
    d.poly(col2, LIMESTONE, INK)
    d.line([(29.5, 23), (32.8, 25.5)], INK, .58)
    # Toppled blocks at right toe
    d.poly([(34, 31.5), (41, 33), (40.5, 36.5), (33.5, 35)], SANDSTONE, INK)

    # Bold concave rotational rupture surface
    d.line(smooth([(13.5, 20), (16.5, 28), (26, 35), (38, 37), (40.5, 34)], 3), INK, 1.2)
    # Rotational slump arrow + forward toppling arrow at brow
    _curved_arrow(d, [(15, 9), (22, 9.5), (26, 12.5)], INK, .88, 2.3)
    _curved_arrow(d, [(30, 11.5), (37, 15), (41, 24)], INK, .95, 2.6)
    return d


def build_rock_slide_rock_fall():
    d = FieldDrawing()
    # Upper inclined rock-slide ramp above a steep lower cliff step (after Varnes Rock Slide-Rock Fall)
    bedrock = Polygon([
        (5, 13), (24, 23), (25, 36), (43, 38), (43, 42), (5, 42)
    ])
    d.shape(bedrock, ROCK, INK)
    _bedrock_joints(d, bedrock, angle=27, spacing=4.5, cross_spacing=6.5, width=.58)

    # Planar sliding rock slab on upper inclined ramp, overhanging the cliff break
    slab1 = Polygon([(7, 9), (15, 13.2), (13.2, 17.2), (5.2, 13)])
    d.shape(slab1, SANDSTONE, INK)
    _bedrock_joints(d, slab1, angle=27, spacing=4.2, cross_spacing=4.5, width=.55)

    slab2 = Polygon([(16.5, 14), (26.5, 19.2), (24.5, 23.2), (14.5, 18)])
    d.shape(slab2, SANDSTONE, INK)
    _bedrock_joints(d, slab2, angle=27, spacing=4.2, cross_spacing=4.5, width=.55)

    # Talus cone at foot of lower cliff
    talus = Polygon([(25, 30), (35, 37.2), (25, 36.5)])
    d.shape(talus, DOLOMITE, INK)

    # Detached rock blocks falling from the overhanging slide snout over the cliff
    d.dashed([(26.5, 21), (31, 25), (34, 33)], INK, .72, 1.9, 1.2)
    d.poly([(28.5, 24), (32.5, 23.2), (33.2, 26.8), (29.2, 27.5)], SANDSTONE, INK)
    d.poly([(34.5, 33.5), (38.5, 32.8), (39.2, 36.5), (35.2, 37)], SANDSTONE, INK)

    # Upper translational slide arrow + lower fall arrow
    d.text_free_arrow(11, 6, 23, 12.5, INK, .95, 2.5)
    d.text_free_arrow(33, 17, 38, 28, INK, .95, 2.5)
    return d


# --------------------------------------------------------- 10-18: Debris ----

def build_debris_fall():
    d = FieldDrawing()
    # Basal bedrock ledge
    ledge = Polygon([(5, 33), (19, 33), (22, 38), (43, 38), (43, 42), (5, 42)])
    d.shape(ledge, ROCK, INK)
    _bedrock_joints(d, ledge, angle=0, spacing=4.5, cross_spacing=7.0, width=.52)

    # Steep undercut bluff of coarse unconsolidated boulder-gravel debris with matrix stipples
    bluff = Polygon(smooth_closed([
        (5, 7.5), (20.5, 7.5), (22, 13.5), (17.5, 20), (19, 33), (5, 33)
    ], 1))
    d.shape(bluff, CONGLOMERATE, INK)
    _earth_texture(d, bluff, seed=100, count=9, angle=15)
    _debris_clasts(d, bluff, seed=101, count=11, min_r=1.45, max_r=2.25, spacing=3.3)

    # Coarse debris talus cone at base of bluff
    cone = Polygon([(19, 27), (34, 38), (21, 38), (19, 33)])
    d.shape(cone, ALLUVIUM, INK)
    _debris_clasts(d, cone, seed=102, count=6, min_r=1.3, max_r=1.9, spacing=2.8)

    # Falling angular cobbles, boulders and pebbles on dashed trajectories
    d.dashed([(21.5, 11), (26, 18), (29, 28)], INK, .72, 2.0, 1.3)
    d.dashed([(19.5, 18), (25, 24), (35, 34)], INK, .72, 1.8, 1.2)
    for seed, x, y, r, col in [
        (11, 25, 16, 2.1, ROCK),
        (12, 29, 23, 1.7, SANDSTONE),
        (13, 23.5, 23, 1.3, BASALT),
        (14, 36.5, 34.5, 2.0, LIMESTONE),
    ]:
        d.poly(irregular_polygon(seed, x, y, r, sides=5, jitter=.3), col, INK)

    d.text_free_arrow(30, 10, 36, 24, INK, .95, 2.7)
    return d


def build_debris_topple():
    d = FieldDrawing()
    # Basal clean sand layer (after Varnes Fig II: Debris Topple — Clayey gravel over Clean sand)
    sand_base = Polygon([(5, 29), (26, 32), (43, 36), (43, 42), (5, 42)])
    d.shape(sand_base, SAND, INK)
    _earth_texture(d, sand_base, seed=110, count=12, angle=6)

    # Intact coarse clayey-gravel layer on left with vertical tension cracks
    gravel_left = Polygon([(5, 10), (15, 11), (14, 30.2), (5, 29)])
    d.shape(gravel_left, CONGLOMERATE, INK)
    _debris_clasts(d, gravel_left, seed=111, count=7, min_r=1.35, max_r=2.0, spacing=3.0)

    # Forward-tilting debris column 1 (separated by deep V-crack)
    col1 = Polygon([(17, 11.5), (24.5, 13.5), (21, 31.2), (14.5, 30.2)])
    d.shape(col1, CONGLOMERATE, INK)
    _debris_clasts(d, col1, seed=112, count=5, min_r=1.3, max_r=1.9, spacing=2.8)

    # Strongly toppling debris column 2 leaning outward over the sand toe
    col2 = Polygon([(27, 15.5), (34, 19.5), (27, 32.5), (21.5, 31.2)])
    d.shape(col2, CONGLOMERATE, INK)
    _debris_clasts(d, col2, seed=113, count=5, min_r=1.3, max_r=1.9, spacing=2.8)

    # Collapsed coarse debris heap on right toe
    heap = Polygon([(27, 32.5), (35, 29.5), (41, 35.5), (27, 33.5)])
    d.shape(heap, ALLUVIUM, INK)
    _debris_clasts(d, heap, seed=114, count=4, min_r=1.2, max_r=1.7, spacing=2.6)

    # Forward overturning arrow
    _curved_arrow(d, [(19, 7.5), (28, 9), (37, 16), (40, 24)], INK, .95, 2.7)
    return d


def build_debris_slump():
    d = FieldDrawing()
    # Underlying stable bedrock and unslumped coarse debris crown on left
    bedrock = Polygon([(5, 27), (14, 28), (22, 35), (35, 38), (43, 38), (43, 42), (5, 42)])
    d.shape(bedrock, ROCK, INK)
    _bedrock_joints(d, bedrock, angle=8, spacing=4.5, cross_spacing=7.0, width=.52)

    crown = Polygon([(5, 9), (14, 9), (15.5, 21), (14, 28), (5, 27)])
    d.shape(crown, CONGLOMERATE, INK)
    _debris_clasts(d, crown, seed=121, count=7, min_r=1.35, max_r=2.0, spacing=3.0)

    # Rotated coarse-debris slump mass with smooth back-tilted bench and bulging bouldery toe
    slump = Polygon(smooth_closed([
        (15.2, 17.5), (25, 14.5), (32, 21), (39.5, 27.5), (41.5, 34),
        (39, 38), (33, 38), (22, 35), (15.5, 25)
    ], 1))
    d.shape(slump, ALLUVIUM, INK)
    _debris_clasts(d, slump, seed=122, count=14, min_r=1.4, max_r=2.2, spacing=3.0)
    # Internal secondary shear crack within debris slump
    d.dashed([(25.5, 15.2), (26.5, 25), (31, 34)], INK, .7, 2.0, 1.3)

    # Bold concave rotational rupture surface along base of debris slump
    slip = smooth([(14, 9), (15.5, 24), (22, 35), (34, 38), (41.5, 34)], 3)
    d.line(slip, INK, 1.25)

    # Rotational movement arrow
    _curved_arrow(d, [(20, 8), (29, 9.5), (37, 15), (41, 22)], INK, .95, 2.6)
    return d


def build_debris_slide():
    d = FieldDrawing()
    # Planar inclined Bedrock slope (after Varnes Fig III.B: Debris Slide over Bedrock)
    bedrock = Polygon([(5, 13), (40, 36), (43, 36), (43, 42), (5, 42)])
    d.shape(bedrock, ROCK, INK)
    _bedrock_joints(d, bedrock, angle=33, spacing=4.5, cross_spacing=7.0, width=.55)

    # Intact upper colluvial debris cap at crown
    upper_debris = Polygon([(5, 7.5), (11, 11), (9.5, 16), (5, 13)])
    d.shape(upper_debris, CONGLOMERATE, INK)
    _debris_clasts(d, upper_debris, seed=131, count=3, min_r=1.2, max_r=1.7, spacing=2.5)

    # Translational sheet of coarse angular debris sliding along planar bedrock contact
    slide_sheet = Polygon([
        (14.5, 14), (23, 18.5), (32, 24.5), (40, 30.5),
        (41.5, 35.5), (38, 36), (13, 18.2)
    ])
    d.shape(slide_sheet, CONGLOMERATE, INK)
    _debris_clasts(d, slide_sheet, seed=132, count=13, min_r=1.3, max_r=2.0, spacing=2.8)

    # Planar basal slip interface line & translational arrow parallel to slope
    d.line([(9.5, 16), (39, 36)], INK, 1.2)
    d.text_free_arrow(19, 10, 35, 20.5, INK, .95, 2.7)
    return d


def build_debris_flow():
    d = FieldDrawing()
    # Clean perspective hillslope block with incised gully, lateral levees & bouldery fan lobe
    # (After Varnes Fig V: Debris Flow)
    _oblique_slope(d, slope_fill=TUFF, side_fill=ROCK, front_fill=SOIL)

    # Raised lateral levees bordering the narrow channel
    levee_l = Polygon(smooth_closed([(13, 15), (21, 22), (24, 26), (21, 27), (11.5, 18)], 2))
    levee_r = Polygon(smooth_closed([(19, 11.5), (28, 19), (31, 22), (28, 23.5), (17.5, 14)], 2))
    d.shape(levee_l, ALLUVIUM, INK, width=.8)
    d.shape(levee_r, ALLUVIUM, INK, width=.8)

    # Upper V-gully channel expanding into a bulbous boulder-rich lobate tongue on the lower apron
    flow_body = Polygon(smooth_closed([
        (13, 12.5), (18, 10), (21, 14), (27, 19.5),
        (37, 25), (38, 31), (31, 34.5), (23, 32),
        (21, 26), (19.5, 21.5), (13, 16)
    ], 2))
    d.shape(flow_body, CONGLOMERATE, INK)
    _debris_clasts(d, flow_body, seed=141, count=13, min_r=1.3, max_r=2.05, spacing=2.6)

    # Clear movement arrow parallel to the channelised flow (well clear of block rim)
    d.text_free_arrow(26.5, 6.8, 39.5, 19.2, INK, .95, 2.6)
    return d


def build_debris_avalanche():
    d = FieldDrawing()
    # Steep high mountain face (taller/steeper silhouette than hillslope blocks) with a broad
    # open-slope bedrock scar and wide rapid chaotic debris apron (after Varnes Debris Avalanche)
    side = Polygon([(5, 18), (19, 6), (19, 30), (5, 38)])
    mountain_face = Polygon([(19, 6), (31, 10), (43, 29), (26, 40), (19, 30)])
    front_toe = Polygon([(5, 38), (19, 30), (26, 40), (43, 29), (43, 34), (26, 44), (5, 42)])
    d.shape(side, ROCK, INK)
    _bedrock_joints(d, side, angle=-32, spacing=4.2, cross_spacing=6.0, width=.55)
    d.shape(mountain_face, VEGETATION, INK)
    d.shape(front_toe, SOIL, INK)

    # Broad open-slope arcuate bedrock scar stripped across the steep upper mountain face
    scar = Polygon(smooth_closed([
        (19.5, 8.5), (29, 11.5), (35, 21), (22, 26), (19, 17)
    ], 1))
    d.shape(scar, LIMESTONE, INK)
    # Steep chute striations inside the bare open-slope scar
    d.line([(22, 11.5), (26, 19)], INK, .6)
    d.line([(26, 12.5), (30, 19.5)], INK, .6)

    # Wide unchannelised chaotic debris-avalanche sheet rushing across the lower mountain face
    apron = Polygon(smooth_closed([
        (21, 20), (33, 19.5), (42, 28.5), (39, 35), (27, 39.5), (19.5, 30)
    ], 2))
    d.shape(apron, CONGLOMERATE, INK)
    _debris_clasts(d, apron, seed=151, count=15, min_r=1.35, max_r=2.15, spacing=2.6)

    # Rapid open-slope avalanche arrow
    d.text_free_arrow(31, 7.5, 41, 22.5, INK, 1.0, 2.7)
    return d


def build_block_stream():
    d = FieldDrawing()
    # Oblique hillslope with a sinuous ribbon of coarse imbricated boulders (after Varnes Block Stream)
    _oblique_slope(d, slope_fill=TUFF, side_fill=ROCK, front_fill=SOIL)

    # Sinuous periglacial boulder-stream hollow winding down the slope
    stream = Polygon(smooth_closed([
        (13, 12), (20, 10), (23, 15), (22, 20), (29, 24),
        (34, 29), (29, 33), (21, 30), (16, 23), (16, 17)
    ], 2))
    d.shape(stream, SOIL_DARK, INK)

    # Tightly packed coarse angular boulders filling the block stream
    boulders = [
        (16.5, 13.5, 2.0, ROCK), (19.5, 13.0, 1.9, PLAGIOCLASE),
        (18.0, 16.8, 2.2, SANDSTONE), (21.0, 17.2, 1.8, LIMESTONE),
        (18.5, 20.5, 2.3, ROCK), (21.5, 21.5, 2.0, PLAGIOCLASE),
        (20.5, 24.8, 2.4, SANDSTONE), (24.5, 24.2, 2.1, ROCK),
        (23.5, 28.0, 2.5, LIMESTONE), (27.8, 27.0, 2.3, PLAGIOCLASE),
        (27.0, 30.2, 2.4, SANDSTONE), (31.0, 29.5, 2.2, ROCK),
    ]
    for idx, (bx, by, br, col) in enumerate(boulders):
        d.shape(Polygon(irregular_polygon(160 + idx, bx, by, br, sides=6, jitter=.25)),
                col, INK, width=.68)

    # Small spruce tree on the stable flank (as in Varnes Block Stream illustration)
    d.line([(36, 22), (36, 26)], INK, .85)
    d.poly([(36, 16.5), (33.2, 23), (38.8, 23)], VEGETATION, INK)

    # Downslope movement arrow along upper flank (well clear of block rim)
    d.text_free_arrow(26.5, 6.8, 39.5, 19.2, INK, .95, 2.5)
    return d


def build_solifluction():
    d = FieldDrawing()
    # Gentle periglacial slope: frozen permafrost base (SKY/QUARTZ) + active layer lobes
    # (After Varnes Fig V: Solifluction — overlapping turf-banked lobes on gentle slope)
    permafrost = Polygon([(5, 21), (43, 33), (43, 42), (5, 42)])
    d.shape(permafrost, SKY, INK)
    with d.clipped(permafrost.buffer(-.4)):
        for x in range(8, 42, 7):
            y = 25 + (x - 5) * .3
            d.line([(x, y), (x + 4, y + 1.2)], WATER, .75)
            d.line([(x + 1, y + 3.5), (x + 5, y + 4.7)], INK, .55)

    # Overlapping tongue-shaped solifluction lobes / terracettes stepping down the gentle slope
    lobes = [
        ([(26, 21), (37, 24), (41.5, 27.5), (41, 31.5), (38, 32), (26, 28)], CLAY),
        ([(15, 16.5), (27, 19.5), (31.5, 23.5), (31, 27.5), (27.5, 28), (15, 24)], SOIL),
        ([(5, 12), (16.5, 15), (21, 19), (20.5, 23), (17, 23.5), (5, 21)], CLAY),
    ]
    for pts, col in lobes:
        poly = Polygon(smooth_closed(pts, 2))
        d.shape(poly, col, INK)
        d.line(smooth(pts[:4], 2), VEGETATION, 1.35)
        d.line(smooth(pts[:4], 2), INK, .85)
        nx, ny = pts[2]
        d.arc(nx - 2.2, ny + 2.0, 2.0, -60, 110, INK)

    d.text_free_arrow(14, 8.5, 34, 15, INK, .95, 2.6)
    return d


def build_soil_creep():
    d = FieldDrawing()
    # Classic soil creep cross-section: steeply dipping strata bent downslope at surface +
    # curved pistol-butt tree + tilted fence posts (after Varnes Fig V: Soil Creep)
    bedrock = Polygon([(5, 21), (43, 34), (43, 42), (5, 42)])
    soil_zone = Polygon([(5, 13), (43, 26), (43, 34), (5, 21)])
    d.shape(bedrock, LIMESTONE, INK)
    d.shape(soil_zone, SOIL, INK)

    # Dashed transition boundary between intact bedrock and creeping soil mantle
    d.dashed([(5, 21), (43, 34)], INK, .7, 2.2, 1.4)

    # Steeply dipping bedrock strata that bend/drag downslope inside the upper soil zone
    full_slope = bedrock.union(soil_zone)
    with d.clipped(full_slope.buffer(-.35)):
        for x0 in range(7, 43, 5):
            y_mid = 21 + (x0 - 5) * (13 / 38)
            pts = [
                (x0 - 3.5, 43),
                (x0 - 1.2, y_mid + 3.5),
                (x0, y_mid),
                (x0 + 3.2, y_mid - 4.2),
                (x0 + 7.5, y_mid - 7.2),
            ]
            d.line(smooth(pts, 2), INK, .68)

    # Pistol-butt tree on upper left slope (curved lower trunk becoming vertical at crown)
    trunk = smooth([(13.5, 16.2), (16.5, 14.5), (17.0, 10.5), (17.0, 7.5)], 2)
    d.line(trunk, INK, 1.35)
    d.poly([(17.0, 3.8), (13.2, 10.5), (20.8, 10.5)], VEGETATION, INK)

    # Downslope-tilted fence posts on mid/lower slope
    d.line([(27, 20.6), (30.2, 14.2)], INK, 1.15)
    d.line([(36, 23.7), (39.8, 17.5)], INK, 1.15)

    # Slow downslope creep arrow
    d.text_free_arrow(20.5, 13.2, 32.5, 17.5, INK, .9, 2.4)
    return d


# --------------------------------------------------- 19-20: Debris/Earth Complex

def build_cambering_valley_bulging():
    d = FieldDrawing()
    # Cross-section from plateau on left to valley floor on right
    # (After Varnes Fig VI: Cambering and Valley Bulging)
    base = Polygon([(5, 38), (43, 38), (43, 42), (5, 42)])
    d.shape(base, ROCK, INK)

    # Thick plastic clay formation squeezing toward valley and folding upward into a valley-floor anticline bulge
    valley_top = smooth([
        (5, 19), (15, 20), (24, 23.5), (31, 28),
        (34.5, 24.5), (38, 21.5), (41.5, 24.5), (43, 27)
    ], 2)
    clay_body = Polygon(valley_top + [(43, 38), (5, 38)])
    d.shape(clay_body, CLAY, INK)

    # Internal clay bedding planes showing lateral squeeze and sharp anticline upwarp in the valley floor
    for y_left, arch_y in [(24.5, 24.5), (29.5, 28.0), (34.5, 32.5)]:
        pts = smooth([
            (5.5, y_left), (16, y_left + .8), (25, y_left + 2.2),
            (31.5, y_left + 3.2), (38, arch_y), (42.5, y_left + 2.5)
        ], 2)
        d.line(pts, INK, .65)

    # Cambered competent caprock (Sandstone/Limestone) draping downslope and broken by V-gulls
    gull_blocks = [
        [(5, 11), (12.2, 11.5), (11.8, 19.3), (5, 19)],
        [(13.8, 12), (20.2, 13.8), (19.2, 21.2), (13.0, 19.6)],
        [(21.8, 14.5), (27.2, 17.2), (25.5, 24.2), (20.5, 21.8)],
        [(28.5, 18.2), (32.8, 21.8), (31.0, 28.0), (26.8, 25.0)],
    ]
    for pts in gull_blocks:
        poly = Polygon(pts)
        d.shape(poly, SANDSTONE, INK)
        _bedrock_joints(d, poly, angle=15, spacing=4.0, cross_spacing=4.8, width=.55)

    # Downslope cambering arrow above caprock + upward valley-bulge arrow above anticline
    _curved_arrow(d, [(14, 7.5), (23, 9.5), (31, 14.5)], INK, .95, 2.5)
    d.text_free_arrow(38, 19.5, 38, 11.5, INK, .95, 2.5)
    return d


def build_slump_earth_flow():
    d = FieldDrawing()
    # Compound Slump–Earth Flow: upper concave scarp & back-tilted rotational slump blocks
    # transitioning downslope into a bulging ridged earth-flow lobe (after Varnes Slump-Earth Flow)
    # Left stratified clay/sand bluff
    side = Polygon([(5, 14), (15, 8), (15, 28), (5, 34)])
    base = Polygon([(5, 34), (15, 28), (43, 35), (33, 42), (5, 39)])
    d.shape(side, CLAY, INK)
    _shale_laminae(d, side, angle=-28, spacing=3.0)
    d.shape(base, SOIL, INK)

    # Upper concave main scarp
    scarp = Polygon([(15, 8), (27, 11), (25, 19), (13, 17)])
    d.shape(scarp, SAND, INK)
    for x in (17, 21, 24):
        d.line([(x, 10), (x - 1, 17)], INK, .58)

    # Stepped back-tilted rotational slump blocks in upper head region
    b1 = Polygon([(12, 17), (24, 18.5), (26, 23), (14, 21.5)])
    b2 = Polygon([(14, 21.5), (26, 23), (29, 27.5), (17, 26)])
    d.shape(b1, SANDSTONE, INK)
    d.shape(b2, SAND, INK)

    # Lower bulbous earth-flow tongue with curved transverse flow ridges
    lobe = Polygon(smooth_closed([
        (17, 25), (28, 25.5), (38, 29.5), (41.5, 34),
        (37, 39), (27, 39.5), (18, 34), (15, 29)
    ], 2))
    d.shape(lobe, CLAY, INK)
    for pts in [
        [(20, 29), (26, 28.5), (30, 31)],
        [(24, 33), (31, 32), (35, 35)],
        [(29, 36.5), (35, 35.5), (38, 37.5)],
    ]:
        d.line(smooth(pts, 2), INK, .68)

    # Clean compound movement arrow above the scarp and flow lobe (no border clash)
    _curved_arrow(d, [(28, 8.5), (33, 16), (40, 25)], INK, .95, 2.6)
    return d


# --------------------------------------------------------- 21-29: Earth -----

def build_earth_fall():
    d = FieldDrawing()
    # Vertical undercut river/terrace bank of cohesive fine-grained earth/clay
    bank = Polygon([(5, 8), (21, 8), (21.5, 16), (17.5, 23),
                    (18.5, 38), (43, 38), (43, 42), (5, 42)])
    d.shape(bank, CLAY, INK)
    _earth_texture(d, Polygon([(5, 11), (19, 11), (18.5, 38), (5, 38)]),
                   seed=211, count=12, angle=0)

    # Dark topsoil rim at top of terrace bank with open vertical desiccation tension crack
    topsoil = Polygon([(5, 8), (21, 8), (21, 11.2), (5, 11.2)])
    d.shape(topsoil, SOIL_DARK, INK)
    d.poly([(17.2, 8), (18.6, 8), (18.0, 15.5)], WHITE, INK)

    # Crumbled fine-earth talus mound at foot of bank
    mound = Polygon(smooth_closed([
        (18, 31), (24, 33), (31, 38), (18, 38)
    ], 2))
    d.shape(mound, SOIL, INK)
    _earth_texture(d, mound, seed=212, count=5, angle=15)

    # Cohesive soil clods dropping vertically from overhanging brow
    d.dashed([(21, 16), (22.5, 23), (23.5, 31)], INK, .72, 2.0, 1.3)
    d.dashed([(24, 13), (26.5, 22), (28, 33)], INK, .72, 2.0, 1.3)
    d.shape(Polygon(smooth_closed([(21, 18), (25, 17.5), (25.5, 21.5), (21.5, 22)], 1)),
            CLAY, INK, width=.75)
    d.shape(Polygon(smooth_closed([(25.5, 25), (29, 24.5), (29.5, 28), (26, 28.5)], 1)),
            SOIL, INK, width=.75)

    # Vertical fall arrow
    d.text_free_arrow(32, 11, 32, 27, INK, .95, 2.7)
    return d


def build_earth_topple():
    d = FieldDrawing()
    # Cohesive fine-grained earth/loess terrace bank with deep vertical columnar shrinkage cracks
    base = Polygon([(5, 35), (43, 37), (43, 42), (5, 42)])
    d.shape(base, SOIL_DARK, INK)

    bank = Polygon([(5, 9), (16, 9), (15.5, 35.5), (5, 35)])
    d.shape(bank, CLAY, INK)
    _earth_texture(d, bank, seed=221, count=10, angle=90)
    d.line([(10.5, 9), (10.5, 29)], INK, .65)

    # Tall cohesive earth column pivoting forward about its toe
    col1 = Polygon([(18, 10.5), (24, 12.2), (19.5, 35.8), (15.5, 35.5)])
    d.shape(col1, LOESS, INK)
    _earth_texture(d, col1, seed=222, count=6, angle=75)

    # Actively overturning earth column leaning steeply outward
    col2 = Polygon([(26.5, 14.5), (32.5, 18.2), (23.5, 36), (19.5, 35.8)])
    d.shape(col2, CLAY, INK)
    _earth_texture(d, col2, seed=223, count=6, angle=55)

    # Previously toppled cohesive earth slab lying at toe
    slab = Polygon([(24, 32.5), (40, 34), (39.5, 37), (23.5, 36)])
    d.shape(slab, LOESS, INK)

    # Forward overturning rotational arrow
    _curved_arrow(d, [(19, 6.5), (28, 8), (36, 14), (39, 23)], INK, .95, 2.7)
    return d


def build_earth_slump():
    d = FieldDrawing()
    # Rotational Earth Slump in cohesive clay (after Varnes Fig III.A: Earth Slump, ref/25.png)
    # Cohesive clay slope with steep arcuate main scarp, stepped back-tilted slumped earth blocks,
    # transverse tension cracks and bulged toe above a concave rotational slip surface
    base = Polygon([
        (5, 9), (12.5, 9),
        (14.0, 17.5), (18.5, 25.0), (26.5, 31.5), (37.5, 35.5),
        (43, 36.5), (43, 42), (5, 42),
    ])
    d.shape(base, SOIL_DARK, INK)
    _earth_texture(d, Polygon([(5, 11), (13, 18), (22, 32), (41, 36.5), (41, 41), (5, 41)]),
                   seed=226, count=10, angle=0)

    # Exposed arcuate main scarp face in upper clay bank
    scarp = Polygon([(12.5, 9), (18.5, 11.5), (17.5, 19.5), (14.0, 17.5)])
    d.shape(scarp, SAND, INK)
    for x in (14.2, 16.2):
        d.line([(x, 10.5), (x + 0.6, 17.0)], INK, .55)

    # Upper back-tilted rotational clay slump block with reverse-dipping terrace surface
    slump1 = Polygon([
        (14.0, 17.5), (23.5, 15.2), (26.2, 23.8), (18.5, 25.0),
    ])
    d.shape(slump1, CLAY, INK)
    _earth_texture(d, slump1, seed=227, count=5, angle=-14)
    d.line([(14.5, 19.5), (24.2, 17.2)], INK, .6)

    # Middle back-tilted clay slump block + transverse tension cracks
    slump2 = Polygon([
        (18.5, 25.0), (26.2, 23.8), (32.5, 22.8), (34.2, 31.2), (26.5, 31.5),
    ])
    d.shape(slump2, SOIL, INK)
    _earth_texture(d, slump2, seed=228, count=5, angle=-10)
    d.line([(28.5, 23.3), (27.2, 27.8)], INK, .65)

    # Bulging earth toe lobe with radial/transverse toe cracks
    toe = Polygon(smooth_closed([
        (26.5, 31.5), (34.2, 27.5), (41.2, 31.0), (42.2, 35.8), (35.5, 36.2),
    ], 2))
    d.shape(toe, CLAY, INK)
    d.line(smooth([(33.5, 30.2), (37.5, 30.8), (40.2, 33.5)], 2), INK, .65)

    # Prominent dashed concave rotational slip surface + rotational arrow
    slip = smooth([(12.5, 9.2), (14.5, 18.2), (20.0, 26.2), (29.5, 32.8), (41.0, 35.8)], 2)
    d.dashed(slip, INK, .85, 2.2, 1.3)
    _curved_arrow(d, [(22, 8.5), (31, 12.5), (38, 21.5)], INK, .95, 2.7)
    return d


def build_earth_block_slide():
    d = FieldDrawing()
    # Translational Earth Block Slide with rear graben & planar basal sensitive-clay seam
    # (After Varnes Fig III.B: Earth Block Slide)
    base = Polygon([(5, 33), (43, 35.5), (43, 42), (5, 42)])
    d.shape(base, SOIL_DARK, INK)

    # Thin planar soft/sensitive clay slip horizon
    seam = Polygon([(11, 30.5), (42, 32.8), (42, 35.5), (11, 33.2)])
    d.shape(seam, SHALE, INK)

    # Left undisturbed cohesive clay bluff (main scarp)
    left_bluff = Polygon([(5, 12), (12, 12), (14, 30.8), (5, 33)])
    d.shape(left_bluff, CLAY, INK)
    _earth_texture(d, left_bluff, seed=231, count=7, angle=0)

    # Sunken counter-scarp graben block dropped between main scarp and sliding block
    graben = Polygon([(12.8, 17.5), (20.5, 18), (19.5, 31.2), (14, 30.8)])
    d.shape(graben, SOIL, INK)
    d.line([(12.8, 21), (20.3, 21.5)], INK, .6)

    # Coherent horizontal earth block translating right as an intact tabular prism
    block_body = Polygon([(21, 13.5), (36.5, 14.5), (38, 32.5), (19.5, 31.2)])
    d.shape(block_body, CLAY, INK)
    _earth_texture(d, block_body, seed=232, count=10, angle=3)
    d.line([(20.8, 17.5), (36.7, 18.5)], INK, .65)

    # Compressed pressure-ridge bulge at the right toe
    bulge = Polygon(smooth_closed([
        (36.8, 24), (41.5, 26), (43, 33), (38, 32.5)
    ], 2))
    d.shape(bulge, SOIL, INK)

    # Bold horizontal translational movement arrow
    d.text_free_arrow(22, 8.5, 36, 9.5, INK, .95, 2.7)
    return d


def build_earth_lateral_spread():
    d = FieldDrawing()
    # Firm clayey gravel substrate at base (after Varnes Fig IV: Earth Lateral Spread)
    gravel_base = Polygon([(5, 35), (43, 36.5), (43, 42), (5, 42)])
    d.shape(gravel_base, CONGLOMERATE, INK)
    _debris_clasts(d, gravel_base, seed=241, count=8, min_r=1.1, max_r=1.5, spacing=3.5)

    # Liquefied water-bearing soft silt and sand layer (WATER fill with flow streaks)
    liquefied = Polygon([(5, 28), (41, 29.5), (43, 36.5), (5, 35)])
    d.shape(liquefied, WATER, INK)
    for y in (30.8, 33.2):
        d.dashed([(7, y), (40, y + 1.2)], INK, .6, 2.5, 1.5)

    # Upper firm clay broken into sharp tilted horst/graben prism blocks spreading over liquefied seam
    blocks = [
        ([(5, 15), (12, 15), (13, 28.2), (5, 28)], CLAY),
        ([(12.5, 18.5), (18, 18.8), (16.5, 28.5), (13, 28.2)], SOIL),
        ([(17.2, 15.5), (23.5, 16), (24.5, 28.8), (16.5, 28.5)], CLAY),
        ([(24, 19), (29.5, 19.5), (28.5, 29), (24.5, 28.8)], SOIL),
        ([(29, 16.8), (35, 18), (35.5, 29.3), (28.5, 29)], CLAY),
        ([(35.2, 20.5), (40.5, 22.5), (41.5, 29.5), (35.5, 29.3)], SOIL),
    ]
    for pts, col in blocks:
        d.shape(Polygon(pts), col, INK)

    # Lateral spreading arrow
    d.text_free_arrow(16, 10, 36, 11, INK, .95, 2.7)
    return d


def build_wet_sand_silt_flow():
    d = FieldDrawing()
    # Coastal/shoreline sand bank meeting a horizontal water body, with a liquefied wet sand-silt
    # density flow tongue sliding subaqueously beneath the water (after Varnes Wet Sand or Silt Flow)
    # Water body on right with horizontal waterline at y=16.5
    water_body = Polygon([(16, 16.5), (43, 16.5), (43, 37), (16, 22)])
    d.shape(water_body, WATER, INK)
    # Horizontal water-surface ripples
    d.dashed([(22, 19.8), (41, 19.8)], INK, .55, 2.8, 1.8)
    d.dashed([(28, 23.2), (41, 23.2)], INK, .55, 2.8, 1.8)

    # Clean sand coastal bank on left with scalloped shoreline liquefaction scar
    sand_bank = Polygon([
        (5, 11), (15, 11), (17, 18), (24, 27), (43, 36), (43, 42), (5, 42)
    ])
    d.shape(sand_bank, SAND, INK)
    _earth_texture(d, sand_bank, seed=251, count=11, angle=14)

    # Fluid wet sand-silt flow tongue slumping from shoreline scar and flowing along submerged bed
    flow_tongue = Polygon(smooth_closed([
        (14.5, 13.5), (19, 17.5), (29, 25.0), (39, 30.8),
        (41.5, 34.5), (37, 36.5), (24, 31.5), (15.5, 22)
    ], 2))
    d.shape(flow_tongue, ALLUVIUM, INK)
    # Internal laminar flow lines and suspended sand-silt streaks
    d.line(smooth([(17, 19.0), (26, 26.0), (36, 31.8)], 2), INK, .62)
    d.line(smooth([(19, 22.8), (27, 28.8), (35, 33.8)], 2), INK, .62)

    # Movement arrow above the shoreline scar / water surface (no crossing of the waterline)
    d.text_free_arrow(19, 8.5, 36, 13.5, INK, .95, 2.6)
    return d


def build_quick_clay_flow():
    d = FieldDrawing()
    # Oblique sensitive-clay terrace cut by a river at front, with a wide circular/pear-shaped
    # retrogressive crater emptying through a tight pinched bottleneck (after Varnes Quick Clay Flow)
    terrace_top = Polygon([(5, 17), (22, 7), (43, 16), (26, 28)])
    terrace_bluff = Polygon([(5, 17), (26, 28), (26, 35), (5, 24)])
    d.shape(terrace_top, CLAY, INK)
    d.shape(terrace_bluff, SHALE, INK)

    # River channel at foot of terrace bluff
    river = Polygon([(5, 24), (26, 35), (43, 23), (43, 33), (27, 43), (5, 31)])
    d.shape(river, WATER, INK)

    # Retrogressive pear-shaped quick-clay crater with tightly pinched bottleneck exit at bluff
    crater = Polygon(smooth_closed([
        (11, 15.5), (21, 9.5), (33, 12.5), (35, 18.5),
        (28, 22.5), (24.2, 24.2),                     # Right bottleneck pinch
        (28, 29), (34, 33), (26, 39), (17, 34.5),     # Liquefied clay lobe spilling into river
        (20.5, 25.5), (17.5, 22), (11.5, 19.5)        # Left bottleneck pinch & wide crater rim
    ], 2))
    d.shape(crater, ALLUVIUM, INK)

    # Concentric stepped retrogressive clay ribs inside crater bowl
    for pts in [
        [(15, 16), (22, 12.5), (30, 15)],
        [(16.5, 19), (22.5, 15.8), (29.5, 18)],
        [(18.5, 21.5), (23, 19.2), (27, 20.5)],
    ]:
        d.line(smooth(pts, 2), INK, .68)

    # Flow arrow squeezing through the narrow bottleneck into the river lobe
    _curved_arrow(d, [(22.5, 14.5), (22.3, 23.5), (26, 33.5)], INK, .95, 2.6)
    return d


def build_earth_flow():
    d = FieldDrawing()
    # Classic hourglass Earth Flow: wide circular source bowl, very narrow middle chute track,
    # and fat bulbous multi-ridged accumulation lobe (after Varnes Fig V: Earth Flow)
    _oblique_slope(d, slope_fill=TUFF, side_fill=SOIL_DARK, front_fill=SOIL, jointed_side=False)

    # Pronounced hourglass silhouette: wide bowl -> narrow waist -> wide bulbous toe lobe
    hourglass = Polygon(smooth_closed([
        (11, 13.5), (18, 9.0), (24.5, 11.8), (23.5, 16.5),  # Wide upper source bowl
        (22.2, 19.8), (24.5, 22.5),                         # Narrow constricted waist (right)
        (33, 24.5), (38.5, 28.5), (36.5, 33.5),             # Wide bulbous toe lobe (right)
        (28, 35.0), (20.5, 31.5), (20.0, 26.5),             # Wide bulbous toe lobe (left)
        (19.2, 21.2), (17.5, 18.8),                         # Narrow constricted waist (left)
        (12, 17.8), (10.5, 15.5)                            # Left rim of source bowl
    ], 2))
    d.shape(hourglass, CLAY, INK)

    # Arcuate headscarp in upper source bowl + convex transverse flow wrinkles on bulbous toe lobe
    d.line(smooth([(13, 14.5), (18, 11.2), (22.5, 13.5)], 2), INK, .72)
    for pts in [
        [(22, 27.5), (28, 26), (34, 28.5)],
        [(23.5, 30.5), (29.5, 29), (35.5, 31)],
        [(26, 33), (31, 32), (34.5, 33.2)],
    ]:
        d.line(smooth(pts, 2), INK, .68)

    # Downslope movement arrow along upper-right flank (well clear of block rim)
    d.text_free_arrow(26.5, 6.8, 39.5, 19.2, INK, .95, 2.6)
    return d


def build_loess_flow():
    d = FieldDrawing()
    # Stepped agricultural/loess terrace hillside on left + vertical arcuate earthquake scarp +
    # rapid dry loess sheet flooding the valley and damming a flank Lake (after Varnes Loess Flow)
    # Stepped staircase profile of terraced loess hill on left, descending to valley on right
    terraced_hill = Polygon([
        (5, 13), (12, 13), (12, 16.5),
        (18, 16.5), (18, 20),
        (24, 20), (24, 24),
        (43, 28), (43, 42), (5, 42)
    ])
    d.shape(terraced_hill, LOESS, INK)
    # Vertical loess cleavage ticks on terrace risers and basal soil lines
    for x, y0, y1 in [(8, 13, 18), (15, 16.5, 21), (21, 20, 24.5)]:
        d.line([(x, y0), (x, y1)], INK, .58)

    # Ponded blue valley Lake at right dammed by the loess flow lobe (as in Varnes diagram)
    lake = Polygon(smooth_closed([
        (31, 23), (41, 22), (43, 27.5), (36, 30), (30, 26.5)
    ], 2))
    d.shape(lake, WATER, INK)

    # Broad fluidized loess flow sheet sweeping from the terraced scarp across the valley floor
    flow = Polygon(smooth_closed([
        (15, 21), (22, 21), (29, 26), (38, 31),
        (40, 36.5), (32, 39), (20, 36.5), (13, 29), (12, 24)
    ], 2))
    d.shape(flow, SAND, INK)
    d.dashed([(16, 25), (25, 30), (35, 34.5)], INK, .62, 2.2, 1.4)
    d.dashed([(19, 23.5), (28, 28.5), (37, 33)], INK, .62, 2.2, 1.4)

    # Rapid earthquake-loess flow arrow
    d.text_free_arrow(24, 13, 36, 20, INK, .95, 2.6)
    return d


def build_dry_sand_flow():
    d = FieldDrawing()
    # 3-layer cliff cross-section/oblique step: upper Dry Sand, middle vertical Firm Silt cliff,
    # lower Sand base + V-funnel notch feeding a conical angle-of-repose dry sand talus cone
    # (After Varnes Fig V: Dry Sand Flow)
    lower_sand = Polygon([(5, 29), (43, 33), (43, 42), (5, 42)])
    firm_silt = Polygon([(5, 17), (27, 19), (27, 31.2), (5, 29)])
    dry_sand = Polygon([(5, 9), (17, 10), (20, 18.2), (24, 10.8), (27, 11), (27, 19), (5, 17)])
    d.shape(lower_sand, ALLUVIUM, INK)
    d.shape(firm_silt, CLAY, INK)
    # Prominent vertical columnar silt joints across the middle Firm Silt cliff band
    for x in (9, 13, 17, 25):
        d.line([(x, 17.5), (x, 29.5)], INK, .6)
    d.shape(dry_sand, SAND, INK)
    _earth_texture(d, dry_sand, seed=290, count=6, angle=5)

    # Sharp triangular/conical angle-of-repose dry sand fan pouring through the V-funnel notch
    sand_cone = Polygon([
        (18, 12.5), (22.5, 13), (23.5, 20.5),
        (38, 34.5), (34, 38.5), (17, 36.5), (19.5, 20.5)
    ])
    sand_cone = Polygon(smooth_closed(list(sand_cone.exterior.coords)[:-1], 1))
    d.shape(sand_cone, SAND, INK)

    # Radial dry grain-flow lines & sand stipples on the conical fan
    d.dashed([(21.5, 19), (22, 34.5)], INK, .62, 2.0, 1.3)
    d.dashed([(22.2, 19), (28, 35.5)], INK, .62, 2.0, 1.3)
    d.dashed([(22.8, 19), (33.5, 34.5)], INK, .62, 2.0, 1.3)
    _earth_texture(d, sand_cone, seed=291, count=9, angle=65)

    # Steep grain-cascade arrow above the conical sand fan
    d.text_free_arrow(30, 13, 37, 27, INK, .95, 2.6)
    return d


# ------------------------------------------------------------------- ROWS --

REF_BEDROCK = 'FGM Landslide classification (after Varnes) - bedrock'
REF_DEBRIS = 'FGM Landslide classification (after Varnes) - debris'
REF_EARTH = 'FGM Landslide classification (after Varnes) - earth'
REF_COMPLEX = 'FGM Landslide classification (after Varnes) - complex'

ROWS = [
    ('gl_rock_fall', 'Rock Fall',
     'Jointed bedrock cliff shedding free-falling and bouncing angular rock blocks onto a basal talus wedge.',
     REF_BEDROCK, build_rock_fall),
    ('gl_rock_topple', 'Rock Topple',
     'Steeply dipping jointed rock columns pivoting and overturning forward about their toe.',
     REF_BEDROCK, build_rock_topple),
    ('gl_rock_slump', 'Rock Slump',
     'Stratified sandstone-over-shale blocks back-tilting along a concave rotational rupture surface.',
     REF_BEDROCK, build_rock_slump),
    ('gl_rock_block_slide', 'Rock Block Slide',
     'Coherent jointed rock slab translating downslope along an inclined planar bedding surface.',
     REF_BEDROCK, build_rock_block_slide),
    ('gl_rock_lateral_spread', 'Rock Lateral Spread',
     'Fractured bedrock caprock separating into horst and graben blocks over a ductile squeezing shale layer.',
     REF_BEDROCK, build_rock_lateral_spread),
    ('gl_rock_creep_sackung', 'Rock Creep (Sackung)',
     'Deep-seated gravitational sagging of a foliated mountain ridge with a double-crested graben and lower-slope bulge.',
     REF_BEDROCK, build_rock_creep_sackung),
    ('gl_rock_fall_debris_flow', 'Rock Fall–Debris Flow',
     'High mountain rock-fall scar feeding a rapid clast-rich debris-avalanche runout lobe across a valley floor.',
     REF_COMPLEX, build_rock_fall_debris_flow),
    ('gl_slump_topple', 'Slump and Topple',
     'Rotational sandstone-over-shale slump block with vertically jointed columns toppling forward from its brow.',
     REF_COMPLEX, build_slump_topple),
    ('gl_rock_slide_rock_fall', 'Rock Slide–Rock Fall',
     'Translational rock slab sliding down an upper inclined ramp and plunging as a rock fall over a lower cliff.',
     REF_COMPLEX, build_rock_slide_rock_fall),
    ('gl_debris_fall', 'Debris Fall',
     'Undercut coarse boulder-gravel bluff shedding angular clasts and matrix fragments onto a talus cone.',
     REF_DEBRIS, build_debris_fall),
    ('gl_debris_topple', 'Debris Topple',
     'Vertical columns of coarse clayey gravel tilting and toppling forward over a basal sand layer.',
     REF_DEBRIS, build_debris_topple),
    ('gl_debris_slump', 'Debris Slump',
     'Coarse clast-rich colluvium rotating along a concave slip surface above bedrock.',
     REF_DEBRIS, build_debris_slump),
    ('gl_debris_slide', 'Debris Slide',
     'Sheet of coarse angular colluvial debris sliding translationally down an inclined planar bedrock surface.',
     REF_DEBRIS, build_debris_slide),
    ('gl_debris_flow', 'Debris Flow',
     'Channelised flow bordered by lateral levees expanding into a boulder-rich lobate tongue on an apron.',
     REF_DEBRIS, build_debris_flow),
    ('gl_debris_avalanche', 'Debris Avalanche',
     'Broad open-slope bedrock scar feeding a wide rapid sheet of chaotic coarse debris down a steep mountain face.',
     REF_DEBRIS, build_debris_avalanche),
    ('gl_block_stream', 'Block Stream',
     'Sinuous valley-floor stream of coarse imbricated angular boulders creeping down a slope.',
     REF_DEBRIS, build_block_stream),
    ('gl_solifluction', 'Solifluction',
     'Overlapping tongue-shaped turf-banked lobes creeping down a gentle slope above frozen ground.',
     REF_DEBRIS, build_solifluction),
    ('gl_soil_creep', 'Soil Creep',
     'Steeply dipping strata bent downslope in the surface soil mantle beneath a pistol-butt tree and tilted posts.',
     REF_DEBRIS, build_soil_creep),
    ('gl_cambering_valley_bulging', 'Cambering and Valley Bulging',
     'Cambered caprock broken by tension gulls draping over plastic clay that squeezes into an upward valley-floor bulge.',
     REF_COMPLEX, build_cambering_valley_bulging),
    ('gl_slump_earth_flow', 'Slump–Earth Flow',
     'Back-tilted rotational slump blocks at the head transitioning downslope into a ridged lobate earth flow.',
     REF_COMPLEX, build_slump_earth_flow),
    ('gl_earth_fall', 'Earth Fall',
     'Vertical cohesive soil bank with a top tension crack dropping detached earth clods onto a basal mound.',
     REF_EARTH, build_earth_fall),
    ('gl_earth_topple', 'Earth Topple',
     'Cohesive columnar earth bank split by vertical shrinkage fissures with columns pivoting outward about the base.',
     REF_EARTH, build_earth_topple),
    ('gl_earth_slump', 'Earth Slump',
     'Cohesive clay slope with a concave rotational slip surface, arcuate main scarp, back-tilted slump blocks and bulged toe.',
     REF_EARTH, build_earth_slump),
    ('gl_earth_block_slide', 'Earth Block Slide',
     'Coherent tabular clay block translating along a planar basal slip seam with a sunken rear graben and toe bulge.',
     REF_EARTH, build_earth_block_slide),
    ('gl_earth_lateral_spread', 'Earth Lateral Spread',
     'Firm clay layer fracturing into tilted horst and graben prisms spreading laterally over a liquefied water-bearing seam.',
     REF_EARTH, build_earth_lateral_spread),
    ('gl_wet_sand_silt_flow', 'Wet Sand or Silt Flow',
     'Shoreline sand bank liquefying at the waterline into a fluid subaqueous sand-silt sheet flow.',
     REF_EARTH, build_wet_sand_silt_flow),
    ('gl_quick_clay_flow', 'Quick Clay Flow',
     'Retrogressive pear-shaped clay crater with concentric ribs emptying through a narrow bottleneck into a river channel.',
     REF_EARTH, build_quick_clay_flow),
    ('gl_earth_flow', 'Earth Flow',
     'Hourglass-shaped landslide with an upper source bowl, narrow chute track, and bulbous ridged accumulation lobe.',
     REF_EARTH, build_earth_flow),
    ('gl_loess_flow', 'Loess Flow',
     'Stepped terraced loess hill shedding a rapid dry sheet flow across a valley floor and damming a flank lake.',
     REF_EARTH, build_loess_flow),
    ('gl_dry_sand_flow', 'Dry Sand Flow',
     'Upper dry sand bed cascading through a V-funnel notch across a vertical silt cliff onto a conical sand fan.',
     REF_EARTH, build_dry_sand_flow),
]
