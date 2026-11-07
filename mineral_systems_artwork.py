"""Approved MineralSystemsQC realm and clan artwork.

One 48-unit vector drawing supplies colour, monochrome and dark-theme output.
Public icon identities are registered by icons_mineral_systems.py.
"""
import math
from functools import lru_cache

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon
from icons_mt import Drawing, INK

SAND = '#DECAA5'
SEDIMENT = '#BCA98B'
ROCK = '#929C96'
BASALT = '#667772'
GRANITE = '#C39D8C'
MELT = '#DC9369'
WATER = '#73B3C9'
WATER_PALE = '#D5E8EB'
QUARTZ = '#E4ECE8'
CARBONATE = '#DEDAC1'
SULFIDE = '#B6A05E'
OXIDE = '#74665E'
IRON = '#B87556'
CLAY = '#C8AB87'
GREEN = '#718E6C'
GOLD = '#CFAD4D'
COPPER = '#759E84'
GEM = '#81B4AC'
PURPLE = '#B2A6BF'
COAL = '#687073'


def polygon(d, points, fill, width=1.0):
    d.shape(Polygon(points), fill, INK, width)


def path(d, points, width=1.1, colour=INK):
    d.line(points, colour, width)


def vein(d, points, width=2.7, fill=QUARTZ):
    surface = LineString(points).buffer(width/2, quad_segs=6, cap_style=1, join_style=1)
    d.shape(surface, fill, INK, .85)


def curve(d, points, colour=INK, width=1.0):
    """Cubic Bezier through four control points, in diagram coordinates."""
    a, b, c, e = points
    samples = []
    for index in range(41):
        t = index / 40
        samples.append(tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]
                             +3*(1-t)*t*t*c[k]+t**3*e[k] for k in (0, 1)))
    path(d, samples, width, colour)


def grains(d, points, fill=SULFIDE, radius=1.1):
    for x, y in points:
        d.circle(x, y, radius, fill, INK)


def crystal(d, x, y, width=5, height=12, fill=QUARTZ, angle=0):
    radians = math.radians(angle)
    def rotate(points):
        return [(x+u*math.cos(radians)-v*math.sin(radians),
                 y+u*math.sin(radians)+v*math.cos(radians)) for u, v in points]
    polygon(d, rotate([(-width/2, 0), (-width/2, -height+width*.55),
                       (0, -height), (width/2, -height+width*.55), (width/2, 0)]), fill, .9)
    path(d, rotate([(0, 0), (0, -height+width*.9), (-width/2, -height+width*.55)]), .65)
    path(d, rotate([(0, -height+width*.9), (width/2, -height+width*.55)]), .65)


def diamond(d, x, y, size=6, fill=GEM):
    polygon(d, [(x-size, y-size*.45), (x-size*.55, y-size),
                (x+size*.55, y-size), (x+size, y-size*.45), (x, y+size)], fill, .95)
    path(d, [(x-size, y-size*.45), (x+size, y-size*.45)], .7)
    path(d, [(x-size*.55, y-size), (x-size*.3, y-size*.45),
             (x, y+size), (x+size*.3, y-size*.45), (x+size*.55, y-size)], .65)


def cube(d, x, y, size=3.5, fill=SULFIDE):
    polygon(d, [(x-size, y-size*.5), (x, y-size), (x+size, y-size*.5),
                (x+size, y+size*.5), (x, y+size), (x-size, y+size*.5)], fill, .9)
    path(d, [(x-size, y-size*.5), (x, y), (x+size, y-size*.5)], .7)
    path(d, [(x, y), (x, y+size)], .7)


def book(d, x, y, width=13, fill=CLAY, layers=3):
    for index in reversed(range(layers)):
        level = y + index*2
        polygon(d, [(x-width/2, level), (x-width*.15, level-3),
                    (x+width/2, level-1), (x+width*.15, level+2)], fill, .8)


def droplet(d, x, y, size=2, fill=WATER):
    polygon(d, [(x, y-size*1.6), (x-size*.8, y), (x-size*.6, y+size*.7),
                (x, y+size), (x+size*.6, y+size*.7), (x+size*.8, y)], fill, .8)


def strata(d, top=12, bottom=43, boundaries=(23, 33), colours=None):
    levels = (top, *boundaries, bottom)
    colours = colours or (SAND, CARBONATE, SEDIMENT, ROCK)
    for index, (upper, lower) in enumerate(zip(levels, levels[1:])):
        polygon(d, [(4, upper), (44, upper), (44, lower), (4, lower)], colours[index % len(colours)], 1)


def folded(d, ore=False):
    def trace(offset):
        return [(4+40*i/40, 12+offset+4.5*math.sin(i/40*math.tau*1.35)) for i in range(41)]
    for index, colour in enumerate((ROCK, CARBONATE, BASALT, SAND)):
        polygon(d, trace(index*7)+list(reversed(trace((index+1)*7))), colour, .95)
    if ore:
        polygon(d, [(13, 43), (21, 28), (23, 15), (28, 6),
                    (32, 7), (27, 18), (26, 30), (18, 44)], QUARTZ, 1)
        grains(d, [(24.8, 21), (21.4, 32), (28.1, 12)], GOLD, .9)


def magma_body(d, fill=GRANITE, top=25):
    polygon(d, [(10, 43), (8, 38), (12, top+3), (18, top), (21, top-4),
                (27, top-4), (31, top), (37, top+3), (40, 38), (37, 43)], fill, 1.1)


def chamber(d, oxide=False):
    polygon(d, [(4, 15), (14, 11), (20, 15), (28, 11), (40, 14),
                (44, 23), (42, 35), (36, 42), (13, 42), (6, 36)], MELT if not oxide else BASALT, 1.2)
    polygon(d, [(6, 32), (17, 35), (29, 34), (42, 31),
                (42, 35), (36, 42), (13, 42), (6, 36)], OXIDE if oxide else SULFIDE, 1)
    path(d, [(9, 37), (18, 39), (29, 38), (39, 36)], 1)
    if oxide:
        path(d, [(8, 29), (18, 32), (29, 31), (42, 28)], 1.6)
        path(d, [(6, 23), (17, 26), (29, 25), (43, 22)], 1.25)
        # Octahedral oxide habit, distinct from the cut-gem diamond symbol.
        polygon(d, [(21, 18), (25, 13), (29, 18), (25, 23)], OXIDE, .85)
        path(d, [(21, 18), (25, 17), (29, 18)], .65)
        path(d, [(25, 13), (25, 17), (25, 23)], .65)
    else:
        for x, y in ((13, 21), (25, 24), (36, 19)):
            crystal(d, x, y, 3.6, 6, CARBONATE, (x-24)*2)
        d.arrow(17, 25, 19, 31, INK)
        d.arrow(34, 24, 32, 31, INK)


def basin(d, fault=False):
    curves = []
    for level, sag in ((9, 0), (17, 9), (27, 9), (37, 6), (44, 0)):
        curves.append([(4+40*i/40, level+sag*math.sin(math.pi*i/40)) for i in range(41)])
    for index, colour in enumerate((SAND, CARBONATE, SEDIMENT, ROCK)):
        polygon(d, curves[index]+list(reversed(curves[index+1])), colour, .95)
    if fault:
        path(d, [(33, 42), (29, 31), (27, 22), (23, 12)], 2.8)
        path(d, [(33, 42), (29, 31), (27, 22), (23, 12)], 1.2, WATER)


def plume(d, x, y, width=5, height=14):
    # Open, lobed smoker plume. Its silhouette remains visible in monochrome.
    curve(d, [(x-width*.4, y), (x-width*1.4, y-height*.3),
              (x-width*1.1, y-height*.7), (x-width*.3, y-height)], COAL, 1.3)
    curve(d, [(x+width*.4, y), (x+width*1.5, y-height*.35),
              (x+width*.4, y-height*.7), (x+width*.9, y-height)], COAL, 1.3)
    curve(d, [(x, y-3), (x+2, y-6), (x-2, y-7), (x+1, y-10)], COAL, .8)


def seafloor(d, lens=False):
    polygon(d, [(4, 29), (15, 28), (20, 30), (29, 28), (37, 29),
                (44, 27), (44, 44), (4, 44)], BASALT, 1.1)
    path(d, [(7, 36), (11, 33), (16, 37), (20, 35)], .8)
    path(d, [(31, 39), (35, 35), (40, 37)], .8)
    if lens:
        polygon(d, [(8, 29), (16, 25), (30, 24), (40, 28),
                    (34, 31), (17, 32)], SULFIDE, 1.1)
        for x in (18, 24, 30):
            path(d, [(x, 42), (x-2, 36), (x+1, 31)], 1.3, SULFIDE)
        grains(d, [(15, 28), (22, 29), (29, 27), (34, 28)], SULFIDE, .8)


def profile(d, supergene=False):
    polygon(d, [(5, 9), (16, 8), (28, 10), (43, 8), (43, 43), (5, 43)], ROCK, 1.1)
    polygon(d, [(5, 9), (16, 8), (28, 10), (43, 8), (43, 18),
                (33, 20), (22, 17), (13, 20), (5, 17)], IRON if not supergene else CLAY, 1)
    polygon(d, [(5, 17), (13, 20), (22, 17), (33, 20), (43, 18),
                (43, 29), (35, 27), (29, 33), (22, 29), (14, 34), (5, 28)],
            CLAY if not supergene else COPPER, 1)
    if supergene:
        polygon(d, [(5, 29), (14, 34), (22, 29), (29, 33), (35, 27),
                    (43, 29), (43, 34), (34, 34), (27, 38), (17, 37), (5, 35)], SULFIDE, 1)
    path(d, [(11, 43), (13, 37), (18, 35)], .8)
    path(d, [(35, 43), (33, 37), (37, 33)], .8)


@lru_cache(maxsize=256)
def drawing(identifier):
    d = Drawing()
    if identifier == 'realm_magmatic':
        chamber(d)
        path(d, [(22, 11), (22, 5), (27, 5), (27, 11)], 1.2)
    elif identifier == 'realm_magmatic_hydrothermal':
        d.ellipse(24, 21, 16, 16, None, GREEN)
        for points in ([(24, 31), (24, 18), (20, 8)],
                       [(24, 25), (13, 16), (9, 11)],
                       [(25, 22), (34, 16), (39, 7)],
                       [(24, 17), (29, 9), (29, 4)]):
            vein(d, points, 2.5)
        magma_body(d, MELT, 34)
        grains(d, [(20, 36), (29, 38)], CARBONATE, 1.2)
        d.arrow(8, 30, 14, 25, WATER)
        d.arrow(39, 29, 34, 24, WATER)
    elif identifier == 'realm_metamorphic_orogenic':
        folded(d, True)
        d.arrow(3, 5, 13, 5, INK)
        d.arrow(45, 5, 35, 5, INK)
    elif identifier == 'realm_basinal_hydrothermal':
        basin(d, True)
        d.arrow(8, 22, 19, 29, WATER)
        d.arrow(39, 25, 31, 30, WATER)
        d.ellipse(26, 31, 5.5, 2.1, SULFIDE, INK)
        grains(d, [(24, 31), (28, 31)], SULFIDE, .7)
    elif identifier == 'realm_submarine_hydrothermal':
        seafloor(d)
        polygon(d, [(19, 29), (20, 21), (24, 20), (25, 29)], SULFIDE)
        polygon(d, [(29, 29), (30, 24), (33, 23), (34, 29)], SULFIDE)
        plume(d, 22, 20, 3.3, 13)
        plume(d, 31, 22, 2.2, 10)
        d.arrow(7, 10, 7, 25, WATER)
        d.arrow(42, 10, 42, 24, WATER)
        d.ellipse(24, 41, 8, 2, MELT, INK)
        path(d, [(16, 36), (13, 32), (10, 32)], .8, WATER)
    elif identifier == 'realm_sedimentary_chemical':
        strata(d, 23, 44, (30, 36), (CARBONATE, IRON, SAND))
        d.wave(4, 44, 9, 1.6, 2, WATER)
        for x, y in ((11, 14), (23, 17), (36, 13)):
            grains(d, [(x, y)], CARBONATE, 1.05)
            d.arrow(x, y+3, x, 22, INK)
        path(d, [(7, 40), (18, 40), (25, 40)], .7)
    elif identifier == 'realm_surficial_weathering':
        profile(d)
        for x in (13, 33):
            d.arrow(x, 3, x, 15, WATER)
        grains(d, [(10, 23), (20, 25), (35, 24), (30, 14)], IRON, 1.1)
        path(d, [(23, 5), (23, 11), (26, 16)], .85, GREEN)
    elif identifier == 'realm_clastic_mechanical':
        polygon(d, [(4, 14), (12, 14), (16, 28), (23, 32), (31, 29),
                    (37, 14), (44, 14), (44, 43), (4, 43)], SAND, 1.1)
        polygon(d, [(12, 14), (37, 14), (31, 27), (24, 30), (17, 26)], WATER_PALE, 1)
        path(d, [(13, 17), (35, 17)], 1, WATER)
        for x, y, radius in ((15, 33, 2.1), (22, 35, 2.2), (29, 34, 1.9), (34, 31, 1.6)):
            d.ellipse(x, y, radius, radius*.65, ROCK, INK)
        grains(d, [(17, 31), (24, 31.5), (29, 30.5)], GOLD, 1.2)
        d.arrow(9, 6, 39, 6, WATER)
    elif identifier == 'realm_hybrid_industrial':
        polygon(d, [(5, 33), (12, 22), (26, 20), (43, 29),
                    (39, 43), (14, 44)], ROCK, 1.05)
        book(d, 13, 32, 13, CLAY, 3)
        crystal(d, 25, 32, 8, 24, QUARTZ, -8)
        diamond(d, 36, 27, 7, GEM)
        path(d, [(15, 41), (23, 36), (29, 41)], .7)
    elif identifier == 'clan_magmatic_sulfide':
        polygon(d, [(5, 18), (17, 18), (19, 5), (27, 5), (29, 18),
                    (43, 18), (42, 29), (35, 38), (15, 40), (6, 32)], BASALT, 1.1)
        polygon(d, [(7, 29), (18, 34), (32, 33), (42, 27),
                    (42, 29), (35, 38), (15, 40), (6, 32)], SULFIDE, 1.1)
        grains(d, [(16, 25), (28, 23), (34, 28)], SULFIDE, 1.6)
        d.arrow(24, 10, 24, 19, INK)
    elif identifier == 'clan_magmatic_oxide':
        chamber(d, True)
    elif identifier == 'clan_carbonatite_alkaline':
        for angle in (0, 55, 110, 170, 230, 290):
            radians = math.radians(angle)
            path(d, [(24+math.cos(radians)*13, 24+math.sin(radians)*13),
                     (24+math.cos(radians)*21, 24+math.sin(radians)*21)], 3.3, CARBONATE)
        d.circle(24, 24, 16, BASALT, INK)
        d.circle(24, 24, 11, GRANITE, INK)
        d.circle(24, 24, 6, CARBONATE, INK)
        for angle in (25, 115, 205, 295):
            radians = math.radians(angle)
            grains(d, [(24+13*math.cos(radians), 24+13*math.sin(radians))], GREEN, 1.2)
    elif identifier == 'clan_pegmatite':
        polygon(d, [(5, 12), (37, 5), (44, 36), (11, 44)], GRANITE, 1.1)
        polygon(d, [(11, 10), (30, 6), (38, 38), (18, 43)], QUARTZ, 1.1)
        crystal(d, 23, 35, 8, 23, PURPLE, -10)
        crystal(d, 32, 29, 6, 15, CARBONATE, 10)
        book(d, 15, 34, 9, COAL, 3)
        path(d, [(7, 17), (12, 18)], .7)
        path(d, [(37, 12), (39, 20)], .7)
    elif identifier == 'clan_kimberlite':
        strata(d, 13, 44, (25, 35), (SAND, ROCK, BASALT))
        polygon(d, [(10, 13), (7, 7), (41, 7), (38, 13),
                    (31, 23), (27, 43), (23, 43), (19, 23)], GREEN, 1.1)
        path(d, [(11, 11), (21, 15), (31, 14), (37, 11)], .85)
        diamond(d, 25, 27, 5.2, QUARTZ)
        grains(d, [(19, 17), (31, 19), (26, 37)], BASALT, .8)
    elif identifier == 'clan_porphyry':
        d.ellipse(24, 23, 19, 17, None, GREEN)
        d.ellipse(24, 23, 13, 13, None, CLAY)
        for points in ([(16, 27), (24, 16), (33, 9)], [(12, 17), (22, 24), (35, 28)],
                       [(17, 10), (21, 23), (30, 32)], [(32, 14), (27, 23), (14, 31)]):
            path(d, points, 1.05)
        magma_body(d, GRANITE, 35)
        grains(d, [(22, 37), (29, 38), (20, 30), (30, 26)], COPPER, 1)
    elif identifier == 'clan_skarn':
        strata(d, 7, 43, (19, 31), (CARBONATE, CARBONATE, CARBONATE))
        polygon(d, [(4, 7), (14, 7), (20, 15), (18, 23),
                    (24, 32), (21, 43), (4, 43)], GRANITE, 1.1)
        polygon(d, [(14, 7), (20, 15), (18, 23), (24, 32), (21, 43),
                    (28, 43), (30, 30), (24, 23), (27, 15), (21, 7)], GREEN, 1)
        for x, y in ((24, 15), (22, 25), (27, 35)):
            polygon(d, [(x-2, y), (x-1, y-2), (x+1.5, y-1.5),
                        (x+2, y+1), (x, y+2.5), (x-2, y+1)], IRON, .7)
        d.arrow(32, 24, 26, 24, WATER)
    elif identifier == 'clan_epithermal':
        polygon(d, [(4, 17), (12, 17), (21, 7), (26, 7), (36, 17),
                    (44, 17), (44, 43), (4, 43)], SAND, 1.1)
        polygon(d, [(19, 43), (22, 29), (20, 21), (24, 12),
                    (28, 13), (25, 22), (28, 31), (26, 43)], QUARTZ, 1.1)
        path(d, [(22, 40), (25, 30), (23, 23), (26, 15)], .8, GOLD)
        d.circle(15, 30, 1.5, WATER_PALE, INK)
        d.circle(15, 24, 1, WATER_PALE, INK)
        path(d, [(29, 11), (35, 11), (35, 13), (40, 13)], 1)
        curve(d, [(24, 5), (21, 3), (28, 2), (25, 0.8)], WATER, .85)
    elif identifier == 'clan_intrusion_related_other':
        strata(d, 10, 43, (23, 33), (ROCK, SAND, ROCK))
        magma_body(d, GRANITE, 26)
        for x in (16, 23, 30):
            vein(d, [(x, 31), (x+1, 22), (x+4, 11)], 2.4)
        book(d, 31, 39, 7, COAL, 2)
    elif identifier == 'clan_iron_oxide':
        polygon(d, [(7, 12), (19, 5), (35, 9), (43, 20),
                    (39, 38), (26, 44), (10, 39), (5, 25)], IRON, 1.1)
        for points in ([(12, 16), (20, 12), (21, 22), (16, 25)],
                       [(27, 12), (36, 16), (34, 23), (26, 21)],
                       [(12, 30), (21, 27), (23, 36), (15, 38)],
                       [(29, 29), (38, 27), (35, 37), (29, 39)]):
            polygon(d, points, BASALT, .9)
        grains(d, [(24, 26), (24, 40), (9, 23), (37, 24)], COPPER, 1.2)
        path(d, [(20, 6), (24, 16), (22, 24), (26, 33), (25, 43)], 1.1, CARBONATE)
    elif identifier == 'clan_orogenic_gold':
        folded(d, True)
        d.arrow(6, 30, 10, 21, INK)
        d.arrow(36, 24, 40, 15, INK)
    elif identifier == 'clan_sediment_hosted_gold':
        strata(d, 6, 44, (16, 29, 36), (CARBONATE, CARBONATE, COAL, ROCK))
        polygon(d, [(8, 20), (18, 18), (29, 21), (41, 19),
                    (41, 27), (30, 26), (21, 28), (8, 26)], CLAY, .85)
        grains(d, [(12, 23), (18, 22), (24, 24), (30, 23), (37, 22)], GOLD, .85)
        path(d, [(35, 43), (31, 35), (29, 29), (30, 26)], 1.3, WATER)
        d.arrow(32, 35, 30, 28, INK)
    elif identifier == 'clan_metamorphic_industrial':
        folded(d)
        book(d, 15, 22, 14, COAL, 4)
        book(d, 33, 32, 16, CARBONATE, 3)
        path(d, [(24, 8), (27, 17), (23, 29), (25, 42)], 2, QUARTZ)
    elif identifier == 'clan_sediment_hosted_zn_pb':
        strata(d, 8, 44, (20, 29, 37), (SAND, CARBONATE, SULFIDE, ROCK))
        path(d, [(31, 44), (27, 30), (23, 18), (19, 8)], 2.7)
        path(d, [(31, 44), (27, 30), (23, 18), (19, 8)], 1.05, WATER)
        cube(d, 13, 32, 3, SULFIDE)
        cube(d, 36, 32, 3, COAL)
        d.arrow(39, 40, 30, 35, WATER)
    elif identifier == 'clan_sediment_hosted_cu':
        strata(d, 6, 44, (18, 27, 35), (IRON, IRON, COAL, SAND))
        polygon(d, [(4, 25), (44, 25), (44, 30), (4, 30)], COPPER, .95)
        grains(d, [(10, 27.5), (18, 27.5), (28, 27.5), (38, 27.5)], COPPER, .8)
        d.arrow(9, 37, 22, 32, WATER)
        d.arrow(37, 37, 27, 32, WATER)
        for x in (10, 22, 34):
            path(d, [(x, 12), (x+3, 12)], .75)
    elif identifier == 'clan_basinal_uranium':
        strata(d, 7, 43, (15, 35), (ROCK, SAND, ROCK))
        polygon(d, [(25, 16), (20, 18), (17, 24), (18, 30), (25, 34),
                    (30, 34), (24, 29), (23, 24), (25, 20), (30, 16)], OXIDE, 1.1)
        for y in (20, 28):
            d.arrow(6, y, 15, y, WATER)
        grains(d, [(21, 20), (20, 26), (24, 31)], GOLD, .85)
        path(d, [(34, 20), (38, 20)], .7)
        path(d, [(34, 29), (40, 29)], .7)
    elif identifier == 'clan_basinal_vein':
        polygon(d, [(6, 8), (35, 5), (44, 16), (41, 41),
                    (13, 44), (4, 33)], SEDIMENT, 1.1)
        points = [(11, 42), (20, 30), (22, 20), (36, 5)]
        vein(d, points, 4.3)
        vein(d, [(22, 23), (35, 24), (42, 18)], 2.5)
        diamond(d, 19, 31, 4.8, PURPLE)
        crystal(d, 30, 22, 5.5, 11, CARBONATE, 27)
    elif identifier == 'clan_vms':
        seafloor(d, True)
        polygon(d, [(21, 25), (22, 20), (26, 20), (27, 25)], SULFIDE, 1)
        plume(d, 24, 18, 4, 13)
        d.wave(5, 15, 11, .9, 1, WATER)
        d.wave(34, 44, 11, .9, 1, WATER)
    elif identifier == 'clan_chemical_sediment_fe_mn':
        for index, (y, colour) in enumerate(((14, IRON), (20, QUARTZ), (26, IRON), (32, QUARTZ), (38, IRON))):
            polygon(d, [(5, y), (18, y-2), (31, y+1), (43, y-1),
                        (43, y+5), (31, y+7), (18, y+4), (5, y+6)], colour, .9)
        d.ellipse(32, 13, 8, 6, OXIDE, INK)
        d.ellipse(32, 13, 4.5, 3, None, INK)
        d.circle(32, 13, 1.2, ROCK, INK)
        d.wave(4, 18, 6, 1, 1, WATER)
    elif identifier == 'clan_chemical_sediment_other':
        strata(d, 25, 44, (32, 38), (CARBONATE, COAL, SAND))
        d.wave(4, 44, 7, 1.5, 2, WATER)
        cube(d, 12, 19, 3.8, QUARTZ)
        cube(d, 35, 18, 4.2, CARBONATE)
        d.arrow(24, 12, 24, 24, INK)
        for x in (12, 22, 32, 39):
            grains(d, [(x, 29)], CARBONATE, .9)
    elif identifier == 'clan_residual_laterite':
        profile(d)
        for x in (11, 21, 33, 39):
            grains(d, [(x, 14)], IRON, 1.1)
        grains(d, [(13, 25), (24, 24), (35, 25)], GREEN, 1.2)
        path(d, [(20, 43), (18, 36), (21, 31)], .9)
        droplet(d, 12, 3, 1.6)
        droplet(d, 33, 3, 1.6)
    elif identifier == 'clan_supergene_sulfide':
        profile(d, True)
        for x in (13, 24, 35):
            d.arrow(x, 12, x, 25, WATER)
        grains(d, [(12, 33), (22, 34), (32, 33), (39, 32)], SULFIDE, 1)
        path(d, [(5, 27), (10, 27)], .8, WATER)
        path(d, [(38, 26), (43, 26)], .8, WATER)
    elif identifier == 'clan_evaporative_brine':
        polygon(d, [(4, 18), (11, 24), (19, 28), (31, 28), (40, 23),
                    (44, 18), (44, 43), (4, 43)], SAND, 1.1)
        polygon(d, [(8, 22), (18, 26), (32, 26), (41, 22),
                    (34, 33), (17, 33)], WATER_PALE, 1)
        path(d, [(14, 31), (33, 31)], 2.3, QUARTZ)
        for x, y in ((13, 19), (24, 17), (35, 19)):
            d.arrow(x, y, x, y-12, WATER)
        cube(d, 23, 37, 3.4, CARBONATE)
    elif identifier == 'clan_placer':
        # Plan view: a river bends around a heavy-mineral-rich point bar.
        host = Polygon([(4, 4), (44, 4), (44, 44), (4, 44)])
        d.shape(host, SAND, INK, 1)
        controls = [(8, 4), (42, 13), (5, 32), (39, 44)]
        points = []
        for index in range(81):
            t = index/80
            points.append(tuple((1-t)**3*controls[0][k]+3*(1-t)**2*t*controls[1][k]
                                +3*(1-t)*t*t*controls[2][k]+t**3*controls[3][k] for k in (0, 1)))
        channel = LineString(points).buffer(5.8, quad_segs=8).intersection(host)
        d.shape(channel, WATER_PALE, INK, 1)
        path(d, points, .8, WATER)
        grains(d, [(24, 11), (27, 15), (26, 19), (21, 30), (24, 34), (28, 36)], GOLD, 1.25)
        d.arrow(13, 9, 20, 12, WATER)
        d.arrow(25, 38, 33, 42, WATER)
    elif identifier == 'clan_industrial_minerals':
        book(d, 13, 31, 17, CLAY, 4)
        crystal(d, 28, 33, 8.5, 27, QUARTZ, -7)
        crystal(d, 37, 34, 6.5, 20, QUARTZ, 15)
        cube(d, 28, 39, 5.5, CARBONATE)
    elif identifier == 'clan_gemstone':
        diamond(d, 29, 30, 14, GEM)
        crystal(d, 11, 31, 8, 23, GREEN, -15)
        crystal(d, 39, 18, 6.5, 13, PURPLE, 13)
        path(d, [(4, 38), (10, 41), (15, 39)], 1)
    elif identifier == 'clan_energy_adjacent':
        strata(d, 23, 44, (30, 36), (SAND, COAL, ROCK))
        path(d, [(29, 8), (29, 40), (36, 40)], 2.5)
        path(d, [(29, 8), (29, 40), (36, 40)], 1.1, WATER)
        path(d, [(24, 8), (34, 8)], 1.2)
        for x in (13, 20, 27):
            curve(d, [(x, 19), (x-4, 15), (x+3, 12), (x, 6)], MELT, 1)
        path(d, [(5, 33), (11, 32), (17, 34), (23, 33)], .7, QUARTZ)
    else:
        from mineral_systems_deposits import DRAWINGS
        if identifier not in DRAWINGS:
            raise ValueError('No draft drawing for taxonomy ID: ' + identifier)
        DRAWINGS[identifier](d)
    return d


def colour_layers(identifier, dark=False):
    """48-unit geometry is identical for every export and theme."""
    result = []
    for part in drawing(identifier).parts:
        if part.face is not None and part.fill is not None:
            result.append((part.face, part.fill))
        colour = '#E1E9EC' if dark and part.colour == INK else part.colour
        result.append((part.ink, colour))
    return result


def mono_geometry(identifier):
    native = drawing(identifier).geometry()
    native = affinity.translate(native, yoff=-1000)
    # Boolean unions can acquire coincident vertices in the canvas round trip.
    return affinity.scale(native, xfact=48/1000, yfact=-48/1000, origin=(0, 0)).buffer(0)
