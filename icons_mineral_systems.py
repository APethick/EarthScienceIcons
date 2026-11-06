"""Append-only icons for the nine MineralSystemsQC realms and 27 clans."""
import json
from functools import partial
from pathlib import Path

from mineral_systems_artwork import drawing

ROWS = json.loads(Path(__file__).with_name('mineral-system-types.json').read_text(encoding='utf-8'))


def geometry(taxonomy_id):
    return drawing(taxonomy_id).geometry().buffer(0)


ICONS = [dict(id='gc_ms_'+row['id'], codepoint=0xE21F+index,
              name=row['name'], domain='Geological', category='Mineral Systems',
              description=row['description'],
              keywords=['mineral', 'system', 'deposit', 'Opus', row['level'], row['id'],
                        *(row['parent'] or '').split('_'), *row['name'].lower().split()],
              group='Mineral systems '+row['level']+'s', taxonomy_id=row['id'],
              builder=partial(geometry, row['id']))
         for index, row in enumerate(ROWS)]
IDS = {icon['id'] for icon in ICONS}
ALIASES = {row['id']: 'gc_ms_'+row['id'] for row in ROWS}


def flat_artwork(icon):
    from icons_geophysics_expanded import flat_artwork as render
    return render(icon, drawing(icon['taxonomy_id']))
