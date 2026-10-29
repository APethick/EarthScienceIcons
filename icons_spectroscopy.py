"""Spectroscopy artwork; append-only IDs, with shared colour/font geometry."""
import math
from functools import lru_cache, partial
from shapely.geometry import Polygon
from icons_geophysics_expanded import Diagram, BLUE, RED, WATER, GLASS, STEEL, SAND, ROCK, INK, WHITE


def label(d, text, x, y, scale=1):
    # Additional stroked capitals used by spectral-region abbreviations.
    extra = {
        'I': [[(0,0),(3,0)],[(1.5,0),(1.5,5)],[(0,5),(3,5)]],
        'W': [[(0,0),(.6,5),(1.5,3),(2.4,5),(3,0)]],
        'L': [[(0,0),(0,5),(3,5)]],
        'B': [[(0,5),(0,0),(2,0),(3,1),(3,2),(0,2.5),(3,3),(3,4),(2,5),(0,5)]],
        'D': [[(0,5),(0,0),(2,0),(3,1),(3,4),(2,5),(0,5)]],
        'G': [[(3,1),(2,0),(0,1),(0,4),(2,5),(3,4),(3,2.5),(1.8,2.5)]],
        'X': [[(0,0),(3,5)],[(3,0),(0,5)]],
    }
    for i, ch in enumerate(text):
        if ch in extra:
            for pts in extra[ch]:
                d.line([(x+(i*4.5+px)*scale,y+py*scale) for px,py in pts],INK,.85*scale)
        else:
            d.word(ch,x+i*4.5*scale,y,scale)


def spectrum(d, region=None):
    colours = ['#8064a8','#527eb8','#548965','#bc9362','#a46f56','#986f80']
    if region is not None:
        # Selected wavelength window; curve remains visible over the window.
        x = 6 + region * 5.8
        d.rect(x,17,5.8,22,colours[region],.1,colours[region])
    d.line([(5,16),(5,40),(43,40)],INK,1.1)
    points=[]
    for i in range(145):
        x=6+i*.25
        y=24+2*math.sin(x/7)+9*math.exp(-((x-18)/2.1)**2)+6*math.exp(-((x-31)/1.6)**2)
        points.append((x,y))
    d.line(points,INK,1.35)
    # Sampling marks express a recorded spectrum rather than an unmeasured wave.
    for x,y in points[::18]:d.circle(x,y,.7,WHITE,INK)


@lru_cache(maxsize=32)
def design(kind):
    d=Diagram()
    if kind == 'gibbs':
        # Header and plot occupy disjoint areas. Minimum sits on the curve.
        d.poly([(7,10),(10,4),(13,10)],None,INK)
        label(d,'G',16,4,1.1)
        d.line([(5,15),(5,42),(43,42)],INK,1.2)
        points=[(8+i*.23,35-19*((8+i*.23-29)/22)**2) for i in range(145)]
        d.line(points,BLUE,1.5)
        d.circle(29,35,1.25,BLUE,BLUE,True)
        d.arrow(29,25,29,32,INK)
    elif kind == 'water':
        # Cubic Bezier silhouette: symmetric shoulders, rounded bowl, sharp tip.
        def bezier(a,b,c,e):
            return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*e[0],
                     (1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*e[1]) for t in [i/40 for i in range(41)]]
        pts=bezier((24,3),(21,13),(10,22),(11,31))
        pts+=bezier((11,31),(12,46),(36,46),(37,31))[1:]
        pts+=bezier((37,31),(38,22),(27,13),(24,3))[1:]
        d.poly(pts,WATER,INK)
        d.line([(16,28),(15.5,31),(17,35)],WHITE,1.8)
        # Activity a, placed inside the broad bowl.
        d.circle(25,31,3,None,INK).line([(28,28),(28,35)],INK,1.2)
    elif kind == 'xrd':
        label(d,'XRD',3,3,.9)
        # Powder sample and symmetric incident/diffracted beam geometry.
        d.rect(4,15,7,6,STEEL,.5)
        d.rect(37,15,7,6,STEEL,.5)
        d.arrow(11,21,23,33,BLUE).arrow(25,33,37,21,RED)
        d.rect(17,34,14,2.5,ROCK,.2)
        d.arc(24,33,13,205,335,STEEL)
        # Separate diffractogram in the top-right inset.
        pts=[]
        for i in range(101):
            x=21+i*.22
            y=13-sum(h*math.exp(-((x-c)/w)**2) for c,h,w in [(26,7,.45),(32,4,.55),(39,6,.45)])
            pts.append((x,y))
        d.line(pts,INK,.9).line([(21,14),(44,14)],INK,.7)
    elif kind == 'lab':
        label(d,'LAB',4,3,.9)
        d.rect(5,13,12,11,STEEL,1).circle(11,19,3,GLASS)
        d.line([(11,24),(11,35)],INK,1.5)
        d.rect(4,36,25,4,STEEL,.5)
        d.poly([(16,34),(20,29),(26,32),(25,36)],SAND)
        for x,col in [(18,BLUE),(22,'#548965'),(26,RED)]:d.line([(15,23),(x,29)],col,.9)
        d.rect(31,19,13,15,GLASS,1)
        d.line([(33,28),(35,25),(37,29),(39,23),(42,24)],INK,.8)
    elif kind == 'satellite':
        d.rect(19,5,10,10,STEEL,1)
        for x in (4,31):
            d.rect(x,6,13,8,'#527eb8',.2)
            for offset in (4,8):d.line([(x+offset,6),(x+offset,14)],WHITE,.5)
        d.poly([(23,16),(8,36),(39,36),(25,16)],GLASS,STEEL)
        d.poly([(6,36),(37,36),(43,42),(12,42)],SAND)
        for i,col in enumerate((BLUE,'#548965',RED)):
            d.line([(13+i*6,37),(18+i*6,41)],col,2)
        d.circle(24,15,2,INK,INK,True)
    elif kind == 'cube':
        for offset,col in [(8,'#a46f56'),(4,'#548965'),(0,'#527eb8')]:
            d.poly([(6+offset,16-offset),(28+offset,16-offset),(28+offset,38-offset),(6+offset,38-offset)],col)
        for x in (13,20):d.line([(x,16),(x,38)],WHITE,.6)
        for y in (23,30):d.line([(6,y),(28,y)],WHITE,.6)
        d.line([(36,7),(41,4),(41,26)],INK,1)
    elif kind == 'bands':
        label(d,'BANDS',3,3,.8)
        for i,col in enumerate(('#8064a8','#527eb8','#548965','#bc9362','#a46f56','#986f80')):
            d.rect(5+i*6.5,16,4.5,23,col,.2)
        d.line([(4,41),(44,41)],INK,1)
    else:
        names={'spectrum':'SPECTRA','uv':'UV','visible':'VIS','vnir':'VNIR',
               'nir':'NIR','ir':'IR','swir':'SWIR','mwir':'MWIR','tir':'TIR'}
        label(d,names[kind],5,4,.85)
        selected={'uv':0,'visible':1,'vnir':2,'nir':2,'swir':3,'mwir':4,'tir':5}.get(kind)
        spectrum(d,selected)
        # VNIR spans visible and NIR; broad IR has its own labelled window.
        if kind=='vnir':d.line([(12,44),(23,44)],BLUE,2)
        if kind=='ir':d.line([(18,44),(42,44)],RED,2)
    return d


def build_geometry(kind):
    return design(kind).geometry()


ROWS = [
    ('lab','Laboratory Hyperspectral Spectroscopy','Sample illumination, spectrometer and recorded spectrum.'),
    ('satellite','Satellite Hyperspectral Imaging','Orbital imaging spectrometer acquiring contiguous spectral channels over a ground swath.'),
    ('cube','Hyperspectral Data Cube','Spatial image pixels with a stack of measured wavelength channels.'),
    ('bands','Hyperspectral Band Selection','Contiguous narrow spectral channels selected along a wavelength axis.'),
    ('spectrum','Recorded Spectral Signature','Sampled reflectance spectrum with diagnostic absorption features.'),
    ('uv','Ultraviolet Spectroscopy (UV)','Ultraviolet spectral-region selection; wavelength limits depend on instrument.'),
    ('visible','Visible Spectroscopy (VIS)','Visible spectral-region selection.'),
    ('vnir','Visible–Near Infrared Spectroscopy (VNIR)','Combined visible and near-infrared reflectance spectroscopy.'),
    ('nir','Near Infrared Spectroscopy (NIR)','Near-infrared spectral-region selection.'),
    ('ir','Infrared Spectroscopy (IR)','Broad infrared spectroscopy; instrument determines wavelength coverage.'),
    ('swir','Shortwave Infrared Spectroscopy (SWIR)','Shortwave infrared reflectance spectroscopy with mineral absorption features.'),
    ('mwir','Midwave Infrared Spectroscopy (MWIR)','Midwave infrared spectral-region selection.'),
    ('tir','Thermal Infrared Spectroscopy (TIR / LWIR)','Thermal infrared spectral-region selection for emitted-radiance and emissivity measurements.'),
]
SPECTROSCOPY_ICONS = [dict(id='gp_hyperspectral_'+kind,codepoint=0xE1D8+i,name=name,
    domain='Geophysical',category='Methods',description=desc,
    keywords=['hyperspectral','spectroscopy','spectrum',kind],kind=kind,builder=partial(build_geometry,kind))
    for i,(kind,name,desc) in enumerate(ROWS)]
SPECTROSCOPY_IDS = {icon['id'] for icon in SPECTROSCOPY_ICONS}
REPLACEMENTS = {'gc_gibbs_free_energy':'gibbs','gc_water_activity_ah2o':'water','gc_xrd_diffractometer':'xrd'}


def flat_artwork(icon):
    from icons_geophysics_expanded import flat_artwork as render
    return render(icon,design(REPLACEMENTS.get(icon['id'],icon.get('kind'))))
