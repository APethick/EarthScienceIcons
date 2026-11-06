"""Export the approved, theme-aware PNG resources used by MineralSystemsQC."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw
from icons_mineral_systems import ROWS
from mineral_systems_artwork import colour_layers


def polygons(geometry):
    if geometry.geom_type == 'Polygon':
        yield geometry
    elif hasattr(geometry, 'geoms'):
        for part in geometry.geoms:
            yield from polygons(part)


def export_resources(destination):
    directory = Path(destination)
    directory.mkdir(parents=True, exist_ok=True)
    scale = 256*4/48
    for row in ROWS:
        for dark in (False, True):
            image = Image.new('RGBA', (1024, 1024))
            for geometry, colour in colour_layers(row['id'], dark):
                mask = Image.new('L', image.size)
                pen = ImageDraw.Draw(mask)
                for polygon in polygons(geometry):
                    pen.polygon([(x*scale, y*scale) for x, y in polygon.exterior.coords], fill=255)
                    for ring in polygon.interiors:
                        pen.polygon([(x*scale, y*scale) for x, y in ring.coords], fill=0)
                image.paste(colour, (0, 0), mask)
            image = image.resize((256, 256), Image.Resampling.LANCZOS)
            name = row['id'] + ('-dark' if dark else '') + '.png'
            image.save(directory/name)
    manifest = [dict(taxonomy_id=row['id'], icon_id='gc_ms_'+row['id'],
                     light=row['id']+'.png', dark=row['id']+'-dark.png') for row in ROWS]
    (directory/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(f'Exported {len(ROWS)*2} MineralSystemsQC theme resources to {directory}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    export_resources(arguments.output)
