"""Equipment-led EM illustrations shared by the flat SVGs and detailed font.

Schematic equipment, without manufacturer logos. Portable instruments show
clothed operators and backpack-mounted hardware; aircraft show actual airframe,
suspension and coil-frame components rather than generic diagram symbols.
"""
import math

from shapely import affinity

from icons_geophysics_expanded import (
    Diagram, Part, INK, STEEL, ALU, GLASS, SOIL, SAND, WATER,
    BLUE, RED, YELLOW, WHITE,
)

SHIRT = '#B7A178'
TROUSERS = '#536570'
SKIN = '#C99573'
FRAME = '#65747B'


class Equipment(Diagram):
    def line(self, points, colour=INK, width=.95):
        return super().line(points, colour, width)

    def shape(self, geometry, fill=None, colour=INK, width=.95, solid=False):
        return super().shape(geometry, fill, colour, width, solid)


def place(drawing, component, x=0, y=0, scale=1):
    def convert(geometry):
        if geometry is None:
            return None
        return affinity.translate(affinity.scale(geometry, scale, scale, origin=(0, 0)), x, y)
    for part in component.parts:
        drawing.parts.append(Part(convert(part.ink), part.colour, convert(part.face), part.fill))
    return drawing


def tag(drawing, text, x, y, scale=.65):
    letters = {
        'T': [[(0, 0), (3, 0)], [(1.5, 0), (1.5, 4)]],
        'R': [[(0, 4), (0, 0), (3, 0), (3, 2), (0, 2), (3, 4)]],
        'X': [[(0, 0), (3, 4)], [(3, 0), (0, 4)]],
        'H': [[(0, 0), (0, 4)], [(3, 0), (3, 4)], [(0, 2), (3, 2)]],
        'E': [[(3, 0), (0, 0), (0, 4), (3, 4)], [(0, 2), (2.5, 2)]],
    }
    for index, letter in enumerate(text):
        for points in letters[letter]:
            drawing.line([(x + (index * 4.5 + px) * scale, y + py * scale) for px, py in points], INK, .6)


def terrain(drawing, y=41):
    drawing.line([(2, y), (12, y-.4), (22, y+.2), (33, y-.2), (46, y)], SOIL, 1)
    for x in (5, 20, 30, 43):
        drawing.line([(x, y+2), (x+2.2, y+2)], SOIL, .7)
    drawing.poly([(8, y-.4), (9, y-1.7), (11, y-1.2), (12, y-.4)], SAND, SOIL)


def controller(receiver=False):
    d = Equipment()
    d.line([(2, 1), (2, -1), (8, -1), (8, 1)])
    d.rect(0, 1, 11, 8, ALU, .9)
    d.rect(1.5, 2.5, 5.2, 3.3, GLASS, .25)
    d.line([(2.3, 4.8), (3.3, 3.8), (4.1, 4.5), (5.7, 3.4)], BLUE, .55)
    d.circle(8.8, 3.4, .65, YELLOW if receiver else STEEL)
    d.circle(8.8, 6.7, .65, YELLOW if receiver else STEEL)
    d.line([(1.5, 7.4), (5.7, 7.4)], FRAME, .6)
    d.rect(1, 9, 2, 1, FRAME, .2).rect(8, 9, 2, 1, FRAME, .2)
    return d


def sensor():
    d = Equipment()
    d.rect(-2.3, -3, 4.6, 6, YELLOW, 1, '#111111')
    d.line([(-2.2, -1.3), (2.2, -1.3)], '#111111', .65)
    d.circle(0, .8, .85, FRAME, '#111111')
    d.line([(0, -3), (0, -5)], FRAME, .8)
    d.line([(-3, 4), (3, 4)], FRAME, .7)
    return d


def operator(transmitter=False, receiver=False, tablet=True):
    """Side profile: boots, trouser legs, jacket, face, cap, pack and harness."""
    d = Equipment()
    # The equipment sits behind the operator; the coil is not worn around them.
    d.rect(-5.2, 4.1, 3.5, 8.7, FRAME, .9)
    d.rect(-5.8, 5.3, 1.5, 5.8, ALU, .4)
    if transmitter:
        d.line([(-4, 10), (-8.5, 10), (-8.5, 14)], FRAME)
        d.ellipse(-8.1, 14, 5.3, 2.15, None, BLUE)
        d.ellipse(-8.1, 14.7, 5.3, 2.15, None, BLUE)
        d.line([(-4.8, 12.5), (-4.8, 15.8), (-8, 15.8)], FRAME, .7)
    if receiver:
        place(d, sensor(), -6.1, 10, .95)
        d.line([(-3.8, 6), (-7.8, 4.4), (-7.8, 2.1)], FRAME, .7)
    # Two distinct leg silhouettes, with a walking stance and separate boots.
    d.poly([(-2, 12), (.4, 12.4), (-.7, 17), (-3.1, 21), (-5, 20.2), (-2.7, 16.1)], TROUSERS)
    d.poly([(-.6, 12), (1.8, 12), (2, 16.7), (4.5, 19.6), (3.1, 21), (-.1, 17.8)], TROUSERS)
    d.poly([(-5, 20), (-3.1, 20.5), (-3, 22), (-6.8, 22), (-6.8, 21.2)], FRAME)
    d.poly([(3, 20.1), (4.5, 19.5), (6.1, 20.5), (6.2, 21.5), (3.4, 21.8)], FRAME)
    d.poly([(-2.9, 4), (-.5, 3.2), (1.8, 4.5), (2.7, 8), (1.3, 13.1), (-2.4, 13.1), (-3.2, 9)], SHIRT)
    d.line([(-1.8, 4.4), (-.6, 8.1), (-1, 12)], FRAME, .65)
    d.line([(-2.4, 12), (1.5, 12)], FRAME, .65)
    d.poly([(-.6, 1), (.8, 1), (.8, 4), (-.5, 4.1)], SKIN)
    d.poly([(-1.5, -.4), (-1.6, 1.3), (-.3, 2.6), (1.3, 2), (1.7, .9), (2.5, .8), (1.7, -.9)], SKIN)
    d.poly([(-2.2, -.6), (-1.5, -2), (.5, -2.2), (1.8, -.8), (3, -.4), (3, .2), (-2.2, .2)], SAND)
    d.poly([(.6, 4.7), (2.1, 5.1), (4, 8.2), (3, 9.6), (1.1, 7.7)], SHIRT)
    d.poly([(3, 8.5), (4, 7.7), (5.3, 8.6), (6.4, 8), (7, 9.3), (5.1, 10.3)], SKIN)
    if tablet:
        d.poly([(4.6, 7.4), (8.9, 6.8), (9.4, 9.9), (5.1, 10.4)], FRAME)
        d.poly([(5.4, 7.9), (8.2, 7.5), (8.5, 9.1), (5.7, 9.5)], GLASS, FRAME)
    return d


def helicopter():
    d = Equipment()
    d.poly([(14, 9.5), (5, 7.8), (3, 3.5), (1.6, 3.5), (2.5, 10), (15.8, 13.4)], ALU)
    d.line([(1, 6.3), (6.2, 6.3)], FRAME, .8)
    d.circle(3.7, 6.5, 1.7, None, FRAME)
    d.line([(2.4, 5.1), (5, 7.9)], FRAME, .65)
    d.poly([(14, 9), (17, 6.2), (26, 6.2), (30.5, 8), (35.2, 11.2), (34.7, 13.5), (30.8, 15.2), (19, 15.4), (14, 13)], ALU)
    d.rect(18, 4.9, 8.8, 2.2, FRAME, .7)
    d.line([(22, 5.1), (22, 2.2)], FRAME, 1.3)
    d.line([(9, 2.2), (39, 2.2)], FRAME, 1)
    d.line([(16, 1.1), (34, 1.1)], ALU, .65)
    d.poly([(27, 7.5), (30.1, 9), (33.4, 11.2), (30.7, 11.7), (27, 11.4)], GLASS)
    d.poly([(20, 7.6), (25.4, 7.6), (25.4, 11.6), (20, 11.6)], GLASS)
    d.line([(18.5, 7.5), (18.5, 14.2), (26.4, 14.2), (26.4, 7.3)], FRAME, .65)
    d.line([(23.5, 12.8), (25, 12.8)], FRAME, .65)
    d.line([(19, 15), (17.4, 18), (33.5, 18), (35, 16.7)], FRAME)
    d.line([(28.4, 15), (29.3, 18)], FRAME)
    d.line([(18, 18), (16, 18)], FRAME, 1.2)
    return d


def aircraft():
    d = Equipment()
    # Three-quarter plan view, with fuselage, wings, glazing and twin engines.
    d.poly([(23, 2), (25, 4), (26, 12), (43, 18), (43, 21), (26, 18), (25, 27), (32, 30), (32, 32), (24, 30), (16, 32), (16, 30), (22, 27), (21, 18), (4, 21), (4, 18), (21, 12), (22, 4)], ALU)
    d.poly([(22.1, 6), (24.4, 6), (25, 9), (21.8, 9)], GLASS)
    d.line([(23.5, 11), (23.5, 26)], FRAME, .65)
    for x in (13, 33):
        d.rect(x-1, 14.7, 2.5, 6, FRAME, 1)
        d.line([(x-3, 15.3), (x+3.5, 15.3)], FRAME, .8)
    d.line([(8, 19.5), (18, 17.3)], FRAME, .6)
    d.line([(29, 17.3), (39, 19.5)], FRAME, .6)
    return d


def waveform(drawing, x, y, width=12, height=4):
    drawing.line([(x, y+height), (x+width*.2, y+height), (x+width*.2, y), (x+width*.65, y), (x+width*.65, y+height), (x+width, y+height)], BLUE, 1)


def response(drawing, x, y, width=13, height=9, gates=True):
    drawing.line([(x, y-1), (x, y+height), (x+width, y+height)], FRAME, .7)
    drawing.line([(x+1+(width-1)*i/60, y+height*(1-math.exp(-i/11))) for i in range(61)], RED, 1)
    if gates:
        for fraction in (.25, .5, .8):
            at = x+width*fraction
            drawing.line([(at, y+height-1), (at, y+height+1)], FRAME, .6)


def airborne(kind):
    d = Equipment()
    if kind in {'fixed_wing_aem', 'airborne_magnetics', 'airborne_radiometrics'}:
        place(d, aircraft(), 3, -1, .85)
        if kind == 'airborne_radiometrics':
            d.poly([(23, 28), (8, 44), (39, 44)], SAND, SOIL)
            for x, text in ((11, 'K'), (21, 'U'), (31, 'TH')):
                d.word(text, x, 37, .75)
            d.rect(20, 24, 5, 3.5, ALU, .5)
        else:
            d.line([(23, 25), (28, 31), (35, 33), (36, 37)], FRAME, .7)
            if kind == 'fixed_wing_aem':
                d.poly([(8, 37), (35, 37), (39, 39), (35, 41), (8, 41), (5, 39)], ALU)
                for x in (12, 22, 32):
                    d.ellipse(x, 39, 1.6, 3, None, BLUE)
                d.line([(18, 37), (18, 34.5), (23, 37)], FRAME, .8)
                d.line([(9, 43.2), (33, 43.2)], SOIL, .65)
            else:
                d.poly([(22, 37), (36, 37), (40, 39), (36, 41), (22, 41), (20, 39)], ALU)
                d.line([(29, 37), (29, 41)], FRAME, .7)
                d.wave(4, 44, 45, 1.3, 1.2, RED)
        return d
    place(d, helicopter(), 2, 0, 1)
    # Suspension rig includes a central tow point and separated bridle legs.
    d.line([(26, 18), (25, 24)], FRAME, .8)
    d.circle(25, 24, .7, ALU)
    if kind == 'vtem':
        d.line([(25, 24), (8, 35)], FRAME, .75)
        d.line([(25, 24), (42, 35)], FRAME, .75)
        d.line([(25, 24), (25, 40)], FRAME, .75)
        d.ellipse(25, 36, 18, 6.6, None, BLUE)
        d.ellipse(25, 36, 16.4, 5.1, None, BLUE)
        for angle in (0, 60, 120, 180, 240, 300):
            radians = math.radians(angle)
            d.line([(25, 36), (25+17.2*math.cos(radians), 36+5.8*math.sin(radians))], FRAME, .65)
        place(d, sensor(), 25, 36, .6)
        d.line([(17, 44.5), (34, 44.5)], SOIL, .65)
    elif kind == 'skytem':
        frame = [(6, 33), (13, 29), (35, 29), (43, 34), (39, 40), (15, 42), (6, 38)]
        for end in ((6, 33), (35, 29), (39, 40)):
            d.line([(25, 24), end], FRAME, .75)
        d.poly(frame, None, BLUE)
        d.poly([(8, 34), (14, 31), (34, 31), (40, 34.5), (37.5, 38), (15, 40), (8, 37)], None, FRAME)
        d.line([(14, 30), (16, 40)], FRAME, .7)
        d.line([(34, 30), (36, 39)], FRAME, .7)
        d.rect(18, 29, 6, 2.6, ALU, .4)
        d.line([(39, 38), (44, 42)], FRAME, .75)
        place(d, sensor(), 44, 42, .55)
        waveform(d, 3, 45, 8, 2)
        waveform(d, 15, 44, 11, 3)
    else:
        d.line([(25, 24), (12, 34)], FRAME, .75)
        d.line([(25, 24), (39, 34)], FRAME, .75)
        d.poly([(9, 33), (38, 33), (42, 36), (38, 39), (9, 39), (6, 36)], ALU)
        for x in (12, 24, 36):
            d.ellipse(x, 36, 2.5, 4, None, BLUE)
        d.rect(19, 34.6, 9, 2.5, FRAME, .4)
        d.line([(20.5, 35.8), (26.5, 35.8)], ALU, .6)
        d.arc(25, 34, 12, 40, 140, RED)
    return d


def portable(kind):
    d = Equipment()
    if kind == 'loupe_tem':
        d.line([(7, 23), (15, 27), (26, 28), (32, 22)], FRAME, .7)
        place(d, operator(transmitter=True), 16, 11, .98)
        place(d, operator(receiver=True), 39, 11, .98)
        tag(d, 'TX', 3, 5)
        tag(d, 'RX', 30, 5)
        terrain(d, 38)
        d.arc(20, 28, 13, 40, 140, RED)
        d.arc(20, 28, 17, 40, 140, RED)
    elif kind == 'slingram_em':
        d.line([(8, 30), (20, 31), (34, 29)], FRAME, .7)
        place(d, operator(tablet=False), 12, 8, 1.05)
        place(d, operator(tablet=False), 35, 8, 1.05)
        d.line([(17, 18), (19, 25), (8, 29)], FRAME)
        d.ellipse(7, 30, 5.5, 2.2, None, BLUE)
        d.ellipse(7, 30.8, 5.5, 2.2, None, BLUE)
        d.line([(40, 19), (42, 24), (34, 28)], FRAME)
        d.ellipse(33, 29.5, 5, 2, YELLOW, '#111111')
        d.ellipse(33, 29.5, 3.4, .9, None, '#111111')
        terrain(d, 36)
        d.wave(10, 37, 42, 1.4, 2, BLUE)
    elif kind == 'ground_magnetics':
        place(d, operator(), 17, 11, 1.15)
        d.line([(26, 22), (32, 25), (34, 9)], FRAME, 1.1)
        d.rect(31.5, 3, 5.5, 7, ALU, 2)
        d.line([(32, 5.5), (36.5, 5.5)], FRAME, .7)
        d.line([(34, 3), (34, 1)], FRAME, .7)
        d.arc(34, 8, 9, 220, 330, RED)
        terrain(d, 40)
        d.wave(4, 44, 45, 1.4, 1.3, RED)
    else:
        # VLF: operator holding a real receiver console beside the transmitting mast.
        d.poly([(3, 34), (8, 5), (13, 34)], None, FRAME)
        for y in (13, 21, 29):
            d.line([(5, y+3), (10.7, y-2)], FRAME, .65)
        d.line([(8, 5), (8, 2)], FRAME)
        d.arc(8, 8, 8, -65, 65, BLUE)
        d.arc(8, 8, 13, -60, 60, BLUE)
        place(d, operator(tablet=False), 33, 12, 1.05)
        place(d, controller(True), 36, 22, .63)
        terrain(d, 40)
    return d


def earth_loop(drawing):
    drawing.poly([(4, 25), (29, 18), (44, 27), (20, 36)], '#E6D8BC', SOIL)
    drawing.poly([(4, 25), (20, 36), (44, 27), (44, 33), (20, 42), (4, 31)], SAND, SOIL)
    drawing.line([(20, 36), (20, 42)], SOIL, .7)
    drawing.line([(7, 30), (17, 36)], SOIL, .65)
    drawing.line([(26, 37), (38, 32.5)], SOIL, .65)
    drawing.poly([(7, 25), (28.5, 20.4), (40.5, 27), (20, 33.8)], None, BLUE)
    drawing.poly([(8, 25.3), (28.5, 21.4), (39, 27), (20, 32.8)], None, BLUE)
    for x, y in ((7, 25), (28.5, 20.4), (40.5, 27), (20, 33.8)):
        drawing.line([(x, y-1.7), (x, y+.8)], FRAME, .75)


def ground_tem(kind):
    d = Equipment()
    earth_loop(d)
    place(d, controller(), 4, 6, 1)
    d.line([(5, 15), (3, 20), (7, 25)], BLUE, .8)
    d.line([(14, 14), (18, 15), (28.5, 20.4)], BLUE, .8)
    if kind == 'tem_fixed_loop':
        for x, y in ((28, 39.5), (35.5, 37), (43, 34.5)):
            place(d, sensor(), x, y, .55)
        d.line([(27, 44), (44, 38)], FRAME, .65)
    elif kind == 'tem_moving_loop':
        place(d, sensor(), 23, 27, .65)
        d.arrow(23, 12, 42, 17, FRAME)
        d.line([(30, 10), (42, 13)], FRAME, .6)
    elif kind == 'tem_central_loop':
        d.ellipse(24, 27, 5.4, 2, None, RED)
        place(d, sensor(), 24, 26, .65)
        d.line([(24, 23), (29, 16), (36, 14)], FRAME, .7)
        place(d, controller(True), 35, 6, .8)
    elif kind == 'tem_in_loop':
        place(d, sensor(), 15, 25, .65)
        d.line([(16, 22), (26, 14), (37, 14)], FRAME, .7)
        place(d, controller(True), 35, 6, .8)
    else:
        place(d, sensor(), 25, 27, .7)
        place(d, controller(True), 35, 6, .8)
        d.line([(25, 23), (30, 15), (35, 13)], FRAME, .7)
        response(d, 30, 43, 13, 4, False)
    return d


def controlled_source(kind):
    d = Equipment()
    if kind == 'csem_marine':
        # Survey vessel, tow cable, horizontal electric dipole and seabed nodes.
        d.poly([(3, 8), (20, 8), (18, 12), (7, 12)], ALU)
        d.rect(7, 3.5, 8, 4.5, WHITE, .5)
        d.rect(8, 4.5, 5, 1.7, GLASS, .2)
        d.line([(11, 3.5), (11, 1), (15, 1)], FRAME, .7)
        d.line([(4, 7), (19, 7)], FRAME, .7)
        d.wave(2, 46, 14, .75, 3, WATER)
        d.line([(19, 10), (26, 16), (30, 22)], FRAME, .75)
        d.rect(27, 21, 8, 3, FRAME, .8)
        d.line([(18, 24), (43, 24)], BLUE, 1.2)
        d.circle(18, 24, 1.1, BLUE).circle(43, 24, 1.1, BLUE)
        d.line([(2, 35), (13, 34), (27, 36), (46, 34)], SOIL, 1)
        d.poly([(2, 36), (13, 35), (27, 37), (46, 35), (46, 46), (2, 46)], '#E2D0AE', SOIL)
        for x in (8, 23, 40):
            place(d, sensor(), x, 34, .65)
            d.line([(x-3, 35), (x-4, 37), (x+4, 37), (x+3, 35)], FRAME, .65)
        d.line([(30, 27), (27, 41), (13, 42), (8, 37)], BLUE, .8)
        d.line([(4, 44), (19, 44), (32, 43), (44, 44)], SOIL, .7)
        return d
    terrain(d, 23)
    place(d, controller(), 5, 8, 1)
    d.line([(5, 17), (2, 20), (2, 28)], BLUE)
    d.line([(16, 16), (23, 19), (23, 28)], BLUE)
    for x in (2, 23):
        d.line([(x-1.5, 26), (x+1.5, 26)], FRAME, .75)
    place(d, controller(True), 34, 9, .9)
    if kind == 'csamt':
        d.line([(32, 18), (29, 23), (28, 28)], BLUE)
        d.line([(42, 18), (45, 23), (45, 28)], BLUE)
        d.rect(31, 27, 11, 2.3, RED, .7)
        tag(d, 'E', 31, 34)
        tag(d, 'H', 40, 34)
        d.wave(28, 45, 5, 1.1, 2, BLUE)
    else:
        place(d, sensor(), 36, 24, .8)
        d.line([(3, 30), (14, 41), (36, 29)], BLUE, .85)
        d.line([(23, 30), (27, 36), (44, 27)], BLUE, .85)
        d.line([(4, 45), (20, 43), (43, 44)], SOIL, .7)
    return d


def frequency_domain():
    d = Equipment()
    # Rigid-boom induction instrument: orthogonal mounting, coils and console.
    d.line([(7, 16), (40, 16)], FRAME, 1.8)
    d.line([(21, 16), (21, 8), (27, 8), (27, 16)], FRAME)
    d.rect(19, 7, 10, 5, ALU, .7)
    d.rect(21, 8.3, 4.5, 2.1, GLASS, .2)
    d.ellipse(7, 16, 5, 7, ALU, BLUE)
    d.ellipse(7, 16, 2.8, 4.7, None, BLUE)
    d.ellipse(40, 16, 5, 7, YELLOW, '#111111')
    d.ellipse(40, 16, 2.8, 4.7, None, '#111111')
    d.wave(16, 32, 3, 1.4, 2, BLUE)
    terrain(d, 29)
    d.ellipse(24, 39, 6, 2, None, RED)
    d.arc(24, 25, 13, 25, 155, RED)
    d.arc(24, 25, 19, 30, 150, RED)
    return d


def transient(kind):
    d = Equipment()
    place(d, controller(), 3, 3, 1.05)
    waveform(d, 20, 3, 24, 6)
    if kind == 'ip_spectral':
        d.line([(5, 20), (5, 43), (44, 43)], FRAME, .8)
        for x in (12, 20, 28, 36, 44):
            d.line([(x, 42), (x, 44)], FRAME, .6)
        d.line([(8, 38), (14, 37.5), (21, 35), (28, 28), (35, 24), (43, 24)], BLUE, 1.1)
        d.line([(8, 40), (15, 39), (22, 31), (29, 25), (36, 32), (43, 39)], RED, 1.1)
        for x, y in ((14, 37.5), (28, 28), (43, 24)):
            d.circle(x, y, .8, WHITE, BLUE)
    elif kind == 'tem_decay_gates':
        response(d, 19, 15, 25, 26)
        for x, y, h in ((23, 22, 18), (29, 31, 9), (37, 36, 4)):
            d.rect(x, y, 3.1, h, GLASS, .2)
        # Response is drawn last so the signal remains visible through the gates.
        d.line([(20+24*i/60, 15+26*(1-math.exp(-i/11))) for i in range(61)], RED, 1.1)
        d.line([(7, 14), (7, 38), (16, 38)], BLUE, .8)
    elif kind == 'electrical_ip_chargeability':
        terrain(d, 24)
        d.line([(5, 13), (3, 18), (3, 29)], BLUE)
        d.line([(14, 12), (18, 18), (18, 29)], BLUE)
        place(d, controller(True), 31, 12, .8)
        d.line([(31, 20), (26, 23), (26, 28)], BLUE, .8)
        d.line([(40, 20), (44, 23), (44, 28)], BLUE, .8)
        response(d, 24, 32, 20, 11)
    else:
        # A receiver, transmitter loop and decay plot show acquisition and response.
        d.poly([(3, 25), (20, 21), (28, 27), (12, 32)], None, BLUE)
        d.poly([(4.5, 25.3), (20, 22), (26, 27), (12, 31)], None, BLUE)
        place(d, sensor(), 15, 26, .7)
        d.line([(6, 13), (2, 18), (3, 25)], BLUE, .8)
        response(d, 31, 20, 14, 22)
        d.arc(15, 29, 11, 30, 150, RED)
        d.arc(15, 29, 15, 40, 140, RED)
    return d


def scene(kind):
    if kind in {'airborne_em_aem', 'fixed_wing_aem', 'vtem', 'skytem', 'airborne_magnetics', 'airborne_radiometrics'}:
        return airborne(kind)
    if kind in {'loupe_tem', 'slingram_em', 'ground_magnetics', 'vlf_em'}:
        return portable(kind)
    if kind in {'ground_tem', 'tem_fixed_loop', 'tem_moving_loop', 'tem_central_loop', 'tem_in_loop'}:
        return ground_tem(kind)
    if kind in {'csem_marine', 'csem_land', 'csamt'}:
        return controlled_source(kind)
    if kind == 'frequency_domain_em_fdem':
        return frequency_domain()
    if kind in {'time_domain_em_tdem', 'electrical_ip_chargeability', 'ip_spectral', 'tem_decay_gates'}:
        return transient(kind)
    if kind == 'tem_lotem':
        d = controlled_source('csem_land')
        d.line([(25, 7), (29, 7), (32, 7)], FRAME, .65)
        d.arrow(27, 4, 43, 4, FRAME)
        return d
    if kind == 'magnetic_gradiometry':
        d = Equipment()
        d.line([(24, 4), (24, 36)], FRAME, 1.6)
        for y in (8, 28):
            d.rect(20, y-4, 8, 9, ALU, 2)
            d.line([(20.5, y-1), (27.5, y-1)], FRAME, .65)
            d.circle(24, y+2, 1, GLASS)
        d.line([(24, 36), (34, 36), (37, 23)], FRAME, .7)
        place(d, controller(), 33, 16, .8)
        d.arrow(12, 10, 12, 28, RED)
        d.wave(3, 45, 43, 1.7, 1.2, RED)
        return d
    raise ValueError(f'Unknown EM equipment composition: {kind}')
