"""
Opus Geology, Petrophysics, Geotechnical, Geometallurgy, Melt & Carbon Icon Definitions (60 icons, U+E03D..U+E078).
Directly aligned with:
  - C:\\projects\\opus\\opus.geo.geochemistry\\src\\opus\\geo\\geochemistry\\geology\\*
    (GeologicalDescriptor, Lithology, RockType, SimpleLithology, CompositionCategory, GeneticCategory,
     MetamorphicGrade, MetamorphicFacies, AlterationType, AlterationIntensity, ConsolidationDegree,
     DeformationStyle, GeologicUnitMorphology, GeologicalStyle, ParticleType, ParticleShape,
     ParticleAspectRatio, FaultType, FaultMovementType, FaultMovementSense, ContactType, FoliationType,
     LineationType, EventProcess, EventEnvironment, BoreholeDrillingMethod, FeatureObservationMethod,
     DeterminationMethodOrientation, MappingFrame, PlanarPolarityCode, StratigraphicRank)
  - opus.base.properties.GeophysicalMethod (SP, MT, GPR, Radiometrics, NMR, Thermal, Acoustics, Geodesy, Remote Sensing)
  - opus.geo.petrophysics.* (MatrixMixingModel, PoreFluidConductivityModel, IPRelaxationModel, DielectricModel,
     MagneticModel, VelocityModel, DensityModel, ThermalModel, PermeabilityModel)
  - opus.geo.geotechnical.GeotechnicalModel (DEERE_RQD, BARTON_Q, BIENIAWSKI_RMR, HOEK_BROWN, UCS_FROM_VELOCITY, BRITTLENESS_INDEX)
  - opus.geo.geometallurgy.* (AcidRockDrainageModel, ComminutionModel, RecoveryModel)
  - opus.geo.melt.MeltChemistryModel & opus.geo.carbon.CarbonSequestrationModel
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
# A. Additional GeophysicalMethod & Petrophysical Models (16 icons: U+E03D..U+E04C)
# =============================================================================

def gp_self_potential():
    """Self-Potential (SP): Non-polarizing porous-pot electrodes measuring natural streaming/electrochemical voltage over sulfide body."""
    parts = [
        line(70, 650, 930, 650, 34),
        # Voltmeter V at top connecting two porous-pot electrodes
        disk_ring(500, 840, 85, 32),
        stroke([(465, 870), (500, 795), (535, 870)], 26),
        stroke([(200, 720), (200, 840), (415, 840)], 28),
        stroke([(585, 840), (800, 840), (800, 720)], 28),
        rect(160, 610, 240, 730),
        rect(760, 610, 840, 730),
        # Inclined oxidizing sulfide body generating negative SP anomaly (- center at top, + at depth)
        ellipse_outline(500, 340, 125, 220, 36),
        line(460, 460, 540, 460, 30),  # minus sign at shallow top
        line(460, 220, 540, 220, 30),  # plus sign at deep base
        line(500, 180, 500, 260, 30),
        curved_arrow(310, 340, 150, -60, 60, 28, 75, 44),
        curved_arrow(690, 340, 150, 240, 120, 28, 75, 44),
    ]
    return union_all(parts)


def gp_magnetotellurics_mt():
    """Magnetotellurics (MT): Natural ionospheric solar/lightning EM plane wave incident on Earth with orthogonal Ex/Hy sensors."""
    parts = [
        # Ionospheric wave layer at top
        sine_wave(100, 870, 900, 870, amp=32, cycles=3.0, width=32),
        arrow(260, 820, 260, 610, 32, 80, 46),
        arrow(740, 820, 740, 610, 32, 80, 46),
        # Ground surface
        line(70, 560, 930, 560, 34),
        # Orthogonal E-field dipole & H-field induction coils in center
        line(200, 320, 800, 320, 36),
        circle(200, 320, 42),
        circle(800, 320, 42),
        line(500, 120, 500, 520, 36),
        circle(500, 120, 42),
        circle(500, 520, 42),
        rounded_rect(430, 250, 570, 390, 24),
    ]
    return union_all(parts)


def gp_ground_penetrating_radar():
    """Ground Penetrating Radar (GPR): Surface radar antenna cart emitting high-frequency radar pulses and recording hyperbolic diffraction."""
    parts = [
        line(70, 680, 930, 680, 34),
        # GPR antenna sled + wheels on surface
        rounded_rect(340, 720, 660, 860, 30),
        circle(395, 705, 38),
        circle(605, 705, 38),
        # Radar bow-tie / radiated wavefronts going down
        arc(500, 680, 140, 215, 325, 28),
        arc(500, 680, 250, 215, 325, 28),
        # Buried pipe/target at (500, 290) + sharp diffraction hyperbola
        circle(500, 290, 56),
        stroke([(160, 120), (330, 290), (500, 385), (670, 290), (840, 120)], 36),
    ]
    return union_all(parts)


def gp_radiometrics_gamma():
    """Radiometric Gamma-Ray Spectrometry: Scintillation crystal detector with K-U-Th gamma-ray channels and radiation trefoil."""
    cx, cy = 500, 630
    parts = [
        # Radiation trefoil blades at top
        circle(cx, cy, 48),
        sector(cx, cy, 220, 0, 60),
        sector(cx, cy, 220, 120, 180),
        sector(cx, cy, 220, 240, 300),
        # K, U, Th 3-channel spectral bars at bottom
        line(120, 110, 880, 110, 36),
        rect(200, 110, 320, 340),
        rect(440, 110, 560, 410),
        rect(680, 110, 800, 270),
    ]
    return diff(union_all(parts), ring(cx, cy, 90, 35))


def gp_nmr_sounding():
    """Nuclear Magnetic Resonance (NMR): Precessing hydrogen proton spin axis with Larmor RF excitation pulse and T2 decay envelope."""
    # T2 exponential relaxation decay on right
    decay_pts = []
    for i in range(41):
        t = i / 40.0
        x = 460 + 430 * t
        y = 320 + 360 * math.exp(-3.2 * t) * math.cos(5.0 * math.pi * t)
        decay_pts.append((x, y))
    parts = [
        # Precessing proton sphere & tilted magnetic moment vector on left
        circle(250, 480, 110),
        arrow(160, 240, 340, 760, 38, 95, 54),
        ellipse_outline(250, 740, 120, 42, 26),
        # T2 relaxation decay waveform on right
        line(460, 320, 900, 320, 26),
        stroke(decay_pts, 32),
    ]
    return union_all(parts)


def gp_thermal_geothermal():
    """Thermal & Heat Flow Model: Borehole thermometer column with geothermal gradient dT/dz and upward heat-flow vectors q."""
    parts = [
        # Thermometer bulb & stem on left
        circle(240, 200, 105),
        rounded_rect_outline(185, 240, 295, 860, 50, 34),
        rect(220, 200, 260, 660),
        # Temperature ticks
        line(315, 760, 375, 760, 28),
        line(315, 600, 375, 600, 28),
        line(315, 440, 375, 440, 28),
        # Upward conductive/advective heat flow wavy arrows on right
        sine_wave(560, 160, 560, 740, amp=30, cycles=2.5, width=32),
        arrow_head(560, 840, 90, 95, 54),
        sine_wave(780, 160, 780, 740, amp=30, cycles=2.5, width=32),
        arrow_head(780, 840, 90, 95, 54),
    ]
    return union_all(parts)


def gp_acoustics_sonar():
    """Acoustics & Borehole Televiewer / Sonar: Transducer emitting acoustic beam fan imaging bathymetry / borehole wall."""
    parts = [
        # Transducer head at top
        rounded_rect(390, 800, 610, 900, 25),
        # Acoustic fan edges and wavefront arcs
        dashed_line(450, 800, 140, 200, 26, dash_count=6),
        dashed_line(550, 800, 860, 200, 26, dash_count=6),
        arc(500, 800, 220, 242, 298, 30),
        arc(500, 800, 370, 242, 298, 32),
        arc(500, 800, 520, 242, 298, 34),
        # Seafloor / rock interface profile at bottom
        stroke([(90, 160), (280, 180), (500, 260), (720, 150), (910, 190)], 42),
    ]
    return union_all(parts)


def gp_geodesy_insar_gnss():
    """Geodesy (GNSS / InSAR): Orbiting satellite radar/GNSS phase fringes measuring crustal uplift/subsidence deformation."""
    parts = [
        # Satellite body + solar panels at top-left
        rect(180, 740, 280, 840),
        rect_outline(70, 755, 170, 825, 26),
        rect_outline(290, 755, 390, 825, 26),
        # Radar LOS beams to ground benchmark
        dashed_line(260, 720, 580, 320, 26, dash_count=5),
        dashed_line(310, 720, 780, 420, 26, dash_count=5),
        # Concentric InSAR interferometric deformation fringes on ground
        ellipse_outline(640, 300, 250, 140, 30),
        ellipse_outline(640, 300, 150, 82, 30),
        circle(640, 300, 38),
        # Uplift/subsidence vertical vector
        arrow(640, 300, 640, 580, 34, 85, 48),
    ]
    return union_all(parts)


def gp_remote_sensing_hyperspectral():
    """Remote Sensing & Hyperspectral Imaging: Multi-layer spectral image cube with mineral absorption feature reflectance curve."""
    # Reflectance spectrum with diagnostic SWIR absorption feature (e.g. 2200 nm Al-OH trough)
    spec_pts = [
        (120, 320),
        (280, 380),
        (430, 370),
        (540, 120),  # Diagnostic clay/carbonate absorption dip
        (650, 360),
        (800, 390),
        (900, 340),
    ]
    parts = [
        # Stacked hyperspectral image bands at top
        poly([(200, 780), (500, 900), (800, 780), (500, 660)]),
        stroke([(200, 690), (500, 570), (800, 690)], 32),
        stroke([(200, 600), (500, 480), (800, 600)], 32),
        # Reflectance spectrum with absorption trough at bottom
        stroke(spec_pts, 38),
        arrow(540, 420, 540, 195, 28, 75, 42),
    ]
    return union_all(parts)


def gp_matrix_mixing_bounds():
    """Petrophysical Matrix Mixing Model (Voigt / Reuss / Hashin-Shtrikman / Bruggeman): Upper & lower bounds vs volume fraction."""
    # Voigt linear upper bound, Reuss harmonic lower bound, and Bruggeman/HS effective curve between (140,160) and (880,840)
    voigt = [(140, 160), (880, 840)]
    reuss = []
    bruggeman = []
    for i in range(31):
        f = i / 30.0
        x = 140 + 740 * f
        y_r = 160 + 680 * (f / (4.0 - 3.0 * f))
        y_b = 160 + 680 * (f ** 1.65)
        reuss.append((x, y_r))
        bruggeman.append((x, y_b))
    parts = [
        arrow(140, 120, 140, 910, 34, 85, 48),
        arrow(100, 160, 920, 160, 34, 85, 48),
        dashed_line(140, 160, 880, 840, 28, dash_count=7),
        stroke(reuss, 28),
        stroke(bruggeman, 40),
        circle(140, 160, 36),
        circle(880, 840, 36),
    ]
    return union_all(parts)


def gp_pore_fluid_archie():
    """Pore Fluid & Archie / Waxman-Smits Conduction: Insulating silicate grains with interstitial conductive brine pathways & EDL."""
    parts = [
        # Three rounded silicate framework grains
        circle(260, 680, 155),
        circle(740, 680, 155),
        circle(260, 260, 155),
        circle(740, 260, 155),
        # Tortuous electrolytic pore-throat current pathway flowing through connected pore space
        stroke([(90, 470), (350, 470), (500, 620), (500, 320), (650, 470), (910, 470)], 40),
        arrow_head(925, 470, 0, 95, 54),
        arrow_head(500, 895, 90, 85, 48),
        line(500, 620, 500, 840, 32),
    ]
    # Hollow out centers of framework grains so electrical double layer (EDL) rim is highlighted
    grain_cores = union_all([
        circle(260, 680, 95),
        circle(740, 680, 95),
        circle(260, 260, 95),
        circle(740, 260, 95),
    ])
    return diff(union_all(parts), grain_cores)


def gp_ip_cole_cole():
    """Induced Polarization Relaxation (Cole-Cole / Revil Metallic): Complex conductivity Argand phase arc & polarized sulfide grain."""
    parts = [
        # Axes: Real (sigma') vs Imaginary/Quadrature conductivity (sigma'')
        arrow(120, 200, 120, 860, 34, 85, 48),
        arrow(90, 230, 920, 230, 34, 85, 48),
        # Depressed Cole-Cole semicircle arc in Argand plane
        arc(520, 130, 340, 18, 162, 38),
        # Peak relaxation frequency (omega * tau = 1) marker at apex (520, 470)
        circle(520, 470, 44),
        dashed_line(520, 230, 520, 470, 26, dash_count=4),
        # Polarized metallic grain icon in upper right (+ and - charge double layer)
        circle(760, 740, 85),
        arc(760, 740, 125, -45, 45, 28),
        arc(760, 740, 125, 135, 225, 28),
    ]
    return union_all(parts)


def gp_dielectric_permittivity():
    """Dielectric Permittivity Model (CRIM / Maxwell-Wagner): Capacitor plates with polarized water/mineral dipoles & frequency dispersion."""
    parts = [
        # Parallel capacitor plates on left and right
        rect(110, 160, 175, 840),
        rect(825, 160, 890, 840),
        # Oriented dipolar water molecules inside electric field
        ellipse_outline(360, 660, 95, 55, 30, angle_deg=25),
        circle(415, 685, 24),
        ellipse_outline(640, 660, 95, 55, 30, angle_deg=25),
        circle(695, 685, 24),
        ellipse_outline(360, 340, 95, 55, 30, angle_deg=25),
        circle(415, 365, 24),
        ellipse_outline(640, 340, 95, 55, 30, angle_deg=25),
        circle(695, 365, 24),
        # Electric field vector E across center
        arrow(220, 500, 780, 500, 36, 90, 52),
    ]
    return union_all(parts)


def gp_koenigsberger_remanence():
    """Magnetic Remanence & Koenigsberger Ratio (Q = Jr / Ji): Vector addition of Induced Magnetization (Ji) and Natural Remanent (Jr)."""
    ox, oy = 180, 180
    parts = [
        # Origin rock sample circle
        circle(ox, oy, 52),
        # Induced magnetization vector Ji (aligned with present Earth field B0, horizontal-right/up)
        arrow(ox, oy, 780, 260, 38, 95, 54),
        # Remanent magnetization vector Jr (steeply inclined ancient direction)
        arrow(ox, oy, 320, 820, 38, 95, 54),
        # Resultant total magnetization vector J_total = Ji + Jr (diagonal)
        arrow(ox, oy, 860, 840, 44, 105, 60),
        # Parallelogram completion dashed lines
        dashed_line(320, 820, 860, 840, 24, dash_count=6),
        dashed_line(780, 260, 860, 840, 24, dash_count=6),
    ]
    return union_all(parts)


def gp_gassmann_fluid_sub():
    """Gassmann Fluid Substitution & Rock Physics: Porous mineral frame + dry pore vs fluid-saturated stiffening arrow."""
    parts = [
        # Left: Dry porous frame cube with hollow pore
        rect_outline(90, 260, 420, 740, 34),
        disk_ring(255, 500, 105, 30),
        # Fluid substitution arrow in center
        arrow(445, 500, 555, 500, 38, 85, 50),
        # Right: Fluid-saturated stiffened rock frame with filled pore + acoustic wave
        rect_outline(580, 260, 910, 740, 38),
        circle(745, 500, 115),
        sine_wave(580, 840, 910, 840, amp=34, cycles=2.0, width=32),
    ]
    return union_all(parts)


def gp_permeability_kozeny():
    """Permeability Model (Kozeny-Carman / Katz-Thompson): Tortuous connected pore throat channel between packed grains with Darcy flux."""
    parts = [
        # Top and bottom packed grain boundaries forming a constriction (pore throat)
        sector(320, 880, 280, 200, 340),
        sector(700, 880, 260, 200, 340),
        sector(320, 120, 280, 20, 160),
        sector(700, 120, 260, 20, 160),
        # Confining cell top & bottom walls
        line(80, 880, 920, 880, 36),
        line(80, 120, 920, 120, 36),
        # Tortuous streamline squeezing through pore throat
        stroke([(90, 500), (310, 500), (510, 575), (700, 500), (850, 500)], 38),
        arrow_head(925, 500, 0, 95, 54),
        # Throat radius caliper arrows at narrowest constriction
        arrow(510, 380, 510, 620, 24, 60, 36, both_ends=True),
    ]
    return union_all(parts)


# =============================================================================
# B. Additional GeotechnicalModel Icons (6 icons: U+E04D..U+E052)
# =============================================================================

def gt_deere_rqd():
    """Deere RQD (Rock Quality Designation): Drill core run next to a 100 mm threshold scale bar distinguishing intact vs fractured zones."""
    parts = [
        # Measuring scale ruler at top with 100 mm ticks
        line(100, 800, 900, 800, 34),
        line(100, 740, 100, 860, 32),
        line(366, 755, 366, 845, 28),
        line(633, 755, 633, 845, 28),
        line(900, 740, 900, 860, 32),
        # Intact core piece 1 (>100 mm, solid highlighted)
        rounded_rect(100, 450, 430, 630, 18),
        # Heavily fractured rubblized zone (<100 mm pieces, excluded from RQD)
        rect_outline(460, 450, 520, 630, 26),
        rect_outline(545, 450, 605, 630, 26),
        # Intact core piece 2 (>100 mm, solid highlighted)
        rounded_rect(635, 450, 900, 630, 18),
        # Dimension arrows under the two valid >100 mm pieces
        arrow(100, 260, 430, 260, 32, 80, 46, both_ends=True),
        arrow(635, 260, 900, 260, 32, 80, 46, both_ends=True),
    ]
    return union_all(parts)


def gt_barton_q_tunnel():
    """Barton Q-System Tunnel Support: Horseshoe tunnel arch reinforced with radial rockbolts and shotcrete liner."""
    cx, cy = 500, 380
    parts = [
        # Horseshoe tunnel arch & floor
        arc(cx, cy, 240, 0, 180, 42),
        line(260, 180, 260, 380, 42),
        line(740, 180, 740, 380, 42),
        line(180, 180, 820, 180, 38),
        # Radial grouted rockbolts with faceplate nuts around tunnel crown
        line(500, 620, 500, 890, 34),
        rect(455, 595, 545, 640),
        line(330, 550, 140, 740, 34),
        line(670, 550, 860, 740, 34),
        line(268, 442, 75, 495, 34),
        line(732, 442, 925, 495, 34),
    ]
    return union_all(parts)


def gt_bieniawski_rmr():
    """Bieniawski RMR (Rock Mass Rating): Six-parameter weighted rating scorecard (UCS, RQD, Spacing, Condition, Water, Orientation)."""
    bar_lengths = [720, 620, 800, 540, 440, 680]
    parts = [
        line(140, 100, 140, 900, 38),
        line(140, 100, 900, 100, 38),
    ]
    for i, blen in enumerate(bar_lengths):
        y = 820 - i * 125
        parts.append(rounded_rect(140, y - 36, 140 + blen, y + 36, 14))
    return union_all(parts)


def gt_hoek_brown_criterion():
    """Generalized Hoek-Brown Criterion: Non-linear parabolic failure envelope in principal stress space (sigma_1 vs sigma_3)."""
    # Non-linear Hoek-Brown curve: sigma_1 = sigma_3 + sigma_ci * (mb * sigma_3 / sigma_ci + s)^a
    hb_intact = []
    hb_rockmass = []
    for i in range(41):
        t = i / 40.0
        x = 150 + 730 * t
        y_intact = 320 + 560 * (t ** 0.58)
        y_rm = 180 + 440 * (t ** 0.45)
        hb_intact.append((x, y_intact))
        hb_rockmass.append((x, y_rm))
    parts = [
        # Principal stress axes: sigma_1 (vertical) vs sigma_3 (horizontal)
        arrow(150, 110, 150, 920, 36, 90, 52),
        arrow(110, 150, 920, 150, 36, 90, 52),
        # Upper dashed curve (intact rock sigma_ci, GSI=100)
        stroke(hb_intact, 28),
        # Lower bold curve (jointed rock mass with GSI < 100)
        stroke(hb_rockmass, 42),
        # Downward GSI degradation arrow between intact and rock-mass envelopes
        arrow(560, 720, 560, 520, 30, 78, 44),
    ]
    return union_all(parts)


def gt_ucs_from_velocity():
    """UCS from P-Wave Velocity (UCS = a Vp^b): Rock core specimen under uniaxial compression platens with acoustic P-wave pulse."""
    parts = [
        # Top and bottom steel loading platens
        rect(220, 760, 780, 830),
        rect(220, 170, 780, 240),
        arrow(500, 940, 500, 835, 38, 85, 50),
        arrow(500, 60, 500, 165, 38, 85, 50),
        # Rock core cylinder
        rect_outline(310, 240, 690, 760, 36),
        # Ultrasonic P-wave pulse traveling axially through core
        sine_wave(500, 270, 500, 730, amp=95, cycles=2.5, width=32),
    ]
    return union_all(parts)


def gt_brittleness_index():
    """Brittleness Index (UCS vs Tensile Splitting): Brazilian disc indirect tensile test with central axial tensile fracture split."""
    cx, cy = 500, 500
    disc = diff(
        circle(cx, cy, 300),
        # Jagged vertical tensile splitting crack down the diameter
        stroke([(500, 790), (475, 650), (525, 500), (480, 350), (500, 210)], 40),
    )
    parts = [
        disc,
        # Top and bottom curved loading jaws + diametral compression arrows
        rect(340, 800, 660, 855),
        rect(340, 145, 660, 200),
        arrow(500, 950, 500, 855, 38, 85, 50),
        arrow(500, 50, 500, 145, 38, 85, 50),
        # Lateral tensile opening arrows
        arrow(260, 500, 90, 500, 34, 82, 48),
        arrow(740, 500, 910, 500, 34, 82, 48),
    ]
    return union_all(parts)


# =============================================================================
# C. Opus Geological Descriptors, Rock Types & Sulfide Styles (32 icons: U+E053..U+E072)
# =============================================================================

def gl_rock_type_igneous():
    """Igneous Rock Type (RockType.IGNEOUS): Volcano/magma chamber + interlocking random granitic/basaltic phenocrysts."""
    parts = [
        # Magma volcano silhouette with interlocking crystal crosses (+)
        stroke([(100, 180), (340, 780), (450, 700), (550, 700), (660, 780), (900, 180)], 38, closed=True),
        # Magma throat & eruption plume
        curved_arrow(410, 780, 110, 0, 125, 32, 80, 46),
        curved_arrow(590, 780, 110, 180, 55, 32, 80, 46),
        # Standard geological "+" igneous pattern inside
        line(310, 350, 430, 350, 30),
        line(370, 290, 370, 410, 30),
        line(570, 350, 690, 350, 30),
        line(630, 290, 630, 410, 30),
        line(440, 520, 560, 520, 30),
        line(500, 460, 500, 580, 30),
    ]
    return union_all(parts)


def gl_rock_type_sedimentary():
    """Sedimentary Rock Type (RockType.SEDIMENTARY): Horizontal bedded strata of sandstone, limestone masonry, and conglomerate clasts."""
    parts = [
        rect_outline(100, 120, 900, 880, 38),
        line(100, 630, 900, 630, 34),
        line(100, 370, 900, 370, 34),
        # Top bed: Limestone masonry joints
        line(360, 630, 360, 880, 30),
        line(640, 630, 640, 880, 30),
        # Middle bed: Sandstone stipple dots & cross-lamination
        circle(240, 500, 32),
        circle(500, 500, 32),
        circle(760, 500, 32),
        # Bottom bed: Conglomerate pebbles
        circle(280, 245, 58),
        circle(540, 245, 48),
        circle(750, 245, 54),
    ]
    return union_all(parts)


def gl_rock_type_metamorphic():
    """Metamorphic Rock Type (RockType.METAMORPHIC): Disharmonic ptygmatic/gneissic banded folds with garnet augen."""
    parts = [
        rect_outline(100, 120, 900, 880, 38),
        sine_wave(140, 720, 860, 720, amp=48, cycles=2.0, width=36),
        sine_wave(140, 500, 860, 500, amp=55, cycles=2.0, width=38),
        sine_wave(140, 280, 860, 280, amp=48, cycles=2.0, width=36),
        regular_poly(500, 500, 85, 6),
    ]
    return union_all(parts)


def gl_composition_category():
    """Composition Category (Ultramafic / Mafic / Intermediate / Felsic): SiO2 vs MgO-FeO compositional bar & crystal."""
    parts = [
        # Stepped compositional partition bar (Ultramafic <45%, Mafic 45-52%, Intermediate 52-63%, Felsic >63% SiO2)
        rect_outline(100, 540, 900, 860, 36),
        rect(100, 540, 300, 860),
        line(500, 540, 500, 860, 32),
        line(700, 540, 700, 860, 32),
        circle(400, 700, 42),
        # SiO4 tetrahedron at bottom representing silicate chemistry
        stroke([(500, 460), (240, 120), (760, 120)], 38, closed=True),
        line(500, 460, 500, 230, 30),
        line(240, 120, 500, 230, 30),
        line(760, 120, 500, 230, 30),
        circle(500, 230, 42),
    ]
    return union_all(parts)


def gl_genetic_category():
    """Genetic Category (Igneous / Sedimentary / Metamorphic / Cataclastic / Hydrothermal Genesis): Rock-cycle triad arrows."""
    cx, cy = 500, 480
    parts = [
        # Three genetic nodes in an equilateral rock-cycle triangle
        circle(500, 830, 85),
        rect(125, 165, 295, 335),
        regular_poly(790, 250, 95, 6),
        # Three curved cycle arrows linking the nodes
        curved_arrow(cx, cy, 310, 120, 195, 36, 90, 52),
        curved_arrow(cx, cy, 310, 240, 315, 36, 90, 52),
        curved_arrow(cx, cy, 310, 0, 75, 36, 90, 52),
    ]
    return union_all(parts)


def gl_metamorphic_facies_pt():
    """Metamorphic Facies & Grade (P-T Diagram): Pressure (depth) vs Temperature axes with Blueschist, Greenschist, Amphibolite, Granulite, Eclogite fields."""
    parts = [
        # Temperature (horizontal) and Pressure (vertical) axes
        arrow(130, 120, 130, 910, 36, 90, 52),
        arrow(110, 140, 920, 140, 36, 90, 52),
        # Forbidden low-T high-P limit (dashed) & Geothermal gradient curves
        dashed_line(130, 140, 460, 880, 28, dash_count=6),
        line(130, 140, 880, 840, 34),
        line(130, 140, 890, 420, 34),
        # Facies field dividers (Greenschist -> Amphibolite -> Granulite)
        line(420, 140, 350, 630, 30),
        line(670, 140, 580, 830, 30),
        # Prograde P-T-t clockwise loop path arrow
        curved_arrow(520, 480, 150, 200, 40, 36, 85, 48),
    ]
    return union_all(parts)


def gl_consolidation_degree():
    """Consolidation Degree (Unconsolidated Loose Sediment -> Indurated / Lithified Rock): Loose grains compacting into cemented rock."""
    parts = [
        # Left: Loose unconsolidated grains with wide pore spaces
        circle(160, 740, 52),
        circle(320, 780, 48),
        circle(230, 560, 55),
        circle(140, 360, 50),
        circle(330, 390, 52),
        circle(220, 190, 48),
        # Compaction / lithification arrow in center
        arrow(400, 500, 540, 500, 38, 85, 50),
        # Right: Tightly interlocked, cemented indurated rock block
        rect_outline(580, 160, 900, 840, 38),
        line(580, 390, 900, 390, 32),
        line(580, 610, 900, 610, 32),
        line(740, 160, 740, 390, 32),
        line(700, 390, 700, 610, 32),
        line(760, 610, 760, 840, 32),
    ]
    return union_all(parts)


def gl_deformation_brittle_ductile():
    """Deformation Style (Brittle vs Ductile vs Brittle-Ductile): Left half faulted brittlely, right half folded ductilely."""
    parts = [
        # Central transition divider
        dashed_line(500, 90, 500, 910, 26, dash_count=8),
        # Left side: Brittle sharp fault offset of two beds
        line(110, 820, 430, 180, 38),
        line(80, 640, 200, 640, 40),
        line(265, 510, 450, 510, 40),
        line(80, 380, 330, 380, 40),
        line(395, 250, 460, 250, 40),
        # Right side: Smooth continuous ductile S-fold
        sine_wave(540, 660, 910, 660, amp=95, cycles=1.0, width=40),
        sine_wave(540, 360, 910, 360, amp=95, cycles=1.0, width=40),
    ]
    return union_all(parts)


def gl_unit_morphology():
    """Geologic Unit Morphology (Dome / Pipe / Ring Dyke / Boudin / Laccolith): Pinch-and-swell boudinage & diapir dome."""
    # Pinch-and-swell boudinaged layer at top + diapiric dome below
    boudin1 = ellipse(270, 730, 175, 90)
    boudin2 = ellipse(730, 730, 175, 90)
    parts = [
        boudin1,
        boudin2,
        # Necking lines between boudins
        dashed_line(445, 730, 555, 730, 28, dash_count=3),
        # Diapiric dome / pipe rising from base
        stroke([(90, 160), (310, 160), (380, 480), (500, 560), (620, 480), (690, 160), (910, 160)], 40),
        stroke([(90, 320), (260, 390), (500, 620), (740, 390), (910, 320)], 32),
    ]
    return union_all(parts)


def gl_style_disseminated():
    """GeologicalStyle.DISSEMINATED (<15% modal sulfide): Sparse sulfide blebs/specks scattered uniformly inside host rock matrix."""
    pts = [
        (240, 740), (520, 770), (750, 710),
        (340, 570), (640, 540), (210, 420),
        (480, 380), (770, 350), (310, 220), (610, 210),
    ]
    parts = [rect_outline(100, 100, 900, 900, 38)]
    for x, y in pts:
        parts.append(circle(x, y, 36))
    return union_all(parts)


def gl_style_net_textured():
    """GeologicalStyle.NET_TEXTURED (30-60% modal sulfide): Continuous intergranular sulfide network enclosing rounded cumulate silicate grains."""
    # Solid sulfide matrix box with rounded silicate cumulate grains subtracted out, leaving a continuous net-textured web
    matrix = rect(100, 100, 900, 900)
    silicate_grains = union_all([
        ellipse(290, 710, 140, 115, angle_deg=15),
        ellipse(690, 720, 145, 110, angle_deg=-20),
        ellipse(500, 500, 150, 115, angle_deg=8),
        ellipse(240, 440, 95, 110, angle_deg=-10),
        ellipse(760, 450, 95, 115, angle_deg=12),
        ellipse(310, 260, 150, 105, angle_deg=-15),
        ellipse(690, 250, 140, 110, angle_deg=20),
    ])
    return diff(matrix, silicate_grains)


def gl_style_massive_sulfide():
    """GeologicalStyle.MASSIVE & SEMI_MASSIVE (>80% modal sulfide): Solid pooled massive sulfide body with minor silicate xenolith inclusions."""
    body = rounded_rect(100, 100, 900, 900, 45)
    # Subtract a couple of small silicate inclusions and a bold metallic luster slash
    inclusions = union_all([
        regular_poly(280, 680, 68, 5, 20),
        regular_poly(710, 310, 58, 6, 15),
        line(260, 260, 740, 740, 36),
        line(420, 220, 780, 580, 30),
    ])
    return diff(body, inclusions)


def gl_style_veined_stringer():
    """GeologicalStyle.VEINED / STRINGER_VEIN / FRACTURE_CONTROLLED: Anastomosing planar & stringer sulfide veins cutting host rock."""
    parts = [
        rect_outline(100, 100, 900, 900, 38),
        # Major crosscutting planar vein
        stroke([(120, 200), (460, 520), (880, 820)], 56),
        # Conjugate and branching stringer veinlets
        stroke([(460, 520), (220, 780)], 34),
        stroke([(630, 640), (860, 420)], 34),
        stroke([(310, 380), (680, 180)], 30),
        stroke([(140, 560), (390, 600)], 26),
    ]
    return union_all(parts)


def gl_particle_shape_roundness():
    """ParticleShape & Aspect Ratio (Angular -> Subrounded -> Well-Rounded & Prolate/Oblate): End-member clast shapes."""
    parts = [
        # Top-left: Very Angular clast (sharp triangle/polygon)
        poly([(110, 560), (420, 620), (360, 890), (140, 840)]),
        # Top-right: Well-Rounded spherical clast
        circle(720, 730, 155),
        # Bottom: Elongate prolate rod clast with Sneed & Folk axial calipers
        ellipse(500, 250, 340, 95),
        arrow(160, 95, 840, 95, 28, 70, 40, both_ends=True),
    ]
    return union_all(parts)


def gl_contact_unconformity():
    """ContactType (Angular Unconformity / Intrusive / Gradational Contact): Tilted truncated beds beneath horizontal strata across wavy erosion surface."""
    parts = [
        rect_outline(100, 100, 900, 900, 38),
        # Wavy unconformity contact across middle (y=540)
        sine_wave(100, 540, 900, 540, amp=28, cycles=3.5, width=40),
        # Upper horizontal younger beds
        line(100, 720, 900, 720, 32),
        # Lower steeply dipping truncated older beds
        line(180, 100, 420, 530, 34),
        line(420, 100, 660, 530, 34),
        line(660, 100, 890, 510, 34),
    ]
    return union_all(parts)


def gl_foliation_lineation():
    """FoliationType & LineationType (S-L Tectonite Fabric): Inclined foliation plane (S) carrying mineral stretching lineation arrows (L)."""
    # Inclined 3D plane parallelogram
    plane = [(120, 260), (660, 160), (880, 740), (340, 840)]
    parts = [
        stroke(plane, 38, closed=True),
        # Internal foliation traces parallel to strike
        dashed_line(230, 550, 770, 450, 26, dash_count=5),
        # Mineral stretching lineations (L) plunging down the foliation plane
        arrow(390, 750, 220, 300, 34, 85, 48),
        arrow(590, 710, 420, 260, 34, 85, 48),
        arrow(770, 670, 600, 220, 34, 85, 48),
    ]
    return union_all(parts)


def gl_borehole_drilling_methods():
    """BoreholeDrillingMethod (RAB / RC / Auger / Diamond / Sonic): Tricone rotary bit & reverse-circulation air/chip return arrows."""
    parts = [
        # Drill pipe string with inner RC sample tube
        line(360, 420, 360, 910, 34),
        line(640, 420, 640, 910, 34),
        line(445, 440, 445, 910, 24),
        line(555, 440, 555, 910, 24),
        # Upward inner RC chip return arrow
        arrow(500, 460, 500, 880, 30, 78, 44),
        # Downward outer annulus air injection arrows
        arrow(260, 820, 260, 520, 28, 72, 42),
        arrow(740, 820, 740, 520, 28, 72, 42),
        # Rotary tricone / hammer bit cones at bottom
        regular_poly(380, 250, 130, 3, -90),
        regular_poly(620, 250, 130, 3, -90),
        circle(500, 140, 32),
        circle(310, 130, 28),
        circle(690, 130, 28),
    ]
    return union_all(parts)


def gl_planar_polarity_overturned():
    """PlanarPolarityCode (Upright vs Overturned Bedding & Way-Up Indicators): Graded bedding & overturned fold limb symbol."""
    parts = [
        # Left: Upright strike & dip symbol with graded bedding way-up arrow
        line(240, 140, 240, 860, 40),
        line(240, 500, 410, 500, 40),
        # Right: Overturned bedding symbol (J-hook dip tick wrapping over strike line)
        line(680, 140, 680, 860, 40),
        arc(680, 560, 120, 90, 270, 38),
        line(680, 440, 860, 440, 38),
        arrow_head(890, 440, 0, 85, 48),
    ]
    return union_all(parts)


# =============================================================================
# D. Opus Geometallurgy, Melt Chemistry & Carbon Sequestration (6 icons: U+E073..U+E078)
# =============================================================================

def gm_acid_rock_drainage():
    """AcidRockDrainageModel (MPA / ANC / NAPP / NAG pH): Sulfide waste-rock dump oxidizing under rain/O2 into acidic leachate droplet."""
    parts = [
        # Waste rock / tailings trapezoid pile at top
        poly([(160, 520), (320, 820), (680, 820), (840, 520)]),
        # Sulfide (FeS2) crystals inside pile (cut out below)
        # Acidic leachate droplet at bottom containing H+ / pH symbol
        poly([(500, 460), (340, 240), (660, 240)]),
        circle(500, 210, 160),
    ]
    cuts = union_all([
        regular_poly(420, 670, 55, 4, 45),
        regular_poly(590, 670, 55, 4, 45),
        # Plus sign inside acid droplet
        line(430, 210, 570, 210, 34),
        line(500, 140, 500, 280, 34),
    ])
    return diff(union_all(parts), cuts)


def gm_comminution_work_index():
    """ComminutionModel (Bond Work Index Wi / SAG Mill A*b / SMC): Rotating tumbling mill shell with lifters, steel balls, and crushing trajectory."""
    cx, cy = 500, 500
    parts = [
        # Rotating mill shell with internal lifter bars
        disk_ring(cx, cy, 390, 42),
        rect(475, 810, 525, 890),
        rect(475, 110, 525, 190),
        rect(110, 475, 190, 525),
        rect(810, 475, 890, 525),
        # Cataracting grinding ball trajectory arc inside mill
        curved_arrow(480, 480, 230, 155, 35, 34, 85, 48),
        # Grinding media balls & rock charge at toe of mill
        circle(340, 320, 48),
        circle(460, 280, 52),
        circle(590, 290, 46),
        circle(670, 380, 42),
        regular_poly(410, 410, 48, 5, 20),
    ]
    return union_all(parts)


def gm_flotation_recovery():
    """RecoveryModel (First-Order Flotation / Klimpel / Grade-Recovery): Froth flotation cell with rising air bubbles carrying attached hydrophobic sulfide particles."""
    parts = [
        # Flotation cell tank + overflow launder lip
        stroke([(160, 860), (160, 120), (840, 120), (840, 740), (920, 660)], 38),
        # Froth layer wave at top
        sine_wave(160, 740, 840, 740, amp=26, cycles=3.0, width=30),
        # Agitator impeller shaft & rotor at bottom
        line(500, 240, 500, 880, 34),
        rounded_rect(330, 200, 670, 265, 20),
        # Air bubbles with attached dark sulfide mineral specks rising to froth
        disk_ring(330, 450, 65, 28),
        circle(330, 520, 30),
        disk_ring(670, 520, 65, 28),
        circle(670, 590, 30),
        disk_ring(350, 680, 55, 26),
        disk_ring(640, 700, 55, 26),
    ]
    return union_all(parts)


def gc_melt_chemistry_f02():
    """MeltChemistryModel (Optical Basicity / NBO/T / Oxygen Fugacity Delta-FMQ): Polymerized silicate melt network & fO2 buffer curve."""
    # FMQ buffer curve from bottom-left to top-right
    fmq_pts = []
    for i in range(31):
        t = i / 30.0
        x = 140 + 740 * t
        y = 160 + 680 * (t ** 0.65)
        fmq_pts.append((x, y))
    parts = [
        arrow(140, 120, 140, 910, 34, 85, 48),
        arrow(100, 160, 920, 160, 34, 85, 48),
        stroke(fmq_pts, 40),
        # Linked silicate tetrahedra dimer (NBO/T bridging oxygen) in upper-left
        regular_poly(310, 720, 85, 3, 90),
        regular_poly(460, 720, 85, 3, -90),
        circle(385, 720, 34),
        # Oxidized (+Delta FMQ) vs Reduced (-Delta FMQ) markers
        circle(640, 760, 38),
        circle(740, 420, 38),
    ]
    return union_all(parts)


def gc_carbon_mineralisation():
    """CarbonSequestrationModel (Ultramafic Serpentinisation & CO2 Mineral Trapping): CO2 injection into ultramafic rock precipitating carbonate crystals."""
    parts = [
        # Hexagonal carbonate crystal ring enclosing CO2 -> MgCO3 lock
        stroke(
            [(500, 900), (840, 700), (840, 300), (500, 100), (160, 300), (160, 700)],
            40,
            closed=True,
        ),
        # Downward CO2 mineralization injection arrow into solid rhombohedral magnesite/calcite crystal
        arrow(500, 840, 500, 540, 38, 90, 52),
        poly([(500, 510), (700, 380), (500, 210), (300, 380)]),
    ]
    return union_all(parts)


def gl_lithology_tensor_anisotropy():
    """Lithology & PropertyTensor Anisotropy (Isotropic / VTI / TTI / Triaxial Ellipsoid): Tilted 3D anisotropy ellipsoid with principal axes."""
    cx, cy = 500, 500
    parts = [
        # Tilted anisotropy ellipsoid (30 degrees dip)
        ellipse_outline(cx, cy, 370, 175, 38, angle_deg=30),
        ellipse_outline(cx, cy, 370, 80, 26, angle_deg=30),
        # Three orthogonal principal tensor axes (along-fabric fast axis & across-fabric slow axis)
        arrow(cx - 340, cy - 196, cx + 340, cy + 196, 34, 85, 48, both_ends=True),
        arrow(cx + 140, cy - 242, cx - 140, cy + 242, 32, 80, 46, both_ends=True),
        circle(cx, cy, 40),
    ]
    return union_all(parts)


def gl_fault_normal_graben():
    """Horst & Graben Extensional Rift: Conjugate normal faults dropping central graben valley between horst shoulders."""
    parts = [
        # Ground surface stepped down in center
        stroke([(80, 780), (330, 780), (390, 560), (610, 560), (670, 780), (920, 780)], 38),
        # Two conjugate normal fault planes dipping inward
        line(330, 780, 550, 120, 36),
        line(670, 780, 450, 120, 36),
        # Marker beds in horsts and dropped graben
        line(80, 560, 400, 560, 30),
        line(600, 560, 920, 560, 30),
        line(420, 340, 580, 340, 34),
        # Downward graben subsidence arrow
        arrow(500, 760, 500, 580, 34, 80, 46),
        # Regional horizontal extensional arrows
        arrow(260, 860, 90, 860, 32, 75, 44),
        arrow(740, 860, 910, 860, 32, 75, 44),
    ]
    return union_all(parts)


def gl_fault_thrust_ramp():
    """Fold-and-Thrust Belt Ramp-Flat: Basal decollement ramping up to form hanging-wall fault-bend anticline."""
    parts = [
        # Stepped thrust fault trace (flat -> ramp -> upper flat)
        stroke([(90, 240), (420, 240), (680, 680), (910, 680)], 44),
        # Sawtooth thrust teeth on hanging wall ramp
        poly([(480, 342), (540, 370), (490, 410)]),
        poly([(580, 512), (640, 540), (590, 580)]),
        # Hanging-wall folded anticlinal strata
        stroke([(280, 360), (480, 360), (660, 840), (880, 840)], 34),
        stroke([(280, 500), (450, 500), (640, 930), (820, 930)], 34),
        # Tectonic compression push arrow from left
        arrow(80, 460, 280, 460, 38, 95, 54),
    ]
    return union_all(parts)


def gl_fault_strike_slip_dextral():
    """Dextral (Right-Lateral) Strike-Slip Fault: Offset marker horizon in map view with synthetic Riedel shears."""
    parts = [
        # Vertical principal displacement zone (PDZ) fault trace
        line(500, 90, 500, 910, 42),
        # Right-lateral offset of horizontal marker horizon across fault
        line(90, 640, 500, 640, 40),
        line(500, 360, 910, 360, 40),
        # Dextral shear arrows along fault trace
        arrow(420, 340, 420, 720, 36, 95, 54),
        arrow(580, 660, 580, 280, 36, 95, 54),
        # Synthetic Riedel (R) shear fracture traces inclined at 15 deg
        line(320, 480, 480, 530, 26),
        line(520, 470, 680, 520, 26),
    ]
    return union_all(parts)


def gl_shear_zone_sigmoidal():
    """Ductile Shear Zone & Delta Porphyroclast: Rotated porphyroclast with sweeping sigmoidal recrystallized mantle tails."""
    cx, cy = 500, 500
    parts = [
        # Central rounded porphyroclast
        circle(cx, cy, 130),
        # Sigmoidal delta tails wrapping top-right and bottom-left
        stroke([(cx, cy + 110), (660, 640), (890, 680)], 44),
        stroke([(cx, cy - 110), (340, 360), (110, 320)], 44),
        # Shear zone boundary lines at top and bottom
        dashed_line(80, 820, 920, 820, 28, dash_count=8),
        dashed_line(80, 180, 920, 180, 28, dash_count=8),
        # Dextral shear sense arrows
        arrow(300, 890, 700, 890, 34, 85, 48),
        arrow(700, 110, 300, 110, 34, 85, 48),
    ]
    return union_all(parts)


def gl_chevron_kink_fold():
    """Chevron & Kink Folds: Angular zigzag fold train with planar limbs and sharp hinge lines."""
    parts = [
        # Multilayer angular chevron fold train
        stroke([(90, 350), (280, 720), (500, 260), (720, 720), (910, 350)], 42),
        stroke([(90, 480), (280, 850), (500, 390), (720, 850), (910, 480)], 34),
        stroke([(90, 220), (280, 590), (500, 130), (720, 590), (910, 220)], 34),
        # Sharp hinge trace (axial plane) dashed line
        dashed_line(280, 920, 280, 520, 24, dash_count=4),
        dashed_line(500, 480, 500, 80, 24, dash_count=4),
        dashed_line(720, 920, 720, 520, 24, dash_count=4),
    ]
    return union_all(parts)


def gl_ptygmatic_vein_fold():
    """Ptygmatic Metamorphic Vein: Sinuous meandering folded competent quartz/aplite vein in ductile metamorphic gneiss."""
    # Sinuous meander curve
    pts = [
        (130, 880),
        (280, 820),
        (460, 840),
        (380, 680),
        (220, 640),
        (340, 490),
        (660, 540),
        (760, 410),
        (560, 310),
        (370, 330),
        (450, 180),
        (640, 140),
        (820, 120),
    ]
    parts = [
        # Surrounding gneissic foliation lines (straight background)
        dashed_line(100, 760, 900, 760, 22, dash_count=7),
        dashed_line(100, 580, 900, 580, 22, dash_count=7),
        dashed_line(100, 420, 900, 420, 22, dash_count=7),
        dashed_line(100, 240, 900, 240, 22, dash_count=7),
        # Bold ptygmatic folded vein
        stroke(pts, 48),
    ]
    return union_all(parts)


def gl_columnar_jointing():
    """Basalt Columnar Jointing: Isometric array of vertical hexagonal basalt cooling columns with cross-joints."""
    # 3 hexagonal columns in 3D perspective
    col_w, col_h = 240, 680
    parts = [
        # Hexagonal caps at top
        regular_poly(300, 760, 125, 6, 30),
        regular_poly(500, 680, 125, 6, 30),
        regular_poly(700, 760, 125, 6, 30),
        # Vertical prism edges running down
        line(190, 700, 190, 120, 36),
        line(300, 640, 300, 120, 36),
        line(410, 700, 410, 120, 36),
        line(500, 560, 500, 120, 36),
        line(590, 700, 590, 120, 36),
        line(700, 640, 700, 120, 36),
        line(810, 700, 810, 120, 36),
        # Horizontal ball-and-socket cross jointing
        stroke([(190, 420), (300, 370), (410, 420)], 28),
        stroke([(410, 340), (500, 290), (590, 340)], 28),
        stroke([(590, 420), (700, 370), (810, 420)], 28),
    ]
    return union_all(parts)


def gl_spinifex_texture():
    """Komatiite Spinifex Texture: Criss-crossing radiating skeletal bladed olivine needles in ultramafic lava flow."""
    parts = [
        rect_outline(100, 100, 900, 900, 38),
        # Primary long radiating skeletal blades
        line(160, 850, 720, 150, 44),
        line(320, 880, 860, 340, 40),
        line(820, 860, 240, 180, 42),
        line(640, 880, 140, 380, 38),
        # Secondary acute intersecting blades
        line(460, 740, 880, 560, 32),
        line(240, 580, 680, 440, 32),
        line(380, 360, 790, 220, 32),
        line(540, 620, 360, 140, 30),
    ]
    return union_all(parts)


def gl_pillow_lava():
    """Pillow Basalt (Geopetal Way-Up): Stacked bulbous pillow lava toes with convex upper surfaces and downward cusps."""
    # Top pillow (large bulbous with downward cusp pointing into notch between lower pillows)
    p_top = poly([(250, 620), (330, 860), (670, 860), (750, 620), (500, 480)])
    p_bl = poly([(120, 240), (180, 520), (460, 520), (420, 240), (270, 140)])
    p_br = poly([(540, 240), (580, 520), (860, 520), (880, 240), (730, 140)])
    parts = [
        p_top,
        p_bl,
        p_br,
        # Chilled glass vesicular rims (dotted lines)
        arc(500, 740, 120, 20, 160, 24),
    ]
    return diff(union_all(parts), union_all([circle(500, 720, 42), circle(300, 360, 32), circle(700, 360, 32)]))


def gl_fiamme_ignimbrite():
    """Welded Ignimbrite & Fiamme: Eutaxitic flattened lens-like glassy pumice fiamme with wispy flame-like tails."""
    parts = [
        rect_outline(100, 100, 900, 900, 38),
        # Large central flattened fiamme with ragged flame ends
        poly([(160, 520), (320, 620), (680, 620), (840, 520), (740, 470), (520, 440), (280, 460)]),
        # Upper smaller fiamme lens
        poly([(240, 750), (410, 810), (620, 810), (760, 750), (580, 710), (380, 710)]),
        # Lower smaller fiamme lens
        poly([(210, 270), (380, 330), (610, 330), (790, 270), (590, 220), (360, 220)]),
    ]
    return union_all(parts)


def gl_banded_iron_formation():
    """Banded Iron Formation (BIF): Alternating micro-laminated layers of dark iron oxide (hematite/magnetite) and red chert/jasper."""
    parts = [
        rect_outline(100, 100, 900, 900, 38),
        # Alternating micro-laminated beds with subtle mesoproterozoic fold wave
        rect(100, 770, 900, 840),
        rect(100, 610, 900, 680),
        rect(100, 450, 900, 520),
        rect(100, 290, 900, 360),
        rect(100, 130, 900, 200),
    ]
    return union_all(parts)


def gl_hydrothermal_breccia():
    """Hydrothermal Breccia: Jigsaw-fit angular wall-rock clasts cemented by open-space hydrothermal mineral matrix."""
    parts = [
        rect_outline(100, 100, 900, 900, 38),
        # Angular fragmented clasts with dilation gaps between them (jigsaw puzzle fit)
        poly([(150, 540), (320, 850), (480, 740), (360, 510)]),
        poly([(540, 850), (850, 820), (780, 560), (490, 660)]),
        poly([(150, 160), (160, 440), (420, 420), (350, 160)]),
        poly([(480, 460), (740, 480), (850, 220), (560, 160)]),
        # Euhedral quartz crystal sparkles in the hydrothermal dilation matrix
        regular_poly(510, 560, 36, 6),
        regular_poly(420, 480, 28, 6),
    ]
    return union_all(parts)


def gl_potassic_alteration():
    """Potassic Hydrothermal Alteration: Hydrothermal quartz-sulfide veinlet flanked by symmetric K-feldspar + secondary biotite selvage."""
    parts = [
        # Outer host rock frame
        rect_outline(100, 100, 900, 900, 38),
        # Pervasive potassic alteration halo envelope around central vein
        rect(280, 100, 720, 900),
        # Central quartz-sulfide vein cutting through halo (subtracted then re-outlined with sulfide beads)
    ]
    vein_trough = rect(440, 100, 560, 900)
    base = diff(union_all(parts), vein_trough)
    vein_parts = [
        stroke([(440, 100), (440, 900)], 32),
        stroke([(560, 100), (560, 900)], 32),
        circle(500, 280, 38),
        circle(500, 500, 38),
        circle(500, 720, 38),
    ]
    return union_all([base] + vein_parts)


def gl_phyllic_sericitic_alteration():
    """Phyllic / Sericitic Alteration (QSP): Quartz-sericite bleached alteration halo studded with disseminated cubic pyrite crystals."""
    parts = [
        rect_outline(100, 100, 900, 900, 38),
        # Disseminated cubic pyrite (FeS2) crystals in sericite bleached groundmass
        regular_poly(280, 740, 72, 4, 45),
        regular_poly(700, 710, 64, 4, 15),
        regular_poly(480, 490, 85, 4, 30),
        regular_poly(260, 270, 68, 4, 10),
        regular_poly(720, 290, 76, 4, 40),
        # Sericite microscopic micaceous foliation dashes
        line(380, 820, 540, 820, 24),
        line(160, 520, 320, 520, 24),
        line(640, 510, 840, 510, 24),
        line(410, 210, 570, 210, 24),
    ]
    return union_all(parts)


def gl_advanced_argillic():
    """Advanced Argillic Alteration & Vuggy Silica: Extremely leached residual sponge with open cavities (vugs) lined with alunite/quartz."""
    host = rect(100, 100, 900, 900)
    # Vuggy silica cavities leached out by hypogene hyper-acidic fluids
    vugs = union_all([
        ellipse(320, 710, 140, 90, angle_deg=20),
        ellipse(700, 690, 120, 105, angle_deg=-15),
        ellipse(480, 480, 160, 110, angle_deg=5),
        ellipse(250, 290, 110, 85, angle_deg=-25),
        ellipse(690, 280, 145, 95, angle_deg=18),
    ])
    sponge = diff(host, vugs)
    # Re-add euhedral quartz crystals protruding into the open vug cavities
    crystals = [
        regular_poly(480, 480, 42, 6),
        regular_poly(320, 710, 32, 6),
        regular_poly(690, 280, 36, 6),
    ]
    return union_all([sponge] + crystals)


def gl_propylitic_chlorite_epidote():
    """Propylitic Alteration Halo: Pistachio-green prismatic epidote crystal clusters and radial chlorite rosettes."""
    parts = [
        # Prismatic epidote crystal columns
        stroke([(240, 160), (320, 760), (380, 840), (440, 760), (360, 160)], 36, closed=True),
        stroke([(440, 160), (520, 820), (580, 900), (640, 820), (560, 160)], 36, closed=True),
        # Intersecting epidote cross-column
        stroke([(620, 240), (790, 640), (840, 720), (880, 640), (710, 240)], 32, closed=True),
        # Chlorite basal rosette at base
        circle(500, 180, 75),
    ]
    return union_all(parts)


def gl_serpentinite_mesh():
    """Serpentinisation & Mesh Texture: Network of fibrous lizardite/antigorite veins surrounding relict olivine cores with magnetite granules."""
    parts = [
        rect_outline(100, 100, 900, 900, 38),
        # Serpentine mesh vein network dividing relict olivine kernels
        line(100, 480, 900, 480, 38),
        line(460, 100, 460, 900, 38),
        line(100, 720, 900, 720, 28),
        line(100, 260, 900, 260, 28),
        line(710, 100, 710, 900, 28),
        line(240, 100, 240, 900, 28),
        # Relict rounded olivine cores inside mesh cells
        ellipse(350, 600, 65, 48),
        ellipse(585, 600, 70, 48),
        ellipse(350, 370, 65, 48),
        ellipse(585, 370, 70, 48),
    ]
    return union_all(parts)


def gl_skarn_calc_silicate():
    """Calc-Silicate Skarn: Metasomatic reaction zone between granite intrusion and carbonate marble with euhedral garnet."""
    parts = [
        # Granite intrusion on left
        stroke([(100, 100), (320, 100), (320, 900), (100, 900)], 38),
        line(210, 450, 210, 550, 30),
        line(160, 500, 260, 500, 30),
        # Pure carbonate marble on right (brick masonry)
        stroke([(680, 100), (900, 100), (900, 900), (680, 900)], 38),
        line(680, 500, 900, 500, 30),
        line(790, 500, 790, 900, 30),
        # Metasomatic reaction skarn zone in center with massive grossular-andradite garnet dodecahedron
        regular_poly(500, 500, 155, 6, 30),
        stroke([(500, 345), (500, 655)], 26),
        stroke([(365, 425), (635, 575)], 26),
        stroke([(365, 575), (635, 425)], 26),
    ]
    return union_all(parts)


def gl_greisen_cassiterite():
    """Greisen Pneumatolytic Alteration: Coarse quartz-muscovite-topaz rock containing twinned tetragonal cassiterite elbow crystal."""
    parts = [
        # Geniculate twinned cassiterite (SnO2) "visiergraupen" elbow crystal in center
        poly([(360, 240), (500, 500), (640, 240), (560, 160), (500, 340), (440, 160)]),
        poly([(500, 500), (640, 760), (560, 840), (500, 660), (440, 840), (360, 760)]),
        # Greisen muscovite mica book laths flanking crystal
        stroke([(160, 640), (310, 640), (280, 560), (130, 560)], 30, closed=True),
        stroke([(690, 440), (840, 440), (870, 360), (720, 360)], 30, closed=True),
    ]
    return union_all(parts)


def gl_tourmaline_sun_rosette():
    """Tourmaline Sun Rosette: Starburst of acicular needle-like schorl tourmaline prisms radiating from common nucleus."""
    cx, cy = 500, 500
    parts = [circle(cx, cy, 52)]
    # 12 radiating tourmaline needle prisms
    for i in range(12):
        ang_deg = i * 30.0
        rad = math.radians(ang_deg)
        x_tip = cx + 380 * math.cos(rad)
        y_tip = cy + 380 * math.sin(rad)
        parts.append(line(cx, cy, x_tip, y_tip, 34))
    return union_all(parts)


def gl_turbidite_bouma_sequence():
    """Turbidite Bouma Sequence (Ta-Te): Complete submarine turbidity current sedimentation cycle."""
    parts = [
        rect_outline(160, 90, 840, 910, 38),
        # Te (800..910): Pelagic / hemipelagic mud
        line(160, 800, 840, 800, 30),
        # Td (680..800): Upper parallel laminated silt
        line(160, 680, 840, 680, 30),
        dashed_line(200, 740, 800, 740, 20, dash_count=6),
        # Tc (490..680): Ripple cross-laminae and convolute bedding
        line(160, 490, 840, 490, 30),
        sine_wave(200, 580, 800, 580, amp=36, cycles=2.5, width=28),
        # Tb (320..490): Lower parallel laminated sand
        line(160, 320, 840, 320, 30),
        line(200, 405, 800, 405, 24),
        # Ta (90..320): Massive graded sandstone with coarse basal flute casts
        circle(320, 200, 48),
        circle(500, 210, 56),
        circle(680, 195, 44),
    ]
    return union_all(parts)


def gl_fluvial_point_bar_channel():
    """Fluvial Point Bar & Meander Channel: Sinuous river bend showing lateral accretion clinoforms on point bar vs cut-bank scarp."""
    parts = [
        # Outer cut-bank steep cliff on left
        stroke([(160, 880), (120, 500), (220, 120)], 48),
        # Inner point-bar convex curvature with lateral accretion clinoform ridges
        arc(740, 500, 450, 135, 225, 34),
        arc(740, 500, 320, 135, 225, 32),
        arc(740, 500, 190, 135, 225, 30),
        # Flow velocity core arrow following the outer talweg
        curved_arrow(440, 500, 340, 140, 220, 38, 90, 52),
    ]
    return union_all(parts)


OPUS_GEOLOGY_ICONS: List[Dict[str, Any]] = [
    {
        "id": "gp_self_potential",
        "name": "Self-Potential (SP) Method",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE03D,
        "description": "Non-polarizing electrodes measuring natural streaming and electrochemical potentials over an oxidizing orebody (GeophysicalMethod.SELF_POTENTIAL).",
        "keywords": ["self potential", "sp", "spontaneous potential", "geophysical.method.electrical.self.potential"],
        "builder": gp_self_potential,
    },
    {
        "id": "gp_magnetotellurics_mt",
        "name": "Magnetotellurics (MT)",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE03E,
        "description": "Natural ionospheric electromagnetic plane waves recorded by orthogonal electric dipoles and magnetic induction coils (GeophysicalMethod.MAGNETOTELLURICS).",
        "keywords": ["mt", "magnetotellurics", "ionos", "geophysical.method.em.mt", "impedance"],
        "builder": gp_magnetotellurics_mt,
    },
    {
        "id": "gp_ground_penetrating_radar",
        "name": "Ground Penetrating Radar (GPR)",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE03F,
        "description": "High-frequency radar antenna imaging shallow dielectric contrasts and hyperbolic point diffractions (GeophysicalMethod.GROUND_PENETRATING_RADAR).",
        "keywords": ["gpr", "ground penetrating radar", "georadar", "geophysical.method.radar"],
        "builder": gp_ground_penetrating_radar,
    },
    {
        "id": "gp_radiometrics_gamma",
        "name": "Radiometric Gamma Spectrometry",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE040,
        "description": "Gamma-ray spectrometry measuring natural K, U, and Th radioelement decay channels (GeophysicalMethod.RADIOMETRICS).",
        "keywords": ["radiometrics", "gamma ray", "potassium", "uranium", "thorium", "geophysical.method.radiometric"],
        "builder": gp_radiometrics_gamma,
    },
    {
        "id": "gp_nmr_sounding",
        "name": "Nuclear Magnetic Resonance (NMR)",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE041,
        "description": "Hydrogen proton spin precession and T2 relaxation decay measuring mobile pore water and permeability (GeophysicalMethod.NUCLEAR_MAGNETIC_RESONANCE).",
        "keywords": ["nmr", "mrs", "nuclear magnetic resonance", "t2 relaxation", "geophysical.method.nmr"],
        "builder": gp_nmr_sounding,
    },
    {
        "id": "gp_thermal_geothermal",
        "name": "Thermal & Heat Flow Survey",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE042,
        "description": "Subsurface temperature gradient and conductive/advective terrestrial heat flow (GeophysicalMethod.THERMAL & ThermalModel).",
        "keywords": ["thermal", "geothermal", "heat flow", "thermal conductivity", "geophysical.method.thermal"],
        "builder": gp_thermal_geothermal,
    },
    {
        "id": "gp_acoustics_sonar",
        "name": "Acoustics & Sonar Imaging",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE043,
        "description": "Acoustic wave propagation and backscatter imaging of water bodies, seabed, or borehole walls (GeophysicalMethod.ACOUSTICS).",
        "keywords": ["acoustics", "sonar", "televiewer", "backscatter", "geophysical.method.acoustic"],
        "builder": gp_acoustics_sonar,
    },
    {
        "id": "gp_geodesy_insar_gnss",
        "name": "Geodesy, GNSS & InSAR",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE044,
        "description": "Satellite radar interferometry (InSAR) and GNSS measuring crustal deformation and subsidence fringes (GeophysicalMethod.GEODESY).",
        "keywords": ["geodesy", "insar", "gnss", "subsidence", "crustal deformation", "geophysical.method.geodetic"],
        "builder": gp_geodesy_insar_gnss,
    },
    {
        "id": "gp_remote_sensing_hyperspectral",
        "name": "Remote Sensing & Hyperspectral",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE045,
        "description": "Multi-band hyperspectral image cube with diagnostic mineral SWIR/VNIR absorption trough (GeophysicalMethod.REMOTE_SENSING & HyperspectralProperty).",
        "keywords": ["remote sensing", "hyperspectral", "swir", "vnir", "spectral absorption", "geophysical.method.remote.sensing"],
        "builder": gp_remote_sensing_hyperspectral,
    },
    {
        "id": "gp_matrix_mixing_bounds",
        "name": "Matrix Mixing Model (Voigt / Reuss / HS / Bruggeman)",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE046,
        "description": "Effective medium conductivity/elastic mixing laws between Voigt upper and Reuss lower bounds (opus.geo.petrophysics.MatrixMixingModel).",
        "keywords": ["matrix mixing", "bruggeman", "hashin shtrikman", "voigt reuss hill", "percolation"],
        "builder": gp_matrix_mixing_bounds,
    },
    {
        "id": "gp_pore_fluid_archie",
        "name": "Pore Fluid & Archie / Waxman-Smits Model",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE047,
        "description": "Electrolytic pore-throat conduction and clay electrical double layer surface conduction (opus.geo.petrophysics.PoreFluidConductivityModel).",
        "keywords": ["archie", "waxman smits", "dual water", "revil cec", "pore fluid", "formation factor"],
        "builder": gp_pore_fluid_archie,
    },
    {
        "id": "gp_ip_cole_cole",
        "name": "IP Relaxation Model (Cole-Cole / Revil)",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE048,
        "description": "Complex conductivity Cole-Cole Argand phase arc and metallic grain polarization (opus.geo.petrophysics.IPRelaxationModel).",
        "keywords": ["cole cole", "pelton", "ip relaxation", "chargeability", "revil metallic", "warburg"],
        "builder": gp_ip_cole_cole,
    },
    {
        "id": "gp_dielectric_permittivity",
        "name": "Dielectric Permittivity Model (CRIM / Topp)",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE049,
        "description": "High-frequency dielectric polarization of water and mineral phases (opus.geo.petrophysics.DielectricModel).",
        "keywords": ["dielectric", "permittivity", "crim", "topp", "maxwell wagner", "hanai bruggeman"],
        "builder": gp_dielectric_permittivity,
    },
    {
        "id": "gp_koenigsberger_remanence",
        "name": "Magnetic Remanence & Koenigsberger Model",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE04A,
        "description": "Vector sum of induced magnetization (Ji) and natural remanent magnetization (Jr) with self-demagnetization (opus.geo.petrophysics.MagneticModel).",
        "keywords": ["koenigsberger", "remanence", "nrm", "self demagnetising", "magnetic model"],
        "builder": gp_koenigsberger_remanence,
    },
    {
        "id": "gp_gassmann_fluid_sub",
        "name": "Gassmann & Rock Physics Velocity Model",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE04B,
        "description": "Porous elastic mineral frame stiffening under Gassmann pore-fluid substitution (opus.geo.petrophysics.VelocityModel).",
        "keywords": ["gassmann", "velocity model", "wyllie", "hertz mindlin", "kuster toksoz", "critical porosity"],
        "builder": gp_gassmann_fluid_sub,
    },
    {
        "id": "gp_permeability_kozeny",
        "name": "Permeability Model (Kozeny-Carman / Timur)",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE04C,
        "description": "Hydraulic fluid flux through a constricted pore throat governed by grain size and tortuosity (opus.geo.petrophysics.PermeabilityModel).",
        "keywords": ["permeability", "kozeny carman", "katz thompson", "timur", "pore throat", "hydraulic"],
        "builder": gp_permeability_kozeny,
    },
    {
        "id": "gt_deere_rqd",
        "name": "Deere RQD (Rock Quality Designation)",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE04D,
        "description": "Percentage of drill core run recovered in intact pieces longer than 100 mm (GeotechnicalModel.DEERE_RQD).",
        "keywords": ["rqd", "deere", "rock quality designation", "core recovery", "geotech.model.rqd"],
        "builder": gt_deere_rqd,
    },
    {
        "id": "gt_barton_q_tunnel",
        "name": "Barton Q-System Tunnel Support",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE04E,
        "description": "Rock mass Q-value tunnel support classification with radial rockbolts and arch liner (GeotechnicalModel.BARTON_Q).",
        "keywords": ["barton q", "q-system", "rockbolt", "tunnel support", "geotech.model.q"],
        "builder": gt_barton_q_tunnel,
    },
    {
        "id": "gt_bieniawski_rmr",
        "name": "Bieniawski RMR Scorecard",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE04F,
        "description": "Six-parameter Bieniawski Rock Mass Rating (0-100) composite profile (GeotechnicalModel.BIENIAWSKI_RMR).",
        "keywords": ["rmr", "bieniawski", "rock mass rating", "geotech.model.rmr"],
        "builder": gt_bieniawski_rmr,
    },
    {
        "id": "gt_hoek_brown_criterion",
        "name": "Generalized Hoek-Brown Criterion",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE050,
        "description": "Non-linear principal stress failure envelope controlled by GSI, intact mi, and blast disturbance D (GeotechnicalModel.HOEK_BROWN).",
        "keywords": ["hoek brown", "generalized hoek brown", "gsi", "disturbance factor", "geotech.model.hoekbrown"],
        "builder": gt_hoek_brown_criterion,
    },
    {
        "id": "gt_ucs_from_velocity",
        "name": "UCS from P-Wave Velocity",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE051,
        "description": "Unconfined compressive strength correlated with sonic compressional velocity Vp across a core specimen (GeotechnicalModel.UCS_FROM_VELOCITY).",
        "keywords": ["ucs", "unconfined compressive strength", "sonic velocity", "geotech.model.ucsfromvp"],
        "builder": gt_ucs_from_velocity,
    },
    {
        "id": "gt_brittleness_index",
        "name": "Rock Brittleness Index",
        "domain": "Geotechnical",
        "category": "Earth Model Types",
        "codepoint": 0xE052,
        "description": "Compressive-to-tensile strength ratio illustrated by Brazilian indirect tensile disc splitting (GeotechnicalModel.BRITTLENESS_INDEX).",
        "keywords": ["brittleness", "brazilian test", "tensile strength", "spalling", "geotech.model.brittleness"],
        "builder": gt_brittleness_index,
    },
    {
        "id": "gl_rock_type_igneous",
        "name": "Igneous Rock Type",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE053,
        "description": "Magmatic/volcanic genesis and crystalline igneous fabric (opus.geo.geochemistry.geology.RockType.IGNEOUS).",
        "keywords": ["igneous", "plutonic", "volcanic", "magmatic", "rock.type"],
        "builder": gl_rock_type_igneous,
    },
    {
        "id": "gl_rock_type_sedimentary",
        "name": "Sedimentary Rock Type",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE054,
        "description": "Stratified clastic, carbonate, and chemical sedimentary beds (opus.geo.geochemistry.geology.RockType.SEDIMENTARY).",
        "keywords": ["sedimentary", "strata", "limestone", "sandstone", "conglomerate", "rock.type"],
        "builder": gl_rock_type_sedimentary,
    },
    {
        "id": "gl_rock_type_metamorphic",
        "name": "Metamorphic Rock Type",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE055,
        "description": "Foliated, banded gneissic/schistose metamorphic fabric with porphyroblast (opus.geo.geochemistry.geology.RockType.METAMORPHIC).",
        "keywords": ["metamorphic", "gneiss", "schist", "foliated", "rock.type"],
        "builder": gl_rock_type_metamorphic,
    },
    {
        "id": "gl_composition_category",
        "name": "Silicate & Lithological Composition",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE056,
        "description": "Ultramafic, mafic, intermediate, and felsic compositional spectrum with silicate tetrahedron (CompositionCategory).",
        "keywords": ["composition category", "ultramafic", "mafic", "felsic", "calc-silicate", "silica"],
        "builder": gl_composition_category,
    },
    {
        "id": "gl_genetic_category",
        "name": "Genetic Classification & Rock Cycle",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE057,
        "description": "Petrogenetic process cycle linking igneous, sedimentary, metamorphic, and hydrothermal origins (GeneticCategory & EventProcess).",
        "keywords": ["genetic category", "petrogenesis", "rock cycle", "event process"],
        "builder": gl_genetic_category,
    },
    {
        "id": "gl_metamorphic_facies_pt",
        "name": "Metamorphic Facies & Grade (P-T Grid)",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE058,
        "description": "Pressure-Temperature metamorphic facies diagram with prograde-retrograde P-T-t loop (MetamorphicFacies & MetamorphicGrade).",
        "keywords": ["metamorphic facies", "greenschist", "amphibolite", "granulite", "eclogite", "blueschist", "metamorphic grade"],
        "builder": gl_metamorphic_facies_pt,
    },
    {
        "id": "gl_consolidation_degree",
        "name": "Consolidation & Induration Degree",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE059,
        "description": "Transition from loose unconsolidated sediment grains to compacted, cemented indurated rock (ConsolidationDegree).",
        "keywords": ["consolidation degree", "induration", "unconsolidated", "lithification", "diagenesis"],
        "builder": gl_consolidation_degree,
    },
    {
        "id": "gl_deformation_brittle_ductile",
        "name": "Brittle-Ductile Deformation Style",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE05A,
        "description": "Contrast between brittle fracture faulting and continuous ductile folding (DeformationStyle).",
        "keywords": ["deformation style", "brittle", "ductile", "brittle-ductile", "rheology"],
        "builder": gl_deformation_brittle_ductile,
    },
    {
        "id": "gl_unit_morphology",
        "name": "Geologic Unit Morphology (Boudin & Dome)",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE05B,
        "description": "3D/2D morphology of geological bodies including boudinage, domes, pipes, and diapirs (GeologicUnitMorphology).",
        "keywords": ["morphology", "boudin", "dome", "pipe", "ring dyke", "laccolith"],
        "builder": gl_unit_morphology,
    },
    {
        "id": "gl_style_disseminated",
        "name": "Disseminated Sulfide Texture",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE05C,
        "description": "Fine sulfide grains (<15% modal) scattered loosely through silicate host rock (GeologicalStyle.DISSEMINATED).",
        "keywords": ["disseminated", "heavily disseminated", "blebby", "interstitial", "sulfide texture", "geological style"],
        "builder": gl_style_disseminated,
    },
    {
        "id": "gl_style_net_textured",
        "name": "Net-Textured Matrix Sulfide",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE05D,
        "description": "Continuous intercumulus sulfide network (30-60% modal) enclosing rounded silicate crystals (GeologicalStyle.NET_TEXTURED).",
        "keywords": ["net textured", "matrix sulfide", "cumulate", "magmatic sulfide", "geological style"],
        "builder": gl_style_net_textured,
    },
    {
        "id": "gl_style_massive_sulfide",
        "name": "Semi-Massive & Massive Sulfide Ore",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE05E,
        "description": "Pooled solid massive sulfide ore (>80% modal) containing minor silicate clasts (GeologicalStyle.MASSIVE).",
        "keywords": ["massive sulfide", "semi massive", "pooled sulfide", "ore texture", "geological style"],
        "builder": gl_style_massive_sulfide,
    },
    {
        "id": "gl_style_veined_stringer",
        "name": "Veined & Stringer Stockwork Texture",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE05F,
        "description": "Planar structural veins and anastomosing stringer veinlets crosscutting host rock (GeologicalStyle.VEINED & STRINGER_VEIN).",
        "keywords": ["veined", "stringer vein", "patchy vein", "fracture controlled", "stockwork", "geological style"],
        "builder": gl_style_veined_stringer,
    },
    {
        "id": "gl_particle_shape_roundness",
        "name": "Particle Shape, Roundness & Aspect Ratio",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE060,
        "description": "Clast angularity/roundness and Sneed & Folk axial aspect ratio affecting porosity and demagnetization (ParticleShape & ParticleAspectRatio).",
        "keywords": ["particle shape", "angular", "rounded", "aspect ratio", "sneed folk", "clast"],
        "builder": gl_particle_shape_roundness,
    },
    {
        "id": "gl_contact_unconformity",
        "name": "Geological Contact & Unconformity",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE061,
        "description": "Angular unconformity and lithological boundary separating truncated dipping strata from overlying beds (ContactType).",
        "keywords": ["contact type", "unconformity", "intrusive contact", "conformable", "boundary"],
        "builder": gl_contact_unconformity,
    },
    {
        "id": "gl_foliation_lineation",
        "name": "Foliation & Mineral Lineation (S-L Fabric)",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE062,
        "description": "Inclined metamorphic foliation plane carrying down-dip mineral stretching lineations (FoliationType & LineationType).",
        "keywords": ["foliation", "lineation", "stretching lineation", "crenulation", "mylonite", "s-l tectonite"],
        "builder": gl_foliation_lineation,
    },
    {
        "id": "gl_borehole_drilling_methods",
        "name": "Rotary, RC & Auger Borehole Drilling",
        "domain": "Geological",
        "category": "Methods",
        "codepoint": 0xE063,
        "description": "Reverse-circulation (RC) and rotary tricone drilling bit with downhole air injection and inner sample return (BoreholeDrillingMethod).",
        "keywords": ["borehole drilling", "rc drilling", "rab", "rotary", "tricone", "auger"],
        "builder": gl_borehole_drilling_methods,
    },
    {
        "id": "gl_planar_polarity_overturned",
        "name": "Planar Polarity (Upright vs Overturned)",
        "domain": "Geological",
        "category": "Methods",
        "codepoint": 0xE064,
        "description": "Structural way-up polarity comparing upright bedding strike-and-dip with overturned bedding (PlanarPolarityCode).",
        "keywords": ["planar polarity", "upright", "overturned", "vertical", "way up", "younging"],
        "builder": gl_planar_polarity_overturned,
    },
    {
        "id": "gm_acid_rock_drainage",
        "name": "Acid Rock Drainage (ARD / NAPP / NAG)",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE065,
        "description": "Sulfide oxidation in waste rock generating acid rock drainage vs carbonate neutralization (AcidRockDrainageModel).",
        "keywords": ["ard", "amd", "acid rock drainage", "napp", "mpa", "anc", "nag ph", "environmental"],
        "builder": gm_acid_rock_drainage,
    },
    {
        "id": "gm_comminution_work_index",
        "name": "Comminution & Bond Work Index (Wi / SAG)",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE066,
        "description": "Tumbling SAG/ball mill grinding charge measuring rock comminution energy and Bond Work Index (ComminutionModel).",
        "keywords": ["comminution", "bond work index", "sag mill", "jk axb", "smc", "geometallurgy"],
        "builder": gm_comminution_work_index,
    },
    {
        "id": "gm_flotation_recovery",
        "name": "Mineral Liberation & Flotation Recovery",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE067,
        "description": "Froth flotation cell with agitated impeller and air bubbles levitating liberated sulfide particles (RecoveryModel).",
        "keywords": ["flotation", "recovery model", "klimpel", "liberation", "grade recovery", "geometallurgy"],
        "builder": gm_flotation_recovery,
    },
    {
        "id": "gc_melt_chemistry_f02",
        "name": "Silicate Melt Chemistry & Oxygen Fugacity (fO2)",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE068,
        "description": "Silicate melt polymerization (NBO/T, optical basicity) and FMQ oxygen fugacity buffer (MeltChemistryModel).",
        "keywords": ["melt chemistry", "oxygen fugacity", "fmq", "optical basicity", "nbo/t", "asi"],
        "builder": gc_melt_chemistry_f02,
    },
    {
        "id": "gc_carbon_mineralisation",
        "name": "Ultramafic CO2 Sequestration & Carbonation",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE069,
        "description": "CO2 mineralization and carbonate precipitation in serpentinized ultramafic and basaltic rocks (CarbonSequestrationModel).",
        "keywords": ["carbon sequestration", "mineral carbonation", "serpentinisation", "brucite", "forsterite", "co2"],
        "builder": gc_carbon_mineralisation,
    },
    {
        "id": "gl_lithology_tensor_anisotropy",
        "name": "Lithology Fabric & Tensor Anisotropy",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE06A,
        "description": "3D tilted transverse isotropic (TTI/VTI) property tensor ellipsoid aligned with rock foliation fabric (Lithology & PropertyTensor).",
        "keywords": ["anisotropy", "property tensor", "vti", "tti", "triaxial", "lithology fabric"],
        "builder": gl_lithology_tensor_anisotropy,
    },
    {
        "id": "gl_fault_normal_graben",
        "name": "Horst & Graben Extensional Rift",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE06B,
        "description": "Conjugate normal faults dropping a central graben rift valley between elevated horst shoulders (FaultType.HIGH_ANGLE_NORMAL_FAULT & EventProcess.RIFTING).",
        "keywords": ["graben", "horst", "rift", "normal fault", "extension", "fault.type"],
        "builder": gl_fault_normal_graben,
    },
    {
        "id": "gl_fault_thrust_ramp",
        "name": "Thrust Fault & Ramp-Flat Anticline",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE06C,
        "description": "Basal decollement ramping upward to form a hanging-wall fault-bend fold and thrust sheet (FaultMovementSense.THRUST_DECOLLEMENT).",
        "keywords": ["thrust", "ramp", "fault-bend fold", "decollement", "nappe", "compressional"],
        "builder": gl_fault_thrust_ramp,
    },
    {
        "id": "gl_fault_strike_slip_dextral",
        "name": "Dextral Strike-Slip & Riedel Shears",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE06D,
        "description": "Right-lateral horizontal strike-slip displacement accompanied by synthetic Riedel shear fractures (FaultMovementType.STRIKE_SLIP).",
        "keywords": ["strike slip", "dextral", "transcurrent", "riedel shear", "fault.movement.type"],
        "builder": gl_fault_strike_slip_dextral,
    },
    {
        "id": "gl_shear_zone_sigmoidal",
        "name": "Ductile Shear Zone & Delta Porphyroclast",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE06E,
        "description": "Mylonite ductile shear zone with a rotated delta porphyroclast showing kinematic sense of shear (DeformationStyle.DUCTILE & Mylonitic foliation).",
        "keywords": ["shear zone", "porphyroclast", "delta tail", "mylonite", "kinematic", "ductile"],
        "builder": gl_shear_zone_sigmoidal,
    },
    {
        "id": "gl_chevron_kink_fold",
        "name": "Chevron & Kink Band Folds",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE06F,
        "description": "Angular zigzag chevron fold train with straight planar limbs and sharp hinge lines (FoliationType.CRENULATION_CLEAVAGE).",
        "keywords": ["chevron fold", "kink band", "angular fold", "hinge", "crenulation"],
        "builder": gl_chevron_kink_fold,
    },
    {
        "id": "gl_ptygmatic_vein_fold",
        "name": "Ptygmatic Metamorphic Fold",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE070,
        "description": "Sinuous, tortuously folded competent quartz/leucosome vein enclosed in ductile metamorphic gneiss.",
        "keywords": ["ptygmatic", "migmatite", "meander vein", "viscous buckling", "ductile gneiss"],
        "builder": gl_ptygmatic_vein_fold,
    },
    {
        "id": "gl_columnar_jointing",
        "name": "Basalt Columnar Cooling Jointing",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE071,
        "description": "Array of vertical hexagonal prismatic basalt columns formed by thermal contraction during lava cooling (SimpleLithology.BASALT).",
        "keywords": ["columnar jointing", "hexagonal columns", "basalt", "thermal contraction", "cooling joints"],
        "builder": gl_columnar_jointing,
    },
    {
        "id": "gl_spinifex_texture",
        "name": "Komatiite Spinifex Texture",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE072,
        "description": "Criss-crossing bladed skeletal olivine and pyroxene needles formed by rapid quenching of ultramafic lava (SimpleLithology.KOMATIITE).",
        "keywords": ["spinifex", "komatiite", "ultramafic", "skeletal olivine", "quench texture"],
        "builder": gl_spinifex_texture,
    },
    {
        "id": "gl_pillow_lava",
        "name": "Pillow Basalt & Geopetal Way-Up",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE073,
        "description": "Submarine pillow lava toes with convex tops and downward-pointing cusps used as younging way-up indicators (SimpleLithology.PILLOW_BASALT).",
        "keywords": ["pillow basalt", "pillow lava", "geopetal", "way up", "subaqueous volcanism"],
        "builder": gl_pillow_lava,
    },
    {
        "id": "gl_fiamme_ignimbrite",
        "name": "Ignimbrite & Welded Fiamme",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE074,
        "description": "Flattened lenticular glassy pumice fiamme defining eutaxitic compaction fabric in welded pyroclastic tuff (ParticleType.FIAMME).",
        "keywords": ["fiamme", "ignimbrite", "pyroclastic", "welded tuff", "eutaxitic"],
        "builder": gl_fiamme_ignimbrite,
    },
    {
        "id": "gl_banded_iron_formation",
        "name": "Banded Iron Formation (BIF)",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE075,
        "description": "Precambrian chemical sedimentary rock with micro-laminated alternating beds of iron oxide and chert (SimpleLithology.BANDED_IRON_FORMATION).",
        "keywords": ["bif", "banded iron formation", "hematite", "magnetite", "jasper", "iron ore"],
        "builder": gl_banded_iron_formation,
    },
    {
        "id": "gl_hydrothermal_breccia",
        "name": "Hydrothermal Jigsaw Breccia",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE076,
        "description": "Angular wall-rock fragments with jigsaw-puzzle fit cemented by open-space hydrothermal quartz and sulfides (ParticleType.HYDROTHERMAL_VEIN).",
        "keywords": ["breccia", "hydrothermal breccia", "jigsaw", "hydraulic fracture", "epithermal"],
        "builder": gl_hydrothermal_breccia,
    },
    {
        "id": "gl_potassic_alteration",
        "name": "Potassic Hydrothermal Alteration",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE077,
        "description": "High-temperature core alteration envelope of secondary K-feldspar and biotite selvage flanking quartz-sulfide veinlets (AlterationType.POTASSIC).",
        "keywords": ["potassic", "k-feldspar", "biotite", "alteration", "porphyry core"],
        "builder": gl_potassic_alteration,
    },
    {
        "id": "gl_phyllic_sericitic_alteration",
        "name": "Phyllic (Sericitic / QSP) Alteration",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE078,
        "description": "Pervasive bleached alteration assemblage of quartz, sericite (white mica), and cubic pyrite (AlterationType.PHYLLIC).",
        "keywords": ["phyllic", "sericite", "qsp", "pyrite", "alteration halo"],
        "builder": gl_phyllic_sericitic_alteration,
    },
    {
        "id": "gl_advanced_argillic",
        "name": "Advanced Argillic & Vuggy Silica",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE079,
        "description": "Extreme acid-leached residual vuggy silica sponge lined with pyrophyllite, alunite, and dickite (AlterationType.ADVANCED_ARGILLIC_ALTERATION).",
        "keywords": ["advanced argillic", "vuggy silica", "alunite", "pyrophyllite", "high sulfidation"],
        "builder": gl_advanced_argillic,
    },
    {
        "id": "gl_propylitic_chlorite_epidote",
        "name": "Propylitic Alteration (Chlorite-Epidote)",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE07A,
        "description": "Low-temperature outer greenstone halo composed of epidote, chlorite, albite, and calcite (AlterationType.EPIDOTE_ALTERATION).",
        "keywords": ["propylitic", "epidote", "chlorite", "greenstone", "outer halo"],
        "builder": gl_propylitic_chlorite_epidote,
    },
    {
        "id": "gl_serpentinite_mesh",
        "name": "Serpentinisation Mesh Texture",
        "domain": "Geological",
        "category": "Processes",
        "codepoint": 0xE07B,
        "description": "Hydrothermal/metamorphic hydration of ultramafic peridotite with lizardite/antigorite mesh veins and magnetite (AlterationType.SERPENTINISATION).",
        "keywords": ["serpentinisation", "serpentine", "mesh texture", "antigorite", "lizardite", "ultramafic"],
        "builder": gl_serpentinite_mesh,
    },
    {
        "id": "gl_skarn_calc_silicate",
        "name": "Calc-Silicate Skarn Reaction Zone",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE07C,
        "description": "High-temperature contact metasomatic reaction zone between granite intrusion and carbonate marble with euhedral garnets (AlterationType.CALCSILICATE_ALTERATION).",
        "keywords": ["skarn", "calc-silicate", "andradite", "grossular", "metasomatism", "contact zone"],
        "builder": gl_skarn_calc_silicate,
    },
    {
        "id": "gl_greisen_cassiterite",
        "name": "Greisen & Twinned Cassiterite",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE07D,
        "description": "Pneumatolytic quartz-muscovite-topaz altered granite border containing geniculate twinned cassiterite elbow crystals (AlterationType.GREISEN).",
        "keywords": ["greisen", "cassiterite", "topaz", "tin", "tungsten", "pneumatolytic"],
        "builder": gl_greisen_cassiterite,
    },
    {
        "id": "gl_tourmaline_sun_rosette",
        "name": "Tourmaline Sun Rosette",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE07E,
        "description": "Starburst cluster of needle-like acicular schorl tourmaline crystals radiating from a common hydrothermal center (AlterationType.TOURMALINE).",
        "keywords": ["tourmaline", "tourmaline sun", "schorl", "boron metasomatism", "rosette"],
        "builder": gl_tourmaline_sun_rosette,
    },
    {
        "id": "gl_turbidite_bouma_sequence",
        "name": "Turbidite Bouma Sequence (Ta-Te)",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE07F,
        "description": "Idealized submarine gravity-flow turbidite deposit displaying graded sand (Ta), laminated sand (Tb), ripples (Tc), silt (Td), and pelagite (Te).",
        "keywords": ["turbidite", "bouma sequence", "gravity flow", "submarine fan", "graded bedding"],
        "builder": gl_turbidite_bouma_sequence,
    },
    {
        "id": "gl_fluvial_point_bar_channel",
        "name": "Fluvial Point Bar & Meander Channel",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE080,
        "description": "Sinuous meandering river channel with outer cut-bank erosion and inner point-bar lateral accretion clinoforms (EventEnvironment.FLOODPLAIN).",
        "keywords": ["meander", "point bar", "fluvial", "channel", "lateral accretion", "cut bank"],
        "builder": gl_fluvial_point_bar_channel,
    },
]
