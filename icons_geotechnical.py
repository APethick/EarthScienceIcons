"""
Geotechnical Icon Definitions (15 icons):
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


def gt_spt_test():
    """Standard Penetration Test (SPT): Drop hammer, anvil, drill rod, split-spoon sampler shoe, and blow-count N profile."""
    parts = [
        # Ground surface line
        line(70, 620, 620, 620, 36),
        # Borehole walls below ground
        line(235, 110, 235, 620, 28),
        line(445, 110, 445, 620, 28),
        # Drop weight hammer at top + anvil + drill rod
        rounded_rect(225, 760, 455, 910, 25),
        rect(275, 695, 405, 745),
        line(340, 410, 340, 930, 34),
        # Downward impact arrows flanking hammer
        arrow(155, 900, 155, 720, 28, 75, 44),
        arrow(525, 900, 525, 720, 28, 75, 44),
        # Split-spoon sampler tube & cutting shoe at bottom of borehole
        rect_outline(285, 200, 395, 410, 30),
        poly([(285, 200), (315, 130), (365, 130), (395, 200)]),
        # Right side: SPT N-value blow count step log
        line(670, 110, 670, 880, 30),
        stroke(
            [
                (670, 820),
                (750, 820),
                (750, 640),
                (830, 640),
                (830, 460),
                (780, 460),
                (780, 290),
                (910, 290),
                (910, 130),
            ],
            34,
        ),
    ]
    return union_all(parts)


def gt_cpt_cone():
    """Cone Penetration Test (CPT): 60-degree piezocone tip, u2 pore pressure filter ring, friction sleeve, and qc/fs logs."""
    parts = [
        # Ground line
        line(70, 820, 930, 820, 34),
        # Push rod & friction sleeve (left-center)
        rect_outline(220, 330, 380, 890, 34),
        # Friction sleeve section boundaries & u2 filter element band
        line(220, 660, 380, 660, 30),
        rect(205, 315, 395, 365),
        # 60-degree conical tip at bottom
        poly([(205, 315), (395, 315), (300, 110)]),
        # Upward sleeve friction arrows (fs) along shaft
        arrow(135, 390, 135, 620, 28, 75, 42),
        # Upward tip resistance arrow (qc) below cone
        arrow(450, 110, 450, 285, 28, 75, 42),
        # Continuous CPT resistance log on right
        line(570, 110, 570, 770, 28),
        stroke(
            [
                (640, 750),
                (710, 650),
                (660, 550),
                (860, 460),
                (820, 360),
                (900, 250),
                (740, 140),
            ],
            34,
        ),
    ]
    return union_all(parts)


def gt_triaxial_shear():
    """Triaxial Compression Shear Test: Cylindrical soil sample in pressure cell with axial stress sigma_1, confining sigma_3, and shear plane."""
    parts = [
        # Outer triaxial chamber dome and base plate
        rounded_rect_outline(210, 170, 790, 800, 70, 34),
        rect(140, 110, 860, 175),
        # Soil specimen cylinder in center with top/bottom porous platens
        rect_outline(375, 255, 625, 665, 32),
        rect(355, 665, 645, 715),
        rect(355, 205, 645, 255),
        # Diagonal shear failure plane across specimen
        dashed_line(385, 310, 615, 610, 30, dash_count=5),
        # Axial load piston & downward arrow (sigma_1) at top
        arrow(500, 930, 500, 725, 42, 95, 56),
        # Lateral confining fluid pressure arrows (sigma_3) on left and right
        arrow(95, 550, 345, 550, 32, 80, 46),
        arrow(95, 370, 345, 370, 32, 80, 46),
        arrow(905, 550, 655, 550, 32, 80, 46),
        arrow(905, 370, 655, 370, 32, 80, 46),
    ]
    return union_all(parts)


def gt_piezometer_well():
    """Standpipe / Borehole Piezometer: Cased monitoring well with slotted screen intake, water column, and phreatic water table triangle."""
    parts = [
        # Ground surface
        line(70, 780, 930, 780, 36),
        # Wellhead cap at surface
        rounded_rect(350, 780, 530, 890, 20),
        # Standpipe casing walls
        line(380, 140, 380, 780, 32),
        line(500, 140, 500, 780, 32),
        # Slotted intake screen & gravel pack zone at bottom
        line(350, 290, 530, 290, 26),
        line(350, 220, 530, 220, 26),
        line(350, 140, 530, 140, 32),
        # Water column inside standpipe up to piezometric level (y=540)
        rect(408, 140, 472, 540),
        # Phreatic water table dashed line across formation at y=540
        dashed_line(80, 540, 920, 540, 28, dash_count=8),
        # Standard geotechnical inverted water-table triangle symbol on right (x=740, y=540)
        poly([(665, 655), (815, 655), (740, 540)]),
        line(680, 490, 800, 490, 26),
        line(705, 440, 775, 440, 26),
    ]
    return union_all(parts)


def gt_inclinometer_casing():
    """Borehole Inclinometer: Vertical reference casing vs laterally deflected casing profile across active subsurface slip plane."""
    # Deflected casing S-curve displaced to the right above slip zone (y=440)
    defl_pts = [
        (360, 110),
        (360, 260),
        (375, 380),
        (480, 480),
        (600, 600),
        (665, 740),
        (700, 880),
    ]
    parts = [
        # Ground surface
        line(80, 860, 920, 860, 34),
        # Original vertical borehole axis (dashed reference)
        dashed_line(360, 110, 360, 880, 28, dash_count=9),
        # Deflected inclinometer casing with torpedo probe wheels
        stroke(defl_pts, 42),
        circle(540, 540, 48),
        # Subsurface shear / slip plane crossing at y ~ 430
        dashed_line(100, 520, 900, 320, 30, dash_count=7),
        # Horizontal deflection arrows showing delta-x displacement
        arrow(385, 760, 650, 760, 32, 85, 48),
        arrow(385, 610, 575, 610, 30, 80, 45),
    ]
    return union_all(parts)


def gt_mohr_coulomb():
    """Mohr-Coulomb Failure Envelope: Normal stress (sigma_n) vs shear stress (tau) axes, two Mohr circles, and tangent failure line."""
    parts = [
        # tau (vertical) and sigma_n (horizontal) axes
        arrow(120, 140, 120, 900, 36, 95, 54),
        arrow(100, 160, 930, 160, 36, 95, 54),
        # Mohr Circle 1 (smaller, left) centered at (340, 160), r=140 -> semicircle
        arc(340, 160, 140, 0, 180, 32),
        # Mohr Circle 2 (larger, right) centered at (640, 160), r=235 -> semicircle
        arc(640, 160, 235, 0, 180, 36),
        # Mohr-Coulomb tangent failure envelope: tau = c + sigma * tan(phi)
        # At x=120, y=240 (cohesion intercept c); tangent to both circles up to (900, 535)
        line(120, 240, 900, 540, 40),
        # Cohesion intercept marker & tangent points
        circle(120, 240, 34),
        circle(290, 291, 30),
        circle(558, 380, 32),
    ]
    return union_all(parts)


def gt_rock_mass_rmr_gsi():
    """Rock Mass Classification (RMR / GSI / Q): Interlocking fractured rock mass block matrix with joint sets."""
    parts = [
        # Outer GSI/RMR chart frame
        rect_outline(95, 95, 905, 905, 38),
        # Set 1 joints (dipping steeply right-to-left)
        line(95, 680, 420, 905, 30),
        line(95, 380, 720, 905, 32),
        line(240, 95, 905, 660, 32),
        line(560, 95, 905, 390, 30),
        # Set 2 conjugate joints (dipping shallowly left-to-right)
        line(95, 760, 905, 480, 32),
        line(95, 500, 905, 210, 32),
        line(95, 250, 560, 95, 28),
        line(420, 905, 905, 730, 28),
        # Highlight one key intact rock block in the center
        poly([(395, 580), (610, 505), (505, 415), (295, 490)]),
    ]
    return union_all(parts)


def gt_slope_stability_grid():
    """Slope Stability Model (Method of Slices): Embankment slope profile, center of rotation grid, circular slip surface, and vertical slices."""
    # Slope profile from top-left bench (80, 620) to crest (360, 620) down to toe (720, 220) to right (920, 220)
    slope_pts = [(80, 620), (360, 620), (720, 220), (920, 220)]
    # Circular slip arc centered at (620, 780) with radius R = 570
    # From angle ~196 deg (crest x=180, y=620) to ~280 deg (toe x=720, y=220)
    parts = [
        stroke(slope_pts, 40),
        arc(620, 780, 570, 196, 280, 36),
        # Method of slices vertical dividers inside sliding mass
        line(260, 620, 260, 338, 26),
        line(360, 620, 360, 273, 28),
        line(480, 486, 480, 228, 28),
        line(600, 353, 600, 211, 26),
        # Center of rotation cross & radial lines
        circle(620, 780, 38),
        dashed_line(620, 780, 180, 620, 24, dash_count=5),
        dashed_line(620, 780, 720, 220, 24, dash_count=5),
        # Search grid above crest
        rect_outline(520, 700, 820, 900, 24),
        line(620, 700, 620, 900, 20),
        line(720, 700, 720, 900, 20),
        line(520, 780, 820, 780, 20),
    ]
    return union_all(parts)


def gt_soil_profile_log():
    """Geotechnical Soil Horizon Profile: Engineering borehole log showing engineered fill, clay, sand/gravel, and bedrock horizons."""
    parts = [
        # Outer column frame
        rect_outline(140, 80, 860, 920, 36),
        # Depth ticks on left margin
        line(80, 720, 140, 720, 30),
        line(80, 500, 140, 500, 30),
        line(80, 280, 140, 280, 30),
        # Layer 1 (720..920): Fill / Topsoil (diagonal cross-ticks)
        line(140, 720, 860, 720, 32),
        line(240, 760, 340, 880, 26),
        line(340, 760, 240, 880, 26),
        line(560, 760, 660, 880, 26),
        line(660, 760, 560, 880, 26),
        # Layer 2 (500..720): Clayey Silt (horizontal dashed laminations)
        line(140, 500, 860, 500, 32),
        dashed_line(200, 645, 800, 645, 26, dash_count=5),
        dashed_line(250, 575, 750, 575, 26, dash_count=4),
        # Layer 3 (280..500): Sand & Gravel (cobble circles and sand dots)
        line(140, 280, 860, 280, 32),
        circle(280, 390, 48),
        circle(500, 410, 36),
        circle(680, 375, 52),
        circle(390, 345, 28),
        # Layer 4 (80..280): Bedrock (masonry/limestone block pattern)
        line(140, 180, 860, 180, 28),
        line(380, 180, 380, 280, 28),
        line(640, 180, 640, 280, 28),
        line(260, 80, 260, 180, 28),
        line(520, 80, 520, 180, 28),
        line(760, 80, 760, 180, 28),
    ]
    return union_all(parts)


def gt_fe_mesh_tunnel():
    """Geomechanical Finite Element Mesh: Radial & concentric finite element discretization around an underground horseshoe tunnel."""
    # Outer domain boundary
    outer = rect_outline(90, 90, 910, 910, 36)
    # Central circular/horseshoe tunnel opening (radius 170 at 500, 480)
    cx, cy = 500, 480
    r1, r2, r3 = 165, 295, 420
    parts = [
        outer,
        disk_ring(cx, cy, r1, 38),
        disk_ring(cx, cy, r2, 24),
        # Flat tunnel invert floor
        line(cx - 155, cy - 65, cx + 155, cy - 65, 36),
    ]
    # Radial mesh rays from tunnel wall (r1) to outer box
    for ang_deg in range(0, 360, 30):
        rad = math.radians(ang_deg)
        x_start = cx + r1 * math.cos(rad)
        y_start = cy + r1 * math.sin(rad)
        x_end = cx + 560 * math.cos(rad)
        y_end = cy + 560 * math.sin(rad)
        parts.append(line(x_start, y_start, x_end, y_end, 22))

    combined = intersect(union_all(parts), rect(90, 90, 910, 910))
    # Hollow out the tunnel interior cleanly
    tunnel_void = diff(circle(cx, cy, r1 - 18), rect(cx - 200, cy - 200, cx + 200, cy - 82))
    return diff(combined, tunnel_void)


def gt_consolidation_settlement():
    """Terzaghi Soil Consolidation: Surface footing load Q squeezing saturated soil layer, expelling pore water laterally and settling."""
    parts = [
        # Original ground surface (dashed) vs settled profile
        dashed_line(80, 700, 920, 700, 26, dash_count=8),
        stroke([(80, 700), (260, 700), (320, 560), (680, 560), (740, 700), (920, 700)], 34),
        # Footing slab in settled trough + heavy downward load arrows
        rect(330, 575, 670, 675),
        arrow(400, 910, 400, 690, 36, 90, 52),
        arrow(600, 910, 600, 690, 36, 90, 52),
        # Impervious base rock boundary at bottom
        line(80, 140, 920, 140, 38),
        # Compressing soil skeleton springs in center
        stroke([(420, 550), (470, 470), (370, 390), (470, 310), (370, 230), (420, 150)], 28),
        stroke([(580, 550), (630, 470), (530, 390), (630, 310), (530, 230), (580, 150)], 28),
        # Lateral pore water expulsion arrows (u_e dissipation)
        arrow(310, 360, 95, 360, 34, 85, 50),
        arrow(690, 360, 905, 360, 34, 85, 50),
    ]
    return union_all(parts)


def gt_soil_liquefaction():
    """Seismic Soil Liquefaction: Horizontal shear wave shaking at base, upward pore water pressure arrows, floating soil grains & sand boil."""
    parts = [
        # Ground surface with central sand-boil volcano cone erupting
        stroke([(80, 660), (350, 660), (440, 790)], 36),
        stroke([(560, 790), (650, 660), (920, 660)], 36),
        # Upward water/sand fountain spout emerging from boil crater
        curved_arrow(390, 780, 110, 0, 115, 32, 80, 46),
        curved_arrow(610, 780, 110, 180, 65, 32, 80, 46),
        # Suspended soil grains losing grain-to-grain contact
        circle(220, 480, 44),
        circle(780, 480, 44),
        circle(350, 330, 44),
        circle(650, 330, 44),
        circle(500, 460, 44),
        # Upward excess pore pressure (Delta-u) arrows between grains
        arrow(500, 260, 500, 760, 34, 85, 50),
        arrow(260, 260, 260, 610, 30, 78, 45),
        arrow(740, 260, 740, 610, 30, 78, 45),
        # Cyclic horizontal seismic shaking wave at base
        sine_wave(140, 140, 860, 140, amp=40, cycles=3.0, width=36),
    ]
    return union_all(parts)


def gt_slope_landslide():
    """Rotational Slope Landslide: Concave scarp, detached slumping soil mass rotating along curved failure surface with toe bulge."""
    parts = [
        # Intact bedrock footwall / concave failure scarp from (140, 860) down to (880, 180)
        stroke(
            [
                (80, 860),
                (180, 860),
                (230, 630),
                (360, 410),
                (570, 250),
                (840, 180),
                (920, 180),
            ],
            38,
        ),
        # Displaced slumped mass (back-tilted head block & bulging toe)
        poly(
            [
                (265, 680),
                (485, 630),
                (790, 320),
                (835, 235),
                (585, 295),
                (390, 450),
            ]
        ),
        # Curved rotational slip arrow above/along failure mass
        curved_arrow(590, 680, 280, 195, 265, 36, 95, 56),
        # Tension cracks at crown
        line(130, 860, 150, 750, 26),
    ]
    return union_all(parts)


def gt_seepage_flownet():
    """Darcy Seepage Flow Net: Impermeable sheet pile cutoff wall with orthogonal streamlines and equipotential lines beneath."""
    parts = [
        # Ground / reservoir bed on left (upstream) and right (downstream)
        line(70, 620, 465, 620, 34),
        line(535, 620, 930, 620, 34),
        #Upstream high head water level on left
        dashed_line(80, 830, 450, 830, 28, dash_count=5),
        # Impervious base stratum at bottom
        line(70, 110, 930, 110, 40),
        # Central vertical sheet-pile cutoff wall from y=900 down to y=410
        rect(465, 410, 535, 900),
        # Flow channels (U-shaped streamlines wrapping under sheet pile tip at 500, 410)
        arc(500, 620, 290, 185, 355, 30),
        arc(500, 620, 420, 185, 355, 32),
        arrow_head(788, 590, 85, 85, 48),
        arrow_head(918, 590, 85, 85, 48),
        # Radial equipotential drop lines (dashed) orthogonal to streamlines
        dashed_line(500, 410, 150, 310, 24, dash_count=4),
        dashed_line(500, 410, 290, 130, 24, dash_count=4),
        dashed_line(500, 410, 710, 130, 24, dash_count=4),
        dashed_line(500, 410, 850, 310, 24, dash_count=4),
    ]
    return union_all(parts)


def gt_rock_burst_spalling():
    """Excavation Wall Spalling & Rockburst: Deep underground tunnel under high vertical/horizontal stress with sidewall slabbing & ejection."""
    cx, cy = 500, 500
    parts = [
        # Major far-field stress arrows (sigma_1 vertical, sigma_3 horizontal)
        arrow(500, 930, 500, 755, 40, 95, 55),
        arrow(500, 70, 500, 245, 40, 95, 55),
        arrow(70, 500, 230, 500, 32, 80, 46),
        arrow(930, 500, 770, 500, 32, 80, 46),
        # Top and bottom intact tunnel arch arcs
        arc(cx, cy, 220, 40, 140, 38),
        arc(cx, cy, 220, 220, 320, 38),
        # Left and right V-shaped breakout notches + spalling rock slabs
        stroke([(330, 640), (235, 500), (330, 360)], 34),
        stroke([(670, 640), (765, 500), (670, 360)], 34),
        # Onion-skin spalling tensile fractures parallel to sidewalls
        arc(cx, cy, 185, 148, 212, 28),
        arc(cx, cy, 185, -32, 32, 28),
        # Ejected rock fragments flying inward toward tunnel center
        poly([(345, 535), (395, 560), (385, 495)]),
        poly([(655, 535), (605, 560), (615, 495)]),
        arrow(350, 450, 455, 485, 26, 68, 40),
        arrow(650, 450, 545, 485, 26, 68, 40),
    ]
    return union_all(parts)


GEOTECHNICAL_ICONS: List[Dict[str, Any]] = [
    {
        "id": "gt_spt_test",
        "name": "Standard Penetration Test (SPT)",
        "domain": "Geotechnical",
        "category": "Methods",
        "codepoint": 0xE010,
        "description": "Drop hammer driving a split-spoon sampler downhole with SPT N-value blow count depth profile.",
        "keywords": ["spt", "standard penetration test", "split spoon", "blow count", "n-value", "borehole"],
        "builder": gt_spt_test,
    },
    {
        "id": "gt_cpt_cone",
        "name": "Cone Penetration Test (CPT)",
        "domain": "Geotechnical",
        "category": "Methods",
        "codepoint": 0xE011,
        "description": "Instrumented 60-degree piezocone penetrometer measuring tip resistance (qc), sleeve friction (fs), and pore pressure (u2).",
        "keywords": ["cpt", "cptU", "piezocone", "cone penetration", "tip resistance", "sleeve friction"],
        "builder": gt_cpt_cone,
    },
    {
        "id": "gt_triaxial_shear",
        "name": "Triaxial Shear Compression Test",
        "domain": "Geotechnical",
        "category": "Methods",
        "codepoint": 0xE012,
        "description": "Cylindrical soil/rock core specimen under confining fluid stress (sigma_3) and axial deviatoric load (sigma_1).",
        "keywords": ["triaxial", "shear strength", "sigma1", "sigma3", "laboratory test", "soil mechanics"],
        "builder": gt_triaxial_shear,
    },
    {
        "id": "gt_piezometer_well",
        "name": "Piezometer & Groundwater Well",
        "domain": "Geotechnical",
        "category": "Methods",
        "codepoint": 0xE013,
        "description": "Cased borehole standpipe piezometer measuring subsurface hydraulic head and phreatic water table.",
        "keywords": ["piezometer", "water table", "pore pressure", "phreatic surface", "monitoring well"],
        "builder": gt_piezometer_well,
    },
    {
        "id": "gt_inclinometer_casing",
        "name": "Borehole Inclinometer",
        "domain": "Geotechnical",
        "category": "Methods",
        "codepoint": 0xE014,
        "description": "Grooved borehole inclinometer casing tracking lateral ground deformation across an active shear surface.",
        "keywords": ["inclinometer", "slope monitoring", "lateral displacement", "deflection", "shear zone"],
        "builder": gt_inclinometer_casing,
    },
    {
        "id": "gt_mohr_coulomb",
        "name": "Mohr-Coulomb Failure Envelope",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE015,
        "description": "Normal vs. shear stress diagram with Mohr stress circles, cohesion intercept (c), and friction angle slope (phi).",
        "keywords": ["mohr-coulomb", "mohr circle", "cohesion", "friction angle", "failure envelope", "constitutive model"],
        "builder": gt_mohr_coulomb,
    },
    {
        "id": "gt_rock_mass_rmr_gsi",
        "name": "Rock Mass Classification (RMR / GSI)",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE016,
        "description": "Jointed rock mass block structure matrix representing RMR, Q-system, and Geological Strength Index (GSI).",
        "keywords": ["gsi", "rmr", "q-system", "rock mass", "joint sets", "discontinuities", "hoek-brown"],
        "builder": gt_rock_mass_rmr_gsi,
    },
    {
        "id": "gt_slope_stability_grid",
        "name": "Limit Equilibrium Slope Model",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE017,
        "description": "Method of slices limit-equilibrium slope model with circular slip surface and slip-center search grid.",
        "keywords": ["slope stability", "method of slices", "bishop", "factor of safety", "slip circle"],
        "builder": gt_slope_stability_grid,
    },
    {
        "id": "gt_soil_profile_log",
        "name": "Engineering Soil Horizon Profile",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE018,
        "description": "Layered geotechnical engineering soil profile depicting fill, cohesive clay, granular sand/gravel, and bedrock.",
        "keywords": ["soil profile", "borehole log", "uscs", "overburden", "bedrock", "horizon"],
        "builder": gt_soil_profile_log,
    },
    {
        "id": "gt_fe_mesh_tunnel",
        "name": "Geomechanical FEA Tunnel Mesh",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE019,
        "description": "Discretized finite-element numerical mesh surrounding an underground horseshoe tunnel excavation.",
        "keywords": ["fea", "fem", "numerical model", "mesh", "tunnel", "excavation", "geomechanics"],
        "builder": gt_fe_mesh_tunnel,
    },
    {
        "id": "gt_consolidation_settlement",
        "name": "Consolidation & Foundation Settlement",
        "domain": "Geotechnical",
        "category": "Processes",
        "codepoint": 0xE01A,
        "description": "Terzaghi primary consolidation showing foundation load compressing soil skeleton and expelling pore water.",
        "keywords": ["consolidation", "settlement", "terzaghi", "pore water dissipation", "foundation"],
        "builder": gt_consolidation_settlement,
    },
    {
        "id": "gt_soil_liquefaction",
        "name": "Seismic Soil Liquefaction",
        "domain": "Geotechnical",
        "category": "Processes",
        "codepoint": 0xE01B,
        "description": "Cyclic earthquake shaking generating excess pore water pressure, loss of effective stress, and surface sand boils.",
        "keywords": ["liquefaction", "sand boil", "cyclic mobility", "pore pressure", "earthquake"],
        "builder": gt_soil_liquefaction,
    },
    {
        "id": "gt_slope_landslide",
        "name": "Rotational Slope Failure & Landslide",
        "domain": "Geotechnical",
        "category": "Processes",
        "codepoint": 0xE01C,
        "description": "Mass movement and rotational slumping of a soil/rock slope along a concave shear failure surface.",
        "keywords": ["landslide", "slope failure", "slump", "scarp", "mass wasting", "shear failure"],
        "builder": gt_slope_landslide,
    },
    {
        "id": "gt_seepage_flownet",
        "name": "Darcy Seepage & Flow Net",
        "domain": "Geotechnical",
        "category": "Processes",
        "codepoint": 0xE01D,
        "description": "Subsurface groundwater seepage streamlines and orthogonal equipotential drops beneath a cutoff sheet pile.",
        "keywords": ["seepage", "flow net", "darcy", "piping", "cutoff wall", "equipotential"],
        "builder": gt_seepage_flownet,
    },
    {
        "id": "gt_rock_burst_spalling",
        "name": "Stress Spalling & Rockburst",
        "domain": "Geotechnical",
        "category": "Processes",
        "codepoint": 0xE01E,
        "description": "High tangential stress concentration causing brittle sidewall spalling, V-notch breakout, and rockburst in deep excavations.",
        "keywords": ["rockburst", "spalling", "borehole breakout", "brittle failure", "in-situ stress", "mining"],
        "builder": gt_rock_burst_spalling,
    },
]
