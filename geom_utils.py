"""
Geometric primitives and constructive solid geometry (CSG) utilities
for building clean, crisp TrueType (TTF) and SVG vector icons on a 1000x1000 canvas.
Coordinate system: x in [0, 1000] (left to right), y in [0, 1000] (bottom to top).
"""

import math
from typing import Iterable, List, Sequence, Tuple, Union
import numpy as np
from shapely.geometry import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPolygon,
    Point,
    Polygon,
    box,
)
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely import affinity

GeomType = Union[Polygon, MultiPolygon, GeometryCollection]
Point2D = Tuple[float, float]


def union_all(geoms: Iterable[GeomType]) -> GeomType:
    """Boolean union of a list of geometries."""
    valid = [g for g in geoms if g is not None and not g.is_empty]
    if not valid:
        return Polygon()
    return unary_union(valid)


def diff(base: GeomType, *cutters: GeomType) -> GeomType:
    """Boolean subtraction: base - union(cutters)."""
    cut = union_all(cutters)
    if cut.is_empty:
        return base
    return base.difference(cut)


def intersect(a: GeomType, b: GeomType) -> GeomType:
    """Boolean intersection of two geometries."""
    return a.intersection(b)


def circle(cx: float, cy: float, r: float, segs: int = 32) -> Polygon:
    """Filled circle at (cx, cy) with radius r."""
    return Point(cx, cy).buffer(r, quad_segs=segs)


def ring(cx: float, cy: float, r_outer: float, width: float, segs: int = 32) -> Polygon:
    """Stroked circle / annulus with outer radius r_outer and stroke thickness width."""
    outer = Point(cx, cy).buffer(r_outer, quad_segs=segs)
    inner = Point(cx, cy).buffer(max(0.0, r_outer - width), quad_segs=segs)
    return outer.difference(inner)


def disk_ring(cx: float, cy: float, r_center: float, width: float, segs: int = 32) -> Polygon:
    """Circle centered at radius r_center with stroke width."""
    return ring(cx, cy, r_center + width / 2.0, width, segs=segs)


def rect(x0: float, y0: float, x1: float, y1: float) -> Polygon:
    """Filled axis-aligned rectangle from (x0, y0) to (x1, y1)."""
    return box(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def rect_outline(x0: float, y0: float, x1: float, y1: float, width: float, join_style: int = 2) -> GeomType:
    """Stroked axis-aligned rectangle centered on its boundary."""
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    return LineString(pts).buffer(width / 2.0, cap_style=3, join_style=join_style)


def rounded_rect(x0: float, y0: float, x1: float, y1: float, radius: float) -> GeomType:
    """Filled rounded rectangle."""
    r = min(radius, abs(x1 - x0) / 2.0 - 1, abs(y1 - y0) / 2.0 - 1)
    if r <= 0:
        return rect(x0, y0, x1, y1)
    inner = box(min(x0, x1) + r, min(y0, y1) + r, max(x0, x1) - r, max(y0, y1) - r)
    return inner.buffer(r, quad_segs=16)


def rounded_rect_outline(x0: float, y0: float, x1: float, y1: float, radius: float, width: float) -> GeomType:
    """Stroked rounded rectangle with stroke thickness width."""
    outer = rounded_rect(x0 - width / 2, y0 - width / 2, x1 + width / 2, y1 + width / 2, radius + width / 2)
    inner = rounded_rect(x0 + width / 2, y0 + width / 2, x1 - width / 2, y1 - width / 2, max(0.0, radius - width / 2))
    return outer.difference(inner)


def poly(pts: Sequence[Point2D]) -> Polygon:
    """Filled polygon from sequence of (x, y) vertices."""
    return Polygon(pts).buffer(0)


def regular_poly(cx: float, cy: float, r: float, n: int, start_angle_deg: float = 90.0) -> Polygon:
    """Filled regular n-gon."""
    pts = []
    for i in range(n):
        ang = math.radians(start_angle_deg + i * 360.0 / n)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return Polygon(pts).buffer(0)


def stroke(
    pts: Sequence[Point2D],
    width: float = 36.0,
    cap: str = "round",
    join: str = "round",
    closed: bool = False,
) -> GeomType:
    """Stroke a polyline or closed loop with specified width, cap, and join style."""
    cap_map = {"round": 1, "flat": 2, "butt": 2, "square": 3}
    join_map = {"round": 1, "mitre": 2, "miter": 2, "bevel": 3}
    pts_list = list(pts)
    if closed and pts_list[0] != pts_list[-1]:
        pts_list.append(pts_list[0])
    ls = LineString(pts_list)
    return ls.buffer(
        width / 2.0,
        quad_segs=16,
        cap_style=cap_map.get(cap, 1),
        join_style=join_map.get(join, 1),
    )


def line(x0: float, y0: float, x1: float, y1: float, width: float = 36.0, cap: str = "round") -> GeomType:
    """Single stroked line segment."""
    return stroke([(x0, y0), (x1, y1)], width=width, cap=cap)


def dashed_line(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    width: float = 30.0,
    dash_count: int = 5,
    duty: float = 0.55,
    cap: str = "round",
) -> GeomType:
    """Dashed line segment between (x0, y0) and (x1, y1)."""
    segs = []
    for i in range(dash_count):
        t0 = (i + (1 - duty) / 2.0) / dash_count
        t1 = (i + 1 - (1 - duty) / 2.0) / dash_count
        sx0 = x0 + (x1 - x0) * t0
        sy0 = y0 + (y1 - y0) * t0
        sx1 = x0 + (x1 - x0) * t1
        sy1 = y0 + (y1 - y0) * t1
        segs.append(line(sx0, sy0, sx1, sy1, width=width, cap=cap))
    return union_all(segs)


def arc(
    cx: float,
    cy: float,
    r: float,
    start_deg: float,
    end_deg: float,
    width: float = 36.0,
    cap: str = "round",
    steps: int = 48,
) -> GeomType:
    """Stroked circular arc from start_deg to end_deg (counter-clockwise in degrees)."""
    angles = np.linspace(math.radians(start_deg), math.radians(end_deg), max(8, steps))
    pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in angles]
    return stroke(pts, width=width, cap=cap)


def sector(
    cx: float,
    cy: float,
    r: float,
    start_deg: float,
    end_deg: float,
    steps: int = 48,
) -> Polygon:
    """Filled circular sector (pie wedge)."""
    angles = np.linspace(math.radians(start_deg), math.radians(end_deg), max(8, steps))
    pts = [(cx, cy)] + [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in angles] + [(cx, cy)]
    return Polygon(pts).buffer(0)


def ellipse(cx: float, cy: float, rx: float, ry: float, angle_deg: float = 0.0, segs: int = 32) -> GeomType:
    """Filled ellipse centered at (cx, cy) with radii (rx, ry), rotated by angle_deg."""
    c = Point(0, 0).buffer(1.0, quad_segs=segs)
    e = affinity.scale(c, rx, ry)
    if angle_deg != 0.0:
        e = affinity.rotate(e, angle_deg, origin=(0, 0))
    return affinity.translate(e, cx, cy)


def ellipse_outline(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    width: float = 34.0,
    angle_deg: float = 0.0,
    steps: int = 64,
) -> GeomType:
    """Stroked ellipse outline."""
    angles = np.linspace(0, 2 * math.pi, steps)
    pts = [(rx * math.cos(a), ry * math.sin(a)) for a in angles]
    s = stroke(pts, width=width, closed=True)
    if angle_deg != 0.0:
        s = affinity.rotate(s, angle_deg, origin=(0, 0))
    return affinity.translate(s, cx, cy)


def arrow_head(
    tip_x: float,
    tip_y: float,
    angle_deg: float,
    length: float = 95.0,
    half_width: float = 55.0,
) -> Polygon:
    """Filled triangular arrowhead with tip at (tip_x, tip_y) pointing in direction angle_deg."""
    rad = math.radians(angle_deg)
    dx, dy = math.cos(rad), math.sin(rad)
    px, py = -dy, dx
    bx = tip_x - dx * length
    by = tip_y - dy * length
    p1 = (tip_x, tip_y)
    p2 = (bx + px * half_width, by + py * half_width)
    p3 = (bx - px * half_width, by - py * half_width)
    return Polygon([p1, p2, p3]).buffer(6, join_style=1)


def arrow(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    width: float = 36.0,
    head_len: float = 95.0,
    head_half_width: float = 55.0,
    both_ends: bool = False,
) -> GeomType:
    """Stroked line with filled arrowhead at (x1, y1), and optionally at (x0, y0)."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    rad = math.radians(ang)
    sx1 = x1 - math.cos(rad) * (head_len * 0.65)
    sy1 = y1 - math.sin(rad) * (head_len * 0.65)
    sx0, sy0 = x0, y0
    parts = [arrow_head(x1, y1, ang, head_len, head_half_width)]
    if both_ends:
        sx0 = x0 + math.cos(rad) * (head_len * 0.65)
        sy0 = y0 + math.sin(rad) * (head_len * 0.65)
        parts.append(arrow_head(x0, y0, ang + 180.0, head_len, head_half_width))
    parts.append(line(sx0, sy0, sx1, sy1, width=width, cap="round"))
    return union_all(parts)


def curved_arrow(
    cx: float,
    cy: float,
    r: float,
    start_deg: float,
    end_deg: float,
    width: float = 34.0,
    head_len: float = 90.0,
    head_half_width: float = 52.0,
) -> GeomType:
    """Circular arc with an arrowhead at end_deg."""
    direction = 1.0 if end_deg >= start_deg else -1.0
    trim_deg = math.degrees((head_len * 0.55) / max(r, 1.0)) * direction
    arc_geom = arc(cx, cy, r, start_deg, end_deg - trim_deg, width=width, cap="round")
    end_rad = math.radians(end_deg)
    tx = cx + r * math.cos(end_rad)
    ty = cy + r * math.sin(end_rad)
    tangent_deg = end_deg + (90.0 if direction > 0 else -90.0)
    head = arrow_head(tx, ty, tangent_deg, head_len, head_half_width)
    return union_all([arc_geom, head])


def sine_wave(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    amp: float = 40.0,
    cycles: float = 2.0,
    phase_deg: float = 0.0,
    width: float = 32.0,
    steps: int = 80,
) -> GeomType:
    """Stroked sine wave along the segment from (x0, y0) to (x1, y1)."""
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    if length < 1e-3:
        return Polygon()
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    phase = math.radians(phase_deg)
    pts = []
    for i in range(steps + 1):
        t = i / steps
        offset = amp * math.sin(2 * math.pi * cycles * t + phase)
        px = x0 + dx * t + nx * offset
        py = y0 + dy * t + ny * offset
        pts.append((px, py))
    return stroke(pts, width=width, cap="round")


def clean_for_ttf(geom: GeomType, simplify_tol: float = 0.75) -> List[Polygon]:
    """
    Normalize arbitrary shapely geometry into a list of clean, non-self-intersecting
    Polygons oriented for TrueType (exterior CW, interiors CCW).
    """
    if geom is None or geom.is_empty:
        return []
    g = geom.buffer(0)
    if simplify_tol > 0:
        g = g.simplify(simplify_tol, preserve_topology=True).buffer(0)

    polys: List[Polygon] = []
    if isinstance(g, Polygon):
        polys = [g]
    elif isinstance(g, (MultiPolygon, GeometryCollection)):
        for sub in g.geoms:
            if isinstance(sub, Polygon) and not sub.is_empty:
                polys.append(sub)
    result: List[Polygon] = []
    for p in polys:
        if p.area < 25.0:  # Filter tiny sliver artifacts
            continue
        result.append(orient(p, sign=-1.0))
    return result
