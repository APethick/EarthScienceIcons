"""Preview actual compiled glyphs beside full-colour drawings; export JavaFX PNGs."""
from PIL import Image, ImageDraw, ImageFont
from icon_specimen import render_icon, font, save_png
from icons_mt import MT_IDS


def render_dark(icon, size):
    """Lift technical ink for dark surfaces; preserve material and E/H colours."""
    from icons_mt import flat_artwork as mt_artwork
    from icons_alteration import GEOCHEM_IDS, flat_artwork as geochem_artwork
    flat_artwork = geochem_artwork if icon['id'] in GEOCHEM_IDS else mt_artwork
    colours = {'#303A40': '#DEE6EA', '#BEC8CC': '#778A93', '#B0B7B7': '#9BA9AF'}
    result = Image.new('RGBA', (size*3, size*3))
    scale = size*3/24
    for layer in flat_artwork(icon['id']):
        mask = Image.new('L', result.size)
        draw = ImageDraw.Draw(mask)
        geometry = layer.surface
        polygons = [geometry] if geometry.geom_type == 'Polygon' else list(geometry.geoms)
        for polygon in polygons:
            if polygon.geom_type != 'Polygon': continue
            draw.polygon([(x*scale, y*scale) for x, y in polygon.exterior.coords], fill=255)
            for interior in polygon.interiors:
                draw.polygon([(x*scale, y*scale) for x, y in interior.coords], fill=0)
        result.paste(colours.get(layer.color, layer.color), (0, 0), mask)
    return result.resize((size, size), Image.Resampling.LANCZOS)


def render_mt_suite(dist, icons, ttf):
    suite = [icon for icon in icons if icon['id'] in MT_IDS]
    mt_symbol = next(icon for icon in suite if icon['id'] == 'gp_magnetotellurics_mt')
    save_png(render_icon(mt_symbol, 512), dist/'mt_symbol.png')
    render_suite(dist, suite, ttf, 'mt', 'mt_processing_preview', 'MT FIELDS + PROCESSING')


def render_geochemistry_suite(dist, icons, ttf):
    from icons_alteration import GEOCHEM_IDS
    suite = [icon for icon in icons if icon['id'] in GEOCHEM_IDS]
    render_suite(dist, suite, ttf, 'geochemistry', 'geochemistry_preview', 'GEOCHEMISTRY + ALTERATION')


def render_suite(dist, suite, ttf, prefix, preview, heading):
    png = dist/('png-'+prefix)
    png.mkdir(exist_ok=True)
    cols, width, height, header = 4, 420, 260, 110
    sheet = Image.new('RGB', (cols*width+48, ((len(suite)+cols-1)//cols)*height+header+20), '#F2F4F5')
    draw = ImageDraw.Draw(sheet)
    draw.text((30, 20), heading, font=font(30, True), fill='#263238')
    draw.text((30, 66), 'Natural colour artwork  /  actual TTF outlines  /  no lettering inside icons', font=font(18), fill='#617279')
    glyph_font = ImageFont.truetype(str(ttf), 128)
    for index, icon in enumerate(suite):
        x, y = 24+index%cols*width, header+index//cols*height
        draw.rounded_rectangle((x+5, y+4, x+width-8, y+height-9), radius=10, fill='white', outline='#D5DDE0')
        draw.text((x+18, y+16), icon['name'], font=font(19, True), fill='#263238')
        colour = render_icon(icon, 146)
        sheet.paste(colour, (x+20, y+54), colour)
        char = chr(icon['codepoint'])
        bounds = draw.textbbox((0, 0), char, font=glyph_font)
        draw.text((x+236-bounds[0], y+57-bounds[1]), char, font=glyph_font, fill='#303A40')
        draw.text((x+22, y+219), 'COLOUR', font=font(12), fill='#617279')
        draw.text((x+238, y+219), f'TTF  U+{icon["codepoint"]:04X}', font=font(12), fill='#617279')
        save_png(render_icon(icon, 128), png/(icon['id']+'.png'))
        save_png(render_dark(icon, 128), png/(icon['id']+'-dark.png'))
    save_png(sheet, dist/(preview+'.png'))

    # Real UI sizes on light and dark surfaces, to catch vanishing internal detail.
    small = Image.new('RGB', (1050, 54+len(suite)*73), '#F8FAFB')
    draw = ImageDraw.Draw(small)
    draw.text((20, 12), 'OPTICAL CHECK  /  colour 24 32 48  /  font 24 32 48  /  dark background', font=font(19, True), fill='#263238')
    for index, icon in enumerate(suite):
        y = 57+index*73
        draw.text((18, y+20), icon['name'], font=font(15), fill='#263238')
        for offset, size in enumerate((24, 32, 48)):
            art = render_icon(icon, size)
            small.paste(art, (305+offset*65, y+(58-size)//2), art)
            f = ImageFont.truetype(str(ttf), size)
            bounds = draw.textbbox((0, 0), chr(icon['codepoint']), font=f)
            draw.text((530+offset*65-bounds[0], y+8-bounds[1]), chr(icon['codepoint']), font=f, fill='#303A40')
        draw.rounded_rectangle((760, y, 1032, y+61), 5, fill='#202A30')
        for offset, size in enumerate((24, 32, 48)):
            art = render_dark(icon, size)
            small.paste(art, (783+offset*79, y+(58-size)//2), art)
    save_png(small, dist/(prefix+'_small_sizes.png'))
