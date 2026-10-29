"""Detailed field equipment and geological scale compositions, shared by SVG and font."""
import math
from shapely.geometry import Polygon, Point, LineString, box
from shapely import affinity
from em_artwork import Equipment, place, aircraft, controller, terrain
from icons_geophysics_expanded import INK, STEEL, ALU, SAND, ROCK, BLUE, RED, YELLOW, GLASS, WHITE, SOIL

class Detail(Equipment):
    def line(self, points, colour=INK, width=.65):
        return super().line(points,colour,width)
    def shape(self, geometry, fill=None, colour=INK, width=.65, solid=False):
        return super().shape(geometry,fill,colour,width,solid)

COLS=['#d7c5a3','#b99a7d','#899b8b','#b8afb2','#d4b5a0']
def texture(d, region, step=4, colour=INK):
    for i,x in enumerate(range(3,47,step)):
        for y in range(5,47,step):
            p=Point(x+.7*(i%2),y+1.3*(i%3))
            if region.contains(p.buffer(.8)):
                d.line([(p.x-.5,p.y+.35),(p.x+.5,p.y-.35)],colour,.4)

def scalebar(d):
    d.line([(5,44),(17,44)],INK,.8)
    for x in (5,11,17): d.line([(x,42.8),(x,44.8)],INK,.65)

def rock(d,x=0,y=0,scale=1):
    a=Detail(); pts=[(6,28),(9,15),(18,8),(30,10),(41,21),(39,33),(28,40),(13,37)]
    a.poly(pts,ROCK); a.poly([(9,15),(18,8),(30,10),(33,23),(23,29),(6,28)],'#b5b4a9')
    a.line([(23,29),(28,40)]); a.line([(33,23),(41,21)])
    for px,py in [(14,17),(22,13),(27,21),(13,26),(31,31),(22,34),(35,26),(11,32)]:
        a.poly([(px-1,py),(px,py-2),(px+2,py-1),(px+1,py+2)],SAND,INK)
    for px,py in [(18,21),(25,18),(17,31),(33,15),(36,30)]: a.line([(px,py),(px+1.5,py+1)],INK,.9)
    return place(d,a,x,y,scale)

def geology(k):
    d=Detail()
    if k in ('pore','grain'):
        disk=Point(24,23).buffer(19,quad_segs=72)
        d.shape(disk,GLASS if k=='pore' else WHITE)
        centers=[(8,9),(20,7),(34,8),(43,17),(31,21),(18,20),(6,24),(10,38),(24,35),(39,36),(24,46)]
        # Voronoi mineral fabric clipped to the microscope field of view.
        from shapely import voronoi_polygons
        from shapely.geometry import MultiPoint
        cells=voronoi_polygons(MultiPoint(centers),extend_to=box(0,0,48,48))
        for i,cell in enumerate(cells.geoms):
            g=cell.intersection(disk).buffer(-.8 if k=='pore' else -.3)
            if g.is_empty: continue
            d.shape(g,COLS[i%len(COLS)])
            if k=='grain' and i%3==0:
                for yy in range(3,45,2):
                    line=LineString([(0,yy),(48,yy+13)]).intersection(g.buffer(-.8))
                    if not line.is_empty: d.shape(line.buffer(.17),INK,INK,solid=True)
        if k=='pore':
            for x,y in [(13,17),(24,27),(35,30)]: d.circle(x,y,1.2,BLUE,BLUE,True)
        scalebar(d)
    elif k=='specimen': rock(d,1,0,.95); scalebar(d)
    elif k=='outcrop':
        outline=Polygon([(3,36),(6,20),(11,18),(13,11),(20,9),(27,13),(33,8),(40,12),(44,25),(45,38),(33,40),(17,39)])
        d.shape(outline,SAND)
        for i in range(5):
            band=Polygon([(0,15+i*5),(48,6+i*5),(48,9+i*5),(0,18+i*5)]).intersection(outline)
            if not band.is_empty: d.shape(band,COLS[i%5],INK,.55)
        for x in (12,23,34):
            g=LineString([(x,5),(x-2,23),(x+1,42)]).intersection(outline)
            d.shape(g.buffer(.3),INK,INK,solid=True)
        texture(d,outline,5)
        for x,y in [(7,40),(29,42),(41,41)]: d.poly([(x-2,y),(x,y-2),(x+2,y)],ROCK)
        scalebar(d)
    elif k in ('structure','deposit','crust'):
        # Consistent cutaway block: geological front, top surface and depth face.
        d.poly([(4,15),(16,6),(44,12),(34,21)],'#c5c5a8')
        d.poly([(34,21),(44,12),(44,34),(34,43)],'#9b978d')
        face=Polygon([(4,15),(34,21),(34,43),(4,37)])
        d.shape(face,SAND)
        if k=='structure':
            def boundary(x,i): return 26+i*3.4-8*math.exp(-((x-17)/7)**2)+.2*(x-4)
            for i in range(4):
                xs=[4+j*.5 for j in range(61)]
                band=Polygon([(x,boundary(x,i)) for x in xs]+[(x,boundary(x,i+1)) for x in reversed(xs)]).intersection(face)
                d.shape(band,COLS[i],INK,.65)
            d.line([(25,20),(20,40)],INK,1.1)
            for yy in (26,33): d.line([(26,yy),(24,yy+3),(26,yy+2)],RED,.65)
            for y in (12,15,18): d.line([(7,y+3),(17,y-5),(38,y+1)],INK,.5)
        elif k=='deposit':
            for yy in (23,29,35): d.line([(4,yy),(34,yy+6)],INK,.6)
            ore=Polygon([(15,39),(16,31),(22,22),(24,18),(28,22),(25,29),(24,41)])
            halo=ore.buffer(2).intersection(face); d.shape(halo,'#c3a1a1',SOIL,.5)
            d.shape(ore.intersection(face),'#a88758')
            texture(d,ore,3)
            for x in (12,20,29): d.line([(x,11+x*.13),(x+2,24),(x-1,34)],STEEL,.7)
            d.line([(7,13),(15,9),(20,10),(29,17)],RED,.9)
        else:
            # Thickened crustal root beneath an orogenic mountain belt.
            d.poly([(4,15),(10,14),(15,6),(19,11),(23,8),(29,18),(34,21),(34,27),(25,25),(18,18),(11,21),(4,22)],'#b4afa2')
            d.poly([(4,28),(11,29),(17,35),(23,38),(29,34),(34,34),(34,43),(4,37)],'#bd8e74')
            d.line([(4,28),(11,29),(17,35),(23,38),(29,34),(34,34)],INK,1)
            for yy in (23,26): d.line([(5,yy),(11,yy+1),(17,yy+6),(22,yy+8)],INK,.5)
            texture(d,face,5)
        scalebar(d)
    elif k=='district':
        field=Polygon([(4,8),(41,5),(44,38),(7,42)])
        d.shape(field,'#e4dfc8')
        for i in range(5):
            pts=[(3+j*.7,12+i*5+3*math.sin(j*.16+i)) for j in range(60)]
            g=LineString(pts).intersection(field); d.shape(g.buffer(.22),SOIL,SOIL,solid=True)
        d.line([(10,7),(15,16),(26,24),(29,39)],RED,.9)
        d.line([(40,10),(31,18),(34,27),(25,36),(15,39)],BLUE,.7)
        for x,y in [(15,16),(26,24),(29,33)]:
            d.poly([(x-2,y-1),(x,y-3),(x+3,y),(x+1,y+2)],'#ae8559')
        d.arrow(7,18,7,10,INK); scalebar(d)
    return d

def curved_outline(start, segments):
    points=[start]
    for c1,c2,end in segments:
        p0=points[-1]
        for j in range(1,21):
            t=j/20;u=1-t
            points.append((u**3*p0[0]+3*u*u*t*c1[0]+3*u*t*t*c2[0]+t**3*end[0],
                           u**3*p0[1]+3*u*u*t*c1[1]+3*u*t*t*c2[1]+t**3*end[1]))
    return points


def tool(k):
    d=Detail()
    if k=='hammer':
        # Trace the user reference proportions: near-horizontal left pick,
        # short square right face, flared forged shoulder and long blue grip.
        def outline(start, segments):
            points=[start]
            for c1,c2,end in segments:
                p0=points[-1]
                for j in range(1,17):
                    t=j/16;u=1-t
                    points.append((u*u*u*p0[0]+3*u*u*t*c1[0]+3*u*t*t*c2[0]+t*t*t*end[0],
                                   u*u*u*p0[1]+3*u*u*t*c1[1]+3*u*t*t*c2[1]+t*t*t*end[1]))
            return [(8.5+x*.125, .5+y*.115) for x,y in points]
        steel=outline((12,49),[
            ((62,35),(113,26),(169,29)),
            ((183,29),(194,30),(205,30)),
            ((208,37),(207,47),(205,56)),
            ((194,59),(181,57),(171,52)),
            ((156,45),(145,52),(139,59)),
            ((134,70),(133,92),(132,111)),
            ((131,133),(131,157),(136,181)),
            ((127,184),(118,184),(109,180)),
            ((114,150),(115,123),(115,96)),
            ((115,77),(114,64),(106,57)),
            ((92,42),(68,45),(12,49)),
        ])
        d.poly(steel,'#a4aaad')
        # Restrained forged bevel: preserve broad uninterrupted steel surfaces.
        d.line([(10.4,5.9),(18,4.1),(25,4),(33.6,4.3)],ALU,.45)
        d.line([(24.1,8.2),(23.9,14),(23.4,20.5)],ALU,.55)
        d.line([(33.9,4.3),(34.0,6.7)],STEEL,.65)
        grip=outline((109,177),[
            ((118,178),(128,179),(136,177)),
            ((139,201),(140,230),(140,260)),
            ((140,302),(141,344),(146,374)),
            ((147,384),(104,385),(98,378)),
            ((98,372),(100,361),(101,350)),
            ((106,309),(107,260),(106,231)),
            ((105,208),(107,190),(109,177)),
        ])
        d.poly(grip,'#2879b7')
        # Recessed grip dimples, not transverse bands or a wooden handle.
        for row in range(10):
            for col in range(2):
                x=22.6+col*1.65+(row%2)*.25;y=25+row*1.75
                oval=affinity.scale(Point(x,y).buffer(1,quad_segs=12),.25,.44,origin=(x,y))
                oval=affinity.rotate(oval,20,origin=(x,y))
                d.shape(oval,'#18517f',INK,.15)
        d.line([(22.1,23),(21.8,30),(21.7,38)],'#69a5cf',.35)
    elif k=='compass':
        # Mirrored sighting compass on a long transparent baseplate, in perspective.
        def plate(u,v): return (21+21*u-13*v, 21+5*u+19*v)
        def ring_points(radius, count=120):
            return [plate(.5+.43*radius*math.cos(i*math.tau/count),
                          .39+.34*radius*math.sin(i*math.tau/count)) for i in range(count)]
        # Hinged lid: black moulded frame, silver mirror and central sighting line.
        d.poly(curved_outline((21.5,21),[
            ((21,16),(21.5,7),(22,4)),((22.1,2.4),(23.1,2),(25,2.5)),
            ((30,2.8),(37,4),(42,5)),((44,5.5),(44.3,6.8),(44,9)),
            ((44,15),(43.7,21),(43,26)),((37,24.5),(29,23),(21.5,21))]),'#34383a')
        d.poly([(23.5,5),(42,7.3),(41.4,23),(24,19.8)],'#d5d5d2')
        d.poly([(23.5,5),(26,5.3),(25,20),(24,19.8)],STEEL)
        d.line([(33,6.2),(32.7,21.3)],INK,.3)
        # A restrained reflection in the lower mirror identifies the mirror itself.
        d.arc(33,23,6.5,190,335,STEEL)
        d.line([(29,21.5),(32,18),(35,22)],RED,.35)
        d.line([(23,4),(31,5),(32,4.8),(32.4,3.5)],ALU,.4)
        # Baseplate has thickness, a long ruler edge and a circular magnifier.
        d.poly([plate(0,0),plate(1,0),plate(1,1),plate(0,1)],GLASS)
        d.poly([plate(0,1),plate(1,1), (plate(1,1)[0],plate(1,1)[1]+.9),
                (plate(0,1)[0],plate(0,1)[1]+.9)],ALU)
        for u in (.08,.48,.9):
            x,y=plate(u,0);d.poly([(x-1,y-1.2),(x+1,y-.7),(x+.5,y+1),(x-1.5,y+.5)],ALU)
        for i in range(21):
            for u in (0,1):
                v=i/20;x,y=plate(u,v);xx,yy=plate(u+(.07 if u==0 else -.07)*(1 if i%5==0 else .55),v)
                d.line([(x,y),(xx,yy)],RED,.23)
        d.poly(ring_points(1.13),'#34383a')
        d.poly(ring_points(1.03),ALU)
        d.poly(ring_points(.91),WHITE)
        for i in range(60):
            t=i*math.tau/60
            p1=plate(.5+.43*(.99 if i%5 else .94)*math.cos(t),.39+.34*(.99 if i%5 else .94)*math.sin(t))
            p2=plate(.5+.43*.86*math.cos(t),.39+.34*.86*math.sin(t))
            d.line([p1,p2],INK,.22 if i%5 else .4)
        for u in (.34,.5,.66):d.line([plate(u,.17),plate(u,.62)],RED,.22)
        d.poly([plate(.5,.12),plate(.55,.39),plate(.5,.43),plate(.45,.39)],RED)
        d.poly([plate(.5,.68),plate(.45,.39),plate(.5,.35),plate(.55,.39)],INK)
        x,y=plate(.5,.39);d.ellipse(x,y,1.05,.65,STEEL)
        x,y=plate(.24,.8);d.ellipse(x,y,2.9,1.65,None,STEEL)
        d.poly([plate(.49,.95),plate(.43,.84),plate(.55,.87)],RED)
        d.line([plate(.65,.82),plate(.82,.86)],INK,.5)
    elif k=='clinometer':
        d.rect(5,8,37,31,ALU,4); d.rect(8,11,31,25,WHITE,2)
        d.arc(23,17,15,5,175)
        for a in range(10,180,10):
            t=math.radians(a); r=12 if a%30==0 else 13.5
            d.line([(23+r*math.cos(t),17+r*math.sin(t)),(23+15*math.cos(t),17+15*math.sin(t))],INK,.45)
        d.line([(9,17),(37,17)],INK,.5); d.line([(23,17),(29,30)],RED,1)
        d.circle(23,17,1.2,STEEL); d.rect(9,4,9,4,STEEL,.5); d.rect(30,4,9,4,STEEL,.5)
        d.line([(42,17),(46,20),(45,32),(42,33)],INK,.8)
    elif k=='hand_lens':
        # Parallel circular rims share one projected plane; their displacement is
        # the cylinder axis. The swivel cover is projected in that same plane.
        def project(u,v): return (17+.88*u-.18*v,27+.12*u+.82*v)
        def circular(radius,du=0,dv=0):
            return Polygon([project(du+radius*math.cos(i*math.tau/160),
                                    dv+radius*math.sin(i*math.tau/160)) for i in range(160)])
        front=circular(12)
        rear=affinity.translate(front,xoff=4,yoff=-6)
        barrel=front.union(rear).convex_hull
        d.shape(barrel,'#64717b',INK,.65)
        # Rear rim and side-wall seam follow the same circular projection.
        rear_arc=[project(12*math.cos(t),12*math.sin(t)) for t in [math.pi+i*math.pi/80 for i in range(81)]]
        d.line([(x+4,y-6) for x,y in rear_arc],ALU,.6)
        d.shape(front,ALU,INK,.65)
        d.shape(circular(10.9),STEEL,INK,.4)
        d.shape(circular(10.1),GLASS,INK,.45)
        d.line([project(-7,-4),project(-8,0),project(-7,4)],WHITE,.65)
        # Cover is a rounded shield, turned about its upper hinge in the lens plane.
        cover=curved_outline((5,-12),[
            ((9,-14),(16,-13),(20,-10)),((24,-7),(23,-2),(21,4)),
            ((20,8),(17,12),(12,12)),((8,12),(5,9),(4,4)),
            ((3,0),(3,-8),(5,-12))])
        d.poly([project(u,v) for u,v in cover],'#c7ced0',INK)
        d.line([project(8,-11.8),project(15,-11),project(19,-9)],WHITE,.6)
        d.line([project(5,3),project(7,8),project(11,10)],STEEL,.45)
        d.shape(circular(2,6,-9),STEEL,INK,.4)
        d.shape(circular(1.3,6,-9),ALU,INK,.3)
        d.line([project(5,-9.7),project(7,-8.3)],INK,.45)
        d.line([project(5.3,-8),project(6.7,-10)],INK,.45)
    elif k=='field_notebook':
        d.poly([(8,7),(34,4),(39,8),(39,42),(12,45),(8,41)],'#9aab8c')
        d.poly([(12,10),(36,7),(36,39),(12,42)],WHITE)
        for y in range(13,39,4): d.line([(16,y),(33,y-2)],STEEL,.35)
        for y in range(12,40,5): d.ellipse(10,y,2,1.1,None,INK)
        d.line([(19,25),(24,19),(29,23),(32,18)],INK,.8)
        d.poly([(40,12),(43,13),(40,36),(38,40),(37,36)],YELLOW)
    elif k=='streak_plate':
        d.poly([(4,18),(29,10),(43,25),(19,35)],WHITE)
        d.poly([(4,18),(19,35),(43,25),(43,28),(19,38),(4,21)],ALU)
        for i in range(4): d.line([(12+i,21+i*.4),(28+i,17+i*.4)],'#985c4e',.7)
        rock(d,25,24,.38)
    elif k=='sample_bag':
        d.poly([(10,7),(37,7),(36,16),(40,40),(35,44),(10,43),(7,38),(11,17)],'#eee7cc')
        d.line([(11,12),(36,12)]); d.line([(11,16),(36,16)],STEEL,.5)
        for x in (13,18,25,32): d.line([(x,17),(x-1,21)],SOIL,.5)
        d.rect(15,20,17,10,WHITE,.5); d.line([(18,23),(29,23)],INK,.5); d.line([(18,26),(26,26)],INK,.5)
        d.line([(11,30),(14,39),(19,41)],SOIL,.6); rock(d,18,27,.28)
    elif k=='measuring_tape':
        # Compact retractable tape: rubber case, side lock, steel blade and bent hook.
        rubber='#353a3c';yellow='#f3ba29'
        # Wrist strap passes behind the case and retains a clear opening.
        d.line([(9,25),(5,22),(2.5,24),(2,29),(5,33),(14,34),(14,29)],rubber,1.5)
        # Back/side housing establishes the depth of the moulded case.
        d.poly(curved_outline((11,12),[
            ((16,6),(22,6),(27,9)),((32,12),(33,17),(33,23)),
            ((33,28),(31,32),(32,36)),((27,37),(20,33),(13,32)),
            ((9,27),(8,17),(11,12))]),rubber)
        d.poly(curved_outline((25,11),[
            ((29,10),(31,15),(31,20)),((30,23),(30,26),(29,28)),
            ((26,27),(25,24),(24.5,20)),((24,16),(23,13),(25,11))]),yellow)
        d.poly(curved_outline((10,12),[
            ((15,8),(22,9),(26,15)),((30,21),(29,28),(26,32)),
            ((23,36),(17,36),(12,32)),((6,28),(6,18),(10,12))]),rubber)
        face=affinity.rotate(affinity.scale(Point(18,23).buffer(1,quad_segs=64),9,11,origin=(18,23)),-20,origin=(18,23))
        d.shape(face,yellow,INK,.65)
        d.shape(affinity.scale(face,.82,.82,origin=(18,23)),rubber,INK,.45)
        d.shape(affinity.scale(face,.65,.65,origin=(18,23)),'#555b5d',INK,.4)
        d.line([(14,17),(20,18),(23,23)],STEEL,.5)
        d.poly([(12,25),(20,27),(22,31),(16,31)],yellow)
        # Lock button on the upper-right shoulder, with tactile dimples.
        d.poly([(27,17),(30.8,19),(31,23),(27.5,22)],'#61676b')
        for x,y in [(28,18.5),(29.5,19.3),(28.4,20.4),(30,21)]:d.circle(x,y,.25,INK,INK,True)
        for x,y in [(12,11),(16,9),(23,11)]:d.circle(x,y,.55,STEEL)
        d.poly([(27,30),(32,29),(32,35),(28,34)],rubber)
        # One affine surface defines both blade edges and all printed/mechanical detail.
        def blade(u,v):
            return (29.5+16*u-v, 31+5*u+3*v)
        d.poly([blade(0,0),blade(1,0),blade(1,1),blade(0,1)],yellow)
        for i in range(21):
            u=i/20
            depth=.64 if i%5==0 else .4 if i%2==0 else .24
            d.line([blade(u,0),blade(u,depth)],INK,.24)
        d.line([blade(0,1),blade(1,1)],INK,.35)
        d.poly([blade(.7,.12),blade(1,.12),blade(1,.9),blade(.7,.9)],rubber)
        for u in (.76,.85,.94):
            pts=[blade(u+.018*math.cos(t*math.tau/32),.5+.15*math.sin(t*math.tau/32)) for t in range(32)]
            d.shape(Polygon(pts),ALU,INK,.18)
        # Bent end tab shares the exact blade end points.
        top=blade(1,0);bottom=blade(1,1)
        d.poly([top,(top[0]+.7,top[1]+.2),(bottom[0]+.7,bottom[1]+3),
                (bottom[0]-.2,bottom[1]+3.6),bottom],STEEL)
        d.ellipse(bottom[0]+.25,bottom[1]+1.5,.28,.55,ALU)
    return d

def equipment(k):
    d=Detail()
    if k=='tempest':
        # Airframe-mounted transmitter loop and separate three-component towed receiver.
        place(d,aircraft(),1,-1,.88)
        d.line([(21.7,1),(4.5,17.5),(22,27),(39,17.5),(21.7,1)],RED,.6)
        d.line([(23,27),(24,31),(34,35)],STEEL,.65)
        d.poly([(25,36),(40,36),(45,38),(40,40),(25,40),(22,38)],YELLOW,INK)
        for x in (28,33,38): d.ellipse(x,38,1,1.8,None,INK)
        d.poly([(35,36),(36,32),(39,36)],ALU); terrain(d,45)
    else:
        # Enclosed coil housings: the real instruments are not open hoops.
        if k=='em31':
            d.poly([(3,29),(44,20),(45,23),(4,32)],ALU)
            for x,y in [(3,28),(40,20)]:
                d.poly([(x,y),(x+4,y-1),(x+5,y+4),(x+1,y+5)],'#e1c65c')
                d.line([(x+1,y),(x+2,y+4)],STEEL,.6)
            place(d,controller(),19,16,.85)
            d.line([(22,16),(20,9),(26,8),(29,15)],INK,.9)
            d.line([(17,21),(13,11),(15,6),(19,7),(26,16)],STEEL,.8)
        else:
            d.poly([(5,27),(37,17),(43,21),(11,32)],'#d0c16d')
            d.poly([(11,32),(43,21),(43,27),(11,38)],'#b4a255')
            d.poly([(5,27),(11,32),(11,38),(5,33)],ALU)
            for x,y in [(12,26),(34,19)]: d.line([(x,y),(x+5,y+4),(x+5,y+9)],INK,.7)
            d.poly([(20,22),(20,16),(26,14),(30,17),(30,20)],ALU)
            d.poly([(21.5,21),(21.5,17),(26,15.5),(28,17),(28,19)],WHITE)
            d.poly([(14,28),(19,26),(22,28),(17,30)],GLASS)
            for x in (24,27,30): d.circle(x,27-(x-24)*.3,.5,INK,INK,True)
        terrain(d,43)
    return d

def design(kind):
    if kind.startswith('scale_'): return geology(kind[6:])
    if kind in ('em31','em38','tempest'): return equipment(kind)
    return tool(kind)
