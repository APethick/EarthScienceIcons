"""Approved MineralSystemsQC deposit-type artwork.

The 69 type-level entries below sit under the nine realms and 27 clans drawn by
mineral_systems_artwork.py, and share its 48-unit Y-down drawing vocabulary and
natural-material palette. Each drawing shows the host architecture, the ore
geometry and one diagnostic texture, so a type stays distinguishable from its
own clan at 24 px. Public icon identities are registered by
icons_mineral_systems.py.
"""
import math

from shapely.geometry import LineString, Polygon

from mineral_systems_artwork import (BASALT, CARBONATE, CLAY, COAL, COPPER, GEM, GOLD, GRANITE,
                                     GREEN, INK, IRON, MELT, OXIDE, PURPLE, QUARTZ, ROCK, SAND,
                                     SEDIMENT, SULFIDE, WATER, WATER_PALE,
                                     book, crystal, cube, curve, diamond, droplet, folded, grains,
                                     magma_body, path, polygon, profile, seafloor, strata, vein)

DRAWINGS = {}


def deposit(identifier):
    """Register one taxonomy type drawing."""
    def register(function):
        DRAWINGS[identifier] = function
        return function
    return register


# --------------------------------------------------------------------------
# Shared constructions
# --------------------------------------------------------------------------

def band(d, top, bottom, colour, left=4, right=44, width=.95):
    polygon(d, [(left, top), (right, top), (right, bottom), (left, bottom)], colour, width)


def stack(d, levels, colours, left=4, right=44, width=.95):
    """Flat layer cake from a list of boundary depths."""
    for index, (top, bottom) in enumerate(zip(levels, levels[1:])):
        band(d, top, bottom, colours[index % len(colours)], left, right, width)


def seam(d, y, colour=SULFIDE, thickness=1.6, left=5, right=43, sag=0):
    points = [(left+(right-left)*i/24, y+sag*math.sin(math.pi*i/24)) for i in range(25)]
    polygon(d, points+[(x, y+thickness+sag*math.sin(math.pi*i/24))
                       for i, (x, _) in reversed(list(enumerate(points)))], colour, .85)


def hatch(d, points, colour=INK, width=.6):
    for a, b in points:
        path(d, [a, b], width, colour)


def pipe(d, top=10, bottom=44, half_top=7, half_bottom=3, x=24, fill=GREEN, width=1.1):
    polygon(d, [(x-half_top, top), (x+half_top, top), (x+half_bottom, bottom),
                (x-half_bottom, bottom)], fill, width)


def clasts(d, boxes, fill=ROCK, width=.8):
    for x, y, size, tilt in boxes:
        radians = math.radians(tilt)
        corners = [(-size, -size*.7), (size*.9, -size), (size, size*.6), (-size*.8, size)]
        polygon(d, [(x+u*math.cos(radians)-v*math.sin(radians),
                     y+u*math.sin(radians)+v*math.cos(radians)) for u, v in corners], fill, width)


def nodule(d, x, y, radius=4, fill=OXIDE):
    d.circle(x, y, radius, fill, INK)
    d.circle(x, y, radius*.62, None, INK)
    d.circle(x, y, radius*.3, ROCK, INK)


def blades(d, x, y, angles, length=9, width=1.6, colour=COAL):
    for angle in angles:
        radians = math.radians(angle)
        polygon(d, [(x-width/2, y), (x+width/2, y),
                    (x+width/2+length*math.cos(radians), y+length*math.sin(radians)),
                    (x-width/2+length*math.cos(radians), y+length*math.sin(radians))], colour, .7)


def foliation(d, top=10, bottom=42, colour=INK, count=5, amplitude=1.6, width=.6):
    for index in range(count):
        y = top+(bottom-top)*(index+.5)/count
        path(d, [(5+38*i/20, y+amplitude*math.sin(i/20*math.tau)) for i in range(21)], width, colour)


def water_column(d, bottom=16, colour=WATER_PALE):
    band(d, 4, bottom, colour, 4, 44, .9)
    d.wave(5, 43, 6, 1.3, 2, WATER)


def surface(d, y=12, fill=SAND, bottom=44, relief=((14, -3), (28, 2))):
    points = [(4, y)]
    for x, offset in relief:
        points.append((x, y+offset))
    points += [(44, y), (44, bottom), (4, bottom)]
    polygon(d, points, fill, 1.05)


# --------------------------------------------------------------------------
# Magmatic realm
# --------------------------------------------------------------------------

@deposit('ni_cu_pge_komatiite')
def _komatiite(d):
    # Basal embayment in the footwall traps a massive sulfide pool.
    polygon(d, [(4, 30), (15, 30), (19, 38), (30, 38), (34, 30), (44, 30),
                (44, 44), (4, 44)], SEDIMENT, 1.1)
    polygon(d, [(15, 30), (19, 38), (30, 38), (34, 30)], SULFIDE, 1.1)
    polygon(d, [(4, 10), (44, 10), (44, 30), (4, 30)], BASALT, 1.1)
    # Spinifex: randomly oriented olivine blades below the flow top.
    hatch(d, [((9, 12), (15, 20)), ((16, 12), (11, 21)), ((19, 13), (26, 20)),
              ((27, 12), (22, 22)), ((30, 13), (37, 19)), ((40, 12), (34, 21))],
          CARBONATE, 1)
    grains(d, [(13, 27), (22, 28), (32, 27)], SULFIDE, 1)


@deposit('ni_cu_pge_conduit')
def _conduit(d):
    strata(d, 8, 44, (20, 32), (SAND, ROCK, SEDIMENT))
    vein(d, [(7, 43), (15, 33), (24, 29), (33, 18), (39, 7)], 7.5, BASALT)
    d.ellipse(24, 29, 7.5, 5.5, BASALT, INK)
    polygon(d, [(18, 31), (24, 28), (30, 31), (28, 34), (20, 34)], SULFIDE, 1)
    grains(d, [(15, 34), (24, 25), (32, 20)], SULFIDE, 1.1)
    d.arrow(12, 40, 19, 33, MELT)


@deposit('layered_intrusion_pge')
def _layered_pge(d):
    stack(d, (7, 15, 22, 30, 37, 44), (BASALT, ROCK, BASALT, GRANITE, BASALT))
    seam(d, 28.2, SULFIDE, 2.3)
    grains(d, [(11, 29.4), (19, 29.4), (27, 29.4), (35, 29.4), (41, 29.4)], GOLD, .85)
    d.arrow(24, 41, 24, 32, INK)


@deposit('layered_intrusion_chromite')
def _layered_chromite(d):
    stack(d, (7, 17, 27, 37, 44), (BASALT, ROCK, BASALT, ROCK))
    for y in (15.2, 25.2, 35.2):
        seam(d, y, OXIDE, 2.4)
    grains(d, [(10, 11), (18, 11), (26, 11), (34, 11), (42, 11)], ROCK, .8)


@deposit('podiform_chromite')
def _podiform(d):
    band(d, 6, 44, GREEN, 4, 44, 1.1)
    foliation(d, 8, 42, BASALT, 5, 1.8, .7)
    for x, y, length, height in ((14, 17, 7, 3), (28, 26, 9, 3.6), (19, 36, 6, 2.6)):
        polygon(d, [(x-length, y), (x-length*.3, y-height), (x+length*.6, y-height*.8),
                    (x+length, y+height*.2), (x+length*.2, y+height), (x-length*.5, y+height*.8)],
                OXIDE, 1)
    grains(d, [(36, 15), (37, 36), (9, 27)], OXIDE, 1)


@deposit('fe_ti_v_oxide')
def _fe_ti_v(d):
    band(d, 8, 44, BASALT, 4, 44, 1.1)
    hatch(d, [((6, 14), (20, 15)), ((26, 16), (42, 15)), ((6, 25), (18, 26)),
              ((30, 37), (42, 36))], ROCK, .7)
    polygon(d, [(15, 11), (22, 10), (31, 21), (33, 33), (29, 42), (23, 42),
                (24, 31), (18, 21)], OXIDE, 1.15)
    grains(d, [(20, 16), (28, 27), (26, 38)], IRON, 1)
    crystal(d, 36, 30, 3.6, 9, QUARTZ, 18)
    crystal(d, 11, 36, 3.2, 8, QUARTZ, -14)


@deposit('alaskan_type_pt')
def _alaskan_pt(d):
    # Plan view of a concentrically zoned ultramafic pipe.
    d.circle(24, 24, 19, GREEN, INK)
    d.circle(24, 24, 13, BASALT, INK)
    d.circle(24, 24, 7, OXIDE, INK)
    grains(d, [(24, 20), (21, 26), (27, 27)], GOLD, 1.2)
    for angle in (35, 150, 265):
        radians = math.radians(angle)
        path(d, [(24+16*math.cos(radians), 24+16*math.sin(radians)),
                 (24+22*math.cos(radians), 24+22*math.sin(radians))], .75, INK)


@deposit('carbonatite_ree')
def _carbonatite_ree(d):
    band(d, 6, 44, ROCK, 4, 44, 1.1)
    d.ellipse(24, 27, 17.5, 16, None, PURPLE)
    pipe(d, 7, 44, 9.5, 4.5, 24, CARBONATE, 1.15)
    for x in (12, 37):
        vein(d, [(x, 44), (x+(1 if x < 24 else -1), 24), (x, 10)], 2.4, CARBONATE)
    grains(d, [(21, 16), (27, 22), (22, 31), (26, 38)], PURPLE, 1.15)
    crystal(d, 24, 14, 3.4, 7, QUARTZ, 0)


@deposit('alkaline_peralkaline_ree')
def _alkaline_ree(d):
    band(d, 6, 44, ROCK, 4, 44, 1.05)
    polygon(d, [(5, 20), (19, 11), (40, 15), (44, 26), (43, 44), (6, 44)], GRANITE, 1.15)
    for offset, colour in ((0, PURPLE), (7, CARBONATE), (14, PURPLE)):
        polygon(d, [(6, 28+offset), (43, 21+offset), (43, 25+offset), (6, 32+offset)], colour, .85)
    crystal(d, 16, 23, 5, 11, PURPLE, 12)
    grains(d, [(31, 26), (35, 33), (24, 40)], PURPLE, 1)


@deposit('lct_pegmatite')
def _lct_pegmatite(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    foliation(d, 8, 40, SEDIMENT, 4, 1.4, .65)
    polygon(d, [(13, 5), (23, 4), (35, 44), (25, 44)], QUARTZ, 1.15)
    polygon(d, [(17, 10), (22, 9), (30, 40), (25, 41)], GRANITE, .95)
    crystal(d, 21, 26, 4.2, 15, PURPLE, 8)
    crystal(d, 27, 40, 3.6, 12, QUARTZ, 10)
    book(d, 30, 17, 7, PURPLE, 3)


@deposit('nyf_pegmatite')
def _nyf_pegmatite(d):
    band(d, 4, 44, GRANITE, 4, 44, 1.05)
    d.ellipse(24, 25, 17, 15, QUARTZ, INK)
    hatch(d, [((11, 18), (15, 22)), ((15, 18), (19, 22)), ((31, 33), (35, 37)),
              ((35, 33), (39, 37)), ((10, 32), (14, 36))], INK, .6)
    d.ellipse(25, 26, 9, 7.5, WATER_PALE, INK)
    crystal(d, 20, 32, 4, 9, COAL, -28)
    crystal(d, 30, 32, 3.6, 8, PURPLE, 22)
    crystal(d, 25, 20, 3.6, 8, CARBONATE, 180)


@deposit('kimberlite_diamond')
def _kimberlite(d):
    strata(d, 14, 44, (27, 36), (SAND, ROCK, BASALT))
    polygon(d, [(12, 14), (36, 14), (31, 22), (17, 22)], SEDIMENT, 1.05)
    polygon(d, [(9, 11), (15, 13), (12, 14)], SEDIMENT, .85)
    polygon(d, [(39, 11), (33, 13), (36, 14)], SEDIMENT, .85)
    polygon(d, [(17, 22), (31, 22), (28, 36), (26, 44), (22, 44), (20, 36)], GREEN, 1.15)
    path(d, [(18, 28), (30, 28)], .8)
    path(d, [(20, 36), (28, 36)], .8)
    diamond(d, 24, 29, 4.2, QUARTZ)
    grains(d, [(21, 24), (27, 33), (23, 41)], BASALT, .9)


# --------------------------------------------------------------------------
# Magmatic-hydrothermal realm
# --------------------------------------------------------------------------

@deposit('porphyry_cu')
def _porphyry_cu(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    d.ellipse(24, 26, 20, 19, GREEN, INK)
    d.ellipse(24, 26, 14, 14, CLAY, INK)
    d.ellipse(24, 27, 8.5, 9, SAND, INK)
    for points in ([(13, 30), (24, 17), (34, 11)], [(11, 20), (23, 26), (36, 30)],
                   [(16, 11), (22, 25), (29, 35)], [(34, 15), (26, 26), (13, 34)],
                   [(19, 36), (30, 22), (38, 20)]):
        path(d, points, 1)
    magma_body(d, GRANITE, 36)
    grains(d, [(21, 24), (28, 23), (19, 31), (29, 31), (24, 35)], COPPER, 1.1)


@deposit('alkalic_porphyry')
def _alkalic_porphyry(d):
    band(d, 4, 44, BASALT, 4, 44, 1.05)
    pipe(d, 10, 44, 8, 5, 24, GRANITE, 1.15)
    d.ellipse(24, 21, 13.5, 11, None, CARBONATE)
    for points in ([(19, 36), (23, 24), (21, 13)], [(29, 37), (25, 25), (28, 14)]):
        vein(d, points, 2.2, CARBONATE)
    grains(d, [(21, 19), (27, 20), (24, 27), (20, 32), (28, 33)], GOLD, 1.15)
    grains(d, [(13, 20), (35, 22)], OXIDE, 1.2)


@deposit('porphyry_mo')
def _porphyry_mo(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    # Inverted-cup ore shell over a small, deep, high-silica stock.
    polygon(d, [(9, 30), (12, 19), (19, 12), (29, 12), (36, 19), (39, 30),
                (34, 30), (32, 21), (26, 16), (22, 16), (16, 21), (14, 30)], SULFIDE, 1.1)
    polygon(d, [(17, 44), (18, 33), (22, 26), (26, 26), (30, 33), (31, 44)], GRANITE, 1.15)
    book(d, 15, 26, 6, COAL, 2)
    book(d, 34, 26, 6, COAL, 2)
    grains(d, [(24, 34), (20, 39), (28, 39)], COAL, 1)


@deposit('porphyry_w_sn')
def _porphyry_w_sn(d):
    band(d, 4, 44, SEDIMENT, 4, 44, 1.05)
    polygon(d, [(14, 44), (15, 28), (20, 20), (28, 20), (33, 28), (34, 44)], GRANITE, 1.15)
    for x in (15, 20, 25, 30):
        path(d, [(x, 25), (x+2, 11)], 1.8, QUARTZ)
        path(d, [(x, 25), (x+2, 11)], .65, INK)
    blades(d, 24, 29, (72, 106), 10, 2.4, COAL)
    cube(d, 30, 34, 3.4, OXIDE)
    grains(d, [(18, 36), (25, 40)], OXIDE, 1)


@deposit('skarn')
def _skarn(d):
    strata(d, 6, 44, (18, 31), (CARBONATE, CARBONATE, CARBONATE))
    polygon(d, [(28, 5), (44, 5), (44, 44), (26, 44), (29, 32), (27, 18)], GRANITE, 1.15)
    polygon(d, [(21, 5), (28, 5), (27, 18), (29, 32), (26, 44), (19, 44),
                (22, 31), (20, 18)], GREEN, 1.1)
    polygon(d, [(15, 5), (21, 5), (20, 18), (22, 31), (19, 44), (13, 44),
                (16, 31), (14, 18)], IRON, 1.1)
    for x, y in ((17, 14), (19, 27), (16, 38)):
        diamond(d, x, y, 2.8, IRON)
    grains(d, [(23, 11), (25, 24), (22, 37)], SULFIDE, 1)


@deposit('crd_carbonate_replacement')
def _carbonate_replacement(d):
    strata(d, 7, 44, (17, 27, 37), (CARBONATE, CARBONATE, CARBONATE, CARBONATE))
    polygon(d, [(22, 10), (27, 10), (27, 41), (22, 41)], SULFIDE, 1.1)
    polygon(d, [(27, 18), (41, 19), (41, 24), (27, 23)], SULFIDE, 1.05)
    polygon(d, [(8, 29), (22, 28), (22, 33), (8, 32)], SULFIDE, 1.05)
    path(d, [(24.5, 44), (24.5, 41)], 1.4, GRANITE)
    d.arrow(24.5, 38, 24.5, 22, WATER)
    grains(d, [(34, 21.5), (15, 30.5)], COPPER, 1)
    cube(d, 24.5, 14, 2.8, COAL)


@deposit('manto_type_cu')
def _manto_cu(d):
    for index, y in enumerate((8, 17, 26, 35)):
        band(d, y, y+9, BASALT if index % 2 else ROCK, 4, 44, 1)
        for x in (10+index*3, 22+index*2, 34):
            d.circle(x, y+4.5, 1.3, CARBONATE, INK)
    seam(d, 17, COPPER, 3.4)
    path(d, [(34, 44), (31, 33), (29, 22), (31, 10)], 2.4)
    path(d, [(34, 44), (31, 33), (29, 22), (31, 10)], 1, WATER)
    grains(d, [(12, 18.8), (20, 18.8), (27, 18.8)], COPPER, .9)


@deposit('high_sulfidation_epithermal')
def _high_sulfidation(d):
    polygon(d, [(4, 24), (14, 22), (22, 10), (27, 10), (35, 22), (44, 24),
                (44, 44), (4, 44)], SEDIMENT, 1.1)
    # Vuggy residual silica ledge inside an advanced argillic lithocap.
    polygon(d, [(11, 25), (19, 13), (30, 13), (38, 25), (34, 29), (15, 29)], CLAY, 1.1)
    polygon(d, [(17, 24), (22, 15), (28, 15), (33, 24), (29, 26), (21, 26)], QUARTZ, 1.05)
    for x, y in ((21, 21), (25, 19), (28, 22), (24, 24)):
        d.circle(x, y, .9, SEDIMENT, INK)
    grains(d, [(20, 28), (27, 28), (32, 27)], GOLD, .95)
    for x in (22, 27):
        curve(d, [(x, 10), (x-3, 7), (x+3, 5), (x, 2)], ROCK, .9)
    d.arrow(24, 44, 24, 32, MELT)


@deposit('intermediate_sulfidation_epithermal')
def _intermediate_sulfidation(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    polygon(d, [(16, 4), (24, 4), (33, 44), (25, 44)], CARBONATE, 1.15)
    for offset, colour in ((1.5, SULFIDE), (4, QUARTZ), (6.5, COAL)):
        polygon(d, [(16+offset, 4), (17.5+offset, 4), (26.5+offset, 44), (25+offset, 44)],
                colour, .7)
    cube(d, 21, 16, 3, SULFIDE)
    cube(d, 27, 31, 3, COAL)
    grains(d, [(38, 16), (10, 33)], CARBONATE, 1.1)


@deposit('low_sulfidation_epithermal')
def _low_sulfidation(d):
    polygon(d, [(4, 15), (13, 14), (20, 9), (31, 9), (38, 14), (44, 15),
                (44, 44), (4, 44)], SAND, 1.1)
    # Sinter terrace above a colloform-banded adularia-sericite vein.
    for x0, x1, y in ((18, 34, 9), (20, 32, 7), (22, 30, 5)):
        polygon(d, [(x0, y), (x1, y), (x1-1.5, y-2), (x0+1.5, y-2)], QUARTZ, .85)
    polygon(d, [(19, 44), (21, 28), (20, 18), (23, 12), (28, 12), (26, 19),
                (28, 29), (27, 44)], QUARTZ, 1.15)
    for offset, colour in ((1.3, GOLD), (3, CARBONATE), (4.6, QUARTZ)):
        path(d, [(19.6+offset, 43), (21.6+offset, 28), (20.6+offset, 18), (23.6+offset, 13)],
             .8, colour)
    blades(d, 14, 26, (58, 86, 114), 6, 1.4, CARBONATE)
    droplet(d, 24, 3, 1.6)


@deposit('rirgs')
def _rirgs(d):
    band(d, 4, 44, SEDIMENT, 4, 44, 1.05)
    foliation(d, 6, 20, ROCK, 2, 1.2, .6)
    polygon(d, [(11, 44), (13, 30), (19, 22), (30, 22), (36, 30), (38, 44)], GRANITE, 1.15)
    for x in (16, 21, 26, 31):
        path(d, [(x, 42), (x, 24)], 1.9, QUARTZ)
        path(d, [(x, 42), (x, 24)], .6, INK)
        grains(d, [(x, 33)], GOLD, .95)
    d.dash((9, 20), (40, 20), ROCK, 8, .7)


@deposit('sn_w_granite')
def _sn_w_granite(d):
    band(d, 4, 44, SEDIMENT, 4, 44, 1.05)
    polygon(d, [(10, 44), (12, 28), (18, 18), (31, 18), (37, 28), (39, 44)], GRANITE, 1.15)
    polygon(d, [(13, 25), (18, 18), (31, 18), (36, 25), (30, 28), (19, 28)], QUARTZ, 1.05)
    grains(d, [(17, 23), (23, 21), (29, 23), (33, 26)], COAL, .85)
    vein(d, [(24, 18), (23, 10), (26, 4)], 3, QUARTZ)
    vein(d, [(14, 30), (10, 22), (11, 13)], 2.6, QUARTZ)
    cube(d, 24.5, 11, 3.2, OXIDE)
    cube(d, 11, 21, 2.6, OXIDE)


@deposit('be_f_replacement')
def _be_f_replacement(d):
    polygon(d, [(4, 18), (13, 17), (20, 9), (30, 9), (37, 17), (44, 18),
                (44, 44), (4, 44)], ROCK, 1.1)
    stack(d, (20, 26, 32, 38, 44), (SAND, CARBONATE, SAND, SEDIMENT), 4, 44, .95)
    seam(d, 26.4, PURPLE, 4.4)
    hatch(d, [((8, 23), (14, 23)), ((30, 22), (38, 22)), ((10, 35), (17, 35)),
              ((28, 41), (36, 41))], ROCK, .6)
    cube(d, 14, 28.5, 2.6, PURPLE)
    cube(d, 33, 28.5, 2.6, PURPLE)
    d.arrow(24, 42, 24, 31, MELT)


@deposit('magmatic_uranium')
def _magmatic_uranium(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    foliation(d, 7, 43, BASALT, 6, 2.1, .9)
    for points in ([(6, 16), (20, 13), (34, 17), (44, 14)],
                   [(5, 29), (18, 33), (33, 28), (44, 31)]):
        polygon(d, points+[(x, y+4) for x, y in reversed(points)], QUARTZ, .95)
    grains(d, [(13, 16.5), (24, 16.5), (36, 18.5), (12, 32), (26, 32), (38, 31)], OXIDE, 1.05)
    crystal(d, 36, 42, 3.4, 8, GRANITE, 8)


@deposit('iocg')
def _iocg(d):
    strata(d, 4, 44, (16, 30), (ROCK, SEDIMENT, ROCK))
    polygon(d, [(15, 6), (33, 6), (31, 24), (28, 44), (20, 44), (17, 24)], IRON, 1.15)
    clasts(d, [(21, 12, 3.2, 15), (28, 15, 2.8, -25), (23, 21, 3, 40),
               (27, 29, 2.6, -10), (22, 35, 2.4, 25), (26, 40, 2.2, -35)], ROCK, .8)
    grains(d, [(19, 17), (30, 21), (20, 27), (29, 35), (24, 42)], COPPER, 1.05)
    d.arrow(9, 40, 16, 34, WATER)
    d.arrow(39, 40, 32, 34, WATER)


@deposit('iron_oxide_apatite')
def _iron_oxide_apatite(d):
    band(d, 4, 44, BASALT, 4, 44, 1.05)
    polygon(d, [(14, 6), (26, 5), (33, 20), (31, 34), (23, 43), (15, 41),
                (12, 26)], OXIDE, 1.2)
    for x, y, angle in ((19, 20, -12), (26, 24, 14), (21, 33, 6), (28, 36, -18)):
        crystal(d, x, y, 3, 8, QUARTZ, angle)
    grains(d, [(16, 12), (29, 13), (17, 38)], IRON, 1)
    for points in ([(33, 12), (40, 9)], [(34, 30), (41, 33)], [(9, 18), (6, 14)]):
        path(d, points, 2.2, OXIDE)


# --------------------------------------------------------------------------
# Metamorphic and orogenic realm
# --------------------------------------------------------------------------

@deposit('orogenic_gold')
def _orogenic_gold(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    polygon(d, [(7, 44), (19, 44), (41, 8), (29, 8)], GREEN, 1.1)
    for offset in (-6, 0, 6):
        curve(d, [(12+offset, 42), (22+offset, 32), (24+offset, 22), (34+offset, 10)],
              SEDIMENT, .75)
    vein(d, [(13, 41), (22, 29), (29, 19), (34, 10)], 4.4, QUARTZ)
    path(d, [(13.8, 41.5), (22.8, 29.5), (29.8, 19.5), (34.8, 10.5)], .55)
    path(d, [(12.2, 40.5), (21.2, 28.5), (28.2, 18.5), (33.2, 9.5)], .55)
    grains(d, [(17, 35), (25, 25), (31, 15)], GOLD, 1.05)
    for x, y in ((9, 22), (38, 30)):
        curve(d, [(x-3, y+4), (x, y+2), (x, y-2), (x+3, y-4)], QUARTZ, 2.2)


@deposit('listwaenite_gold')
def _listwaenite(d):
    band(d, 4, 44, GREEN, 4, 44, 1.05)
    polygon(d, [(26, 4), (36, 4), (24, 44), (14, 44)], CARBONATE, 1.1)
    path(d, [(31, 4), (19, 44)], 2.6)
    for points in ([(24, 15), (30, 11)], [(20, 28), (26, 24)], [(17, 38), (23, 34)]):
        vein(d, points, 2.6, QUARTZ)
    grains(d, [(27, 13), (23, 26), (20, 36)], GOLD, 1.1)
    hatch(d, [((7, 14), (13, 16)), ((6, 28), (12, 27)), ((38, 36), (43, 38))], BASALT, .8)
    cube(d, 33, 20, 3, CARBONATE)


@deposit('sb_hg_epizonal')
def _sb_hg(d):
    polygon(d, [(4, 13), (15, 12), (24, 14), (34, 11), (44, 13), (44, 44), (4, 44)],
            SEDIMENT, 1.1)
    polygon(d, [(21, 44), (20, 30), (22, 20), (21, 12), (27, 12), (26, 20),
                (28, 30), (27, 44)], QUARTZ, 1.15)
    blades(d, 24, 25, (248, 278, 308, 62, 92, 122), 7.5, 1.5, COAL)
    grains(d, [(20, 34), (28, 36), (24, 40)], IRON, 1.1)
    d.arrow(24, 10, 24, 5, WATER_PALE)
    hatch(d, [((9, 20), (15, 21)), ((33, 26), (40, 25)), ((8, 35), (14, 36))], ROCK, .6)


@deposit('carlin_type_gold')
def _carlin(d):
    strata(d, 7, 44, (16, 26, 35), (CARBONATE, SEDIMENT, CARBONATE, CARBONATE))
    polygon(d, [(4, 24), (44, 20), (44, 25), (4, 29)], CLAY, .9)
    polygon(d, [(10, 22), (26, 19), (38, 21), (38, 25), (25, 23), (10, 26)], IRON, 1)
    path(d, [(34, 44), (30, 33), (27, 24), (29, 12)], 2.3)
    d.arrow(32, 38, 29, 27, WATER)
    grains(d, [(14, 24), (20, 23), (26, 22.5), (33, 23.5)], GOLD, .75)
    hatch(d, [((8, 12), (16, 12)), ((28, 39), (37, 39))], ROCK, .6)


@deposit('graphite_metamorphic')
def _graphite(d):
    def trace(offset):
        return [(4+40*i/40, 10+offset+4.2*math.sin(i/40*math.tau*1.35)) for i in range(41)]
    for index, colour in enumerate((ROCK, COAL, SEDIMENT, ROCK)):
        polygon(d, trace(index*7)+list(reversed(trace((index+1)*7))), colour, .95)
    vein(d, [(30, 44), (26, 30), (29, 18), (26, 6)], 3.4, COAL)
    book(d, 14, 38, 11, COAL, 3)
    grains(d, [(36, 20), (39, 33)], COAL, 1.1)


@deposit('magnesite_talc')
def _magnesite_talc(d):
    band(d, 4, 44, SEDIMENT, 4, 44, 1.05)
    polygon(d, [(9, 11), (34, 7), (43, 20), (40, 38), (22, 44), (8, 33)], GREEN, 1.15)
    for points in ([(12, 20), (24, 17), (36, 21)], [(14, 30), (27, 28), (39, 31)],
                   [(19, 13), (21, 26), (18, 39)], [(31, 11), (29, 25), (32, 38)]):
        vein(d, points, 2.4, CARBONATE)
    polygon(d, [(9, 11), (34, 7), (36, 13), (11, 17)], CLAY, 1)
    book(d, 21, 13, 10, CLAY, 2)
    grains(d, [(16, 24), (34, 34)], CARBONATE, 1)


# --------------------------------------------------------------------------
# Basinal and diagenetic hydrothermal realm
# --------------------------------------------------------------------------

@deposit('sedex_clastic_dominated')
def _sedex(d):
    stack(d, (10, 19, 30, 44), (SEDIMENT, COAL, SEDIMENT))
    # Laminated, vent-proximal stratiform lens thinning away from the feeder.
    top = [(7, 24), (15, 22.5), (24, 21), (32, 20), (39, 19.5)]
    polygon(d, top+[(39, 28), (32, 27.5), (24, 26.5), (15, 26), (7, 26)], SULFIDE, 1.1)
    for offset in (1.8, 3.6):
        path(d, [(x, y+offset) for x, y in top], .7, COAL)
    path(d, [(42, 44), (39, 34), (38, 26), (39, 19)], 2.6)
    path(d, [(42, 44), (39, 34), (38, 26), (39, 19)], 1.1, WATER)
    d.arrow(39, 37, 39, 25, IRON)
    d.wave(6, 22, 8, 1.1, 1, WATER)
    grains(d, [(13, 15), (26, 14)], COAL, .9)


@deposit('mvt_zn_pb')
def _mvt(d):
    stack(d, (7, 18, 30, 44), (CARBONATE, CARBONATE, CARBONATE))
    # Karst void and collapse breccia filled by sphalerite and galena.
    polygon(d, [(13, 22), (20, 19), (30, 20), (36, 25), (34, 31), (24, 34),
                (15, 30)], SEDIMENT, 1.1)
    clasts(d, [(18, 24, 2.4, 12), (26, 23, 2.2, -20), (31, 28, 2, 30),
               (20, 30, 2.1, -8)], CARBONATE, .75)
    grains(d, [(23, 27), (29, 25), (17, 28), (33, 27)], SULFIDE, 1.05)
    cube(d, 24, 38, 3, COAL)
    d.arrow(4, 36, 14, 33, WATER)
    d.arrow(44, 14, 36, 20, WATER)


@deposit('irish_type_zn_pb')
def _irish_type(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    band(d, 4, 13, WATER_PALE, 4, 44, .95)
    # Carbonate wedge thickening into a syn-rift normal fault.
    polygon(d, [(4, 13), (28, 13), (17, 43), (4, 43)], CARBONATE, 1.15)
    polygon(d, [(13, 42), (21, 35), (26, 28), (24, 25), (16, 32), (9, 41)], SULFIDE, 1.1)
    path(d, [(31, 5), (14, 44)], 2.6)
    d.wave(5, 43, 7, 1.2, 2, WATER)
    d.arrow(35, 14, 28, 26, WATER)
    d.arrow(20, 42, 24, 31, IRON)
    grains(d, [(15, 38), (21, 31)], SULFIDE, .9)


@deposit('sediment_hosted_stratiform_cu')
def _stratiform_cu(d):
    stack(d, (6, 18, 34, 44), (IRON, COAL, IRON))
    front = [(4+40*i/20, 22+3.4*math.sin(i/20*math.tau*1.1)) for i in range(21)]
    for offset, colour in ((0, COPPER), (3.4, SULFIDE), (6.8, COAL)):
        polygon(d, [(x, y+offset) for x, y in front]
                + [(x, y+offset+3.4) for x, y in reversed(front)], colour, .85)
    grains(d, [(12, 23), (24, 21), (36, 23)], COPPER, .85)
    d.arrow(9, 12, 9, 19, WATER)
    d.arrow(38, 12, 38, 19, WATER)
    hatch(d, [((10, 40), (18, 40)), ((28, 38), (37, 38))], ROCK, .6)


@deposit('unconformity_uranium')
def _unconformity_uranium(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    polygon(d, [(4, 7), (18, 8), (31, 6), (44, 8), (44, 24), (30, 23),
                (16, 25), (4, 23)], SAND, 1.1)
    foliation(d, 28, 42, BASALT, 3, 1.8, .8)
    path(d, [(4, 23), (16, 25), (30, 23), (44, 24)], 1.6)
    path(d, [(34, 44), (29, 34), (25, 26), (22, 16)], 2.4, COAL)
    polygon(d, [(21, 18), (28, 20), (31, 27), (26, 32), (19, 29), (18, 23)], OXIDE, 1.1)
    d.ellipse(24.5, 25, 13, 10, None, CLAY)
    grains(d, [(22, 24), (27, 26)], GOLD, .9)


@deposit('sandstone_hosted_uranium')
def _sandstone_uranium(d):
    band(d, 4, 44, COAL, 4, 44, 1.05)
    polygon(d, [(4, 16), (14, 12), (28, 11), (40, 14), (44, 18), (44, 32),
                (30, 35), (16, 34), (4, 30)], SAND, 1.15)
    polygon(d, [(4, 17), (14, 13), (24, 13), (24, 33), (14, 33), (4, 29)], IRON, 1.05)
    polygon(d, [(24, 13), (29, 15), (31, 22), (29, 30), (24, 33), (27, 27),
                (28, 22), (27, 17)], OXIDE, 1.1)
    d.arrow(8, 22, 19, 22, WATER)
    grains(d, [(33, 18), (36, 27)], ROCK, 1)
    hatch(d, [((8, 38), (16, 38)), ((28, 40), (38, 40)), ((10, 8), (20, 8))], ROCK, .6)


@deposit('five_element_vein')
def _five_element(d):
    band(d, 4, 44, SEDIMENT, 4, 44, 1.05)
    polygon(d, [(17, 4), (27, 4), (31, 44), (21, 44)], CARBONATE, 1.15)
    for y in (11, 37):
        d.ellipse(23.5, y, 4.4, 3.2, ROCK, INK)
        d.ellipse(23.5, y, 2.4, 1.7, CARBONATE, INK)
    # Dendritic native silver with arsenide branches.
    for y in (20, 29):
        path(d, [(19, y+3), (23.5, y), (28, y+3)], 1.2, ROCK)
        for x, direction in ((21, -1), (26, 1)):
            path(d, [(x, y+1.7), (x+direction*2.6, y-.6)], 1, ROCK)
        path(d, [(23.5, y), (23.5, y-3.4)], 1.1, ROCK)
    grains(d, [(19, 44), (28, 5)], OXIDE, 1)


@deposit('fluorite_barite_vein_strata')
def _fluorite_barite(d):
    stack(d, (7, 17, 27, 37, 44), (CARBONATE, SEDIMENT, CARBONATE, SEDIMENT))
    polygon(d, [(20, 5), (26, 5), (29, 44), (23, 44)], PURPLE, 1.15)
    polygon(d, [(6, 18), (21, 17), (21, 23), (6, 24)], PURPLE, 1.05)
    polygon(d, [(27, 29), (42, 28), (42, 34), (27, 35)], PURPLE, 1.05)
    cube(d, 13, 20.5, 3, PURPLE)
    cube(d, 35, 31.5, 3, PURPLE)
    blades(d, 24, 10, (74, 106), 7, 1.8, QUARTZ)
    grains(d, [(24, 26), (26, 38)], CARBONATE, .95)


# --------------------------------------------------------------------------
# Submarine hydrothermal realm
# --------------------------------------------------------------------------

@deposit('vms_clan')
def _vms(d):
    band(d, 4, 44, BASALT, 4, 44, 1.05)
    band(d, 4, 14, SEDIMENT, 4, 44, 1)
    polygon(d, [(24, 44), (13, 25), (35, 25)], GREEN, 1.1)
    for points in ([(24, 42), (23, 33), (24, 26)], [(19, 40), (21, 32), (22, 27)],
                   [(29, 40), (27, 32), (26, 27)]):
        path(d, points, 1.5, SULFIDE)
    polygon(d, [(12, 25), (18, 17), (30, 17), (36, 25)], SULFIDE, 1.15)
    seam(d, 14, CARBONATE, 1.8)
    grains(d, [(16, 22), (24, 21), (31, 22)], COAL, .85)


@deposit('seafloor_massive_sulfide')
def _sms(d):
    band(d, 4, 44, BASALT, 4, 44, 1.05)
    band(d, 4, 26, WATER_PALE, 4, 44, .95)
    polygon(d, [(4, 26), (14, 27), (18, 33), (30, 33), (34, 26), (44, 27),
                (44, 44), (4, 44)], BASALT, 1.1)
    for x, height in ((19, 8), (24, 11), (29, 7)):
        polygon(d, [(x-2, 33), (x-1.3, 33-height), (x+1.3, 33-height), (x+2, 33)], SULFIDE, 1)
    for x, y in ((19, 25), (24, 22)):
        curve(d, [(x, y), (x-4, y-5), (x+2, y-9), (x-2, y-14)], COAL, 1.2)
    hatch(d, [((10, 36), (10, 43)), ((14, 37), (14, 43)), ((34, 36), (34, 43)),
              ((38, 37), (38, 43))], ROCK, .7)
    grains(d, [(15, 32), (33, 32)], SULFIDE, .9)
    d.wave(5, 43, 8, 1.2, 2, WATER)


# --------------------------------------------------------------------------
# Sedimentary and chemical-sedimentary realm
# --------------------------------------------------------------------------

@deposit('bif_iron_formation')
def _bif(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    for index in range(10):
        offset = index*3.9
        polygon(d, [(4, 6+offset), (44, 2+offset), (44, 4.9+offset), (4, 8.9+offset)],
                IRON if index % 2 == 0 else QUARTZ, .7)
    grains(d, [(12, 20), (31, 26)], OXIDE, 1.2)


@deposit('sedimentary_manganese')
def _sed_manganese(d):
    band(d, 4, 16, WATER_PALE, 4, 44, .95)
    stack(d, (16, 24, 34, 44), (SEDIMENT, SAND, SEDIMENT))
    band(d, 24, 32, OXIDE, 4, 44, 1.05)
    for x in (9, 16, 23, 30, 37, 42):
        d.circle(x, 28, 2, ROCK, INK)
        d.circle(x, 28, .9, OXIDE, INK)
    d.wave(5, 43, 7, 1.2, 2, WATER)
    d.arrow(38, 14, 28, 20, WATER)


@deposit('ferromanganese_nodule_crust')
def _ferromanganese(d):
    band(d, 4, 44, WATER_PALE, 4, 44, .95)
    polygon(d, [(4, 33), (13, 32), (22, 33), (28, 27), (36, 25), (44, 29),
                (44, 44), (4, 44)], SEDIMENT, 1.1)
    # Manganese crust mantling a seamount flank, nodules on the abyssal floor.
    polygon(d, [(22, 33), (28, 27), (36, 25), (44, 29), (44, 32), (36, 28),
                (29, 30), (23, 36)], OXIDE, 1)
    for x, y, radius in ((9, 31, 2.6), (16, 35, 2.2), (12, 40, 2.4), (21, 40, 2)):
        nodule(d, x, y, radius)
    d.wave(5, 43, 9, 1.3, 2, WATER)


@deposit('phosphorite')
def _phosphorite(d):
    band(d, 4, 44, WATER_PALE, 4, 44, .95)
    polygon(d, [(4, 22), (16, 23), (26, 30), (33, 39), (44, 41), (44, 44), (4, 44)],
            SEDIMENT, 1.1)
    polygon(d, [(4, 22), (16, 23), (26, 30), (25, 34), (15, 27), (4, 26)], CARBONATE, 1.1)
    grains(d, [(8, 24), (13, 25), (18, 27), (22, 30)], CLAY, 1.05)
    curve(d, [(36, 41), (32, 36), (31, 31), (27, 28)], WATER, 1.1)
    d.arrow(29, 29, 24, 25, WATER)
    d.wave(5, 43, 8, 1.2, 2, WATER)


@deposit('black_shale_polymetallic')
def _black_shale(d):
    band(d, 4, 44, COAL, 4, 44, 1.05)
    band(d, 4, 12, ROCK, 4, 44, .95)
    for y in (17, 22, 32, 38):
        seam(d, y, SULFIDE, 1, 6, 42)
    seam(d, 26, OXIDE, 3.2, 5, 43)
    grains(d, [(12, 27.5), (24, 27.5), (36, 27.5)], SULFIDE, .9)
    d.wave(5, 9, 6, 1, 2, WATER)


@deposit('evaporite_potash')
def _potash(d):
    band(d, 4, 12, WATER_PALE, 4, 44, .95)
    stack(d, (12, 18, 24, 30, 36, 44), (QUARTZ, CARBONATE, PURPLE, QUARTZ, CARBONATE))
    cube(d, 13, 27, 3.4, PURPLE)
    cube(d, 35, 27, 3.4, PURPLE)
    cube(d, 24, 15, 3.2, QUARTZ)
    for x in (10, 22, 34):
        d.arrow(x, 10, x, 4, WATER)
    hatch(d, [((8, 40), (17, 40)), ((28, 39), (38, 39))], ROCK, .6)


# --------------------------------------------------------------------------
# Surficial and weathering realm
# --------------------------------------------------------------------------

@deposit('bauxite')
def _bauxite(d):
    stack(d, (8, 20, 32, 44), (CLAY, SAND, ROCK))
    for x in (9, 15, 21, 27, 33, 39):
        d.circle(x, 14, 2.2, SEDIMENT, INK)
        d.circle(x, 14, 1, CLAY, INK)
    hatch(d, [((8, 26), (16, 25)), ((26, 27), (36, 26)), ((10, 38), (20, 38)),
              ((28, 40), (38, 39))], ROCK, .6)
    for x in (14, 34):
        d.arrow(x, 5, x, 10, WATER)


@deposit('nickel_laterite')
def _nickel_laterite(d):
    stack(d, (8, 18, 30, 44), (IRON, SAND, GREEN))
    for points in ([(8, 22), (14, 26), (12, 30)], [(22, 20), (26, 25), (24, 30)],
                   [(33, 21), (38, 26), (36, 30)]):
        vein(d, points, 2.2, GREEN)
    grains(d, [(12, 13), (24, 12), (36, 13)], OXIDE, 1.1)
    clasts(d, [(17, 36, 3, 18), (31, 38, 2.6, -22)], BASALT, .8)
    droplet(d, 20, 5, 1.6)
    droplet(d, 30, 5, 1.6)


@deposit('ion_adsorption_clay_ree')
def _ion_adsorption(d):
    stack(d, (9, 15, 31, 44), (SAND, CLAY, GRANITE))
    book(d, 14, 27, 14, SEDIMENT, 3)
    book(d, 33, 26, 13, SEDIMENT, 3)
    grains(d, [(9, 20), (20, 18), (29, 20), (39, 18), (24, 29), (38, 30)], PURPLE, 1.2)
    hatch(d, [((8, 38), (14, 36)), ((21, 41), (27, 39)), ((33, 36), (40, 38))], ROCK, .65)
    for x in (18, 32):
        d.arrow(x, 5, x, 12, WATER)


@deposit('supergene_iron_enrichment')
def _supergene_iron(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    for index in range(6):
        offset = index*3.6
        polygon(d, [(4, 24+offset), (44, 22+offset), (44, 24.4+offset), (4, 26.4+offset)],
                IRON if index % 2 == 0 else QUARTZ, .7)
    polygon(d, [(4, 9), (16, 8), (30, 10), (44, 8), (44, 24), (30, 26),
                (16, 24), (4, 25)], IRON, 1.15)
    band(d, 5, 9, SEDIMENT, 4, 44, .95)
    grains(d, [(12, 17), (24, 18), (36, 17)], OXIDE, 1.1)


@deposit('channel_iron_deposit')
def _channel_iron(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    polygon(d, [(6, 14), (14, 13), (18, 26), (30, 30), (36, 20), (42, 14),
                (42, 10), (6, 10)], SEDIMENT, 1.05)
    polygon(d, [(10, 13), (38, 13), (34, 24), (27, 31), (19, 29), (14, 21)], IRON, 1.15)
    for x, y in ((17, 18), (23, 21), (29, 23), (33, 18), (20, 25), (27, 27)):
        d.circle(x, y, 1.9, OXIDE, INK)
        d.circle(x, y, .8, SEDIMENT, INK)
    hatch(d, [((7, 34), (15, 33)), ((25, 38), (35, 37)), ((33, 8), (41, 8))], ROCK, .6)


@deposit('supergene_copper')
def _supergene_copper(d):
    stack(d, (8, 18, 26, 32, 44), (SAND, GREEN, COAL, ROCK))
    grains(d, [(11, 13), (22, 12), (34, 13)], IRON, 1.1)
    d.dash((4, 26), (44, 26), WATER, 10, .9)
    grains(d, [(14, 29), (24, 29), (34, 29)], SULFIDE, 1)
    grains(d, [(12, 38), (26, 40), (37, 37)], COPPER, 1)
    for x in (17, 31):
        d.arrow(x, 4, x, 11, WATER)


@deposit('non_sulfide_zn')
def _non_sulfide_zn(d):
    stack(d, (7, 20, 32, 44), (CARBONATE, CARBONATE, CARBONATE))
    polygon(d, [(12, 18), (20, 13), (30, 14), (35, 20), (34, 27), (28, 32),
                (18, 31), (12, 25)], IRON, 1.15)
    grains(d, [(18, 21), (25, 19), (30, 24), (21, 27), (28, 29)], QUARTZ, 1.3)
    polygon(d, [(17, 30), (31, 31), (29, 35), (20, 35)], SULFIDE, 1.05)
    for x in (10, 38):
        d.arrow(x, 5, x, 14, WATER)
    d.arrow(24, 10, 24, 15, WATER)
    hatch(d, [((7, 36), (14, 36)), ((33, 40), (41, 40))], ROCK, .6)


@deposit('lithium_brine')
def _lithium_brine(d):
    polygon(d, [(4, 16), (13, 26), (24, 29), (35, 26), (44, 16), (44, 44), (4, 44)],
            ROCK, 1.1)
    polygon(d, [(10, 24), (20, 29), (30, 29), (39, 24), (36, 38), (14, 38)],
            WATER_PALE, 1.1)
    seam(d, 27.5, QUARTZ, 2.4, 13, 36)
    grains(d, [(19, 34), (25, 35), (31, 33)], CARBONATE, .9)
    for x in (17, 24, 31):
        d.arrow(x, 22, x, 13, WATER)
    d.arrow(7, 22, 13, 27, WATER)
    cube(d, 24, 42, 3, QUARTZ)


@deposit('lithium_clay')
def _lithium_clay(d):
    polygon(d, [(4, 10), (10, 18), (17, 22), (31, 22), (38, 18), (44, 10),
                (44, 44), (4, 44)], ROCK, 1.1)
    stack(d, (24, 30, 36, 44), (CLAY, SEDIMENT, CLAY), 10, 38, .95)
    book(d, 17, 33, 10, CLAY, 3)
    book(d, 31, 33, 10, CLAY, 3)
    grains(d, [(24, 27), (14, 40), (34, 40)], PURPLE, 1)
    hatch(d, [((6, 16), (9, 20)), ((39, 20), (42, 16))], ROCK, .7)


@deposit('borate_nitrate')
def _borate_nitrate(d):
    stack(d, (12, 20, 30, 44), (QUARTZ, SAND, SEDIMENT))
    for x in (9, 17, 25, 33, 41):
        path(d, [(x, 12), (x+1.5, 20)], .7)
    crystal(d, 14, 29, 4.2, 8, QUARTZ, -12)
    crystal(d, 24, 30, 4.6, 9, QUARTZ, 4)
    crystal(d, 34, 29, 4, 7.5, QUARTZ, 14)
    seam(d, 36, CARBONATE, 2.4)
    for x in (12, 36):
        d.arrow(x, 9, x, 4, WATER)


@deposit('calcrete_uranium')
def _calcrete_uranium(d):
    polygon(d, [(4, 10), (13, 14), (24, 20), (35, 14), (44, 10), (44, 44), (4, 44)],
            SAND, 1.1)
    polygon(d, [(9, 18), (17, 23), (24, 25), (32, 23), (39, 18), (37, 28),
                (24, 31), (11, 28)], QUARTZ, 1.15)
    grains(d, [(17, 26), (24, 27.5), (31, 26)], GOLD, 1.1)
    d.dash((6, 33), (42, 33), WATER, 9, .8)
    d.arrow(13, 36, 24, 34, WATER)
    hatch(d, [((8, 14), (12, 16)), ((36, 16), (40, 14))], ROCK, .65)


# --------------------------------------------------------------------------
# Clastic and mechanical realm
# --------------------------------------------------------------------------

@deposit('placer_gold')
def _placer_gold(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    # Bedrock riffles trap gold at the base of a gravel terrace.
    riffle = [(4, 30)]
    for index in range(8):
        riffle += [(6+index*5, 34), (8.5+index*5, 29)]
    riffle += [(44, 32), (44, 44), (4, 44)]
    polygon(d, riffle, BASALT, 1.1)
    polygon(d, [(4, 14), (16, 12), (30, 15), (44, 13), (44, 31), (4, 30)], SAND, 1.1)
    for x, y, radius in ((11, 20, 2.4), (20, 18, 2.8), (29, 21, 2.2), (37, 19, 2.6),
                         (16, 25, 2.1), (33, 26, 2)):
        d.ellipse(x, y, radius, radius*.68, ROCK, INK)
    grains(d, [(11, 31), (21, 31), (31, 32), (39, 31)], GOLD, 1.1)
    d.wave(6, 20, 9, 1, 1, WATER)


@deposit('quartz_pebble_conglomerate_gold_u')
def _banket(d):
    band(d, 4, 44, SEDIMENT, 4, 44, 1.05)
    polygon(d, [(4, 18), (44, 13), (44, 26), (4, 31)], SAND, 1.1)
    for x, y in ((9, 26), (17, 24), (25, 22), (33, 20), (40, 18.5),
                 (13, 21), (29, 17), (37, 24)):
        d.circle(x, y, 2.6, QUARTZ, INK)
    grains(d, [(12, 29.6), (21, 28.4), (31, 27), (39, 25.8)], GOLD, 1)
    hatch(d, [((8, 10), (18, 9)), ((28, 38), (38, 37))], ROCK, .6)


@deposit('heavy_mineral_sands')
def _mineral_sands(d):
    band(d, 4, 20, WATER_PALE, 4, 20, .95)
    polygon(d, [(4, 20), (16, 21), (26, 16), (33, 10), (40, 13), (44, 20),
                (44, 44), (4, 44)], SAND, 1.1)
    for offset in (0, 3.2, 6.4):
        path(d, [(8+offset*.4, 24+offset), (18+offset*.4, 24+offset),
                 (27+offset*.4, 20+offset), (34+offset*.4, 16+offset)], 1.5, COAL)
    d.wave(5, 18, 10, 1.3, 2, WATER)
    d.arrow(7, 15, 15, 19, WATER)
    grains(d, [(23, 27), (31, 25)], OXIDE, 1)


@deposit('placer_tin')
def _placer_tin(d):
    band(d, 4, 18, WATER_PALE, 4, 44, .95)
    polygon(d, [(4, 18), (12, 20), (18, 30), (30, 30), (36, 20), (44, 18),
                (44, 44), (4, 44)], GRANITE, 1.1)
    polygon(d, [(4, 18), (12, 20), (18, 30), (30, 30), (36, 20), (44, 18),
                (44, 24), (34, 26), (28, 34), (20, 34), (14, 26), (4, 24)],
            SEDIMENT, 1.05)
    polygon(d, [(14, 26), (20, 34), (28, 34), (34, 26), (28, 28), (20, 28)], SAND, 1.05)
    cube(d, 20, 31, 2.8, OXIDE)
    cube(d, 28, 31, 2.8, OXIDE)
    grains(d, [(24, 32), (16, 27)], OXIDE, .85)
    d.wave(5, 43, 8, 1.3, 2, WATER)


@deposit('placer_diamond')
def _placer_diamond(d):
    band(d, 4, 44, ROCK, 4, 44, 1.05)
    polygon(d, [(4, 26), (11, 27), (14, 35), (19, 36), (22, 27), (29, 27),
                (32, 37), (37, 36), (39, 27), (44, 26), (44, 44), (4, 44)], BASALT, 1.1)
    polygon(d, [(4, 13), (15, 11), (28, 14), (44, 12), (44, 27), (4, 27)], SAND, 1.1)
    for x, y, radius in ((10, 19, 2.6), (19, 17, 2.4), (28, 20, 2.8), (37, 18, 2.4)):
        d.ellipse(x, y, radius, radius*.7, ROCK, INK)
    diamond(d, 16.5, 32, 3.4, GEM)
    diamond(d, 34.5, 32, 3, GEM)
    d.wave(6, 22, 8, 1, 1, WATER)


# --------------------------------------------------------------------------
# Hybrid and industrial realm
# --------------------------------------------------------------------------

@deposit('industrial_minerals_overview')
def _industrial_overview(d):
    stack(d, (8, 16, 24, 32, 44), (CLAY, CARBONATE, SAND, ROCK))
    # Stepped quarry benches cut down into the sequence, with a product stockpile.
    polygon(d, [(4, 8), (34, 8), (34, 16), (26, 16), (26, 24), (18, 24),
                (18, 32), (4, 32)], QUARTZ, 1.1)
    for x0, x1, y in ((4, 34, 8), (4, 26, 16), (4, 18, 24)):
        path(d, [(x0, y), (x1, y)], .65)
    polygon(d, [(6, 32), (11, 22), (16, 32)], CLAY, 1.1)
    crystal(d, 38, 29, 5, 11, QUARTZ, 8)
    cube(d, 24, 39, 3.6, CARBONATE)


@deposit('gemstone_systems')
def _gemstone(d):
    band(d, 4, 44, GREEN, 4, 44, 1.05)
    foliation(d, 6, 42, BASALT, 5, 1.6, .7)
    polygon(d, [(12, 4), (20, 4), (33, 44), (25, 44)], QUARTZ, 1.15)
    # Hexagonal beryl prism in the vein, corundum barrel and an opal nodule.
    polygon(d, [(19, 22), (23, 20), (27, 23), (26, 30), (22, 32), (18, 29)], GEM, 1.05)
    path(d, [(19, 22), (26, 25), (27, 23)], .65)
    path(d, [(26, 25), (22, 32)], .65)
    polygon(d, [(14, 12), (19, 10), (21, 14), (19, 18), (14, 17), (13, 15)], PURPLE, 1)
    d.ellipse(35, 31, 5, 4, WATER_PALE, INK)
    grains(d, [(35, 31)], GEM, 1.4)


@deposit('energy_adjacent_note')
def _energy_adjacent(d):
    stack(d, (16, 24, 32, 44), (SAND, SEDIMENT, ROCK))
    arch = [(4+40*i/20, 28-6*math.sin(math.pi*i/20)) for i in range(21)]
    polygon(d, arch+[(x, y+5) for x, y in reversed(arch)], QUARTZ, 1)
    polygon(d, [(x, y+.4) for x, y in arch[6:15]]
            + [(x, y+2.6) for x, y in reversed(arch[6:15])], MELT, .9)
    seam(d, 36, COAL, 3)
    for x in (12, 24, 36):
        curve(d, [(x, 14), (x-3.5, 11), (x+3, 8), (x, 4)], ROCK, 1)
    grains(d, [(18, 37.5), (30, 37.5)], COAL, .85)
