"""
Geophysical Icon Definitions (15 icons):
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


def gp_seismic_reflection():
    """Seismic Reflection Survey: surface source star, geophones, subsurface reflectors, and V-shaped reflection raypaths."""
    parts = [
        # Ground surface
        line(70, 740, 930, 740, 36),
        # Subsurface horizon 1 & 2
        line(90, 440, 910, 440, 32),
        dashed_line(90, 200, 910, 200, 32, dash_count=7),
        # Source star at left (180, 740)
        circle(180, 790, 48),
        line(180, 790, 110, 875, 28),
        line(180, 790, 180, 900, 28),
        line(180, 790, 250, 875, 28),
        # Geophones at surface (540, 740) and (820, 740)
        poly([(500, 820), (580, 820), (540, 735)]),
        line(540, 820, 540, 870, 28),
        poly([(780, 820), (860, 820), (820, 735)]),
        line(820, 820, 820, 870, 28),
        # Raypath 1: shallow reflection (180,740) -> (360,440) -> (540,740)
        stroke([(180, 740), (360, 440), (540, 740)], 30),
        arrow_head(485, 648, 59, 85, 48),
        # Raypath 2: deep reflection (180,740) -> (500,200) -> (820,740)
        stroke([(180, 740), (500, 200), (820, 740)], 30),
        arrow_head(725, 580, 59, 85, 48),
    ]
    return union_all(parts)


def gp_gravity_survey():
    """Gravity Survey: Bouguer anomaly profile at top, gravimeter spring-mass sensor, and dense subsurface body."""
    # Bouguer gravity bell-curve at top
    curve_pts = []
    for i in range(41):
        t = i / 40.0
        x = 100 + 800 * t
        y = 740 + 165 * math.exp(-((t - 0.5) ** 2) / 0.035)
        curve_pts.append((x, y))
    # Spring coil inside gravimeter frame
    spring_pts = [
        (360, 620),
        (430, 585),
        (290, 545),
        (430, 505),
        (290, 465),
        (360, 430),
    ]
    parts = [
        stroke(curve_pts, 34),
        dashed_line(100, 735, 900, 735, 22, dash_count=8),
        # Gravimeter housing on left-center
        rounded_rect_outline(210, 250, 510, 660, 35, 32),
        stroke(spring_pts, 28),
        # Proof mass suspended from spring
        rounded_rect(285, 310, 435, 425, 20),
        # Dense ore body on right with downward gravity vector g
        circle(730, 450, 135),
        arrow(730, 300, 730, 110, 38, 100, 58),
    ]
    return diff(union_all(parts), circle(730, 450, 55))


def gp_magnetic_survey():
    """Magnetic Survey: inclined dipolar target bar with symmetrical magnetic flux loops and surface sensor."""
    # Rotated dipole bar in center
    dipole_outer = rounded_rect(425, 260, 575, 660, 28)
    dipole_hollow = rect(455, 290, 545, 455)  # South pole hollow, North pole solid
    dipole = diff(dipole_outer, dipole_hollow)

    parts = [
        dipole,
        # Left flux loops (inner and outer)
        ellipse_outline(330, 460, 155, 210, 30),
        ellipse_outline(255, 460, 225, 300, 28),
        arrow_head(180, 495, -90, 85, 48),
        # Right flux loops (inner and outer)
        ellipse_outline(670, 460, 155, 210, 30),
        ellipse_outline(745, 460, 225, 300, 28),
        arrow_head(820, 495, -90, 85, 48),
        # Airborne/ground magnetometer sensor at top
        rounded_rect(370, 825, 630, 910, 35),
        line(500, 750, 500, 825, 30),
    ]
    # Clean inside of dipole from flux ellipses
    base = diff(union_all(parts[1:]), rounded_rect(405, 240, 595, 680, 20))
    return union_all([base, dipole])


def gp_electromagnetic_em():
    """Electromagnetic (TEM/FDEM) Induction: Tx and Rx coils, primary/secondary EM waves, and subsurface eddy currents."""
    parts = [
        # Ground line
        dashed_line(70, 620, 930, 620, 26, dash_count=9),
        # Tx loop on top-left
        ellipse_outline(250, 780, 150, 65, 34),
        circle(250, 780, 28),
        # Rx loop on top-right
        ellipse_outline(750, 780, 150, 65, 34),
        circle(750, 780, 28),
        # Primary field arc from Tx to conductor
        curved_arrow(430, 580, 250, 145, 235, 30, 85, 48),
        # Secondary field arc from conductor to Rx
        curved_arrow(570, 580, 250, -55, 35, 30, 85, 48),
        # Subsurface conductive body & induced eddy current rings
        ellipse_outline(500, 260, 290, 145, 34),
        ellipse_outline(500, 260, 175, 82, 30),
        circle(500, 260, 32),
        arrow_head(500, 405, 180, 85, 48),
        arrow_head(500, 115, 0, 85, 48),
    ]
    return union_all(parts)


def gp_ert_ip():
    """Electrical Resistivity / IP Survey: 4 surface stakes (C1, P1, P2, C2) with semicircular current paths in ground."""
    stakes_x = [140, 380, 620, 860]
    parts = [
        # Ground line
        line(60, 680, 940, 680, 36),
        # Wire connecting outer current electrodes C1-C2 through top source meter
        stroke([(140, 750), (140, 860), (415, 860)], 28),
        stroke([(585, 860), (860, 860), (860, 750)], 28),
        disk_ring(500, 860, 80, 32),
        # Plus/minus or wave inside meter
        line(465, 860, 535, 860, 26),
        line(500, 825, 500, 895, 26),
        # Semicircular current flow lines below ground
        arc(500, 680, 130, 195, 345, 28),
        arc(500, 680, 255, 192, 348, 30),
        arc(500, 680, 380, 190, 350, 32),
        arrow_head(535, 300, 0, 85, 48),
        arrow_head(535, 425, 0, 80, 45),
    ]
    for x in stakes_x:
        parts.append(poly([(x - 36, 760), (x + 36, 760), (x, 600)]))
    return union_all(parts)


def gp_velocity_model():
    """Seismic Velocity Model (Vp/Vs): Subsurface velocity layers with step-velocity log and wavefront rays."""
    parts = [
        # Outer model frame
        rect_outline(90, 90, 910, 910, 36),
        # Layer boundaries (dipping / undulating)
        stroke([(90, 680), (480, 680), (910, 620)], 30),
        stroke([(90, 450), (520, 410), (910, 410)], 30),
        stroke([(90, 240), (910, 240)], 30),
        # Stepwise 1D velocity function V(z) in bold
        stroke(
            [
                (230, 900),
                (230, 680),
                (420, 680),
                (420, 430),
                (630, 430),
                (630, 240),
                (800, 240),
                (800, 100),
            ],
            44,
        ),
        # Velocity gradient dots/markers in layers
        circle(740, 775, 28),
        circle(700, 535, 28),
        circle(790, 535, 28),
        circle(260, 335, 28),
        circle(350, 335, 28),
        circle(440, 335, 28),
    ]
    return union_all(parts)


def gp_density_model():
    """Density Block Model (Delta-rho): Discretized 2D voxel grid with high-density core anomaly and gravity curve."""
    parts = []
    # Top gravity curve
    curve_pts = []
    for i in range(33):
        t = i / 32.0
        x = 110 + 780 * t
        y = 755 + 155 * math.exp(-((t - 0.5) ** 2) / 0.04)
        curve_pts.append((x, y))
    parts.append(stroke(curve_pts, 36))

    # 5 cols x 4 rows voxel grid in lower two-thirds
    cols, rows = 5, 4
    x0, y0, w, h = 110, 90, 780, 580
    cw, ch = w / cols, h / rows
    # Outer grid frame and grid lines
    parts.append(rect_outline(x0, y0, x0 + w, y0 + h, 32))
    for c in range(1, cols):
        parts.append(line(x0 + c * cw, y0, x0 + c * cw, y0 + h, 24))
    for r in range(1, rows):
        parts.append(line(x0, y0 + r * ch, x0 + w, y0 + r * ch, 24))

    # Fill dense core cells (center cells solid, surrounding medium density dots)
    dense_cells = [(2, 1), (2, 2), (1, 1), (3, 1)]
    medium_cells = [(1, 2), (3, 2), (2, 0)]
    for c, r in dense_cells:
        parts.append(rect(x0 + c * cw + 22, y0 + r * ch + 22, x0 + (c + 1) * cw - 22, y0 + (r + 1) * ch - 22))
    for c, r in medium_cells:
        cx = x0 + (c + 0.5) * cw
        cy = y0 + (r + 0.5) * ch
        parts.append(circle(cx, cy, 34))
    return union_all(parts)


def gp_susceptibility_model():
    """Magnetic Susceptibility Voxel Model (Chi): Grid cells containing aligned/induced dipole magnetization vectors."""
    parts = [
        rect_outline(95, 95, 905, 905, 36),
        line(365, 95, 365, 905, 26),
        line(635, 95, 635, 905, 26),
        line(95, 365, 905, 365, 26),
        line(95, 635, 905, 635, 26),
    ]
    # 3x3 cells with magnetization arrows (center cell highlighted with thick border and strong vector)
    centers = [230, 500, 770]
    angles = [
        [45, 65, 45],
        [60, 65, 60],
        [35, 65, 35],
    ]
    for r_idx, cy in enumerate(centers):
        for c_idx, cx in enumerate(centers):
            ang = math.radians(angles[r_idx][c_idx])
            rad = 85 if (r_idx == 1 and c_idx == 1) else 70
            dx = rad * math.cos(ang)
            dy = rad * math.sin(ang)
            parts.append(arrow(cx - dx, cy - dy, cx + dx, cy + dy, 28, 72, 42))
    # Highlight anomalous center susceptibility block
    parts.append(rect_outline(365, 365, 635, 635, 44))
    return union_all(parts)


def gp_resistivity_section():
    """Inverted Resistivity Pseudosection: Trapezoidal ERT depth section with conductive/resistive contour anomaly."""
    trap_pts = [(75, 760), (925, 760), (710, 140), (290, 140)]
    parts = [
        # Trapezoidal section boundary
        stroke(trap_pts, 36, closed=True),
        # Surface electrode ticks
        line(160, 760, 160, 845, 32),
        line(330, 760, 330, 845, 32),
        line(500, 760, 500, 845, 32),
        line(670, 760, 670, 845, 32),
        line(840, 760, 840, 845, 32),
        # Pseudosection level lines
        dashed_line(145, 560, 855, 560, 22, dash_count=7),
        dashed_line(220, 350, 780, 350, 22, dash_count=5),
        # Iso-resistivity anomaly contours in center of section
        ellipse_outline(500, 480, 195, 115, 32),
        ellipse(500, 480, 95, 52),
    ]
    return union_all(parts)


def gp_seismic_cube_3d():
    """3D Seismic Volume Cube: Isometric cube displaying inline, crossline, and time-slice seismic reflections."""
    # Isometric vertices
    top = [(500, 920), (880, 720), (500, 520), (120, 720)]
    left = [(120, 720), (500, 520), (500, 80), (120, 280)]
    right = [(500, 520), (880, 720), (880, 280), (500, 80)]
    parts = [
        stroke(top, 36, closed=True),
        stroke(left, 36, closed=True),
        stroke(right, 36, closed=True),
        # Seismic horizons across left (inline) and right (crossline) faces
        stroke([(120, 570), (310, 495), (500, 370), (690, 470), (880, 570)], 30),
        stroke([(120, 425), (310, 340), (500, 225), (690, 325), (880, 425)], 30),
        # Time slice contour on top face
        ellipse_outline(500, 720, 175, 78, 28),
        ellipse(500, 720, 65, 28),
    ]
    return union_all(parts)


def gp_wave_propagation():
    """Seismic Wave Propagation: Hypocenter star radiating concentric P- and S-wavefronts with ray vector."""
    cx, cy = 200, 200
    parts = [
        # Hypocenter focal star
        circle(cx, cy, 65),
        # Expanding wavefront arcs in quadrant 1
        arc(cx, cy, 240, 8, 82, 34),
        arc(cx, cy, 420, 8, 82, 36),
        arc(cx, cy, 600, 8, 82, 38),
        # Ray direction arrow with shear wave wiggle along diagonal
        sine_wave(260, 260, 760, 760, amp=42, cycles=3.5, width=30),
        arrow_head(865, 865, 45, 110, 62),
        line(745, 745, 820, 820, 34),
    ]
    return union_all(parts)


def gp_ray_refraction_snell():
    """Snell's Law & Critical Refraction: Incident ray, refracted ray, critical head-wave along V2 > V1 interface."""
    parts = [
        # Interface boundary between Layer 1 (V1) and Layer 2 (V2 > V1)
        line(70, 500, 930, 500, 38),
        # Normal dashed line at incidence point (340, 500)
        dashed_line(340, 140, 340, 860, 26, dash_count=7),
        # Incident ray from top-left to (340, 500)
        arrow(120, 840, 330, 515, 36, 95, 54),
        # Refracted ray bent closer to interface in lower layer (smaller grazing angle)
        arrow(340, 500, 860, 210, 36, 95, 54),
        # Critical head wave traveling along interface and emerging upward to surface
        stroke([(340, 500), (660, 500)], 44),
        arrow(660, 500, 870, 825, 34, 95, 54),
        # Angle arcs showing theta_1 < theta_2
        arc(340, 500, 140, 90, 123, 24),
        arc(340, 500, 180, -90, -29, 24),
    ]
    return union_all(parts)


def gp_geophysical_inversion():
    """Geophysical Forward/Inverse Loop: Iterative transformation between observed data curve and subsurface earth model."""
    # Top data waveform box
    wave_pts = []
    for i in range(31):
        t = i / 30.0
        x = 120 + 300 * t
        y = 730 + 95 * math.sin(2 * math.pi * t)
        wave_pts.append((x, y))

    parts = [
        # Top-left: Data space (d_obs)
        rounded_rect_outline(80, 580, 460, 880, 30, 32),
        stroke(wave_pts, 32),
        # Bottom-right: Model space (m) discretized grid
        rect_outline(540, 100, 920, 440, 32),
        line(666, 100, 666, 440, 24),
        line(793, 100, 793, 440, 24),
        line(540, 213, 920, 213, 24),
        line(540, 326, 920, 326, 24),
        rect(666, 213, 793, 326),
        # Top-right curved arrow: Inverse operator F^-1 (Data -> Model)
        curved_arrow(520, 540, 260, 80, -5, 36, 100, 58),
        # Bottom-left curved arrow: Forward operator F(m) (Model -> Data)
        curved_arrow(480, 460, 260, 260, 175, 36, 100, 58),
    ]
    return union_all(parts)


def gp_signal_deconvolution():
    """Seismic Deconvolution: Convolved wavelet trace transformed via filter operator into clean reflectivity spikes."""
    # Left wavelet (Ricker wavelet vertical trace)
    ricker_pts = []
    for i in range(61):
        t = (i / 60.0 - 0.5) * 4.0
        y = 140 + (i / 60.0) * 720
        amp = (1.0 - 2.0 * (t ** 2)) * math.exp(-(t ** 2))
        x = 210 + 145 * amp
        ricker_pts.append((x, y))

    parts = [
        # Baseline for wavelet
        dashed_line(210, 110, 210, 890, 22, dash_count=8),
        stroke(ricker_pts, 36),
        # Deconvolution transformation arrow in center
        arrow(390, 500, 575, 500, 40, 100, 58),
        # Right reflectivity spike series (impulse train)
        line(670, 110, 670, 890, 32),
        line(670, 740, 890, 740, 40),
        circle(890, 740, 36),
        line(670, 520, 580, 520, 36),
        circle(580, 520, 32),
        line(670, 290, 860, 290, 40),
        circle(860, 290, 36),
    ]
    return union_all(parts)


def gp_nmo_stacking():
    """NMO Correction & Stacking: Hyperbolic CMP reflection moveout curves flattened into horizontal NMO-corrected events."""
    # Bottom hyperbolic moveout curves
    hyp1 = []
    hyp2 = []
    for i in range(41):
        t = (i / 40.0 - 0.5) * 2.0  # -1..1
        x = 120 + (i / 40.0) * 760
        y1 = 440 - 250 * (math.sqrt(1.0 + 1.4 * t * t) - 1.0)
        y2 = 260 - 210 * (math.sqrt(1.0 + 1.4 * t * t) - 1.0)
        hyp1.append((x, y1))
        hyp2.append((x, y2))

    parts = [
        # Vertical CMP gather traces (background)
        dashed_line(220, 90, 220, 910, 22, dash_count=9),
        dashed_line(500, 90, 500, 910, 22, dash_count=9),
        dashed_line(780, 90, 780, 910, 22, dash_count=9),
        # Uncorrected NMO hyperbolas (lower half)
        stroke(hyp1, 36),
        stroke(hyp2, 34),
        # Upward NMO correction arrows on outer offsets
        arrow(160, 340, 160, 670, 32, 85, 48),
        arrow(840, 340, 840, 670, 32, 85, 48),
        # Flattened horizontal reflection horizons (top half)
        line(110, 730, 890, 730, 42),
        line(110, 850, 890, 850, 42),
    ]
    return union_all(parts)


GEOPHYSICAL_ICONS: List[Dict[str, Any]] = [
    {
        "id": "gp_seismic_reflection",
        "name": "Seismic Reflection Survey",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE001,
        "description": "Active seismic source and geophone receiver array recording subsurface horizon reflections.",
        "keywords": ["seismic", "reflection", "geophone", "raypath", "survey", "horizon"],
        "builder": gp_seismic_reflection,
    },
    {
        "id": "gp_gravity_survey",
        "name": "Gravity Survey",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE002,
        "description": "Relative/absolute gravimeter spring-mass sensor measuring Bouguer gravity anomaly over dense body.",
        "keywords": ["gravity", "gravimeter", "bouguer", "anomaly", "mass", "mgal"],
        "builder": gp_gravity_survey,
    },
    {
        "id": "gp_magnetic_survey",
        "name": "Magnetic Survey",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE003,
        "description": "Magnetometer sensor measuring dipolar magnetic flux lines around a magnetized subsurface body.",
        "keywords": ["magnetics", "dipole", "flux", "magnetometer", "tmi", "anomaly"],
        "builder": gp_magnetic_survey,
    },
    {
        "id": "gp_electromagnetic_em",
        "name": "Electromagnetic (EM) Induction",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE004,
        "description": "Transmitter and receiver coils inducing and measuring secondary eddy currents in a conductor.",
        "keywords": ["em", "electromagnetic", "tem", "fdem", "induction", "eddy current", "coil"],
        "builder": gp_electromagnetic_em,
    },
    {
        "id": "gp_ert_ip",
        "name": "Electrical Resistivity & IP (ERT/IP)",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE005,
        "description": "Four-electrode galvanic array injecting current and measuring subsurface potential distribution.",
        "keywords": ["ert", "ip", "resistivity", "induced polarization", "electrode", "wenner", "schlumberger"],
        "builder": gp_ert_ip,
    },
    {
        "id": "gp_velocity_model",
        "name": "Seismic Velocity Model",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE006,
        "description": "Layered subsurface seismic velocity structure (Vp/Vs) with depth-increasing velocity profile.",
        "keywords": ["velocity model", "vp", "vs", "layered", "seismic velocity", "tomography"],
        "builder": gp_velocity_model,
    },
    {
        "id": "gp_density_model",
        "name": "Density Contrast Block Model",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE007,
        "description": "Discretized subsurface density voxel grid (delta-rho) with corresponding surface gravity response.",
        "keywords": ["density model", "voxel", "gravity inversion", "block model", "rho"],
        "builder": gp_density_model,
    },
    {
        "id": "gp_susceptibility_model",
        "name": "Magnetic Susceptibility Model",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE008,
        "description": "Discretized cell model of magnetic susceptibility (chi) and magnetization vector orientation.",
        "keywords": ["susceptibility", "magnetization", "mvi", "chi", "voxel", "magnetic model"],
        "builder": gp_susceptibility_model,
    },
    {
        "id": "gp_resistivity_section",
        "name": "Resistivity Pseudosection",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE009,
        "description": "Trapezoidal 2D electrical resistivity depth section showing conductive/resistive anomaly contours.",
        "keywords": ["pseudosection", "resistivity section", "ert model", "conductivity", "ohm-m"],
        "builder": gp_resistivity_section,
    },
    {
        "id": "gp_seismic_cube_3d",
        "name": "3D Seismic Volume Cube",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE00A,
        "description": "Isometric 3D seismic reflection volume displaying inline, crossline, and time-slice sections.",
        "keywords": ["3d seismic", "seismic cube", "inline", "crossline", "time slice", "volume"],
        "builder": gp_seismic_cube_3d,
    },
    {
        "id": "gp_wave_propagation",
        "name": "Seismic Wave Propagation",
        "domain": "Geophysical",
        "category": "Processes",
        "codepoint": 0xE00B,
        "description": "Expanding spherical P- and S-wavefronts radiating outward from a seismic source hypocenter.",
        "keywords": ["wavefront", "propagation", "p-wave", "s-wave", "seismic wave", "huygens"],
        "builder": gp_wave_propagation,
    },
    {
        "id": "gp_ray_refraction_snell",
        "name": "Snell's Law & Critical Refraction",
        "domain": "Geophysical",
        "category": "Processes",
        "codepoint": 0xE00C,
        "description": "Ray bending across an acoustic impedance interface and head-wave refraction at the critical angle.",
        "keywords": ["snell", "refraction", "head wave", "critical angle", "ray tracing"],
        "builder": gp_ray_refraction_snell,
    },
    {
        "id": "gp_geophysical_inversion",
        "name": "Forward & Inverse Modeling",
        "domain": "Geophysical",
        "category": "Processes",
        "codepoint": 0xE00D,
        "description": "Iterative geophysical inversion cycle mapping between observed geophysical data and earth model parameters.",
        "keywords": ["inversion", "forward modeling", "optimization", "data fit", "regularization"],
        "builder": gp_geophysical_inversion,
    },
    {
        "id": "gp_signal_deconvolution",
        "name": "Wavelet Deconvolution",
        "domain": "Geophysical",
        "category": "Processes",
        "codepoint": 0xE00E,
        "description": "Signal processing compressing a seismic source wavelet into sharp earth reflectivity spikes.",
        "keywords": ["deconvolution", "wavelet", "ricker", "reflectivity", "signal processing", "fft"],
        "builder": gp_signal_deconvolution,
    },
    {
        "id": "gp_nmo_stacking",
        "name": "NMO Correction & Stacking",
        "domain": "Geophysical",
        "category": "Processes",
        "codepoint": 0xE00F,
        "description": "Normal Moveout correction flattening hyperbolic offset reflection gathers into aligned horizons.",
        "keywords": ["nmo", "normal moveout", "stacking", "cmp gather", "hyperbola", "seismic processing"],
        "builder": gp_nmo_stacking,
    },
]
