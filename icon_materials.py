"""Material colours for flat artwork; never choose a palette by discipline.

Physical objects use representative materials (steel, glass, rock, soil,
water, foliage). Abstract diagrams use neutral ink and paper. These colours
illustrate familiar appearances, not a scientific lithology or assay legend.
"""

MATERIALS = {
    'ink': '#303A40', 'paper': '#E7E8E3', 'steel': '#7C8991',
    'aluminium': '#C4CCD0', 'glass': '#CCE3EB', 'water': '#4C9FC3',
    'sand': '#DBC49C', 'soil': '#A7825D', 'clay': '#BB8B70',
    'stone': '#979B97', 'limestone': '#D5D0BD', 'slate': '#78898F',
    'basalt': '#535B5F', 'granite': '#BD9A8E', 'quartz': '#D7E1E3',
    'feldspar': '#D7A49A', 'sulfide': '#BAA05C', 'hematite': '#A85F49',
    'magnetite': '#42494D', 'serpentine': '#718D6A', 'chlorite': '#64866A',
    'leaf': '#518B4E', 'oil': '#564539', 'lava': '#E67C43',
    'heat': '#DA6452', 'gold': '#D2AD4C', 'ceramic': '#DCD4BD',
    'housing': '#DDB448', 'rubber': '#434B50', 'copper': '#B87C55',
}

# Each icon has its own surface/body materials. Aliases a and p refer to
# geometric roles in the flat recipe, not the domain or category of the icon.
PAIRS = """
gp_seismic_reflection steel soil
gp_gravity_survey steel aluminium
gp_magnetic_survey steel aluminium
gp_electromagnetic_em steel glass
gp_ert_ip steel soil
gp_velocity_model slate limestone
gp_density_model basalt stone
gp_susceptibility_model magnetite stone
gp_resistivity_section clay sand
gp_seismic_cube_3d slate limestone
gp_wave_propagation ink paper
gp_ray_refraction_snell ink sand
gp_geophysical_inversion ink paper
gp_signal_deconvolution ink paper
gp_nmo_stacking ink aluminium
gt_spt_test steel aluminium
gt_cpt_cone steel aluminium
gt_triaxial_shear stone glass
gt_piezometer_well steel soil
gt_inclinometer_casing steel aluminium
gt_mohr_coulomb ink paper
gt_rock_mass_rmr_gsi stone granite
gt_slope_stability_grid soil sand
gt_soil_profile_log soil sand
gt_fe_mesh_tunnel basalt stone
gt_consolidation_settlement stone soil
gt_soil_liquefaction stone sand
gt_slope_landslide soil sand
gt_seepage_flownet water soil
gt_rock_burst_spalling basalt stone
gl_strike_dip_mapping steel aluminium
gl_diamond_core_drilling stone steel
gl_thin_section_petrography feldspar quartz
gl_stratigraphic_logging soil limestone
gl_structural_stereonet ink paper
gl_block_model_3d granite limestone
gl_wireframe_mesh steel paper
gl_faulted_stratigraphy clay limestone
gl_folded_anticline_model clay limestone
gl_intrusive_pluton_model granite limestone
gl_plate_subduction basalt granite
gl_fault_slip_tectonics stone limestone
gl_sedimentation_deposition sand soil
gl_metamorphism_pt quartz slate
gl_weathering_erosion soil stone
gc_soil_stream_sampling steel soil
gc_pxrf_analyzer housing glass
gc_icp_ms_spectrometry ink paper
gc_fire_assay lava ceramic
gc_isotope_ratio_analysis steel paper
gc_alteration_zonation hematite clay
gc_geochem_anomaly_contours soil sand
gc_ternary_classification ink paper
gc_eh_ph_pourbaix ink paper
gc_downhole_geochem_log ink paper
gc_hydrothermal_circulation water stone
gc_supergene_leaching copper soil
gc_redox_front_roll hematite sand
gc_magmatic_differentiation lava basalt
gc_element_dispersion_halo soil sand
gp_self_potential steel aluminium
gp_magnetotellurics_mt steel soil
gp_ground_penetrating_radar housing aluminium
gp_radiometrics_gamma steel aluminium
gp_nmr_sounding steel glass
gp_thermal_geothermal heat glass
gp_acoustics_sonar steel water
gp_geodesy_insar_gnss aluminium steel
gp_remote_sensing_hyperspectral leaf soil
gp_matrix_mixing_bounds ink paper
gp_pore_fluid_archie water sand
gp_ip_cole_cole ink paper
gp_dielectric_permittivity steel aluminium
gp_koenigsberger_remanence magnetite stone
gp_gassmann_fluid_sub water sand
gp_permeability_kozeny water sand
gt_deere_rqd stone granite
gt_barton_q_tunnel steel stone
gt_bieniawski_rmr ink paper
gt_hoek_brown_criterion ink paper
gt_ucs_from_velocity ink stone
gt_brittleness_index slate stone
gl_rock_type_igneous basalt stone
gl_rock_type_sedimentary soil sand
gl_rock_type_metamorphic slate quartz
gl_composition_category feldspar quartz
gl_genetic_category basalt granite
gl_metamorphic_facies_pt ink paper
gl_consolidation_degree soil stone
gl_deformation_brittle_ductile slate stone
gl_unit_morphology slate limestone
gl_style_disseminated sulfide basalt
gl_style_net_textured sulfide basalt
gl_style_massive_sulfide sulfide stone
gl_style_veined_stringer quartz basalt
gl_particle_shape_roundness granite limestone
gl_contact_unconformity soil sand
gl_foliation_lineation slate quartz
gl_borehole_drilling_methods steel stone
gl_planar_polarity_overturned ink paper
gm_acid_rock_drainage hematite stone
gm_comminution_work_index stone steel
gm_flotation_recovery sulfide water
gc_melt_chemistry_f02 lava glass
gc_carbon_mineralisation limestone serpentine
gl_lithology_tensor_anisotropy slate quartz
gl_fault_normal_graben clay limestone
gl_fault_thrust_ramp clay limestone
gl_fault_strike_slip_dextral stone limestone
gl_shear_zone_sigmoidal quartz slate
gl_chevron_kink_fold slate limestone
gl_ptygmatic_vein_fold quartz slate
gl_columnar_jointing basalt slate
gl_spinifex_texture serpentine basalt
gl_pillow_lava basalt slate
gl_fiamme_ignimbrite basalt clay
gl_banded_iron_formation hematite limestone
gl_hydrothermal_breccia granite quartz
gl_potassic_alteration feldspar granite
gl_phyllic_sericitic_alteration quartz limestone
gl_advanced_argillic ceramic quartz
gl_propylitic_chlorite_epidote chlorite serpentine
gl_serpentinite_mesh serpentine basalt
gl_skarn_calc_silicate chlorite limestone
gl_greisen_cassiterite oil quartz
gl_tourmaline_sun_rosette basalt stone
gl_turbidite_bouma_sequence clay sand
gl_fluvial_point_bar_channel sand soil
gc_la_icp_ms_laser steel quartz
gc_epma_wds_microprobe steel aluminium
gc_xrd_diffractometer steel aluminium
gc_xanes_synchrotron steel aluminium
gc_libs_laser_plasma heat stone
gc_ftir_raman_spectroscopy ink paper
gc_four_acid_total_digest glass glass
gc_aqua_regia_partial_digest gold glass
gc_cyanide_bottle_roll water glass
gc_sequential_extraction water glass
gc_gas_chromatography_ms steel aluminium
gc_sims_shrimp_microprobe steel quartz
gc_tims_thermal_ionization heat aluminium
gc_stable_isotope_gas_irms steel aluminium
gc_fluid_inclusion_microtherm quartz glass
gc_radon_emanometry steel soil
gc_biogeochem_vegetation leaf soil
gc_ree_chondrite_spidergram ink paper
gc_primitive_mantle_spidergram ink paper
gc_tas_volcanic_diagram ink paper
gc_qapf_ternary_double ink paper
gc_pearce_tectonic_discrimination ink paper
gc_activity_activity_diagram ink paper
gc_zircon_upb_concordia ink paper
gc_rb_sr_isochron_diagram ink paper
gc_sulfur_isotope_delta34s ink paper
gc_swir_mineral_spectral_trough ink paper
gc_campbell_vectoring_ratio ink paper
gc_alumina_saturation_asi ink paper
gc_harker_variation_diagram ink paper
gc_water_solubility_melt water paper
gc_oxygen_isotope_delta18o water paper
gc_hydrothermal_boiling_immiscibility water glass
gc_sulfide_melt_immiscibility sulfide basalt
gc_fluid_rock_metasomatism water stone
gc_bacterial_sulfate_reduction stone sulfide
gc_heavy_mineral_placer gold sand
gc_gossan_boxwork_weathering hematite soil
gc_fumarolic_gas_exsolution aluminium basalt
gc_clay_adsorption_cec copper clay
gc_metal_chloride_complexation copper paper
gc_hydrocarbon_catagenesis oil stone
gc_colloid_flocculation clay sand
gc_gibbs_free_energy ink paper
gc_chemical_elements steel paper
gl_minerals_specimen quartz aluminium
gc_element_diff_wtpct ink paper
gc_temperature_thermo heat glass
gc_pressure_gauge steel aluminium
gc_gradient_perturbation_factor ink paper
gc_l1_norm_regularization ink paper
gc_n_iterations_loop ink paper
gc_thermodynamics_system heat aluminium
gp_petrophysics_core_matrix sand stone
gl_positions_spatial_coords ink paper
gc_volatiles_degassing aluminium lava
gc_water_activity_ah2o water glass
gc_fluid_xco2_mole_fraction steel glass
gc_oxygen_fugacity_fo2 steel aluminium
gc_major_element_oxides steel quartz
gc_gradient_initial_step ink paper
gc_sensitivity_jacobian ink paper
gp_specific_gravity_balance steel glass
gc_log_error_residuals ink paper
gl_geological_tagging_domain soil paper
"""

ICON_MATERIALS = {identifier: (accent, body) for identifier, accent, body in
                  (row.split() for row in PAIRS.strip().splitlines())}

