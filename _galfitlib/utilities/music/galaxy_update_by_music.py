from _galfitlib.classes.parameters import FourierMode
from _galfitlib.classes.components import Sersic, Power, Fourier
import numpy as np

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
    Evaluates the lambda function to modify the galaxy property
    using the crucial if-statement to check if the note is in
    the dictionary of notes to modify.

    Parameters
    ----------
    parameter : Parameter
        The GALFIT parameter to modify
    lambda_func : function
        The lambda function to evaluate
    modify_dict : dict
        The dictionary of notes used to modify the galaxy property
    note : str
        The note (priority number) being used
    args : list
        Any additional arguments to pass to the lambda function if used
        (Fourier modes looking at you)

    Returns
    -------
    None
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
    Modifies the bulge object based on the dictionary of note (priority number) values

    Parameters
    ----------
    bulge_object : Sersic
        The galfitlib bulge object to modify
    dict_modify_values : dict
        The dictionary of notes (priority numbers) used to modify the galaxy property

    Returns
    -------
    None
    """
    # Magnitude is an inverse property
    magnitude_lambda        = lambda x: (12 - 16) * x + 16
    # There is a relationship between effective radius and sersic index
    # so these two together do not follow the same pattern as the others
    effective_radius_lambda = lambda x: (4 - 2) * (1 + x) + 2
    # Traditional bulge value is 4... so a minimum of 2 should be OK
    sersic_index_lambda     = lambda x: (5 - 2) * (1 - x) + 2
    axis_ratio_lambda       = lambda x: (1 - 0.5) * (1 - x) + 0.5
    # Nor does this, but it's an angle, it gets a pass.
    position_angle_lambda   = lambda x: 2 * np.arcsin(x) * 180.0 / np.pi

    # Convert all one at a time to check for the existence of the note/priority number
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
            '4'
    )

# =============================================================================
# ============================ DISK ===========================================
# =============================================================================

def disk_modify(
        disk_object: Sersic,
        dict_modify_values: dict
):
    """
    Modifies the bulge object based on the dictionary of note (priority number) values

    Parameters
    ----------
    disk_object : Sersic
        The galfitlib disk object to modify
    dict_modify_values : dict
        The dictionary of notes (priority numbers) used to modify the galaxy property

    Returns
    -------
    None
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
            '1'
    )

# =============================================================================
# ============================== ARMS =========================================
# =============================================================================

def arms_modify(
        arms_object: Power,
        dict_modify_values: dict
):
    """
    Modifies the bulge object based on the dictionary of note (priority number) values

    Parameters
    ----------
    arms_object : Sersic
        The galfitlib arms object to modify
    dict_modify_values : dict
        The dictionary of notes (priority numbers) used to modify the galaxy property

    Returns
    -------
    None
    """
    inner_radius_lambda       = lambda x: (15 - 0) * (1 - x) + 0
    outer_radius_lambda       = lambda x: (15 - 0) * (1 + x) + 25
    cumul_rot_lambda          = lambda x: 90 * np.pi / 180 * np.arcsin(x) * 180.0 / np.pi + 90
    powerlaw_index_lambda     = lambda x: (2.5 - -1) * (1 - x) + -1
    inclination_lambda        = lambda x: min(np.arcsin(x) * 180.0 / np.pi, 55)
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

    Parameters
    ----------
    dict_modify_values : dict
        The dictionary of notes (priority numbers) used to modify the galaxy property

    Returns
    -------
    Fourier object
    """
    # Max 5, Min 1
    num_fourier_modes_lambda = lambda x: int((5 - 1) * (1 - x) + 1)
    # formerly
    # The FourierMode parameter requires both amplitude and phase angle to be
    # specified. I use the default phase angle because at this point, there's
    # already enough going on angle-wise.
    amplitude_lambda         = lambda x, default_amplitude, default_phase_angle: (
        #((0.75 + x) * default_amplitude),
        (0.05 - 0.001) * (1 - x) + 0.001,
        default_phase_angle
    )

    # Default is 2 modes, F1, F3 (F2 is degenerate with the Power function).
    if '1' in dict_modify_values:
        num_fourier_modes = num_fourier_modes_lambda(dict_modify_values['1'])
    else:
        num_fourier_modes = 2

    # Create new modes with amplitude and phase angle lessened as we increase the mode number
    # This follows general GALFIT convention
    new_fourier_modes = {
        num_mode : (
            0.02 * (num_fourier_modes - num_mode),
            45 * 1/num_mode
        )
        for num_mode in range(1, num_fourier_modes + 1)
        if num_mode != 2
    }
    fourier_object = Fourier(2, n = new_fourier_modes)

    # Modify the Fourier modes individually. And rather than select
    # priority numbers for each, I iterate up from the count value.
    count = 3
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
        dict_modify_values: dict
):
    """
    Modifies the galaxy properties based on the dictionary of note values as (generally) follows:
    (max_value - min_value) * (1 +/- normalized_note_value) + min_value

    Parameters
    ----------
    bulge_object : Sersic
        The galfitlib bulge object to modify
    disk_object : Sersic
        The galfitlib disk object to modify
    arms_object : Power
        The galfitlib arms object to modify
    dict_modify_values : dict
        The dictionary of notes (priority numbers) used to modify the galaxy property

    Returns
    -------
    Fourier object
        As initialized by the music
    """
    # BULGE
    bulge_modify(bulge_object, dict_modify_values)

    # DISK
    disk_modify(disk_object, dict_modify_values)

    # ARMS
    arms_modify(arms_object, dict_modify_values)

    # FOURIER
    # The number of arms depends on the song so the fourier object operates differently
    return fourier_modify(dict_modify_values)
