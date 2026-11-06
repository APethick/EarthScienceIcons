"""Magnetic-field and wave concepts on the shared 48-unit canvas."""
import math
from functools import lru_cache, partial
from field_detail import Detail
from icons_geophysics_expanded import INK, RED, BLUE, WATER, SAND, SOIL, WHITE

def seismic_block(kind):
    d=Detail()
    def point(u,v,w):
        phase=u*math.tau*2.15
        du=dv=dz=0
        if kind=='p': du=.026*math.sin(phase)
        if kind=='s': dz=2.4*math.sin(phase)
        if kind=='love': dv=.16*math.sin(phase)*math.exp(-3*w)
        if kind=='rayleigh':
            dz=2.4*math.sin(phase)*math.exp(-2*w)
            du=.035*math.cos(phase)*math.exp(-2*w)
        return (3+37*(u+du)+6*(v+dv),20-7*(v+dv)+13*w+dz)
    def path(axis, value, face):
        return [point(t,value,0) if face=='top' and axis=='u' else
                point(value,t,0) if face=='top' else
                point(t,0,value) if axis=='u' else point(value,0,t)
                for t in (i/100 for i in range(101))]
    # Rear end, front face and top surface share the deformed lattice.
    d.poly([point(1,0,0),point(1,1,0),point(1,1,1),point(1,0,1)],'#b6d3df','#286c92')
    d.poly(path('u',0,'front')+list(reversed(path('u',1,'front'))),'#e0edf2','#286c92')
    d.poly(path('u',0,'top')+list(reversed(path('u',1,'top'))),'#c7d8a0','#286c92')
    for i in range(22):
        for face in ('top','front'): d.line(path('v',i/21,face),'#286c92',.28)
    for j in range(5):
        for face in ('top','front'): d.line(path('u',j/4,face),'#286c92',.3)
    d.arrow(5,40,43,40,'#bd442e')
    if kind=='p':
        d.arrow(12,9,18,9,'#bd442e'); d.arrow(28,9,22,9,'#bd442e')
    elif kind=='s':
        d.arrow(24,9,24,3,'#bd442e'); d.arrow(24,9,24,14,'#bd442e')
    elif kind=='love':
        d.arrow(17,13,20,8,'#bd442e'); d.arrow(30,8,27,13,'#bd442e')
    else:
        d.ellipse(25,27,3.5,4.5,None,'#bd442e')
        d.arrow(28.4,26,27.4,23.8,'#bd442e')
    return d

@lru_cache(maxsize=None)
def design(kind):
    if kind in ('igrf','magnetosphere'):
        from magnetic_field_traces import design as traced_field
        return traced_field(kind)
    if kind in ('p','s','love','rayleigh'): return seismic_block(kind)
    d=Detail()
    if kind=='plane':
        for offset in (0,7,14,21):
            d.poly([(5+offset,17),(12+offset,7),(19+offset,24),(12+offset,34)],'#dcebf2','#397ea6')
            for j in (1,2,3):
                t=j/4
                d.line([(5+offset+7*t,17-10*t),(12+offset+7*t,34-10*t)],'#6eabc2',.35)
        d.arrow(5,41,44,41,INK)
        return d
    if kind=='diffraction':
        for x in (3,8,13): d.line([(x,6),(x,41)],BLUE,.7)
        d.rect(18,3,3,17,'#8f989e',.1); d.rect(18,27,3,17,'#8f989e',.1)
        for radius in (6,12,18,24): d.arc(20,23.5,radius,-58,58,BLUE)
        d.arrow(3,45,14,45,INK)
        return d
    if kind in ('reflection','refraction'):
        d.poly([(3,24),(39,24),(45,19),(9,19)],'#b9d6df','#6c8b9d')
        d.poly([(3,24),(39,24),(39,41),(3,41)],'#decca7',SOIL)
        d.poly([(39,24),(45,19),(45,36),(39,41)],'#b8a383',SOIL)
        for x in range(6,39,6): d.line([(x,35),(x+2,36)],SOIL,.4)
        for y in (4,9,14,19,26,31,36): d.line([(23,y),(23,y+2)],INK,.4)
        d.arrow(6,5,23,24,BLUE)
        if kind=='reflection': d.arrow(23,24,39,6,BLUE)
        else: d.arrow(23,24,31,40,BLUE)
        # Wavefront ticks perpendicular to the incident and outgoing rays.
        for x,y in ((10,10),(15,16)): d.line([(x-2,y+2),(x+2,y-2)],BLUE,.55)
        d.arc(23,24,6,225,270,INK)
        return d
    if kind=='tube':
        d.poly([(4,4),(44,4),(44,43),(4,43)],'#d6c19a',SOIL)
        for y in (10,20,32): d.line([(4,y),(44,y+3)],SOIL,.6)
        d.rect(17,3,14,41,'#a4d3df',.2,INK)
        d.line([(19,4),(19,43)],'#6a7c88',.6); d.line([(29,4),(29,43)],'#6a7c88',.6)
        for y in (10,18,26,34):
            d.ellipse(24,y,4.5,1.8,None,BLUE)
            d.arrow(17,y,14,y,RED); d.arrow(31,y,34,y,RED)
        d.arrow(24,5,24,40,BLUE)
        for x in (7,39):
            for y in (7,16,26,37): d.line([(x,y),(x+1,y+1)],SOIL,.4)
        return d
    raise ValueError(f"Unknown field/wave concept: {kind}")

ROWS = [
 ('gp_igrf','International Geomagnetic Reference Field (IGRF)','Gridded globe, tilted magnetic axis and meridional dipole loops representing the reference geomagnetic field.','igrf'),
 ('gp_magnetosphere','Magnetosphere','Earth surrounded by magnetic field lines compressed on the sunward side and extended into a tail.','magnetosphere'),
 ('gp_plane_wave','Plane Wave','Parallel gridded phase planes perpendicular to the propagation direction.','plane'),
 ('gp_wave_diffraction','Wave Diffraction','Plane wavefronts spread after passing through an aperture.','diffraction'),
 ('gp_wave_reflection','Wave Reflection','Incident and reflected rays at an interface.','reflection'),
 ('gp_seismic_p_wave','P Wave','Gridded three-dimensional block with alternating compression and expansion parallel to propagation.','p'),
 ('gp_seismic_s_wave','S Wave','Transverse seismic wave with particle motion perpendicular to propagation.','s'),
 ('gp_seismic_love_wave','Love Wave','Surface wave with horizontal transverse motion concentrated near the surface.','love'),
 ('gp_seismic_rayleigh_wave','Rayleigh Wave','Surface wave with elliptical particle motion.','rayleigh'),
 ('gp_seismic_tube_wave','Tube Wave','Guided wave travelling along a fluid-filled borehole.','tube'),
]
ICONS = [dict(id=i, codepoint=0xE215+n, name=name, domain='Geophysical', category='Methods', description=desc, keywords=[name, 'wave' if 'wave' in i else 'magnetic', kind], group='Fields and waves', kind=kind, builder=partial(lambda k: design(k).geometry(), kind)) for n,(i,name,desc,kind) in enumerate(ROWS)]
IDS = {icon['id'] for icon in ICONS}
def flat_artwork(icon):
    from icons_geophysics_expanded import flat_artwork as render
    return render(icon, design(icon['kind']))
