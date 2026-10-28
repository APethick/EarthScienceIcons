"""Geological icons from the Field Geologists' Manual (AusIMM Monograph 9, 4th ed.).

Reference: Berkman, D. A. (ed.) Field Geologists' Manual, 4th edition,
Australasian Institute of Mining and Metallurgy (AusIMM).

All 148 icons are under the Geological domain ('gl_' prefix), text-free, and
generate both detailed monochrome font outlines and natural-colour flat SVGs
from the same 48-unit engineering drawings.
"""
from functools import lru_cache

from fgm_common import flat_layers
from fgm_patterns_igneous import ROWS as IGNEOUS_PATTERN_ROWS
from fgm_patterns_sedimentary import ROWS as SEDIMENTARY_PATTERN_ROWS
from fgm_structure import ROWS as STRUCTURE_ROWS
from fgm_mass_movement import ROWS as MASS_MOVEMENT_ROWS
from fgm_petrology import ROWS as PETROLOGY_ROWS

MANUAL_CITATION = "Berkman (ed.), Field Geologists' Manual, 4th ed., AusIMM Monograph 9"

_METHODS_IDS = {
    'gl_dip_isogon_construction',
    'gl_fold_attitude_grid',
    'gl_fold_attitude_classification',
    'gl_orthographic_net',
    'gl_wulff_net',
    'gl_schmidt_net',
    'gl_stereonet_contouring_device',
} | {f'gl_grain_percent_{pct:02d}' for pct in (1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50)}

_PROCESS_IDS = {row[0] for row in MASS_MOVEMENT_ROWS} | {'gl_earthquake_magnitude_energy', 'gl_fold_vergence'}


def _category_for(identifier):
    if identifier in _METHODS_IDS:
        return 'Methods'
    if identifier in _PROCESS_IDS:
        return 'Processes'
    return 'Earth Model Types'


FGM_ROWS = (
    list(IGNEOUS_PATTERN_ROWS)
    + list(SEDIMENTARY_PATTERN_ROWS)
    + list(STRUCTURE_ROWS)
    + list(MASS_MOVEMENT_ROWS)
    + list(PETROLOGY_ROWS)
)

FGM_ICONS = []
for index, (identifier, name, description, fgm_reference, builder) in enumerate(FGM_ROWS):
    base_desc = description.rstrip('.')
    full_description = f"{base_desc} ({fgm_reference}, Field Geologists' Manual)."
    ref_tokens = [
        tok.lower().strip('(),.-:;[]')
        for tok in fgm_reference.replace('/', ' ').split()
        if len(tok.strip('(),.-:;[]')) > 1
    ]
    keywords = list(dict.fromkeys(
        identifier.split('_')[1:]
        + ref_tokens
        + ['geology', 'field', 'geologists', 'manual', 'fgm', 'berkman', 'ausimm']
    ))
    FGM_ICONS.append(
        dict(
            id=identifier,
            codepoint=0xE144 + index,
            name=name,
            domain='Geological',
            category=_category_for(identifier),
            description=full_description,
            reference=f"{fgm_reference} — {MANUAL_CITATION}",
            keywords=keywords,
            builder=lambda builder=builder: builder().geometry(),
        )
    )

FGM_IDS = {icon['id'] for icon in FGM_ICONS}
FGM_BUILDERS = {row[0]: row[4] for row in FGM_ROWS}
FGM_ALIASES = {
    row[0][3:]: row[0]
    for row in FGM_ROWS
    if row[0].startswith('gl_')
}


@lru_cache(maxsize=256)
def flat_artwork(identifier):
    return flat_layers(FGM_BUILDERS[identifier]())
