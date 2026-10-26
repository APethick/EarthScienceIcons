"""Refresh the self-contained GitHub Pages assets from the compiled icon set."""
from pathlib import Path
import shutil
import zipfile
import json
import re


def build_site():
    root = Path(__file__).resolve().parent
    dist = root / 'dist'
    assets = root / 'docs' / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    catalog = json.loads((dist / 'geoscience-icons.json').read_text(encoding='utf-8'))
    total, version = catalog['totalIcons'], catalog['version']
    page = root / 'docs' / 'index.html'
    markup = page.read_text(encoding='utf-8')
    markup = re.sub(r'(<span data-total>)\d+(</span>)', lambda match: match[1] + str(total) + match[2], markup)
    markup = re.sub(r'content="Explore \d+ detailed Earth', f'content="Explore {total} detailed Earth', markup)
    markup = re.sub(r'([?&]v=)[0-9.]+', lambda match: match[1] + version, markup)
    page.write_text(markup, encoding='utf-8')
    script = root / 'docs' / 'app.js'
    javascript = script.read_text(encoding='utf-8')
    javascript = re.sub(r"const RELEASE = '[^']+';", f"const RELEASE = '{version}';", javascript)
    script.write_text(javascript, encoding='utf-8')
    for name in ('svg', 'svg-mono'):
        shutil.copytree(dist / name, assets / name, dirs_exist_ok=True)
    for name in ('GeoScienceIcons.ttf', 'GeoScienceIcons.woff', 'geoscience-icons.css', 'geoscience-icons.json'):
        shutil.copy2(dist / name, assets / name)
    with zipfile.ZipFile(assets / 'EarthScienceIcons.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(dist.rglob('*')):
            if path.is_file():
                archive.write(path, path.relative_to(dist))
        archive.write(root / 'LICENSE', 'LICENSE')
    (root / 'docs' / '.nojekyll').touch()
    print('GitHub Pages assets ready in docs/. Preview with: python -m http.server 8080 --directory docs')


if __name__ == '__main__':
    build_site()
