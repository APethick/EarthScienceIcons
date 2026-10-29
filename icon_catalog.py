"""Ordered, append-only icon registry shared by all distribution builders."""
from icons_geophysical import GEOPHYSICAL_ICONS
from icons_geotechnical import GEOTECHNICAL_ICONS
from icons_geological import GEOLOGICAL_ICONS
from icons_geochemical import GEOCHEMICAL_ICONS
from icons_opus_geology import OPUS_GEOLOGY_ICONS
from icons_geochemical_expanded import EXPANDED_GEOCHEMISTRY_ICONS
from icons_mineralis_inversion import MINERALIS_INVERSION_ICONS
from icons_geophysics_expanded import EXPANDED_GEOPHYSICS_ICONS
from icons_mt import MT_ICONS, mt_survey
from icons_alteration import GEOCHEM_ICONS
from icons_field_manual import FGM_ICONS

ALL_ICONS = (GEOPHYSICAL_ICONS + GEOTECHNICAL_ICONS + GEOLOGICAL_ICONS +
             GEOCHEMICAL_ICONS + OPUS_GEOLOGY_ICONS +
             EXPANDED_GEOCHEMISTRY_ICONS + MINERALIS_INVERSION_ICONS +
             EXPANDED_GEOPHYSICS_ICONS + MT_ICONS + GEOCHEM_ICONS + FGM_ICONS)

# User-approved MT acquisition layout replacement; stable ID and codepoint.
ALL_ICONS = [dict(icon, builder=lambda: mt_survey().geometry(),
                  description="Crossed electric dipoles, four electrodes, three orthogonal magnetic sensors and a central acquisition unit.")
             if icon["id"] == "gp_magnetotellurics_mt" else icon for icon in ALL_ICONS]

from icons_spectroscopy import SPECTROSCOPY_ICONS
ALL_ICONS += SPECTROSCOPY_ICONS

from icons_field_instruments import ICONS as FIELD_INSTRUMENT_ICONS
ALL_ICONS += FIELD_INSTRUMENT_ICONS

from icons_seismic_equipment import ICONS as SEISMIC_EQUIPMENT_ICONS
ALL_ICONS += SEISMIC_EQUIPMENT_ICONS
