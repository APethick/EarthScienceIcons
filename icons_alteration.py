"""Geochemistry processes and all 24 Opus AlterationType descriptors.

Illustrative mineral colours, not a diagnostic colour legend. Distinct habits,
assemblages, reaction fronts and geological settings identify each alteration.
All designs are text-free and generate both detailed font and colour artwork.
"""
import json
import math
from functools import lru_cache, partial
from pathlib import Path
from shapely import affinity
from shapely.geometry import Point, Polygon
from icons_mt import Drawing, INK, STEEL, GLASS, SOIL, SAND, PAPER, GRID
from icons_geophysics_expanded import native

QUARTZ = '#DCE5E4'
FELDSPAR = '#CFABA0'
ALBITE = '#E1E1D8'
EPIDOTE = '#8E9E59'
CHLORITE = '#5C7E68'
SERPENTINE = '#78916A'
CALCITE = '#DDD3B8'
GARNET = '#974D43'
PYROXENE = '#596F60'
MICA = '#C1BEA4'
CLAY = '#C4A587'
KAOLIN = '#E8E4D6'
ALUNITE = '#E2CBB4'
PYRITE = '#BDA260'
HEMATITE = '#A55B48'
BIOTITE = '#685548'
BASALT = '#596462'
GRANITE = '#B89D92'
WATER = '#5D9EB8'
HEAT = '#D58659'


def host(d, colour='#9AA29A'):
    d.poly([(5, 15), (13, 7), (33, 6), (43, 15), (44, 35),
            (35, 43), (13, 44), (4, 34)], colour, INK)
    d.line([(5, 25), (10, 23), (15, 26)], STEEL, .65)
    d.line([(31, 42), (29, 36), (32, 32)], STEEL, .65)
    return d


def crystal(d, x, y, width=5, height=13, colour=QUARTZ, angle=0):
    def rotate(points):
        a = math.radians(angle)
        return [(x+u*math.cos(a)-v*math.sin(a), y+u*math.sin(a)+v*math.cos(a)) for u, v in points]
    points = [(-width/2, 0), (-width/2, -height+width*.6), (0, -height),
              (width/2, -height+width*.6), (width/2, 0)]
    d.poly(rotate(points), colour, INK)
    d.line(rotate([(0, 0), (0, -height)]), INK, .55)
    d.line(rotate([(-width/2, -height+width*.6), (0, -height+width),
                   (width/2, -height+width*.6)]), INK, .55)


def rhomb(d, x, y, scale=1, colour=CALCITE):
    d.poly([(x-5*scale, y), (x-1*scale, y-4*scale), (x+5*scale, y-2*scale),
            (x+1*scale, y+2*scale)], colour, INK)
    d.line([(x-1*scale, y-4*scale), (x-1*scale, y-.8*scale), (x+1*scale, y+2*scale)], INK, .55)
    d.line([(x-5*scale, y), (x-1*scale, y-.8*scale), (x+5*scale, y-2*scale)], INK, .55)


def mica_book(d, x, y, colour=MICA, width=12, layers=4, angle=0):
    for i in reversed(range(layers)):
        dy = i*1.3
        d.poly([(x-width/2, y+dy), (x-width*.18, y-3+dy),
                (x+width/2, y-1+dy), (x+width*.18, y+2+dy)], colour, INK)
    d.line([(x-width/2, y+1.3*(layers-1)), (x-width/2, y)], INK, .6)


def grains(d, points, colour, radius=.8):
    for x, y in points: d.circle(x, y, radius, colour, INK)


def droplet(d, x, y, scale=1, colour=WATER):
    points = [(x, y-3*scale), (x-1.6*scale, y), (x-1.4*scale, y+1.6*scale),
              (x, y+2.2*scale), (x+1.4*scale, y+1.6*scale), (x+1.6*scale, y)]
    d.poly(points, colour, INK)


def feldspar(d, x, y, colour=FELDSPAR, width=12, height=19):
    d.poly([(x-width/2, y+height/2), (x-width/2, y-height/2),
            (x+width/2, y-height/2-2), (x+width/2, y+height/2-2)], colour, INK)
    for offset in (-3, 0, 3):
        d.line([(x+offset, y-height/2+.8), (x+offset, y+height/2-2)], STEEL, .55)


def pyrite_cube(d, x, y, size=5):
    d.poly([(x-size, y-size*.5), (x, y-size), (x+size, y-size*.5),
            (x+size, y+size*.5), (x, y+size), (x-size, y+size*.5)], PYRITE, INK)
    d.line([(x-size, y-size*.5), (x, y), (x+size, y-size*.5)], INK, .65)
    d.line([(x, y), (x, y+size)], INK, .65)
    for offset in (.25, .6):
        d.line([(x+size*offset, y-size*.22+size*.25*offset),
                (x+size*offset, y+size*.7-size*.5*offset)], INK, .45)


def alteration(kind):
    d = Drawing()
    host(d, GRANITE if kind in {'potassic_alteration', 'greisen', 'deuteric_alteration', 'red_rock_alteration'}
         else BASALT if kind in {'zeolitic_alteration', 'serpentinisation'} else '#A9AFA4')
    if kind == 'saussuritised':
        feldspar(d, 23, 25, ALBITE, 19, 25)
        d.line([(16, 14), (21, 19), (18, 25), (22, 30), (17, 37)], INK, .7)
        grains(d, [(17, 15), (21, 21), (19, 28), (24, 32), (16, 34), (28, 17), (30, 28)], EPIDOTE, 1.45)
        rhomb(d, 30, 34, .6)
        mica_book(d, 12, 30, MICA, 6, 3)
    elif kind == 'serpentinisation':
        for x, y, radius in ((15, 20, 7), (30, 18, 7), (24, 32, 9)):
            d.circle(x, y, radius, SERPENTINE, INK)
            d.arc(x, y, radius-2.5, 195, 330, CHLORITE)
        for points in [[(7, 29), (17, 27), (24, 23), (37, 28)],
                       [(19, 8), (22, 19), (24, 23), (22, 41)]]:
            d.line(points, INK, 3)
            d.line(points, '#A8B990', 1.5)
    elif kind == 'epidote_alteration':
        feldspar(d, 15, 26, ALBITE, 10, 22)
        for x, y, angle, height in ((23, 35, -28, 18), (27, 37, -8, 24), (30, 35, 15, 20), (34, 34, 35, 14)):
            crystal(d, x, y, 4, height, EPIDOTE, angle)
    elif kind == 'silicification':
        d.poly([(5, 31), (15, 25), (18, 14), (24, 8), (29, 9), (25, 25), (40, 32), (36, 38), (21, 31), (9, 38)], QUARTZ, INK)
        for x, y, height, angle in ((15, 34, 10, -25), (22, 31, 17, 0), (28, 33, 15, 25), (32, 35, 9, 40)):
            crystal(d, x, y, 5, height, QUARTZ, angle)
    elif kind == 'carbonate_alteration':
        d.line([(7, 37), (18, 27), (24, 20), (39, 12)], CALCITE, 7)
        for x, y, scale in ((14, 32, .9), (23, 25, 1.2), (33, 17, 1)):
            rhomb(d, x, y, scale)
        rhomb(d, 33, 36, .6)
    elif kind == 'calcsilicate_alteration':
        d.poly([(29, 7), (25, 17), (28, 30), (22, 43), (41, 37), (44, 17)], CALCITE, SOIL)
        for x, y, angle in ((14, 23, -25), (21, 37, 24), (33, 32, 5)):
            crystal(d, x, y, 4, 15, PYROXENE, angle)
        for x, y, radius in ((25, 20, 6), (15, 34, 4)):
            points = [(x+radius*math.cos(i*math.tau/8), y+radius*math.sin(i*math.tau/8)) for i in range(8)]
            d.poly(points, GARNET, INK)
            d.poly([(x, y-radius*.55), (x+radius*.55, y), (x, y+radius*.55), (x-radius*.55, y)], None, INK)
    elif kind == 'greisen':
        for x, y, angle in ((13, 30, -25), (22, 32, 0), (32, 29, 28)):
            crystal(d, x, y, 6, 18, QUARTZ, angle)
        mica_book(d, 15, 36, MICA, 13, 4)
        mica_book(d, 33, 34, MICA, 11, 4)
        crystal(d, 25, 39, 6, 10, '#C3D6CF', 15)
    elif kind == 'albitic_alteration':
        feldspar(d, 15, 27, FELDSPAR, 10, 19)
        feldspar(d, 32, 25, ALBITE, 11, 26)
        d.arrow(20, 12, 31, 10, INK)
        d.line([(28, 13), (32, 20), (29, 27), (34, 32)], INK, .6)
    elif kind == 'advanced_argillic_alteration':
        d.poly([(11, 14), (20, 10), (37, 14), (38, 33), (27, 38), (12, 34)], QUARTZ, INK)
        for x, y, radius in ((17, 19, 2.6), (27, 16, 2.4), (33, 25, 3), (23, 30, 2.8), (15, 28, 2)):
            d.circle(x, y, radius, BASALT, INK)
        mica_book(d, 18, 36, KAOLIN, 12, 3)
        rhomb(d, 34, 37, .65, ALUNITE)
        droplet(d, 8, 11, .65)
    elif kind == 'not_altered':
        for x, y, colour, width in ((15, 23, FELDSPAR, 10), (31, 21, ALBITE, 9)):
            feldspar(d, x, y, colour, width, 18)
        crystal(d, 24, 38, 8, 14, QUARTZ, 20)
        d.line([(7, 37), (10, 40), (16, 34)], INK, 1.4)
    elif kind == 'chloritic_alteration':
        for x, y, width in ((14, 19, 12), (28, 28, 17), (16, 35, 12)):
            mica_book(d, x, y, CHLORITE, width, 4)
        d.line([(30, 11), (35, 16), (32, 20), (39, 27)], CHLORITE, 1.8)
    elif kind == 'zeolitic_alteration':
        d.ellipse(24, 25, 16, 14, None, INK)
        for angle in (-62, -37, -12, 12, 37, 62):
            crystal(d, 24, 34, 3.4, 19, '#E2D4C5', angle)
        d.circle(13, 13, 2.4, None, STEEL)
        d.circle(37, 37, 2, None, STEEL)
    elif kind == 'propylitic_alteration':
        mica_book(d, 14, 28, CHLORITE, 12, 4)
        crystal(d, 27, 29, 5, 20, EPIDOTE, 10)
        rhomb(d, 33, 35, .95)
        feldspar(d, 16, 14, ALBITE, 8, 7)
    elif kind == 'potassic_alteration':
        feldspar(d, 20, 22, FELDSPAR, 16, 25)
        d.line([(15, 12), (19, 16), (16, 21), (22, 25), (19, 31)], ALBITE, 1.3)
        mica_book(d, 31, 34, BIOTITE, 15, 4)
        crystal(d, 10, 37, 5, 10, QUARTZ)
    elif kind == 'alteration_not_specified':
        d.ellipse(24, 25, 15, 13, '#B9B6A4', INK)
        d.ellipse(24, 25, 10, 9, '#B6C1B0', INK)
        d.line([(17, 19), (23, 23), (20, 29), (28, 34)], INK, .7)
        for x, y in ((13, 20), (32, 15), (34, 29), (19, 36)):
            crystal(d, x, y+2, 3.5, 5.5, '#D6CFBA', 25)
        d.arrow(3, 10, 11, 15, WATER)
    elif kind == 'kaolinitic_alteration':
        for x, y, radius in ((19, 22, 9), (30, 30, 8), (14, 35, 6)):
            for i in (2, 1, 0):
                d.poly([(x+radius*math.cos(j*math.tau/6), y+i*1.7+radius*.55*math.sin(j*math.tau/6))
                        for j in range(6)], KAOLIN, INK)
    elif kind == 'sericitic_alteration':
        feldspar(d, 24, 25, ALBITE, 24, 26)
        d.line([(15, 13), (22, 23), (18, 32), (29, 38)], INK, .7)
        for x, y in ((17, 20), (29, 16), (25, 28), (31, 33), (17, 34)):
            mica_book(d, x, y, MICA, 8, 3)
        pyrite_cube(d, 35, 35, 2.3)
    elif kind == 'argillic_alteration':
        for y in (14, 19, 25, 31, 37):
            points = [(9+30*i/40, y+1.4*math.sin(i/40*math.tau*1.5)) for i in range(41)]
            d.line(points, INK, 2.5)
            d.line(points, CLAY, 1.2)
        droplet(d, 34, 11, .85)
        droplet(d, 14, 25, .65)
    elif kind == 'alunitic_alteration':
        # Alunite is rhombohedral/tabular, not a quartz-like long prism.
        for x, y, scale in ((14, 20, 1), (25, 17, 1.2), (32, 27, 1.1), (18, 32, 1.3)):
            rhomb(d, x, y+2, scale, ALUNITE)
            rhomb(d, x, y-.3, scale, '#ECDCC8')
        rhomb(d, 29, 37, .7, ALUNITE)
        droplet(d, 37, 12, .7)
        grains(d, [(9, 17), (30, 35), (34, 38)], '#C99D8C', .8)
    elif kind == 'hematitic_alteration':
        d.ellipse(24, 25, 15, 13, HEMATITE, INK)
        d.ellipse(24, 25, 8.5, 7, BASALT, INK)
        for angle in range(0, 360, 45):
            a = math.radians(angle)
            x, y = 24+12*math.cos(a), 25+10*math.sin(a)
            mica_book(d, x, y, HEMATITE, 6.5, 3)
    elif kind == 'pyritic_alteration':
        d.line([(8, 38), (15, 29), (26, 24), (39, 10)], PYRITE, 2.6)
        for x, y, size in ((15, 29, 6), (30, 17, 6), (31, 35, 4)):
            pyrite_cube(d, x, y, size)
    elif kind == 'deuteric_alteration':
        feldspar(d, 15, 23, FELDSPAR, 9, 15)
        crystal(d, 33, 31, 6, 17, QUARTZ, 22)
        mica_book(d, 23, 36, CHLORITE, 10, 3)
        d.line([(14, 12), (22, 17), (25, 22), (20, 27), (28, 29)], WATER, 1.2)
        d.arrow(35, 35, 28, 34, WATER)
        d.arc(24, 25, 18, 190, 285, HEAT)
        grains(d, [(30, 10), (36, 14), (10, 34)], QUARTZ, 1)
    elif kind == 'uralitisation':
        crystal(d, 23, 37, 15, 24, PYROXENE, 0)
        for offset in (-7, -4, -1, 2, 5, 8):
            d.line([(23+offset*.5, 34), (23+offset, 17-abs(offset)*.5)], '#8AA18B', 1.3)
            d.line([(23+offset*.5, 34), (23+offset, 17-abs(offset)*.5)], INK, .45)
        d.arrow(6, 10, 16, 15, WATER)
    elif kind == 'red_rock_alteration':
        feldspar(d, 17, 23, FELDSPAR, 12, 22)
        feldspar(d, 32, 29, '#BC8171', 10, 19)
        for index in range(17):
            x = 10+(index*7)%28
            y = 13+(index*11)%25
            d.circle(x, y, .7+(index%2)*.2, HEMATITE, HEMATITE, True)
        d.line([(7, 34), (16, 30), (24, 32), (38, 17)], HEMATITE, 1.2)
    else:
        raise ValueError('No alteration drawing for '+kind)
    return d


def process(kind):
    d = Drawing()
    if kind == 'geochemical_vectoring':
        for rx, ry in ((19, 15), (14, 11), (9, 7)):
            shape = affinity.rotate(affinity.scale(Point(25, 25).buffer(1, quad_segs=32), rx, ry,
                                                   origin=(25, 25)), -20, origin=(25, 25))
            d.shape(shape, None, SOIL if rx == 19 else STEEL, .8)
        for x, y in ((8, 9), (39, 11), (9, 39), (39, 38)):
            d.circle(x, y, 1.2, CALCITE, INK)
            d.arrow(x+(25-x)*.2, y+(25-y)*.2, x+(25-x)*.72, y+(25-y)*.72, INK)
        pyrite_cube(d, 25, 25, 3)
    elif kind == 'hydrothermal_alteration':
        host(d)
        d.poly([(15, 8), (21, 17), (18, 24), (27, 32), (25, 43),
                (35, 42), (34, 31), (27, 22), (30, 14), (23, 7)], CHLORITE, INK)
        d.line([(20, 6), (25, 17), (22, 24), (30, 32), (30, 44)], WATER, 2)
        d.arrow(9, 21, 17, 21, WATER)
        grains(d, [(17, 14), (31, 18), (28, 36), (21, 27)], EPIDOTE, 1)
    elif kind == 'magmatic_intrusion':
        for y, colour in ((7, CALCITE), (16, SAND), (26, '#9AA6A1'), (36, CLAY)):
            d.poly([(3, y), (17, y-1), (25, y-3), (34, y), (45, y),
                    (45, y+8), (3, y+8)], colour, INK)
        d.poly([(13, 44), (11, 35), (15, 27), (21, 23), (22, 13),
                (26, 6), (29, 10), (27, 23), (33, 26), (37, 35), (35, 44)], GRANITE, INK)
        d.line([(23, 38), (23, 29), (26, 21), (25, 12)], HEAT, 1.7)
        grains(d, [(18, 32), (28, 29), (31, 37), (20, 41)], QUARTZ, 1)
        for x, y in ((10, 31), (34, 24), (38, 38)):
            d.arc(x, y, 2.1, 230, 360, HEAT)
    elif kind == 'dehydration':
        host(d, '#B7A793')
        mica_book(d, 15, 32, MICA, 16, 4)
        crystal(d, 32, 37, 7, 16, PYROXENE, 12)
        d.arrow(19, 21, 19, 8, WATER)
        d.arrow(32, 17, 32, 5, WATER)
        droplet(d, 19, 5, .8)
        droplet(d, 32, 2, .6)
        for x in (9, 23, 37):
            d.line([(x, 46), (x+1, 42), (x, 39)], HEAT, 1)
    elif kind in {'reducing_environment', 'oxidizing_environment'}:
        reducing = kind == 'reducing_environment'
        d.rect(3, 5, 42, 35, GLASS, 1)
        d.poly([(3, 22), (14, 20), (25, 22), (36, 20), (45, 21), (45, 41), (3, 41)],
               '#676D5D' if reducing else '#B78166', INK)
        for x in (10, 24, 38):
            d.arrow(x, 10, x, 24, WATER)
        if reducing:
            # Organic debris and sulfide grains in an oxygen-poor sediment.
            d.poly([(9, 31), (13, 26), (17, 28), (15, 33)], BIOTITE, INK)
            d.line([(10, 31), (16, 28)], INK, .55)
            pyrite_cube(d, 30, 32, 4)
            for x, y in ((9, 16), (18, 18), (34, 15)):
                d.circle(x, y, .85, INK, INK, True)
        else:
            # Paired oxygen atoms enter an iron-rich weathering front.
            for x, y in ((15, 12), (32, 8)):
                d.circle(x, y, 1.8, '#CF8174', INK)
                d.circle(x+2.8, y, 1.8, '#CF8174', INK)
            d.ellipse(24, 32, 12, 7, HEMATITE, INK)
            d.ellipse(24, 32, 6, 3.8, BASALT, INK)
            grains(d, [(9, 27), (37, 27), (11, 36), (37, 36)], HEMATITE, 1.1)
    else:
        raise ValueError(kind)
    return d


PROCESS_ROWS = [
    ('geochemical_vectoring', 'Geochemical Vectoring', 'Sample stations and nested anomaly contours converge on a mineralized target.'),
    ('hydrothermal_alteration', 'Hydrothermal Alteration', 'Fluid flow along a fracture produces a reaction halo and replacement minerals.'),
    ('magmatic_intrusion', 'Magmatic Intrusion', 'A crystallizing pluton and feeder dike cut layered country rock and produce a contact aureole.'),
    ('dehydration', 'Dehydration', 'Heating drives water release from a hydrous mineral assemblage as new anhydrous crystals form.'),
    ('reducing_environment', 'Reducing Environment', 'Organic-rich oxygen-poor sediment with sulfide mineral growth and porewater transport.'),
    ('oxidizing_environment', 'Oxidizing Environment', 'Dissolved oxygen enters a weathering front and forms iron oxide rims around primary grains.'),
]
ALTERATION_ROWS = json.loads(Path(__file__).with_name('alteration-types.json').read_text(encoding='utf-8-sig'))
GEOCHEM_ROWS = [(identifier, name, description, partial(process, identifier))
                for identifier, name, description in PROCESS_ROWS]
GEOCHEM_ROWS += [(row['id'], row['name'].capitalize(), row['description'], partial(alteration, row['id']))
                 for row in ALTERATION_ROWS]
GEOCHEM_ICONS = [dict(id='gc_'+identifier, codepoint=0xE126+index, name=name,
                      domain='Geochemical', category='Processes', description=description,
                      keywords=identifier.split('_')+['geochemistry', 'alteration', 'mineral', 'Opus'],
                      builder=lambda builder=builder: builder().geometry())
                 for index, (identifier, name, description, builder) in enumerate(GEOCHEM_ROWS)]
GEOCHEM_IDS = {icon['id'] for icon in GEOCHEM_ICONS}
GEOCHEM_BUILDERS = {'gc_'+row[0]: row[3] for row in GEOCHEM_ROWS}
PROPERTY_ALIASES = {row['id']: 'gc_'+row['id'] for row in ALTERATION_ROWS}
PROPERTY_ALIASES.update({identifier: 'gc_'+identifier for identifier, _, _ in PROCESS_ROWS})
PROPERTY_ALIASES.update({'vectoring': 'gc_geochemical_vectoring', 'alteration': 'gc_hydrothermal_alteration',
                         'intrusion': 'gc_magmatic_intrusion', 'dehydrating': 'gc_dehydration',
                         'reducing': 'gc_reducing_environment', 'oxidizing': 'gc_oxidizing_environment',
                         'oxidising': 'gc_oxidizing_environment'})


@lru_cache(maxsize=40)
def flat_artwork(identifier):
    from detailed_flat import FlatLayer
    drawing = GEOCHEM_BUILDERS[identifier]()
    geometry = drawing.geometry()
    cleaned = geometry.buffer(.65, quad_segs=4, join_style=1).buffer(-.65, quad_segs=4, join_style=1)
    x0, y0, x1, y1 = cleaned.bounds
    factor = 880/max(x1-x0, y1-y0)

    def convert(shape):
        shape = native(shape)
        shape = affinity.translate(shape, xoff=-(x0+x1)/2, yoff=-(y0+y1)/2)
        shape = affinity.scale(shape, factor, factor, origin=(0, 0))
        shape = affinity.translate(shape, xoff=500, yoff=500)
        shape = affinity.scale(shape, 24/1000, -24/1000, origin=(0, 0))
        return affinity.translate(shape, yoff=24)

    layers = []
    for part in drawing.parts:
        if part.face is not None and part.fill is not None:
            layers.append(FlatLayer(convert(part.face), part.fill))
        layers.append(FlatLayer(convert(part.ink), part.colour))
    return layers
