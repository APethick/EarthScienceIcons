"""Shared drawing kit for the Field Geologists' Manual (FGM) icon family.

Reference: Berkman, D. A. (ed.) Field Geologists' Manual, 4th edition,
Australasian Institute of Mining and Metallurgy (AusIMM) Monograph 9.

Every FGM icon is a 48-unit, Y-down drawing built with :class:`FieldDrawing`.
The same parts generate the detailed monochrome font outline (ink only, with
filled faces knocking out what lies beneath) and the flat natural-colour SVG
(faces filled with material colours, ink on top). No lettering is drawn.

Conventions
-----------
* Keep artwork inside roughly x 3..45, y 4..44; it is re-centred and scaled.
* Outline weight: 0.95 (default) for main outlines, 0.55-0.75 for texture.
* ``FieldDrawing.clipped(region)`` clips texture parts to a swatch, block face
  or diagram field, so patterns never spill over their frame.
* ``scatter`` and ``rng`` are deterministic; artwork never changes between
  builds.
"""
import math
import random
from contextlib import contextmanager
from functools import lru_cache

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

from icons_geophysics_expanded import native
from icons_mt import (Drawing, INK, STEEL, ALU, COPPER, SOIL, SAND, ROCK, GLASS,
                      BLUE, RED, YELLOW, PAPER, GRID)

# ---------------------------------------------------------------- palette --
# Representative natural colours, consistent with the 2.6 geochemistry family.
WHITE = '#FFFFFF'
QUARTZ = '#DCE5E4'
FELDSPAR = '#CFABA0'
PLAGIOCLASE = '#E1E1D8'
OLIVINE = '#93A35A'
PYROXENE = '#596F60'
HORNBLENDE = '#3F4B44'
GRANITE = '#C9877C'      # map convention: granite patterns on red ground
GRANITE_LIGHT = '#E3B4A8'
VOLCANIC = '#9A84B4'     # map convention: purple felsic volcanic patterns
BASALT_MAP = '#E3A15E'   # map convention: orange plateau basalt
DOLERITE_MAP = '#7FA77A' # map convention: green dolerite pattern
BASALT = '#596462'
LIMESTONE = '#C9D3D6'
DOLOMITE = '#D8CDB6'
SANDSTONE = '#E4CF9F'
CONGLOMERATE = '#D9C29A'
SHALE = '#A5ABA3'
MUDSTONE = '#9FA095'
CHERT = '#B8B7A6'
SLATE = '#7D8A8E'
SCHIST = '#A3A68E'
GNEISS = '#C2B6A6'
HORNFELS = '#8C8F86'
TUFF = '#D6C9B0'
SOIL_DARK = '#8B6B4C'
ALLUVIUM = '#D9C79F'
GOSSAN = '#A55B48'
COAL = '#262B2E'         # bright/vitrain coal
COAL_DULL = '#4A4F52'    # dull/durain coal
BROWN_COAL = '#6B5444'
OIL_SHALE = '#6E6A58'
HEAT = '#D58659'
WATER = '#5D9EB8'
VEGETATION = '#7E9B5E'
SKY = '#EEF4F5'
CLAY = '#C4A587'
LOESS = '#D7BE8E'

# ---------------------------------------------------------------- drawing --


class FieldDrawing(Drawing):
    """Drawing with clipping, dashed lines and hatching helpers."""

    @contextmanager
    def clipped(self, region):
        """Clip every part added inside the block to ``region`` (a Polygon)."""
        start = len(self.parts)
        yield region
        for part in self.parts[start:]:
            part.ink = part.ink.intersection(region)
            if part.face is not None:
                part.face = part.face.intersection(region)

    def dashed(self, points, colour=INK, width=.75, dash=2.2, gap=1.4):
        """Dashed polyline with real gaps (survives in the monochrome font)."""
        path = LineString(points)
        position, length = 0.0, path.length
        while position < length:
            end = min(position + dash, length)
            segment = [path.interpolate(t) for t in (position, end)]
            if end - position > .2:
                self.line([(p.x, p.y) for p in segment], colour, width)
            position = end + gap
        return self

    def dotted(self, points, colour=INK, radius=.42, spacing=1.6):
        path = LineString(points)
        steps = max(1, int(path.length / spacing))
        for index in range(steps + 1):
            p = path.interpolate(index / steps, normalized=True)
            self.circle(p.x, p.y, radius, colour, colour, True)
        return self

    def hatch(self, region, angle=45, spacing=1.6, colour=INK, width=.45):
        """Parallel ruling clipped to ``region``."""
        x0, y0, x1, y1 = region.bounds
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        reach = math.hypot(x1 - x0, y1 - y0)
        a = math.radians(angle)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        with self.clipped(region):
            offset = -reach
            while offset <= reach:
                px, py = cx + nx * offset, cy + ny * offset
                self.line([(px - ux * reach, py - uy * reach),
                           (px + ux * reach, py + uy * reach)], colour, width)
                offset += spacing
        return self

    def solid(self, geometry, colour=INK):
        """A filled ink shape (black in the font, ``colour`` in flat art)."""
        return self.shape(geometry, colour, colour, solid=True)

    def text_free_arrow(self, x0, y0, x1, y1, colour=INK, width=.95, head=2.6):
        """Arrow with a proportionate head, for movement and vergence cues."""
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        ux, uy = dx / length, dy / length
        self.line([(x0, y0), (x1 - ux * head * .7, y1 - uy * head * .7)], colour, width)
        w = head * .58
        self.poly([(x1, y1), (x1 - ux * head - uy * w, y1 - uy * head + ux * w),
                   (x1 - ux * head + uy * w, y1 - uy * head - ux * w)], colour, colour, True)
        return self


# ---------------------------------------------------------------- helpers --

def rng(seed):
    return random.Random(seed)


def scatter(seed, count, region, spacing=2.0, margin=0.0, attempts=4000):
    """Deterministic blue-noise points inside ``region`` (Polygon)."""
    r = rng(seed)
    inner = region.buffer(-margin) if margin else region
    x0, y0, x1, y1 = inner.bounds
    points = []
    tries = 0
    while len(points) < count and tries < attempts:
        tries += 1
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        if not inner.contains(Point(x, y)):
            continue
        if all((x - px) ** 2 + (y - py) ** 2 >= spacing ** 2 for px, py in points):
            points.append((x, y))
    return points


def grid_points(region, dx, dy, stagger=True, inset=1.5):
    """Regular (optionally brick-staggered) pattern points inside ``region``."""
    x0, y0, x1, y1 = region.bounds
    points, row, y = [], 0, y0 + inset + dy / 2
    while y < y1 - inset:
        shift = dx / 2 if stagger and row % 2 else 0
        x = x0 + inset + dx / 2 + shift
        while x < x1 - inset:
            if region.contains(Point(x, y)):
                points.append((x, y))
            x += dx
        y += dy
        row += 1
    return points


def irregular_polygon(seed, x, y, radius, sides=7, jitter=.35, stretch=1.0, angle=0):
    """Angular grain/clast outline; ``jitter`` controls angularity."""
    r = rng(seed)
    points = []
    for index in range(sides):
        t = index / sides * math.tau + r.uniform(-.25, .25) / sides * math.tau
        rad = radius * (1 + r.uniform(-jitter, jitter))
        u, v = rad * math.cos(t) * stretch, rad * math.sin(t)
        a = math.radians(angle)
        points.append((x + u * math.cos(a) - v * math.sin(a), y + u * math.sin(a) + v * math.cos(a)))
    return points


def swatch(d, fill, x=4, y=8, width=40, height=32, radius=1.2):
    """Standard map-pattern swatch; returns the clip region for its texture."""
    d.rect(x, y, width, height, fill, radius)
    return box(x, y, x + width, y + height).buffer(-.5)


def block(d, x=6, y=14, width=30, depth=12, height=20, top=None, front=None, side=None,
          dx=.72, dy=-.48):
    """Oblique block diagram. Returns (top, front, side) polygons for clipping.

    ``x, y`` is the top-left corner of the front face. Depth recedes up-right.
    """
    ox, oy = depth * dx, depth * dy
    front_poly = Polygon([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])
    top_poly = Polygon([(x, y), (x + ox, y + oy), (x + width + ox, y + oy), (x + width, y)])
    side_poly = Polygon([(x + width, y), (x + width + ox, y + oy),
                         (x + width + ox, y + height + oy), (x + width, y + height)])
    d.shape(top_poly, top, INK)
    d.shape(front_poly, front, INK)
    d.shape(side_poly, side, INK)
    return top_poly, front_poly, side_poly


def ellipse_points(x, y, rx, ry, start=0, stop=360, steps=48, angle=0):
    a = math.radians(angle)
    points = []
    for index in range(steps + 1):
        t = math.radians(start + (stop - start) * index / steps)
        u, v = rx * math.cos(t), ry * math.sin(t)
        points.append((x + u * math.cos(a) - v * math.sin(a), y + u * math.sin(a) + v * math.cos(a)))
    return points


def smooth(points, iterations=3):
    """Chaikin corner cutting for open polylines (keeps the end points)."""
    for _ in range(iterations):
        out = [points[0]]
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            out += [(.75 * x0 + .25 * x1, .75 * y0 + .25 * y1), (.25 * x0 + .75 * x1, .25 * y0 + .75 * y1)]
        out.append(points[-1])
        points = out
    return points


def smooth_closed(points, iterations=3):
    for _ in range(iterations):
        out = []
        for index, (x0, y0) in enumerate(points):
            x1, y1 = points[(index + 1) % len(points)]
            out += [(.75 * x0 + .25 * x1, .75 * y0 + .25 * y1), (.25 * x0 + .75 * x1, .25 * y0 + .75 * y1)]
        points = out
    return points


# ------------------------------------------------------------- rendering --

def flat_layers(drawing):
    """Convert a drawing into FlatLayer objects on the shared 24-unit canvas."""
    from detailed_flat import FlatLayer
    geometry = drawing.geometry()
    cleaned = geometry.buffer(.65, quad_segs=4, join_style=1).buffer(-.65, quad_segs=4, join_style=1)
    x0, y0, x1, y1 = cleaned.bounds
    factor = 880 / max(x1 - x0, y1 - y0)

    def convert(shape):
        shape = native(shape)
        shape = affinity.translate(shape, xoff=-(x0 + x1) / 2, yoff=-(y0 + y1) / 2)
        shape = affinity.scale(shape, factor, factor, origin=(0, 0))
        shape = affinity.translate(shape, xoff=500, yoff=500)
        shape = affinity.scale(shape, 24 / 1000, -24 / 1000, origin=(0, 0))
        return affinity.translate(shape, yoff=24)

    layers = []
    for part in drawing.parts:
        if part.face is not None and part.fill is not None and not part.face.is_empty:
            layers.append(FlatLayer(convert(part.face), part.fill))
        if not part.ink.is_empty:
            layers.append(FlatLayer(convert(part.ink), part.colour))
    return layers
