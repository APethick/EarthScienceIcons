"""Detailed equipment, acquisition, borehole and petrophysical glyphs.

Append-only extension: original IDs/codepoints remain untouched. Drawings use
a 48-unit engineering canvas; one composition supplies line and material-colour
outputs. Equipment silhouettes are schematic, not manufacturer logos.
"""

import math
from dataclasses import dataclass
from functools import lru_cache, partial

from shapely import affinity
from shapely.geometry import Point, LineString, Polygon, box
from shapely.ops import unary_union

INK = '#303A40'
STEEL = '#849199'
ALU = '#C7D0D4'
GLASS = '#D1E6ED'
SOIL = '#B58D65'
SAND = '#DECAA5'
ROCK = '#8B9391'
WATER = '#61A9C8'
BLUE = '#3478F6'
RED = '#E35D65'
YELLOW = '#F2C94C'
WHITE = '#F8FAF7'


@dataclass
class Part:
    ink: object
    colour: str = INK
    face: object = None
    fill: str = None


class Diagram:
    def __init__(self):
        self.parts = []

    def line(self, points, colour=INK, width=1.35):
        self.parts.append(Part(LineString(points).buffer(width / 2, quad_segs=6, cap_style=1, join_style=1), colour))
        return self

    def shape(self, geometry, fill=None, colour=INK, width=1.35, solid=False):
        ink = geometry if solid else geometry.boundary.buffer(width / 2, quad_segs=6, join_style=1)
        self.parts.append(Part(ink, colour if not solid else fill or colour, geometry, fill))
        return self

    def rect(self, x, y, width, height, fill=None, radius=.8, colour=INK):
        radius = min(radius, width / 2, height / 2)
        geometry = box(x + radius, y + radius, x + width - radius, y + height - radius).buffer(radius, quad_segs=6) if radius else box(x, y, x + width, y + height)
        return self.shape(geometry, fill, colour)

    def circle(self, x, y, radius, fill=None, colour=INK, solid=False):
        return self.shape(Point(x, y).buffer(radius, quad_segs=18), fill, colour, solid=solid)

    def ellipse(self, x, y, rx, ry, fill=None, colour=INK):
        geometry = affinity.scale(Point(x, y).buffer(1, quad_segs=20), rx, ry, origin=(x, y))
        return self.shape(geometry, fill, colour)

    def poly(self, points, fill=None, colour=INK, solid=False):
        return self.shape(Polygon(points), fill, colour, solid=solid)

    def arrow(self, x0, y0, x1, y1, colour=INK):
        dx, dy = x1-x0, y1-y0
        length = math.hypot(dx, dy)
        ux, uy = dx/length, dy/length
        self.line([(x0,y0),(x1-ux*1.5,y1-uy*1.5)], colour)
        self.poly([(x1,y1),(x1-ux*3-uy*1.7,y1-uy*3+ux*1.7),(x1-ux*3+uy*1.7,y1-uy*3-ux*1.7)], colour, colour, True)
        return self

    def arc(self, x, y, radius, start, stop, colour=INK):
        return self.line([(x+radius*math.cos(math.radians(start+(stop-start)*i/40)),y+radius*math.sin(math.radians(start+(stop-start)*i/40))) for i in range(41)], colour)

    def wave(self, x0, x1, y, amp=2, cycles=2, colour=INK):
        return self.line([(x0+(x1-x0)*i/80,y+amp*math.sin(i/80*cycles*math.tau)) for i in range(81)], colour)

    def receiver(self, x, y, radius=1.8):
        return self.circle(x,y,radius,YELLOW,'#111111')

    def ground(self, y=24):
        self.line([(3,y),(45,y)])
        for x in (5,14,23,32,41):
            self.line([(x,y+1),(x-1.5,y+3)], SOIL, .9)
        return self

    def coil(self, x, y, rx=5, ry=2.2, colour=BLUE):
        self.ellipse(x,y,rx,ry,None,colour)
        self.line([(x-rx,y),(x-rx,y+2)], colour)
        return self

    def word(self, text, x, y, scale=1, colour=INK):
        alphabet = {
            'A': [[(0,5),(1.5,0),(3,5)],[(.6,3),(2.4,3)]],
            'C': [[(3,.5),(2,0),(0,1),(0,4),(2,5),(3,4.5)]],
            'E': [[(3,0),(0,0),(0,5),(3,5)],[(0,2.5),(2.5,2.5)]],
            'H': [[(0,0),(0,5)],[(3,0),(3,5)],[(0,2.5),(3,2.5)]],
            'K': [[(0,0),(0,5)],[(3,0),(0,2.5),(3,5)]],
            'M': [[(0,5),(0,0),(1.5,3),(3,0),(3,5)]],
            'N': [[(0,5),(0,0),(3,5),(3,0)]],
            'P': [[(0,5),(0,0),(3,0),(3,2.5),(0,2.5)]],
            'R': [[(0,5),(0,0),(3,0),(3,2.5),(0,2.5),(3,5)]],
            'S': [[(3,0),(0,0),(0,2.5),(3,2.5),(3,5),(0,5)]],
            'T': [[(0,0),(3,0)],[(1.5,0),(1.5,5)]],
            'U': [[(0,0),(0,4),(1,5),(2,5),(3,4),(3,0)]],
            'V': [[(0,0),(1.5,5),(3,0)]],
            '0': [[(0,1),(1,0),(2,0),(3,1),(3,4),(2,5),(1,5),(0,4),(0,1)]],
            '1': [[(0,1),(1.5,0),(1.5,5)],[(0,5),(3,5)]],
            '+': [[(0,2.5),(3,2.5)],[(1.5,1),(1.5,4)]],
            '-': [[(0,2.5),(3,2.5)]],
        }
        for index, character in enumerate(text.upper()):
            for points in alphabet[character]:
                self.line([(x+(index*4.5+px)*scale,y+py*scale) for px,py in points], colour, .85*scale)
        return self

    def geometry(self):
        result=Polygon()
        for part in self.parts:
            if part.face is not None:
                result=result.difference(part.face)
            result=result.union(part.ink)
        return native(result)


def native(geometry):
    geometry=affinity.scale(geometry,xfact=1000/48,yfact=-1000/48,origin=(0,0))
    return affinity.translate(geometry,yoff=1000)


def pulse(d, x=5, y=6, width=18, height=6):
    d.line([(x,y+height),(x+width*.2,y+height),(x+width*.2,y),(x+width*.6,y),(x+width*.6,y+height),(x+width,y+height)],BLUE)


def decay(d, x=27, y=8, width=16, height=10, gates=False):
    d.line([(x,y-1),(x,y+height),(x+width,y+height)],STEEL,.9)
    d.line([(x+1+width*i/40,y+height*(1-math.exp(-i/8))) for i in range(41)],RED)
    if gates:
        for t in (3,7,12):
            d.line([(x+t,y+height-2),(x+t,y+height+1)],INK,.85)


def em_scene(kind):
    from em_artwork import scene
    return scene(kind)


def gpr_scene(kind):
    d=Diagram()
    if kind=='gpr_b_scan':
        d.rect(3,4,42,39,GLASS)
        d.line([(4,11),(44,11)],STEEL)
        for cx,top in ((15,17),(33,25)):
            d.line([(cx+t,top+math.sqrt(t*t+8)-math.sqrt(8)) for t in range(-10,11)],BLUE)
        d.line([(7,39),(41,39)],STEEL,.9)
    elif kind=='gpr_time_slice':
        d.rect(4,4,39,39,SAND)
        for x in (14,24,34):d.line([(x,5),(x,42)],WHITE,.9)
        for y in (14,24,34):d.line([(5,y),(42,y)],WHITE,.9)
        d.line([(8,35),(35,9)],BLUE,3)
        d.line([(10,8),(39,37)],STEEL,2)
        d.circle(23,23,3,None,RED)
    elif kind=='gpr_volume_3d':
        d.poly([(24,3),(44,13),(24,24),(4,13)],SAND)
        d.poly([(4,13),(24,24),(24,45),(4,34)],SOIL)
        d.poly([(24,24),(44,13),(44,34),(24,45)],ROCK)
        d.line([(5,25),(24,35),(43,24)],BLUE,2)
        d.line([(15,9),(35,19),(35,39)],WHITE,.9)
    elif kind=='gpr_cmp_velocity':
        d.ground(13)
        d.rect(7,7,8,4,STEEL).rect(33,7,8,4,STEEL)
        d.arrow(16,4,6,4).arrow(32,4,42,4)
        d.line([(11,14),(24,39),(37,14)],BLUE)
        d.line([(19,14),(24,28),(29,14)],BLUE)
        d.line([(4,39),(44,39)],SOIL)
    elif kind in {'gpr_utility_detection','gpr_concrete_rebar','gpr_antenna'}:
        d.ground(21)
        if kind=='gpr_utility_detection':
            d.rect(10,11,17,6,ALU).line([(22,11),(29,4),(33,4)])
            d.circle(12,19,2,STEEL,solid=True).circle(25,19,2,STEEL,solid=True)
            d.circle(15,37,4,ALU).circle(35,31,3,WATER)
            d.line([(6,40),(15,28),(24,40)],BLUE)
            d.line([(27,35),(35,24),(43,35)],BLUE)
        elif kind=='gpr_concrete_rebar':
            d.rect(14,9,17,8,STEEL).line([(19,9),(19,5),(27,5),(27,9)])
            d.rect(4,26,40,17,ROCK)
            for x in (10,24,38):d.circle(x,33,2.2,STEEL)
            d.line([(5,39),(43,39)],STEEL,2)
            d.arc(24,20,8,30,150,BLUE)
        else:
            d.rect(8,5,32,10,STEEL,2)
            d.poly([(13,17),(23,9),(23,25)],BLUE)
            d.poly([(35,17),(25,9),(25,25)],BLUE)
            d.arc(24,22,11,25,155,BLUE).arc(24,22,18,25,155,BLUE)
    else:
        d.ground(6)
        for x in (8,36):d.rect(x,7,5,37,SAND,.2)
        d.rect(8,15,5,11,ALU).receiver(38.5,31,2.5)
        d.line([(14,20),(35,31)],BLUE).line([(14,21),(25,40),(35,32)],BLUE)
        d.wave(17,32,12,1,3,BLUE)
    return d


def radiometric_scene(kind):
    d=Diagram()
    if kind=='radiometrics_ternary':
        d.poly([(24,4),(45,42),(3,42)],None)
        d.poly([(24,24),(24,4),(3,42)],SOIL,SOIL)
        d.poly([(24,24),(24,4),(45,42)],ROCK,ROCK)
        d.poly([(24,24),(3,42),(45,42)],SAND,SAND)
        d.word('K',2,33,1.1).word('U',40,33,1.1).word('TH',20,4,1)
        d.circle(24,25,1.5,WHITE,solid=True)
        return d
    d.rect(4,4,40,39,GLASS,2)
    # Spectral peaks and a distinct channel window, not four copies of one badge.
    selected={'radiometrics_total':None,'radiometrics_potassium_k':14,'radiometrics_uranium_u':25,'radiometrics_thorium_th':36}[kind]
    for x,height in ((14,14),(25,21),(36,28)):
        colour=YELLOW if selected is None or x==selected else ALU
        if selected==x:d.rect(x-3,12,6,27,SAND,.3)
        d.poly([(x-4,38),(x,38-height),(x+4,38)],colour,INK)
    d.line([(8,39),(41,39)],INK)
    if selected is None:d.word('T',9,8,1.2).line([(17,11),(38,11)],STEEL)
    else:d.word('K' if selected==14 else 'U' if selected==25 else 'TH',8,7,1.2)
    return d


def seismic_scene(kind):
    d=Diagram().ground(11)
    if kind in {'seismic_crosshole','seismic_downhole','seismic_uphole','seismic_vsp','crosshole_seismic_tomography'}:
        left=kind in {'seismic_crosshole','crosshole_seismic_tomography','seismic_uphole'}
        d.rect(35,12,5,32,SAND,.3)
        if left:d.rect(8,12,5,32,SAND,.3)
        source=(10.5,29) if left else (8,9)
        d.circle(*source,1.7,STEEL,solid=True)
        if kind=='seismic_uphole':
            d.receiver(37,9)
            for sy in (22,34,41):d.line([(11,sy),(37,10)],INK,.9)
        else:
            for y in (20,30,40):
                d.receiver(37.5,y,1.6)
                if kind=='crosshole_seismic_tomography':
                    for sy in (19,31,42):d.line([(11,sy),(35,y)],STEEL,.8)
                else:d.line([source,(35,y)],INK,1.1)
            if kind=='seismic_vsp':
                d.line([(8,10),(22,39),(35,31)],BLUE)
                d.line([(4,40),(32,40)],SOIL)
        return d
    if kind=='seismic_refraction':
        for x in (13,25,39):d.receiver(x,9)
        d.circle(5,9,1.5,STEEL,solid=True)
        d.line([(3,32),(45,32)],SOIL,2)
        d.line([(5,11),(16,32),(31,32),(39,11)],INK)
        d.arrow(20,32,29,32)
    elif kind=='seismic_masw':
        for x in (10,19,28,37,44):d.receiver(x,9,1.4)
        for y,amp in ((20,2),(29,3),(39,4)):d.wave(4,44,y,amp,1.5,INK)
    else:
        d.rect(6,4,12,12,ALU)
        d.arrow(12,10,12,4,RED).arrow(12,10,18,10,BLUE)
        d.line([(5,43),(5,24),(44,24)],STEEL,.9)
        d.line([(8,40),(16,38),(24,29),(28,32),(33,39),(42,40)],INK)
        d.word('H',23,5,1.5).word('V',34,5,1.5)
        d.line([(23,13),(39,13)])
    return d


def borehole_scene(kind):
    d=Diagram().ground(7)
    if kind in {'crosshole_ert','crosshole_em_tomography'}:
        for x in (6,36):d.rect(x,8,6,36,SAND,.3)
        for y in (17,28,39):
            d.receiver(39,y)
            if kind=='crosshole_ert':
                d.circle(9,y,1.4,BLUE,BLUE)
                d.line([(10,y),(37,28)],BLUE,.9)
            else:
                d.coil(9,y,4,1.8,BLUE)
                d.line([(12,y),(36,17),(12,39)],RED,.9)
        return d
    # Cable, borehole wall and depth ticks remain shared, with distinct tools
    # and response graphics for each measurement principle.
    d.rect(7,8,13,36,SAND,.3).line([(13.5,4),(13.5,15)],STEEL)
    d.rect(10,15,7,20,ALU,2)
    d.line([(26,10),(26,43),(45,43)],STEEL,.9)
    for y in (15,24,33,42):d.line([(24,y),(26,y)],STEEL,.9)
    if kind in {'borehole_em_bhem','borehole_induction_log','borehole_nmr','borehole_magnetic_susceptibility'}:
        for y in (19,25,31):d.coil(13.5,y,5,1.5,BLUE if kind!='borehole_magnetic_susceptibility' else RED)
        if kind=='borehole_em_bhem':
            d.line([(3,9),(3,3),(43,3),(43,7)],BLUE)
            d.line([(28,38),(31,30),(34,17),(38,27),(42,39)],RED)
        elif kind=='borehole_induction_log':
            d.line([(29,12),(29,23),(39,25),(39,35),(30,38)],BLUE)
        elif kind=='borehole_nmr':
            d.wave(29,44,24,4,3,RED)
            d.line([(29,37),(33,35),(36,32),(39,20),(43,14)],INK)
        else:
            d.line([(29,17),(33,17),(33,25),(42,25),(42,28),(31,31),(31,40)],RED)
            d.word('K',32,7,1.2)
    elif kind in {'borehole_resistivity_log','borehole_ip_log','borehole_sp_log','borehole_fluid_conductivity'}:
        for y in ((19,31) if kind=='borehole_fluid_conductivity' else (17,23,29,34)):
            d.rect(9,y,9,1.2,STEEL,.2)
        if kind=='borehole_ip_log':
            pulse(d,29,12,13,5);decay(d,29,25,14,14,True)
        elif kind=='borehole_sp_log':
            d.word('+',30,12,.9).word('-',40,12,.9)
            d.line([(36,20),(31,25),(40,31),(34,39)],BLUE)
        elif kind=='borehole_fluid_conductivity':
            d.circle(13.5,25,1.5,WATER,solid=True)
            d.line([(30,13),(30,24),(40,28),(40,39)],BLUE)
        else:d.line([(30,12),(38,19),(31,25),(43,30),(34,39)],BLUE)
    elif kind=='borehole_magnetometer':
        d.arrow(13.5,27,13.5,17,RED).arrow(13.5,27,19,23,RED)
        d.line([(29,18),(34,20),(40,24),(32,28),(39,34),(42,39)],RED)
        d.line([(29,12),(32,16),(30,21),(38,29),(34,38)],STEEL,.9)
    elif kind in {'borehole_natural_gamma','borehole_spectral_gamma','borehole_density_log','borehole_neutron_porosity'}:
        d.circle(13.5,27,1.5,YELLOW,'#111111',True)
        d.arc(13.5,27,6,-60,60,INK)
        if kind=='borehole_spectral_gamma':
            for x,height in ((30,10),(35,17),(41,23)):d.rect(x,40-height,2.3,height,SAND,.3)
            d.word('K',29,10,.7).word('U',34,10,.7).word('TH',39,10,.6)
        elif kind=='borehole_density_log':
            d.receiver(13.5,17,1.4).receiver(13.5,34,1.4)
            d.line([(19,27),(23,22),(19,17)],INK,.9)
            d.line([(31,13),(38,18),(34,24),(41,31),(32,39)],INK)
        elif kind=='borehole_neutron_porosity':
            for x,y in ((22,20),(24,28),(21,36)):d.circle(x,y,.8,WATER,solid=True)
            d.line([(30,13),(39,20),(31,25),(37,32),(40,39)],INK)
        else:d.line([(30,12),(37,16),(31,23),(42,28),(31,34),(35,39)],INK)
    elif kind=='borehole_sonic_log':
        d.circle(13.5,31,1.4,STEEL,solid=True).receiver(13.5,18,1.4).receiver(13.5,23,1.4)
        for y,amp in ((16,1),(26,2),(36,3)):d.wave(29,44,y,amp,2,INK)
    elif kind in {'borehole_acoustic_televiewer','borehole_optical_televiewer'}:
        d.receiver(13.5,25,2)
        d.line([(16,25),(20,20),(20,30),(16,25)],BLUE if 'acoustic' in kind else STEEL)
        d.rect(29,12,15,28,ROCK,.4)
        if 'acoustic' in kind:
            d.wave(30,43,21,2,1,BLUE).wave(30,43,32,2,1,INK)
        else:
            d.line([(30,18),(43,24)],SOIL,3).line([(30,29),(43,35)],SAND,3)
            d.circle(13.5,25,.8,INK,solid=True)
    elif kind=='borehole_caliper':
        d.line([(12,23),(7,28),(12,33)]).line([(15,23),(20,28),(15,33)])
        d.line([(31,12),(31,22),(42,27),(32,31),(32,40)],INK)
    elif kind=='borehole_temperature':
        d.circle(13.5,31,2,RED,RED).line([(13.5,19),(13.5,31)],RED)
        d.line([(30,12),(32,20),(35,29),(42,40)],RED)
        d.word('T',35,10,1)
    elif kind=='borehole_flowmeter':
        d.circle(13.5,25,2,None)
        for angle in (0,120,240):
            cx,cy=13.5,25
            points=[(cx,cy),(cx+4*math.cos(math.radians(angle)),cy+4*math.sin(math.radians(angle))),(cx+2*math.cos(math.radians(angle+60)),cy+2*math.sin(math.radians(angle+60)))]
            d.poly(points,STEEL)
        d.arrow(22,36,22,17,WATER)
        d.line([(30,39),(30,28),(40,23),(40,12)],WATER)
    elif kind=='borehole_gravity':
        d.line([(13.5,17),(11,21),(16,24),(11,27),(13.5,30)])
        d.rect(11,30,5,3,STEEL,.2)
        d.line([(30,12),(32,22),(38,28),(42,39)],INK)
        d.arrow(35,6,35,13)
    else:raise ValueError(f'Unknown borehole method: {kind}')
    return d


def symbol(d, name, x=25, y=8, size=9):
    if name=='sigma':
        d.ellipse(x,y+size*.55,size*.4,size*.42)
        d.line([(x,y+size*.13),(x+size*.65,y+size*.13)])
    elif name=='rho':
        d.ellipse(x,y+size*.4,size*.38,size*.4)
        d.line([(x-size*.38,y+size*.4),(x-size*.38,y+size*1.35)])
    elif name=='chi':
        d.line([(x-size*.4,y),(x+size*.4,y+size)])
        d.line([(x+size*.4,y),(x-size*.4,y+size)])
    elif name=='phi':
        d.ellipse(x,y+size*.5,size*.4,size*.4)
        d.line([(x,y-.1*size),(x,y+size*1.1)])
    elif name=='epsilon':
        d.arc(x,y+size*.5,size*.45,70,290)
        d.line([(x-size*.45,y+size*.5),(x+size*.15,y+size*.5)])


def property_scene(kind):
    d=Diagram()
    if kind in {'property_conductivity','property_resistivity'}:
        d.rect(8,21,32,20,ROCK,1)
        d.line([(4,31),(11,31)],BLUE).line([(37,31),(44,31)],BLUE)
        d.rect(10,27,3,8,STEEL,.3).rect(35,27,3,8,STEEL,.3)
        if kind=='property_conductivity':
            d.arrow(17,31,31,31,BLUE);symbol(d,'sigma',24,4,9)
        else:
            d.line([(15,31),(18,27),(22,35),(26,27),(30,35),(33,31)],BLUE)
            symbol(d,'rho',24,3,8)
    elif kind=='property_density':
        d.poly([(25,17),(40,25),(25,34),(10,25)],ROCK)
        d.poly([(10,25),(25,34),(25,44),(10,35)],SOIL)
        d.poly([(25,34),(40,25),(40,35),(25,44)],STEEL)
        for x,y in ((16,29),(20,34),(30,35),(35,30)):d.circle(x,y,.7,INK,solid=True)
        symbol(d,'rho',24,2,8)
    elif kind in {'property_magnetic_susceptibility','property_remanent_magnetization'}:
        d.rect(12,19,25,24,ROCK)
        if kind=='property_magnetic_susceptibility':
            symbol(d,'chi',24,3,9)
            for x in (18,25,32):d.arrow(x,37,x,25,RED)
            d.arrow(5,38,5,22,RED).arrow(43,38,43,22,RED)
        else:
            d.word('M',23,3,1.5)
            d.arrow(17,38,32,24,RED).arrow(17,38,17,24,STEEL)
            d.line([(32,24),(32,38),(17,38)],STEEL,.8)
    elif kind=='property_chargeability':
        pulse(d,5,6,19,8);decay(d,27,6,15,12,True)
        d.rect(6,27,21,14,ROCK)
        d.line([(9,24),(9,35)],BLUE).line([(24,24),(24,35)],BLUE)
        d.circle(36,33,8,WHITE).line([(36,28),(36,33),(40,35)])
    elif kind in {'property_vp','property_vs'}:
        d.word('VP' if kind=='property_vp' else 'VS',17,3,1.6)
        d.arrow(5,39,43,39)
        if kind=='property_vp':
            for index,x in enumerate((6,10,13,16,24,32,35,38,42)):
                d.line([(x,21),(x,32)],STEEL,1.3)
            d.arrow(15,17,23,17,BLUE)
        else:
            d.wave(5,43,26,6,2,BLUE)
            d.arrow(24,18,24,33,BLUE)
    elif kind in {'property_porosity','property_permeability'}:
        d.rect(5,17,38,27,SAND)
        if kind=='property_porosity':
            symbol(d,'phi',24,2,9)
            for x,y,r in ((13,25,3),(31,24,4),(24,36,3.5),(37,37,2)):
                d.circle(x,y,r,WHITE)
        else:
            d.word('K',23,3,1.6)
            for x,y in ((13,24),(34,24),(12,38),(35,38)):d.circle(x,y,4,ROCK)
            d.arrow(6,31,42,31,WATER)
    elif kind=='property_dielectric_permittivity':
        symbol(d,'epsilon',24,2,9)
        d.rect(9,19,4,24,STEEL,.2).rect(35,19,4,24,STEEL,.2)
        for y in (24,36):
            d.circle(21,y,1.6,BLUE,BLUE).circle(29,y,1.6,RED,RED)
            d.line([(23,y),(27,y)],STEEL,.9)
        d.line([(4,31),(9,31)],BLUE).line([(39,31),(44,31)],BLUE)
    elif kind=='property_thermal_conductivity':
        d.word('K',23,3,1.6)
        d.rect(10,19,28,24,ROCK)
        for x in (16,24,32):d.arrow(x,39,x,23,RED)
        d.line([(5,44),(43,44)],RED,2).line([(5,17),(43,17)],BLUE,2)
    else:raise ValueError(f'Unknown property: {kind}')
    return d


# category | identifier suffix | readable name | meaning | search synonyms
CATALOG_ROWS = """
Methods|airborne_em_aem|Airborne Electromagnetics (AEM)|Aircraft-carried transmitter and receiver used to map subsurface electrical structure.|aem airborne electromagnetic helicopter induction
Methods|fixed_wing_aem|Fixed-Wing AEM & Towed Bird|Fixed-wing aircraft towing an electromagnetic receiver bird and induction coils.|aem aircraft plane towed bird airborne em
Methods|frequency_domain_em_fdem|Frequency-Domain EM (FDEM)|Separated transmitter and receiver coils driven by a continuous sinusoidal excitation.|fdem frequency domain em slingram conductivity
Methods|time_domain_em_tdem|Time-Domain EM (TDEM)|Transmitter current shutoff followed by recording the decaying secondary electromagnetic response.|tdem tem transient electromagnetic pulse decay
Methods|csem_marine|Marine Controlled-Source EM (CSEM)|A vessel tows a horizontal electric dipole above an array of seafloor receivers.|csem marine ocean seabed seafloor controlled source em
Methods|csem_land|Land Controlled-Source EM (CSEM)|Grounded electric dipole source and separated land receivers measuring controlled electromagnetic fields.|csem land terrestrial grounded dipole controlled source
Methods|csamt|Controlled-Source Audio-MT (CSAMT)|Separated transmitter and electric/magnetic field receivers for controlled-source audio-frequency magnetotellurics.|csamt controlled source audio magnetotelluric
Methods|ground_tem|Ground TEM Survey|Ground transmitter loop, receiver and transient decay response.|ground tem tdem transient electromagnetic
Methods|tem_fixed_loop|Fixed-Loop TEM|A stationary transmitter loop with receiver stations sampled around the loop.|tem flem fixed loop stationary transmitter
Methods|tem_moving_loop|Moving-Loop TEM|Transmitter loop and receiver moved along the survey line together.|tem mlem moving loop mobile transmitter
Methods|tem_central_loop|Central-Loop TEM|Receiver coil located at the centre of a ground transmitter loop.|tem central loop coincident central receiver
Methods|tem_in_loop|In-Loop TEM|Receiver positioned inside a transmitter loop, away from the central point.|tem in loop offset receiver
Methods|tem_lotem|Long-Offset TEM (LOTEM)|Grounded long-wire source and remote receiver recording transient electromagnetic fields.|lotem long offset long wire grounded source
Methods|loupe_tem|Loupe Portable TEM|Two walking operators carrying a transmitter loop and three-component receiver connected at a fixed separation.|loupe backpack portable walking mobile tem near surface
Methods|vtem|VTEM Airborne TEM|Helicopter-borne circular transmitter loop with a coincident receiver arrangement.|vtem versatile time domain electromagnetic geotech helicopter
Methods|skytem|SkyTEM Dual-Moment AEM|Helicopter-borne rigid transmitter frame, offset receiver and low/high moment pulse modes.|skytem dual moment low moment high moment rigid frame aem
Methods|slingram_em|Slingram Ground EM|Separated ground transmitter and receiver coils for electromagnetic profiling.|slingram ground em horizontal loop hlem
Methods|vlf_em|Very Low Frequency EM (VLF)|Remote radio transmitter and portable receiver used to measure very-low-frequency electromagnetic fields.|vlf very low frequency radio em
Methods|airborne_magnetics|Airborne Magnetic Survey|Aircraft and towed magnetic sensor recording the geomagnetic field along flight lines.|airborne magnetics aeromagnetic towed bird
Methods|ground_magnetics|Ground Magnetic Survey|Walking magnetometer sensor and a magnetic anomaly profile.|ground magnetics walking magnetometer total magnetic intensity tmi
Methods|magnetic_gradiometry|Magnetic Gradiometry|Two separated magnetic sensors measuring spatial magnetic-field gradients.|magnetic gradiometer gradient vertical horizontal
Methods|electrical_ip_chargeability|Time-Domain Induced Polarization|Ground electrodes with transmitter current pulse and delayed polarization voltage decay.|ip induced polarization chargeability time domain
Methods|ip_spectral|Spectral Induced Polarization (SIP)|Frequency-dependent amplitude and phase response of induced polarization.|sip spectral ip complex resistivity phase frequency
Processes|tem_decay_gates|TEM Decay & Time Gates|Transient response sampled in successive off-time windows after transmitter shutoff.|tem decay gates time channels off time transient response
Methods|gpr_b_scan|GPR Radargram / B-Scan|Profile radar image with subsurface diffraction hyperbolas and a shallow reflector.|gpr radargram b scan hyperbola profile radar
Methods|gpr_time_slice|GPR Time / Depth Slice|Plan-view radar slice highlighting linear subsurface targets.|gpr c scan time slice depth slice plan view
Methods|gpr_volume_3d|3D GPR Volume|Three-dimensional radar cube containing a mapped subsurface reflector.|gpr 3d radar volume cube reflector
Methods|gpr_cmp_velocity|GPR CMP / WARR Velocity|Variable-offset transmitter and receiver geometry for radar propagation-velocity analysis.|gpr cmp common midpoint warr velocity wide angle
Methods|gpr_utility_detection|GPR Utility Detection|Surface radar cart above buried pipes and localized diffraction responses.|gpr utilities pipes cables locator buried targets
Methods|gpr_concrete_rebar|GPR Concrete & Rebar Scan|Handheld concrete radar scanner above embedded reinforcing bars.|gpr concrete rebar reinforcement structural scan
Methods|gpr_borehole|Borehole / Crosshole Radar|Radar transmission between probes placed in adjacent boreholes.|gpr borehole radar crosshole downhole radar
Methods|gpr_antenna|GPR Shielded Antenna|Shielded radar antenna with a bow-tie element and downward electromagnetic wavefronts.|gpr shielded antenna bow tie radar transmitter
Methods|radiometrics_total|Radiometrics — Total Count|Combined natural gamma-ray response across the recorded spectrum.|radiometric gamma total count total counts tc
Methods|radiometrics_potassium_k|Radiometrics — Potassium (K)|Potassium-associated gamma spectral window within a natural radiation spectrum.|radiometric potassium k k40 gamma spectral channel
Methods|radiometrics_uranium_u|Radiometrics — Uranium (eU)|Equivalent uranium channel inferred from gamma-emitting uranium-series daughter products.|radiometric uranium u eu equivalent uranium gamma
Methods|radiometrics_thorium_th|Radiometrics — Thorium (eTh)|Equivalent thorium channel inferred from gamma-emitting thorium-series daughter products.|radiometric thorium th eth equivalent thorium gamma
Methods|radiometrics_ternary|Radiometric K–U–Th Ternary|Three-channel potassium, equivalent uranium and equivalent thorium composition diagram.|radiometric ternary k u th kut rgb gamma
Methods|airborne_radiometrics|Airborne Gamma Spectrometry|Aircraft gamma survey with potassium, uranium and thorium channels.|airborne radiometrics gamma spectrometer k u th
Methods|seismic_crosshole|Crosshole Seismic Survey|Seismic source in one borehole and receivers in a neighbouring borehole.|crosshole seismic borehole source receivers travel time
Methods|seismic_downhole|Downhole Seismic Survey|Surface seismic source and receivers deployed at increasing borehole depths.|downhole seismic borehole surface source velocity
Methods|seismic_uphole|Uphole Seismic Survey|Borehole seismic sources with receivers at the ground surface.|uphole seismic source borehole surface receivers
Methods|seismic_vsp|Vertical Seismic Profile (VSP)|Borehole receiver array recording direct and reflected waves from a surface source.|vsp vertical seismic profile downhole reflection
Methods|seismic_refraction|Seismic Refraction Survey|Surface source and receiver array recording critically refracted arrivals along an interface.|seismic refraction head wave first breaks
Methods|seismic_masw|Surface-Wave Seismics (MASW)|Multi-channel surface receiver array recording dispersive surface-wave motion.|masw sasw surface wave rayleigh dispersion shear velocity
Methods|seismic_hvsr|Passive Seismic H/V (HVSR)|Three-component passive seismic recording and a horizontal-to-vertical spectral ratio peak.|hvsr h v passive seismic microtremor resonance
Methods|borehole_em_bhem|Borehole EM (BHEM / DHEM)|Surface transmitter loop and downhole electromagnetic receiver measuring off-hole conductor response.|bhem dhem borehole em downhole em three component
Methods|borehole_induction_log|Borehole Induction Conductivity|Coaxial transmitter and receiver coils with a formation conductivity log.|downhole borehole induction conductivity log em
Methods|borehole_resistivity_log|Borehole Resistivity Log|Multi-electrode resistivity probe with a depth-dependent formation response.|downhole borehole resistivity normal laterolog electrodes
Methods|borehole_ip_log|Borehole IP Log|Downhole electrode measurements of induced-polarization voltage decay.|downhole borehole ip chargeability induced polarization
Methods|borehole_sp_log|Borehole Self-Potential (SP)|Downhole electrode and natural spontaneous-potential response versus depth.|downhole borehole sp spontaneous potential self potential
Methods|borehole_magnetic_susceptibility|Borehole Magnetic Susceptibility|Downhole coil probe measuring magnetic susceptibility of the surrounding formation.|downhole borehole mag sus susceptibility kappa chi log
Methods|borehole_magnetometer|Borehole Magnetometer|Downhole vector magnetic sensor and component logs.|downhole borehole magnetometer magnetic vector three component
Methods|borehole_natural_gamma|Borehole Natural Gamma|Downhole gamma detector and natural formation count-rate log.|downhole borehole natural gamma gr log
Methods|borehole_spectral_gamma|Borehole Spectral Gamma|Downhole gamma spectrometry separating potassium, uranium and thorium channels.|downhole borehole spectral gamma k u th
Methods|borehole_density_log|Borehole Gamma-Gamma Density|Gamma source and separated detectors used to infer formation bulk density.|downhole borehole gamma gamma density compensated density log
Methods|borehole_neutron_porosity|Borehole Neutron Porosity|Neutron-source and detector probe responding to hydrogen content and apparent porosity.|downhole borehole neutron porosity hydrogen log
Methods|borehole_sonic_log|Borehole Sonic / Full Waveform|Acoustic source and spaced receivers recording formation wave travel times and waveforms.|downhole borehole sonic acoustic full waveform p s velocity
Methods|borehole_acoustic_televiewer|Acoustic Borehole Televiewer|Rotating ultrasonic transducer and unwrapped borehole-wall image with sinusoidal fractures.|downhole borehole acoustic televiewer atv ultrasound image
Methods|borehole_optical_televiewer|Optical Borehole Televiewer|Downhole camera and illuminated optical image of the borehole wall.|downhole borehole optical televiewer otv camera image
Methods|borehole_caliper|Borehole Caliper|Extending caliper arms and a log of borehole diameter changes.|downhole borehole caliper diameter arms hole size
Methods|borehole_temperature|Borehole Temperature Log|Downhole thermometer and fluid or formation temperature variation with depth.|downhole borehole temperature geothermal thermal log
Methods|borehole_fluid_conductivity|Borehole Fluid Conductivity|Immersed electrodes measuring electrical conductivity of borehole fluid.|downhole borehole fluid conductivity resistivity water log
Methods|borehole_flowmeter|Borehole Flowmeter|Spinner-style probe and vertical flow direction through a borehole.|downhole borehole flowmeter spinner flow heat pulse
Methods|borehole_nmr|Borehole NMR Log|Downhole magnetic resonance tool and relaxation response related to pore fluids.|downhole borehole nmr nuclear magnetic resonance porosity
Methods|borehole_gravity|Borehole Gravimetry|Downhole gravimeter and changes in gravitational acceleration with depth.|downhole borehole gravity gravimetry density
Methods|crosshole_ert|Crosshole Electrical Tomography|Electrode arrays in adjacent boreholes for electrical resistivity tomography.|crosshole ert resistivity tomography borehole electrodes
Methods|crosshole_em_tomography|Crosshole EM Tomography|Electromagnetic source and receiver arrays in neighbouring boreholes.|crosshole em electromagnetic tomography borehole induction
Methods|crosshole_seismic_tomography|Crosshole Seismic Tomography|Intersecting borehole source-receiver raypaths used to reconstruct a velocity section.|crosshole seismic tomography velocity inversion raypaths
Petrophysical Quantities|property_conductivity|Electrical Conductivity|Electrical conductivity represented by sigma and current transport through a rock sample.|conductivity sigma electrical bulk formation property
Petrophysical Quantities|property_resistivity|Electrical Resistivity|Electrical resistivity represented by rho and a resistive rock sample.|resistivity rho electrical bulk rock property
Petrophysical Quantities|property_density|Bulk Density|Bulk density represented by rho and a solid rock volume.|density rho bulk mass volume rock property
Petrophysical Quantities|property_magnetic_susceptibility|Magnetic Susceptibility|Magnetic susceptibility represented by chi and induced magnetization within a sample.|mag sus magnetic susceptibility chi kappa property
Petrophysical Quantities|property_remanent_magnetization|Remanent Magnetization|Remanent magnetization represented by a retained vector in a rock sample.|remanence remanent magnetization nrm jr magnetic property
Petrophysical Quantities|property_chargeability|IP Chargeability|Electrical polarization chargeability represented by delayed voltage decay after current shutoff.|chargeability ip m polarization property
Petrophysical Quantities|property_vp|P-Wave Velocity (Vp)|Compressional-wave velocity represented by longitudinal particle motion.|vp p wave velocity compressional seismic property
Petrophysical Quantities|property_vs|S-Wave Velocity (Vs)|Shear-wave velocity represented by transverse particle motion.|vs s wave velocity shear seismic property
Petrophysical Quantities|property_porosity|Porosity|Porosity represented by phi and void spaces within a rock matrix.|porosity phi pore void fraction property
Petrophysical Quantities|property_permeability|Permeability|Permeability represented by connected flow paths through pore space.|permeability k hydraulic flow property
Petrophysical Quantities|property_dielectric_permittivity|Dielectric Permittivity|Dielectric permittivity represented by epsilon and polarization between capacitor plates.|dielectric permittivity epsilon relative dielectric gpr property
Petrophysical Quantities|property_thermal_conductivity|Thermal Conductivity|Thermal conductivity represented by heat flow through a rock sample.|thermal conductivity heat k lambda property
"""


@lru_cache(maxsize=128)
def design(kind):
    if kind.startswith('gpr_'):return gpr_scene(kind)
    if kind.startswith('radiometrics_'):return radiometric_scene(kind)
    if kind.startswith('seismic_') or kind=='crosshole_seismic_tomography':return seismic_scene(kind)
    if kind.startswith('borehole_') or kind.startswith('crosshole_'):return borehole_scene(kind)
    if kind.startswith('property_'):return property_scene(kind)
    return em_scene(kind)


def build_geometry(kind):
    return design(kind).geometry()


EXPANDED_GEOPHYSICS_ICONS = []
for offset, row in enumerate(CATALOG_ROWS.strip().splitlines()):
    category, kind, name, description, synonyms = row.split('|')
    EXPANDED_GEOPHYSICS_ICONS.append({
        'id': 'gp_'+kind, 'codepoint': 0xE0C2+offset, 'name': name,
        'domain': 'Geophysical', 'category': category,
        'description': description, 'keywords': synonyms.split(),
        'builder': partial(build_geometry, kind), 'kind': kind,
    })
EXPANDED_IDS = {icon['id'] for icon in EXPANDED_GEOPHYSICS_ICONS}


def flat_artwork(icon):
    from detailed_flat import FlatLayer
    drawing=design(icon['kind'])
    native_ink=drawing.geometry()
    cleaned=native_ink.buffer(.65,quad_segs=4,join_style=1).buffer(-.65,quad_segs=4,join_style=1)
    x0,y0,x1,y1=cleaned.bounds
    factor=880/max(x1-x0,y1-y0)

    def convert(geometry):
        geometry=native(geometry)
        geometry=affinity.translate(geometry,xoff=-(x0+x1)/2,yoff=-(y0+y1)/2)
        geometry=affinity.scale(geometry,xfact=factor,yfact=factor,origin=(0,0))
        geometry=affinity.translate(geometry,xoff=500,yoff=500)
        geometry=affinity.scale(geometry,xfact=24/1000,yfact=-24/1000,origin=(0,0))
        return affinity.translate(geometry,yoff=24)

    layers=[]
    for part in drawing.parts:
        if part.face is not None and part.fill is not None:
            layers.append(FlatLayer(convert(part.face),part.fill))
        layers.append(FlatLayer(convert(part.ink),part.colour))
    return layers
