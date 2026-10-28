"""Detailed technical glyphs, independent of the simplified flat SVG artwork.

Keep raypaths, electrodes, field lines, crystal faces, rock textures, chart
boundaries and instrument components in the font. Fit each composition to a
shared optical envelope without distorting its proportions or deleting detail.
"""

from shapely import affinity

from geom_utils import (
    circle, disk_ring, ellipse_outline, line, poly, regular_poly,
    rounded_rect_outline, stroke, union_all,
)


def fluid_inclusion():
    # An outlined host is essential: a filled hexagon hides the entire inclusion.
    host = regular_poly(500, 500, 410, 6, 30)
    return union_all([
        host.boundary.buffer(17, join_style=1),
        ellipse_outline(500, 500, 240, 160, 34, angle_deg=-15),
        disk_ring(580, 520, 62, 24),
        circle(580, 520, 15),
        regular_poly(410, 460, 42, 4, 15).boundary.buffer(12, join_style=1),
        line(255, 650, 300, 690, 22),
        line(700, 310, 745, 350, 22),
    ])


def mineral_cluster():
    parts = [
        stroke([(100, 150), (100, 260), (230, 300), (370, 260),
                (510, 300), (680, 260), (810, 300), (900, 260),
                (900, 150), (100, 150)], 32),
        line(180, 210, 280, 210, 24),
        line(380, 195, 480, 195, 24),
        line(650, 210, 780, 210, 24),
    ]
    # Smaller needles sit behind three faceted main prisms. Clear negative space
    # keeps face edges and horizontal growth striations visible in one colour.
    for x, bottom, top, width in [
        (155, 300, 520, 75), (840, 300, 540, 75),
        (290, 320, 730, 145), (710, 320, 760, 145),
        (500, 320, 920, 170),
    ]:
        shoulder = top - width * .9
        outline = [(x - width / 2, bottom), (x - width / 2, shoulder),
                   (x, top), (x + width / 2, shoulder),
                   (x + width / 2, bottom)]
        parts.extend([
            stroke(outline, 30, closed=True),
            line(x, bottom, x, top, 22),
            stroke([(x - width / 2, shoulder), (x, shoulder - width * .3),
                    (x + width / 2, shoulder)], 22),
        ])
        if width > 100:
            for height in (bottom + 100, bottom + 190):
                parts.append(line(x - width * .35, height, x - width * .12, height, 20))
    return union_all(parts)


OVERRIDES = {
    "gc_fluid_inclusion_microtherm": fluid_inclusion,
    "gl_minerals_specimen": mineral_cluster,
}


FOLD_ATTITUDE_IDS = {
    'gl_fold_upright_horizontal', 'gl_fold_upright_plunging',
    'gl_fold_vertical', 'gl_fold_inclined_plunging',
    'gl_fold_overturned_horizontal', 'gl_fold_overturned_plunging',
    'gl_fold_recumbent', 'gl_fold_reclined',
}


def detailed_font_geometry(icon):
    builder = OVERRIDES.get(icon["id"], icon["builder"])
    geometry = builder()
    if icon['id'] not in FOLD_ATTITUDE_IDS:
        geometry = geometry.buffer(0)
    if geometry.is_empty or not geometry.is_valid:
        raise ValueError(f"Invalid detailed artwork: {icon['id']}")
    # Sub-unit corner cleanup removes brittle polygon tips without thinning
    # instrument marks, plot ticks, dashed paths or fine lithological textures.
    # Repair can incorrectly fill gaps in these detailed fold traces.
    if icon['id'] not in FOLD_ATTITUDE_IDS:
        geometry = geometry.buffer(.65, quad_segs=4, join_style=1).buffer(-.65, quad_segs=4, join_style=1)
    x0, y0, x1, y1 = geometry.bounds
    factor = 880 / max(x1 - x0, y1 - y0)
    geometry = affinity.translate(geometry, xoff=-(x0 + x1) / 2, yoff=-(y0 + y1) / 2)
    geometry = affinity.scale(geometry, xfact=factor, yfact=factor, origin=(0, 0))
    return affinity.translate(geometry, xoff=500, yoff=500)
