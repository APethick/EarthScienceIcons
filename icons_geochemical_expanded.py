"""
Expanded Geochemistry Icon Definitions (43 additional icons, U+E081..U+E0AB).
Together with the 21 existing geochemistry icons, this provides 64 dedicated,
domain-accurate Geochemistry icons covering:
  - 22 Analytical & Field Geochemical Methods
  - 22 Geochemical Earth Model Types & Classification Diagrams
  - 20 Geochemical Processes, Reactions & Cycles
Aligned with:
  - C:\\projects\\opus\\opus.geo.geochemistry (assay, pathfinder, mineralogy, thermodynamics, melt, hyperspectral)
  - International exploration geochemistry, petrology, and isotope standards.
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


# =============================================================================
# A. Expanded Geochemical Analytical Methods (17 icons: U+E081..U+E091)
# =============================================================================

def gc_la_icp_ms_laser():
    """Laser Ablation ICP-MS (LA-ICP-MS): Pulsed laser beam firing at mineral crystal in sample cell, generating ablation aerosol plume."""
    parts = [
        # Laser optics objective housing at top
        rounded_rect(420, 780, 580, 920, 20),
        # Focused laser beam cone narrowing onto target crystal
        poly([(460, 780), (540, 780), (505, 410), (495, 410)]),
        # Polished sample mount disc & target zircon crystal at bottom
        rounded_rect_outline(160, 160, 840, 360, 30, 34),
        regular_poly(500, 350, 75, 6, 30),
        # Ablation micro-crater & luminous aerosol plume expanding upward to sample gas exit
        circle(500, 420, 36),
        curved_arrow(500, 430, 220, 45, 135, 30, 75, 42),
        curved_arrow(500, 430, 220, 135, 45, 30, 75, 42),
        # Helium carrier gas sweep arrow (left-to-right through cell)
        arrow(180, 480, 340, 480, 28, 70, 40),
        arrow(660, 480, 820, 480, 28, 70, 40),
    ]
    return union_all(parts)


def gc_epma_wds_microprobe():
    """Electron Probe Microanalyzer (EPMA / WDS): Focused electron beam with Rowland circle and curved crystal spectrometer."""
    cx, cy = 500, 520
    parts = [
        # Electron gun column at top
        rect(455, 760, 545, 910),
        arrow(500, 760, 500, 260, 36, 85, 48),
        # Polished thin section sample at bottom
        rect(240, 150, 760, 230),
        # Circular Rowland focal spectrometer circle on right
        disk_ring(640, 480, 240, 32),
        # Curved diffraction crystal & proportional counter detector on circle
        rounded_rect(760, 620, 880, 700, 15),
        circle(500, 230, 40),
    ]
    return union_all(parts)


def gc_xrd_diffractometer():
    """X-Ray Powder Diffraction (XRD): X-ray tube, powder mount, and detector scanning 2-theta circle with Bragg peak spectrum."""
    parts = [
        # Goniometer circular arc
        arc(500, 260, 400, 25, 155, 34),
        # Incident X-ray tube source on left arm
        rect(150, 520, 250, 640),
        arrow(250, 530, 480, 280, 30, 75, 42),
        # Flat powder sample stage in center
        rect(360, 220, 640, 270),
        # Diffracted beam & detector on right arm
        arrow(520, 280, 750, 530, 30, 75, 42),
        rounded_rect(750, 520, 850, 640, 18),
        # Bragg diffraction peaks (d-spacing spectrum) in upper center
        stroke([(340, 660), (410, 660), (450, 880), (490, 660), (550, 660), (580, 810), (610, 660), (660, 660)], 32),
    ]
    return union_all(parts)


def gc_xanes_synchrotron():
    """Synchrotron X-Ray Absorption Spectroscopy (XANES / EXAFS): Storage ring with tangential X-ray beam and oxidation-state absorption edge."""
    # XANES white-line absorption edge curve
    edge_pts = [
        (480, 180),
        (560, 180),
        (610, 480),  # Pre-edge peak
        (640, 340),
        (690, 840),  # Intense white-line peak (oxidation state marker)
        (730, 620),
        (780, 710),
        (830, 600),
        (890, 630),
    ]
    parts = [
        # Synchrotron storage ring arc on left
        arc(260, 500, 220, -75, 75, 42),
        # Tangential intense relativistic X-ray beam arrow
        arrow(260, 720, 460, 720, 38, 90, 52),
        # Undulator magnet poles
        rect(170, 745, 230, 805),
        rect(290, 745, 350, 805),
        rect(170, 635, 230, 695),
        rect(290, 635, 350, 695),
        # Absorption edge spectrum on right
        line(480, 180, 910, 180, 32),
        stroke(edge_pts, 36),
    ]
    return union_all(parts)


def gc_libs_laser_plasma():
    """Laser-Induced Breakdown Spectroscopy (LIBS): Pulsed laser focusing on rock surface generating atomic spark emission plasma."""
    parts = [
        # Laser head at top
        rounded_rect(410, 780, 590, 920, 20),
        # Converging laser beam
        line(440, 780, 500, 400, 30),
        line(560, 780, 500, 400, 30),
        # Exploding plasma spark star on rock surface
        regular_poly(500, 400, 115, 8, 22.5),
        # Rock sample at base
        poly([(120, 120), (880, 120), (840, 340), (160, 340)]),
        # Fiber-optic spectrometer collection cone on right
        arrow(580, 460, 780, 620, 28, 72, 40),
        circle(810, 645, 38),
    ]
    return union_all(parts)


def gc_ftir_raman_spectroscopy():
    """FTIR & Raman Vibrational Spectroscopy: Molecule vibrating with shifted scattered photon spectrum."""
    parts = [
        # Central triatomic molecule (e.g. H2O or CO2) with stretching vibration springs
        circle(500, 720, 70),
        circle(280, 610, 50),
        circle(720, 610, 50),
        # Chemical bonding vibration coils
        sine_wave(330, 635, 430, 695, amp=20, cycles=2.5, width=28),
        sine_wave(570, 695, 670, 635, amp=20, cycles=2.5, width=28),
        # Raman shift / infrared absorption spectrum at bottom
        line(120, 150, 880, 150, 34),
        stroke([(160, 150), (250, 150), (310, 440), (370, 150), (470, 150), (530, 520), (590, 150), (710, 150), (760, 360), (810, 150)], 36),
    ]
    return union_all(parts)


def gc_four_acid_total_digest():
    """Four-Acid Near-Total Digestion: Hotplate digestion vessel with boiling HF-HNO3-HClO4-HCl acid dissolving silicate rock."""
    parts = [
        # Heated hotplate base
        rect(180, 100, 820, 175),
        # Digestion beaker / tube
        stroke([(280, 860), (280, 200), (720, 200), (720, 860)], 38),
        # Boiling acid surface wave
        sine_wave(280, 480, 720, 480, amp=24, cycles=2.0, width=30),
        # Completely dissolved rock clasts breaking into ions at bottom
        circle(420, 320, 38),
        circle(580, 320, 38),
        # Ascending acid vapor fumes (HF/HClO4)
        sine_wave(380, 540, 380, 790, amp=28, cycles=2.0, width=28),
        sine_wave(620, 540, 620, 790, amp=28, cycles=2.0, width=28),
    ]
    return union_all(parts)


def gc_aqua_regia_partial_digest():
    """Aqua Regia Partial Digestion: 3:1 HCl:HNO3 reaction flask selectively leaching sulfides from quartz matrix."""
    parts = [
        # Conical Erlenmeyer reaction flask
        stroke([(440, 910), (440, 680), (210, 170), (790, 170), (560, 680), (560, 910)], 38),
        # Partial digestion meniscus
        line(265, 300, 735, 300, 34),
        # Insoluble residual quartz grain remaining at bottom
        regular_poly(500, 235, 52, 6),
        # Rising nascent chlorine / nitrosyl chloride bubbles
        circle(380, 440, 26),
        circle(620, 420, 26),
        circle(480, 560, 32),
    ]
    return union_all(parts)


def gc_cyanide_bottle_roll():
    """Cyanide Bottle Roll Leach Test: Rotating cylindrical bottle on roller shafts measuring gold extraction kinetics."""
    parts = [
        # Twin roller shafts at bottom
        circle(320, 210, 65),
        circle(680, 210, 65),
        line(140, 130, 860, 130, 36),
        # Cylindrical roll bottle lying horizontally
        rounded_rect_outline(180, 290, 820, 750, 45, 38),
        rect(820, 440, 890, 600),
        # Slurry contents inside bottle & rotation arrow
        curved_arrow(500, 520, 135, 35, 235, 34, 80, 46),
        circle(430, 430, 28),
        circle(570, 430, 28),
    ]
    return union_all(parts)


def gc_sequential_extraction():
    """Sequential Chemical Extraction: 5-step fraction rack (Water-soluble, Exchangeable, Carbonate, Fe-Mn Oxides, Residual)."""
    tubes_x = [190, 345, 500, 655, 810]
    fluid_levels = [320, 430, 540, 650, 760]
    parts = [
        # Rack stand
        line(100, 160, 900, 160, 38),
        line(100, 520, 900, 520, 26),
    ]
    for x, f_y in zip(tubes_x, fluid_levels):
        parts.append(stroke([(x - 42, 860), (x - 42, 220), (x + 42, 220), (x + 42, 860)], 26))
        parts.append(rect(x - 36, 220, x + 36, f_y))
    return union_all(parts)


def gc_gas_chromatography_ms():
    """Gas Chromatography Mass Spectrometry (GC-MS): Helical capillary column separating biomarker hydrocarbons into mass peaks."""
    parts = [
        # Helical capillary GC column coils inside oven on left
        arc(310, 640, 140, 0, 360, 30),
        arc(310, 520, 140, 0, 360, 30),
        arc(310, 400, 140, 0, 360, 30),
        # Transfer line to MS on right
        arrow(450, 520, 570, 520, 34, 85, 48),
        # Total Ion Chromatogram (TIC) peaks on right (pristane, phytane, steranes)
        line(570, 200, 910, 200, 32),
        stroke([(600, 200), (640, 460), (670, 200), (730, 780), (760, 200), (820, 610), (860, 200)], 36),
    ]
    return union_all(parts)


def gc_sims_shrimp_microprobe():
    """Secondary Ion Mass Spectrometry (SIMS / SHRIMP): High-energy primary ion beam sputtering secondary ions into sector."""
    parts = [
        # Primary ion gun at top-left firing at 45 deg onto sample
        stroke([(160, 880), (320, 720)], 42),
        arrow(280, 760, 480, 560, 36, 85, 48),
        # Target sample stage in center
        rect(360, 480, 640, 540),
        circle(500, 550, 28),
        # Secondary sputtered ions entering electrostatic analyzer
        arrow(520, 560, 720, 760, 36, 85, 48),
        rounded_rect_outline(660, 700, 890, 890, 30, 32),
    ]
    return union_all(parts)


def gc_tims_thermal_ionization():
    """Thermal Ionization Mass Spectrometry (TIMS): Heated high-vacuum rhenium ribbon filament evaporating high-precision isotopes."""
    parts = [
        # Vacuum chamber bell jar outline
        rounded_rect_outline(160, 160, 840, 880, 65, 36),
        # Twin filament electrical posts & heated rhenium ribbon filament
        line(340, 240, 340, 500, 36),
        line(660, 240, 660, 500, 36),
        stroke([(340, 500), (500, 580), (660, 500)], 42),
        # Radiant thermal heat glow sparkles
        line(500, 620, 500, 700, 28),
        line(420, 560, 370, 610, 28),
        line(580, 560, 630, 610, 28),
        # Focused positive ion beam entering acceleration slit at top
        arrow(500, 640, 500, 860, 36, 90, 52),
    ]
    return union_all(parts)


def gc_stable_isotope_gas_irms():
    """Stable Isotope Gas Ratio Mass Spec: Viscous gas capillary inlet splitting into Faraday multi-collector cups."""
    parts = [
        # Dual gas inlet capillary tubes
        line(120, 720, 320, 720, 32),
        line(120, 600, 320, 600, 32),
        disk_ring(360, 660, 60, 28),
        # Electron ionization box & magnetic sector flight tube
        stroke([(420, 660), (620, 660), (780, 380)], 38),
        # Triple Faraday collectors for delta13C/delta18O ratios
        rect(820, 480, 890, 560),
        rect(820, 360, 890, 440),
        rect(820, 240, 890, 320),
    ]
    return union_all(parts)


def gc_fluid_inclusion_microtherm():
    """Fluid Inclusion Microthermometry: Biphase inclusion (liquid water + vapor bubble + halite cube) inside crystal host."""
    parts = [
        # Outer quartz crystal prism boundary
        regular_poly(500, 500, 410, 6, 30),
        # Fluid inclusion negative crystal cavity
        ellipse_outline(500, 500, 240, 160, 34, angle_deg=-15),
        # Vapor bubble inside fluid cavity
        circle(580, 520, 62),
        # Halite daughter cube in inclusion
        regular_poly(410, 460, 42, 4, 15),
    ]
    return union_all(parts)


def gc_radon_emanometry():
    """Radon Soil-Gas Emanometry: Hollow sampling probe in ground with scintillation chamber detecting alpha particle tracks."""
    parts = [
        # Ground surface line
        line(80, 560, 920, 560, 36),
        # Soil-gas drive point probe penetrating regolith
        stroke([(470, 910), (470, 220), (500, 140), (530, 220), (530, 910)], 30),
        # Slotted radon gas intake holes at bottom of probe
        circle(500, 310, 20),
        circle(500, 240, 20),
        # Alpha scintillation flask / counter at surface
        rounded_rect_outline(280, 640, 440, 880, 24, 30),
        line(440, 760, 470, 760, 28),
        # Alpha particle decay track stars (Rn-222 -> Po-218)
        circle(360, 760, 32),
        line(320, 760, 400, 760, 20),
        line(360, 720, 360, 800, 20),
    ]
    return union_all(parts)


def gc_biogeochem_vegetation():
    """Biogeochemical Vegetation Sampling: Tree roots extracting deep anomalous pathfinder elements into foliage."""
    parts = [
        # Ground surface
        line(80, 440, 920, 440, 34),
        # Tree canopy & trunk
        rect(460, 440, 540, 680),
        circle(500, 780, 140),
        circle(380, 720, 110),
        circle(620, 720, 110),
        # Deep penetrating root system reaching buried ore body
        stroke([(500, 440), (420, 300), (340, 160)], 32),
        stroke([(500, 440), (580, 300), (660, 160)], 32),
        stroke([(500, 440), (500, 140)], 32),
        # Upward elemental translocation arrows through trunk
        arrow(500, 200, 500, 620, 28, 70, 40),
    ]
    return union_all(parts)


# =============================================================================
# B. Expanded Geochemical Earth Models & Diagrams (15 icons: U+E092..U+E0A0)
# =============================================================================

def gc_ree_chondrite_spidergram():
    """Chondrite-Normalized REE Spidergram: La to Lu plot with negative Europium anomaly dip (Eu/Eu*)."""
    # Normalized REE curve from La to Lu with sharp Eu dip
    ree_pts = [
        (130, 820),  # La
        (220, 760),  # Ce
        (310, 710),  # Pr
        (400, 660),  # Nd
        (480, 590),  # Sm
        (540, 340),  # Eu anomaly dip!
        (610, 540),  # Gd
        (700, 480),  # Tb-Dy
        (790, 440),  # Er-Tm
        (880, 420),  # Yb-Lu
    ]
    parts = [
        # Logarithmic concentration axes
        arrow(130, 160, 130, 920, 34, 85, 48),
        arrow(100, 200, 920, 200, 34, 85, 48),
        # Chondrite normalized REE curve
        stroke(ree_pts, 38),
        # Eu anomaly caliper arrow
        arrow(540, 560, 540, 370, 26, 65, 36),
    ]
    for pt in ree_pts:
        parts.append(circle(pt[0], pt[1], 28))
    return union_all(parts)


def gc_primitive_mantle_spidergram():
    """Primitive Mantle Multi-Element Spidergram: Incompatible trace elements with subduction Nb-Ta and Ti troughs."""
    pts = [
        (120, 860),  # Cs-Rb
        (200, 810),  # Ba
        (270, 780),  # Th-U
        (350, 410),  # Nb-Ta trough (arc signature)
        (430, 740),  # K
        (510, 680),  # La-Ce
        (590, 640),  # Pb peak
        (670, 520),  # Sr
        (750, 320),  # Ti trough
        (830, 460),  # Y-Yb
        (890, 440),  # Lu
    ]
    parts = [
        arrow(120, 150, 120, 920, 34, 85, 48),
        arrow(90, 180, 920, 180, 34, 85, 48),
        stroke(pts, 36),
    ]
    for pt in pts:
        parts.append(circle(pt[0], pt[1], 26))
    return union_all(parts)


def gc_tas_volcanic_diagram():
    """Total Alkali vs Silica (TAS) Diagram: Volcanic rock classification grid (Basalt, Andesite, Dacite, Rhyolite)."""
    parts = [
        # Axes: Na2O+K2O (vertical) vs SiO2 (horizontal)
        arrow(120, 140, 120, 910, 36, 90, 52),
        arrow(90, 160, 920, 160, 36, 90, 52),
        # Alkaline vs Subalkaline boundary curve
        stroke([(200, 260), (420, 490), (680, 710), (880, 820)], 38),
        # Internal TAS classification cell boundaries
        line(380, 160, 380, 600, 24),
        line(560, 160, 560, 720, 24),
        line(740, 160, 740, 840, 24),
        line(120, 440, 560, 440, 24),
    ]
    return union_all(parts)


def gc_qapf_ternary_double():
    """Double Ternary QAPF Diamond: Plutonic & volcanic classification (Quartz, Alkali feldspar, Plagioclase, Foids)."""
    # Upper triangle (Q-A-P) and lower inverted triangle (F-A-P)
    # Top Q (500, 900), Left A (120, 500), Right P (880, 500), Bottom F (500, 100)
    diamond = [(500, 900), (880, 500), (500, 100), (120, 500)]
    parts = [
        stroke(diamond, 38, closed=True),
        line(120, 500, 880, 500, 34),  # A-P tie line
        # Internal field boundaries (Granite, Granodiorite, Tonalite, Syenite, Gabbro)
        line(500, 900, 500, 500, 26),
        line(340, 660, 660, 660, 24),
        line(340, 340, 660, 340, 24),
    ]
    return union_all(parts)


def gc_pearce_tectonic_discrimination():
    """Pearce Tectonic Discrimination Diagram: Trace element discrimination (Nb vs Y / Rb vs Y+Nb) separating tectonic settings."""
    parts = [
        arrow(130, 140, 130, 910, 36, 90, 52),
        arrow(100, 160, 920, 160, 36, 90, 52),
        # Tectonic field dividers separating VAG, ORG, WPG, syn-COLG
        line(130, 560, 860, 560, 32),
        line(520, 160, 520, 900, 32),
        line(520, 560, 880, 840, 30),
        # Plotted sample clusters in Volcanic Arc and Within-Plate fields
        circle(320, 360, 36),
        circle(710, 740, 36),
    ]
    return union_all(parts)


def gc_activity_activity_diagram():
    """Activity-Activity Diagram (log aK+/aH+ vs log aSiO2): Hydrothermal mineral stability fields (K-feldspar, Muscovite, Kaolinite)."""
    parts = [
        arrow(130, 130, 130, 910, 36, 90, 52),
        arrow(100, 150, 920, 150, 36, 90, 52),
        # Quartz saturation vertical boundary on right
        dashed_line(780, 150, 780, 890, 28, dash_count=7),
        # Muscovite-Kaolinite and Muscovite-K-feldspar phase boundary lines
        line(130, 420, 540, 420, 34),
        line(540, 420, 540, 780, 34),
        line(540, 420, 880, 640, 34),
    ]
    return union_all(parts)


def gc_zircon_upb_concordia():
    """Wetherill U-Pb Concordia Diagram: 206Pb/238U vs 207Pb/235U concordia curve with discordant lead-loss line."""
    # Concordia curved arc from (180, 220) to (840, 820)
    concordia_pts = []
    for i in range(41):
        t = i / 40.0
        x = 180 + 660 * t
        y = 220 + 600 * math.sqrt(t)
        concordia_pts.append((x, y))
    parts = [
        arrow(150, 150, 150, 920, 36, 90, 52),
        arrow(110, 180, 920, 180, 36, 90, 52),
        stroke(concordia_pts, 40),
        # Discordia chord line intersecting concordia at upper and lower intercepts
        dashed_line(260, 180, 780, 780, 30, dash_count=7),
        # Upper crystallization age intercept & lower lead-loss thermal event intercept
        circle(780, 780, 44),
        circle(260, 180, 36),
    ]
    return union_all(parts)


def gc_rb_sr_isochron_diagram():
    """Rb-Sr / Sm-Nd Radiogenic Isochron: 87Sr/86Sr vs 87Rb/86Sr linear isochron with initial strontium intercept."""
    parts = [
        arrow(140, 130, 140, 910, 36, 90, 52),
        arrow(110, 150, 920, 150, 36, 90, 52),
        # Linear isochron line: y = y0 + m * x (slope = exp(lambda * t) - 1)
        line(140, 340, 880, 820, 42),
        # Initial ratio (87Sr/86Sr)0 intercept on y-axis
        circle(140, 340, 40),
        # Co-genetic mineral/whole-rock sample points on isochron
        circle(350, 476, 34),
        circle(560, 612, 34),
        circle(780, 755, 34),
    ]
    return union_all(parts)


def gc_sulfur_isotope_delta34s():
    """Sulfur Isotope (delta34S) Fractionation Bar: Mantle sulfur (0 permil) vs magmatic sulfides vs bacteriogenic sulfate."""
    parts = [
        # Central baseline at 0 permil (Vienna CDT standard)
        dashed_line(500, 120, 500, 880, 30, dash_count=8),
        line(100, 500, 900, 500, 34),
        # Mantle / Magmatic sulfide narrow bar around 0 (-3 to +3 permil)
        rounded_rect(440, 640, 560, 780, 15),
        # Sedimentary bacteriogenic negative delta34S bar (left, -30 to -10 permil)
        rounded_rect(160, 430, 380, 570, 15),
        # Seawater sulfate heavy positive delta34S bar (right, +15 to +35 permil)
        rounded_rect(620, 220, 840, 360, 15),
    ]
    return union_all(parts)


def gc_swir_mineral_spectral_trough():
    """Diagnostic SWIR Mineral Absorption Trough (Al-OH / Fe-OH / Mg-OH): High-resolution reflectance absorption curve."""
    pts = [
        (100, 780),
        (260, 760),
        (420, 720),
        (500, 180),  # Sharp diagnostic 2200 nm Al-OH illite doublet trough
        (580, 720),
        (740, 760),
        (900, 740),
    ]
    parts = [
        stroke(pts, 42),
        # Wavelength calibration calipers at absorption minimum
        arrow(500, 880, 500, 260, 32, 85, 48),
        dashed_line(500, 180, 500, 100, 24, dash_count=3),
    ]
    return union_all(parts)


def gc_campbell_vectoring_ratio():
    """Geochemical Vectoring Molar Ratio Index: Vector ratio rising monotonically toward porphyry/VMS deposit center."""
    pts = [
        (120, 220),
        (260, 260),
        (420, 340),
        (580, 510),
        (740, 760),
        (880, 880),
    ]
    parts = [
        arrow(120, 140, 120, 910, 36, 90, 52),
        arrow(90, 160, 920, 160, 36, 90, 52),
        stroke(pts, 40),
        # Target deposit bullseye in upper-right
        circle(880, 880, 55),
        circle(880, 880, 22),
    ]
    for pt in pts[:-1]:
        parts.append(circle(pt[0], pt[1], 30))
    return union_all(parts)


def gc_alumina_saturation_asi():
    """Alumina Saturation Index (ASI / Shand): A/CNK vs A/NK plot separating peraluminous, metaluminous, and peralkaline magmas."""
    parts = [
        arrow(130, 130, 130, 910, 36, 90, 52),
        arrow(100, 150, 920, 150, 36, 90, 52),
        # A/CNK = 1.0 vertical boundary
        line(520, 150, 520, 890, 36),
        # A/NK = 1.0 horizontal boundary
        line(130, 500, 900, 500, 36),
        # Indicator crystal markers in Peraluminous (S-type granite) and Metaluminous (I-type) fields
        circle(720, 720, 42),
        regular_poly(320, 720, 48, 4, 45),
    ]
    return union_all(parts)


def gc_harker_variation_diagram():
    """Harker Major Oxide Variation Diagram: Bivariate plot (MgO vs SiO2) displaying magmatic liquid line of descent."""
    pts = [
        (180, 820),
        (310, 680),
        (460, 530),
        (620, 390),
        (780, 270),
        (890, 210),
    ]
    parts = [
        arrow(140, 140, 140, 910, 36, 90, 52),
        arrow(110, 160, 920, 160, 36, 90, 52),
        # Liquid line of descent trend curve
        stroke(pts, 38),
    ]
    for pt in pts:
        parts.append(circle(pt[0], pt[1], 32))
    return union_all(parts)


def gc_water_solubility_melt():
    """Volatile H2O & CO2 Solubility in Magma: Pressure/depth vs dissolved volatile content saturation isobars."""
    # Saturation curve
    pts = []
    for i in range(31):
        t = i / 30.0
        x = 150 + 730 * t
        y = 180 + 680 * (t ** 0.5)
        pts.append((x, y))
    parts = [
        arrow(150, 140, 150, 910, 36, 90, 52),
        arrow(110, 180, 920, 180, 36, 90, 52),
        stroke(pts, 40),
        # Exsolved vapor bubble in super-saturated region
        circle(420, 720, 65),
        circle(680, 820, 48),
    ]
    return union_all(parts)


def gc_oxygen_isotope_delta18o():
    """Oxygen & Hydrogen Stable Isotopes (deltaD vs delta18O): Global Meteoric Water Line and hydrothermal fluid shift."""
    parts = [
        arrow(130, 130, 130, 910, 36, 90, 52),
        arrow(100, 150, 920, 150, 36, 90, 52),
        # Global Meteoric Water Line (GMWL: deltaD = 8 * delta18O + 10)
        line(150, 180, 820, 850, 36),
        # Horizontal hydrothermal oxygen isotope shift arrow
        arrow(480, 510, 820, 510, 34, 85, 48),
    ]
    return union_all(parts)


# =============================================================================
# C. Expanded Geochemical Processes (11 icons: U+E0A1..U+E0AB)
# =============================================================================

def gc_hydrothermal_boiling_immiscibility():
    """Hydrothermal Boiling & Phase Separation: Deep pressurized fluid unmixing into vapor steam and hypersaline brine precipitating gold."""
    parts = [
        # Upward boiling fluid conduit narrowing to boiling horizon
        stroke([(320, 120), (450, 480)], 42),
        stroke([(680, 120), (550, 480)], 42),
        # Low-density vapor steam bubble rising (left)
        circle(350, 740, 110),
        # Hypersaline brine droplet with precipitated gold nuggets (right)
        poly([(680, 840), (560, 660), (800, 660)]),
        circle(680, 610, 90),
        # Precipitated bonanza gold crystals
        regular_poly(680, 610, 44, 8),
    ]
    return union_all(parts)


def gc_sulfide_melt_immiscibility():
    """Sulfide Liquid Immiscibility: Dense immiscible Ni-Cu-PGE sulfide droplet exsolving and settling out of silicate magma."""
    parts = [
        # Ambient silicate magma chamber frame
        rect_outline(100, 100, 900, 900, 38),
        # Dense falling immiscible sulfide droplet (droplet teardrop shape)
        poly([(500, 780), (360, 520), (640, 520)]),
        circle(500, 460, 140),
        # Gravitational settling arrow
        arrow(500, 400, 500, 160, 38, 90, 52),
    ]
    return union_all(parts)


def gc_fluid_rock_metasomatism():
    """Fluid-Rock Metasomatic Reaction Front: Reactive hydrothermal fluid infiltrating and altering pristine host rock."""
    parts = [
        # Infiltrating fluid flow arrows from left
        arrow(90, 720, 320, 720, 36, 85, 48),
        arrow(90, 500, 320, 500, 36, 85, 48),
        arrow(90, 280, 320, 280, 36, 85, 48),
        # Wavy reactive metasomatic replacement front
        stroke([(420, 100), (480, 340), (410, 580), (490, 900)], 44),
        # Altered metasomatic mineral zone (interlocking reaction product polygons)
        regular_poly(650, 680, 75, 6),
        regular_poly(780, 480, 65, 6),
        regular_poly(630, 300, 75, 6),
    ]
    return union_all(parts)


def gc_bacterial_sulfate_reduction():
    """Bacterial Sulfate Reduction (BSR): Anaerobic bacteria reducing sulfate to precipitate framboidal pyrite microspheres."""
    parts = [
        # Rod-shaped anaerobic bacterium cell on left
        rounded_rect_outline(140, 360, 460, 640, 75, 34),
        # Raspberry-like framboidal pyrite sphere composed of micro-crystallites on right
        circle(700, 500, 190),
    ]
    # Subtract micro-crystallite gaps inside the framboid to create true framboidal texture
    holes = union_all([
        circle(700, 500, 38),
        circle(640, 560, 34),
        circle(760, 560, 34),
        circle(640, 440, 34),
        circle(760, 440, 34),
        circle(700, 620, 32),
        circle(700, 380, 32),
    ])
    base = diff(union_all(parts), holes)
    # Re-add micro-crystallite centers
    micro_crystals = [
        circle(700, 500, 18),
        circle(640, 560, 16),
        circle(760, 560, 16),
        circle(640, 440, 16),
        circle(760, 440, 16),
    ]
    return union_all([base] + micro_crystals)


def gc_heavy_mineral_placer():
    """Heavy Mineral Placer Trap: High-density gold/cassiterite grains concentrating in stream riffle vortex trap."""
    parts = [
        # Riverbed floor with stepped wooden/bedrock riffle bar trap
        stroke([(80, 560), (360, 560), (360, 320), (560, 320), (560, 560), (920, 560)], 42),
        # Hydrodynamic vortex circulation flow arrow behind riffle
        curved_arrow(460, 430, 85, 20, 260, 32, 75, 42),
        # Concentrated heavy gold/zircon nuggets settling in trap depression
        circle(420, 365, 42),
        circle(500, 365, 46),
        circle(460, 415, 36),
    ]
    return union_all(parts)


def gc_gossan_boxwork_weathering():
    """Gossan Cellular Boxwork Weathering: Oxidized limonite/goethite ribs left as hollow pseudomorphic mold after leached sulfides."""
    parts = [
        rect_outline(100, 100, 900, 900, 38),
        # Intersecting goethite/limonite boxwork septa ribs
        line(100, 380, 900, 380, 38),
        line(100, 660, 900, 660, 38),
        line(370, 100, 370, 900, 38),
        line(670, 100, 670, 900, 38),
        # Diagonal cellular boxwork ribs
        line(100, 100, 370, 380, 30),
        line(670, 660, 900, 900, 30),
        line(370, 660, 670, 380, 30),
    ]
    return union_all(parts)


def gc_fumarolic_gas_exsolution():
    """Volcanic Fumarolic Gas Vent: Exsolving SO2, H2S, HCl gases precipitating native sulfur crystals around vent."""
    parts = [
        # Volcanic rock vent throat
        stroke([(140, 220), (360, 220), (440, 500)], 42),
        stroke([(860, 220), (640, 220), (560, 500)], 42),
        # Rising gas plume
        curved_arrow(460, 540, 160, 45, 145, 34, 85, 48),
        curved_arrow(540, 540, 160, 135, 35, 34, 85, 48),
        # Sublimate native sulfur orthorhombic dipyramids on vent lip
        regular_poly(320, 290, 58, 4, 45),
        regular_poly(680, 290, 58, 4, 45),
    ]
    return union_all(parts)


def gc_clay_adsorption_cec():
    """Clay Cation Adsorption & CEC: Smectite/illite 2:1 interlayer sheet trapping hydrated heavy metal cations."""
    parts = [
        # Upper and lower aluminosilicate 2:1 clay mineral sheets
        rounded_rect(100, 680, 900, 820, 20),
        rounded_rect(100, 180, 900, 320, 20),
        # Hydrated metal cations (Cu2+, Pb2+, Zn2+) adsorbed inside interlayer gallery
        circle(300, 500, 72),
        circle(500, 500, 72),
        circle(700, 500, 72),
        # Cation attraction exchange arrows
        arrow(500, 410, 500, 335, 24, 55, 32),
        arrow(500, 590, 500, 665, 24, 55, 32),
    ]
    return union_all(parts)


def gc_metal_chloride_complexation():
    """Metal Coordination Complex: Central transition metal cation coordinated by chloride/bisulfide ligands."""
    cx, cy = 500, 500
    parts = [
        # Central transition metal ion (e.g. Cu+, Au+, Zn2+)
        circle(cx, cy, 95),
        # 4 coordinating chloride/bisulfide ligands (tetrahedral/planar)
        circle(220, 500, 70),
        circle(780, 500, 70),
        circle(500, 220, 70),
        circle(500, 780, 70),
        # Coordination donor-acceptor chemical bonds
        line(300, 500, 400, 500, 36),
        line(700, 500, 600, 500, 36),
        line(500, 300, 500, 400, 36),
        line(500, 700, 500, 600, 36),
    ]
    return union_all(parts)


def gc_hydrocarbon_catagenesis():
    """Hydrocarbon Catagenesis & Kerogen Cracking: Thermal oil/gas generation window cracking kerogen into oil and gas."""
    parts = [
        # Kerogen complex organic polymer network
        stroke([(160, 760), (340, 860), (520, 740), (680, 860), (840, 760)], 38),
        line(340, 860, 340, 660, 34),
        line(680, 860, 680, 660, 34),
        # Geothermal maturation heat arrows
        arrow(340, 380, 340, 580, 34, 80, 46),
        arrow(680, 380, 680, 580, 34, 80, 46),
        # Generated liquid oil droplet and natural gas bubble
        poly([(400, 290), (300, 140), (500, 140)]),
        circle(400, 120, 95),
        circle(700, 160, 80),
    ]
    return union_all(parts)


def gc_colloid_flocculation():
    """Colloid Flocculation & Aggregation: Dispersed nanoparticles aggregating into settleable floc at salinity front."""
    parts = [
        # Dispersed individual colloids on left
        circle(160, 720, 34),
        circle(280, 810, 34),
        circle(200, 520, 34),
        circle(310, 360, 34),
        circle(160, 240, 34),
        # Estuarine salinity flocculation barrier arrow
        arrow(380, 500, 520, 500, 38, 85, 50),
        # Aggregated dense floc cluster settling on right
        circle(680, 560, 44),
        circle(750, 610, 44),
        circle(720, 490, 48),
        circle(800, 510, 44),
        circle(740, 410, 46),
        arrow(740, 350, 740, 140, 36, 85, 48),
    ]
    return union_all(parts)


EXPANDED_GEOCHEMISTRY_ICONS: List[Dict[str, Any]] = [
    {
        "id": "gc_la_icp_ms_laser",
        "name": "LA-ICP-MS Laser Microprobe",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE081,
        "description": "Focused pulsed ultraviolet laser beam ablating micro-spot on polished mineral crystal into helium carrier aerosol (LA-ICP-MS).",
        "keywords": ["la-icp-ms", "laser ablation", "microprobe", "zircon geochronology", "in-situ geochemistry"],
        "builder": gc_la_icp_ms_laser,
    },
    {
        "id": "gc_epma_wds_microprobe",
        "name": "Electron Microprobe (EPMA / WDS)",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE082,
        "description": "Electron probe microanalyzer focused beam exciting characteristic X-rays focused along a Rowland circle spectrometer (EPMA/WDS).",
        "keywords": ["epma", "wds", "electron microprobe", "microanalysis", "rowland circle"],
        "builder": gc_epma_wds_microprobe,
    },
    {
        "id": "gc_xrd_diffractometer",
        "name": "X-Ray Powder Diffraction (XRD)",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE083,
        "description": "X-ray powder diffractometer goniometer measuring mineral crystal lattice d-spacings via Bragg diffraction peaks (XRD).",
        "keywords": ["xrd", "x-ray diffraction", "bragg peak", "crystallography", "mineral identification"],
        "builder": gc_xrd_diffractometer,
    },
    {
        "id": "gc_xanes_synchrotron",
        "name": "Synchrotron X-Ray Absorption (XANES)",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE084,
        "description": "Synchrotron storage ring radiation measuring X-ray Absorption Near-Edge Structure (XANES) oxidation state and speciation.",
        "keywords": ["xanes", "exafs", "synchrotron", "oxidation state", "speciation", "x-ray absorption"],
        "builder": gc_xanes_synchrotron,
    },
    {
        "id": "gc_libs_laser_plasma",
        "name": "Laser-Induced Breakdown (LIBS)",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE085,
        "description": "Focused high-energy laser spark generating an elemental plasma plume measured by optical emission spectroscopy (LIBS).",
        "keywords": ["libs", "laser breakdown", "plasma spark", "atomic emission", "field assay"],
        "builder": gc_libs_laser_plasma,
    },
    {
        "id": "gc_ftir_raman_spectroscopy",
        "name": "FTIR & Raman Vibrational Spectroscopy",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE086,
        "description": "Infrared and Raman inelastic laser scattering measuring mineral molecular bond stretching and bending vibrations.",
        "keywords": ["raman", "ftir", "infrared", "molecular vibration", "spectroscopy", "mineralogy"],
        "builder": gc_ftir_raman_spectroscopy,
    },
    {
        "id": "gc_four_acid_total_digest",
        "name": "Four-Acid Near-Total Digestion",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE087,
        "description": "Hotplate hydrofluoric-nitric-perchloric-hydrochloric acid total dissolution of silicate rock matrices (Four-Acid Digest).",
        "keywords": ["four acid", "total digest", "hf", "perchloric", "geochemical assay", "digestion"],
        "builder": gc_four_acid_total_digest,
    },
    {
        "id": "gc_aqua_regia_partial_digest",
        "name": "Aqua Regia Partial Digestion",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE088,
        "description": "3:1 hydrochloric-nitric acid digest selectively dissolving sulfides and precious metals while leaving silicate matrix intact.",
        "keywords": ["aqua regia", "partial digest", "sulfide digest", "gold extraction", "exploration assay"],
        "builder": gc_aqua_regia_partial_digest,
    },
    {
        "id": "gc_cyanide_bottle_roll",
        "name": "Cyanide Bottle Roll Leach Test",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE089,
        "description": "Rotating bottle leach test measuring gold cyanidation dissolution kinetics and metallurgical recovery.",
        "keywords": ["bottle roll", "cyanide leach", "gold recovery", "cyanidation", "metallurgical test"],
        "builder": gc_cyanide_bottle_roll,
    },
    {
        "id": "gc_sequential_extraction",
        "name": "Sequential Chemical Extraction",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE08A,
        "description": "Multi-stage selective extraction partitioning metals into water-soluble, exchangeable, carbonate, oxide, and residual phases.",
        "keywords": ["sequential extraction", "tessier", "metal partitioning", "speciation", "environmental geochemistry"],
        "builder": gc_sequential_extraction,
    },
    {
        "id": "gc_gas_chromatography_ms",
        "name": "Gas Chromatography-MS (GC-MS)",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE08B,
        "description": "Capillary gas chromatography separating organic biomarker hydrocarbon compounds (pristane, phytane, steranes).",
        "keywords": ["gc-ms", "gas chromatography", "organic geochemistry", "biomarkers", "petroleum"],
        "builder": gc_gas_chromatography_ms,
    },
    {
        "id": "gc_sims_shrimp_microprobe",
        "name": "Secondary Ion Mass Spectrometry (SIMS / SHRIMP)",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE08C,
        "description": "Primary ion beam sputtering secondary ions from mineral micro-spots into a large-radius magnetic sector mass spectrometer.",
        "keywords": ["sims", "shrimp", "ion microprobe", "secondary ion", "in-situ geochronology"],
        "builder": gc_sims_shrimp_microprobe,
    },
    {
        "id": "gc_tims_thermal_ionization",
        "name": "Thermal Ionization Mass Spectrometry (TIMS)",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE08D,
        "description": "High-vacuum thermal ionization from heated rhenium ribbon filaments delivering high-precision isotopic ratios.",
        "keywords": ["tims", "thermal ionization", "isotope dilution", "radiogenic isotopes", "u-pb"],
        "builder": gc_tims_thermal_ionization,
    },
    {
        "id": "gc_stable_isotope_gas_irms",
        "name": "Gas Stable Isotope Ratio MS (IRMS)",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE08E,
        "description": "Dual-inlet gas mass spectrometer measuring delta13C, delta18O, and delta34S stable isotope fractionation.",
        "keywords": ["irms", "stable isotopes", "carbon isotopes", "sulfur isotopes", "gas mass spec"],
        "builder": gc_stable_isotope_gas_irms,
    },
    {
        "id": "gc_fluid_inclusion_microtherm",
        "name": "Fluid Inclusion Microthermometry",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE08F,
        "description": "Microscopic biphase fluid inclusion (liquid + vapor + halite) measured on heating-freezing stage for Th and salinity.",
        "keywords": ["fluid inclusion", "microthermometry", "homogenization", "salinity", "hydrothermal fluid"],
        "builder": gc_fluid_inclusion_microtherm,
    },
    {
        "id": "gc_radon_emanometry",
        "name": "Soil-Gas Radon Emanometry",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE090,
        "description": "In-situ soil-gas radon probe detecting alpha-decay tracks from deeply buried uranium and fault conduits.",
        "keywords": ["radon", "emanometry", "soil gas", "alpha track", "uranium exploration"],
        "builder": gc_radon_emanometry,
    },
    {
        "id": "gc_biogeochem_vegetation",
        "name": "Biogeochemical Vegetation Sampling",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE091,
        "description": "Deep tree root absorption translocating mobile pathfinder metals into leaves and bark above blind orebodies.",
        "keywords": ["biogeochemistry", "vegetation sampling", "plant assay", "deep detection", "pathfinder"],
        "builder": gc_biogeochem_vegetation,
    },
    {
        "id": "gc_ree_chondrite_spidergram",
        "name": "Chondrite-Normalized REE Spidergram",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE092,
        "description": "Rare Earth Element profile (La to Lu) normalized to chondrite with pronounced negative/positive Europium anomaly.",
        "keywords": ["ree", "spidergram", "chondrite normalized", "europium anomaly", "rare earths"],
        "builder": gc_ree_chondrite_spidergram,
    },
    {
        "id": "gc_primitive_mantle_spidergram",
        "name": "Primitive Mantle Multi-Element Spidergram",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE093,
        "description": "Extended incompatible trace element spidergram displaying diagnostic subduction Nb-Ta and Ti negative anomaly troughs.",
        "keywords": ["multi-element", "primitive mantle", "trace elements", "nb-ta anomaly", "subduction signature"],
        "builder": gc_primitive_mantle_spidergram,
    },
    {
        "id": "gc_tas_volcanic_diagram",
        "name": "TAS Volcanic Classification Diagram",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE094,
        "description": "Total Alkali vs. Silica (TAS) discrimination diagram classifying volcanic rocks from basalt to rhyolite.",
        "keywords": ["tas", "total alkali silica", "volcanic classification", "basalt", "rhyolite"],
        "builder": gc_tas_volcanic_diagram,
    },
    {
        "id": "gc_qapf_ternary_double",
        "name": "QAPF Double-Ternary Diamond",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE095,
        "description": "IUGS double-ternary diamond diagram classifying plutonic and volcanic rocks by Quartz, Alkali feldspar, Plagioclase, and Foids.",
        "keywords": ["qapf", "double ternary", "plutonic classification", "granite", "gabbro", "foids"],
        "builder": gc_qapf_ternary_double,
    },
    {
        "id": "gc_pearce_tectonic_discrimination",
        "name": "Pearce Granite Tectonic Discrimination",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE096,
        "description": "Trace element discrimination diagram (Nb-Y / Rb) classifying volcanic arc, ocean ridge, and collision granites.",
        "keywords": ["pearce diagram", "tectonic discrimination", "granitoid", "volcanic arc", "within-plate"],
        "builder": gc_pearce_tectonic_discrimination,
    },
    {
        "id": "gc_activity_activity_diagram",
        "name": "Hydrothermal Activity-Activity Diagram",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE097,
        "description": "Log activity-activity phase diagram (log aK+/aH+ vs log aSiO2) displaying K-feldspar, muscovite, and kaolinite fields.",
        "keywords": ["activity diagram", "hydrothermal equilibrium", "k-feldspar", "muscovite", "kaolinite"],
        "builder": gc_activity_activity_diagram,
    },
    {
        "id": "gc_zircon_upb_concordia",
        "name": "Wetherill U-Pb Concordia Diagram",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE098,
        "description": "Wetherill U-Pb Concordia curve and Discordia chord line yielding crystallization and lead-loss event ages.",
        "keywords": ["concordia", "discordia", "u-pb", "zircon age", "geochronology", "intercept"],
        "builder": gc_zircon_upb_concordia,
    },
    {
        "id": "gc_rb_sr_isochron_diagram",
        "name": "Radiogenic Isochron Diagram (Rb-Sr)",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE099,
        "description": "Radiogenic isochron plot (87Sr/86Sr vs 87Rb/86Sr) with linear regression slope defining crystallization age.",
        "keywords": ["isochron", "rb-sr", "sm-nd", "radiogenic age", "initial strontium"],
        "builder": gc_rb_sr_isochron_diagram,
    },
    {
        "id": "gc_sulfur_isotope_delta34s",
        "name": "Sulfur Isotope (delta34S) Fractionation",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE09A,
        "description": "delta34S isotope fractionation ranges distinguishing mantle sulfur from magmatic sulfides and bacteriogenic sulfate.",
        "keywords": ["sulfur isotopes", "delta34s", "bacteriogenic", "fractionation", "pyrite isotopes"],
        "builder": gc_sulfur_isotope_delta34s,
    },
    {
        "id": "gc_swir_mineral_spectral_trough",
        "name": "Diagnostic SWIR Mineral Absorption Trough",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE09B,
        "description": "Diagnostic 2200 nm Al-OH and 2300 nm Mg-OH short-wave infrared reflectance absorption minima.",
        "keywords": ["swir", "al-oh", "absorption feature", "spectral reflectance", "illite crystallinity"],
        "builder": gc_swir_mineral_spectral_trough,
    },
    {
        "id": "gc_campbell_vectoring_ratio",
        "name": "Campbell Porphyry Geochemical Vector",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE09C,
        "description": "Molar alteration index vectoring ratio increasing systematically toward porphyry and VMS mineralized centers.",
        "keywords": ["vectoring ratio", "campbell", "porphyry vector", "alteration index", "exploration vector"],
        "builder": gc_campbell_vectoring_ratio,
    },
    {
        "id": "gc_alumina_saturation_asi",
        "name": "Alumina Saturation Index (ASI / Shand)",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE09D,
        "description": "A/CNK vs A/NK molar diagram dividing igneous rocks into peraluminous, metaluminous, and peralkaline suites.",
        "keywords": ["asi", "alumina saturation", "peraluminous", "metaluminous", "peralkaline", "shand"],
        "builder": gc_alumina_saturation_asi,
    },
    {
        "id": "gc_harker_variation_diagram",
        "name": "Harker Major Oxide Variation Diagram",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE09E,
        "description": "Bivariate major-oxide Harker plot tracking magma chamber differentiation and fractional crystallization liquid lines.",
        "keywords": ["harker diagram", "liquid line of descent", "fractionation", "major oxides", "magma evolution"],
        "builder": gc_harker_variation_diagram,
    },
    {
        "id": "gc_water_solubility_melt",
        "name": "Volatile H2O-CO2 Magma Solubility",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE09F,
        "description": "Dissolved water and CO2 solubility saturation isobars controlling magma degassing and explosive eruption pressure.",
        "keywords": ["water solubility", "co2 solubility", "magma degassing", "volatiles", "saturation isobar"],
        "builder": gc_water_solubility_melt,
    },
    {
        "id": "gc_oxygen_isotope_delta18o",
        "name": "Meteoric Water Line & Oxygen Shift",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE0A0,
        "description": "Global Meteoric Water Line (deltaD vs delta18O) showing hydrothermal fluid-rock exchange oxygen isotope shift.",
        "keywords": ["oxygen isotopes", "delta18o", "meteoric water line", "hydrothermal shift", "water rock reaction"],
        "builder": gc_oxygen_isotope_delta18o,
    },
    {
        "id": "gc_hydrothermal_boiling_immiscibility",
        "name": "Hydrothermal Boiling & Phase Separation",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0A1,
        "description": "Depressurized fluid boiling separating into low-density steam and hypersaline brine precipitating bonanza gold.",
        "keywords": ["boiling", "phase separation", "epithermal gold", "bonanza", "immiscibility"],
        "builder": gc_hydrothermal_boiling_immiscibility,
    },
    {
        "id": "gc_sulfide_melt_immiscibility",
        "name": "Magmatic Sulfide Liquid Immiscibility",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0A2,
        "description": "Exsolution of dense immiscible Ni-Cu-PGE sulfide melt droplets from silicate magma settling by gravity.",
        "keywords": ["sulfide immiscibility", "magmatic sulfide", "ni-cu-pge", "droplet settling", "scss"],
        "builder": gc_sulfide_melt_immiscibility,
    },
    {
        "id": "gc_fluid_rock_metasomatism",
        "name": "Metasomatic Infiltration Reaction Front",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0A3,
        "description": "Infiltrating hydrothermal fluid reacting with host rock across a sharp chemical metasomatic replacement boundary.",
        "keywords": ["metasomatism", "reaction front", "infiltration", "skarn replacement", "fluid-rock"],
        "builder": gc_fluid_rock_metasomatism,
    },
    {
        "id": "gc_bacterial_sulfate_reduction",
        "name": "Bacterial Sulfate Reduction (BSR / Framboid)",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0A4,
        "description": "Anaerobic microbial sulfate reduction generating H2S and precipitating spherical raspberry-like framboidal pyrite.",
        "keywords": ["bsr", "bacterial sulfate reduction", "framboidal pyrite", "biogeochemistry", "sulfur cycle"],
        "builder": gc_bacterial_sulfate_reduction,
    },
    {
        "id": "gc_heavy_mineral_placer",
        "name": "Heavy Mineral Placer Hydrodynamics",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0A5,
        "description": "Hydrodynamic vortex sorting concentrating dense gold, zircon, and monazite heavy minerals in riverbed riffle traps.",
        "keywords": ["placer", "heavy minerals", "gold nugget", "hydrodynamic sorting", "riffle trap"],
        "builder": gc_heavy_mineral_placer,
    },
    {
        "id": "gc_gossan_boxwork_weathering",
        "name": "Gossan Cellular Boxwork Weathering",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0A6,
        "description": "Oxidized iron hydroxide boxwork ribs left as hollow pseudomorphic mold after leached sulfide minerals.",
        "keywords": ["gossan", "boxwork", "limonite", "leached cap", "sulfide weathering"],
        "builder": gc_gossan_boxwork_weathering,
    },
    {
        "id": "gc_fumarolic_gas_exsolution",
        "name": "Volcanic Fumarolic Gas Exsolution",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0A7,
        "description": "Magmatic degassing venting volcanic SO2, H2S, and HCl gases and precipitating native sulfur sublimates.",
        "keywords": ["fumarole", "volcanic gas", "sublimate", "native sulfur", "degassing"],
        "builder": gc_fumarolic_gas_exsolution,
    },
    {
        "id": "gc_clay_adsorption_cec",
        "name": "Clay Interlayer Cation Adsorption (CEC)",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0A8,
        "description": "Smectite 2:1 clay mineral sheet interlayer gallery adsorbing and exchanging dissolved heavy metal cations.",
        "keywords": ["cec", "cation exchange", "adsorption", "smectite", "clay mineralogy", "heavy metals"],
        "builder": gc_clay_adsorption_cec,
    },
    {
        "id": "gc_metal_chloride_complexation",
        "name": "Hydrothermal Metal Complexation",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0A9,
        "description": "Aqueous metal transport via chloride and bisulfide ligand coordination complexes in hydrothermal brines.",
        "keywords": ["metal complex", "chloride complex", "bisulfide", "ligand", "hydrothermal transport"],
        "builder": gc_metal_chloride_complexation,
    },
    {
        "id": "gc_hydrocarbon_catagenesis",
        "name": "Hydrocarbon Catagenesis & Cracking",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0AA,
        "description": "Thermal maturation cracking kerogen into liquid petroleum and natural gas within the oil generation window.",
        "keywords": ["catagenesis", "kerogen cracking", "oil window", "petroleum generation", "source rock"],
        "builder": gc_hydrocarbon_catagenesis,
    },
    {
        "id": "gc_colloid_flocculation",
        "name": "Estuarine Colloid Flocculation",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0AB,
        "description": "Riverine iron/manganese oxyhydroxide nanoparticle colloids aggregating and precipitating at estuarine salinity fronts.",
        "keywords": ["flocculation", "colloids", "nanoparticles", "estuary", "salinity front", "aggregation"],
        "builder": gc_colloid_flocculation,
    },
]
