"""
Geochemical Icon Definitions (15 icons):
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


def gc_soil_stream_sampling():
    """Soil & Stream Geochemical Sampling: T-handle soil auger in ground on left, plus systematic spatial sampling grid & sieve on right."""
    parts = [
        # Left side: T-handle helical soil auger penetrating horizon
        rounded_rect(100, 830, 440, 905, 30),
        line(270, 520, 270, 830, 40),
        # Auger helical flights
        stroke(
            [
                (270, 520),
                (350, 450),
                (190, 380),
                (350, 310),
                (190, 240),
                (270, 140),
            ],
            38,
        ),
        line(80, 560, 460, 560, 32),
        # Right side: 3x3 systematic geochemical sample grid with anomalous sample points
        dashed_line(560, 200, 900, 200, 22, dash_count=4),
        dashed_line(560, 480, 900, 480, 22, dash_count=4),
        dashed_line(560, 760, 900, 760, 22, dash_count=4),
        dashed_line(580, 180, 580, 780, 22, dash_count=4),
        dashed_line(730, 180, 730, 780, 22, dash_count=4),
        dashed_line(880, 180, 880, 780, 22, dash_count=4),
        # Grid sample stations (center-right stations enlarged for anomaly)
        circle(580, 760, 32),
        circle(730, 760, 32),
        circle(880, 760, 32),
        circle(580, 480, 36),
        circle(730, 480, 62),  # High-grade anomaly station
        circle(880, 480, 42),
        circle(580, 200, 32),
        circle(730, 200, 38),
        circle(880, 200, 32),
    ]
    return union_all(parts)


def gc_pxrf_analyzer():
    """Portable XRF (pXRF) Analyzer: Handheld XRF analyzer nosecone emitting primary X-ray beam onto rock sample with secondary fluorescence."""
    # Handheld pXRF body on left
    gun_body = poly(
        [
            (85, 680),
            (460, 680),
            (540, 590),
            (540, 470),
            (340, 440),
            (270, 150),
            (130, 150),
            (180, 440),
            (85, 480),
        ]
    )
    gun_screen = rect(145, 520, 360, 625)
    gun = diff(gun_body, gun_screen)

    parts = [
        gun,
        # Primary excitation X-ray beam (lightning/wave ray) from nose (540, 540) to rock (800, 470)
        arrow(560, 560, 770, 480, 30, 80, 46),
        # Secondary characteristic X-ray fluorescence returning from rock to detector
        curved_arrow(670, 610, 145, -15, 135, 28, 78, 44),
        # Rock specimen on right with atomic orbital rings
        poly([(770, 220), (925, 280), (915, 620), (795, 680), (730, 450)]),
    ]
    return union_all(parts)


def gc_icp_ms_spectrometry():
    """ICP-MS / OES Mass Spectrometry: Elemental mass-to-charge (m/z) spectral baseline with sharp analytical isotope/element peaks."""
    # Continuous baseline + sharp Lorentzian/Gaussian mass spectrum peaks
    spec_pts = [
        (100, 200),
        (170, 200),
        (215, 580),  # Peak 1 (e.g. Cu)
        (260, 200),
        (340, 200),
        (385, 390),  # Peak 2 (e.g. Zn)
        (430, 200),
        (490, 200),
        (555, 860),  # Major Peak 3 (e.g. Au / pathfinder)
        (620, 200),
        (690, 200),
        (745, 670),  # Peak 4 (e.g. As)
        (800, 200),
        (900, 200),
    ]
    parts = [
        # Axes (Intensity vs m/z)
        arrow(100, 130, 100, 910, 34, 90, 50),
        arrow(80, 150, 930, 150, 34, 90, 50),
        # Mass spectrum curve
        stroke(spec_pts, 38),
        # Peak apex markers
        circle(215, 580, 32),
        circle(555, 860, 38),
        circle(745, 670, 34),
        # Horizontal detection limit (LOD) threshold dashed line
        dashed_line(120, 310, 890, 310, 24, dash_count=8),
    ]
    return union_all(parts)


def gc_fire_assay():
    """Fire Assay Crucible & Cupellation: Tapered refractory crucible containing molten flux, precious metal doré prill bead, and heat flames."""
    # Tapered crucible cup outline in center
    crucible_pts = [(220, 820), (780, 820), (650, 250), (350, 250)]
    parts = [
        stroke(crucible_pts, 40, closed=True),
        # Molten slag wave surface inside crucible at y=630
        sine_wave(265, 630, 735, 630, amp=26, cycles=2.0, width=30),
        # Precious metal Au-Ag doré bead / lead button settled at bottom of crucible
        circle(500, 365, 80),
        # Radiant sparkle rays around precious metal bead
        line(500, 475, 500, 535, 26),
        line(390, 420, 340, 455, 26),
        line(610, 420, 660, 455, 26),
        # Furnace flame tongues rising around crucible base
        sine_wave(260, 80, 260, 220, amp=24, cycles=1.0, width=32),
        sine_wave(500, 70, 500, 210, amp=28, cycles=1.0, width=36),
        sine_wave(740, 80, 740, 220, amp=24, cycles=1.0, width=32),
    ]
    return union_all(parts)


def gc_isotope_ratio_analysis():
    """Isotope Ratio Mass Analysis: Ion source beam splitting in magnetic sector into light, medium, and heavy isotope trajectories."""
    # Clean fan of 3 curved isotope beams (light = tight bend, medium = middle, heavy = shallow bend)
    # All starting at (180, 220) going up through magnet sector around (260, 520) and bending right to collector cups
    beam1 = stroke([(180, 140), (180, 420), (240, 580), (400, 740), (680, 820)], 30)
    beam2 = stroke([(180, 140), (180, 420), (260, 540), (450, 620), (740, 650)], 30)
    beam3 = stroke([(180, 140), (180, 420), (280, 500), (490, 495), (790, 480)], 30)

    parts = [
        # Ion source block at bottom-left
        rounded_rect(100, 90, 260, 230, 24),
        # Magnetic sector outline (trapezoidal prism around bend zone)
        stroke([(110, 380), (350, 380), (450, 680), (130, 680)], 34, closed=True),
        # Three diverging isotopic mass trajectories
        beam1,
        beam2,
        beam3,
        # Faraday collector cups at ends of the 3 beams
        stroke([(720, 885), (840, 885), (840, 765), (720, 765)], 32),
        stroke([(775, 715), (895, 715), (895, 595), (775, 595)], 32),
        stroke([(815, 545), (930, 545), (930, 425), (815, 425)], 32),
        # Ion impact dots inside Faraday cups
        circle(775, 825, 28),
        circle(830, 655, 28),
        circle(870, 485, 28),
    ]
    return union_all(parts)


def gc_alteration_zonation():
    """Hydrothermal Alteration Zonation Halo: Concentric porphyry alteration shells (potassic core, phyllic, argillic, propylitic halo)."""
    cx, cy = 500, 470
    parts = [
        # Outer propylitic halo (dashed ellipse)
        ellipse_outline(cx, cy, 415, 340, 28),
        # Intermediate argillic shell
        ellipse_outline(cx, cy, 295, 235, 32),
        # Inner phyllic (quartz-sericite-pyrite) shell
        ellipse_outline(cx, cy, 180, 140, 36),
        # Central potassic core + feeder stock at bottom
        ellipse(cx, cy, 82, 62),
        rect(455, 80, 545, 430),
        # Outward radial zoning arrows indicating thermal/chemical gradient
        arrow(500, 610, 500, 895, 30, 80, 46),
        arrow(210, 470, 65, 470, 28, 75, 44),
        arrow(790, 470, 935, 470, 28, 75, 44),
    ]
    return union_all(parts)


def gc_geochem_anomaly_contours():
    """Geochemical Iso-Grade Contour Map: Spatial multi-ring isoconcentration contours converging on a high-grade pathfinder anomaly bullseye."""
    parts = [
        # Outer asymmetric geochemical dispersion contour
        stroke(
            [
                (110, 480),
                (170, 760),
                (460, 880),
                (820, 790),
                (900, 490),
                (760, 170),
                (410, 110),
                (150, 240),
            ],
            32,
            closed=True,
        ),
        # Intermediate contour
        stroke(
            [
                (235, 500),
                (290, 700),
                (510, 775),
                (750, 690),
                (790, 490),
                (670, 275),
                (430, 235),
                (260, 340),
            ],
            34,
            closed=True,
        ),
        # Inner high-grade contour
        ellipse_outline(540, 520, 155, 130, 38, angle_deg=18),
        # Bullseye anomaly peak + target crosshairs
        circle(555, 530, 62),
        line(555, 340, 555, 720, 26),
        line(365, 530, 745, 530, 26),
    ]
    return union_all(parts)


def gc_ternary_classification():
    """Geochemical Ternary Diagram (AFM / QAPF): Equilateral triangle with internal classification field boundaries and plotted sample cluster."""
    # Equilateral triangle vertices: Top (500, 890), Bottom-Left (110, 160), Bottom-Right (890, 160)
    tri = [(500, 890), (110, 160), (890, 160)]
    parts = [
        stroke(tri, 40, closed=True),
        # Internal petrogenetic / classification field boundaries (e.g. QAPF / AFM tholeiitic-calc-alkaline curve)
        line(305, 525, 695, 525, 28),
        line(395, 695, 605, 695, 26),
        line(500, 525, 500, 160, 28),
        stroke([(230, 385), (500, 470), (770, 385)], 28),
        # Plotted geochemical differentiation trend / sample points
        circle(370, 330, 34),
        circle(450, 420, 34),
        circle(555, 455, 36),
        circle(640, 360, 34),
    ]
    return union_all(parts)


def gc_eh_ph_pourbaix():
    """Eh-pH (Pourbaix) Stability Diagram: Redox potential (Eh) vs acidity (pH) axes, water stability limits, and aqueous/solid species fields."""
    parts = [
        # Eh (vertical) and pH (horizontal) axes
        arrow(130, 110, 130, 910, 36, 90, 52),
        arrow(110, 130, 920, 130, 36, 90, 52),
        # Upper and lower stability limits of water (sloping parallel dashed lines)
        dashed_line(130, 820, 890, 540, 28, dash_count=7),
        dashed_line(130, 440, 890, 160, 28, dash_count=7),
        # Phase boundary lines separating dissolved ion (left) from oxide/sulfide precipitates (right)
        line(470, 280, 470, 695, 34),
        line(470, 480, 880, 330, 34),
        line(130, 560, 470, 480, 34),
        # Field indicator symbols (solid mineral crystal in upper-right field, aqueous circle in left field)
        regular_poly(680, 530, 52, 4, 45),
        circle(290, 620, 42),
    ]
    return union_all(parts)


def gc_downhole_geochem_log():
    """Downhole Multi-Element Assay Log: Inclined drillhole trace with perpendicular assay histogram bars along depth."""
    # Drillhole axis from top-left collar (210, 870) to bottom-right EOH (650, 110)
    # Angle is -60 degrees; perpendicular normal to upper-right is +30 degrees (cos=0.866, sin=0.5)
    x0, y0 = 200, 860
    x1, y1 = 620, 120
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux  # points to upper-right

    # Assay histogram bar lengths along drillhole intervals
    bar_lengths = [75, 110, 65, 210, 340, 275, 130, 80, 145, 70]
    n_bars = len(bar_lengths)
    parts = [
        # Surface ground line & drillhole collar circle
        line(80, 860, 420, 860, 34),
        disk_ring(x0, y0, 48, 30),
        # Drillhole trace line
        line(x0, y0, x1, y1, 36),
    ]
    for i, blen in enumerate(bar_lengths):
        t_mid = (i + 0.5) / n_bars
        bx = x0 + dx * t_mid
        by = y0 + dy * t_mid
        ex = bx + nx * blen
        ey = by + ny * blen
        parts.append(line(bx, by, ex, ey, 46, cap="butt"))
    return union_all(parts)


def gc_hydrothermal_circulation():
    """Hydrothermal Fluid Convection Cell: Magmatic heat source at base driving symmetrically convecting fluid loops and central quartz-sulfide vein."""
    parts = [
        # Basal magma chamber heat dome at bottom
        sector(500, 70, 240, 0, 180),
        # Central vertical hydrothermal upflow pipe / vein system
        arrow(500, 320, 500, 880, 44, 105, 60),
        # Left convection cell (descending cold meteoric water on far left, heating near base, rising in center)
        curved_arrow(275, 540, 185, 65, 295, 34, 90, 52),
        # Right convection cell (mirror image on right)
        curved_arrow(725, 540, 185, 115, -115, 34, 90, 52),
        # Vein stockwork branches at top of central conduit
        line(500, 680, 370, 810, 30),
        line(500, 680, 630, 810, 30),
        line(500, 560, 390, 670, 28),
        line(500, 560, 610, 670, 28),
    ]
    return union_all(parts)


def gc_supergene_leaching():
    """Supergene Leaching & Enrichment Blanket: Meteoric water percolating through oxidized leached cap into a rich supergene sulfide blanket above protore."""
    parts = [
        # Ground surface + infiltrating rainwater droplets/arrows at top
        line(80, 780, 920, 780, 34),
        arrow(260, 920, 260, 610, 30, 78, 45),
        arrow(500, 920, 500, 610, 30, 78, 45),
        arrow(740, 920, 740, 610, 30, 78, 45),
        # Oxidized leached zone (540..780) -> Water table at y=530
        dashed_line(80, 530, 920, 530, 28, dash_count=8),
        # Supergene enrichment blanket (bold solid lens between y=320 and y=470)
        rounded_rect(120, 320, 880, 465, 65),
        # Hypogene primary protore zone below (y=90..260) with disseminated sulfide dots
        line(80, 250, 920, 250, 28),
        circle(220, 160, 34),
        circle(410, 175, 34),
        circle(600, 155, 34),
        circle(790, 170, 34),
    ]
    # Cut "+" enrichment symbols out of the solid supergene blanket so it looks super sharp
    cuts = union_all(
        [
            line(260, 392, 340, 392, 26),
            line(300, 352, 300, 432, 26),
            line(460, 392, 540, 392, 26),
            line(500, 352, 500, 432, 26),
            line(660, 392, 740, 392, 26),
            line(700, 352, 700, 432, 26),
        ]
    )
    return diff(union_all(parts), cuts)


def gc_redox_front_roll():
    """Geochemical Roll-Front Redox Interface: Crescentic uranium/redox roll front migrating down-dip between confining mudstone beds."""
    # Confining upper and lower shale/mudstone aquitards
    # Crescentic roll front nose facing right (x=680, y=500)
    crescent = diff(
        ellipse(460, 500, 260, 230),
        ellipse(320, 500, 240, 165),
    )
    parts = [
        # Upper and lower confining beds
        line(70, 790, 930, 790, 40),
        line(70, 210, 930, 210, 40),
        # Oxidized groundwater flow arrows entering from left into the crescentic roll front
        arrow(95, 590, 370, 590, 34, 85, 48),
        arrow(95, 410, 370, 410, 34, 85, 48),
        # Solid crescentic roll-front ore body at redox interface
        crescent,
        # Reduced zone ahead of front on right (stippled/dotted pyrite/reductants)
        circle(790, 620, 32),
        circle(855, 500, 36),
        circle(790, 380, 32),
    ]
    return union_all(parts)


def gc_magmatic_differentiation():
    """Magmatic Differentiation & Crystal Settling: Domed magma chamber with dense early-formed phenocrysts settling into basal cumulate layers."""
    # Domed magma chamber outline
    chamber_pts = [
        (140, 120),
        (140, 520),
        (220, 760),
        (370, 880),
        (630, 880),
        (780, 760),
        (860, 520),
        (860, 120),
    ]
    parts = [
        stroke(chamber_pts, 38, closed=True),
        # Basal cumulate layering at bottom of chamber
        line(140, 235, 860, 235, 32),
        line(140, 340, 860, 340, 30),
        # Settled cumulate crystals in bottom layer
        regular_poly(260, 178, 42, 6),
        regular_poly(420, 178, 42, 6),
        regular_poly(580, 178, 42, 6),
        regular_poly(740, 178, 42, 6),
        # Euhedral crystals nucleating in upper melt and sinking (with downward arrows)
        regular_poly(330, 680, 55, 6, 15),
        arrow(330, 600, 330, 400, 30, 78, 45),
        regular_poly(650, 710, 55, 6, 45),
        arrow(650, 630, 650, 430, 30, 78, 45),
        # Evolved residual melt/volatile arrow rising in center
        arrow(500, 430, 500, 800, 32, 82, 48),
    ]
    return union_all(parts)


def gc_element_dispersion_halo():
    """Primary & Secondary Geochemical Dispersion Plume: Subsurface orebody shedding an upward/down-gradient dispersion fan into regolith and soil."""
    parts = [
        # Sloping ground surface at top
        line(70, 860, 930, 720, 36),
        # Base of regolith / top of bedrock unconformity
        dashed_line(70, 480, 930, 360, 28, dash_count=8),
        # Deep primary steeply-dipping orebody at bottom-left
        poly([(160, 80), (330, 80), (410, 445), (240, 465)]),
        # Secondary dispersion plume arrows fanning upward & down-slope to the right
        arrow(330, 470, 560, 690, 32, 82, 46),
        arrow(390, 430, 790, 560, 32, 82, 46),
        # Dispersed pathfinder element dots in upper soil horizon fading rightward
        circle(310, 660, 52),
        circle(460, 720, 44),
        circle(640, 680, 38),
        circle(790, 655, 32),
        circle(900, 625, 26),
    ]
    return union_all(parts)


GEOCHEMICAL_ICONS: List[Dict[str, Any]] = [
    {
        "id": "gc_soil_stream_sampling",
        "name": "Soil & Stream Geochemical Sampling",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE02E,
        "description": "Helical soil auger and systematic spatial sampling grid highlighting an anomalous pathfinder station.",
        "keywords": ["soil sampling", "stream sediment", "auger", "sampling grid", "exploration geochemistry"],
        "builder": gc_soil_stream_sampling,
    },
    {
        "id": "gc_pxrf_analyzer",
        "name": "Portable XRF (pXRF) Analyzer",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE02F,
        "description": "Handheld portable X-ray fluorescence analyzer irradiating a rock specimen and measuring secondary X-ray emission.",
        "keywords": ["pxrf", "xrf", "handheld analyzer", "fluorescence", "elemental analysis", "field geochemistry"],
        "builder": gc_pxrf_analyzer,
    },
    {
        "id": "gc_icp_ms_spectrometry",
        "name": "ICP-MS / OES Mass Spectrometry",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE030,
        "description": "High-resolution elemental mass/optical emission spectrum with sharp analytical peaks above detection limit.",
        "keywords": ["icp-ms", "icp-oes", "mass spectrometry", "trace elements", "spectrum", "detection limit"],
        "builder": gc_icp_ms_spectrometry,
    },
    {
        "id": "gc_fire_assay",
        "name": "Fire Assay & Cupellation",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE031,
        "description": "High-temperature refractory assay crucible separating molten silicate slag from a dense precious-metal doré bead.",
        "keywords": ["fire assay", "cupellation", "crucible", "gold assay", "dore bead", "precious metals"],
        "builder": gc_fire_assay,
    },
    {
        "id": "gc_isotope_ratio_analysis",
        "name": "Radiogenic & Stable Isotope Analysis",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE032,
        "description": "Magnetic-sector mass separator deflecting light, medium, and heavy isotopic ion beams into Faraday collectors.",
        "keywords": ["isotopes", "mass sector", "faraday cup", "geochronology", "stable isotopes", "radiogenic"],
        "builder": gc_isotope_ratio_analysis,
    },
    {
        "id": "gc_alteration_zonation",
        "name": "Hydrothermal Alteration Zonation",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE033,
        "description": "Concentric hydrothermal alteration shells (potassic core, phyllic, argillic, and propylitic outer halo).",
        "keywords": ["alteration halo", "zonation", "potassic", "phyllic", "argillic", "propylitic", "porphyry"],
        "builder": gc_alteration_zonation,
    },
    {
        "id": "gc_geochem_anomaly_contours",
        "name": "Geochemical Iso-Grade Contour Map",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE034,
        "description": "Spatial iso-concentration geochemical contours converging on a high-grade anomaly bullseye.",
        "keywords": ["geochemical contour", "isograd", "anomaly map", "pathfinder", "bullseye", "kriging"],
        "builder": gc_geochem_anomaly_contours,
    },
    {
        "id": "gc_ternary_classification",
        "name": "Geochemical Ternary Diagram",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE035,
        "description": "Three-component equilateral ternary plot (AFM / QAPF / major oxides) with petrogenetic fields and sample trend.",
        "keywords": ["ternary diagram", "afm", "qapf", "lithogeochemistry", "classification plot", "oxides"],
        "builder": gc_ternary_classification,
    },
    {
        "id": "gc_eh_ph_pourbaix",
        "name": "Eh-pH (Pourbaix) Stability Diagram",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE036,
        "description": "Redox potential (Eh) vs. pH phase diagram showing water stability limits and mineral/aqueous stability fields.",
        "keywords": ["eh-ph", "pourbaix", "redox", "thermodynamics", "stability field", "aqueous geochemistry"],
        "builder": gc_eh_ph_pourbaix,
    },
    {
        "id": "gc_downhole_geochem_log",
        "name": "Downhole Multi-Element Assay Log",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE037,
        "description": "Inclined exploration drillhole trace displaying perpendicular interval assay grade histogram bars.",
        "keywords": ["downhole assay", "strip log", "drillhole geochemistry", "grade intercept", "histogram"],
        "builder": gc_downhole_geochem_log,
    },
    {
        "id": "gc_hydrothermal_circulation",
        "name": "Hydrothermal Fluid Convection",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE038,
        "description": "Magmatic heat source driving convective hydrothermal fluid circulation cells and central stockwork vein deposition.",
        "keywords": ["hydrothermal", "convection cell", "fluid flow", "vein deposition", "stockwork", "ore genesis"],
        "builder": gc_hydrothermal_circulation,
    },
    {
        "id": "gc_supergene_leaching",
        "name": "Supergene Leaching & Enrichment",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE039,
        "description": "Meteoric water percolating through a leached gossan cap to precipitate a secondary supergene enrichment blanket.",
        "keywords": ["supergene", "leached cap", "gossan", "enrichment blanket", "oxidation", "weathering"],
        "builder": gc_supergene_leaching,
    },
    {
        "id": "gc_redox_front_roll",
        "name": "Roll-Front Redox Migration",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE03A,
        "description": "Oxidized aquifer groundwater migrating down-dip to precipitate a crescentic roll-front orebody at a redox boundary.",
        "keywords": ["roll front", "redox front", "uranium", "aquifer", "oxidation reduction", "precipitation"],
        "builder": gc_redox_front_roll,
    },
    {
        "id": "gc_magmatic_differentiation",
        "name": "Magmatic Differentiation & Cumulates",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE03B,
        "description": "Fractional crystallization in a magma chamber with dense early phenocrysts settling into basal cumulate horizons.",
        "keywords": ["magmatic differentiation", "fractional crystallization", "cumulate", "bowen", "crystal settling"],
        "builder": gc_magmatic_differentiation,
    },
    {
        "id": "gc_element_dispersion_halo",
        "name": "Geochemical Dispersion Halo",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE03C,
        "description": "Deep primary orebody shedding a secondary hydromorphic and mechanical pathfinder dispersion plume through regolith.",
        "keywords": ["dispersion halo", "secondary dispersion", "pathfinder plume", "regolith", "hydromorphic"],
        "builder": gc_element_dispersion_halo,
    },
]
