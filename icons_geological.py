"""
Geological Icon Definitions (15 icons):
- 5 Methods
- 5 Earth Model Types
- 5 Processes
Canvas: 1000 x 1000 (x: 60..940, y: 60..940).
"""

import math
from typing import Dict, Any, List
from geom_utils import (
    union_all,
    diff,
    intersect,
    circle,
    ring,
    disk_ring,
    rect,
    rect_outline,
    rounded_rect,
    rounded_rect_outline,
    poly,
    regular_poly,
    stroke,
    line,
    dashed_line,
    arc,
    sector,
    ellipse,
    ellipse_outline,
    arrow_head,
    arrow,
    curved_arrow,
    sine_wave,
)


def gl_strike_dip_mapping():
    """Structural Strike & Dip Mapping: Compass-clinometer ring containing a bold geological strike-and-dip symbol and North tick."""
    cx, cy = 500, 500
    # Strike line rotated at 35 degrees, length 520; dip tick perpendicular (pointing SE at -55 deg)
    ang = math.radians(55)
    dx, dy = math.cos(ang), math.sin(ang)
    px, py = dy, -dx  # perpendicular (SE)
    parts = [
        # Outer compass bezel ring & cardinal ticks
        disk_ring(cx, cy, 400, 38),
        poly([(500, 945), (450, 825), (550, 825)]),  # North pointer triangle
        line(500, 65, 500, 135, 30),
        line(65, 500, 135, 500, 30),
        line(865, 500, 935, 500, 30),
        # Strike line across center
        line(cx - dx * 275, cy - dy * 275, cx + dx * 275, cy + dy * 275, 48),
        # Dip tick perpendicular to strike line + dip direction arrowhead/triangle
        line(cx, cy, cx + px * 195, cy + py * 195, 46),
        poly(
            [
                (cx + px * 225, cy + py * 225),
                (cx + dx * 85, cy + dy * 85),
                (cx - dx * 85, cy - dy * 85),
            ]
        ),
    ]
    return union_all(parts)


def gl_diamond_core_drilling():
    """Diamond Core Drilling: Core barrel bit with annular cutting crown extracting cylindrical rock core + core box below."""
    parts = [
        # Inclined or vertical diamond core barrel & inner rock core cylinder (top two-thirds)
        # Outer drill casing walls
        rect(220, 460, 290, 910),
        rect(710, 460, 780, 910),
        # Diamond-impregnated annular bit teeth at bottom of barrel (y=390..460)
        poly([(210, 460), (315, 460), (295, 385), (210, 385)]),
        poly([(685, 460), (790, 460), (790, 385), (705, 385)]),
        # Recovered cylindrical rock core inside barrel with inclined bedding/vein fractures
        rect_outline(375, 410, 625, 880, 32),
        line(375, 730, 625, 650, 28),
        line(375, 570, 625, 490, 28),
        # Core tray box at bottom holding logged core runs
        rect_outline(110, 90, 890, 310, 34),
        line(110, 200, 890, 200, 26),
        line(420, 200, 445, 310, 26),
        line(680, 200, 705, 310, 26),
        line(310, 90, 335, 200, 26),
        line(590, 90, 615, 200, 26),
    ]
    return union_all(parts)


def gl_thin_section_petrography():
    """Thin-Section Optical Petrography: Circular polarized microscope field of view with crosshairs and interlocking mineral crystals."""
    cx, cy, r = 500, 500, 400
    # Interlocking crystal grain boundaries inside circular FOV
    grains = [
        # Euhedral hexagonal/prismatic phenocryst in center-left with cleavage lines
        poly([(240, 620), (430, 680), (480, 480), (330, 360), (200, 440)]),
        # Twinned plagioclase lath on right (outlined + albite twin lamellae)
        stroke([(530, 720), (790, 640), (710, 310), (460, 390)], 30, closed=True),
        line(595, 700, 515, 370, 24),
        line(665, 678, 585, 348, 24),
        line(730, 658, 650, 328, 24),
        # Triple-junction groundmass grain boundaries
        line(480, 480, 500, 100, 28),
        line(430, 680, 500, 900, 28),
        line(200, 440, 100, 410, 28),
        # Crossed polars (XPL) ocular reticle ticks around rim
        line(500, 70, 500, 195, 32),
        line(500, 805, 500, 930, 32),
        line(70, 500, 195, 500, 32),
        line(805, 500, 930, 500, 32),
        disk_ring(cx, cy, r, 40),
    ]
    # Cut cleavage lines inside the solid phenocryst so it reads as a distinct mineral grain
    cleavage = union_all([line(250, 560, 450, 520, 24), line(230, 480, 440, 440, 24)])
    return diff(union_all(grains), cleavage)


def gl_stratigraphic_logging():
    """Measured Stratigraphic Column: Vertical lithostratigraphic log with grain-size ragged right profile (mud/sand/conglomerate)."""
    parts = [
        # Left vertical depth scale axis + tick marks
        line(180, 80, 180, 920, 38),
        line(110, 900, 180, 900, 30),
        line(110, 690, 180, 690, 30),
        line(110, 490, 180, 490, 30),
        line(110, 280, 180, 280, 30),
        line(110, 95, 180, 95, 30),
        # Bed 1 (top, 690..900): Limestone (width to x=680, brick masonry pattern)
        rect_outline(180, 690, 680, 900, 32),
        line(180, 795, 680, 795, 26),
        line(430, 795, 430, 900, 26),
        line(310, 690, 310, 795, 26),
        line(550, 690, 550, 795, 26),
        # Bed 2 (490..690): Recessive Shale/Mudstone (narrow width to x=520, dashed laminations)
        rect_outline(180, 490, 520, 690, 32),
        dashed_line(230, 625, 470, 625, 24, dash_count=3),
        dashed_line(230, 555, 470, 555, 24, dash_count=3),
        # Bed 3 (280..490): Cross-bedded Sandstone (wider width to x=780)
        rect_outline(180, 280, 780, 490, 32),
        stroke([(230, 490), (350, 340), (520, 280)], 26),
        stroke([(450, 490), (570, 340), (740, 280)], 26),
        # Bed 4 (bottom, 95..280): Basal Conglomerate (widest width to x=890, rounded clasts)
        rect_outline(180, 95, 890, 280, 32),
        circle(310, 185, 44),
        circle(520, 195, 50),
        circle(730, 180, 46),
        circle(420, 145, 28),
        circle(630, 145, 30),
    ]
    return union_all(parts)


def gl_structural_stereonet():
    """Schmidt / Wulff Structural Stereonet: Equatorial primitive circle, great circle cyclographic traces, and contoured poles to planes."""
    cx, cy, r = 500, 500, 405
    # Great circle 1 (dipping West-Northwest)
    gc1_pts = []
    # Great circle 2 (dipping East-Southeast, conjugate set)
    gc2_pts = []
    for i in range(41):
        t = (i / 40.0) * math.pi - math.pi / 2.0  # -pi/2 .. pi/2
        y = cy + r * math.sin(t)
        x1 = cx - 220 * math.cos(t)
        x2 = cx + 140 * math.cos(t)
        gc1_pts.append((x1, y))
        gc2_pts.append((x2, y))

    parts = [
        # Primitive circle + center cross
        disk_ring(cx, cy, r, 38),
        line(cx - 45, cy, cx + 45, cy, 26),
        line(cx, cy - 45, cx, cy + 45, 26),
        # North tick at top
        line(cx, cy + r, cx, cy + r + 55, 36),
        # Great circles rotated by 25 deg
        stroke(gc1_pts, 32),
        stroke(gc2_pts, 30),
        # Pole cluster & density contour in SW/NE quadrants
        circle(725, 420, 36),
        circle(765, 495, 32),
        circle(685, 510, 32),
        ellipse_outline(725, 475, 105, 125, 24, angle_deg=-20),
    ]
    return union_all(parts)


def gl_block_model_3d():
    """3D Resource Block Model: Isometric voxel block model with cutaway bench exposing high-grade mineralized core blocks."""
    # Build isometric 3x3x3 cube with front-top-right corner cut out (stepped open-pit / sub-block view)
    # Isometric basis vectors from center (500, 500)
    # Let's draw a clean isometric 3x3 grid cube + solid highlighted ore blocks in the cutaway step
    top = [(500, 920), (880, 720), (500, 520), (120, 720)]
    left = [(120, 720), (500, 520), (500, 80), (120, 280)]
    right = [(500, 520), (880, 720), (880, 280), (500, 80)]

    parts = [
        stroke(top, 36, closed=True),
        stroke(left, 36, closed=True),
        stroke(right, 36, closed=True),
        # 3x3 subdivisions on top face
        line(247, 787, 627, 587, 24),
        line(373, 853, 753, 653, 24),
        line(247, 653, 627, 853, 24),
        line(373, 587, 753, 787, 24),
        # 3x3 subdivisions on left face
        line(247, 653, 247, 213, 24),
        line(373, 587, 373, 147, 24),
        line(120, 573, 500, 373, 24),
        line(120, 427, 500, 227, 24),
        # 3x3 subdivisions on right face
        line(627, 587, 627, 147, 24),
        line(753, 653, 753, 213, 24),
        line(500, 373, 880, 573, 24),
        line(500, 227, 880, 427, 24),
        # Solid filled high-grade ore voxels in center-front faces
        poly([(500, 520), (627, 587), (627, 440), (500, 373)]),
        poly([(373, 587), (500, 520), (500, 373), (373, 440)]),
        poly([(500, 373), (627, 440), (627, 293), (500, 227)]),
        poly([(500, 653), (627, 720), (500, 787), (373, 720)]),
    ]
    return union_all(parts)


def gl_wireframe_mesh():
    """3D Geological Wireframe Mesh: Triangulated 3D surface mesh (TIN / implicit shell) of an orebody or geological unit."""
    # Vertices of a 3D faceted orebody shell
    v = {
        "top": (540, 910),
        "ul": (200, 730),
        "uc": (480, 640),
        "ur": (830, 690),
        "ml": (120, 420),
        "mc": (450, 370),
        "mr": (760, 430),
        "bl": (260, 150),
        "bc": (530, 90),
        "br": (860, 210),
    }
    edges = [
        ("top", "ul"), ("top", "uc"), ("top", "ur"),
        ("ul", "uc"), ("uc", "ur"),
        ("ul", "ml"), ("ul", "mc"), ("uc", "mc"), ("uc", "mr"), ("ur", "mr"),
        ("ml", "mc"), ("mc", "mr"),
        ("ml", "bl"), ("ml", "bc"), ("mc", "bl"), ("mc", "bc"), ("mc", "br"), ("mr", "bc"), ("mr", "br"),
        ("bl", "bc"), ("bc", "br"),
    ]
    parts = [line(v[a][0], v[a][1], v[b][0], v[b][1], 30) for a, b in edges]
    for pt in v.values():
        parts.append(circle(pt[0], pt[1], 36))
    return union_all(parts)


def gl_faulted_stratigraphy():
    """Fault-Bounded Stratigraphic Model: Sedimentary horizon layers offset across a dipping normal fault plane."""
    # Fault plane from top-left (370, 900) to bottom-right (630, 100)
    # Footwall on left (upthrown), Hanging wall on right (downthrown by dy = -120)
    parts = [
        # Outer geological section box
        rect_outline(90, 100, 910, 900, 36),
        # Bold fault plane cutting across entire section
        line(370, 900, 630, 100, 44),
        # Footwall horizons (left of fault): y = 700, 500, 300
        line(90, 700, 435, 700, 32),
        line(90, 500, 500, 500, 32),
        line(90, 300, 565, 300, 32),
        # Hanging wall horizons (right of fault, displaced downward): y = 570, 370, 170
        line(477, 570, 910, 570, 32),
        line(542, 370, 910, 370, 32),
        line(607, 170, 910, 170, 32),
        # Solid marker bed in both blocks to make stratigraphic offset visually instant
        poly([(90, 500), (500, 500), (542, 370), (90, 370)]),
        poly([(542, 370), (910, 370), (910, 240), (584, 240)]),
    ]
    # Keep marker bed split cleanly by a white gap along fault or distinct halves:
    fw_marker = poly([(90, 500), (500, 500), (539, 380), (90, 380)])
    hw_marker = poly([(542, 370), (910, 370), (910, 250), (581, 250)])
    base = union_all(parts[:-2] + [fw_marker, hw_marker])
    return base


def gl_folded_anticline_model():
    """Folded Structural Earth Model: Concentric multilayer anticline-syncline fold train with axial plane trace."""
    layers_y = [190, 350, 510, 670]
    parts = []
    for idx, y_base in enumerate(layers_y):
        pts = []
        for i in range(61):
            t = i / 60.0
            x = 85 + 830 * t
            # Asymmetric anticline on left-center, syncline on right
            y = y_base + 150 * math.sin(1.65 * math.pi * t - 0.15)
            pts.append((x, y))
        parts.append(stroke(pts, 44 if idx == 2 else 34))

    # Axial plane trace (dashed line passing through hinge points)
    parts.append(dashed_line(345, 95, 345, 910, 28, dash_count=8))
    return union_all(parts)


def gl_intrusive_pluton_model():
    """Igneous Pluton, Dike & Sill Earth Model: Deep magma batholith stock crosscutting horizontal country rock layers with sill & volcanic pipe."""
    # Country rock horizontal bedding lines
    parts = [
        rect_outline(90, 90, 910, 910, 36),
        line(90, 740, 910, 740, 28),
        line(90, 560, 910, 560, 28),
        line(90, 380, 910, 380, 28),
        # Solid igneous pluton dome at base + feeder dike + lateral sill + laccolith/cone
        poly(
            [
                (180, 90),
                (820, 90),
                (760, 290),
                (640, 410),
                (545, 450),
                (545, 590),
                (840, 590),  # lateral sill intruding along bedding
                (840, 665),
                (545, 665),
                (545, 860),  # feeder dike reaching near surface
                (455, 860),
                (455, 450),
                (350, 410),
                (240, 290),
            ]
        ),
    ]
    return union_all(parts)


def gl_plate_subduction():
    """Convergent Plate Subduction: Descending oceanic lithosphere slab beneath overriding continental plate, trench, and volcanic arc."""
    parts = [
        # Descending oceanic slab from left (80, 540) bending down to (760, 100)
        poly(
            [
                (80, 580),
                (380, 580),
                (790, 150),
                (690, 80),
                (330, 460),
                (80, 460),
            ]
        ),
        # Overriding continental crust wedge on right + volcanic arc cone at surface
        stroke(
            [
                (410, 560),
                (560, 660),
                (640, 660),
                (730, 860),
                (820, 660),
                (920, 660),
            ],
            38,
        ),
        line(560, 480, 920, 480, 32),
        # Magma diapirs rising from slab into volcano (x=730)
        circle(670, 390, 28),
        circle(710, 500, 32),
        circle(730, 610, 34),
        # Eruption plume above volcano crater
        curved_arrow(670, 865, 60, 0, 120, 28, 70, 40),
        curved_arrow(790, 865, 60, 180, 60, 28, 70, 40),
        # Subduction motion arrow on descending slab
        arrow(130, 660, 320, 660, 34, 85, 48),
    ]
    return union_all(parts)


def gl_fault_slip_tectonics():
    """Tectonic Fault Slip Kinematics: Inclined fault plane separating displaced rock blocks with opposing shear sense half-arrows."""
    # Fault plane at 55 deg through (500, 500)
    parts = [
        # Bold fault plane line from (260, 110) to (740, 890)
        line(260, 110, 740, 890, 38),
        # Left (footwall) block outline displaced upward
        stroke([(290, 390), (95, 390), (95, 760), (615, 760)], 36),
        # Right (hanging wall) block outline displaced downward
        stroke([(385, 240), (905, 240), (905, 610), (710, 610)], 36),
        # Opposing shear sense arrows parallel to fault plane
        arrow(330, 470, 490, 730, 36, 95, 54),
        arrow(670, 530, 510, 270, 36, 95, 54),
    ]
    return union_all(parts)


def gl_sedimentation_deposition():
    """Sediment Transport & Basin Deposition: Downslope fluvial transport arrows carrying clasts and settling into aggrading basin strata."""
    parts = [
        # Basin slope & horizontal floor profile
        stroke([(80, 840), (360, 460), (920, 460)], 38),
        # Underlying deposited horizontal basin strata
        line(310, 310, 920, 310, 32),
        line(240, 160, 920, 160, 32),
        # Downslope sediment transport arrow
        arrow(160, 890, 410, 550, 36, 95, 54),
        # Suspended sediment particles settling vertically into water column (with downward arrows)
        circle(540, 780, 38),
        arrow(540, 720, 540, 515, 30, 78, 45),
        circle(720, 820, 32),
        arrow(720, 765, 720, 515, 30, 78, 45),
        circle(850, 740, 28),
        arrow(850, 690, 850, 515, 28, 75, 42),
        # Deposited clasts on basin floor
        circle(480, 385, 34),
        circle(640, 385, 34),
        circle(800, 385, 34),
    ]
    return union_all(parts)


def gl_metamorphism_pt():
    """Metamorphic P-T Recrystallization & Foliation: Directed tectonic compression arrows flattening and crenulating schistose foliation planes."""
    parts = [
        # Opposing heavy tectonic compression arrows (sigma_1) from left and right
        arrow(65, 500, 265, 500, 46, 110, 64),
        arrow(935, 500, 735, 500, 46, 110, 64),
        # Vertical S1/S2 crenulation foliation waves between jaws (x=310..690)
        sine_wave(340, 120, 340, 880, amp=32, cycles=3.0, width=32),
        sine_wave(660, 120, 660, 880, amp=32, cycles=3.0, width=32),
        # Rotated garnet porphyroblast in center wrapped by foliation
        regular_poly(500, 500, 115, 6, start_angle_deg=30),
        stroke([(450, 880), (430, 680), (355, 500), (430, 320), (450, 120)], 30),
        stroke([(550, 880), (570, 680), (645, 500), (570, 320), (550, 120)], 30),
    ]
    # Hollow center spiral inclusion trail inside garnet porphyroblast
    inclusion = line(445, 470, 555, 530, 28)
    return diff(union_all(parts), inclusion)


def gl_weathering_erosion():
    """Weathering & Erosional Breakdown: Jointed rock outcrop fracturing into detached blocks and eroding downslope under rain/wind."""
    parts = [
        # Intact jointed rock crag on left
        poly([(80, 140), (80, 720), (240, 780), (380, 700), (420, 440), (490, 140)]),
        # Weathering exfoliation/frost-wedging cracks cut into rock mass (subtracted below)
        # Detached angular talus boulders & fine regolith rolling downslope to right
        regular_poly(535, 585, 72, 5, 15),
        regular_poly(650, 410, 62, 5, 40),
        regular_poly(775, 275, 48, 6, 10),
        circle(885, 195, 34),
        circle(790, 165, 28),
        # Erosional transport wind/water sweep arrow
        curved_arrow(620, 490, 270, 110, 20, 34, 90, 52),
        # Rain / chemical weathering slashes at top-left
        line(160, 910, 120, 820, 28),
        line(290, 920, 250, 830, 28),
        line(420, 900, 380, 810, 28),
    ]
    cracks = union_all(
        [
            stroke([(250, 785), (270, 560), (160, 450)], 32),
            stroke([(385, 705), (310, 580), (425, 440)], 32),
        ]
    )
    return diff(union_all(parts), cracks)


GEOLOGICAL_ICONS: List[Dict[str, Any]] = [
    {
        "id": "gl_strike_dip_mapping",
        "name": "Structural Strike & Dip Mapping",
        "domain": "Geological",
        "category": "Methods",
        "codepoint": 0xE01F,
        "description": "Compass-clinometer bezel enclosing a structural geology strike-and-dip orientation symbol.",
        "keywords": ["strike and dip", "structural mapping", "clinometer", "compass", "bedding", "foliation"],
        "builder": gl_strike_dip_mapping,
    },
    {
        "id": "gl_diamond_core_drilling",
        "name": "Diamond Core Drilling",
        "domain": "Geological",
        "category": "Methods",
        "codepoint": 0xE020,
        "description": "Diamond-impregnated annular drill bit recovering cylindrical rock core above a compartmentalized core tray.",
        "keywords": ["core drilling", "diamond drill", "core barrel", "core logging", "core box", "exploration"],
        "builder": gl_diamond_core_drilling,
    },
    {
        "id": "gl_thin_section_petrography",
        "name": "Thin-Section Optical Petrography",
        "domain": "Geological",
        "category": "Methods",
        "codepoint": 0xE021,
        "description": "Polarized-light microscope reticle field of view showing interlocking mineral grains, cleavage, and twinning.",
        "keywords": ["thin section", "petrography", "microscope", "mineralogy", "twinned", "xpl"],
        "builder": gl_thin_section_petrography,
    },
    {
        "id": "gl_stratigraphic_logging",
        "name": "Measured Stratigraphic Column",
        "domain": "Geological",
        "category": "Methods",
        "codepoint": 0xE022,
        "description": "Lithostratigraphic column log with weathering/grain-size profile across limestone, shale, sandstone, and conglomerate.",
        "keywords": ["stratigraphic column", "lithology", "sedimentology", "logging", "grain size", "strata"],
        "builder": gl_stratigraphic_logging,
    },
    {
        "id": "gl_structural_stereonet",
        "name": "Schmidt Structural Stereonet",
        "domain": "Geological",
        "category": "Methods",
        "codepoint": 0xE023,
        "description": "Equal-area lower-hemisphere stereographic projection showing conjugate great circles and contoured pole clusters.",
        "keywords": ["stereonet", "schmidt net", "wulff net", "great circle", "poles to planes", "structural geology"],
        "builder": gl_structural_stereonet,
    },
    {
        "id": "gl_block_model_3d",
        "name": "3D Resource Block Model",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE024,
        "description": "Isometric 3D discretized voxel block model with cutaway bench exposing mineralized resource blocks.",
        "keywords": ["block model", "voxel", "resource estimation", "kriging", "sub-blocked", "3d geology"],
        "builder": gl_block_model_3d,
    },
    {
        "id": "gl_wireframe_mesh",
        "name": "3D Geological Wireframe Mesh",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE025,
        "description": "Triangulated 3D surface wireframe (TIN / implicit shell) representing an orebody or lithological contact.",
        "keywords": ["wireframe", "triangulation", "tin", "implicit model", "orebody shell", "3d mesh"],
        "builder": gl_wireframe_mesh,
    },
    {
        "id": "gl_faulted_stratigraphy",
        "name": "Faulted Stratigraphic Horizon Model",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE026,
        "description": "Layered sedimentary earth model offset across an inclined normal fault plane.",
        "keywords": ["fault model", "stratigraphy", "horizon", "throw", "normal fault", "structural model"],
        "builder": gl_faulted_stratigraphy,
    },
    {
        "id": "gl_folded_anticline_model",
        "name": "Folded Anticline-Syncline Model",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE027,
        "description": "Ductile multilayer folded earth model showing anticline/syncline curvature and axial plane trace.",
        "keywords": ["anticline", "syncline", "fold", "structural trap", "axial plane", "folded strata"],
        "builder": gl_folded_anticline_model,
    },
    {
        "id": "gl_intrusive_pluton_model",
        "name": "Igneous Pluton, Dike & Sill Model",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE028,
        "description": "Subsurface magmatic batholith stock, discordant feeder dike, and concordant sill intruding country rock.",
        "keywords": ["pluton", "batholith", "dike", "sill", "intrusion", "igneous model", "porphyry"],
        "builder": gl_intrusive_pluton_model,
    },
    {
        "id": "gl_plate_subduction",
        "name": "Plate Tectonic Subduction",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE029,
        "description": "Convergent margin subduction of oceanic lithosphere beneath a continental plate generating arc volcanism.",
        "keywords": ["subduction", "plate tectonics", "volcanic arc", "trench", "slab", "geodynamics"],
        "builder": gl_plate_subduction,
    },
    {
        "id": "gl_fault_slip_tectonics",
        "name": "Tectonic Fault Slip & Rupture",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE02A,
        "description": "Relative hanging-wall and footwall displacement along a tectonic fault plane with kinematic shear arrows.",
        "keywords": ["fault slip", "tectonics", "hanging wall", "footwall", "shear sense", "kinematics"],
        "builder": gl_fault_slip_tectonics,
    },
    {
        "id": "gl_sedimentation_deposition",
        "name": "Sediment Transport & Deposition",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE02B,
        "description": "Clastic sediment transport down a basin margin and gravitational settling into aggrading horizontal beds.",
        "keywords": ["sedimentation", "deposition", "aggradation", "basin", "stratigraphy", "clastic"],
        "builder": gl_sedimentation_deposition,
    },
    {
        "id": "gl_metamorphism_pt",
        "name": "Metamorphic P-T Recrystallization",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE02C,
        "description": "Tectonic compressive stress generating metamorphic foliation wrapping around a rotated garnet porphyroblast.",
        "keywords": ["metamorphism", "foliation", "schistosity", "porphyroblast", "pressure temperature", "recrystallization"],
        "builder": gl_metamorphism_pt,
    },
    {
        "id": "gl_weathering_erosion",
        "name": "Weathering & Erosional Breakdown",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE02D,
        "description": "Physical and chemical breakdown of a fractured rock outcrop shedding angular talus and regolith downslope.",
        "keywords": ["weathering", "erosion", "regolith", "exfoliation", "mass wasting", "denudation"],
        "builder": gl_weathering_erosion,
    },
]
