"""Refresh the self-contained GitHub Pages assets from the compiled icon set."""
from pathlib import Path
import shutil
import zipfile


def build_site():
    root = Path(__file__).resolve().parent
    dist = root / 'dist'
    assets = root / 'docs' / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
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
