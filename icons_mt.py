"""Append-only MT field, signal and transfer-function artwork, without lettering.

48-unit Y-down engineering drawings. The same geometry generates monochrome
font outlines and natural-colour SVG/PNG illustrations. Coordinates and contours
carry meaning: electrodes, ferrite/coil windings, response axes and sample marks.
"""
import math
from functools import lru_cache, partial
from shapely import affinity
from shapely.geometry import LineString, Point, box
from icons_geophysics_expanded import Diagram, Part, native

INK = '#303A40'
STEEL = '#849199'
ALU = '#C7D0D4'
COPPER = '#B5794D'
SOIL = '#B58D65'
SAND = '#DECAA5'
ROCK = '#8B9391'
GLASS = '#D1E6ED'
BLUE = '#3478F6'
RED = '#D9525D'
YELLOW = '#F2C94C'
PAPER = '#F8FAF7'
GRID = '#BEC8CC'


class Drawing(Diagram):
    def line(self, points, colour=INK, width=.95):
        return super().line(points, colour, width)

    def shape(self, geometry, fill=None, colour=INK, width=.95, solid=False):
        super().shape(geometry, fill, colour, width, solid)
        # An unfilled field loop or coil winding must not erase the sensor
        # inside it when the monochrome contours are combined.
        if fill is None:
            self.parts[-1].face = None
        return self

    def dash(self, start, end, colour=GRID, count=6, width=.65):
        for index in range(count):
            a, b = (index+.12)/count, (index+.64)/count
            self.line([(start[0]+(end[0]-start[0])*t, start[1]+(end[1]-start[1])*t)
                       for t in (a, b)], colour, width)
        return self


def wave(d, left, right, y, amplitude=2, cycles=2, colour=INK, phase=0, width=.95):
    return d.line([(left+(right-left)*i/100,
                    y+amplitude*math.sin(i/100*math.tau*cycles+phase)) for i in range(101)], colour, width)


def axes(d, x=5, y=40, width=38, height=31, grid=False):
    if grid:
        for t in (.25, .5, .75):
            d.dash((x, y-height*t), (x+width, y-height*t), GRID, 9, .45)
    d.line([(x, y-height), (x, y), (x+width, y)], INK, 1)
    for t in (.2, .4, .6, .8):
        d.line([(x+width*t, y), (x+width*t, y+1.3)], INK, .65)
        d.line([(x-1.2, y-height*t), (x, y-height*t)], INK, .65)


def vector_inset(d, component, colour):
    # Three spatial directions, with one selected. No X/Y/Z lettering required.
    origin = (35, 36)
    ends = [(45, 36), (28.5, 42), (35, 25)]
    for index, end in enumerate(ends):
        if index == 'xyz'.index(component):
            d.arrow(*origin, *end, colour)
        else:
            d.line([origin, end], GRID, .7)
    d.circle(*origin, .85, INK, INK, True)


def electric(component=None):
    d = Drawing()
    # Paired porous-pot electrodes: copper contacts, insulated tops and lead wires.
    for x in (10, 37):
        d.rect(x-1.8, 22, 3.6, 11, COPPER, .8)
        d.rect(x-2.5, 20, 5, 4, ALU, .7)
        d.line([(x, 33), (x, 35)], COPPER, 1.4)
        d.line([(x-4, 35), (x+4, 35)], SOIL, .7)
        d.line([(x-3, 37), (x-1, 36)], SOIL, .65)
    d.line([(10, 20), (10, 16), (15, 16)], BLUE)
    d.line([(37, 20), (37, 16), (32, 16)], BLUE)
    d.rect(18, 12, 11, 7, YELLOW, .8, '#111111')
    d.rect(20, 13.7, 4.5, 2.2, GLASS, .35)
    d.circle(26.5, 16.8, .6, STEEL)
    # Equipotential/field trajectories retain open space around the receiver.
    for y, bow in ((9, -5), (23, 5), (28, 7)):
        points = [(11+25*i/60, y+bow*math.sin(math.pi*i/60)) for i in range(61)]
        d.line(points, BLUE, .85)
        if y != 9:
            d.arrow(20, y+bow*.9, 27, y+bow*.9, BLUE)
    if component:
        vector_inset(d, component, BLUE)
    else:
        d.arrow(16, 42, 32, 42, BLUE)
    return d


def magnetic(component=None):
    d = Drawing()
    # Ferrite induction rod with multiple real windings and end caps.
    d.rect(11, 19, 26, 7, ROCK, 2)
    for x in (12, 36):
        d.rect(x-1.3, 18.5, 2.6, 8, ALU, .7)
    for x in (17, 20, 23, 26, 29, 32):
        d.ellipse(x, 22.5, 1.45, 5, None, COPPER)
    d.line([(17, 27), (17, 31), (10, 31)], RED, .8)
    d.line([(32, 27), (32, 31), (38, 31)], RED, .8)
    # Curved closed field lines distinguish magnetism from the electric dipole.
    d.ellipse(24, 22.5, 20, 11, None, RED)
    d.arc(24, 22.5, 17, 205, 335, RED)
    d.arrow(21, 11.5, 28, 11.5, RED)
    d.arrow(29, 33.5, 22, 33.5, RED)
    if component:
        vector_inset(d, component, RED)
    else:
        d.arrow(8, 42, 25, 42, RED)
    return d


def poynting():
    d = Drawing()
    # Orthogonal electric and magnetic oscillations around a common energy ray.
    d.dash((7, 38), (43, 11), GRID, 10)
    d.arrow(7, 38, 44, 10, YELLOW)
    for i in range(2):
        cx, cy = 15+i*13, 32-i*10
        d.arrow(cx, cy, cx-2, cy-15, BLUE)
        d.arrow(cx, cy, cx+12, cy+4, RED)
        d.line([(cx, cy-3), (cx+2.3, cy-2.3), (cx+2.3, cy+.8)], STEEL, .65)
    wave(d, 6, 42, 39, 2.2, 2, BLUE, width=.75)
    d.line([(7, 45), (43, 45)], SOIL, .8)
    for x in (10, 20, 30, 40):
        d.line([(x, 45), (x-1.5, 47)], SOIL, .6)
    return d


def spectrum():
    d = Drawing()
    axes(d, grid=True)
    def response(t):
        return 34-20*math.exp(-((t-.3)/.065)**2)-13*math.exp(-((t-.67)/.09)**2)+3*t
    d.line([(7+35*i/160, response(i/160)) for i in range(161)], INK, 1.35)
    d.dash((17.5, 12), (17.5, 39), STEEL, 7, .65)
    d.line([(15.5, 11), (19.5, 11)], INK, .8)
    for x, y in ((11, 33), (26, 32), (37, 37)):
        d.circle(x, y, .85, PAPER, STEEL)
    return d


def fft():
    d = Drawing()
    d.rect(3, 7, 17, 17, PAPER, 1)
    wave(d, 4.5, 18.5, 15, 3.6, 2.1, INK)
    d.dash((7, 8), (7, 23), STEEL, 5)
    d.dash((16, 8), (16, 23), STEEL, 5)
    d.arrow(23, 15, 32, 15, INK)
    axes(d, 23, 41, 22, 17)
    for i, height in enumerate((2, 4, 13, 6, 3, 9, 4, 2)):
        x = 25+i*2.5
        d.line([(x, 40), (x, 40-height)], INK, 1)
        d.circle(x, 40-height, .7, STEEL, INK, True)
    d.line([(5, 30), (5, 37), (16, 37)], STEEL, .8)
    d.line([(9, 33), (9, 41)], STEEL, .8)
    d.line([(13, 33), (13, 41)], STEEL, .8)
    return d


def spectrogram():
    d = Drawing()
    axes(d, 5, 42, 37, 35)
    # Discrete energy cells, with curved ridge/strong transient; no decorative text.
    palette = ['#E7EEF0', '#B8CFD1', '#79A5AB', '#D8B75C', '#BA744B']
    for column in range(9):
        for row in range(6):
            ridge = 2.8+1.3*math.sin(column*.6)
            energy = max(0, 3.4-abs(row-ridge)*2)
            if column == 6: energy = max(energy, 2.4)
            d.rect(7+column*3.7, 8+row*5.1, 3.25, 4.5,
                   palette[min(4, int(energy))], .15, '#D1DBDD')
    d.line([(8+column*3.7, 10+(2.8+1.3*math.sin(column*.6))*5.1)
            for column in range(9)], INK, 1.2)
    d.rect(43.5, 12, 2.4, 25, None, .2)
    for row, colour in enumerate(reversed(palette)):
        d.rect(43.7, 12+row*5, 2, 4.6, colour, .1, colour)
    return d


def waveform():
    d = Drawing()
    d.rect(3, 5, 42, 37, PAPER, 1)
    for y in (16, 32): d.dash((5, y), (43, y), GRID, 12, .55)
    for x in (10, 19, 28, 37):
        d.line([(x, 40), (x, 42)], INK, .7)
    for y, colour, phase in ((16, BLUE, 0), (32, RED, .7)):
        points = []
        for i in range(121):
            t = i/120
            spike = -6*math.exp(-((t-.63)/.016)**2)+3*math.exp(-((t-.67)/.02)**2)
            points.append((5+38*t, y+2.5*math.sin(t*math.tau*3+phase)+spike))
        d.line(points, colour, 1)
        for x, value in points[::10]: d.circle(x, value, .6, colour, colour, True)
    return d


def cross_power():
    d = Drawing()
    d.rect(3, 5, 16, 10, PAPER, .8)
    d.rect(3, 30, 16, 10, PAPER, .8)
    wave(d, 4, 18, 10, 2.6, 1.6, BLUE)
    wave(d, 4, 18, 35, 2.6, 1.6, RED, .8)
    d.line([(19, 10), (24, 10), (24, 19)], BLUE)
    d.line([(19, 35), (24, 35), (24, 26)], RED)
    d.poly([(24, 17), (29, 22.5), (24, 28), (19, 22.5)], GLASS)
    d.line([(22.3, 20.8), (25.7, 24.2)], INK, .8)
    d.line([(25.7, 20.8), (22.3, 24.2)], INK, .8)
    d.arrow(30, 22.5, 36, 22.5, INK)
    d.line([(35, 36), (35, 30), (46, 30)], STEEL, .8)
    d.line([(40, 14), (40, 37)], GRID, .7)
    d.circle(40, 24, 6.5, None, STEEL)
    d.arrow(40, 24, 45, 19, INK)
    return d


def coherence():
    d = Drawing()
    wave(d, 4, 44, 9, 2.4, 3, BLUE)
    wave(d, 4, 44, 18, 2.4, 3, RED, .13)
    for x in (8, 21.3, 34.6): d.dash((x, 7), (x, 20), STEEL, 4, .55)
    axes(d, 5, 43, 38, 16)
    d.dash((6, 28), (43, 28), GRID, 10, .65)
    d.line([(7+35*i/100, 30+7*math.exp(-((i/100-.6)/.12)**2)
             +.7*math.sin(i*.1)) for i in range(101)], INK, 1.2)
    return d


def calibration():
    d = Drawing()
    d.rect(3, 16, 18, 6, STEEL, 2)
    for x in (7, 10, 13, 16): d.ellipse(x, 19, 1.4, 5.5, None, COPPER)
    d.rect(2, 28, 18, 12, YELLOW, 1, '#111111')
    d.rect(4, 30, 9, 4, GLASS, .4)
    d.circle(16, 32, .9, STEEL)
    d.line([(7, 25), (7, 28)], RED)
    d.line([(17, 24), (23, 24), (23, 36), (20, 36)], RED)
    axes(d, 28, 23, 17, 17)
    d.line([(29+15*t, 20-11/(1+math.exp(-(t-.4)*12)))
            for t in (i/60 for i in range(61))], INK, 1.1)
    axes(d, 28, 43, 17, 14)
    d.line([(29+15*t, 31+10/(1+math.exp(-(t-.5)*10)))
            for t in (i/60 for i in range(61))], STEEL, 1.1)
    d.circle(35, 14.8, .8, PAPER, INK)
    d.circle(39, 37.8, .8, PAPER, INK)
    return d


def remote_reference():
    d = Drawing()
    for x, y in ((11, 28), (37, 15)):
        d.line([(x-7, y+8), (x+7, y+8)], SOIL, .8)
        d.rect(x-3, y-2, 6, 6, YELLOW, .7, '#111111')
        d.rect(x-1.8, y-.9, 2.2, 1.5, GLASS, .2)
        d.line([(x-7, y+5), (x+7, y+5)], BLUE, .9)
        for end in (-7, 7):
            d.line([(x+end, y+4), (x+end, y+7)], COPPER, 1)
        d.line([(x, y-7), (x, y-2)], RED, 2.4)
        d.line([(x-.9, y-6), (x+.9, y-6)], COPPER, .65)
    d.dash((15, 25), (32, 17), STEEL, 6, .85)
    d.arrow(16, 12, 25, 8, INK)
    wave(d, 5, 21, 43, 2, 1.5, BLUE)
    wave(d, 28, 44, 37, 2, 1.5, RED, .1)
    return d


def mt_survey():
    """Simplified reference layout: two E dipoles, three H rods, one logger."""
    d = Drawing()
    # The survey plane sets the perspective; no compass, dimensions or labels.
    d.poly([(3, 20), (23, 4), (45, 23), (25, 44)], '#F1EEE7', '#B0B7B7')
    d.line([(8, 33), (39, 12)], BLUE, 1.4)
    d.line([(10, 12), (39, 35)], BLUE, 1.4)
    for x, y in ((8, 33), (39, 12), (10, 12), (39, 35)):
        d.rect(x-1, y-.6, 2, 3.4, COPPER, .25, INK)
        d.line([(x-1.7, y+3.1), (x+1.7, y+3.1)], SOIL, .5)
    # Three magnetic rods have separate orientations and visible end caps.
    for start, end in (((17, 30), (23, 26)), ((29, 29), (35, 32)), ((27, 19), (27, 13))):
        d.line([start, end], INK, 2.7)
        d.line([start, end], RED, 1.65)
        for point in (start, end): d.circle(*point, .8, ALU, INK)
    d.line([(20, 24), (19, 27), (18, 28)], INK, .65)
    d.line([(20, 23), (25, 25), (29, 29)], INK, .65)
    d.line([(20, 22), (24, 21), (27, 19)], INK, .65)
    d.rect(13, 20, 8, 5.2, YELLOW, .65, '#111111')
    d.rect(14.3, 21, 3.2, 1.8, GLASS, .25, INK)
    d.circle(19, 23.2, .5, STEEL, INK)
    return d


def impedance():
    d = Drawing()
    # Four complex response panels and the E/H mapping; a matrix, without letters.
    for x in (8, 26):
        for y in (8, 26):
            d.rect(x, y, 15, 15, PAPER, .7)
            d.line([(x+2, y+11), (x+12, y+11)], GRID, .6)
            d.line([(x+5, y+13), (x+5, y+2)], GRID, .6)
            phase = .5 if x == y else 1.3
            d.line([(x+3+9*t, y+11-7*math.sin(t*phase))
                    for t in (i/30 for i in range(31))], INK, 1.1)
    d.line([(5, 7), (3, 7), (3, 42), (5, 42)], BLUE, 1.2)
    d.line([(43, 7), (45, 7), (45, 42), (43, 42)], RED, 1.2)
    for x in (14, 32): d.arrow(x, 2, x, 6, RED)
    return d


def phase_tensor():
    d = Drawing()
    axes(d, 7, 41, 36, 34)
    ellipse = affinity.rotate(affinity.scale(Point(25, 24).buffer(1, quad_segs=48),
                                            17, 9, origin=(25, 24)), -32, origin=(25, 24))
    d.shape(ellipse, GLASS, INK, 1.3)
    d.dash((8, 35), (42, 13), STEEL, 9, .7)
    d.dash((18, 12), (32, 36), STEEL, 7, .7)
    d.arrow(25, 24, 37, 16.5, INK)
    d.arc(25, 24, 20, 215, 310, STEEL)
    d.arrow(35.5, 7.3, 38, 9.2, STEEL)
    d.circle(25, 24, 1.25, YELLOW, '#111111')
    return d


def tipper():
    d = Drawing()
    # A station and one horizontal induction arrow above a conductive contact.
    d.line([(4, 34), (44, 34)], INK, 1.4)
    d.poly([(25, 34), (30, 34), (35, 44), (20, 44)], ROCK, INK)
    d.receiver(13, 34, 2.5)
    d.arrow(13, 25, 37, 25, RED)
    return d


ROWS = [
    ('electric_field', 'Electric Field', 'Electric dipole electrodes, insulated leads, receiver and directed electric field lines.', electric, ['electric', 'field', 'E', 'dipole']),
    *[(f'electric_field_{axis}', f'Electric Field E{axis}', f'Electric dipole with the {axis} component selected on an unlabelled spatial triad.', partial(electric, axis), ['electric', 'field', f'E{axis}', 'component']) for axis in 'xyz'],
    ('magnetic_field', 'Magnetic Field', 'Ferrite induction coil with copper windings and closed magnetic field trajectories.', magnetic, ['magnetic', 'field', 'H', 'induction']),
    *[(f'magnetic_field_{axis}', f'Magnetic Field H{axis}', f'Induction coil with the {axis} component selected on an unlabelled spatial triad.', partial(magnetic, axis), ['magnetic', 'field', f'H{axis}', 'component']) for axis in 'xyz'],
    ('poynting_vector', 'Poynting Vector', 'Perpendicular electric and magnetic vectors with a yellow energy-flow ray.', poynting, ['poynting', 'energy', 'flux', 'E', 'H']),
    ('signal_spectrum', 'Recording Spectrum', 'Frequency spectrum with distinct resonant peaks, logarithmic-style ticks and a peak marker.', spectrum, ['spectrum', 'frequency', 'power', 'PSD']),
    ('fft_transform', 'Fourier Transform FFT', 'Windowed oscillation converted to discrete frequency bins with distinct spectral peaks.', fft, ['FFT', 'Fourier', 'transform', 'window', 'frequency']),
    ('signal_spectrogram', 'Recording Spectrogram', 'Time-frequency energy cells with a curved spectral ridge, transient and colour scale.', spectrogram, ['spectrogram', 'time', 'frequency', 'FFT']),
    ('raw_waveform', 'Raw Time Series', 'Sampled electric and magnetic traces with shared time markers and a transient spike.', waveform, ['raw', 'waveform', 'samples', 'time', 'series']),
    ('cross_power', 'Cross Power', 'Two channel spectra enter a product operator and produce a complex cross-power phasor.', cross_power, ['cross', 'power', 'complex', 'spectrum']),
    ('signal_coherence', 'Signal Coherence', 'Phase-aligned channel waveforms and a bounded coherence curve with a local loss of coherence.', coherence, ['coherence', 'correlation', 'cross', 'spectra']),
    ('sensor_calibration', 'Sensor Calibration Response', 'Wound induction sensor and receiver beside separate gain and phase calibration curves.', calibration, ['sensor', 'coil', 'calibration', 'response', 'gain', 'phase']),
    ('remote_reference', 'Remote Reference Pair', 'Two spatially separated electrode and coil stations with paired traces and a shared reference link.', remote_reference, ['remote', 'reference', 'station', 'pair', 'MT']),
    ('mt_impedance_tensor', 'MT Impedance Tensor', 'Four complex response plots arranged as a two-by-two electric-to-magnetic transfer matrix.', impedance, ['MT', 'impedance', 'tensor', 'Z', 'transfer']),
    ('mt_phase_tensor', 'MT Phase Tensor', 'Rotated phase ellipse with principal directions, azimuth arc and a central station.', phase_tensor, ['MT', 'phase', 'tensor', 'ellipse', 'azimuth']),
    ('mt_tipper', 'MT Tipper', 'Horizontal magnetic induction arrow at a station above a conductive geological contact.', tipper, ['MT', 'tipper', 'induction', 'arrow', 'Hz']),
]

MT_ICONS = [dict(id='gp_'+identifier, codepoint=0xE112+index, name=name,
                 domain='Geophysical', category='Processes', description=description,
                 keywords=keywords+['magnetotellurics', 'Ionos'], builder=lambda builder=builder: builder().geometry())
            for index, (identifier, name, description, builder, keywords) in enumerate(ROWS)]
MT_IDS = {icon['id'] for icon in MT_ICONS} | {'gp_magnetotellurics_mt'}
BUILDERS = {'gp_'+row[0]: row[3] for row in ROWS}
BUILDERS['gp_magnetotellurics_mt'] = mt_survey


@lru_cache(maxsize=32)
def flat_artwork(identifier):
    from detailed_flat import FlatLayer
    drawing = BUILDERS[identifier]()
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
