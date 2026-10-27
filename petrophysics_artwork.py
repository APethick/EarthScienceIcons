"""Detailed rock-property specimens and petrophysical logging instruments.

One layered composition supplies the natural-material SVG and technical font.
Hardware and samples carry the meaning; symbols supplement the illustration.
"""
from shapely.geometry import LineString

from em_artwork import Equipment, controller, place, response
from icons_geophysics_expanded import (
    INK, STEEL, ALU, GLASS, SOIL, SAND, ROCK, WATER, BLUE, RED,
    YELLOW, WHITE, symbol, PETROPHYSICAL_LOGGING_KINDS,
)

LOGGING_KINDS = PETROPHYSICAL_LOGGING_KINDS


def grains(d, positions, colour=SOIL):
    for x, y, scale in positions:
        d.poly([(x-scale, y), (x-.3*scale, y-.8*scale), (x+.8*scale, y-.4*scale), (x+scale, y+.6*scale), (x, y+scale)], None, colour)


def core(d, porous=False):
    d.rect(9, 20, 28, 17, SAND, 0)
    d.ellipse(9, 28.5, 3.7, 8.5, SAND)
    d.ellipse(37, 28.5, 3.7, 8.5, '#E8D9BA')
    d.line([(10, 22), (31, 22)], SOIL, .65)
    grains(d, [(14, 25, 1.2), (20, 32, 1.4), (27, 25, 1.3), (31, 33, .9), (36, 26, .9), (37, 32, 1.1)])
    if porous:
        for x, y, rx, ry in ((17, 28, 1.8, 1.2), (25, 30, 2.1, 1.4), (32, 27, 1.3, 1.7)):
            d.ellipse(x, y, rx, ry, WATER)


def collars(d):
    for x in (6, 38):
        d.rect(x, 18.8, 3, 19.4, ALU, .5)
        d.line([(x+.6, 21), (x+2.3, 21)], STEEL, .6)
        d.line([(x+.6, 36), (x+2.3, 36)], STEEL, .6)


def electrical(kind):
    d = Equipment()
    core(d, porous=kind == 'property_conductivity')
    collars(d)
    place(d, controller(), 4, 2, 1.1)
    d.line([(5, 13), (2, 16), (2, 29), (6, 29)], BLUE, .85)
    d.line([(16, 11), (44, 12), (44, 29), (41, 29)], BLUE, .85)
    for x in (17, 29):
        d.rect(x, 18, 1.7, 4.4, STEEL, .3)
        d.line([(x+.8, 18), (x+.8, 15), (24, 15)], BLUE, .65)
    if kind == 'property_conductivity':
        symbol(d, 'sigma', 35, 2, 7)
        d.line([(10, 29), (15, 27), (21, 30), (27, 27), (35, 29)], WATER, 2.1)
        d.arrow(16, 42, 33, 42, BLUE)
    else:
        symbol(d, 'rho', 35, 1, 7)
        d.line([(11, 29), (15, 29), (18, 25), (22, 32), (26, 25), (30, 32), (33, 29), (36, 29)], BLUE, .9)
        d.line([(17, 42), (31, 42)], INK, .7)
        for x in (17, 24, 31):
            d.line([(x, 40.5), (x, 43.5)], INK, .7)
    return d


def density():
    d = Equipment()
    # A rock core on a load-cell balance communicates mass and physical volume.
    d.rect(4, 33, 40, 11, ALU, 1.2)
    d.rect(7, 36, 15, 5, GLASS, .5)
    d.line([(9, 39), (11, 37.5), (14, 39.5), (17, 37.5), (20, 39)], INK, .65)
    d.circle(29, 38.5, 1, STEEL).circle(37, 38.5, 1, STEEL)
    d.rect(7, 44, 5, 1.5, STEEL, .3).rect(36, 44, 5, 1.5, STEEL, .3)
    d.rect(9, 29, 30, 3.5, STEEL, .6)
    d.rect(21, 26, 6, 3, ALU, .3)
    d.rect(14, 11, 20, 14, ROCK, .3)
    d.ellipse(24, 25, 10, 3.4, ROCK)
    d.ellipse(24, 11, 10, 3.4, '#B6B5A6')
    grains(d, [(17, 16, 1.1), (26, 20, 1.3), (30, 15, .9)], '#576567')
    d.line([(5, 9), (5, 27)], INK, .7)
    d.line([(3.5, 9), (7, 9)], INK, .7).line([(3.5, 27), (7, 27)], INK, .7)
    for y in (14, 19, 23):
        d.line([(4, y), (5, y)], INK, .6)
    symbol(d, 'rho', 39, 2, 6)
    return d


def magnetism(kind):
    d = Equipment()
    core(d)
    if kind == 'property_magnetic_susceptibility':
        place(d, controller(), 3, 1, .95)
        d.line([(5, 10), (2, 15), (10, 23)], RED, .8)
        for x in (14, 19, 24, 29, 34):
            d.ellipse(x, 28.5, 2.3, 10, None, RED)
        d.line([(34, 18.5), (43, 15), (43, 8), (14, 8)], RED, .8)
        d.arrow(7, 43, 39, 43, RED)
        symbol(d, 'chi', 36, 1, 6)
    else:
        d.word('M', 6, 3, 1.3)
        # Compass and orientation axes indicate a retained magnetization vector.
        d.circle(37, 7, 5.5, WHITE)
        d.poly([(37, 2.8), (38.4, 7.8), (35.5, 7.8)], RED, RED)
        d.poly([(37, 11), (38.4, 7.8), (35.5, 7.8)], ALU)
        for x, y in ((15, 27), (24, 31), (31, 25)):
            d.arrow(x-1, y+3, x+3, y-2, RED)
        d.line([(7, 43), (23, 43), (23, 39)], STEEL, .7)
        d.arrow(7, 43, 7, 36, STEEL)
        d.arrow(7, 43, 16, 39, RED)
    return d


def chargeability():
    d = Equipment()
    core(d)
    collars(d)
    d.line([(6, 28), (2, 28), (2, 6), (13, 6)], BLUE, .85)
    d.line([(40, 28), (45, 28), (45, 15)], BLUE, .85)
    response(d, 26, 2, 17, 10)
    d.line([(12, 12), (12, 3), (20, 3), (20, 12), (24, 12)], BLUE, 1)
    # Polarized grain interfaces and delayed response distinguish IP from DC.
    for x in (16, 25, 33):
        d.ellipse(x, 28.5, 2.8, 4.4, '#C4AE8A')
        d.circle(x-3.4, 26.5, .8, BLUE, BLUE, True)
        d.circle(x+3.4, 30, .8, RED, RED, True)
    d.circle(37, 42, 4.1, WHITE)
    d.line([(37, 39.5), (37, 42), (39, 43)], INK, .7)
    d.line([(7, 43), (26, 43)], STEEL, .7)
    return d


def velocity(kind):
    d = Equipment()
    core(d)
    d.rect(4, 19, 4, 19, ALU, .5, BLUE)
    d.rect(40, 19, 4, 19, YELLOW, .5, '#111111')
    place(d, controller(), 3, 2, .9)
    d.line([(4, 12), (2, 15), (2, 28), (4, 28)], BLUE, .75)
    d.line([(13, 10), (45, 11), (45, 28), (44, 28)], STEEL, .75)
    d.word('VP' if kind == 'property_vp' else 'VS', 27, 1, 1.25)
    if kind == 'property_vp':
        for x in (12, 14, 16, 22, 29, 31, 33, 35):
            d.line([(x, 25), (x, 33)], BLUE, .85)
        d.arrow(17, 42, 32, 42, BLUE)
    else:
        d.wave(11, 37, 28.5, 4, 2, BLUE)
        d.arrow(23, 39, 23, 46, BLUE)
    d.line([(6, 45), (42, 45)], STEEL, .65)
    d.line([(6, 43.5), (6, 46)], STEEL, .65).line([(42, 43.5), (42, 46)], STEEL, .65)
    return d


def porous_block(d):
    d.poly([(6, 20), (13, 15), (44, 15), (38, 20)], '#E8DBBF')
    d.poly([(38, 20), (44, 15), (44, 36), (38, 41)], SOIL)
    d.rect(6, 20, 32, 21, SAND, 0)
    grains(d, [(10, 24, 1.1), (24, 23, 1), (33, 38, .9), (13, 37, .8), (23, 34, .8)])


def pores(kind):
    d = Equipment()
    porous_block(d)
    if kind == 'property_porosity':
        symbol(d, 'phi', 34, 1, 7)
        place(d, controller(), 4, 2, .8)
        for x, y, rx, ry in ((14, 28, 3, 2), (30, 27, 3.5, 2.8), (20, 36, 2.7, 2), (35, 34, 1.4, 2), (9, 34, 1.3, 1.2)):
            d.ellipse(x, y, rx, ry, WHITE)
        d.ellipse(29.7, 28, 2.6, .8, WATER, WATER)
        d.line([(7, 45), (37, 45)], INK, .65)
        for x in (7, 17, 27, 37):
            d.line([(x, 43.5), (x, 46)], INK, .65)
    else:
        d.word('K', 35, 2, 1.25)
        # Connected pore throats convey permeability, unlike isolated porosity.
        paths = [[(3, 31), (12, 28), (23, 30), (32, 26), (43, 29)], [(12, 28), (17, 36), (28, 36), (32, 26)]]
        for points in paths:
            d.shape(LineString(points).buffer(1.3, quad_segs=8, join_style=1), WATER)
        for x, y in ((12, 28), (23, 30), (32, 26), (17, 36), (28, 36)):
            d.ellipse(x, y, 2.5, 2, WATER)
        d.arrow(2, 44, 19, 44, WATER)
        d.arrow(27, 44, 44, 44, WATER)
        for x in (7, 23):
            d.circle(x, 7, 4, WHITE)
            d.line([(x, 7), (x+1.7, 5.3)], INK, .65)
            d.line([(x, 11), (x, 17)], STEEL, .8)
    return d


def dielectric():
    d = Equipment()
    d.rect(13, 19, 22, 22, SAND, .4)
    grains(d, [(18, 23, .9), (29, 36, 1), (18, 37, .8)])
    d.rect(8, 17, 4, 26, ALU, .4)
    d.rect(36, 17, 4, 26, ALU, .4)
    place(d, controller(), 3, 1, 1)
    d.line([(4, 12), (2, 15), (2, 30), (8, 30)], BLUE, .85)
    d.line([(15, 11), (45, 12), (45, 30), (40, 30)], BLUE, .85)
    symbol(d, 'epsilon', 35, 1, 7)
    for x, y in ((19, 27), (29, 27), (24, 35)):
        d.line([(x-1.5, y), (x+1.5, y)], INK, .7)
        d.circle(x-2, y, 1, BLUE, BLUE, True)
        d.circle(x+2, y, 1, RED, RED, True)
    d.arrow(12, 46, 36, 46, BLUE)
    return d


def thermal():
    d = Equipment()
    d.rect(11, 17, 26, 22, ROCK, .5)
    grains(d, [(16, 23, 1.1), (30, 34, 1), (31, 22, 1)], '#5C686B')
    d.rect(7, 14, 34, 3, ALU, .3, BLUE)
    d.rect(7, 39, 34, 3, ALU, .3, RED)
    for x in (17, 24, 31):
        d.arrow(x, 36, x, 22, RED)
    place(d, controller(), 4, 1, .9)
    d.line([(14, 6), (43, 6), (43, 24), (37, 24)], STEEL, .75)
    d.line([(4, 11), (2, 15), (2, 32), (11, 32)], STEEL, .75)
    d.circle(37, 24, 1.1, ALU).circle(11, 32, 1.1, ALU)
    d.word('K', 35, 1, 1.1)
    d.line([(11, 46), (37, 46)], INK, .7)
    return d


def logging(kind):
    d = Equipment()
    # Layered formation, fluid-filled open hole and a cable-mounted sonde.
    d.rect(3, 13, 20, 32, SAND, 0)
    d.poly([(3, 23), (23, 20), (23, 28), (3, 31)], '#AC9D83', SOIL)
    d.poly([(3, 38), (23, 35), (23, 40), (3, 43)], '#C2B08C', SOIL)
    d.rect(8, 13, 9, 32, GLASS, 0)
    d.line([(12.5, 5), (12.5, 19)], STEEL, .85)
    d.rect(9.6, 19, 5.8, 21, ALU, 2)
    d.line([(10, 21), (15, 21)], STEEL, .6).line([(10, 38), (15, 38)], STEEL, .6)
    place(d, controller(), 3, 1, .7)
    d.circle(12.5, 8, 2, ALU)
    d.line([(10.5, 8), (9.8, 7)], STEEL, .6)
    d.rect(27, 6, 19, 39, WHITE, .6)
    d.line([(27, 13), (46, 13)], STEEL, .6)
    for y in (19, 27, 35, 43):
        d.line([(27, y), (46, y)], '#BDC5C6', .5)
        d.line([(1, y), (3, y)], INK, .6)
    d.line([(31, 13), (31, 44)], '#BDC5C6', .5)
    d.line([(41, 13), (41, 44)], '#BDC5C6', .5)
    curve = [(33, 15), (34, 20), (39, 23), (35, 27), (42, 32), (36, 37), (38, 42)]
    colour = INK
    if kind in {'borehole_induction_log', 'borehole_magnetic_susceptibility', 'borehole_nmr'}:
        colour = BLUE if kind == 'borehole_induction_log' else RED
        for y in (23, 28, 34):
            d.ellipse(12.5, y, 3.6, 1.3, None, colour)
        d.arc(13, 28, 9, -55, 55, colour)
        if kind == 'borehole_nmr':
            d.wave(32, 43, 24, 2.5, 3, RED)
            curve = [(32, 40), (34, 38), (36, 35), (38, 27), (42, 16)]
            d.word('M', 34, 7, .7)
        else:
            symbol(d, 'sigma' if kind == 'borehole_induction_log' else 'chi', 36, 6.5, 4)
    elif kind in {'borehole_resistivity_log', 'borehole_fluid_conductivity', 'borehole_ip_log'}:
        colour = BLUE
        for y in (23, 28, 34):
            d.rect(9, y, 7, 1.6, STEEL, .3)
        symbol(d, 'rho' if kind == 'borehole_resistivity_log' else 'sigma', 36, 6, 4)
        if kind == 'borehole_fluid_conductivity':
            d.ellipse(12.5, 31.5, 1.2, 1, WATER)
            curve = [(33, 15), (33, 24), (41, 25), (41, 35), (34, 36), (34, 42)]
        elif kind == 'borehole_ip_log':
            response(d, 32, 17, 11, 23)
            curve = []
        else:
            d.line([(15, 24), (21, 24), (21, 32), (15, 32)], BLUE, .7)
    elif kind in {'borehole_density_log', 'borehole_neutron_porosity'}:
        d.circle(12.5, 34, 1.3, STEEL)
        d.receiver(12.5, 23, 1.25).receiver(12.5, 28, 1.25)
        d.poly([(15.5, 21), (17, 23), (17, 36), (15.5, 38)], ALU)
        d.line([(15, 34), (21, 30), (15, 23)], INK, .7)
        if kind == 'borehole_density_log':
            symbol(d, 'rho', 36, 6, 4)
        else:
            symbol(d, 'phi', 36, 6, 4)
            for x, y in ((20, 21), (21, 34), (5.5, 34)):
                d.circle(x, y, .8, WATER, WATER, True)
    elif kind == 'borehole_sonic_log':
        d.circle(12.5, 35, 1.2, BLUE, BLUE)
        d.receiver(12.5, 23, 1.25).receiver(12.5, 28, 1.25)
        d.word('VP', 32, 7, .7)
        for y in (20, 29, 38):
            d.wave(32, 44, y, 1.5, 2.3, BLUE)
        d.arc(12.5, 33, 8, -50, 40, BLUE)
        curve = []
    elif kind == 'borehole_temperature':
        d.circle(12.5, 33, 1.5, RED, RED)
        d.line([(12.5, 24), (12.5, 33)], RED, 1.3)
        d.word('T', 35, 7, .75)
        curve = [(33, 15), (34, 22), (36, 29), (39, 35), (43, 42)]
        colour = RED
    else:
        raise ValueError(f'Unknown petrophysical logging tool: {kind}')
    if curve:
        d.line(curve, colour, 1.05)
    return d


def scene(kind):
    if kind in LOGGING_KINDS:
        return logging(kind)
    if kind in {'property_conductivity', 'property_resistivity'}:
        return electrical(kind)
    if kind == 'property_density':
        return density()
    if kind in {'property_magnetic_susceptibility', 'property_remanent_magnetization'}:
        return magnetism(kind)
    if kind == 'property_chargeability':
        return chargeability()
    if kind in {'property_vp', 'property_vs'}:
        return velocity(kind)
    if kind in {'property_porosity', 'property_permeability'}:
        return pores(kind)
    if kind == 'property_dielectric_permittivity':
        return dielectric()
    if kind == 'property_thermal_conductivity':
        return thermal()
    raise ValueError(f'Unknown petrophysical property: {kind}')
