"""
Mineralis Inversion, Petrophysics, and Thermodynamic Icon Definitions (22 icons, U+E0AC..U+E0C1).
Comprehensive icon suite covering:
  - Gibbs free energy, Elements, Minerals, Element differences (in wt pct)
  - Temperature, Pressure, Gradient perturbation factor, L1 norm, n iterations
  - Thermodynamics, Petrophysics, Positions, Volatiles, aH2O, XCO2, FO2, Oxides
  - Gradient descent initial step size, Jacobian sensitivity, Specific gravity,
    Logarithmic residual error, and Geological domain tagging.
Directly aligned with:
  - C:\\projects\\opus\\opus.geo.geochemistry (Mineralis inversion, thermodynamics, petrophysics, assay)
"""

import math
from typing import Dict, Any, List
import numpy as np
from shapely.geometry import Polygon

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


def gc_gibbs_free_energy():
    """Gibbs Free Energy Minimisation (Delta-G): Thermodynamic potential well curve showing free energy landscape, global equilibrium minimum, and Delta-G symbol."""
    y_axis = arrow(140, 140, 140, 890, 32, 80, 44)
    x_axis = arrow(110, 180, 900, 180, 32, 80, 44)

    curve_pts = []
    for i in range(51):
        t = i / 50.0
        x = 180 + 680 * t
        s = t - 0.70
        y = 260 + 950 * (s ** 2) - 350 * (s ** 3) + 110 * math.exp(-(((t - 0.25) / 0.15) ** 2))
        curve_pts.append((x, y))

    landscape = stroke(curve_pts, 38)
    marble = circle(656, 310, 42)
    eq_arrow = arrow(656, 480, 656, 360, 26, 65, 36)

    # Delta symbol
    delta_outer = poly([(220, 710), (330, 880), (440, 710)])
    delta_inner = poly([(255, 735), (330, 845), (405, 735)])
    delta_sym = delta_outer.difference(delta_inner)

    # Capital G symbol
    g_arc = arc(510, 790, 85, 45, 315, 30)
    g_bar = line(510, 790, 595, 790, 30)
    g_vert = line(595, 730, 595, 795, 30)
    g_sym = union_all([g_arc, g_bar, g_vert])

    d_line1 = dashed_line(140, 720, 656, 720, 22, 6)
    d_line2 = dashed_line(140, 260, 656, 260, 22, 6)
    delta_g_bracket = arrow(180, 710, 180, 270, 24, 60, 32, both_ends=True)

    return union_all([y_axis, x_axis, landscape, marble, eq_arrow, delta_sym, g_sym, d_line1, d_line2, delta_g_bracket])


def gc_chemical_elements():
    """Chemical Elements & Atomic Structure: Periodic table element tile with Rutherford-Bohr electron orbitals and atomic nucleus."""
    parts = [
        rounded_rect_outline(140, 140, 860, 860, 70, 34),
        circle(500, 500, 58),
        ellipse_outline(500, 500, 290, 110, width=28, angle_deg=0),
        ellipse_outline(500, 500, 290, 110, width=28, angle_deg=60),
        ellipse_outline(500, 500, 290, 110, width=28, angle_deg=-60),
        circle(790, 500, 24),
        circle(210, 500, 24),
        circle(355, 750, 24),
        circle(645, 250, 24),
        circle(355, 250, 24),
        circle(645, 750, 24),
        rect(180, 780, 300, 820),
        rect(340, 180, 660, 215),
    ]
    return union_all(parts)


def gl_minerals_specimen():
    """Minerals & Crystal Aggregate: Idiomorphic cluster of prismatic mineral crystals on rock base with termination pyramids."""
    parts = [
        poly([(130, 150), (130, 280), (240, 320), (420, 270), (600, 310), (780, 260), (870, 300), (870, 150)]),
        line(190, 220, 360, 220, 22),
        line(480, 200, 680, 200, 22),
        line(720, 230, 820, 230, 22),
        # Central dominant crystal
        poly([(420, 280), (420, 720), (500, 890), (500, 690), (500, 280)]),
        poly([(514, 280), (514, 690), (500, 890), (580, 720), (580, 280)]),
        line(435, 450, 485, 450, 18),
        line(435, 530, 485, 530, 18),
        line(435, 610, 485, 610, 18),
        line(528, 470, 565, 470, 18),
        line(528, 550, 565, 550, 18),
        # Left inclined crystal
        poly([(220, 290), (230, 580), (270, 710), (330, 590), (340, 290), (280, 290)]),
        line(270, 710, 285, 290, 20),
        # Right inclined crystal
        poly([(660, 290), (670, 600), (730, 740), (790, 610), (780, 280), (720, 280)]),
        line(730, 740, 725, 285, 20),
        # Flanking crystal needles
        poly([(150, 260), (160, 440), (180, 510), (210, 430), (210, 270)]),
        poly([(790, 270), (810, 450), (830, 530), (860, 440), (850, 270)]),
    ]
    return union_all(parts)


def gc_element_diff_wtpct():
    """Element Difference in Weight Percent (Delta-wt%): Comparative assay bars with discrepancy gap, Delta symbol, and wt% notation."""
    parts = [
        line(140, 180, 860, 180, 34),
        rect(200, 180, 340, 640),
        rect(400, 180, 540, 400),
        dashed_line(340, 640, 570, 640, 24, 4),
        arrow(470, 410, 470, 630, 28, 65, 36, both_ends=True),
        poly([(210, 700), (270, 860), (330, 700)]).difference(
            poly([(235, 720), (270, 830), (305, 720)])
        ),
        line(650, 260, 830, 820, 36),
        disk_ring(670, 700, 65, 28),
        disk_ring(810, 380, 65, 28),
    ]
    return union_all(parts)


def gc_temperature_thermo():
    """Temperature & Geothermometry (T / Celsius): Scientific graduated thermometer with thermal bulb, mercury column, and degree Celsius mark."""
    parts = [
        disk_ring(440, 250, 110, 32),
        circle(440, 250, 75),
        rect_outline(400, 250, 480, 860, 32),
        arc(440, 860, 40, 0, 180, 32),
        rect(422, 250, 458, 670),
        circle(440, 670, 18),
        line(496, 400, 560, 400, 26),
        line(496, 470, 590, 470, 32),
        line(496, 540, 560, 540, 26),
        line(496, 610, 590, 610, 32),
        line(496, 680, 560, 680, 26),
        line(496, 750, 590, 750, 32),
        line(496, 820, 560, 820, 26),
        disk_ring(710, 800, 36, 22),
        arc(790, 680, 95, 45, 315, 32),
        arc(440, 250, 160, 215, 325, 26),
        arc(440, 250, 210, 225, 315, 24),
    ]
    return union_all(parts)


def gc_pressure_gauge():
    """Pressure & Geobarometry (P / Gauge): High-pressure Bourdon dial gauge with needle, pressure scale ticks, inlet fitting, and P symbol."""
    cx, cy, r = 500, 560, 320
    parts = [
        disk_ring(cx, cy, r, 36),
        rect(445, 120, 555, 260),
        rect(410, 160, 590, 210),
        arc(cx, cy, 260, 40, 320, 22),
    ]
    for deg in [45, 75, 105, 135, 165, 195, 225, 255, 285, 315]:
        rad = math.radians(deg)
        r1 = 235 if deg % 45 == 0 else 250
        r2 = 280
        parts.append(
            line(
                cx + r1 * math.cos(rad),
                cy + r1 * math.sin(rad),
                cx + r2 * math.cos(rad),
                cy + r2 * math.sin(rad),
                30 if deg % 45 == 0 else 20,
            )
        )

    parts.append(arc(cx, cy, 285, 40, 90, 32))
    parts.append(circle(cx, cy, 48))

    needle_ang = 60
    n_rad = math.radians(needle_ang)
    tx = cx + 240 * math.cos(n_rad)
    ty = cy + 240 * math.sin(n_rad)
    parts.append(arrow(cx, cy, tx, ty, 32, 70, 38))

    p_stem = line(450, 370, 450, 470, 28)
    p_loop = arc(450, 440, 30, -90, 90, 28)
    parts.append(p_stem)
    parts.append(p_loop)

    return union_all(parts)


def gc_gradient_perturbation_factor():
    """Gradient Perturbation Factor (delta-nabla): Nabla vector differential operator with numerical perturbation step delta and sensitivity offset."""
    parts = [
        line(220, 820, 780, 820, 38),
        line(230, 820, 500, 420, 38),
        line(770, 820, 500, 420, 38),
        circle(500, 420, 26),
        dashed_line(500, 420, 740, 420, 26, 4),
        dashed_line(740, 420, 740, 220, 26, 4),
        arrow(500, 420, 820, 160, 36, 85, 48),
        arc(320, 360, 140, 35, 145, 28),
        arc(320, 360, 95, 30, 150, 28),
        arc(320, 360, 50, 25, 155, 28),
        circle(320, 360, 18),
    ]
    return union_all(parts)


def gc_l1_norm_regularization():
    """L1 Norm Sparse Regularization (||x||_1): Diamond unit ball (|x1| + |x2| <= 1), Cartesian axes, and Manhattan taxicab path."""
    cx, cy = 500, 500
    r = 290
    parts = [
        arrow(140, cy, 860, cy, 30, 70, 40),
        arrow(cx, 140, cx, 860, 30, 70, 40),
        stroke([(cx, cy + r), (cx + r, cy), (cx, cy - r), (cx - r, cy), (cx, cy + r)], width=36, closed=True),
        stroke([(cx, cy), (cx + 145, cy), (cx + 145, cy + 145), (cx + 290, cy + 145)], width=28),
        line(180, 720, 180, 840, 28),
        line(205, 720, 205, 840, 28),
        line(795, 720, 795, 840, 28),
        line(820, 720, 820, 840, 28),
        line(845, 720, 845, 760, 24),
        line(835, 750, 845, 760, 24),
    ]
    return union_all(parts)


def gc_n_iterations_loop():
    """Optimization Iteration Loop (n Iterations): Recurrent circular process loop with directional arrows enclosing the n-iteration counter."""
    cx, cy, r = 500, 500, 320
    parts = [
        curved_arrow(cx, cy, r, 195, 25, width=36, head_len=85, head_half_width=48),
        curved_arrow(cx, cy, r, 15, -155, width=36, head_len=85, head_half_width=48),
        line(410, 350, 410, 620, 38),
        arc(485, 545, 75, 0, 180, 38),
        line(560, 350, 560, 545, 38),
        line(380, 350, 440, 350, 28),
        line(530, 350, 590, 350, 28),
        circle(380, 250, 22),
        circle(460, 250, 22),
        circle(540, 250, 22),
        circle(620, 250, 22),
    ]
    return union_all(parts)


def gc_thermodynamics_system():
    """Thermodynamic System & Heat Cycle: Closed thermodynamic system boundary with heat input (Q), work output (W), and thermal equilibrium."""
    parts = [
        rounded_rect_outline(240, 280, 760, 760, 40, 36),
        poly([(500, 120), (460, 220), (500, 320), (540, 220)]),
        poly([(420, 140), (390, 210), (430, 280), (450, 200)]),
        poly([(580, 140), (550, 200), (570, 280), (610, 210)]),
        arrow(500, 220, 500, 360, 32, 65, 36),
        arrow(720, 520, 890, 520, 36, 85, 48),
        stroke([(370, 450), (430, 620), (630, 580), (570, 420), (370, 450)], width=30, closed=True),
        arrow_head(400, 535, 70, 55, 30),
        arrow_head(530, 600, -10, 55, 30),
        arrow_head(600, 500, -110, 55, 30),
        arrow_head(470, 435, 170, 55, 30),
    ]
    return union_all(parts)


def gp_petrophysics_core_matrix():
    """Petrophysics & Core Plug Porosity: Cylindrical drill core specimen showing solid mineral grain matrix, pore network, and permeability fluid lines."""
    cx, cy = 500, 740
    rx, ry = 300, 110
    h = 420
    parts = [
        ellipse_outline(cx, cy, rx, ry, width=34),
        line(cx - rx, cy, cx - rx, cy - h, width=34),
        line(cx + rx, cy, cx + rx, cy - h, width=34),
        arc(cx, cy - h, rx, 180, 360, width=34),
        rect_outline(280, 380, 720, 640, 26),
        circle(350, 570, 35),
        circle(440, 600, 40),
        circle(560, 580, 38),
        circle(650, 590, 34),
        circle(380, 460, 42),
        circle(490, 480, 46),
        circle(610, 450, 40),
        stroke([(310, 400), (330, 510), (390, 530), (430, 640)], width=22),
        stroke([(500, 380), (530, 440), (510, 540), (540, 640)], width=22),
        stroke([(690, 400), (660, 510), (620, 530), (670, 640)], width=22),
        arrow(420, 740, 420, 870, 28, 65, 36),
        arrow(580, 740, 580, 870, 28, 65, 36),
    ]
    return union_all(parts)


def gl_positions_spatial_coords():
    """Spatial Coordinate Positions (X, Y, Z): 3D georeferenced Cartesian coordinate system with located sample point and spatial projection drop lines."""
    ox, oy = 280, 280
    parts = [
        arrow(ox, oy, ox, 880, 34, 80, 44),
        arrow(ox, oy, 880, oy, 34, 80, 44),
        arrow(ox, oy, 740, 600, 34, 80, 44),
        line(210, 860, 250, 860, 24),
        line(250, 860, 210, 820, 24),
        line(210, 820, 250, 820, 24),
        dashed_line(620, 680, 620, 420, 22, 5),
        dashed_line(620, 420, 420, oy, 22, 5),
        dashed_line(620, 420, 500, 440, 22, 4),
        ellipse(620, 420, 40, 18),
        disk_ring(620, 680, 60, 24),
        circle(620, 680, 26),
        line(620, 745, 620, 775, 24),
        line(620, 615, 620, 585, 24),
        line(555, 680, 525, 680, 24),
        line(685, 680, 715, 680, 24),
    ]
    return union_all(parts)


def gc_volatiles_degassing():
    """Magmatic Volatiles & Degassing: Silicate melt fluid reservoir with ascending volatile exsolution bubbles nucleating and venting vapor plume."""
    parts = [
        sine_wave(140, 460, 860, 460, amp=20, cycles=3.0, width=32),
        line(160, 460, 160, 160, 32),
        line(840, 460, 840, 160, 32),
        line(145, 160, 855, 160, 32),
        disk_ring(320, 250, 40, 22),
        circle(320, 250, 16),
        disk_ring(480, 320, 55, 24),
        circle(480, 320, 22),
        disk_ring(680, 260, 45, 22),
        circle(680, 260, 18),
        disk_ring(390, 390, 35, 20),
        disk_ring(610, 380, 50, 22),
        line(320, 180, 320, 205, 20),
        line(480, 230, 480, 260, 20),
        line(680, 180, 680, 210, 20),
        stroke([(500, 480), (510, 620), (470, 740), (500, 880)], width=34),
        stroke([(380, 480), (340, 600), (370, 720), (320, 830)], width=28),
        stroke([(620, 480), (660, 600), (630, 720), (680, 830)], width=28),
        circle(430, 800, 24),
        circle(570, 780, 28),
        circle(500, 700, 22),
    ]
    return union_all(parts)


def gc_water_activity_ah2o():
    """Water Activity (aH2O): Thermodynamic water chemical activity with iconic water drop, H2O bent molecule, and activity waves."""
    pts = [(500, 880)]
    for deg in np.linspace(55, -125, 32):
        rad = math.radians(deg)
        pts.append((500 + 175 * math.cos(rad), 340 + 175 * math.sin(rad)))
    drop_poly = Polygon(pts).buffer(0)
    drop_outer = drop_poly.buffer(18)
    drop_inner = drop_poly.buffer(-18)
    drop_stroke = drop_outer.difference(drop_inner)

    ox = circle(500, 440, 48)
    h1 = circle(500 - 85, 440 - 75, 32)
    h2 = circle(500 + 85, 440 - 75, 32)
    b1 = line(500, 440, 500 - 85, 440 - 75, 24)
    b2 = line(500, 440, 500 + 85, 440 - 75, 24)

    a_bowl = disk_ring(480, 620, 40, 22)
    a_bar = line(520, 580, 520, 660, 22)

    rip1 = arc(500, 340, 225, 200, 340, 24)
    rip2 = arc(500, 340, 275, 210, 330, 24)

    return union_all([drop_stroke, ox, h1, h2, b1, b2, a_bowl, a_bar, rip1, rip2])


def gc_fluid_xco2_mole_fraction():
    """Fluid CO2 Mole Fraction (XCO2): Volatile mole fraction pie partition and linear O=C=O carbon dioxide molecular bonds."""
    cx, cy, r = 500, 500, 330
    parts = [
        disk_ring(cx, cy, r, 32),
        sector(cx, cy, r - 16, 30, 150),
        circle(cx, cy, 54),
        circle(cx - 240, cy, 46),
        circle(cx + 240, cy, 46),
        line(cx - 240, cy + 18, cx, cy + 18, 20),
        line(cx - 240, cy - 18, cx, cy - 18, 20),
        line(cx, cy + 18, cx + 240, cy + 18, 20),
        line(cx, cy - 18, cx + 240, cy - 18, 20),
        line(465, 830, 535, 750, 28),
        line(465, 750, 535, 830, 28),
    ]
    return union_all(parts)


def gc_oxygen_fugacity_fo2():
    """Oxygen Fugacity & Redox State (fO2): Redox equilibrium balance scale, O2 diatomic molecule, and logarithmic FMQ buffer curve."""
    parts = [
        poly([(450, 160), (550, 160), (520, 520), (480, 520)]),
        circle(500, 530, 28),
        line(220, 590, 780, 490, 30),
        line(250, 585, 250, 360, 20),
        arc(250, 360, 80, 180, 360, 26),
        circle(250, 360, 35),
        line(750, 495, 750, 270, 20),
        arc(750, 270, 80, 180, 360, 26),
        circle(750, 270, 35),
        circle(440, 740, 48),
        circle(560, 740, 48),
        line(440, 754, 560, 754, 20),
        line(440, 726, 560, 726, 20),
        arc(500, 740, 260, 20, 80, 24),
    ]
    return union_all(parts)


def gc_major_element_oxides():
    """Major Element Oxides (SiO2, Al2O3, etc.): 3D metal-oxygen coordination octahedron polyhedron with cation-oxygen bonds."""
    v_top = (500, 860)
    v_bot = (500, 140)
    v_left = (200, 470)
    v_right = (800, 530)
    v_front = (380, 320)
    v_back = (620, 680)

    parts = [
        line(*v_top, *v_left, 32),
        line(*v_top, *v_right, 32),
        line(*v_top, *v_front, 34),
        line(*v_top, *v_back, 24),
        line(*v_bot, *v_left, 32),
        line(*v_bot, *v_right, 32),
        line(*v_bot, *v_front, 34),
        line(*v_bot, *v_back, 24),
        line(*v_left, *v_front, 32),
        line(*v_front, *v_right, 32),
        line(*v_right, *v_back, 24),
        line(*v_back, *v_left, 24),
        line(500, 500, *v_top, 22),
        line(500, 500, *v_bot, 22),
        line(500, 500, *v_left, 22),
        line(500, 500, *v_right, 22),
        circle(500, 500, 42),
        circle(*v_top, 36),
        circle(*v_bot, 36),
        circle(*v_left, 34),
        circle(*v_right, 34),
        circle(*v_front, 38),
        circle(*v_back, 28),
    ]
    return union_all(parts)


def gc_gradient_initial_step():
    """Gradient Descent Initial Step Size (alpha_0): Loss valley descent trajectory showing initial step leap and line-search bracket."""
    curve_pts = []
    for i in range(41):
        t = i / 40.0
        x = 160 + 680 * t
        y = 220 + 620 * ((t - 0.75) ** 2) / 0.56
        curve_pts.append((x, y))

    parts = [
        stroke(curve_pts, 34),
        circle(262, 696, 32),
        arrow(262, 696, 534, 270, 36, 85, 46),
        circle(534, 270, 26),
        arrow(534, 270, 670, 220, 26, 60, 32),
        circle(670, 220, 22),
        dashed_line(262, 730, 262, 790, 20, 3),
        dashed_line(534, 310, 534, 790, 20, 5),
        line(262, 780, 534, 780, 26),
        disk_ring(398, 830, 34, 20),
    ]
    return union_all(parts)


def gc_sensitivity_jacobian():
    """Inversion Sensitivity Matrix (Jacobian J): Parameter derivative matrix grid mapping model space to data perturbations."""
    b_left = stroke([(220, 780), (160, 780), (160, 220), (220, 220)], width=32)
    b_right = stroke([(780, 780), (840, 780), (840, 220), (780, 220)], width=32)

    parts = [b_left, b_right]
    grid = [
        (300, 680, 55),
        (500, 680, 35),
        (700, 680, 20),
        (300, 500, 25),
        (500, 500, 60),
        (700, 500, 30),
        (300, 320, 18),
        (500, 320, 32),
        (700, 320, 52),
    ]
    for x, y, r in grid:
        parts.append(circle(x, y, r))

    return union_all(parts)


def gp_specific_gravity_balance():
    """Specific Gravity & Hydrostatic Balance (SG): Archimedes hydrostatic immersion apparatus with submerged rock core and buoyancy forces."""
    parts = [
        line(240, 820, 760, 820, 34),
        circle(500, 820, 30),
        line(500, 820, 500, 890, 32),
        line(340, 820, 340, 380, 18),
        rounded_rect(280, 260, 400, 380, 20),
        line(220, 520, 220, 180, 28),
        line(220, 180, 460, 180, 28),
        line(460, 180, 460, 520, 28),
        line(222, 450, 458, 450, 22),
        line(660, 820, 660, 520, 18),
        arc(660, 520, 70, 180, 360, 24),
        rect(625, 520, 695, 580),
        arrow(430, 260, 430, 380, 22, 55, 28),
    ]
    return union_all(parts)


def gc_log_error_residuals():
    """Logarithmic Residual Error (log10 Error): Semilogarithmic decay curve of inversion residuals across decade orders of magnitude."""
    parts = [
        arrow(160, 160, 160, 880, 34, 80, 44),
        arrow(130, 200, 880, 200, 34, 80, 44),
        line(140, 320, 190, 320, 26),
        line(140, 480, 190, 480, 26),
        line(140, 640, 190, 640, 26),
        line(140, 800, 190, 800, 26),
    ]
    pts = []
    for i in range(41):
        t = i / 40.0
        x = 180 + 660 * t
        y = 220 + 600 * math.exp(-3.5 * t)
        pts.append((x, y))
    parts.append(stroke(pts, 36))

    for idx in [0, 5, 12, 22, 38]:
        parts.append(circle(pts[idx][0], pts[idx][1], 24))

    parts.append(line(640, 720, 640, 840, 28))
    parts.append(disk_ring(700, 755, 35, 22))
    parts.append(disk_ring(780, 755, 35, 22))
    parts.append(line(815, 690, 815, 790, 22))
    parts.append(arc(780, 690, 35, 180, 360, 22))

    return union_all(parts)


def gl_geological_tagging_domain():
    """Geological Domain Tagging: Lithological classification tag badge with stratigraphic rock facies patterns."""
    tag_outline = stroke(
        [(260, 200), (740, 200), (740, 680), (640, 800), (360, 800), (260, 680), (260, 200)],
        width=34,
        closed=True,
    )
    eyelet = disk_ring(500, 720, 36, 20)
    lanyard = arc(500, 810, 75, 45, 135, 26)

    dots = [
        circle(340, 270, 16),
        circle(440, 290, 16),
        circle(540, 270, 16),
        circle(640, 290, 16),
        circle(390, 240, 16),
        circle(490, 240, 16),
        circle(590, 240, 16),
    ]
    div1 = line(280, 340, 720, 340, 24)
    div2 = line(280, 480, 720, 480, 24)
    bricks = [
        line(420, 340, 420, 410, 22),
        line(580, 340, 580, 410, 22),
        line(350, 410, 350, 480, 22),
        line(500, 410, 500, 480, 22),
        line(650, 410, 650, 480, 22),
        line(280, 410, 720, 410, 20),
    ]
    shales = [
        line(320, 540, 440, 540, 20),
        line(520, 540, 660, 540, 20),
        line(380, 600, 500, 600, 20),
        line(560, 600, 680, 600, 20),
    ]
    return union_all([tag_outline, eyelet, lanyard, *dots, div1, div2, *bricks, *shales])


# =============================================================================
# Icon Catalog Entries (22 Icons: U+E0AC..U+E0C1)
# =============================================================================

MINERALIS_INVERSION_ICONS: List[Dict[str, Any]] = [
    {
        "id": "gc_gibbs_free_energy",
        "name": "Gibbs Free Energy Minimisation",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0AC,
        "description": "Gibbs free energy curve and thermodynamic potential minimisation landscape governing chemical equilibrium and mineral phase stability.",
        "keywords": ["gibbs", "free energy", "delta g", "thermodynamics", "equilibrium", "potential", "phase stability"],
        "builder": gc_gibbs_free_energy,
    },
    {
        "id": "gc_chemical_elements",
        "name": "Chemical Elements & Atomic Structure",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE0AD,
        "description": "Fundamental chemical elements represented by Rutherford-Bohr electron orbitals around an atomic nucleus and periodic element grid.",
        "keywords": ["elements", "periodic table", "atom", "atomic number", "chemistry", "orbitals", "isotopes"],
        "builder": gc_chemical_elements,
    },
    {
        "id": "gl_minerals_specimen",
        "name": "Minerals & Crystal Aggregate",
        "domain": "Geological",
        "category": "Earth Model Types",
        "codepoint": 0xE0AE,
        "description": "Faceted idiomorphic mineral crystal cluster exhibiting diagnostic prism faces, terminations, and cleavage planes on rock matrix.",
        "keywords": ["minerals", "mineralogy", "crystal", "euhedral", "facets", "assemblage", "prismatic"],
        "builder": gl_minerals_specimen,
    },
    {
        "id": "gc_element_diff_wtpct",
        "name": "Element Difference in Weight Percent",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE0AF,
        "description": "Inversion objective metric quantifying residuals between measured and modeled elemental concentrations in weight percent (Delta-wt%).",
        "keywords": ["element difference", "weight percent", "wt pct", "wt%", "residual", "objective function", "assay"],
        "builder": gc_element_diff_wtpct,
    },
    {
        "id": "gc_temperature_thermo",
        "name": "Temperature & Geothermometry",
        "domain": "Geochemical",
        "category": "Methods",
        "codepoint": 0xE0B0,
        "description": "Temperature measurement and geothermometer scale with graduated thermometer column, thermal bulb, and thermal expansion gradient.",
        "keywords": ["temperature", "geothermometer", "celsius", "kelvin", "heat", "thermal", "geotherm"],
        "builder": gc_temperature_thermo,
    },
    {
        "id": "gc_pressure_gauge",
        "name": "Pressure & Geobarometry",
        "domain": "Geotechnical",
        "category": "Methods",
        "codepoint": 0xE0B1,
        "description": "Lithostatic and hydrostatic pressure indicator and Bourdon tube dial gauge measuring pressure in kilobars and gigapascals.",
        "keywords": ["pressure", "geobarometer", "gauge", "kbar", "gpa", "stress", "lithostatic"],
        "builder": gc_pressure_gauge,
    },
    {
        "id": "gc_gradient_perturbation_factor",
        "name": "Gradient Perturbation Factor",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE0B2,
        "description": "Numerical gradient descent perturbation step (delta) applied along the nabla vector for Jacobian finite-difference sensitivity.",
        "keywords": ["gradient perturbation", "nabla", "step size", "finite difference", "sensitivity", "derivative", "optimization"],
        "builder": gc_gradient_perturbation_factor,
    },
    {
        "id": "gc_l1_norm_regularization",
        "name": "L1 Norm Sparse Regularization",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE0B3,
        "description": "L1-norm diamond unit ball and Manhattan distance metric for robust outlier rejection and sparse mineral inversion.",
        "keywords": ["l1 norm", "manhattan distance", "sparsity", "regularization", "robust inversion", "lasso"],
        "builder": gc_l1_norm_regularization,
    },
    {
        "id": "gc_n_iterations_loop",
        "name": "Optimization Iteration Loop",
        "domain": "Geophysical",
        "category": "Processes",
        "codepoint": 0xE0B4,
        "description": "Algorithmic convergence loop cycle tracking iteration count (n) through successive gradient descent or NNLS refinement steps.",
        "keywords": ["iterations", "loop", "convergence", "algorithm", "cycle", "optimization", "refinement"],
        "builder": gc_n_iterations_loop,
    },
    {
        "id": "gc_thermodynamics_system",
        "name": "Thermodynamic Equilibrium & Heat System",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0B5,
        "description": "Closed thermodynamic system illustrating heat flow (Q), work boundary displacement (W), and thermodynamic phase equilibrium.",
        "keywords": ["thermodynamics", "heat cycle", "entropy", "enthalpy", "energy", "state function", "carnot"],
        "builder": gc_thermodynamics_system,
    },
    {
        "id": "gp_petrophysics_core_matrix",
        "name": "Petrophysics & Core Plug Porosity",
        "domain": "Geophysical",
        "category": "Earth Model Types",
        "codepoint": 0xE0B6,
        "description": "Cylindrical drill core rock specimen detailing solid mineral matrix, interconnected pore throats, and fluid permeability channels.",
        "keywords": ["petrophysics", "rock physics", "porosity", "permeability", "core plug", "pore fluid", "formation"],
        "builder": gp_petrophysics_core_matrix,
    },
    {
        "id": "gl_positions_spatial_coords",
        "name": "Spatial Coordinate Positions",
        "domain": "Geological",
        "category": "Methods",
        "codepoint": 0xE0B7,
        "description": "3D georeferenced spatial coordinate reference frame with Cartesian X, Y, Z axes and located borehole collar / sample survey point.",
        "keywords": ["positions", "coordinates", "spatial", "xyz", "northing", "easting", "elevation", "survey"],
        "builder": gl_positions_spatial_coords,
    },
    {
        "id": "gc_volatiles_degassing",
        "name": "Magmatic Volatiles & Degassing Bubbles",
        "domain": "Geochemical",
        "category": "Processes",
        "codepoint": 0xE0B8,
        "description": "Volatile exsolution showing ascending supercritical fluid bubbles (H2O, CO2, SO2) nucleating and degassing through silicate melt.",
        "keywords": ["volatiles", "degassing", "bubbles", "exsolution", "magma", "vapor phase", "fluid"],
        "builder": gc_volatiles_degassing,
    },
    {
        "id": "gc_water_activity_ah2o",
        "name": "Water Activity (aH2O)",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE0B9,
        "description": "Chemical activity of water (aH2O) in hydrothermal fluids and hydrous mineral hydration and dehydration reactions.",
        "keywords": ["ah2o", "water activity", "chemical activity", "hydration", "fluid", "h2o", "fugacity"],
        "builder": gc_water_activity_ah2o,
    },
    {
        "id": "gc_fluid_xco2_mole_fraction",
        "name": "Fluid Carbon Dioxide Mole Fraction (XCO2)",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE0BA,
        "description": "Mole fraction of carbon dioxide (XCO2) in binary H2O-CO2 hydrothermal and metamorphic fluid systems.",
        "keywords": ["xco2", "mole fraction", "carbon dioxide", "co2", "fluid composition", "decarbonation"],
        "builder": gc_fluid_xco2_mole_fraction,
    },
    {
        "id": "gc_oxygen_fugacity_fo2",
        "name": "Oxygen Fugacity & Redox State (fO2)",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE0BB,
        "description": "Oxygen fugacity (fO2) and oxidation state relative to mineral redox buffers (FMQ, NNO, HM) controlling multi-valent cations.",
        "keywords": ["fo2", "oxygen fugacity", "redox", "oxidation state", "fmq buffer", "iron redox", "buffer"],
        "builder": gc_oxygen_fugacity_fo2,
    },
    {
        "id": "gc_major_element_oxides",
        "name": "Major Element Silicate Oxides",
        "domain": "Geochemical",
        "category": "Earth Model Types",
        "codepoint": 0xE0BC,
        "description": "Major rock-forming oxide polyhedron (cation-oxygen coordination cluster) and whole-rock silicate oxide chemical components.",
        "keywords": ["oxides", "major oxides", "silicate", "sio2", "al2o3", "cation-oxygen", "geochemistry", "coordination"],
        "builder": gc_major_element_oxides,
    },
    {
        "id": "gc_gradient_initial_step",
        "name": "Gradient Descent Initial Step Size",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE0BD,
        "description": "Learning rate and initial step size parameter scaling line-search progress along the objective descent trajectory.",
        "keywords": ["step size", "initial step", "learning rate", "gradient descent", "optimization", "line search"],
        "builder": gc_gradient_initial_step,
    },
    {
        "id": "gc_sensitivity_jacobian",
        "name": "Inversion Sensitivity Matrix",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE0BE,
        "description": "Sensitivity matrix (Jacobian J) mapping perturbations in mineral abundances to assay response changes.",
        "keywords": ["sensitivity", "jacobian", "partial derivatives", "covariance", "resolution matrix"],
        "builder": gc_sensitivity_jacobian,
    },
    {
        "id": "gp_specific_gravity_balance",
        "name": "Specific Gravity & Hydrostatic Balance",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE0BF,
        "description": "Petrophysical specific gravity and grain density measurement using analytical Archimedes hydrostatic immersion balance.",
        "keywords": ["specific gravity", "density", "archimedes", "pycnometer", "petrophysics", "gravity balance"],
        "builder": gp_specific_gravity_balance,
    },
    {
        "id": "gc_log_error_residuals",
        "name": "Logarithmic Residual Error",
        "domain": "Geophysical",
        "category": "Methods",
        "codepoint": 0xE0C0,
        "description": "Log-scale error metric and log-normal residual distribution for wide dynamic range trace element inversion.",
        "keywords": ["log error", "logarithmic", "residuals", "trace elements", "misfit", "objective function"],
        "builder": gc_log_error_residuals,
    },
    {
        "id": "gl_geological_tagging_domain",
        "name": "Geological Domain Tagging",
        "domain": "Geological",
        "category": "Methods",
        "codepoint": 0xE0C1,
        "description": "Geological lithological tagging flag and lithofacies boundary constraint guiding Bayesian mineralogical inversion.",
        "keywords": ["geological tagging", "lithology tag", "stratigraphic domain", "categorical constraint", "facies"],
        "builder": gl_geological_tagging_domain,
    },
]
