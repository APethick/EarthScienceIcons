from functools import lru_cache, partial
from icons_geophysics_expanded import Diagram, INK, STEEL, SAND, ROCK, BLUE, RED, YELLOW, GLASS, WHITE

# Schematic field instruments and geological scales on the shared 48-unit canvas.
@lru_cache(maxsize=None)
def design(kind):
    if kind not in ("jacobian", "hessian"):
        from field_detail import design as detailed_design
        return detailed_design(kind)
    d = Diagram()
    if kind in ('jacobian','hessian'):
        d.line([(9,6),(6,6),(6,42),(9,42)],INK,1.5); d.line([(39,6),(42,6),(42,42),(39,42)],INK,1.5)
        # Hessian is symmetric, Jacobian is rectangular with independently varying entries.
        for row in range(3 if kind == 'jacobian' else 4):
            for col in range(4):
                radius = ((1.1,2.4,1.5,2.0),(2.2,1.3,2.5,1.1),(1.4,2.1,1.2,2.4))[row][col] if kind == 'jacobian' else (2.5 if row == col else (1.1 if abs(row-col)>1 else 1.8))
                d.circle(13+col*7.2, 13+row*(11 if kind == 'jacobian' else 7.2),radius,INK,INK,True)
    return d

ROWS = [
 ('gp_em31','EM31 Ground Conductivity Meter','Long boom electromagnetic ground conductivity instrument with end coils.', 'em31'),
 ('gp_em38','EM38 Ground Conductivity Meter','Compact electromagnetic ground conductivity instrument with end coils.', 'em38'),
 ('gp_tempest_aem','TEMPEST Airborne EM System','Fixed-wing airborne electromagnetic survey aircraft with towed receiver bird.', 'tempest'),
 ('gc_inversion_jacobian_matrix','Jacobian Matrix','Rectangular matrix of model-to-data first derivatives.', 'jacobian'),
 ('gc_inversion_hessian_matrix','Hessian Matrix','Symmetric matrix of second derivatives or curvature.', 'hessian'),
 ('gl_scale_pore','Pore Scale','Pore spaces between mineral grains.', 'scale_pore'),
 ('gl_scale_grain','Mineral Grain Scale','Individual mineral grains and grain boundaries.', 'scale_grain'),
 ('gl_scale_specimen','Rock Specimen Scale','Hand specimen with internal geological texture.', 'scale_specimen'),
 ('gl_scale_outcrop','Outcrop Scale','Exposed rock with layers in an outcrop.', 'scale_outcrop'),
 ('gl_scale_structure','Structural Scale','Folded geological layers cut by a fault.', 'scale_structure'),
 ('gl_scale_deposit','Mineral Deposit Scale','Mineralised body within host rocks.', 'scale_deposit'),
 ('gl_scale_district','Mining District Scale','Map with several mineral occurrences.', 'scale_district'),
 ('gl_scale_crustal','Crustal Scale','Cross section through layered continental crust.', 'scale_crust'),
 ('gl_tool_compass','Geological Compass','Field compass for orientation and geological mapping.', 'compass'),
 ('gl_tool_clinometer','Geological Clinometer','Inclination gauge for measuring geological dip.', 'clinometer'),
 ('gl_tool_rock_hammer','Geological Rock Hammer','Geologist hammer for exposing and collecting rock.', 'hammer'),
 ('gl_tool_hand_lens','Geological Hand Lens','Hand lens for examining mineral grains and textures.', 'hand_lens'),
 ('gl_tool_field_notebook','Geological Field Notebook','Field notebook for recording observations.', 'field_notebook'),
 ('gl_tool_streak_plate','Mineral Streak Plate','Unglazed plate and mineral sample for streak testing.', 'streak_plate'),
 ('gl_tool_sample_bag','Geological Sample Bag','Bag holding a geological specimen.', 'sample_bag'),
 ('gl_tool_measuring_tape','Field Measuring Tape','Tape measure for field observations and geological logging.', 'measuring_tape'),
]
ICONS = [dict(id=identifier, codepoint=0xE1E5+i, name=name, domain=('Geophysical' if identifier.startswith('gp_') else 'Geochemical' if identifier.startswith('gc_') else 'Geological'), category=('Processes' if identifier.startswith('gc_') or identifier.startswith('gl_scale_') else 'Methods'), description=desc, keywords=[kind.replace('_',' '),name], kind=kind, builder=partial(lambda k: design(k).geometry(),kind)) for i,(identifier,name,desc,kind) in enumerate(ROWS)]
IDS = {icon['id'] for icon in ICONS}
def flat_artwork(icon):
    from icons_geophysics_expanded import flat_artwork as render
    return render(icon, design(icon['kind']))
