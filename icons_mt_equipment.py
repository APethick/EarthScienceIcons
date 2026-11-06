"""Magnetotelluric acquisition units, based on field equipment references."""
from functools import lru_cache, partial
from field_detail import Detail
from icons_geophysics_expanded import INK, STEEL, ALU, GLASS, BLUE, RED, WHITE

def mtu_reference(kind):
    """Trace in reference-photo pixels, then uniformly fit the whole case.

    Connector centres remain in photo coordinates so they can be overlaid for QA.
    MTU-5C reference: 688x445; MTU-8A reference: 1001x666.
    """
    from shapely.geometry import Polygon, Point, box
    from em_artwork import place
    d = Detail()
    metal = '#bfc3b8'
    brass = '#c7a052'
    def poly(points, fill):
        d.shape(Polygon(points), fill, INK, 4)
    def rect(x,y,w,h,fill,r=8):
        d.shape(box(x+r,y+r,x+w-r,y+h-r).buffer(r),fill,INK,4)
    def circle(x,y,r,fill,stroke=INK,width=4):
        d.shape(Point(x,y).buffer(r,quad_segs=24),fill,stroke,width)
    def line(points,width=4,colour=INK):
        d.line(points,colour,width)
    def cap(x,y,r,tether=True):
        circle(x-4,y-3,r+3,'#92988e')
        circle(x,y,r,metal)
        circle(x+3,y+2,4,'#dce0d5',STEEL,2)
        if tether:
            line([(x+3,y+2),(x-2,y+25),(x-15,y+45),(x-30,y+48),(x-34,y+35)],3)
    def terminal(x,y,colour):
        circle(x-5,y-2,13,brass,width=3)
        circle(x,y,10,colour,'#ebce80',3)
    if kind == 'mtu5c':
        # Top/left volume and front perimeter follow the supplied image.
        poly([(75,84),(94,45),(135,33),(432,31),(552,76),(582,101),
              (177,121),(174,382),(132,363),(76,280)],'#939e94')
        poly([(95,64),(135,33),(432,31),(552,76),(177,94)],'#aab3a7')
        poly([(176,102),(216,91),(555,87),(590,113),(607,171),
              (618,311),(596,361),(550,379),(202,391),(170,373),(153,320),(155,155)],metal)
        # E1/E2 are paired terminals on black rectangular plates.
        rect(274,108,98,56,INK,3); rect(382,107,96,56,INK,3)
        for x,colour in ((320,'#dd4835'),(360,INK),(429,'#dd4835'),(467,INK)):
            terminal(x,145,colour)
        terminal(519,136,INK)
        cap(558,140,17,False)
        circle(215,141,24,STEEL); circle(215,141,17,metal)
        line([(215,125),(215,154)],3)
        rect(201,181,71,130,'#d3d5cc',5); circle(253,251,13,STEEL)
        rect(290,194,112,85,INK,12)
        cap(486,242,38,False)
        circle(215,343,24,STEEL); circle(215,343,16,metal)
        cap(294,344,29); cap(390,337,29); cap(481,323,26)
        cap(555,339,17,False)
        line([(489,243),(501,294),(512,349),(482,386),(454,401),(451,387)],3)
        # Integral end grips, rather than an invented outer rectangular frame.
        line([(166,150),(171,177),(171,312),(162,333)],14,'#a1aaa0')
        line([(597,159),(609,177),(609,304),(600,326)],14,'#a1aaa0')
        bounds=(65,25,630,415)
    else:
        poly([(55,176),(68,153),(113,139),(830,136),(915,149),
              (958,181),(956,478),(898,513),(139,526),(92,460),(55,386)],'#8f998e')
        poly([(123,145),(178,139),(874,139),(923,154),(961,198),
              (969,449),(936,493),(891,517),(171,527),(137,506),(124,467),(124,199)],metal)
        # All centres below are read directly from the MTU-8A photo.
        rect(434,166,117,70,INK,4); rect(617,167,119,70,INK,4)
        for x,colour in ((503,'#dd4835'),(553,INK),(694,'#dd4835'),(742,INK),(800,'#e8dfad')):
            terminal(x,204,colour)
        circle(220,205,31,STEEL); circle(220,205,22,metal)
        line([(220,183),(220,224)],4)
        rect(188,257,83,164,'#d0d2c7',7); circle(248,338,16,STEEL)
        for x,y in ((369,202),(365,334),(366,464),(877,202),(870,325),(855,454)):
            cap(x,y,38)
        rect(617,277,133,109,INK,12); rect(632,291,101,80,'#657897',4)
        cap(490,456,51,False)
        cap(608,455,22,False); cap(750,455,23,False)
        circle(221,461,28,STEEL); circle(221,461,19,metal)
        line([(144,206),(151,240),(151,447),(143,475)],17,'#a1aaa0')
        line([(946,210),(959,238),(959,438),(944,472)],17,'#a1aaa0')
        bounds=(45,126,985,544)
    x0,y0,x1,y1=bounds
    scale=42/(x1-x0)
    return place(Detail(),d,3-x0*scale,24-(y0+y1)*scale/2,scale)

@lru_cache(maxsize=None)
def design(kind):
    d = Detail()
    if kind == 'v8':
        # Upright computer/logger with display, keyboard and top connectors.
        d.rect(7, 7, 34, 35, STEEL, 1.5)
        d.rect(9, 9, 30, 17, INK, .8)
        d.rect(11, 11, 26, 13, GLASS, .4)
        for x in (14, 20, 26, 32):
            d.line([(x, 14), (x+2, 14)], STEEL, .35)
        d.rect(10, 28, 28, 11, '#48555b', .5)
        for y in (30, 32.5, 35, 37.5):
            for x in (12, 15, 18, 21, 24, 27, 30, 33, 36):
                d.rect(x, y, 1.4, 1, ALU, .1)
        for x, colour in ((12, STEEL), (18, '#bd352b'), (24, STEEL), (30, '#bd352b'), (36, INK)):
            d.circle(x, 7, 1.1, colour)
        d.line([(8, 11), (4, 11), (4, 4)], INK, 1)
        d.line([(17, 6), (17, 3), (20, 2), (22, 3), (22, 6)], INK, 1)
    elif kind in ('mtu5c', 'mtu8a'):
        return mtu_reference(kind)
    elif kind == 'adu07':
        # Lid, panel and base share the same hinge and perspective axes.
        orange = '#d64b26'
        d.poly([(4,7),(28,2),(30,21),(6,26)], orange)
        d.poly([(6,9),(26.5,4.8),(28,19.5),(7.5,23.8)], '#b83820')
        d.line([(7.5,23.8),(6,9),(26.5,4.8)], '#ef7947', .4)
        for x,y in ((7,6.4),(23,3.1)):
            d.poly([(x,y),(x-.3,y-2),(x+3,y-2.7),(x+3.3,y-.7)], orange)
        # Small white identification label inside the lid.
        d.poly([(7,10),(14,8.6),(14.3,10.4),(7.3,11.8)], WHITE)
        d.line([(8,10.6),(12.8,9.6)], STEEL, .25)
        d.poly([(6,26),(30,21),(44,34),(20,39)], orange)
        d.poly([(6,26),(20,39),(20,42),(6,29)], '#9d361f')
        d.poly([(20,39),(44,34),(44,37),(20,42)], '#bf3c20')
        def panel(u,v):
            return (6+24*u+14*v,26-5*u+13*v)
        def panel_shape(points,fill,colour=INK,width=.45):
            from shapely.geometry import Polygon
            d.shape(Polygon([panel(u,v) for u,v in points]),fill,colour,width)
        panel_shape([(.06,.07),(.94,.07),(.94,.91),(.06,.91)], '#8cabb9')
        panel_shape([(.2,.22),(.48,.22),(.48,.53),(.2,.53)], INK)
        panel_shape([(.22,.24),(.46,.24),(.46,.46),(.22,.46)], '#29454f')
        x,y=panel(.4,.46); d.ellipse(x,y,.65,.45,WHITE)
        panel_shape([(.36,.6),(.5,.6),(.5,.69),(.36,.69)], '#5f879b')
        # Two raised panel handles, aligned with the sloping instrument panel.
        for u in (.12,.84):
            d.line([panel(u,.29),panel(u,.18),panel(u,.63),panel(u,.74)],ALU,.85)
        for u,v in ((.1,.13),(.9,.13),(.1,.85),(.9,.85)):
            x,y=panel(u,v); d.ellipse(x,y,.35,.25,STEEL)
        # Front carry handle is orange and has a clear open centre.
        from shapely.geometry import Polygon
        handle=Polygon([(27,40),(28,44),(41,41),(42,37),(40,37.5),(39.5,39.5),(29.5,42),(29,39.5)])
        d.shape(handle,orange,INK,.45)
        # Metal connector rail on the left side of the lower case.
        d.poly([(6.2,28.5),(18,39.5),(18,41),(6.2,30)], ALU)
        for x,y in ((8,31),(11,33.8),(14,36.6)):
            d.ellipse(x,y,.65,.85,INK,STEEL)
    else:
        # ADU-10e: broad low case, fixed top cover and vertical front panel.
        d.poly([(6,11),(33,11),(41,25),(9,25)], '#aeb9bd')
        d.poly([(8,12.5),(32,12.5),(38.5,23),(10,23)], '#687d84')
        d.poly([(6,11),(9,25),(9,35),(6,30)], '#87969b')
        d.poly([(9,25),(41,25),(41,35),(9,35)], '#a9b9c0')
        d.line([(9,25),(41,25)], ALU, 1)
        for i in range(6):
            d.ellipse(11+i*.4,14+i*1.3,.3,.16,WHITE)
            d.line([(12.5+i*.4,14+i*1.3),(15+i*.4,14+i*1.3)], '#405b6a', .22)
        # Actual socket colours: silver bezels, dark inserts and pale pins.
        for x,y in ((13,28),(19,28),(25,28),(31,28),
                    (14.5,32),(20.5,32),(26.5,32),(32.5,32)):
            d.ellipse(x,y,1.25,1.05,ALU,INK)
            d.ellipse(x,y,.8,.65,INK,INK)
            for dx,dy in ((-.3,-.2),(.3,-.2),(0,.3)):
                d.ellipse(x+dx,y+dy,.13,.12,'#e4d8a3','#e4d8a3')
        for y in (28,32):
            d.ellipse(37,y,1.35,1.1,ALU,STEEL)
            d.line([(36.3,y+.1),(37.7,y-.1)],STEEL,.35)
        # Protective metal end handles project ahead of the front panel.
        d.line([(9,26),(6,28),(6,38),(9,35)],STEEL,1.2)
        d.line([(41,26),(45,29),(44,38),(40,35)],STEEL,1.2)
    return d

ROWS = [
    ('gp_mt_v8', 'Phoenix V8 Magnetotelluric System', 'Upright V8 acquisition computer with display, keyboard and connectors.', 'v8'),
    ('gp_mt_mtu_5c', 'Phoenix MTU-5C Magnetotelluric Receiver', 'Compact MTU-5C receiver with electric and magnetic input connectors.', 'mtu5c'),
    ('gp_mt_mtu_8a', 'Phoenix MTU-8A Magnetotelluric Receiver', 'Wide MTU-8A receiver with display and multiple magnetic input connectors.', 'mtu8a'),
    ('gp_mt_adu_07', 'Metronix ADU-07 Magnetotelluric Unit', 'ADU-07 acquisition unit in an open orange field case.', 'adu07'),
    ('gp_mt_adu_10e', 'Metronix ADU-10e Magnetotelluric Unit', 'Low-profile ADU-10e acquisition unit with front sockets and side handles.', 'adu10e'),
]
ICONS = [dict(id=identifier, codepoint=0xE210+i, name=name, domain='Geophysical', category='Methods', description=description, keywords=[name, 'magnetotelluric', 'equipment', kind], group='MT instruments', kind=kind, builder=partial(lambda k: design(k).geometry(), kind)) for i, (identifier, name, description, kind) in enumerate(ROWS)]
IDS = {icon['id'] for icon in ICONS}
def flat_artwork(icon):
    from icons_geophysics_expanded import flat_artwork as render
    return render(icon, design(icon['kind']))

