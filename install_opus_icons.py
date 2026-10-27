"""Install the reviewed font, matching vector/PNG assets and preview sheets in Opus."""
import argparse
import json
import shutil
from pathlib import Path


def install(distribution, repository):
    distribution, repository = Path(distribution).resolve(), Path(repository).resolve()
    base = repository/'opus.base'
    if not (base/'src/opus/base/icons').is_dir() or not (repository/'opus.geo.em').is_dir():
        raise ValueError('Destination must be an existing Opus repository')
    catalog = json.loads((distribution/'geoscience-icons.json').read_text(encoding='utf-8'))
    if catalog['totalIcons'] != 323:
        raise ValueError('Expected the complete 323-icon distribution')
    shutil.copy2(distribution/'GeoScienceIcons.java', base/'src/opus/base/icons/GeoScienceIcons.java')
    for directory in (base/'src/opus/base/icons', base/'resources/fonts'):
        shutil.copy2(distribution/'GeoScienceIcons.ttf', directory/'GeoScienceIcons.ttf')
    for family, first, last in (('mt', 0xE112, 0xE125), ('geochemistry', 0xE126, 0xE143)):
        records = [icon for icon in catalog['icons'] if first <= icon['codepoint_int'] <= last
                   or (family == 'mt' and icon['id'] == 'gp_magnetotellurics_mt')]
        target = base/'resources/icons'/family
        target.mkdir(parents=True, exist_ok=True)
        for record in records:
            for suffix in ('', '-dark'):
                filename = record['id']+suffix+'.png'
                shutil.copy2(distribution/('png-'+family)/filename, target/filename)
            for field, folder in (('svg_file', 'svg'), ('svg_mono_file', 'svg-mono')):
                (target/folder).mkdir(exist_ok=True)
                shutil.copy2(distribution/record[field], target/folder/(record['id']+'.svg'))
        (target/'manifest.json').write_text(json.dumps(records, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    em_images = repository/'opus.geo.em/docs/images'
    chemistry_images = repository/'opus.geo.geochemistry/docs/images'
    em_images.mkdir(parents=True, exist_ok=True)
    chemistry_images.mkdir(parents=True, exist_ok=True)
    for source, target in (('mt_processing_preview.png', em_images/'mt-icons.png'),
                           ('mt_small_sizes.png', em_images/'mt-icons-small.png'),
                           ('mt_symbol.png', em_images/'mt-symbol.png'),
                           ('geochemistry_preview.png', chemistry_images/'geochemistry-icons.png'),
                           ('geochemistry_small_sizes.png', chemistry_images/'geochemistry-icons-small.png')):
        shutil.copy2(distribution/source, target)
    print('Installed font, 51 colour/vector compositions, 102 theme PNGs and preview sheets in Opus')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--distribution', type=Path, required=True)
    parser.add_argument('--opus', type=Path, required=True)
    args = parser.parse_args()
    install(args.distribution, args.opus)
