"""Seismic acquisition equipment and EM field-process illustrations."""
import math
from functools import partial
from field_detail import Detail, texture
from em_artwork import place, terrain, controller
from icons_geophysics_expanded import INK, STEEL, ALU, SAND, ROCK, BLUE, RED, YELLOW, GLASS, WHITE, SOIL

BLACK='#111111'
def waves(d,x=24,y=35):
    for r in (5,9,13): d.arc(x,y,r,25,155,SOIL)
def wheel(d,x,y,r=4):
    d.circle(x,y,r,'#53595c');d.circle(x,y,r*.5,ALU)
    for a in range(0,360,60):
        t=math.radians(a);d.line([(x+r*.68*math.cos(t),y+r*.68*math.sin(t)),(x+r*.92*math.cos(t+.1),y+r*.92*math.sin(t+.1))],ALU,.4)
def spike(d,x,y,s=1):
    a=Detail();a.poly([(-1.4,5),(1.4,5),(0,17)],STEEL,BLACK)
    a.rect(-4,-4,8,10,YELLOW,1,BLACK);a.ellipse(0,-4,4,1.5,YELLOW,BLACK)
    a.line([(-3,3),(3,3)],BLACK,.5);a.rect(-1,-7,2,2,STEEL,.2,BLACK)
    place(d,a,x,y,s)

def source(k):
    d=Detail()
    if k=='hammer':
        d.poly([(10,7),(13,5),(29,29),(26,31)],'#ae8962')
        d.poly([(21,27),(27,23),(36,34),(30,38)],STEEL)
        d.line([(24,28),(30,35)],ALU,.6)
        d.poly([(20,38),(36,38),(39,40),(18,40)],ALU)
        d.line([(15,30),(18,33)],RED,.8);d.line([(37,29),(35,32)],RED,.8)
        waves(d,28,39)
    elif k=='explosive':
        terrain(d,15);d.rect(21,15,5,22,SAND,.1)
        d.rect(21.8,28,3.4,7,RED,.4);d.line([(23.5,28),(23.5,11),(13,8)],INK,.6)
        place(d,controller(),3,4,.8)
        for r in (6,11,16): d.arc(24,33,r,10,170,SOIL)
        for x,y in [(17,29),(31,29),(18,37),(31,38)]:d.line([(24,33),(x,y)],RED,.7)
    elif k=='betsy':
        # External powder-actuated source silhouette; no mechanism or loading diagram.
        d.poly([(18,9),(23,7),(28,31),(23,33)],STEEL)
        d.rect(15,6,10,4,ALU,.6);d.line([(15,7),(10,9),(11,15)],INK,1)
        d.line([(24,10),(32,7),(35,8)],INK,1)
        d.poly([(17,34),(29,31),(33,35),(20,38)],STEEL)
        d.line([(14,14),(10,29),(19,35)],ALU,1)
        terrain(d,38);waves(d,25,37)
    elif k in ('weight_drop_ute','weight_drop_skid','vibroseis'):
        if k=='weight_drop_ute':
            d.poly([(3,24),(7,22),(10,14),(19,14),(23,22),(36,22),(36,32),(3,32)],'#b6c5ce')
            d.poly([(10,16),(17,16),(20,22),(8,22)],GLASS)
            d.line([(22,23),(22,31)],INK,.6);d.rect(24,20,12,5,STEEL,.2)
            wheel(d,10,32);wheel(d,30,32)
            d.line([(37,34),(37,8),(43,8),(43,34)],INK,1)
            d.rect(38,15,4,8,STEEL,.3);d.arrow(40,24,40,30,RED)
            d.rect(35,35,10,2,ALU,.2)
        elif k=='weight_drop_skid':
            d.rect(4,28,29,10,'#50575a',4);wheel(d,11,33,3.4);wheel(d,26,33,3.4)
            d.poly([(7,27),(8,13),(22,10),(28,27)],YELLOW)
            d.poly([(11,14),(20,13),(24,25),(10,25)],GLASS)
            for x in (13,17,21):d.line([(x,14),(x,24)],INK,.5)
            d.line([(7,27),(28,21),(35,29)],STEEL,2)
            d.line([(34,34),(34,8),(42,8),(42,34)],INK,1)
            d.rect(35,15,6,9,STEEL,.3);d.arrow(38,25,38,31,RED);d.rect(32,36,13,2,ALU,.2)
        else:
            d.poly([(3,18),(9,14),(15,14),(18,21),(44,21),(44,31),(3,31)],YELLOW)
            d.poly([(6,18),(13,16),(16,21),(6,21)],GLASS)
            d.rect(22,13,20,8,STEEL,.5)
            for x in range(25,41,3):d.line([(x,15),(x,19)],INK,.45)
            wheel(d,9,32,4.5);wheel(d,38,32,4.5)
            d.line([(21,23),(21,35)],STEEL,2);d.line([(28,23),(28,35)],STEEL,2)
            d.rect(20,27,9,6,ALU,.3);d.rect(17,36,15,2,STEEL,.2)
            d.wave(19,30,42,1.4,2,RED)
        terrain(d,39)
    elif k=='evibe':
        d.rect(11,35,25,3,STEEL,.5)
        d.line([(13,35),(13,7),(34,7),(34,35)],ALU,1.7)
        d.rect(17,14,13,18,STEEL,2);d.rect(20,9,7,5,ALU,.7)
        for y in (18,21,24,27):d.line([(18,y),(29,y)],INK,.6)
        d.line([(23,32),(23,35)],INK,1.6)
        d.rect(2,23,7,10,YELLOW,.8);d.line([(9,25),(11,22),(17,22)],INK,.7)
        d.wave(12,36,43,2,2,RED);terrain(d,39)
    elif k in ('airgun','sparker','boomer'):
        d.wave(3,45,7,1,3,BLUE)
        d.line([(8,8),(12,16),(24,18)],STEEL,.8)
        if k=='airgun':
            d.poly([(12,18),(33,18),(38,21),(33,25),(12,25),(9,21)],STEEL)
            for x in (15,21,28):d.rect(x,17,2,9,ALU,.2)
            d.circle(29,26,3,None,BLUE);d.circle(31,32,5,None,BLUE)
            for r in (10,15):d.arc(29,26,r,25,150,BLUE)
        elif k=='sparker':
            d.rect(12,16,25,4,ALU,.4)
            for x in (15,20,25,30,35):
                d.line([(x,20),(x,27)],STEEL,1)
                d.line([(x,28),(x-1,31),(x+1,32),(x,35)],BLUE,.7)
            for r in (10,15):d.arc(24,27,r,30,150,BLUE)
        else:
            d.ellipse(25,21,14,4,ALU);d.ellipse(25,24,11,3,STEEL)
            for r in (8,13,18):d.arc(25,24,r,20,160,BLUE)
    elif k=='land_streamer':
        d.line([(3,9),(9,13),(44,37)],STEEL,1)
        for x,y in [(12,15),(22,22),(32,29),(42,36)]:
            d.poly([(x-5,y+2),(x+1,y-1),(x+5,y+2),(x-1,y+5)],ALU)
            d.rect(x-2,y-2,4,5,YELLOW,.6,BLACK)
        d.line([(4,34),(18,39),(32,42),(44,44)],SOIL,.6)
    return d

def receiver(k):
    d=Detail()
    if k=='spiked':spike(d,24,20,1.5)
    elif k=='wired':
        d.line([(2,13),(9,11),(17,13),(26,11),(35,14),(46,12)],BLACK,.7)
        for x,y in [(9,24),(24,23),(39,24)]:
            d.line([(x,12),(x+3,17),(x,20)],BLACK,.6);spike(d,x,y,.72)
    elif k=='wireless':
        d.rect(12,16,24,20,YELLOW,3,BLACK);d.rect(17,20,14,7,GLASS,.7,BLACK)
        d.circle(20,31,1,STEEL,BLACK);d.circle(28,31,1,STEEL,BLACK)
        d.line([(32,16),(32,9)],BLACK,1);d.arc(32,9,5,220,320,BLACK);d.arc(32,9,9,220,320,BLACK)
        d.poly([(22,36),(26,36),(24,45)],STEEL,BLACK)
    elif k=='quantum':
        d.poly([(9,15),(15,9),(34,9),(40,16),(38,30),(29,34),(13,31)],YELLOW,BLACK)
        d.poly([(15,9),(34,9),(37,15),(12,15)],'#f6dc73',BLACK)
        d.rect(17,18,15,9,YELLOW,1,BLACK)
        d.circle(25,13,1,STEEL,BLACK);d.poly([(22,33),(27,33),(24,46)],STEEL,BLACK)
        for x in (13,35):d.line([(x,19),(x,28)],BLACK,.6)
    elif k=='smartsolo':
        d.poly([(14,10),(32,10),(35,15),(34,34),(30,38),(16,38),(12,33),(12,15)],YELLOW,BLACK)
        d.ellipse(23,11,9,3,WHITE,BLACK)
        d.line([(13,18),(34,18)],BLACK,.65);d.line([(16,20),(16,33)],BLACK,.5);d.line([(30,20),(30,33)],BLACK,.5)
        d.rect(19,21,8,8,WHITE,.5,BLACK);d.poly([(21,38),(25,38),(23,46)],STEEL,BLACK)
    elif k=='wing':
        d.poly([(6,22),(15,10),(33,10),(42,22),(36,34),(12,34)],YELLOW,BLACK)
        d.poly([(15,13),(32,13),(36,22),(31,29),(16,29),(12,22)],YELLOW,BLACK)
        d.circle(24,20,3,ALU,BLACK);d.circle(24,20,1,STEEL,BLACK)
        for x in (12,36):d.circle(x,24,.8,INK,BLACK)
        d.poly([(22,34),(26,34),(24,45)],STEEL,BLACK)
    elif k=='geospace':
        d.rect(6,10,28,25,YELLOW,3,BLACK);d.rect(11,14,18,16,YELLOW,1,BLACK)
        d.line([(14,10),(14,6),(26,6),(26,10)],BLACK,1)
        for x,y in [(9,13),(31,13),(9,32),(31,32)]:d.circle(x,y,.7,STEEL,BLACK)
        d.line([(34,18),(40,18),(43,24)],BLACK,.8);spike(d,41,31,.65)
    elif k=='three_component':
        spike(d,24,27,1)
        d.arrow(24,15,24,4,BLACK);d.arrow(24,15,9,12,BLACK);d.arrow(24,15,36,7,BLACK)
        d.ellipse(24,33,15,5,None,SOIL)
    elif k=='hydrophone':
        d.wave(3,45,8,1,3,BLUE);d.line([(24,9),(24,18)],BLACK,.9)
        d.rect(18,18,12,20,YELLOW,4,BLACK)
        for y in (23,27,31):d.line([(19,y),(29,y)],BLACK,.55)
        for r in (8,13):d.arc(24,27,r,200,340,BLUE)
    return d

def em(k):
    d=Detail()
    if k=='loop_field':
        # Dipolar meridian loops: upward through the centre, downward outside.
        for offset,rx,ry in [(7,6,13),(10,9,19)]:
            for sign in (-1,1):
                cx=24+sign*offset
                d.ellipse(cx,24,rx,ry,None,RED)
                outer=cx+sign*rx
                d.arrow(outer,21,outer,27,RED)
        d.ellipse(24,26,14,4,None,STEEL)
        d.line([(10,27),(6,32),(8,35)],STEEL,.8)
        d.arrow(24,32,24,12,RED)
    else:
        d.poly([(3,12),(14,6),(45,12),(35,18)],'#ddd2b9')
        d.line([(3,12),(3,41),(35,47),(45,40),(45,12)],SOIL,.65)
        d.ellipse(24,12,8,2.7,None,STEEL)
        # Expanding induced-current rings diffuse downwards and outwards after shutoff.
        for y,rx,ry in [(22,10,3),(31,14,4),(40,18,5)]:
            d.ellipse(24,y,rx,ry,None,BLUE)
            d.arrow(24+rx*.4,y+ry*.9,24-rx*.1,y+ry,BLUE)
        d.arrow(5,19,5,33,INK)
    return d

SOURCES=[('hammer','Sledgehammer Seismic Source'),('explosive','Buried Explosive Seismic Source'),('betsy','Betsy Gun Seismic Source'),('weight_drop_ute','Ute-Mounted Weight Drop'),('weight_drop_skid','Skid-Steer Weight Drop'),('evibe','Electric Seismic Vibrator (eVibe)'),('vibroseis','Vibroseis Truck'),('airgun','Marine Air Gun'),('land_streamer','Land Streamer'),('sparker','Marine Sparker'),('boomer','Marine Boomer')]
RECEIVERS=[('spiked','Spiked Geophone'),('wired','Wired Geophone String'),('wireless','Wireless Seismic Recorder'),('quantum','INOVA Quantum Node'),('smartsolo','SmartSolo IGU Node'),('wing','Sercel WiNG Node'),('geospace','Geospace Recorder with Geophone'),('three_component','Three-Component Geophone'),('hydrophone','Hydrophone')]
ROWS=[('gp_seismic_source_'+k,n,k,source,'Seismic sources') for k,n in SOURCES]+[('gp_seismic_receiver_'+k,n,k,receiver,'Seismic receivers') for k,n in RECEIVERS]+[('gp_loop_magnetic_field','Magnetic Field Around a Loop','loop_field',em,'EM field processes'),('gp_em_smoke_ring','Propagating EM Smoke Ring','smoke_ring',em,'EM field processes')]
ICONS=[dict(id=identifier,codepoint=0xE1FA+i,name=name,domain='Geophysical',category='Methods' if fun!=em else 'Processes',description=(name+'. Equipment illustration; schematic proportions.' if fun!=em else 'Closed magnetic flux around a current loop.' if k=='loop_field' else 'Induced current rings expanding and diffusing downwards after transmitter shutoff.'),keywords=[name,k.replace('_',' '),group],group=group,kind=k,builder=partial(lambda f,k:f(k).geometry(),fun,k)) for i,(identifier,name,k,fun,group) in enumerate(ROWS)]
IDS={icon['id'] for icon in ICONS}
def flat_artwork(icon):
    from icons_geophysics_expanded import flat_artwork as render
    fun=next(row[3] for row in ROWS if row[0]==icon['id'])
    return render(icon,fun(icon['kind']))
