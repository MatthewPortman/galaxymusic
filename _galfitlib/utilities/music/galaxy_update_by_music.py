from _galfitlib.classes.galaxy_components import Sersic, Power, Fourier, FourierMode

# =============================================================================
# ====================== CONVERTER HELPER FUNC ================================
# =============================================================================
def note_converter(
        parameter,
        lambda_func,
        modify_dict,
        note,
        *args
):
    """
    Performs the calculation to modify the galaxy property
    if the note is in the dictionary of notes to modify.
    """
    if note in modify_dict:
        parameter.value =  lambda_func(modify_dict[note], *args)


# =============================================================================
# ============================ BULGE ==========================================
# =============================================================================

def bulge_modify(
        bulge_object: Sersic,
        dict_modify_values: dict
):
    """
    Modifies the bulge object based on the dictionary of note values
    """
    # Magnitude is an inverse property
    magnitude_lambda = lambda x: (12 - 16) * x + 16
    # There is a relationship between effective radius and sersic index
    # so these two together do not follow the same pattern as the others
    effective_radius_lambda = lambda x: (4 - 2) * (1 + x) + 2
    # Traditional bulge value is 4... so a minimum of 2 should be OK
    sersic_index_lambda = lambda x: (5 - 2) * (1 - x) + 2
    axis_ratio_lambda = lambda x: (1 - 0.5) * (1 - x) + 0.5
    # Nor does this, but it's an angle, it gets a pass.
    position_angle_lambda = lambda x: 2 * np.arcsin(x) * 180.0 / np.pi

    note_converter(
            bulge_object.magnitude,
            magnitude_lambda,
            dict_modify_values,
            '1'
    )

    note_converter(
            bulge_object.effective_radius,
            effective_radius_lambda,
            dict_modify_values,
            '3'
    )

    note_converter(
            bulge_object.sersic_index,
            sersic_index_lambda,
            dict_modify_values,
            '6'
    )

    note_converter(
            bulge_object.axis_ratio,
            axis_ratio_lambda,
            dict_modify_values,
            '7'
    )

    note_converter(
            bulge_object.position_angle,
            position_angle_lambda,
            dict_modify_values,
            '5'
    )

# =============================================================================
# ============================ DISK ===========================================
# =============================================================================

def disk_modify(
        disk_object: Sersic,
        dict_modify_values: dict
):
    """
    Modifies the disk object based on the dictionary of note values
    """
    # Magnitude is an inverse property
    magnitude_lambda = lambda x: (14 - 16) * x + 16
    # There is a relationship between effective radius and sersic index
    # so these two together do not follow the same pattern as the others
    effective_radius_lambda = lambda x: (25 - 10) * (1 + x) + 10
    # Traditional disk value is 1... so limiting it to 2 should give us some nice lookin' galaxies
    sersic_index_lambda = lambda x: (2 - 0.25) * (1 - x) + 0.25
    axis_ratio_lambda = lambda x: (1 - 0.5) * x + 0.5
    position_angle_lambda = lambda x: 2 * np.arcsin(x) * 180.0 / np.pi

    note_converter(
            disk_object.magnitude,
            magnitude_lambda,
            dict_modify_values,
            '1'
    )

    note_converter(
            disk_object.effective_radius,
            effective_radius_lambda,
            dict_modify_values,
            'RMS'
    )

    note_converter(
            disk_object.sersic_index,
            sersic_index_lambda,
            dict_modify_values,
            '0'
    )

    note_converter(
            disk_object.axis_ratio,
            axis_ratio_lambda,
            dict_modify_values,
            '2'
    )

    note_converter(
            disk_object.position_angle,
            position_angle_lambda,
            dict_modify_values,
            '2'
    )

# =============================================================================
# ============================== ARMS =========================================
# =============================================================================

def arms_modify(
        arms_object: Power,
        dict_modify_values: dict
):
    """
    Modifies the arms object based on the dictionary of note values
    """
    inner_radius_lambda = lambda x: (15 - 0) * (1 - x) + 0
    outer_radius_lambda = lambda x: (15 - 0) * (1 + x) + 25
    cumul_rot_lambda = lambda x: 90 * np.pi / 180 * np.arcsin(x) * 180.0 / np.pi + 90
    powerlaw_index_lambda = lambda x: (2.5 - -1) * (1 - x) + -1
    inclination_lambda = lambda x: min(np.arcsin(x) * 180.0 / np.pi, 55)
    sky_position_angle_lambda = lambda x: 2 * np.arcsin(x) * 180.0 / np.pi

    note_converter(
            arms_object.inner_rad,
            inner_radius_lambda,
            dict_modify_values,
            '5'
    )

    note_converter(
            arms_object.outer_rad,
            outer_radius_lambda,
            dict_modify_values,
            'RMS'
    )

    note_converter(
            arms_object.cumul_rot,
            cumul_rot_lambda,
            dict_modify_values,
            '3'
    )

    note_converter(
            arms_object.powerlaw_index,
            powerlaw_index_lambda,
            dict_modify_values,
            '4'
    )

    note_converter(
            arms_object.inclination,
            inclination_lambda,
            dict_modify_values,
            '6'
    )

    note_converter(
            arms_object.sky_position_angle,
            sky_position_angle_lambda,
            dict_modify_values,
            '3'
    )

# =============================================================================
# ============================ FOURIER ========================================
# =============================================================================

def fourier_modify(
        dict_modify_values: dict
):
    """
    Modifies the fourier object based on the dictionary of note values
    Of course, the Fourier modes always complicate things so this is
    much different than the previous.
    """
    num_fourier_modes_lambda = lambda x: (5 - 1) * (1 - x) + 1
    # formerly (0.05 - 0.001) * (1 - x) + 0.001
    amplitude_lambda = lambda x, default_amplitude, default_phase_angle: (
        ((0.75 + x) * default_amplitude),
        default_phase_angle
    )

    if '1' in dict_modify_values:
        num_fourier_modes = num_fourier_modes_lambda(dict_modify_values['1'])
    else:
        num_fourier_modes = 2

    fourier_object = Fourier(num_fourier_modes)

    count = 5
    for Fmode in fourier_object.parameters.values():
        if isinstance(Fmode, FourierMode):
            note_converter(
                    Fmode,
                    amplitude_lambda,
                    dict_modify_values,
                    str(count),
                    Fmode.amplitude,
                    Fmode.phase_angle
            )
        count += 1

    return fourier_object

# =============================================================================
# ============================ GALAXY =========================================
# =============================================================================

def music_to_galaxy_properties(
        bulge_object: Sersic,
        disk_object: Sersic,
        arms_object: Power,
        # fourier_object : Fourier,
        dict_modify_values: dict
):
    """
    KEY:
    PRIORITY - GALAXY PROPERTY

    BULGE
    2 – ‘Magnitude’ [10,16] -> Linearly [0,1] | Set: 15 | Direction: Longer -> Lower Value
    4 – ‘Effective Radius’ [0, 75] | Set: 3 | Direction: Longer -> Higher Value
    7 – ‘Sersic Index’ [0.1, 8] (linear-ish scaling) | Set: 1.0 | Direction: Longer -> Higher Value
    8 – ‘Axis Ratio’ [0.5, 1] | Set: 1.0 | Direction: Longer -> Lower Value
    6 – ‘Position Angle’ [0.5, 1] | Set: 1.0 | Direction: Longer -> Lower Value

    DISK
    2   – ‘Magnitude’ [10, 16] -> Linearly [0, 1] | Set: 15 | Direction: Longer -> Lower Value
    RMS – ‘Eff_Rad’ [0, 75] | Set: 20 | Direction: Longer -> Higher Value
    1   – ‘Sersic_Index’ [0.1, 8] (linear-ish scaling) | Set: 1.0 | Direction: Longer -> Higher Value
    3   – ‘Pos_Angle’ [0, 180] -> [0,1] Sin(theta/2) | Set: 0 | Direction: Longer -> Higher Value
    4   – ‘Axis_Ratio’ [0.5, 1] | Set: 1.0 | Direction: Longer -> Lower Value

    ARMS
    6   - spiral inner radius
    RMS - spiral outer radius
    4   - cumulative rotation
    5   - spiral power law
    7   - inclination
    6   - position angle

    FOURIER
    3   - # of fourier modes
    9   - strength of fourier modes
    """
    # Modification of the galaxy properties based on the music notes
    # As (generally) follows:
    # (max_value - min_value) * (1 +/- normalized_note_value) + min_value

    # BULGE
    bulge_modify(bulge_object, dict_modify_values)

    # DISK
    disk_modify(disk_object, dict_modify_values)

    # ARMS
    arms_modify(arms_object, dict_modify_values)

    # FOURIER
    # The number of arms depends on the song so the fourier object operates differently
    return fourier_modify(dict_modify_values)
