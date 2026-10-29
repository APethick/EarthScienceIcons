package opus.base.icons;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Arrays;

import org.controlsfx.glyphfont.GlyphFont;
import org.controlsfx.glyphfont.GlyphFontRegistry;
import org.controlsfx.glyphfont.INamedCharacter;

import opus.base.properties.OpusProperty;
import opus.base.resources.OpusResources;

/**
 * GeoScienceIcons TrueType glyph font (527 icons) covering Geophysical, Geotechnical,
 * Geological, and Geochemical methods, earth model types, and processes.
 * Includes dedicated suites for Inversion, Thermodynamics, Petrophysics, and Geochemistry,
 * aligned with opus.geo.geochemistry, opus.geo.petrophysics, and opus.geo.geotechnical.
 */
public class GeoScienceIcons extends GlyphFont {

    private static final Logger logger = LogManager.getLogger(GeoScienceIcons.class.getName());
    public static final String FONT_NAME = "GeoScience Icons";

    public enum Glyph implements INamedCharacter {
		GP_SEISMIC_REFLECTION('\ue001'), // Seismic Reflection Survey (Geophysical - Methods)
		GP_GRAVITY_SURVEY('\ue002'), // Gravity Survey (Geophysical - Methods)
		GP_MAGNETIC_SURVEY('\ue003'), // Magnetic Survey (Geophysical - Methods)
		GP_ELECTROMAGNETIC_EM('\ue004'), // Electromagnetic (EM) Induction (Geophysical - Methods)
		GP_ERT_IP('\ue005'), // Electrical Resistivity & IP (ERT/IP) (Geophysical - Methods)
		GP_VELOCITY_MODEL('\ue006'), // Seismic Velocity Model (Geophysical - Earth Model Types)
		GP_DENSITY_MODEL('\ue007'), // Density Contrast Block Model (Geophysical - Earth Model Types)
		GP_SUSCEPTIBILITY_MODEL('\ue008'), // Magnetic Susceptibility Model (Geophysical - Earth Model Types)
		GP_RESISTIVITY_SECTION('\ue009'), // Resistivity Pseudosection (Geophysical - Earth Model Types)
		GP_SEISMIC_CUBE_3D('\ue00a'), // 3D Seismic Volume Cube (Geophysical - Earth Model Types)
		GP_WAVE_PROPAGATION('\ue00b'), // Seismic Wave Propagation (Geophysical - Processes)
		GP_RAY_REFRACTION_SNELL('\ue00c'), // Snell's Law & Critical Refraction (Geophysical - Processes)
		GP_GEOPHYSICAL_INVERSION('\ue00d'), // Forward & Inverse Modeling (Geophysical - Processes)
		GP_SIGNAL_DECONVOLUTION('\ue00e'), // Wavelet Deconvolution (Geophysical - Processes)
		GP_NMO_STACKING('\ue00f'), // NMO Correction & Stacking (Geophysical - Processes)
		GT_SPT_TEST('\ue010'), // Standard Penetration Test (SPT) (Geotechnical - Methods)
		GT_CPT_CONE('\ue011'), // Cone Penetration Test (CPT) (Geotechnical - Methods)
		GT_TRIAXIAL_SHEAR('\ue012'), // Triaxial Shear Compression Test (Geotechnical - Methods)
		GT_PIEZOMETER_WELL('\ue013'), // Piezometer & Groundwater Well (Geotechnical - Methods)
		GT_INCLINOMETER_CASING('\ue014'), // Borehole Inclinometer (Geotechnical - Methods)
		GT_MOHR_COULOMB('\ue015'), // Mohr-Coulomb Failure Envelope (Geotechnical - Earth Model Types)
		GT_ROCK_MASS_RMR_GSI('\ue016'), // Rock Mass Classification (RMR / GSI) (Geotechnical - Earth Model Types)
		GT_SLOPE_STABILITY_GRID('\ue017'), // Limit Equilibrium Slope Model (Geotechnical - Earth Model Types)
		GT_SOIL_PROFILE_LOG('\ue018'), // Engineering Soil Horizon Profile (Geotechnical - Earth Model Types)
		GT_FE_MESH_TUNNEL('\ue019'), // Geomechanical FEA Tunnel Mesh (Geotechnical - Earth Model Types)
		GT_CONSOLIDATION_SETTLEMENT('\ue01a'), // Consolidation & Foundation Settlement (Geotechnical - Processes)
		GT_SOIL_LIQUEFACTION('\ue01b'), // Seismic Soil Liquefaction (Geotechnical - Processes)
		GT_SLOPE_LANDSLIDE('\ue01c'), // Rotational Slope Failure & Landslide (Geotechnical - Processes)
		GT_SEEPAGE_FLOWNET('\ue01d'), // Darcy Seepage & Flow Net (Geotechnical - Processes)
		GT_ROCK_BURST_SPALLING('\ue01e'), // Stress Spalling & Rockburst (Geotechnical - Processes)
		GL_STRIKE_DIP_MAPPING('\ue01f'), // Structural Strike & Dip Mapping (Geological - Methods)
		GL_DIAMOND_CORE_DRILLING('\ue020'), // Diamond Core Drilling (Geological - Methods)
		GL_THIN_SECTION_PETROGRAPHY('\ue021'), // Thin-Section Optical Petrography (Geological - Methods)
		GL_STRATIGRAPHIC_LOGGING('\ue022'), // Measured Stratigraphic Column (Geological - Methods)
		GL_STRUCTURAL_STEREONET('\ue023'), // Schmidt Structural Stereonet (Geological - Methods)
		GL_BLOCK_MODEL_3D('\ue024'), // 3D Resource Block Model (Geological - Earth Model Types)
		GL_WIREFRAME_MESH('\ue025'), // 3D Geological Wireframe Mesh (Geological - Earth Model Types)
		GL_FAULTED_STRATIGRAPHY('\ue026'), // Faulted Stratigraphic Horizon Model (Geological - Earth Model Types)
		GL_FOLDED_ANTICLINE_MODEL('\ue027'), // Folded Anticline-Syncline Model (Geological - Earth Model Types)
		GL_INTRUSIVE_PLUTON_MODEL('\ue028'), // Igneous Pluton, Dike & Sill Model (Geological - Earth Model Types)
		GL_PLATE_SUBDUCTION('\ue029'), // Plate Tectonic Subduction (Geological - Processes)
		GL_FAULT_SLIP_TECTONICS('\ue02a'), // Tectonic Fault Slip & Rupture (Geological - Processes)
		GL_SEDIMENTATION_DEPOSITION('\ue02b'), // Sediment Transport & Deposition (Geological - Processes)
		GL_METAMORPHISM_PT('\ue02c'), // Metamorphic P-T Recrystallization (Geological - Processes)
		GL_WEATHERING_EROSION('\ue02d'), // Weathering & Erosional Breakdown (Geological - Processes)
		GC_SOIL_STREAM_SAMPLING('\ue02e'), // Soil & Stream Geochemical Sampling (Geochemical - Methods)
		GC_PXRF_ANALYZER('\ue02f'), // Portable XRF (pXRF) Analyzer (Geochemical - Methods)
		GC_ICP_MS_SPECTROMETRY('\ue030'), // ICP-MS / OES Mass Spectrometry (Geochemical - Methods)
		GC_FIRE_ASSAY('\ue031'), // Fire Assay & Cupellation (Geochemical - Methods)
		GC_ISOTOPE_RATIO_ANALYSIS('\ue032'), // Radiogenic & Stable Isotope Analysis (Geochemical - Methods)
		GC_ALTERATION_ZONATION('\ue033'), // Hydrothermal Alteration Zonation (Geochemical - Earth Model Types)
		GC_GEOCHEM_ANOMALY_CONTOURS('\ue034'), // Geochemical Iso-Grade Contour Map (Geochemical - Earth Model Types)
		GC_TERNARY_CLASSIFICATION('\ue035'), // Geochemical Ternary Diagram (Geochemical - Earth Model Types)
		GC_EH_PH_POURBAIX('\ue036'), // Eh-pH (Pourbaix) Stability Diagram (Geochemical - Earth Model Types)
		GC_DOWNHOLE_GEOCHEM_LOG('\ue037'), // Downhole Multi-Element Assay Log (Geochemical - Earth Model Types)
		GC_HYDROTHERMAL_CIRCULATION('\ue038'), // Hydrothermal Fluid Convection (Geochemical - Processes)
		GC_SUPERGENE_LEACHING('\ue039'), // Supergene Leaching & Enrichment (Geochemical - Processes)
		GC_REDOX_FRONT_ROLL('\ue03a'), // Roll-Front Redox Migration (Geochemical - Processes)
		GC_MAGMATIC_DIFFERENTIATION('\ue03b'), // Magmatic Differentiation & Cumulates (Geochemical - Processes)
		GC_ELEMENT_DISPERSION_HALO('\ue03c'), // Geochemical Dispersion Halo (Geochemical - Processes)
		GP_SELF_POTENTIAL('\ue03d'), // Self-Potential (SP) Method (Geophysical - Methods)
		GP_MAGNETOTELLURICS_MT('\ue03e'), // Magnetotellurics (MT) (Geophysical - Methods)
		GP_GROUND_PENETRATING_RADAR('\ue03f'), // Ground Penetrating Radar (GPR) (Geophysical - Methods)
		GP_RADIOMETRICS_GAMMA('\ue040'), // Radiometric Gamma Spectrometry (Geophysical - Methods)
		GP_NMR_SOUNDING('\ue041'), // Nuclear Magnetic Resonance (NMR) (Geophysical - Methods)
		GP_THERMAL_GEOTHERMAL('\ue042'), // Thermal & Heat Flow Survey (Geophysical - Methods)
		GP_ACOUSTICS_SONAR('\ue043'), // Acoustics & Sonar Imaging (Geophysical - Methods)
		GP_GEODESY_INSAR_GNSS('\ue044'), // Geodesy, GNSS & InSAR (Geophysical - Methods)
		GP_REMOTE_SENSING_HYPERSPECTRAL('\ue045'), // Remote Sensing & Hyperspectral (Geophysical - Methods)
		GP_MATRIX_MIXING_BOUNDS('\ue046'), // Matrix Mixing Model (Voigt / Reuss / HS / Bruggeman) (Geophysical - Earth Model Types)
		GP_PORE_FLUID_ARCHIE('\ue047'), // Pore Fluid & Archie / Waxman-Smits Model (Geophysical - Earth Model Types)
		GP_IP_COLE_COLE('\ue048'), // IP Relaxation Model (Cole-Cole / Revil) (Geophysical - Earth Model Types)
		GP_DIELECTRIC_PERMITTIVITY('\ue049'), // Dielectric Permittivity Model (CRIM / Topp) (Geophysical - Earth Model Types)
		GP_KOENIGSBERGER_REMANENCE('\ue04a'), // Magnetic Remanence & Koenigsberger Model (Geophysical - Earth Model Types)
		GP_GASSMANN_FLUID_SUB('\ue04b'), // Gassmann & Rock Physics Velocity Model (Geophysical - Earth Model Types)
		GP_PERMEABILITY_KOZENY('\ue04c'), // Permeability Model (Kozeny-Carman / Timur) (Geophysical - Earth Model Types)
		GT_DEERE_RQD('\ue04d'), // Deere RQD (Rock Quality Designation) (Geotechnical - Earth Model Types)
		GT_BARTON_Q_TUNNEL('\ue04e'), // Barton Q-System Tunnel Support (Geotechnical - Earth Model Types)
		GT_BIENIAWSKI_RMR('\ue04f'), // Bieniawski RMR Scorecard (Geotechnical - Earth Model Types)
		GT_HOEK_BROWN_CRITERION('\ue050'), // Generalized Hoek-Brown Criterion (Geotechnical - Earth Model Types)
		GT_UCS_FROM_VELOCITY('\ue051'), // UCS from P-Wave Velocity (Geotechnical - Earth Model Types)
		GT_BRITTLENESS_INDEX('\ue052'), // Rock Brittleness Index (Geotechnical - Earth Model Types)
		GL_ROCK_TYPE_IGNEOUS('\ue053'), // Igneous Rock Type (Geological - Earth Model Types)
		GL_ROCK_TYPE_SEDIMENTARY('\ue054'), // Sedimentary Rock Type (Geological - Earth Model Types)
		GL_ROCK_TYPE_METAMORPHIC('\ue055'), // Metamorphic Rock Type (Geological - Earth Model Types)
		GL_COMPOSITION_CATEGORY('\ue056'), // Silicate & Lithological Composition (Geological - Earth Model Types)
		GL_GENETIC_CATEGORY('\ue057'), // Genetic Classification & Rock Cycle (Geological - Processes)
		GL_METAMORPHIC_FACIES_PT('\ue058'), // Metamorphic Facies & Grade (P-T Grid) (Geological - Earth Model Types)
		GL_CONSOLIDATION_DEGREE('\ue059'), // Consolidation & Induration Degree (Geological - Processes)
		GL_DEFORMATION_BRITTLE_DUCTILE('\ue05a'), // Brittle-Ductile Deformation Style (Geological - Processes)
		GL_UNIT_MORPHOLOGY('\ue05b'), // Geologic Unit Morphology (Boudin & Dome) (Geological - Earth Model Types)
		GL_STYLE_DISSEMINATED('\ue05c'), // Disseminated Sulfide Texture (Geological - Earth Model Types)
		GL_STYLE_NET_TEXTURED('\ue05d'), // Net-Textured Matrix Sulfide (Geological - Earth Model Types)
		GL_STYLE_MASSIVE_SULFIDE('\ue05e'), // Semi-Massive & Massive Sulfide Ore (Geological - Earth Model Types)
		GL_STYLE_VEINED_STRINGER('\ue05f'), // Veined & Stringer Stockwork Texture (Geological - Earth Model Types)
		GL_PARTICLE_SHAPE_ROUNDNESS('\ue060'), // Particle Shape, Roundness & Aspect Ratio (Geological - Earth Model Types)
		GL_CONTACT_UNCONFORMITY('\ue061'), // Geological Contact & Unconformity (Geological - Earth Model Types)
		GL_FOLIATION_LINEATION('\ue062'), // Foliation & Mineral Lineation (S-L Fabric) (Geological - Earth Model Types)
		GL_BOREHOLE_DRILLING_METHODS('\ue063'), // Rotary, RC & Auger Borehole Drilling (Geological - Methods)
		GL_PLANAR_POLARITY_OVERTURNED('\ue064'), // Planar Polarity (Upright vs Overturned) (Geological - Methods)
		GM_ACID_ROCK_DRAINAGE('\ue065'), // Acid Rock Drainage (ARD / NAPP / NAG) (Geochemical - Processes)
		GM_COMMINUTION_WORK_INDEX('\ue066'), // Comminution & Bond Work Index (Wi / SAG) (Geochemical - Processes)
		GM_FLOTATION_RECOVERY('\ue067'), // Mineral Liberation & Flotation Recovery (Geochemical - Processes)
		GC_MELT_CHEMISTRY_F02('\ue068'), // Silicate Melt Chemistry & Oxygen Fugacity (fO2) (Geochemical - Earth Model Types)
		GC_CARBON_MINERALISATION('\ue069'), // Ultramafic CO2 Sequestration & Carbonation (Geochemical - Processes)
		GL_LITHOLOGY_TENSOR_ANISOTROPY('\ue06a'), // Lithology Fabric & Tensor Anisotropy (Geological - Earth Model Types)
		GL_FAULT_NORMAL_GRABEN('\ue06b'), // Horst & Graben Extensional Rift (Geological - Earth Model Types)
		GL_FAULT_THRUST_RAMP('\ue06c'), // Thrust Fault & Ramp-Flat Anticline (Geological - Earth Model Types)
		GL_FAULT_STRIKE_SLIP_DEXTRAL('\ue06d'), // Dextral Strike-Slip & Riedel Shears (Geological - Processes)
		GL_SHEAR_ZONE_SIGMOIDAL('\ue06e'), // Ductile Shear Zone & Delta Porphyroclast (Geological - Processes)
		GL_CHEVRON_KINK_FOLD('\ue06f'), // Chevron & Kink Band Folds (Geological - Earth Model Types)
		GL_PTYGMATIC_VEIN_FOLD('\ue070'), // Ptygmatic Metamorphic Fold (Geological - Earth Model Types)
		GL_COLUMNAR_JOINTING('\ue071'), // Basalt Columnar Cooling Jointing (Geological - Earth Model Types)
		GL_SPINIFEX_TEXTURE('\ue072'), // Komatiite Spinifex Texture (Geological - Earth Model Types)
		GL_PILLOW_LAVA('\ue073'), // Pillow Basalt & Geopetal Way-Up (Geological - Earth Model Types)
		GL_FIAMME_IGNIMBRITE('\ue074'), // Ignimbrite & Welded Fiamme (Geological - Earth Model Types)
		GL_BANDED_IRON_FORMATION('\ue075'), // Banded Iron Formation (BIF) (Geological - Earth Model Types)
		GL_HYDROTHERMAL_BRECCIA('\ue076'), // Hydrothermal Jigsaw Breccia (Geological - Earth Model Types)
		GL_POTASSIC_ALTERATION('\ue077'), // Potassic Hydrothermal Alteration (Geological - Processes)
		GL_PHYLLIC_SERICITIC_ALTERATION('\ue078'), // Phyllic (Sericitic / QSP) Alteration (Geological - Processes)
		GL_ADVANCED_ARGILLIC('\ue079'), // Advanced Argillic & Vuggy Silica (Geological - Processes)
		GL_PROPYLITIC_CHLORITE_EPIDOTE('\ue07a'), // Propylitic Alteration (Chlorite-Epidote) (Geological - Processes)
		GL_SERPENTINITE_MESH('\ue07b'), // Serpentinisation Mesh Texture (Geological - Processes)
		GL_SKARN_CALC_SILICATE('\ue07c'), // Calc-Silicate Skarn Reaction Zone (Geological - Earth Model Types)
		GL_GREISEN_CASSITERITE('\ue07d'), // Greisen & Twinned Cassiterite (Geological - Earth Model Types)
		GL_TOURMALINE_SUN_ROSETTE('\ue07e'), // Tourmaline Sun Rosette (Geological - Earth Model Types)
		GL_TURBIDITE_BOUMA_SEQUENCE('\ue07f'), // Turbidite Bouma Sequence (Ta-Te) (Geological - Earth Model Types)
		GL_FLUVIAL_POINT_BAR_CHANNEL('\ue080'), // Fluvial Point Bar & Meander Channel (Geological - Earth Model Types)
		GC_LA_ICP_MS_LASER('\ue081'), // LA-ICP-MS Laser Microprobe (Geochemical - Methods)
		GC_EPMA_WDS_MICROPROBE('\ue082'), // Electron Microprobe (EPMA / WDS) (Geochemical - Methods)
		GC_XRD_DIFFRACTOMETER('\ue083'), // X-Ray Powder Diffraction (XRD) (Geochemical - Methods)
		GC_XANES_SYNCHROTRON('\ue084'), // Synchrotron X-Ray Absorption (XANES) (Geochemical - Methods)
		GC_LIBS_LASER_PLASMA('\ue085'), // Laser-Induced Breakdown (LIBS) (Geochemical - Methods)
		GC_FTIR_RAMAN_SPECTROSCOPY('\ue086'), // FTIR & Raman Vibrational Spectroscopy (Geochemical - Methods)
		GC_FOUR_ACID_TOTAL_DIGEST('\ue087'), // Four-Acid Near-Total Digestion (Geochemical - Methods)
		GC_AQUA_REGIA_PARTIAL_DIGEST('\ue088'), // Aqua Regia Partial Digestion (Geochemical - Methods)
		GC_CYANIDE_BOTTLE_ROLL('\ue089'), // Cyanide Bottle Roll Leach Test (Geochemical - Methods)
		GC_SEQUENTIAL_EXTRACTION('\ue08a'), // Sequential Chemical Extraction (Geochemical - Methods)
		GC_GAS_CHROMATOGRAPHY_MS('\ue08b'), // Gas Chromatography-MS (GC-MS) (Geochemical - Methods)
		GC_SIMS_SHRIMP_MICROPROBE('\ue08c'), // Secondary Ion Mass Spectrometry (SIMS / SHRIMP) (Geochemical - Methods)
		GC_TIMS_THERMAL_IONIZATION('\ue08d'), // Thermal Ionization Mass Spectrometry (TIMS) (Geochemical - Methods)
		GC_STABLE_ISOTOPE_GAS_IRMS('\ue08e'), // Gas Stable Isotope Ratio MS (IRMS) (Geochemical - Methods)
		GC_FLUID_INCLUSION_MICROTHERM('\ue08f'), // Fluid Inclusion Microthermometry (Geochemical - Methods)
		GC_RADON_EMANOMETRY('\ue090'), // Soil-Gas Radon Emanometry (Geochemical - Methods)
		GC_BIOGEOCHEM_VEGETATION('\ue091'), // Biogeochemical Vegetation Sampling (Geochemical - Methods)
		GC_REE_CHONDRITE_SPIDERGRAM('\ue092'), // Chondrite-Normalized REE Spidergram (Geochemical - Earth Model Types)
		GC_PRIMITIVE_MANTLE_SPIDERGRAM('\ue093'), // Primitive Mantle Multi-Element Spidergram (Geochemical - Earth Model Types)
		GC_TAS_VOLCANIC_DIAGRAM('\ue094'), // TAS Volcanic Classification Diagram (Geochemical - Earth Model Types)
		GC_QAPF_TERNARY_DOUBLE('\ue095'), // QAPF Double-Ternary Diamond (Geochemical - Earth Model Types)
		GC_PEARCE_TECTONIC_DISCRIMINATION('\ue096'), // Pearce Granite Tectonic Discrimination (Geochemical - Earth Model Types)
		GC_ACTIVITY_ACTIVITY_DIAGRAM('\ue097'), // Hydrothermal Activity-Activity Diagram (Geochemical - Earth Model Types)
		GC_ZIRCON_UPB_CONCORDIA('\ue098'), // Wetherill U-Pb Concordia Diagram (Geochemical - Earth Model Types)
		GC_RB_SR_ISOCHRON_DIAGRAM('\ue099'), // Radiogenic Isochron Diagram (Rb-Sr) (Geochemical - Earth Model Types)
		GC_SULFUR_ISOTOPE_DELTA34S('\ue09a'), // Sulfur Isotope (delta34S) Fractionation (Geochemical - Earth Model Types)
		GC_SWIR_MINERAL_SPECTRAL_TROUGH('\ue09b'), // Diagnostic SWIR Mineral Absorption Trough (Geochemical - Earth Model Types)
		GC_CAMPBELL_VECTORING_RATIO('\ue09c'), // Campbell Porphyry Geochemical Vector (Geochemical - Earth Model Types)
		GC_ALUMINA_SATURATION_ASI('\ue09d'), // Alumina Saturation Index (ASI / Shand) (Geochemical - Earth Model Types)
		GC_HARKER_VARIATION_DIAGRAM('\ue09e'), // Harker Major Oxide Variation Diagram (Geochemical - Earth Model Types)
		GC_WATER_SOLUBILITY_MELT('\ue09f'), // Volatile H2O-CO2 Magma Solubility (Geochemical - Earth Model Types)
		GC_OXYGEN_ISOTOPE_DELTA18O('\ue0a0'), // Meteoric Water Line & Oxygen Shift (Geochemical - Earth Model Types)
		GC_HYDROTHERMAL_BOILING_IMMISCIBILITY('\ue0a1'), // Hydrothermal Boiling & Phase Separation (Geochemical - Processes)
		GC_SULFIDE_MELT_IMMISCIBILITY('\ue0a2'), // Magmatic Sulfide Liquid Immiscibility (Geochemical - Processes)
		GC_FLUID_ROCK_METASOMATISM('\ue0a3'), // Metasomatic Infiltration Reaction Front (Geochemical - Processes)
		GC_BACTERIAL_SULFATE_REDUCTION('\ue0a4'), // Bacterial Sulfate Reduction (BSR / Framboid) (Geochemical - Processes)
		GC_HEAVY_MINERAL_PLACER('\ue0a5'), // Heavy Mineral Placer Hydrodynamics (Geochemical - Processes)
		GC_GOSSAN_BOXWORK_WEATHERING('\ue0a6'), // Gossan Cellular Boxwork Weathering (Geochemical - Processes)
		GC_FUMAROLIC_GAS_EXSOLUTION('\ue0a7'), // Volcanic Fumarolic Gas Exsolution (Geochemical - Processes)
		GC_CLAY_ADSORPTION_CEC('\ue0a8'), // Clay Interlayer Cation Adsorption (CEC) (Geochemical - Processes)
		GC_METAL_CHLORIDE_COMPLEXATION('\ue0a9'), // Hydrothermal Metal Complexation (Geochemical - Processes)
		GC_HYDROCARBON_CATAGENESIS('\ue0aa'), // Hydrocarbon Catagenesis & Cracking (Geochemical - Processes)
		GC_COLLOID_FLOCCULATION('\ue0ab'), // Estuarine Colloid Flocculation (Geochemical - Processes)
		GC_GIBBS_FREE_ENERGY('\ue0ac'), // Gibbs Free Energy Minimisation (Geochemical - Processes)
		GC_CHEMICAL_ELEMENTS('\ue0ad'), // Chemical Elements & Atomic Structure (Geochemical - Earth Model Types)
		GL_MINERALS_SPECIMEN('\ue0ae'), // Minerals & Crystal Aggregate (Geological - Earth Model Types)
		GC_ELEMENT_DIFF_WTPCT('\ue0af'), // Element Difference in Weight Percent (Geochemical - Methods)
		GC_TEMPERATURE_THERMO('\ue0b0'), // Temperature & Geothermometry (Geochemical - Methods)
		GC_PRESSURE_GAUGE('\ue0b1'), // Pressure & Geobarometry (Geotechnical - Methods)
		GC_GRADIENT_PERTURBATION_FACTOR('\ue0b2'), // Gradient Perturbation Factor (Geophysical - Methods)
		GC_L1_NORM_REGULARIZATION('\ue0b3'), // L1 Norm Sparse Regularization (Geophysical - Methods)
		GC_N_ITERATIONS_LOOP('\ue0b4'), // Optimization Iteration Loop (Geophysical - Processes)
		GC_THERMODYNAMICS_SYSTEM('\ue0b5'), // Thermodynamic Equilibrium & Heat System (Geochemical - Processes)
		GP_PETROPHYSICS_CORE_MATRIX('\ue0b6'), // Petrophysics & Core Plug Porosity (Geophysical - Earth Model Types)
		GL_POSITIONS_SPATIAL_COORDS('\ue0b7'), // Spatial Coordinate Positions (Geological - Methods)
		GC_VOLATILES_DEGASSING('\ue0b8'), // Magmatic Volatiles & Degassing Bubbles (Geochemical - Processes)
		GC_WATER_ACTIVITY_AH2O('\ue0b9'), // Water Activity (aH2O) (Geochemical - Earth Model Types)
		GC_FLUID_XCO2_MOLE_FRACTION('\ue0ba'), // Fluid Carbon Dioxide Mole Fraction (XCO2) (Geochemical - Earth Model Types)
		GC_OXYGEN_FUGACITY_FO2('\ue0bb'), // Oxygen Fugacity & Redox State (fO2) (Geochemical - Earth Model Types)
		GC_MAJOR_ELEMENT_OXIDES('\ue0bc'), // Major Element Silicate Oxides (Geochemical - Earth Model Types)
		GC_GRADIENT_INITIAL_STEP('\ue0bd'), // Gradient Descent Initial Step Size (Geophysical - Methods)
		GC_SENSITIVITY_JACOBIAN('\ue0be'), // Inversion Sensitivity Matrix (Geophysical - Methods)
		GP_SPECIFIC_GRAVITY_BALANCE('\ue0bf'), // Specific Gravity & Hydrostatic Balance (Geophysical - Methods)
		GC_LOG_ERROR_RESIDUALS('\ue0c0'), // Logarithmic Residual Error (Geophysical - Methods)
		GL_GEOLOGICAL_TAGGING_DOMAIN('\ue0c1'), // Geological Domain Tagging (Geological - Methods)
		GP_AIRBORNE_EM_AEM('\ue0c2'), // Airborne Electromagnetics (AEM) (Geophysical - Methods)
		GP_FIXED_WING_AEM('\ue0c3'), // Fixed-Wing AEM & Towed Bird (Geophysical - Methods)
		GP_FREQUENCY_DOMAIN_EM_FDEM('\ue0c4'), // Frequency-Domain EM (FDEM) (Geophysical - Methods)
		GP_TIME_DOMAIN_EM_TDEM('\ue0c5'), // Time-Domain EM (TDEM) (Geophysical - Methods)
		GP_CSEM_MARINE('\ue0c6'), // Marine Controlled-Source EM (CSEM) (Geophysical - Methods)
		GP_CSEM_LAND('\ue0c7'), // Land Controlled-Source EM (CSEM) (Geophysical - Methods)
		GP_CSAMT('\ue0c8'), // Controlled-Source Audio-MT (CSAMT) (Geophysical - Methods)
		GP_GROUND_TEM('\ue0c9'), // Ground TEM Survey (Geophysical - Methods)
		GP_TEM_FIXED_LOOP('\ue0ca'), // Fixed-Loop TEM (Geophysical - Methods)
		GP_TEM_MOVING_LOOP('\ue0cb'), // Moving-Loop TEM (Geophysical - Methods)
		GP_TEM_CENTRAL_LOOP('\ue0cc'), // Central-Loop TEM (Geophysical - Methods)
		GP_TEM_IN_LOOP('\ue0cd'), // In-Loop TEM (Geophysical - Methods)
		GP_TEM_LOTEM('\ue0ce'), // Long-Offset TEM (LOTEM) (Geophysical - Methods)
		GP_LOUPE_TEM('\ue0cf'), // Loupe Portable TEM (Geophysical - Methods)
		GP_VTEM('\ue0d0'), // VTEM Airborne TEM (Geophysical - Methods)
		GP_SKYTEM('\ue0d1'), // SkyTEM Dual-Moment AEM (Geophysical - Methods)
		GP_SLINGRAM_EM('\ue0d2'), // Slingram Ground EM (Geophysical - Methods)
		GP_VLF_EM('\ue0d3'), // Very Low Frequency EM (VLF) (Geophysical - Methods)
		GP_AIRBORNE_MAGNETICS('\ue0d4'), // Airborne Magnetic Survey (Geophysical - Methods)
		GP_GROUND_MAGNETICS('\ue0d5'), // Ground Magnetic Survey (Geophysical - Methods)
		GP_MAGNETIC_GRADIOMETRY('\ue0d6'), // Magnetic Gradiometry (Geophysical - Methods)
		GP_ELECTRICAL_IP_CHARGEABILITY('\ue0d7'), // Time-Domain Induced Polarization (Geophysical - Methods)
		GP_IP_SPECTRAL('\ue0d8'), // Spectral Induced Polarization (SIP) (Geophysical - Methods)
		GP_TEM_DECAY_GATES('\ue0d9'), // TEM Decay & Time Gates (Geophysical - Processes)
		GP_GPR_B_SCAN('\ue0da'), // GPR Radargram / B-Scan (Geophysical - Methods)
		GP_GPR_TIME_SLICE('\ue0db'), // GPR Time / Depth Slice (Geophysical - Methods)
		GP_GPR_VOLUME_3D('\ue0dc'), // 3D GPR Volume (Geophysical - Methods)
		GP_GPR_CMP_VELOCITY('\ue0dd'), // GPR CMP / WARR Velocity (Geophysical - Methods)
		GP_GPR_UTILITY_DETECTION('\ue0de'), // GPR Utility Detection (Geophysical - Methods)
		GP_GPR_CONCRETE_REBAR('\ue0df'), // GPR Concrete & Rebar Scan (Geophysical - Methods)
		GP_GPR_BOREHOLE('\ue0e0'), // Borehole / Crosshole Radar (Geophysical - Methods)
		GP_GPR_ANTENNA('\ue0e1'), // GPR Shielded Antenna (Geophysical - Methods)
		GP_RADIOMETRICS_TOTAL('\ue0e2'), // Radiometrics — Total Count (Geophysical - Methods)
		GP_RADIOMETRICS_POTASSIUM_K('\ue0e3'), // Radiometrics — Potassium (K) (Geophysical - Methods)
		GP_RADIOMETRICS_URANIUM_U('\ue0e4'), // Radiometrics — Uranium (eU) (Geophysical - Methods)
		GP_RADIOMETRICS_THORIUM_TH('\ue0e5'), // Radiometrics — Thorium (eTh) (Geophysical - Methods)
		GP_RADIOMETRICS_TERNARY('\ue0e6'), // Radiometric K–U–Th Ternary (Geophysical - Methods)
		GP_AIRBORNE_RADIOMETRICS('\ue0e7'), // Airborne Gamma Spectrometry (Geophysical - Methods)
		GP_SEISMIC_CROSSHOLE('\ue0e8'), // Crosshole Seismic Survey (Geophysical - Methods)
		GP_SEISMIC_DOWNHOLE('\ue0e9'), // Downhole Seismic Survey (Geophysical - Methods)
		GP_SEISMIC_UPHOLE('\ue0ea'), // Uphole Seismic Survey (Geophysical - Methods)
		GP_SEISMIC_VSP('\ue0eb'), // Vertical Seismic Profile (VSP) (Geophysical - Methods)
		GP_SEISMIC_REFRACTION('\ue0ec'), // Seismic Refraction Survey (Geophysical - Methods)
		GP_SEISMIC_MASW('\ue0ed'), // Surface-Wave Seismics (MASW) (Geophysical - Methods)
		GP_SEISMIC_HVSR('\ue0ee'), // Passive Seismic H/V (HVSR) (Geophysical - Methods)
		GP_BOREHOLE_EM_BHEM('\ue0ef'), // Borehole EM (BHEM / DHEM) (Geophysical - Methods)
		GP_BOREHOLE_INDUCTION_LOG('\ue0f0'), // Borehole Induction Conductivity (Geophysical - Methods)
		GP_BOREHOLE_RESISTIVITY_LOG('\ue0f1'), // Borehole Resistivity Log (Geophysical - Methods)
		GP_BOREHOLE_IP_LOG('\ue0f2'), // Borehole IP Log (Geophysical - Methods)
		GP_BOREHOLE_SP_LOG('\ue0f3'), // Borehole Self-Potential (SP) (Geophysical - Methods)
		GP_BOREHOLE_MAGNETIC_SUSCEPTIBILITY('\ue0f4'), // Borehole Magnetic Susceptibility (Geophysical - Methods)
		GP_BOREHOLE_MAGNETOMETER('\ue0f5'), // Borehole Magnetometer (Geophysical - Methods)
		GP_BOREHOLE_NATURAL_GAMMA('\ue0f6'), // Borehole Natural Gamma (Geophysical - Methods)
		GP_BOREHOLE_SPECTRAL_GAMMA('\ue0f7'), // Borehole Spectral Gamma (Geophysical - Methods)
		GP_BOREHOLE_DENSITY_LOG('\ue0f8'), // Borehole Gamma-Gamma Density (Geophysical - Methods)
		GP_BOREHOLE_NEUTRON_POROSITY('\ue0f9'), // Borehole Neutron Porosity (Geophysical - Methods)
		GP_BOREHOLE_SONIC_LOG('\ue0fa'), // Borehole Sonic / Full Waveform (Geophysical - Methods)
		GP_BOREHOLE_ACOUSTIC_TELEVIEWER('\ue0fb'), // Acoustic Borehole Televiewer (Geophysical - Methods)
		GP_BOREHOLE_OPTICAL_TELEVIEWER('\ue0fc'), // Optical Borehole Televiewer (Geophysical - Methods)
		GP_BOREHOLE_CALIPER('\ue0fd'), // Borehole Caliper (Geophysical - Methods)
		GP_BOREHOLE_TEMPERATURE('\ue0fe'), // Borehole Temperature Log (Geophysical - Methods)
		GP_BOREHOLE_FLUID_CONDUCTIVITY('\ue0ff'), // Borehole Fluid Conductivity (Geophysical - Methods)
		GP_BOREHOLE_FLOWMETER('\ue100'), // Borehole Flowmeter (Geophysical - Methods)
		GP_BOREHOLE_NMR('\ue101'), // Borehole NMR Log (Geophysical - Methods)
		GP_BOREHOLE_GRAVITY('\ue102'), // Borehole Gravimetry (Geophysical - Methods)
		GP_CROSSHOLE_ERT('\ue103'), // Crosshole Electrical Tomography (Geophysical - Methods)
		GP_CROSSHOLE_EM_TOMOGRAPHY('\ue104'), // Crosshole EM Tomography (Geophysical - Methods)
		GP_CROSSHOLE_SEISMIC_TOMOGRAPHY('\ue105'), // Crosshole Seismic Tomography (Geophysical - Methods)
		GP_PROPERTY_CONDUCTIVITY('\ue106'), // Electrical Conductivity (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_RESISTIVITY('\ue107'), // Electrical Resistivity (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_DENSITY('\ue108'), // Bulk Density (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_MAGNETIC_SUSCEPTIBILITY('\ue109'), // Magnetic Susceptibility (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_REMANENT_MAGNETIZATION('\ue10a'), // Remanent Magnetization (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_CHARGEABILITY('\ue10b'), // IP Chargeability (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_VP('\ue10c'), // P-Wave Velocity (Vp) (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_VS('\ue10d'), // S-Wave Velocity (Vs) (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_POROSITY('\ue10e'), // Porosity (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_PERMEABILITY('\ue10f'), // Permeability (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_DIELECTRIC_PERMITTIVITY('\ue110'), // Dielectric Permittivity (Geophysical - Petrophysical Quantities)
		GP_PROPERTY_THERMAL_CONDUCTIVITY('\ue111'), // Thermal Conductivity (Geophysical - Petrophysical Quantities)
		GP_ELECTRIC_FIELD('\ue112'), // Electric Field (Geophysical - Processes)
		GP_ELECTRIC_FIELD_X('\ue113'), // Electric Field Ex (Geophysical - Processes)
		GP_ELECTRIC_FIELD_Y('\ue114'), // Electric Field Ey (Geophysical - Processes)
		GP_ELECTRIC_FIELD_Z('\ue115'), // Electric Field Ez (Geophysical - Processes)
		GP_MAGNETIC_FIELD('\ue116'), // Magnetic Field (Geophysical - Processes)
		GP_MAGNETIC_FIELD_X('\ue117'), // Magnetic Field Hx (Geophysical - Processes)
		GP_MAGNETIC_FIELD_Y('\ue118'), // Magnetic Field Hy (Geophysical - Processes)
		GP_MAGNETIC_FIELD_Z('\ue119'), // Magnetic Field Hz (Geophysical - Processes)
		GP_POYNTING_VECTOR('\ue11a'), // Poynting Vector (Geophysical - Processes)
		GP_SIGNAL_SPECTRUM('\ue11b'), // Recording Spectrum (Geophysical - Processes)
		GP_FFT_TRANSFORM('\ue11c'), // Fourier Transform FFT (Geophysical - Processes)
		GP_SIGNAL_SPECTROGRAM('\ue11d'), // Recording Spectrogram (Geophysical - Processes)
		GP_RAW_WAVEFORM('\ue11e'), // Raw Time Series (Geophysical - Processes)
		GP_CROSS_POWER('\ue11f'), // Cross Power (Geophysical - Processes)
		GP_SIGNAL_COHERENCE('\ue120'), // Signal Coherence (Geophysical - Processes)
		GP_SENSOR_CALIBRATION('\ue121'), // Sensor Calibration Response (Geophysical - Processes)
		GP_REMOTE_REFERENCE('\ue122'), // Remote Reference Pair (Geophysical - Processes)
		GP_MT_IMPEDANCE_TENSOR('\ue123'), // MT Impedance Tensor (Geophysical - Processes)
		GP_MT_PHASE_TENSOR('\ue124'), // MT Phase Tensor (Geophysical - Processes)
		GP_MT_TIPPER('\ue125'), // MT Tipper (Geophysical - Processes)
		GC_GEOCHEMICAL_VECTORING('\ue126'), // Geochemical Vectoring (Geochemical - Processes)
		GC_HYDROTHERMAL_ALTERATION('\ue127'), // Hydrothermal Alteration (Geochemical - Processes)
		GC_MAGMATIC_INTRUSION('\ue128'), // Magmatic Intrusion (Geochemical - Processes)
		GC_DEHYDRATION('\ue129'), // Dehydration (Geochemical - Processes)
		GC_REDUCING_ENVIRONMENT('\ue12a'), // Reducing Environment (Geochemical - Processes)
		GC_OXIDIZING_ENVIRONMENT('\ue12b'), // Oxidizing Environment (Geochemical - Processes)
		GC_SAUSSURITISED('\ue12c'), // Saussuritised (Geochemical - Processes)
		GC_SERPENTINISATION('\ue12d'), // Serpentinisation (Geochemical - Processes)
		GC_EPIDOTE_ALTERATION('\ue12e'), // Epidote alteration (Geochemical - Processes)
		GC_SILICIFICATION('\ue12f'), // Silicification (Geochemical - Processes)
		GC_CARBONATE_ALTERATION('\ue130'), // Carbonate alteration (Geochemical - Processes)
		GC_CALCSILICATE_ALTERATION('\ue131'), // Calcsilicate alteration (Geochemical - Processes)
		GC_GREISEN('\ue132'), // Greisen (Geochemical - Processes)
		GC_ALBITIC_ALTERATION('\ue133'), // Albitic alteration (Geochemical - Processes)
		GC_ADVANCED_ARGILLIC_ALTERATION('\ue134'), // Advanced argillic alteration (Geochemical - Processes)
		GC_NOT_ALTERED('\ue135'), // Not altered (Geochemical - Processes)
		GC_CHLORITIC_ALTERATION('\ue136'), // Chloritic alteration (Geochemical - Processes)
		GC_ZEOLITIC_ALTERATION('\ue137'), // Zeolitic alteration (Geochemical - Processes)
		GC_PROPYLITIC_ALTERATION('\ue138'), // Propylitic alteration (Geochemical - Processes)
		GC_POTASSIC_ALTERATION('\ue139'), // Potassic alteration (Geochemical - Processes)
		GC_ALTERATION_NOT_SPECIFIED('\ue13a'), // Alteration type not specified (Geochemical - Processes)
		GC_KAOLINITIC_ALTERATION('\ue13b'), // Kaolinitic alteration (Geochemical - Processes)
		GC_SERICITIC_ALTERATION('\ue13c'), // Sericitic alteration (Geochemical - Processes)
		GC_ARGILLIC_ALTERATION('\ue13d'), // Argillic alteration (Geochemical - Processes)
		GC_ALUNITIC_ALTERATION('\ue13e'), // Alunitic alteration (Geochemical - Processes)
		GC_HEMATITIC_ALTERATION('\ue13f'), // Hematitic alteration (Geochemical - Processes)
		GC_PYRITIC_ALTERATION('\ue140'), // Pyritic alteration (Geochemical - Processes)
		GC_DEUTERIC_ALTERATION('\ue141'), // Deuteric alteration (Geochemical - Processes)
		GC_URALITISATION('\ue142'), // Uralitisation (Geochemical - Processes)
		GC_RED_ROCK_ALTERATION('\ue143'), // Red rock alteration (Geochemical - Processes)
		GL_GRANITE_POST_KINEMATIC('\ue144'), // Post-Kinematic Granite (Geological - Earth Model Types)
		GL_GRANITE_LATE_POST_KINEMATIC('\ue145'), // Late- to Post-Kinematic Granite (Geological - Earth Model Types)
		GL_GRANITE_SYN_LATE_KINEMATIC('\ue146'), // Syn- to Late-Kinematic Granite (Geological - Earth Model Types)
		GL_GRANITE_SYN_KINEMATIC_FOLIATED('\ue147'), // Syn-Kinematic Foliated Granite (Geological - Earth Model Types)
		GL_GRANITE_GNEISSIC_ANATECTIC('\ue148'), // Gneissic Anatectic Granite (Geological - Earth Model Types)
		GL_GABBRO_DIORITE_OROGENIC('\ue149'), // Orogenic Gabbro-Diorite (Geological - Earth Model Types)
		GL_PORPHYRY_PATTERN('\ue14a'), // Porphyry Pattern (Geological - Earth Model Types)
		GL_ISLAND_ARC_VOLCANICS('\ue14b'), // Island-Arc Volcanics (Geological - Earth Model Types)
		GL_FELSIC_VOLCANICS_RARE_BASICS('\ue14c'), // Rift Felsic Volcanics with Rare Basics (Geological - Earth Model Types)
		GL_RHYOLITE_DACITE_VOLCANICS('\ue14d'), // Rhyolite and Dacite Volcanics (Geological - Earth Model Types)
		GL_FELSIC_VOLCANICS_WITH_GRANITE('\ue14e'), // Felsic Volcanics Associated with Granite (Geological - Earth Model Types)
		GL_FLOOD_BASALT('\ue14f'), // Flood Basalt and Trap (Geological - Earth Model Types)
		GL_DOLERITE_GRANOPHYRE('\ue150'), // Dolerite-Granophyre (Geological - Earth Model Types)
		GL_KERATOPHYRE('\ue151'), // Keratophyre (Geological - Earth Model Types)
		GL_GRANITE_INTRUDING_CRATON('\ue152'), // Granite Intruding Craton (Geological - Earth Model Types)
		GL_LAYERED_INTRUSION('\ue153'), // Layered Mafic-Ultramafic Intrusion (Geological - Earth Model Types)
		GL_ALKALINE_INTRUSIVE('\ue154'), // Alkaline Intrusive (Geological - Earth Model Types)
		GL_KIMBERLITE_LAMPROITE('\ue155'), // Kimberlite and Lamproite (Geological - Earth Model Types)
		GL_CARBONATITE('\ue156'), // Carbonatite (Geological - Earth Model Types)
		GL_SLATE_PHYLLITE('\ue157'), // Slate and Phyllite Pattern (Geological - Earth Model Types)
		GL_SCHIST_GNEISS_HIGH_GRADE('\ue158'), // High-Grade Schist and Gneiss Pattern (Geological - Earth Model Types)
		GL_SANDY_SLATE_INTERBEDDED('\ue159'), // Sandy Slate and Interbedded Sediments (Geological - Earth Model Types)
		GL_HORNFELS_MASSIVE('\ue15a'), // Massive Hornfels Pattern (Geological - Earth Model Types)
		GL_BASIC_PLUTONIC_HYPABYSSAL('\ue15b'), // Basic Plutonic and Hypabyssal Pattern (Geological - Earth Model Types)
		GL_BEDDED_LAVAS('\ue15c'), // Bedded Lavas Pattern (Geological - Earth Model Types)
		GL_TUFF_TUFFACEOUS_SANDSTONE('\ue15d'), // Tuff and Tuffaceous Sandstone (Geological - Earth Model Types)
		GL_BEDDED_TUFF('\ue15e'), // Bedded Tuff and Tuffaceous Shale (Geological - Earth Model Types)
		GL_BRECCIA_PATTERN('\ue15f'), // Breccia Pattern (Geological - Earth Model Types)
		GL_SCREE_BRECCIATED_ROCK('\ue160'), // Brecciated Rock and Scree (Geological - Earth Model Types)
		GL_SOIL_COVER('\ue161'), // Soil Cover Pattern (Geological - Earth Model Types)
		GL_ALLUVIUM('\ue162'), // Alluvium Pattern (Geological - Earth Model Types)
		GL_GOSSAN_ORE('\ue163'), // Gossan and Ore Outcrop Pattern (Geological - Earth Model Types)
		GL_CONGLOMERATE_PATTERN('\ue164'), // Conglomerate Pattern (Geological - Earth Model Types)
		GL_SANDSTONE_PATTERN('\ue165'), // Sandstone Pattern (Geological - Earth Model Types)
		GL_PEBBLY_SANDSTONE('\ue166'), // Pebbly Sandstone Pattern (Geological - Earth Model Types)
		GL_CROSS_BEDDED_SANDSTONE('\ue167'), // Cross-Bedded Sandstone Pattern (Geological - Earth Model Types)
		GL_LIMESTONE_PATTERN('\ue168'), // Limestone Pattern (Geological - Earth Model Types)
		GL_DOLOMITE_PATTERN('\ue169'), // Dolomite Pattern (Geological - Earth Model Types)
		GL_SANDY_LIMESTONE('\ue16a'), // Sandy Limestone Pattern (Geological - Earth Model Types)
		GL_SHALE_PATTERN('\ue16b'), // Shale Pattern (Geological - Earth Model Types)
		GL_SANDY_SHALE('\ue16c'), // Sandy Shale Pattern (Geological - Earth Model Types)
		GL_BEDDED_CHERT('\ue16d'), // Bedded Chert Pattern (Geological - Earth Model Types)
		GL_MASSIVE_CHERT('\ue16e'), // Massive Chert Pattern (Geological - Earth Model Types)
		GL_COAL_UNDIFFERENTIATED('\ue16f'), // Undifferentiated Coal Pattern (Geological - Earth Model Types)
		GL_BROKEN_COAL('\ue170'), // Broken Coal Pattern (Geological - Earth Model Types)
		GL_COAL_WITH_SHALE_BANDS('\ue171'), // Coal with Shale Bands (Geological - Earth Model Types)
		GL_SHALE_WITH_COAL_BANDS('\ue172'), // Shale with Coal Bands (Geological - Earth Model Types)
		GL_CANNEL_COAL('\ue173'), // Cannel Coal Pattern (Geological - Earth Model Types)
		GL_CANNEL_SHALE('\ue174'), // Cannel Shale Pattern (Geological - Earth Model Types)
		GL_CARBONACEOUS_SHALE('\ue175'), // Carbonaceous Shale Pattern (Geological - Earth Model Types)
		GL_BROWN_COAL('\ue176'), // Brown Coal Pattern (Geological - Earth Model Types)
		GL_OIL_SHALE('\ue177'), // Oil Shale Pattern (Geological - Earth Model Types)
		GL_THIN_SEAM('\ue178'), // Thin Dipping Coal Seam (Geological - Earth Model Types)
		GL_COAL_BRIGHT('\ue179'), // Bright Coal Seam (>90% Bright) (Geological - Earth Model Types)
		GL_COAL_BRIGHT_DULL_BANDS('\ue17a'), // Bright Coal with Dull Bands (60-90%) (Geological - Earth Model Types)
		GL_COAL_INTERBANDED('\ue17b'), // Interbanded Dull and Bright Coal (40-60%) (Geological - Earth Model Types)
		GL_COAL_DULL_BRIGHT_BANDS('\ue17c'), // Mainly Dull Coal with Bright Bands (10-40%) (Geological - Earth Model Types)
		GL_COAL_DULL_MINOR_BRIGHT('\ue17d'), // Dull Coal with Minor Bright Bands (1-10%) (Geological - Earth Model Types)
		GL_COAL_DULL('\ue17e'), // Dull Coal (Up to 1% Bright) (Geological - Earth Model Types)
		GL_COAL_CANNELOID('\ue17f'), // Canneloid Dull Conchoidal Coal (Geological - Earth Model Types)
		GL_COAL_FIBROUS('\ue180'), // Fibrous Coal (Fusain) (Geological - Earth Model Types)
		GL_COAL_WEATHERED('\ue181'), // Weathered Coal Seam (Geological - Earth Model Types)
		GL_COAL_HEAT_ALTERED('\ue182'), // Heat-Altered (Cindered) Coal Seam (Geological - Earth Model Types)
		GL_NON_COAL('\ue183'), // Undifferentiated Non-Coal Seam Parting (Geological - Earth Model Types)
		GL_COAL_INTERLAYERED_NON_COAL('\ue184'), // Coal Interlayered with Non-Coal (Geological - Earth Model Types)
		GL_NON_COAL_INTERLAYERED_COAL('\ue185'), // Non-Coal Interlayered with Coal (Geological - Earth Model Types)
		GL_STONY_COAL('\ue186'), // Stony Coal Seam (Geological - Earth Model Types)
		GL_MUDSTONE_PATTERN('\ue187'), // Mudstone Pattern (Geological - Earth Model Types)
		GL_COAL_SEAM_LOG('\ue188'), // Graphic Coal Seam Column (Geological - Earth Model Types)
		GL_FOLD_UPRIGHT_HORIZONTAL('\ue189'), // Upright Horizontal Fold (Geological - Earth Model Types)
		GL_FOLD_UPRIGHT_PLUNGING('\ue18a'), // Upright Plunging Fold (Geological - Earth Model Types)
		GL_FOLD_VERTICAL('\ue18b'), // Vertical Fold (Geological - Earth Model Types)
		GL_FOLD_INCLINED_PLUNGING('\ue18c'), // Inclined Plunging Fold (Geological - Earth Model Types)
		GL_FOLD_OVERTURNED_HORIZONTAL('\ue18d'), // Overturned Horizontal Fold (Geological - Earth Model Types)
		GL_FOLD_OVERTURNED_PLUNGING('\ue18e'), // Overturned Plunging Fold (Geological - Earth Model Types)
		GL_FOLD_RECUMBENT('\ue18f'), // Recumbent Fold (Geological - Earth Model Types)
		GL_FOLD_RECLINED('\ue190'), // Reclined Fold (Geological - Earth Model Types)
		GL_MONOCLINE('\ue191'), // Monocline (Geological - Earth Model Types)
		GL_FOLD_VERGENCE('\ue192'), // Fold Vergence (Geological - Processes)
		GL_SUPERPOSED_FOLDS('\ue193'), // Superposed Folds (Geological - Earth Model Types)
		GL_FOLD_CLASS_1A('\ue194'), // Fold Class 1A (Strongly Convergent) (Geological - Earth Model Types)
		GL_FOLD_CLASS_1B('\ue195'), // Fold Class 1B (Parallel) (Geological - Earth Model Types)
		GL_FOLD_CLASS_1C('\ue196'), // Fold Class 1C (Weakly Convergent) (Geological - Earth Model Types)
		GL_FOLD_CLASS_2('\ue197'), // Fold Class 2 (Similar) (Geological - Earth Model Types)
		GL_FOLD_CLASS_3('\ue198'), // Fold Class 3 (Divergent) (Geological - Earth Model Types)
		GL_DIP_ISOGON_CONSTRUCTION('\ue199'), // Dip Isogon Construction (Geological - Methods)
		GL_FOLD_ATTITUDE_GRID('\ue19a'), // Fold Attitude Triangular Grid (Geological - Methods)
		GL_FOLD_ATTITUDE_CLASSIFICATION('\ue19b'), // Fold Attitude Classification Triangle (Geological - Methods)
		GL_ORTHOGRAPHIC_NET('\ue19c'), // Orthographic Stereonet (Geological - Methods)
		GL_WULFF_NET('\ue19d'), // Wulff Equal-Angle Stereonet (Geological - Methods)
		GL_SCHMIDT_NET('\ue19e'), // Schmidt Equal-Area Stereonet (Geological - Methods)
		GL_STEREONET_CONTOURING_DEVICE('\ue19f'), // Stereonet Contouring Device (Geological - Methods)
		GL_ROCK_FALL('\ue1a0'), // Rock Fall (Geological - Processes)
		GL_ROCK_TOPPLE('\ue1a1'), // Rock Topple (Geological - Processes)
		GL_ROCK_SLUMP('\ue1a2'), // Rock Slump (Geological - Processes)
		GL_ROCK_BLOCK_SLIDE('\ue1a3'), // Rock Block Slide (Geological - Processes)
		GL_ROCK_LATERAL_SPREAD('\ue1a4'), // Rock Lateral Spread (Geological - Processes)
		GL_ROCK_CREEP_SACKUNG('\ue1a5'), // Rock Creep (Sackung) (Geological - Processes)
		GL_ROCK_FALL_DEBRIS_FLOW('\ue1a6'), // Rock Fall–Debris Flow (Geological - Processes)
		GL_SLUMP_TOPPLE('\ue1a7'), // Slump and Topple (Geological - Processes)
		GL_ROCK_SLIDE_ROCK_FALL('\ue1a8'), // Rock Slide–Rock Fall (Geological - Processes)
		GL_DEBRIS_FALL('\ue1a9'), // Debris Fall (Geological - Processes)
		GL_DEBRIS_TOPPLE('\ue1aa'), // Debris Topple (Geological - Processes)
		GL_DEBRIS_SLUMP('\ue1ab'), // Debris Slump (Geological - Processes)
		GL_DEBRIS_SLIDE('\ue1ac'), // Debris Slide (Geological - Processes)
		GL_DEBRIS_FLOW('\ue1ad'), // Debris Flow (Geological - Processes)
		GL_DEBRIS_AVALANCHE('\ue1ae'), // Debris Avalanche (Geological - Processes)
		GL_BLOCK_STREAM('\ue1af'), // Block Stream (Geological - Processes)
		GL_SOLIFLUCTION('\ue1b0'), // Solifluction (Geological - Processes)
		GL_SOIL_CREEP('\ue1b1'), // Soil Creep (Geological - Processes)
		GL_CAMBERING_VALLEY_BULGING('\ue1b2'), // Cambering and Valley Bulging (Geological - Processes)
		GL_SLUMP_EARTH_FLOW('\ue1b3'), // Slump–Earth Flow (Geological - Processes)
		GL_EARTH_FALL('\ue1b4'), // Earth Fall (Geological - Processes)
		GL_EARTH_TOPPLE('\ue1b5'), // Earth Topple (Geological - Processes)
		GL_EARTH_SLUMP('\ue1b6'), // Earth Slump (Geological - Processes)
		GL_EARTH_BLOCK_SLIDE('\ue1b7'), // Earth Block Slide (Geological - Processes)
		GL_EARTH_LATERAL_SPREAD('\ue1b8'), // Earth Lateral Spread (Geological - Processes)
		GL_WET_SAND_SILT_FLOW('\ue1b9'), // Wet Sand or Silt Flow (Geological - Processes)
		GL_QUICK_CLAY_FLOW('\ue1ba'), // Quick Clay Flow (Geological - Processes)
		GL_EARTH_FLOW('\ue1bb'), // Earth Flow (Geological - Processes)
		GL_LOESS_FLOW('\ue1bc'), // Loess Flow (Geological - Processes)
		GL_DRY_SAND_FLOW('\ue1bd'), // Dry Sand Flow (Geological - Processes)
		GL_QAPF_PLUTONIC_DIAGRAM('\ue1be'), // QAPF Plutonic Rock Diagram (Geological - Earth Model Types)
		GL_GABBROIC_PLAG_PX_OL('\ue1bf'), // Gabbroic Rocks (Plag-Px-Ol) (Geological - Earth Model Types)
		GL_GABBROIC_PLAG_PX_HBL('\ue1c0'), // Gabbroic Rocks (Plag-Px-Hbl) (Geological - Earth Model Types)
		GL_GABBROIC_PLAG_OPX_CPX('\ue1c1'), // Gabbroic Rocks (Plag-Opx-Cpx) (Geological - Earth Model Types)
		GL_METAMORPHIC_FACIES_DIAGRAM('\ue1c2'), // Metamorphic Facies Diagram (P-T) (Geological - Earth Model Types)
		GL_ROUNDNESS_VERY_ANGULAR('\ue1c3'), // Roundness: Very Angular (Geological - Earth Model Types)
		GL_ROUNDNESS_ANGULAR('\ue1c4'), // Roundness: Angular (Geological - Earth Model Types)
		GL_ROUNDNESS_SUBANGULAR('\ue1c5'), // Roundness: Subangular (Geological - Earth Model Types)
		GL_ROUNDNESS_SUBROUNDED('\ue1c6'), // Roundness: Subrounded (Geological - Earth Model Types)
		GL_ROUNDNESS_ROUNDED('\ue1c7'), // Roundness: Rounded (Geological - Earth Model Types)
		GL_ROUNDNESS_WELL_ROUNDED('\ue1c8'), // Roundness: Well-Rounded (Geological - Earth Model Types)
		GL_GRAIN_PERCENT_01('\ue1c9'), // Grain Percentage: 1% (Geological - Methods)
		GL_GRAIN_PERCENT_02('\ue1ca'), // Grain Percentage: 2% (Geological - Methods)
		GL_GRAIN_PERCENT_03('\ue1cb'), // Grain Percentage: 3% (Geological - Methods)
		GL_GRAIN_PERCENT_05('\ue1cc'), // Grain Percentage: 5% (Geological - Methods)
		GL_GRAIN_PERCENT_07('\ue1cd'), // Grain Percentage: 7% (Geological - Methods)
		GL_GRAIN_PERCENT_10('\ue1ce'), // Grain Percentage: 10% (Geological - Methods)
		GL_GRAIN_PERCENT_15('\ue1cf'), // Grain Percentage: 15% (Geological - Methods)
		GL_GRAIN_PERCENT_20('\ue1d0'), // Grain Percentage: 20% (Geological - Methods)
		GL_GRAIN_PERCENT_25('\ue1d1'), // Grain Percentage: 25% (Geological - Methods)
		GL_GRAIN_PERCENT_30('\ue1d2'), // Grain Percentage: 30% (Geological - Methods)
		GL_GRAIN_PERCENT_40('\ue1d3'), // Grain Percentage: 40% (Geological - Methods)
		GL_GRAIN_PERCENT_50('\ue1d4'), // Grain Percentage: 50% (Geological - Methods)
		GL_UNIT_STRATOTYPE('\ue1d5'), // Unit Stratotype (Geological - Earth Model Types)
		GL_BOUNDARY_STRATOTYPE('\ue1d6'), // Boundary Stratotype (Geological - Earth Model Types)
		GL_EARTHQUAKE_MAGNITUDE_ENERGY('\ue1d7'), // Earthquake Magnitude vs Energy (Geological - Processes)
		GP_HYPERSPECTRAL_LAB('\ue1d8'), // Laboratory Hyperspectral Spectroscopy (Geophysical - Methods)
		GP_HYPERSPECTRAL_SATELLITE('\ue1d9'), // Satellite Hyperspectral Imaging (Geophysical - Methods)
		GP_HYPERSPECTRAL_CUBE('\ue1da'), // Hyperspectral Data Cube (Geophysical - Methods)
		GP_HYPERSPECTRAL_BANDS('\ue1db'), // Hyperspectral Band Selection (Geophysical - Methods)
		GP_HYPERSPECTRAL_SPECTRUM('\ue1dc'), // Recorded Spectral Signature (Geophysical - Methods)
		GP_HYPERSPECTRAL_UV('\ue1dd'), // Ultraviolet Spectroscopy (UV) (Geophysical - Methods)
		GP_HYPERSPECTRAL_VISIBLE('\ue1de'), // Visible Spectroscopy (VIS) (Geophysical - Methods)
		GP_HYPERSPECTRAL_VNIR('\ue1df'), // Visible–Near Infrared Spectroscopy (VNIR) (Geophysical - Methods)
		GP_HYPERSPECTRAL_NIR('\ue1e0'), // Near Infrared Spectroscopy (NIR) (Geophysical - Methods)
		GP_HYPERSPECTRAL_IR('\ue1e1'), // Infrared Spectroscopy (IR) (Geophysical - Methods)
		GP_HYPERSPECTRAL_SWIR('\ue1e2'), // Shortwave Infrared Spectroscopy (SWIR) (Geophysical - Methods)
		GP_HYPERSPECTRAL_MWIR('\ue1e3'), // Midwave Infrared Spectroscopy (MWIR) (Geophysical - Methods)
		GP_HYPERSPECTRAL_TIR('\ue1e4'), // Thermal Infrared Spectroscopy (TIR / LWIR) (Geophysical - Methods)
		GP_EM31('\ue1e5'), // EM31 Ground Conductivity Meter (Geophysical - Methods)
		GP_EM38('\ue1e6'), // EM38 Ground Conductivity Meter (Geophysical - Methods)
		GP_TEMPEST_AEM('\ue1e7'), // TEMPEST Airborne EM System (Geophysical - Methods)
		GC_INVERSION_JACOBIAN_MATRIX('\ue1e8'), // Jacobian Matrix (Geochemical - Processes)
		GC_INVERSION_HESSIAN_MATRIX('\ue1e9'), // Hessian Matrix (Geochemical - Processes)
		GL_SCALE_PORE('\ue1ea'), // Pore Scale (Geological - Processes)
		GL_SCALE_GRAIN('\ue1eb'), // Mineral Grain Scale (Geological - Processes)
		GL_SCALE_SPECIMEN('\ue1ec'), // Rock Specimen Scale (Geological - Processes)
		GL_SCALE_OUTCROP('\ue1ed'), // Outcrop Scale (Geological - Processes)
		GL_SCALE_STRUCTURE('\ue1ee'), // Structural Scale (Geological - Processes)
		GL_SCALE_DEPOSIT('\ue1ef'), // Mineral Deposit Scale (Geological - Processes)
		GL_SCALE_DISTRICT('\ue1f0'), // Mining District Scale (Geological - Processes)
		GL_SCALE_CRUSTAL('\ue1f1'), // Crustal Scale (Geological - Processes)
		GL_TOOL_COMPASS('\ue1f2'), // Geological Compass (Geological - Methods)
		GL_TOOL_CLINOMETER('\ue1f3'), // Geological Clinometer (Geological - Methods)
		GL_TOOL_ROCK_HAMMER('\ue1f4'), // Geological Rock Hammer (Geological - Methods)
		GL_TOOL_HAND_LENS('\ue1f5'), // Geological Hand Lens (Geological - Methods)
		GL_TOOL_FIELD_NOTEBOOK('\ue1f6'), // Geological Field Notebook (Geological - Methods)
		GL_TOOL_STREAK_PLATE('\ue1f7'), // Mineral Streak Plate (Geological - Methods)
		GL_TOOL_SAMPLE_BAG('\ue1f8'), // Geological Sample Bag (Geological - Methods)
		GL_TOOL_MEASURING_TAPE('\ue1f9'), // Field Measuring Tape (Geological - Methods)
		GP_SEISMIC_SOURCE_HAMMER('\ue1fa'), // Sledgehammer Seismic Source (Geophysical - Methods)
		GP_SEISMIC_SOURCE_EXPLOSIVE('\ue1fb'), // Buried Explosive Seismic Source (Geophysical - Methods)
		GP_SEISMIC_SOURCE_BETSY('\ue1fc'), // Betsy Gun Seismic Source (Geophysical - Methods)
		GP_SEISMIC_SOURCE_WEIGHT_DROP_UTE('\ue1fd'), // Ute-Mounted Weight Drop (Geophysical - Methods)
		GP_SEISMIC_SOURCE_WEIGHT_DROP_SKID('\ue1fe'), // Skid-Steer Weight Drop (Geophysical - Methods)
		GP_SEISMIC_SOURCE_EVIBE('\ue1ff'), // Electric Seismic Vibrator (eVibe) (Geophysical - Methods)
		GP_SEISMIC_SOURCE_VIBROSEIS('\ue200'), // Vibroseis Truck (Geophysical - Methods)
		GP_SEISMIC_SOURCE_AIRGUN('\ue201'), // Marine Air Gun (Geophysical - Methods)
		GP_SEISMIC_SOURCE_LAND_STREAMER('\ue202'), // Land Streamer (Geophysical - Methods)
		GP_SEISMIC_SOURCE_SPARKER('\ue203'), // Marine Sparker (Geophysical - Methods)
		GP_SEISMIC_SOURCE_BOOMER('\ue204'), // Marine Boomer (Geophysical - Methods)
		GP_SEISMIC_RECEIVER_SPIKED('\ue205'), // Spiked Geophone (Geophysical - Methods)
		GP_SEISMIC_RECEIVER_WIRED('\ue206'), // Wired Geophone String (Geophysical - Methods)
		GP_SEISMIC_RECEIVER_WIRELESS('\ue207'), // Wireless Seismic Recorder (Geophysical - Methods)
		GP_SEISMIC_RECEIVER_QUANTUM('\ue208'), // INOVA Quantum Node (Geophysical - Methods)
		GP_SEISMIC_RECEIVER_SMARTSOLO('\ue209'), // SmartSolo IGU Node (Geophysical - Methods)
		GP_SEISMIC_RECEIVER_WING('\ue20a'), // Sercel WiNG Node (Geophysical - Methods)
		GP_SEISMIC_RECEIVER_GEOSPACE('\ue20b'), // Geospace Recorder with Geophone (Geophysical - Methods)
		GP_SEISMIC_RECEIVER_THREE_COMPONENT('\ue20c'), // Three-Component Geophone (Geophysical - Methods)
		GP_SEISMIC_RECEIVER_HYDROPHONE('\ue20d'), // Hydrophone (Geophysical - Methods)
		GP_LOOP_MAGNETIC_FIELD('\ue20e'), // Magnetic Field Around a Loop (Geophysical - Processes)
		GP_EM_SMOKE_RING('\ue20f'), // Propagating EM Smoke Ring (Geophysical - Processes)
        ;

        private final char ch;

        Glyph(char ch) {
            this.ch = ch;
        }

        @Override
        public char getChar() {
            return ch;
        }
    }

    public GeoScienceIcons() {
        super(FONT_NAME, 14, getBufferedStream(), true);
        GlyphFontRegistry.register(FONT_NAME, getBufferedStream(), 14);
        registerAll(Arrays.asList(Glyph.values()));
    }

    @Override
    public org.controlsfx.glyphfont.Glyph create(String glyphName) {
        GlyphFont font = GlyphFontRegistry.font(FONT_NAME);
        char c = getCharacter(glyphName);
        return font.create(c);
    }

    private static InputStream getBufferedStream() {
        InputStream bundled = GeoScienceIcons.class.getResourceAsStream("/fonts/GeoScienceIcons.ttf");
        if (bundled == null) bundled = GeoScienceIcons.class.getResourceAsStream("GeoScienceIcons.ttf");
        if (bundled != null) return new BufferedInputStream(bundled);
        try {
            return new BufferedInputStream(new FileInputStream(new File(OpusResources.getResourcePath("fonts/GeoScienceIcons.ttf"))));
        } catch (Exception e) {
            logger.error("Failed to load GeoScienceIcons.ttf", e);
        }
        return null;
    }

    public static Glyph forIconId(String iconId) {
        if (iconId == null) return null;
        return switch (iconId.toLowerCase(java.util.Locale.ROOT).trim()) {
			case "gp_seismic_reflection" -> Glyph.GP_SEISMIC_REFLECTION;
			case "gp_gravity_survey" -> Glyph.GP_GRAVITY_SURVEY;
			case "gp_magnetic_survey" -> Glyph.GP_MAGNETIC_SURVEY;
			case "gp_electromagnetic_em" -> Glyph.GP_ELECTROMAGNETIC_EM;
			case "gp_ert_ip" -> Glyph.GP_ERT_IP;
			case "gp_velocity_model" -> Glyph.GP_VELOCITY_MODEL;
			case "gp_density_model" -> Glyph.GP_DENSITY_MODEL;
			case "gp_susceptibility_model" -> Glyph.GP_SUSCEPTIBILITY_MODEL;
			case "gp_resistivity_section" -> Glyph.GP_RESISTIVITY_SECTION;
			case "gp_seismic_cube_3d" -> Glyph.GP_SEISMIC_CUBE_3D;
			case "gp_wave_propagation" -> Glyph.GP_WAVE_PROPAGATION;
			case "gp_ray_refraction_snell" -> Glyph.GP_RAY_REFRACTION_SNELL;
			case "gp_geophysical_inversion" -> Glyph.GP_GEOPHYSICAL_INVERSION;
			case "gp_signal_deconvolution" -> Glyph.GP_SIGNAL_DECONVOLUTION;
			case "gp_nmo_stacking" -> Glyph.GP_NMO_STACKING;
			case "gt_spt_test" -> Glyph.GT_SPT_TEST;
			case "gt_cpt_cone" -> Glyph.GT_CPT_CONE;
			case "gt_triaxial_shear" -> Glyph.GT_TRIAXIAL_SHEAR;
			case "gt_piezometer_well" -> Glyph.GT_PIEZOMETER_WELL;
			case "gt_inclinometer_casing" -> Glyph.GT_INCLINOMETER_CASING;
			case "gt_mohr_coulomb" -> Glyph.GT_MOHR_COULOMB;
			case "gt_rock_mass_rmr_gsi" -> Glyph.GT_ROCK_MASS_RMR_GSI;
			case "gt_slope_stability_grid" -> Glyph.GT_SLOPE_STABILITY_GRID;
			case "gt_soil_profile_log" -> Glyph.GT_SOIL_PROFILE_LOG;
			case "gt_fe_mesh_tunnel" -> Glyph.GT_FE_MESH_TUNNEL;
			case "gt_consolidation_settlement" -> Glyph.GT_CONSOLIDATION_SETTLEMENT;
			case "gt_soil_liquefaction" -> Glyph.GT_SOIL_LIQUEFACTION;
			case "gt_slope_landslide" -> Glyph.GT_SLOPE_LANDSLIDE;
			case "gt_seepage_flownet" -> Glyph.GT_SEEPAGE_FLOWNET;
			case "gt_rock_burst_spalling" -> Glyph.GT_ROCK_BURST_SPALLING;
			case "gl_strike_dip_mapping" -> Glyph.GL_STRIKE_DIP_MAPPING;
			case "gl_diamond_core_drilling" -> Glyph.GL_DIAMOND_CORE_DRILLING;
			case "gl_thin_section_petrography" -> Glyph.GL_THIN_SECTION_PETROGRAPHY;
			case "gl_stratigraphic_logging" -> Glyph.GL_STRATIGRAPHIC_LOGGING;
			case "gl_structural_stereonet" -> Glyph.GL_STRUCTURAL_STEREONET;
			case "gl_block_model_3d" -> Glyph.GL_BLOCK_MODEL_3D;
			case "gl_wireframe_mesh" -> Glyph.GL_WIREFRAME_MESH;
			case "gl_faulted_stratigraphy" -> Glyph.GL_FAULTED_STRATIGRAPHY;
			case "gl_folded_anticline_model" -> Glyph.GL_FOLDED_ANTICLINE_MODEL;
			case "gl_intrusive_pluton_model" -> Glyph.GL_INTRUSIVE_PLUTON_MODEL;
			case "gl_plate_subduction" -> Glyph.GL_PLATE_SUBDUCTION;
			case "gl_fault_slip_tectonics" -> Glyph.GL_FAULT_SLIP_TECTONICS;
			case "gl_sedimentation_deposition" -> Glyph.GL_SEDIMENTATION_DEPOSITION;
			case "gl_metamorphism_pt" -> Glyph.GL_METAMORPHISM_PT;
			case "gl_weathering_erosion" -> Glyph.GL_WEATHERING_EROSION;
			case "gc_soil_stream_sampling" -> Glyph.GC_SOIL_STREAM_SAMPLING;
			case "gc_pxrf_analyzer" -> Glyph.GC_PXRF_ANALYZER;
			case "gc_icp_ms_spectrometry" -> Glyph.GC_ICP_MS_SPECTROMETRY;
			case "gc_fire_assay" -> Glyph.GC_FIRE_ASSAY;
			case "gc_isotope_ratio_analysis" -> Glyph.GC_ISOTOPE_RATIO_ANALYSIS;
			case "gc_alteration_zonation" -> Glyph.GC_ALTERATION_ZONATION;
			case "gc_geochem_anomaly_contours" -> Glyph.GC_GEOCHEM_ANOMALY_CONTOURS;
			case "gc_ternary_classification" -> Glyph.GC_TERNARY_CLASSIFICATION;
			case "gc_eh_ph_pourbaix" -> Glyph.GC_EH_PH_POURBAIX;
			case "gc_downhole_geochem_log" -> Glyph.GC_DOWNHOLE_GEOCHEM_LOG;
			case "gc_hydrothermal_circulation" -> Glyph.GC_HYDROTHERMAL_CIRCULATION;
			case "gc_supergene_leaching" -> Glyph.GC_SUPERGENE_LEACHING;
			case "gc_redox_front_roll" -> Glyph.GC_REDOX_FRONT_ROLL;
			case "gc_magmatic_differentiation" -> Glyph.GC_MAGMATIC_DIFFERENTIATION;
			case "gc_element_dispersion_halo" -> Glyph.GC_ELEMENT_DISPERSION_HALO;
			case "gp_self_potential" -> Glyph.GP_SELF_POTENTIAL;
			case "gp_magnetotellurics_mt" -> Glyph.GP_MAGNETOTELLURICS_MT;
			case "gp_ground_penetrating_radar" -> Glyph.GP_GROUND_PENETRATING_RADAR;
			case "gp_radiometrics_gamma" -> Glyph.GP_RADIOMETRICS_GAMMA;
			case "gp_nmr_sounding" -> Glyph.GP_NMR_SOUNDING;
			case "gp_thermal_geothermal" -> Glyph.GP_THERMAL_GEOTHERMAL;
			case "gp_acoustics_sonar" -> Glyph.GP_ACOUSTICS_SONAR;
			case "gp_geodesy_insar_gnss" -> Glyph.GP_GEODESY_INSAR_GNSS;
			case "gp_remote_sensing_hyperspectral" -> Glyph.GP_REMOTE_SENSING_HYPERSPECTRAL;
			case "gp_matrix_mixing_bounds" -> Glyph.GP_MATRIX_MIXING_BOUNDS;
			case "gp_pore_fluid_archie" -> Glyph.GP_PORE_FLUID_ARCHIE;
			case "gp_ip_cole_cole" -> Glyph.GP_IP_COLE_COLE;
			case "gp_dielectric_permittivity" -> Glyph.GP_DIELECTRIC_PERMITTIVITY;
			case "gp_koenigsberger_remanence" -> Glyph.GP_KOENIGSBERGER_REMANENCE;
			case "gp_gassmann_fluid_sub" -> Glyph.GP_GASSMANN_FLUID_SUB;
			case "gp_permeability_kozeny" -> Glyph.GP_PERMEABILITY_KOZENY;
			case "gt_deere_rqd" -> Glyph.GT_DEERE_RQD;
			case "gt_barton_q_tunnel" -> Glyph.GT_BARTON_Q_TUNNEL;
			case "gt_bieniawski_rmr" -> Glyph.GT_BIENIAWSKI_RMR;
			case "gt_hoek_brown_criterion" -> Glyph.GT_HOEK_BROWN_CRITERION;
			case "gt_ucs_from_velocity" -> Glyph.GT_UCS_FROM_VELOCITY;
			case "gt_brittleness_index" -> Glyph.GT_BRITTLENESS_INDEX;
			case "gl_rock_type_igneous" -> Glyph.GL_ROCK_TYPE_IGNEOUS;
			case "gl_rock_type_sedimentary" -> Glyph.GL_ROCK_TYPE_SEDIMENTARY;
			case "gl_rock_type_metamorphic" -> Glyph.GL_ROCK_TYPE_METAMORPHIC;
			case "gl_composition_category" -> Glyph.GL_COMPOSITION_CATEGORY;
			case "gl_genetic_category" -> Glyph.GL_GENETIC_CATEGORY;
			case "gl_metamorphic_facies_pt" -> Glyph.GL_METAMORPHIC_FACIES_PT;
			case "gl_consolidation_degree" -> Glyph.GL_CONSOLIDATION_DEGREE;
			case "gl_deformation_brittle_ductile" -> Glyph.GL_DEFORMATION_BRITTLE_DUCTILE;
			case "gl_unit_morphology" -> Glyph.GL_UNIT_MORPHOLOGY;
			case "gl_style_disseminated" -> Glyph.GL_STYLE_DISSEMINATED;
			case "gl_style_net_textured" -> Glyph.GL_STYLE_NET_TEXTURED;
			case "gl_style_massive_sulfide" -> Glyph.GL_STYLE_MASSIVE_SULFIDE;
			case "gl_style_veined_stringer" -> Glyph.GL_STYLE_VEINED_STRINGER;
			case "gl_particle_shape_roundness" -> Glyph.GL_PARTICLE_SHAPE_ROUNDNESS;
			case "gl_contact_unconformity" -> Glyph.GL_CONTACT_UNCONFORMITY;
			case "gl_foliation_lineation" -> Glyph.GL_FOLIATION_LINEATION;
			case "gl_borehole_drilling_methods" -> Glyph.GL_BOREHOLE_DRILLING_METHODS;
			case "gl_planar_polarity_overturned" -> Glyph.GL_PLANAR_POLARITY_OVERTURNED;
			case "gm_acid_rock_drainage" -> Glyph.GM_ACID_ROCK_DRAINAGE;
			case "gm_comminution_work_index" -> Glyph.GM_COMMINUTION_WORK_INDEX;
			case "gm_flotation_recovery" -> Glyph.GM_FLOTATION_RECOVERY;
			case "gc_melt_chemistry_f02" -> Glyph.GC_MELT_CHEMISTRY_F02;
			case "gc_carbon_mineralisation" -> Glyph.GC_CARBON_MINERALISATION;
			case "gl_lithology_tensor_anisotropy" -> Glyph.GL_LITHOLOGY_TENSOR_ANISOTROPY;
			case "gl_fault_normal_graben" -> Glyph.GL_FAULT_NORMAL_GRABEN;
			case "gl_fault_thrust_ramp" -> Glyph.GL_FAULT_THRUST_RAMP;
			case "gl_fault_strike_slip_dextral" -> Glyph.GL_FAULT_STRIKE_SLIP_DEXTRAL;
			case "gl_shear_zone_sigmoidal" -> Glyph.GL_SHEAR_ZONE_SIGMOIDAL;
			case "gl_chevron_kink_fold" -> Glyph.GL_CHEVRON_KINK_FOLD;
			case "gl_ptygmatic_vein_fold" -> Glyph.GL_PTYGMATIC_VEIN_FOLD;
			case "gl_columnar_jointing" -> Glyph.GL_COLUMNAR_JOINTING;
			case "gl_spinifex_texture" -> Glyph.GL_SPINIFEX_TEXTURE;
			case "gl_pillow_lava" -> Glyph.GL_PILLOW_LAVA;
			case "gl_fiamme_ignimbrite" -> Glyph.GL_FIAMME_IGNIMBRITE;
			case "gl_banded_iron_formation" -> Glyph.GL_BANDED_IRON_FORMATION;
			case "gl_hydrothermal_breccia" -> Glyph.GL_HYDROTHERMAL_BRECCIA;
			case "gl_potassic_alteration" -> Glyph.GL_POTASSIC_ALTERATION;
			case "gl_phyllic_sericitic_alteration" -> Glyph.GL_PHYLLIC_SERICITIC_ALTERATION;
			case "gl_advanced_argillic" -> Glyph.GL_ADVANCED_ARGILLIC;
			case "gl_propylitic_chlorite_epidote" -> Glyph.GL_PROPYLITIC_CHLORITE_EPIDOTE;
			case "gl_serpentinite_mesh" -> Glyph.GL_SERPENTINITE_MESH;
			case "gl_skarn_calc_silicate" -> Glyph.GL_SKARN_CALC_SILICATE;
			case "gl_greisen_cassiterite" -> Glyph.GL_GREISEN_CASSITERITE;
			case "gl_tourmaline_sun_rosette" -> Glyph.GL_TOURMALINE_SUN_ROSETTE;
			case "gl_turbidite_bouma_sequence" -> Glyph.GL_TURBIDITE_BOUMA_SEQUENCE;
			case "gl_fluvial_point_bar_channel" -> Glyph.GL_FLUVIAL_POINT_BAR_CHANNEL;
			case "gc_la_icp_ms_laser" -> Glyph.GC_LA_ICP_MS_LASER;
			case "gc_epma_wds_microprobe" -> Glyph.GC_EPMA_WDS_MICROPROBE;
			case "gc_xrd_diffractometer" -> Glyph.GC_XRD_DIFFRACTOMETER;
			case "gc_xanes_synchrotron" -> Glyph.GC_XANES_SYNCHROTRON;
			case "gc_libs_laser_plasma" -> Glyph.GC_LIBS_LASER_PLASMA;
			case "gc_ftir_raman_spectroscopy" -> Glyph.GC_FTIR_RAMAN_SPECTROSCOPY;
			case "gc_four_acid_total_digest" -> Glyph.GC_FOUR_ACID_TOTAL_DIGEST;
			case "gc_aqua_regia_partial_digest" -> Glyph.GC_AQUA_REGIA_PARTIAL_DIGEST;
			case "gc_cyanide_bottle_roll" -> Glyph.GC_CYANIDE_BOTTLE_ROLL;
			case "gc_sequential_extraction" -> Glyph.GC_SEQUENTIAL_EXTRACTION;
			case "gc_gas_chromatography_ms" -> Glyph.GC_GAS_CHROMATOGRAPHY_MS;
			case "gc_sims_shrimp_microprobe" -> Glyph.GC_SIMS_SHRIMP_MICROPROBE;
			case "gc_tims_thermal_ionization" -> Glyph.GC_TIMS_THERMAL_IONIZATION;
			case "gc_stable_isotope_gas_irms" -> Glyph.GC_STABLE_ISOTOPE_GAS_IRMS;
			case "gc_fluid_inclusion_microtherm" -> Glyph.GC_FLUID_INCLUSION_MICROTHERM;
			case "gc_radon_emanometry" -> Glyph.GC_RADON_EMANOMETRY;
			case "gc_biogeochem_vegetation" -> Glyph.GC_BIOGEOCHEM_VEGETATION;
			case "gc_ree_chondrite_spidergram" -> Glyph.GC_REE_CHONDRITE_SPIDERGRAM;
			case "gc_primitive_mantle_spidergram" -> Glyph.GC_PRIMITIVE_MANTLE_SPIDERGRAM;
			case "gc_tas_volcanic_diagram" -> Glyph.GC_TAS_VOLCANIC_DIAGRAM;
			case "gc_qapf_ternary_double" -> Glyph.GC_QAPF_TERNARY_DOUBLE;
			case "gc_pearce_tectonic_discrimination" -> Glyph.GC_PEARCE_TECTONIC_DISCRIMINATION;
			case "gc_activity_activity_diagram" -> Glyph.GC_ACTIVITY_ACTIVITY_DIAGRAM;
			case "gc_zircon_upb_concordia" -> Glyph.GC_ZIRCON_UPB_CONCORDIA;
			case "gc_rb_sr_isochron_diagram" -> Glyph.GC_RB_SR_ISOCHRON_DIAGRAM;
			case "gc_sulfur_isotope_delta34s" -> Glyph.GC_SULFUR_ISOTOPE_DELTA34S;
			case "gc_swir_mineral_spectral_trough" -> Glyph.GC_SWIR_MINERAL_SPECTRAL_TROUGH;
			case "gc_campbell_vectoring_ratio" -> Glyph.GC_CAMPBELL_VECTORING_RATIO;
			case "gc_alumina_saturation_asi" -> Glyph.GC_ALUMINA_SATURATION_ASI;
			case "gc_harker_variation_diagram" -> Glyph.GC_HARKER_VARIATION_DIAGRAM;
			case "gc_water_solubility_melt" -> Glyph.GC_WATER_SOLUBILITY_MELT;
			case "gc_oxygen_isotope_delta18o" -> Glyph.GC_OXYGEN_ISOTOPE_DELTA18O;
			case "gc_hydrothermal_boiling_immiscibility" -> Glyph.GC_HYDROTHERMAL_BOILING_IMMISCIBILITY;
			case "gc_sulfide_melt_immiscibility" -> Glyph.GC_SULFIDE_MELT_IMMISCIBILITY;
			case "gc_fluid_rock_metasomatism" -> Glyph.GC_FLUID_ROCK_METASOMATISM;
			case "gc_bacterial_sulfate_reduction" -> Glyph.GC_BACTERIAL_SULFATE_REDUCTION;
			case "gc_heavy_mineral_placer" -> Glyph.GC_HEAVY_MINERAL_PLACER;
			case "gc_gossan_boxwork_weathering" -> Glyph.GC_GOSSAN_BOXWORK_WEATHERING;
			case "gc_fumarolic_gas_exsolution" -> Glyph.GC_FUMAROLIC_GAS_EXSOLUTION;
			case "gc_clay_adsorption_cec" -> Glyph.GC_CLAY_ADSORPTION_CEC;
			case "gc_metal_chloride_complexation" -> Glyph.GC_METAL_CHLORIDE_COMPLEXATION;
			case "gc_hydrocarbon_catagenesis" -> Glyph.GC_HYDROCARBON_CATAGENESIS;
			case "gc_colloid_flocculation" -> Glyph.GC_COLLOID_FLOCCULATION;
			case "gc_gibbs_free_energy" -> Glyph.GC_GIBBS_FREE_ENERGY;
			case "gc_chemical_elements" -> Glyph.GC_CHEMICAL_ELEMENTS;
			case "gl_minerals_specimen" -> Glyph.GL_MINERALS_SPECIMEN;
			case "gc_element_diff_wtpct" -> Glyph.GC_ELEMENT_DIFF_WTPCT;
			case "gc_temperature_thermo" -> Glyph.GC_TEMPERATURE_THERMO;
			case "gc_pressure_gauge" -> Glyph.GC_PRESSURE_GAUGE;
			case "gc_gradient_perturbation_factor" -> Glyph.GC_GRADIENT_PERTURBATION_FACTOR;
			case "gc_l1_norm_regularization" -> Glyph.GC_L1_NORM_REGULARIZATION;
			case "gc_n_iterations_loop" -> Glyph.GC_N_ITERATIONS_LOOP;
			case "gc_thermodynamics_system" -> Glyph.GC_THERMODYNAMICS_SYSTEM;
			case "gp_petrophysics_core_matrix" -> Glyph.GP_PETROPHYSICS_CORE_MATRIX;
			case "gl_positions_spatial_coords" -> Glyph.GL_POSITIONS_SPATIAL_COORDS;
			case "gc_volatiles_degassing" -> Glyph.GC_VOLATILES_DEGASSING;
			case "gc_water_activity_ah2o" -> Glyph.GC_WATER_ACTIVITY_AH2O;
			case "gc_fluid_xco2_mole_fraction" -> Glyph.GC_FLUID_XCO2_MOLE_FRACTION;
			case "gc_oxygen_fugacity_fo2" -> Glyph.GC_OXYGEN_FUGACITY_FO2;
			case "gc_major_element_oxides" -> Glyph.GC_MAJOR_ELEMENT_OXIDES;
			case "gc_gradient_initial_step" -> Glyph.GC_GRADIENT_INITIAL_STEP;
			case "gc_sensitivity_jacobian" -> Glyph.GC_SENSITIVITY_JACOBIAN;
			case "gp_specific_gravity_balance" -> Glyph.GP_SPECIFIC_GRAVITY_BALANCE;
			case "gc_log_error_residuals" -> Glyph.GC_LOG_ERROR_RESIDUALS;
			case "gl_geological_tagging_domain" -> Glyph.GL_GEOLOGICAL_TAGGING_DOMAIN;
			case "gp_airborne_em_aem" -> Glyph.GP_AIRBORNE_EM_AEM;
			case "gp_fixed_wing_aem" -> Glyph.GP_FIXED_WING_AEM;
			case "gp_frequency_domain_em_fdem" -> Glyph.GP_FREQUENCY_DOMAIN_EM_FDEM;
			case "gp_time_domain_em_tdem" -> Glyph.GP_TIME_DOMAIN_EM_TDEM;
			case "gp_csem_marine" -> Glyph.GP_CSEM_MARINE;
			case "gp_csem_land" -> Glyph.GP_CSEM_LAND;
			case "gp_csamt" -> Glyph.GP_CSAMT;
			case "gp_ground_tem" -> Glyph.GP_GROUND_TEM;
			case "gp_tem_fixed_loop" -> Glyph.GP_TEM_FIXED_LOOP;
			case "gp_tem_moving_loop" -> Glyph.GP_TEM_MOVING_LOOP;
			case "gp_tem_central_loop" -> Glyph.GP_TEM_CENTRAL_LOOP;
			case "gp_tem_in_loop" -> Glyph.GP_TEM_IN_LOOP;
			case "gp_tem_lotem" -> Glyph.GP_TEM_LOTEM;
			case "gp_loupe_tem" -> Glyph.GP_LOUPE_TEM;
			case "gp_vtem" -> Glyph.GP_VTEM;
			case "gp_skytem" -> Glyph.GP_SKYTEM;
			case "gp_slingram_em" -> Glyph.GP_SLINGRAM_EM;
			case "gp_vlf_em" -> Glyph.GP_VLF_EM;
			case "gp_airborne_magnetics" -> Glyph.GP_AIRBORNE_MAGNETICS;
			case "gp_ground_magnetics" -> Glyph.GP_GROUND_MAGNETICS;
			case "gp_magnetic_gradiometry" -> Glyph.GP_MAGNETIC_GRADIOMETRY;
			case "gp_electrical_ip_chargeability" -> Glyph.GP_ELECTRICAL_IP_CHARGEABILITY;
			case "gp_ip_spectral" -> Glyph.GP_IP_SPECTRAL;
			case "gp_tem_decay_gates" -> Glyph.GP_TEM_DECAY_GATES;
			case "gp_gpr_b_scan" -> Glyph.GP_GPR_B_SCAN;
			case "gp_gpr_time_slice" -> Glyph.GP_GPR_TIME_SLICE;
			case "gp_gpr_volume_3d" -> Glyph.GP_GPR_VOLUME_3D;
			case "gp_gpr_cmp_velocity" -> Glyph.GP_GPR_CMP_VELOCITY;
			case "gp_gpr_utility_detection" -> Glyph.GP_GPR_UTILITY_DETECTION;
			case "gp_gpr_concrete_rebar" -> Glyph.GP_GPR_CONCRETE_REBAR;
			case "gp_gpr_borehole" -> Glyph.GP_GPR_BOREHOLE;
			case "gp_gpr_antenna" -> Glyph.GP_GPR_ANTENNA;
			case "gp_radiometrics_total" -> Glyph.GP_RADIOMETRICS_TOTAL;
			case "gp_radiometrics_potassium_k" -> Glyph.GP_RADIOMETRICS_POTASSIUM_K;
			case "gp_radiometrics_uranium_u" -> Glyph.GP_RADIOMETRICS_URANIUM_U;
			case "gp_radiometrics_thorium_th" -> Glyph.GP_RADIOMETRICS_THORIUM_TH;
			case "gp_radiometrics_ternary" -> Glyph.GP_RADIOMETRICS_TERNARY;
			case "gp_airborne_radiometrics" -> Glyph.GP_AIRBORNE_RADIOMETRICS;
			case "gp_seismic_crosshole" -> Glyph.GP_SEISMIC_CROSSHOLE;
			case "gp_seismic_downhole" -> Glyph.GP_SEISMIC_DOWNHOLE;
			case "gp_seismic_uphole" -> Glyph.GP_SEISMIC_UPHOLE;
			case "gp_seismic_vsp" -> Glyph.GP_SEISMIC_VSP;
			case "gp_seismic_refraction" -> Glyph.GP_SEISMIC_REFRACTION;
			case "gp_seismic_masw" -> Glyph.GP_SEISMIC_MASW;
			case "gp_seismic_hvsr" -> Glyph.GP_SEISMIC_HVSR;
			case "gp_borehole_em_bhem" -> Glyph.GP_BOREHOLE_EM_BHEM;
			case "gp_borehole_induction_log" -> Glyph.GP_BOREHOLE_INDUCTION_LOG;
			case "gp_borehole_resistivity_log" -> Glyph.GP_BOREHOLE_RESISTIVITY_LOG;
			case "gp_borehole_ip_log" -> Glyph.GP_BOREHOLE_IP_LOG;
			case "gp_borehole_sp_log" -> Glyph.GP_BOREHOLE_SP_LOG;
			case "gp_borehole_magnetic_susceptibility" -> Glyph.GP_BOREHOLE_MAGNETIC_SUSCEPTIBILITY;
			case "gp_borehole_magnetometer" -> Glyph.GP_BOREHOLE_MAGNETOMETER;
			case "gp_borehole_natural_gamma" -> Glyph.GP_BOREHOLE_NATURAL_GAMMA;
			case "gp_borehole_spectral_gamma" -> Glyph.GP_BOREHOLE_SPECTRAL_GAMMA;
			case "gp_borehole_density_log" -> Glyph.GP_BOREHOLE_DENSITY_LOG;
			case "gp_borehole_neutron_porosity" -> Glyph.GP_BOREHOLE_NEUTRON_POROSITY;
			case "gp_borehole_sonic_log" -> Glyph.GP_BOREHOLE_SONIC_LOG;
			case "gp_borehole_acoustic_televiewer" -> Glyph.GP_BOREHOLE_ACOUSTIC_TELEVIEWER;
			case "gp_borehole_optical_televiewer" -> Glyph.GP_BOREHOLE_OPTICAL_TELEVIEWER;
			case "gp_borehole_caliper" -> Glyph.GP_BOREHOLE_CALIPER;
			case "gp_borehole_temperature" -> Glyph.GP_BOREHOLE_TEMPERATURE;
			case "gp_borehole_fluid_conductivity" -> Glyph.GP_BOREHOLE_FLUID_CONDUCTIVITY;
			case "gp_borehole_flowmeter" -> Glyph.GP_BOREHOLE_FLOWMETER;
			case "gp_borehole_nmr" -> Glyph.GP_BOREHOLE_NMR;
			case "gp_borehole_gravity" -> Glyph.GP_BOREHOLE_GRAVITY;
			case "gp_crosshole_ert" -> Glyph.GP_CROSSHOLE_ERT;
			case "gp_crosshole_em_tomography" -> Glyph.GP_CROSSHOLE_EM_TOMOGRAPHY;
			case "gp_crosshole_seismic_tomography" -> Glyph.GP_CROSSHOLE_SEISMIC_TOMOGRAPHY;
			case "gp_property_conductivity" -> Glyph.GP_PROPERTY_CONDUCTIVITY;
			case "gp_property_resistivity" -> Glyph.GP_PROPERTY_RESISTIVITY;
			case "gp_property_density" -> Glyph.GP_PROPERTY_DENSITY;
			case "gp_property_magnetic_susceptibility" -> Glyph.GP_PROPERTY_MAGNETIC_SUSCEPTIBILITY;
			case "gp_property_remanent_magnetization" -> Glyph.GP_PROPERTY_REMANENT_MAGNETIZATION;
			case "gp_property_chargeability" -> Glyph.GP_PROPERTY_CHARGEABILITY;
			case "gp_property_vp" -> Glyph.GP_PROPERTY_VP;
			case "gp_property_vs" -> Glyph.GP_PROPERTY_VS;
			case "gp_property_porosity" -> Glyph.GP_PROPERTY_POROSITY;
			case "gp_property_permeability" -> Glyph.GP_PROPERTY_PERMEABILITY;
			case "gp_property_dielectric_permittivity" -> Glyph.GP_PROPERTY_DIELECTRIC_PERMITTIVITY;
			case "gp_property_thermal_conductivity" -> Glyph.GP_PROPERTY_THERMAL_CONDUCTIVITY;
			case "gp_electric_field" -> Glyph.GP_ELECTRIC_FIELD;
			case "gp_electric_field_x" -> Glyph.GP_ELECTRIC_FIELD_X;
			case "gp_electric_field_y" -> Glyph.GP_ELECTRIC_FIELD_Y;
			case "gp_electric_field_z" -> Glyph.GP_ELECTRIC_FIELD_Z;
			case "gp_magnetic_field" -> Glyph.GP_MAGNETIC_FIELD;
			case "gp_magnetic_field_x" -> Glyph.GP_MAGNETIC_FIELD_X;
			case "gp_magnetic_field_y" -> Glyph.GP_MAGNETIC_FIELD_Y;
			case "gp_magnetic_field_z" -> Glyph.GP_MAGNETIC_FIELD_Z;
			case "gp_poynting_vector" -> Glyph.GP_POYNTING_VECTOR;
			case "gp_signal_spectrum" -> Glyph.GP_SIGNAL_SPECTRUM;
			case "gp_fft_transform" -> Glyph.GP_FFT_TRANSFORM;
			case "gp_signal_spectrogram" -> Glyph.GP_SIGNAL_SPECTROGRAM;
			case "gp_raw_waveform" -> Glyph.GP_RAW_WAVEFORM;
			case "gp_cross_power" -> Glyph.GP_CROSS_POWER;
			case "gp_signal_coherence" -> Glyph.GP_SIGNAL_COHERENCE;
			case "gp_sensor_calibration" -> Glyph.GP_SENSOR_CALIBRATION;
			case "gp_remote_reference" -> Glyph.GP_REMOTE_REFERENCE;
			case "gp_mt_impedance_tensor" -> Glyph.GP_MT_IMPEDANCE_TENSOR;
			case "gp_mt_phase_tensor" -> Glyph.GP_MT_PHASE_TENSOR;
			case "gp_mt_tipper" -> Glyph.GP_MT_TIPPER;
			case "gc_geochemical_vectoring" -> Glyph.GC_GEOCHEMICAL_VECTORING;
			case "gc_hydrothermal_alteration" -> Glyph.GC_HYDROTHERMAL_ALTERATION;
			case "gc_magmatic_intrusion" -> Glyph.GC_MAGMATIC_INTRUSION;
			case "gc_dehydration" -> Glyph.GC_DEHYDRATION;
			case "gc_reducing_environment" -> Glyph.GC_REDUCING_ENVIRONMENT;
			case "gc_oxidizing_environment" -> Glyph.GC_OXIDIZING_ENVIRONMENT;
			case "gc_saussuritised" -> Glyph.GC_SAUSSURITISED;
			case "gc_serpentinisation" -> Glyph.GC_SERPENTINISATION;
			case "gc_epidote_alteration" -> Glyph.GC_EPIDOTE_ALTERATION;
			case "gc_silicification" -> Glyph.GC_SILICIFICATION;
			case "gc_carbonate_alteration" -> Glyph.GC_CARBONATE_ALTERATION;
			case "gc_calcsilicate_alteration" -> Glyph.GC_CALCSILICATE_ALTERATION;
			case "gc_greisen" -> Glyph.GC_GREISEN;
			case "gc_albitic_alteration" -> Glyph.GC_ALBITIC_ALTERATION;
			case "gc_advanced_argillic_alteration" -> Glyph.GC_ADVANCED_ARGILLIC_ALTERATION;
			case "gc_not_altered" -> Glyph.GC_NOT_ALTERED;
			case "gc_chloritic_alteration" -> Glyph.GC_CHLORITIC_ALTERATION;
			case "gc_zeolitic_alteration" -> Glyph.GC_ZEOLITIC_ALTERATION;
			case "gc_propylitic_alteration" -> Glyph.GC_PROPYLITIC_ALTERATION;
			case "gc_potassic_alteration" -> Glyph.GC_POTASSIC_ALTERATION;
			case "gc_alteration_not_specified" -> Glyph.GC_ALTERATION_NOT_SPECIFIED;
			case "gc_kaolinitic_alteration" -> Glyph.GC_KAOLINITIC_ALTERATION;
			case "gc_sericitic_alteration" -> Glyph.GC_SERICITIC_ALTERATION;
			case "gc_argillic_alteration" -> Glyph.GC_ARGILLIC_ALTERATION;
			case "gc_alunitic_alteration" -> Glyph.GC_ALUNITIC_ALTERATION;
			case "gc_hematitic_alteration" -> Glyph.GC_HEMATITIC_ALTERATION;
			case "gc_pyritic_alteration" -> Glyph.GC_PYRITIC_ALTERATION;
			case "gc_deuteric_alteration" -> Glyph.GC_DEUTERIC_ALTERATION;
			case "gc_uralitisation" -> Glyph.GC_URALITISATION;
			case "gc_red_rock_alteration" -> Glyph.GC_RED_ROCK_ALTERATION;
			case "gl_granite_post_kinematic" -> Glyph.GL_GRANITE_POST_KINEMATIC;
			case "gl_granite_late_post_kinematic" -> Glyph.GL_GRANITE_LATE_POST_KINEMATIC;
			case "gl_granite_syn_late_kinematic" -> Glyph.GL_GRANITE_SYN_LATE_KINEMATIC;
			case "gl_granite_syn_kinematic_foliated" -> Glyph.GL_GRANITE_SYN_KINEMATIC_FOLIATED;
			case "gl_granite_gneissic_anatectic" -> Glyph.GL_GRANITE_GNEISSIC_ANATECTIC;
			case "gl_gabbro_diorite_orogenic" -> Glyph.GL_GABBRO_DIORITE_OROGENIC;
			case "gl_porphyry_pattern" -> Glyph.GL_PORPHYRY_PATTERN;
			case "gl_island_arc_volcanics" -> Glyph.GL_ISLAND_ARC_VOLCANICS;
			case "gl_felsic_volcanics_rare_basics" -> Glyph.GL_FELSIC_VOLCANICS_RARE_BASICS;
			case "gl_rhyolite_dacite_volcanics" -> Glyph.GL_RHYOLITE_DACITE_VOLCANICS;
			case "gl_felsic_volcanics_with_granite" -> Glyph.GL_FELSIC_VOLCANICS_WITH_GRANITE;
			case "gl_flood_basalt" -> Glyph.GL_FLOOD_BASALT;
			case "gl_dolerite_granophyre" -> Glyph.GL_DOLERITE_GRANOPHYRE;
			case "gl_keratophyre" -> Glyph.GL_KERATOPHYRE;
			case "gl_granite_intruding_craton" -> Glyph.GL_GRANITE_INTRUDING_CRATON;
			case "gl_layered_intrusion" -> Glyph.GL_LAYERED_INTRUSION;
			case "gl_alkaline_intrusive" -> Glyph.GL_ALKALINE_INTRUSIVE;
			case "gl_kimberlite_lamproite" -> Glyph.GL_KIMBERLITE_LAMPROITE;
			case "gl_carbonatite" -> Glyph.GL_CARBONATITE;
			case "gl_slate_phyllite" -> Glyph.GL_SLATE_PHYLLITE;
			case "gl_schist_gneiss_high_grade" -> Glyph.GL_SCHIST_GNEISS_HIGH_GRADE;
			case "gl_sandy_slate_interbedded" -> Glyph.GL_SANDY_SLATE_INTERBEDDED;
			case "gl_hornfels_massive" -> Glyph.GL_HORNFELS_MASSIVE;
			case "gl_basic_plutonic_hypabyssal" -> Glyph.GL_BASIC_PLUTONIC_HYPABYSSAL;
			case "gl_bedded_lavas" -> Glyph.GL_BEDDED_LAVAS;
			case "gl_tuff_tuffaceous_sandstone" -> Glyph.GL_TUFF_TUFFACEOUS_SANDSTONE;
			case "gl_bedded_tuff" -> Glyph.GL_BEDDED_TUFF;
			case "gl_breccia_pattern" -> Glyph.GL_BRECCIA_PATTERN;
			case "gl_scree_brecciated_rock" -> Glyph.GL_SCREE_BRECCIATED_ROCK;
			case "gl_soil_cover" -> Glyph.GL_SOIL_COVER;
			case "gl_alluvium" -> Glyph.GL_ALLUVIUM;
			case "gl_gossan_ore" -> Glyph.GL_GOSSAN_ORE;
			case "gl_conglomerate_pattern" -> Glyph.GL_CONGLOMERATE_PATTERN;
			case "gl_sandstone_pattern" -> Glyph.GL_SANDSTONE_PATTERN;
			case "gl_pebbly_sandstone" -> Glyph.GL_PEBBLY_SANDSTONE;
			case "gl_cross_bedded_sandstone" -> Glyph.GL_CROSS_BEDDED_SANDSTONE;
			case "gl_limestone_pattern" -> Glyph.GL_LIMESTONE_PATTERN;
			case "gl_dolomite_pattern" -> Glyph.GL_DOLOMITE_PATTERN;
			case "gl_sandy_limestone" -> Glyph.GL_SANDY_LIMESTONE;
			case "gl_shale_pattern" -> Glyph.GL_SHALE_PATTERN;
			case "gl_sandy_shale" -> Glyph.GL_SANDY_SHALE;
			case "gl_bedded_chert" -> Glyph.GL_BEDDED_CHERT;
			case "gl_massive_chert" -> Glyph.GL_MASSIVE_CHERT;
			case "gl_coal_undifferentiated" -> Glyph.GL_COAL_UNDIFFERENTIATED;
			case "gl_broken_coal" -> Glyph.GL_BROKEN_COAL;
			case "gl_coal_with_shale_bands" -> Glyph.GL_COAL_WITH_SHALE_BANDS;
			case "gl_shale_with_coal_bands" -> Glyph.GL_SHALE_WITH_COAL_BANDS;
			case "gl_cannel_coal" -> Glyph.GL_CANNEL_COAL;
			case "gl_cannel_shale" -> Glyph.GL_CANNEL_SHALE;
			case "gl_carbonaceous_shale" -> Glyph.GL_CARBONACEOUS_SHALE;
			case "gl_brown_coal" -> Glyph.GL_BROWN_COAL;
			case "gl_oil_shale" -> Glyph.GL_OIL_SHALE;
			case "gl_thin_seam" -> Glyph.GL_THIN_SEAM;
			case "gl_coal_bright" -> Glyph.GL_COAL_BRIGHT;
			case "gl_coal_bright_dull_bands" -> Glyph.GL_COAL_BRIGHT_DULL_BANDS;
			case "gl_coal_interbanded" -> Glyph.GL_COAL_INTERBANDED;
			case "gl_coal_dull_bright_bands" -> Glyph.GL_COAL_DULL_BRIGHT_BANDS;
			case "gl_coal_dull_minor_bright" -> Glyph.GL_COAL_DULL_MINOR_BRIGHT;
			case "gl_coal_dull" -> Glyph.GL_COAL_DULL;
			case "gl_coal_canneloid" -> Glyph.GL_COAL_CANNELOID;
			case "gl_coal_fibrous" -> Glyph.GL_COAL_FIBROUS;
			case "gl_coal_weathered" -> Glyph.GL_COAL_WEATHERED;
			case "gl_coal_heat_altered" -> Glyph.GL_COAL_HEAT_ALTERED;
			case "gl_non_coal" -> Glyph.GL_NON_COAL;
			case "gl_coal_interlayered_non_coal" -> Glyph.GL_COAL_INTERLAYERED_NON_COAL;
			case "gl_non_coal_interlayered_coal" -> Glyph.GL_NON_COAL_INTERLAYERED_COAL;
			case "gl_stony_coal" -> Glyph.GL_STONY_COAL;
			case "gl_mudstone_pattern" -> Glyph.GL_MUDSTONE_PATTERN;
			case "gl_coal_seam_log" -> Glyph.GL_COAL_SEAM_LOG;
			case "gl_fold_upright_horizontal" -> Glyph.GL_FOLD_UPRIGHT_HORIZONTAL;
			case "gl_fold_upright_plunging" -> Glyph.GL_FOLD_UPRIGHT_PLUNGING;
			case "gl_fold_vertical" -> Glyph.GL_FOLD_VERTICAL;
			case "gl_fold_inclined_plunging" -> Glyph.GL_FOLD_INCLINED_PLUNGING;
			case "gl_fold_overturned_horizontal" -> Glyph.GL_FOLD_OVERTURNED_HORIZONTAL;
			case "gl_fold_overturned_plunging" -> Glyph.GL_FOLD_OVERTURNED_PLUNGING;
			case "gl_fold_recumbent" -> Glyph.GL_FOLD_RECUMBENT;
			case "gl_fold_reclined" -> Glyph.GL_FOLD_RECLINED;
			case "gl_monocline" -> Glyph.GL_MONOCLINE;
			case "gl_fold_vergence" -> Glyph.GL_FOLD_VERGENCE;
			case "gl_superposed_folds" -> Glyph.GL_SUPERPOSED_FOLDS;
			case "gl_fold_class_1a" -> Glyph.GL_FOLD_CLASS_1A;
			case "gl_fold_class_1b" -> Glyph.GL_FOLD_CLASS_1B;
			case "gl_fold_class_1c" -> Glyph.GL_FOLD_CLASS_1C;
			case "gl_fold_class_2" -> Glyph.GL_FOLD_CLASS_2;
			case "gl_fold_class_3" -> Glyph.GL_FOLD_CLASS_3;
			case "gl_dip_isogon_construction" -> Glyph.GL_DIP_ISOGON_CONSTRUCTION;
			case "gl_fold_attitude_grid" -> Glyph.GL_FOLD_ATTITUDE_GRID;
			case "gl_fold_attitude_classification" -> Glyph.GL_FOLD_ATTITUDE_CLASSIFICATION;
			case "gl_orthographic_net" -> Glyph.GL_ORTHOGRAPHIC_NET;
			case "gl_wulff_net" -> Glyph.GL_WULFF_NET;
			case "gl_schmidt_net" -> Glyph.GL_SCHMIDT_NET;
			case "gl_stereonet_contouring_device" -> Glyph.GL_STEREONET_CONTOURING_DEVICE;
			case "gl_rock_fall" -> Glyph.GL_ROCK_FALL;
			case "gl_rock_topple" -> Glyph.GL_ROCK_TOPPLE;
			case "gl_rock_slump" -> Glyph.GL_ROCK_SLUMP;
			case "gl_rock_block_slide" -> Glyph.GL_ROCK_BLOCK_SLIDE;
			case "gl_rock_lateral_spread" -> Glyph.GL_ROCK_LATERAL_SPREAD;
			case "gl_rock_creep_sackung" -> Glyph.GL_ROCK_CREEP_SACKUNG;
			case "gl_rock_fall_debris_flow" -> Glyph.GL_ROCK_FALL_DEBRIS_FLOW;
			case "gl_slump_topple" -> Glyph.GL_SLUMP_TOPPLE;
			case "gl_rock_slide_rock_fall" -> Glyph.GL_ROCK_SLIDE_ROCK_FALL;
			case "gl_debris_fall" -> Glyph.GL_DEBRIS_FALL;
			case "gl_debris_topple" -> Glyph.GL_DEBRIS_TOPPLE;
			case "gl_debris_slump" -> Glyph.GL_DEBRIS_SLUMP;
			case "gl_debris_slide" -> Glyph.GL_DEBRIS_SLIDE;
			case "gl_debris_flow" -> Glyph.GL_DEBRIS_FLOW;
			case "gl_debris_avalanche" -> Glyph.GL_DEBRIS_AVALANCHE;
			case "gl_block_stream" -> Glyph.GL_BLOCK_STREAM;
			case "gl_solifluction" -> Glyph.GL_SOLIFLUCTION;
			case "gl_soil_creep" -> Glyph.GL_SOIL_CREEP;
			case "gl_cambering_valley_bulging" -> Glyph.GL_CAMBERING_VALLEY_BULGING;
			case "gl_slump_earth_flow" -> Glyph.GL_SLUMP_EARTH_FLOW;
			case "gl_earth_fall" -> Glyph.GL_EARTH_FALL;
			case "gl_earth_topple" -> Glyph.GL_EARTH_TOPPLE;
			case "gl_earth_slump" -> Glyph.GL_EARTH_SLUMP;
			case "gl_earth_block_slide" -> Glyph.GL_EARTH_BLOCK_SLIDE;
			case "gl_earth_lateral_spread" -> Glyph.GL_EARTH_LATERAL_SPREAD;
			case "gl_wet_sand_silt_flow" -> Glyph.GL_WET_SAND_SILT_FLOW;
			case "gl_quick_clay_flow" -> Glyph.GL_QUICK_CLAY_FLOW;
			case "gl_earth_flow" -> Glyph.GL_EARTH_FLOW;
			case "gl_loess_flow" -> Glyph.GL_LOESS_FLOW;
			case "gl_dry_sand_flow" -> Glyph.GL_DRY_SAND_FLOW;
			case "gl_qapf_plutonic_diagram" -> Glyph.GL_QAPF_PLUTONIC_DIAGRAM;
			case "gl_gabbroic_plag_px_ol" -> Glyph.GL_GABBROIC_PLAG_PX_OL;
			case "gl_gabbroic_plag_px_hbl" -> Glyph.GL_GABBROIC_PLAG_PX_HBL;
			case "gl_gabbroic_plag_opx_cpx" -> Glyph.GL_GABBROIC_PLAG_OPX_CPX;
			case "gl_metamorphic_facies_diagram" -> Glyph.GL_METAMORPHIC_FACIES_DIAGRAM;
			case "gl_roundness_very_angular" -> Glyph.GL_ROUNDNESS_VERY_ANGULAR;
			case "gl_roundness_angular" -> Glyph.GL_ROUNDNESS_ANGULAR;
			case "gl_roundness_subangular" -> Glyph.GL_ROUNDNESS_SUBANGULAR;
			case "gl_roundness_subrounded" -> Glyph.GL_ROUNDNESS_SUBROUNDED;
			case "gl_roundness_rounded" -> Glyph.GL_ROUNDNESS_ROUNDED;
			case "gl_roundness_well_rounded" -> Glyph.GL_ROUNDNESS_WELL_ROUNDED;
			case "gl_grain_percent_01" -> Glyph.GL_GRAIN_PERCENT_01;
			case "gl_grain_percent_02" -> Glyph.GL_GRAIN_PERCENT_02;
			case "gl_grain_percent_03" -> Glyph.GL_GRAIN_PERCENT_03;
			case "gl_grain_percent_05" -> Glyph.GL_GRAIN_PERCENT_05;
			case "gl_grain_percent_07" -> Glyph.GL_GRAIN_PERCENT_07;
			case "gl_grain_percent_10" -> Glyph.GL_GRAIN_PERCENT_10;
			case "gl_grain_percent_15" -> Glyph.GL_GRAIN_PERCENT_15;
			case "gl_grain_percent_20" -> Glyph.GL_GRAIN_PERCENT_20;
			case "gl_grain_percent_25" -> Glyph.GL_GRAIN_PERCENT_25;
			case "gl_grain_percent_30" -> Glyph.GL_GRAIN_PERCENT_30;
			case "gl_grain_percent_40" -> Glyph.GL_GRAIN_PERCENT_40;
			case "gl_grain_percent_50" -> Glyph.GL_GRAIN_PERCENT_50;
			case "gl_unit_stratotype" -> Glyph.GL_UNIT_STRATOTYPE;
			case "gl_boundary_stratotype" -> Glyph.GL_BOUNDARY_STRATOTYPE;
			case "gl_earthquake_magnitude_energy" -> Glyph.GL_EARTHQUAKE_MAGNITUDE_ENERGY;
			case "gp_hyperspectral_lab" -> Glyph.GP_HYPERSPECTRAL_LAB;
			case "gp_hyperspectral_satellite" -> Glyph.GP_HYPERSPECTRAL_SATELLITE;
			case "gp_hyperspectral_cube" -> Glyph.GP_HYPERSPECTRAL_CUBE;
			case "gp_hyperspectral_bands" -> Glyph.GP_HYPERSPECTRAL_BANDS;
			case "gp_hyperspectral_spectrum" -> Glyph.GP_HYPERSPECTRAL_SPECTRUM;
			case "gp_hyperspectral_uv" -> Glyph.GP_HYPERSPECTRAL_UV;
			case "gp_hyperspectral_visible" -> Glyph.GP_HYPERSPECTRAL_VISIBLE;
			case "gp_hyperspectral_vnir" -> Glyph.GP_HYPERSPECTRAL_VNIR;
			case "gp_hyperspectral_nir" -> Glyph.GP_HYPERSPECTRAL_NIR;
			case "gp_hyperspectral_ir" -> Glyph.GP_HYPERSPECTRAL_IR;
			case "gp_hyperspectral_swir" -> Glyph.GP_HYPERSPECTRAL_SWIR;
			case "gp_hyperspectral_mwir" -> Glyph.GP_HYPERSPECTRAL_MWIR;
			case "gp_hyperspectral_tir" -> Glyph.GP_HYPERSPECTRAL_TIR;
			case "gp_em31" -> Glyph.GP_EM31;
			case "gp_em38" -> Glyph.GP_EM38;
			case "gp_tempest_aem" -> Glyph.GP_TEMPEST_AEM;
			case "gc_inversion_jacobian_matrix" -> Glyph.GC_INVERSION_JACOBIAN_MATRIX;
			case "gc_inversion_hessian_matrix" -> Glyph.GC_INVERSION_HESSIAN_MATRIX;
			case "gl_scale_pore" -> Glyph.GL_SCALE_PORE;
			case "gl_scale_grain" -> Glyph.GL_SCALE_GRAIN;
			case "gl_scale_specimen" -> Glyph.GL_SCALE_SPECIMEN;
			case "gl_scale_outcrop" -> Glyph.GL_SCALE_OUTCROP;
			case "gl_scale_structure" -> Glyph.GL_SCALE_STRUCTURE;
			case "gl_scale_deposit" -> Glyph.GL_SCALE_DEPOSIT;
			case "gl_scale_district" -> Glyph.GL_SCALE_DISTRICT;
			case "gl_scale_crustal" -> Glyph.GL_SCALE_CRUSTAL;
			case "gl_tool_compass" -> Glyph.GL_TOOL_COMPASS;
			case "gl_tool_clinometer" -> Glyph.GL_TOOL_CLINOMETER;
			case "gl_tool_rock_hammer" -> Glyph.GL_TOOL_ROCK_HAMMER;
			case "gl_tool_hand_lens" -> Glyph.GL_TOOL_HAND_LENS;
			case "gl_tool_field_notebook" -> Glyph.GL_TOOL_FIELD_NOTEBOOK;
			case "gl_tool_streak_plate" -> Glyph.GL_TOOL_STREAK_PLATE;
			case "gl_tool_sample_bag" -> Glyph.GL_TOOL_SAMPLE_BAG;
			case "gl_tool_measuring_tape" -> Glyph.GL_TOOL_MEASURING_TAPE;
			case "gp_seismic_source_hammer" -> Glyph.GP_SEISMIC_SOURCE_HAMMER;
			case "gp_seismic_source_explosive" -> Glyph.GP_SEISMIC_SOURCE_EXPLOSIVE;
			case "gp_seismic_source_betsy" -> Glyph.GP_SEISMIC_SOURCE_BETSY;
			case "gp_seismic_source_weight_drop_ute" -> Glyph.GP_SEISMIC_SOURCE_WEIGHT_DROP_UTE;
			case "gp_seismic_source_weight_drop_skid" -> Glyph.GP_SEISMIC_SOURCE_WEIGHT_DROP_SKID;
			case "gp_seismic_source_evibe" -> Glyph.GP_SEISMIC_SOURCE_EVIBE;
			case "gp_seismic_source_vibroseis" -> Glyph.GP_SEISMIC_SOURCE_VIBROSEIS;
			case "gp_seismic_source_airgun" -> Glyph.GP_SEISMIC_SOURCE_AIRGUN;
			case "gp_seismic_source_land_streamer" -> Glyph.GP_SEISMIC_SOURCE_LAND_STREAMER;
			case "gp_seismic_source_sparker" -> Glyph.GP_SEISMIC_SOURCE_SPARKER;
			case "gp_seismic_source_boomer" -> Glyph.GP_SEISMIC_SOURCE_BOOMER;
			case "gp_seismic_receiver_spiked" -> Glyph.GP_SEISMIC_RECEIVER_SPIKED;
			case "gp_seismic_receiver_wired" -> Glyph.GP_SEISMIC_RECEIVER_WIRED;
			case "gp_seismic_receiver_wireless" -> Glyph.GP_SEISMIC_RECEIVER_WIRELESS;
			case "gp_seismic_receiver_quantum" -> Glyph.GP_SEISMIC_RECEIVER_QUANTUM;
			case "gp_seismic_receiver_smartsolo" -> Glyph.GP_SEISMIC_RECEIVER_SMARTSOLO;
			case "gp_seismic_receiver_wing" -> Glyph.GP_SEISMIC_RECEIVER_WING;
			case "gp_seismic_receiver_geospace" -> Glyph.GP_SEISMIC_RECEIVER_GEOSPACE;
			case "gp_seismic_receiver_three_component" -> Glyph.GP_SEISMIC_RECEIVER_THREE_COMPONENT;
			case "gp_seismic_receiver_hydrophone" -> Glyph.GP_SEISMIC_RECEIVER_HYDROPHONE;
			case "gp_loop_magnetic_field" -> Glyph.GP_LOOP_MAGNETIC_FIELD;
			case "gp_em_smoke_ring" -> Glyph.GP_EM_SMOKE_RING;
			case "saussuritised" -> Glyph.GC_SAUSSURITISED;
			case "serpentinisation" -> Glyph.GC_SERPENTINISATION;
			case "epidote_alteration" -> Glyph.GC_EPIDOTE_ALTERATION;
			case "silicification" -> Glyph.GC_SILICIFICATION;
			case "carbonate_alteration" -> Glyph.GC_CARBONATE_ALTERATION;
			case "calcsilicate_alteration" -> Glyph.GC_CALCSILICATE_ALTERATION;
			case "greisen" -> Glyph.GC_GREISEN;
			case "albitic_alteration" -> Glyph.GC_ALBITIC_ALTERATION;
			case "advanced_argillic_alteration" -> Glyph.GC_ADVANCED_ARGILLIC_ALTERATION;
			case "not_altered" -> Glyph.GC_NOT_ALTERED;
			case "chloritic_alteration" -> Glyph.GC_CHLORITIC_ALTERATION;
			case "zeolitic_alteration" -> Glyph.GC_ZEOLITIC_ALTERATION;
			case "propylitic_alteration" -> Glyph.GC_PROPYLITIC_ALTERATION;
			case "potassic_alteration" -> Glyph.GC_POTASSIC_ALTERATION;
			case "alteration_not_specified" -> Glyph.GC_ALTERATION_NOT_SPECIFIED;
			case "kaolinitic_alteration" -> Glyph.GC_KAOLINITIC_ALTERATION;
			case "sericitic_alteration" -> Glyph.GC_SERICITIC_ALTERATION;
			case "argillic_alteration" -> Glyph.GC_ARGILLIC_ALTERATION;
			case "alunitic_alteration" -> Glyph.GC_ALUNITIC_ALTERATION;
			case "hematitic_alteration" -> Glyph.GC_HEMATITIC_ALTERATION;
			case "pyritic_alteration" -> Glyph.GC_PYRITIC_ALTERATION;
			case "deuteric_alteration" -> Glyph.GC_DEUTERIC_ALTERATION;
			case "uralitisation" -> Glyph.GC_URALITISATION;
			case "red_rock_alteration" -> Glyph.GC_RED_ROCK_ALTERATION;
			case "geochemical_vectoring" -> Glyph.GC_GEOCHEMICAL_VECTORING;
			case "hydrothermal_alteration" -> Glyph.GC_HYDROTHERMAL_ALTERATION;
			case "magmatic_intrusion" -> Glyph.GC_MAGMATIC_INTRUSION;
			case "dehydration" -> Glyph.GC_DEHYDRATION;
			case "reducing_environment" -> Glyph.GC_REDUCING_ENVIRONMENT;
			case "oxidizing_environment" -> Glyph.GC_OXIDIZING_ENVIRONMENT;
			case "vectoring" -> Glyph.GC_GEOCHEMICAL_VECTORING;
			case "alteration" -> Glyph.GC_HYDROTHERMAL_ALTERATION;
			case "intrusion" -> Glyph.GC_MAGMATIC_INTRUSION;
			case "dehydrating" -> Glyph.GC_DEHYDRATION;
			case "reducing" -> Glyph.GC_REDUCING_ENVIRONMENT;
			case "oxidizing" -> Glyph.GC_OXIDIZING_ENVIRONMENT;
			case "oxidising" -> Glyph.GC_OXIDIZING_ENVIRONMENT;
			case "granite_post_kinematic" -> Glyph.GL_GRANITE_POST_KINEMATIC;
			case "granite_late_post_kinematic" -> Glyph.GL_GRANITE_LATE_POST_KINEMATIC;
			case "granite_syn_late_kinematic" -> Glyph.GL_GRANITE_SYN_LATE_KINEMATIC;
			case "granite_syn_kinematic_foliated" -> Glyph.GL_GRANITE_SYN_KINEMATIC_FOLIATED;
			case "granite_gneissic_anatectic" -> Glyph.GL_GRANITE_GNEISSIC_ANATECTIC;
			case "gabbro_diorite_orogenic" -> Glyph.GL_GABBRO_DIORITE_OROGENIC;
			case "porphyry_pattern" -> Glyph.GL_PORPHYRY_PATTERN;
			case "island_arc_volcanics" -> Glyph.GL_ISLAND_ARC_VOLCANICS;
			case "felsic_volcanics_rare_basics" -> Glyph.GL_FELSIC_VOLCANICS_RARE_BASICS;
			case "rhyolite_dacite_volcanics" -> Glyph.GL_RHYOLITE_DACITE_VOLCANICS;
			case "felsic_volcanics_with_granite" -> Glyph.GL_FELSIC_VOLCANICS_WITH_GRANITE;
			case "flood_basalt" -> Glyph.GL_FLOOD_BASALT;
			case "dolerite_granophyre" -> Glyph.GL_DOLERITE_GRANOPHYRE;
			case "keratophyre" -> Glyph.GL_KERATOPHYRE;
			case "granite_intruding_craton" -> Glyph.GL_GRANITE_INTRUDING_CRATON;
			case "layered_intrusion" -> Glyph.GL_LAYERED_INTRUSION;
			case "alkaline_intrusive" -> Glyph.GL_ALKALINE_INTRUSIVE;
			case "kimberlite_lamproite" -> Glyph.GL_KIMBERLITE_LAMPROITE;
			case "carbonatite" -> Glyph.GL_CARBONATITE;
			case "slate_phyllite" -> Glyph.GL_SLATE_PHYLLITE;
			case "schist_gneiss_high_grade" -> Glyph.GL_SCHIST_GNEISS_HIGH_GRADE;
			case "sandy_slate_interbedded" -> Glyph.GL_SANDY_SLATE_INTERBEDDED;
			case "hornfels_massive" -> Glyph.GL_HORNFELS_MASSIVE;
			case "basic_plutonic_hypabyssal" -> Glyph.GL_BASIC_PLUTONIC_HYPABYSSAL;
			case "bedded_lavas" -> Glyph.GL_BEDDED_LAVAS;
			case "tuff_tuffaceous_sandstone" -> Glyph.GL_TUFF_TUFFACEOUS_SANDSTONE;
			case "bedded_tuff" -> Glyph.GL_BEDDED_TUFF;
			case "breccia_pattern" -> Glyph.GL_BRECCIA_PATTERN;
			case "scree_brecciated_rock" -> Glyph.GL_SCREE_BRECCIATED_ROCK;
			case "soil_cover" -> Glyph.GL_SOIL_COVER;
			case "alluvium" -> Glyph.GL_ALLUVIUM;
			case "gossan_ore" -> Glyph.GL_GOSSAN_ORE;
			case "conglomerate_pattern" -> Glyph.GL_CONGLOMERATE_PATTERN;
			case "sandstone_pattern" -> Glyph.GL_SANDSTONE_PATTERN;
			case "pebbly_sandstone" -> Glyph.GL_PEBBLY_SANDSTONE;
			case "cross_bedded_sandstone" -> Glyph.GL_CROSS_BEDDED_SANDSTONE;
			case "limestone_pattern" -> Glyph.GL_LIMESTONE_PATTERN;
			case "dolomite_pattern" -> Glyph.GL_DOLOMITE_PATTERN;
			case "sandy_limestone" -> Glyph.GL_SANDY_LIMESTONE;
			case "shale_pattern" -> Glyph.GL_SHALE_PATTERN;
			case "sandy_shale" -> Glyph.GL_SANDY_SHALE;
			case "bedded_chert" -> Glyph.GL_BEDDED_CHERT;
			case "massive_chert" -> Glyph.GL_MASSIVE_CHERT;
			case "coal_undifferentiated" -> Glyph.GL_COAL_UNDIFFERENTIATED;
			case "broken_coal" -> Glyph.GL_BROKEN_COAL;
			case "coal_with_shale_bands" -> Glyph.GL_COAL_WITH_SHALE_BANDS;
			case "shale_with_coal_bands" -> Glyph.GL_SHALE_WITH_COAL_BANDS;
			case "cannel_coal" -> Glyph.GL_CANNEL_COAL;
			case "cannel_shale" -> Glyph.GL_CANNEL_SHALE;
			case "carbonaceous_shale" -> Glyph.GL_CARBONACEOUS_SHALE;
			case "brown_coal" -> Glyph.GL_BROWN_COAL;
			case "oil_shale" -> Glyph.GL_OIL_SHALE;
			case "thin_seam" -> Glyph.GL_THIN_SEAM;
			case "coal_bright" -> Glyph.GL_COAL_BRIGHT;
			case "coal_bright_dull_bands" -> Glyph.GL_COAL_BRIGHT_DULL_BANDS;
			case "coal_interbanded" -> Glyph.GL_COAL_INTERBANDED;
			case "coal_dull_bright_bands" -> Glyph.GL_COAL_DULL_BRIGHT_BANDS;
			case "coal_dull_minor_bright" -> Glyph.GL_COAL_DULL_MINOR_BRIGHT;
			case "coal_dull" -> Glyph.GL_COAL_DULL;
			case "coal_canneloid" -> Glyph.GL_COAL_CANNELOID;
			case "coal_fibrous" -> Glyph.GL_COAL_FIBROUS;
			case "coal_weathered" -> Glyph.GL_COAL_WEATHERED;
			case "coal_heat_altered" -> Glyph.GL_COAL_HEAT_ALTERED;
			case "non_coal" -> Glyph.GL_NON_COAL;
			case "coal_interlayered_non_coal" -> Glyph.GL_COAL_INTERLAYERED_NON_COAL;
			case "non_coal_interlayered_coal" -> Glyph.GL_NON_COAL_INTERLAYERED_COAL;
			case "stony_coal" -> Glyph.GL_STONY_COAL;
			case "mudstone_pattern" -> Glyph.GL_MUDSTONE_PATTERN;
			case "coal_seam_log" -> Glyph.GL_COAL_SEAM_LOG;
			case "fold_upright_horizontal" -> Glyph.GL_FOLD_UPRIGHT_HORIZONTAL;
			case "fold_upright_plunging" -> Glyph.GL_FOLD_UPRIGHT_PLUNGING;
			case "fold_vertical" -> Glyph.GL_FOLD_VERTICAL;
			case "fold_inclined_plunging" -> Glyph.GL_FOLD_INCLINED_PLUNGING;
			case "fold_overturned_horizontal" -> Glyph.GL_FOLD_OVERTURNED_HORIZONTAL;
			case "fold_overturned_plunging" -> Glyph.GL_FOLD_OVERTURNED_PLUNGING;
			case "fold_recumbent" -> Glyph.GL_FOLD_RECUMBENT;
			case "fold_reclined" -> Glyph.GL_FOLD_RECLINED;
			case "monocline" -> Glyph.GL_MONOCLINE;
			case "fold_vergence" -> Glyph.GL_FOLD_VERGENCE;
			case "superposed_folds" -> Glyph.GL_SUPERPOSED_FOLDS;
			case "fold_class_1a" -> Glyph.GL_FOLD_CLASS_1A;
			case "fold_class_1b" -> Glyph.GL_FOLD_CLASS_1B;
			case "fold_class_1c" -> Glyph.GL_FOLD_CLASS_1C;
			case "fold_class_2" -> Glyph.GL_FOLD_CLASS_2;
			case "fold_class_3" -> Glyph.GL_FOLD_CLASS_3;
			case "dip_isogon_construction" -> Glyph.GL_DIP_ISOGON_CONSTRUCTION;
			case "fold_attitude_grid" -> Glyph.GL_FOLD_ATTITUDE_GRID;
			case "fold_attitude_classification" -> Glyph.GL_FOLD_ATTITUDE_CLASSIFICATION;
			case "orthographic_net" -> Glyph.GL_ORTHOGRAPHIC_NET;
			case "wulff_net" -> Glyph.GL_WULFF_NET;
			case "schmidt_net" -> Glyph.GL_SCHMIDT_NET;
			case "stereonet_contouring_device" -> Glyph.GL_STEREONET_CONTOURING_DEVICE;
			case "rock_fall" -> Glyph.GL_ROCK_FALL;
			case "rock_topple" -> Glyph.GL_ROCK_TOPPLE;
			case "rock_slump" -> Glyph.GL_ROCK_SLUMP;
			case "rock_block_slide" -> Glyph.GL_ROCK_BLOCK_SLIDE;
			case "rock_lateral_spread" -> Glyph.GL_ROCK_LATERAL_SPREAD;
			case "rock_creep_sackung" -> Glyph.GL_ROCK_CREEP_SACKUNG;
			case "rock_fall_debris_flow" -> Glyph.GL_ROCK_FALL_DEBRIS_FLOW;
			case "slump_topple" -> Glyph.GL_SLUMP_TOPPLE;
			case "rock_slide_rock_fall" -> Glyph.GL_ROCK_SLIDE_ROCK_FALL;
			case "debris_fall" -> Glyph.GL_DEBRIS_FALL;
			case "debris_topple" -> Glyph.GL_DEBRIS_TOPPLE;
			case "debris_slump" -> Glyph.GL_DEBRIS_SLUMP;
			case "debris_slide" -> Glyph.GL_DEBRIS_SLIDE;
			case "debris_flow" -> Glyph.GL_DEBRIS_FLOW;
			case "debris_avalanche" -> Glyph.GL_DEBRIS_AVALANCHE;
			case "block_stream" -> Glyph.GL_BLOCK_STREAM;
			case "solifluction" -> Glyph.GL_SOLIFLUCTION;
			case "soil_creep" -> Glyph.GL_SOIL_CREEP;
			case "cambering_valley_bulging" -> Glyph.GL_CAMBERING_VALLEY_BULGING;
			case "slump_earth_flow" -> Glyph.GL_SLUMP_EARTH_FLOW;
			case "earth_fall" -> Glyph.GL_EARTH_FALL;
			case "earth_topple" -> Glyph.GL_EARTH_TOPPLE;
			case "earth_slump" -> Glyph.GL_EARTH_SLUMP;
			case "earth_block_slide" -> Glyph.GL_EARTH_BLOCK_SLIDE;
			case "earth_lateral_spread" -> Glyph.GL_EARTH_LATERAL_SPREAD;
			case "wet_sand_silt_flow" -> Glyph.GL_WET_SAND_SILT_FLOW;
			case "quick_clay_flow" -> Glyph.GL_QUICK_CLAY_FLOW;
			case "earth_flow" -> Glyph.GL_EARTH_FLOW;
			case "loess_flow" -> Glyph.GL_LOESS_FLOW;
			case "dry_sand_flow" -> Glyph.GL_DRY_SAND_FLOW;
			case "qapf_plutonic_diagram" -> Glyph.GL_QAPF_PLUTONIC_DIAGRAM;
			case "gabbroic_plag_px_ol" -> Glyph.GL_GABBROIC_PLAG_PX_OL;
			case "gabbroic_plag_px_hbl" -> Glyph.GL_GABBROIC_PLAG_PX_HBL;
			case "gabbroic_plag_opx_cpx" -> Glyph.GL_GABBROIC_PLAG_OPX_CPX;
			case "metamorphic_facies_diagram" -> Glyph.GL_METAMORPHIC_FACIES_DIAGRAM;
			case "roundness_very_angular" -> Glyph.GL_ROUNDNESS_VERY_ANGULAR;
			case "roundness_angular" -> Glyph.GL_ROUNDNESS_ANGULAR;
			case "roundness_subangular" -> Glyph.GL_ROUNDNESS_SUBANGULAR;
			case "roundness_subrounded" -> Glyph.GL_ROUNDNESS_SUBROUNDED;
			case "roundness_rounded" -> Glyph.GL_ROUNDNESS_ROUNDED;
			case "roundness_well_rounded" -> Glyph.GL_ROUNDNESS_WELL_ROUNDED;
			case "grain_percent_01" -> Glyph.GL_GRAIN_PERCENT_01;
			case "grain_percent_02" -> Glyph.GL_GRAIN_PERCENT_02;
			case "grain_percent_03" -> Glyph.GL_GRAIN_PERCENT_03;
			case "grain_percent_05" -> Glyph.GL_GRAIN_PERCENT_05;
			case "grain_percent_07" -> Glyph.GL_GRAIN_PERCENT_07;
			case "grain_percent_10" -> Glyph.GL_GRAIN_PERCENT_10;
			case "grain_percent_15" -> Glyph.GL_GRAIN_PERCENT_15;
			case "grain_percent_20" -> Glyph.GL_GRAIN_PERCENT_20;
			case "grain_percent_25" -> Glyph.GL_GRAIN_PERCENT_25;
			case "grain_percent_30" -> Glyph.GL_GRAIN_PERCENT_30;
			case "grain_percent_40" -> Glyph.GL_GRAIN_PERCENT_40;
			case "grain_percent_50" -> Glyph.GL_GRAIN_PERCENT_50;
			case "unit_stratotype" -> Glyph.GL_UNIT_STRATOTYPE;
			case "boundary_stratotype" -> Glyph.GL_BOUNDARY_STRATOTYPE;
			case "earthquake_magnitude_energy" -> Glyph.GL_EARTHQUAKE_MAGNITUDE_ENERGY;
            default -> null;
        };
    }

    /** Resolve an Opus quantity or geological descriptor by its stable ID. */
    public static Glyph forProperty(OpusProperty property) {
        return property == null ? null : forIconId(property.id());
    }

    public static org.controlsfx.glyphfont.Glyph createGlyph(Glyph glyph, double size) {
        GlyphFont font = GlyphFontRegistry.font(FONT_NAME);
        return font.create(glyph).size(size);
    }
}
