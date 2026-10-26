"""Offline catalog and supersampled artwork previews for both icon styles."""

import io
import math
from html import escape

from PIL import Image, ImageDraw, ImageFont

from icon_artwork import artwork, PALETTES, INK


def save_png(image, path):
    """Replace previews atomically, including when a viewer holds the old file."""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    temporary = path.with_suffix(".tmp.png")
    temporary.write_bytes(buffer.getvalue())
    temporary.replace(path)


def font(size, bold=False):
    candidates = ["C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
                  "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def render_icon(icon, size):
    scale = size * 3 / 24
    result = Image.new("RGBA", (size * 3, size * 3))
    for layer in artwork(icon):
        mask = Image.new("L", result.size)
        draw = ImageDraw.Draw(mask)
        geometry = layer.surface
        polygons = [geometry] if geometry.geom_type == "Polygon" else list(geometry.geoms)
        for polygon in polygons:
            if polygon.geom_type != "Polygon":
                continue
            draw.polygon([(x * scale, y * scale) for x, y in polygon.exterior.coords], fill=255)
            for interior in polygon.interiors:
                draw.polygon([(x * scale, y * scale) for x, y in interior.coords], fill=0)
        result.paste(layer.color, (0, 0), mask)
    return result.resize((size, size), Image.Resampling.LANCZOS)


def render_flat_sheet(path, icons):
    columns, cell_w, cell_h = 12, 176, 150
    result = Image.new("RGB", (columns * cell_w + 64, math.ceil(len(icons) / columns) * cell_h + 150), "#F3F5F8")
    draw = ImageDraw.Draw(result)
    draw.text((40, 25), "GEOSCIENCE / FLAT ICON COLLECTION", fill=INK, font=font(26, True))
    draw.text((40, 68), "193 detailed compositions  /  Natural material colours  /  Matching detailed TTF", fill="#66758C", font=font(17))
    for i, icon in enumerate(icons):
        x, y = 32 + i % columns * cell_w, 120 + i // columns * cell_h
        draw.rounded_rectangle((x + 4, y + 4, x + cell_w - 4, y + cell_h - 4), 12, fill="white")
        tile = render_icon(icon, 76)
        result.paste(tile, (x + (cell_w - 76) // 2, y + 16), tile)
        name = icon["name"]
        while draw.textlength(name, font=font(11)) > cell_w - 20:
            name = name[:-2].rstrip(".") + "."
        draw.text((x + 10, y + 104), name, fill=INK, font=font(11))
        draw.text((x + 10, y + 124), f'U+{icon["codepoint"]:04X}', fill=PALETTES[icon["domain"]][0], font=font(10))
    save_png(result, path)


def render_style_preview(path, icons, ttf_path):
    featured = ["gp_magnetic_survey", "gp_gravity_survey", "gp_ground_penetrating_radar", "gp_geodesy_insar_gnss", "gl_minerals_specimen", "gl_rock_type_igneous", "gl_faulted_stratigraphy", "gl_banded_iron_formation", "gc_pxrf_analyzer", "gc_aqua_regia_partial_digest", "gc_temperature_thermo", "gc_chemical_elements", "gt_cpt_cone", "gt_triaxial_shear", "gt_soil_profile_log", "gl_geological_tagging_domain"]
    by_id = {icon["id"]: icon for icon in icons}
    result = Image.new("RGB", (1440, 1010), "#F3F5F8")
    draw = ImageDraw.Draw(result)
    draw.text((52, 28), "GEOSCIENCE", fill=INK, font=font(16, True))
    draw.text((52, 58), "Scientific detail. Natural colour.", fill=INK, font=font(42, True))
    draw.text((52, 120), "The detailed TTF compositions, now in flat material colours. All 193 mappings preserved.", fill="#65748A", font=font(19))
    for i, icon_id in enumerate(featured):
        icon = by_id[icon_id]
        x, y = 48 + i % 8 * 169, 174 + i // 8 * 208
        draw.rounded_rectangle((x, y, x + 156, y + 192), 14, fill="white")
        tile = render_icon(icon, 100)
        result.paste(tile, (x + 28, y + 18), tile)
        words, lines, line = icon["name"].split(), [], ""
        for word in words:
            if draw.textlength((line + " " + word).strip(), font=font(12)) > 136 and line:
                lines.append(line)
                line = word
            else:
                line = (line + " " + word).strip()
        lines.append(line)
        for j, line in enumerate(lines[:3]):
            draw.text((x + 10, y + 128 + j * 17), line, fill=INK, font=font(12))
    draw.rounded_rectangle((48, 610, 1392, 960), 18, fill="#182438")
    draw.text((76, 632), "DETAILED TECHNICAL TTF", fill="#F5F7FC", font=font(19, True))
    draw.text((76, 664), "Field lines, instrument components and geological structure. Rendered from the compiled font.", fill="#AAB8CB", font=font(15))
    glyph_font = ImageFont.truetype(str(ttf_path), 66)
    for i, icon_id in enumerate(featured):
        x, y = 84 + i % 8 * 164, 707 + i // 8 * 112
        draw.text((x, y), chr(by_id[icon_id]["codepoint"]), font=glyph_font, fill="#EEF4FF")
        draw.text((x, y + 77), f'U+{by_id[icon_id]["codepoint"]:04X}', font=font(11), fill="#AAB8CB")
    save_png(result, path)


def render_material_preview(path, icons):
    selected = ["gp_seismic_reflection", "gp_electromagnetic_em", "gl_minerals_specimen",
                "gc_fluid_inclusion_microtherm", "gc_aqua_regia_partial_digest", "gt_soil_profile_log",
                "gl_banded_iron_formation", "gl_rock_type_igneous", "gl_propylitic_chlorite_epidote",
                "gc_water_activity_ah2o", "gc_temperature_thermo", "gc_biogeochem_vegetation"]
    by_id = {icon['id']: icon for icon in icons}
    result = Image.new('RGB', (1440, 970), '#F3F5F8')
    draw = ImageDraw.Draw(result)
    draw.text((45, 28), 'EARTHSCIENCE ICONS / DETAILED COLOUR', font=font(17, True), fill='#28705D')
    draw.text((45, 64), 'Scientific detail. Natural colour.', font=font(40, True), fill=INK)
    draw.text((45, 126), 'Detailed compositions with rock, soil, glass, metal, water and vegetation colours.', font=font(19), fill='#65748A')
    for index, identifier in enumerate(selected):
        icon = by_id[identifier]
        x, y = 40 + index % 4 * 342, 180 + index // 4 * 250
        draw.rounded_rectangle((x, y, x + 326, y + 232), 15, fill='white')
        tile = render_icon(icon, 140)
        result.paste(tile, (x + 93, y + 17), tile)
        lines, current = [], ''
        for word in icon['name'].split():
            trial = (current + ' ' + word).strip()
            if draw.textlength(trial, font=font(15)) > 294 and current:
                lines.append(current)
                current = word
            else:
                current = trial
        lines.append(current)
        for row, text in enumerate(lines[:2]):
            draw.text((x + 16, y + 174 + row * 21), text, font=font(15), fill=INK)
    save_png(result, path)


def build_catalog(path, catalog):
    cards = []
    for item in catalog:
        search = escape(" ".join([item["id"], item["name"], *item["keywords"]]).lower(), quote=True)
        cards.append(f'''<article class="card" data-domain="{item['domain']}" data-category="{item['category']}" data-search="{search}">
<div class="sample"><img src="{item['svg_file']}" alt="{escape(item['name'], quote=True)}" loading="lazy"><span class="glyph" aria-hidden="true">{chr(item['codepoint_int'])}</span></div>
<div class="info"><span class="domain">{item['domain']}</span><h2>{escape(item['name'])}</h2><p>{escape(item['description'])}</p><footer><code>{item['codepoint_hex']}</code><a href="{item['svg_file']}" download>Flat SVG</a><a href="{item['svg_mono_file']}" download>Detailed SVG</a></footer></div></article>''')
    template = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GeoScience — Icon Library</title><link rel="stylesheet" href="geoscience-icons.css">
<style>
:root{--bg:#f3f5f8;--card:#fff;--ink:#26354d;--muted:#69788d;--border:#dfe5ed;--accent:#3478f6}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 'Segoe UI',sans-serif}body.dark{--bg:#111d2f;--card:#1b2a40;--ink:#eef4ff;--muted:#aab8cb;--border:#34435a}header,main{max-width:1440px;margin:auto;padding:36px}header{padding-bottom:20px}.eyebrow{letter-spacing:.18em;font-size:12px;font-weight:700;color:var(--accent)}h1{font-size:48px;letter-spacing:-.04em;margin:12px 0}header p{color:var(--muted);font-size:17px;max-width:760px}.top{display:flex;align-items:center;justify-content:space-between}.tools{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:28px}button,select,input{font:inherit;color:var(--ink);border:1px solid var(--border);background:var(--card);border-radius:9px;padding:10px 14px}button{cursor:pointer}button[aria-pressed=true]{background:var(--ink);color:var(--bg)}input{flex:1;min-width:200px}input:focus-visible,button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:3px}.downloads{display:flex;gap:14px;flex-wrap:wrap}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}.status{margin:18px 0 0;color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(252px,1fr));gap:18px;padding-top:10px}.card{background:var(--card);border:1px solid var(--border);border-radius:15px;overflow:hidden;display:flex;flex-direction:column}.card[hidden]{display:none}.sample{height:154px;display:flex;align-items:center;justify-content:center;background:color-mix(in srgb,var(--bg) 45%,var(--card))}.sample img{width:var(--size,72px);height:var(--size,72px)}.glyph{display:none;font-family:'GeoScience Icons';font-size:var(--size,72px);line-height:1}.line .sample img{display:none}.line .glyph{display:block}.info{padding:18px;display:flex;flex-direction:column;flex:1}.domain{font-size:10px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}h2{font-size:15px;line-height:1.35;margin:8px 0}article p{font-size:12px;color:var(--muted);margin:0 0 18px}footer{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:auto;font-size:11px}code{color:var(--muted)}label{color:var(--muted);display:flex;align-items:center;gap:8px}input[type=range]{width:90px;min-width:0;padding:0}#empty{text-align:center;color:var(--muted);padding:70px 20px}@media(max-width:700px){header,main{padding:22px}h1{font-size:36px}.top{align-items:flex-start;gap:20px}.tools{gap:8px}.grid{grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}}
</style></head><body><header><div class="top"><span class="eyebrow">GEOSCIENCE / ICON LIBRARY</span><button id="theme" aria-pressed="false">Dark theme</button></div><h1>Clear at a glance.</h1><p>193 detailed geoscience compositions in natural material colours, with matching technical linework for your icon font.</p><nav class="downloads" aria-label="Downloads"><a href="GeoScienceIcons.ttf" download>Download TTF ↗</a><a href="GeoScienceIcons.woff" download>Download WOFF ↗</a><a href="geoscience-icons.json" download>Icon manifest ↗</a></nav><div class="tools"><input id="search" type="search" placeholder="Search icons, methods, models…" aria-label="Search icons"><select id="domain" aria-label="Discipline"><option value="all">All disciplines</option><option>Geophysical</option><option>Geotechnical</option><option>Geological</option><option>Geochemical</option></select><select id="category" aria-label="Category"><option value="all">All categories</option><option>Methods</option><option>Earth Model Types</option><option>Processes</option></select><button id="flat" aria-pressed="true">Flat SVG</button><button id="line" aria-pressed="false">Detailed font</button><label>Size <input id="size" aria-label="Icon size" type="range" min="16" max="112" value="72" step="4"><output id="sizeValue">72px</output></label></div><p class="status" id="status" role="status">193 icons</p></header><main class="grid">CARDS</main><p id="empty" hidden>No icons match. Try another search or discipline.</p><script>
const cards=[...document.querySelectorAll('.card')];const byId=id=>document.getElementById(id);
function filter(){const q=byId('search').value.trim().toLowerCase(),d=byId('domain').value,c=byId('category').value;let count=0;for(const card of cards){const show=(!q||card.dataset.search.includes(q))&&(d==='all'||card.dataset.domain===d)&&(c==='all'||card.dataset.category===c);card.hidden=!show;if(show)count++;}byId('status').textContent=count+' of 193 icons';byId('empty').hidden=count!==0;}
byId('search').addEventListener('input',filter);['domain','category'].forEach(id=>byId(id).addEventListener('change',filter));
for(const mode of ['flat','line'])byId(mode).addEventListener('click',()=>{document.body.classList.toggle('line',mode==='line');byId('flat').setAttribute('aria-pressed',mode==='flat');byId('line').setAttribute('aria-pressed',mode==='line');});
byId('size').addEventListener('input',event=>{document.documentElement.style.setProperty('--size',event.target.value+'px');byId('sizeValue').value=event.target.value+'px';});
byId('theme').addEventListener('click',()=>{const dark=document.body.classList.toggle('dark');byId('theme').setAttribute('aria-pressed',dark);byId('theme').textContent=dark?'Light theme':'Dark theme';});
</script></body></html>'''
    path.write_text(template.replace("CARDS", "\n".join(cards)), encoding="utf-8")
