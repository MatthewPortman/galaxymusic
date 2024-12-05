from pathlib import Path
from copy import deepcopy

from astropy.io import fits
import numpy as np

from _galfitlib.functions.helper_functions import sp, RUN_GALFIT
from _galfitlib.classes.components import Sersic, Power, GalfitHeader, Sky
from _galfitlib.classes.containers import FeedmeContainer
from _galfitlib.utilities.music.galaxy_update_by_music import music_to_galaxy_properties

def galfitting(
        feedme_0: Path,
        input_filename_0: Path,
        output_filename_0: Path,
        gname: str,
        x_pos: int,
        y_pos: int,
        model_offset: int,
        note_priority_map: dict[str, int],
        notes_chunk: list[tuple[str, float]],
        norm_volume: float,
        i: int
):
    """
    Prepares for and runs GALFIT using the modified galaxy properties

    Parameters
    ----------
    feedme_0 : Path
        The path to the feedme file
    input_filename_0 : Path
        The path to the input FITS file
    output_filename_0 : Path
        The path to the output FITS file
    gname : str
        The name of the galaxy
    x_pos : int
        The x-coordinate of the center of the galaxy
    y_pos : int
        The y-coordinate of the center of the galaxy
    model_offset : int
        The offset of the model == half the size of the model
    note_priority_map : dict[str, int]
        The dictionary of notes and their frequency (aka priority)
    notes_chunk : list[tuple[str, float]]
        The list of notes and their normalized frequency differences (deltas)
    norm_volume : float
        The normalized volume
    i : int
        The looping index for naming files

    Returns
    -------
    output_filename : Path
        The path to the output FITS file
    """
    feedme = feedme_0.with_stem(f"{feedme_0.stem}_{i}")

    position = (x_pos, y_pos)

    # Create the components
    # The component number is the order in which the components are added
    # if components share a number, it means that the latter components modify
    # the former, i.e. Power and Fourier modify Sersic
    bulge = Sersic(
            component_number = 1,
            position = position,
    )

    disk = Sersic(
            component_number = 2,
            position = position,
    )

    arms = Power(
            component_number = 2,
            position = position,
    )

    output_filename = output_filename_0.with_stem(f"{output_filename_0.stem}_out_{i}")

    # The header holds hyperparameters for GALFIT
    header = GalfitHeader(
            galaxy_name   = gname,
            input_image   = input_filename_0,
            output_image  = output_filename,
            optimize      = 1,
            region_to_fit = (
                x_pos - model_offset,
                x_pos + model_offset - 1,
                y_pos - model_offset,
                y_pos + model_offset - 1
            )
    )

    # Normalized delta refers to the normalized value
    # (w.r.t the length of the range for a note)
    # of the difference between the note frequency
    # and the start of the note's range.
    priority_numbers_and_norm_delta = {
        str(note_priority_map[note]): norm_delta
        for note, norm_delta in notes_chunk
    }

    priority_numbers_and_norm_delta['RMS'] = norm_volume

    # Updating the components based on the music and extracting the Fourier component
    fourier = music_to_galaxy_properties(
            bulge_object       = bulge,
            disk_object        = disk,
            arms_object        = arms,
            dict_modify_values = priority_numbers_and_norm_delta
    )
    fourier.component_number = 2

    # Creating the FeedmeContainer object from galfitlib and writing to file
    galaxy_feedme = FeedmeContainer(
            path_to_feedme = feedme,
            header         = header,
            bulge          = bulge,
            disk           = disk,
            arms           = arms,
            fourier        = fourier,
            sky            = Sky(3),
            load_default   = False
    )

    galaxy_feedme.to_file()

    # Running GALFIT via subprocess
    _ = sp(f"{RUN_GALFIT} {feedme}")

    return output_filename


def process_galfit_output(
        output_filename: Path,
        height: int,
        width: int,
        x_pos: int,
        y_pos: int,
        model_dim: int,
        model_offset: int
) -> np.ndarray:
    """
    Processes the output from GALFIT. Notably does not use the galfitlib since the
    other utilities therein are unnecessary.

    Parameters
    ----------
    output_filename : Path
        The path to the output FITS file
    height : int
        The height of the image
    width : int
        The width of the image
    x_pos : int
        The x-coordinate of the center of the galaxy
    y_pos : int
        The y-coordinate of the center of the galaxy
    model_dim : int
        The (square) dimension of the model
    model_offset : int
        The offset of the model == half the size of the model

    Returns
    -------
    dummy_array : np.ndarray
        The image data from the FITS file transposed onto a dummy array the size
        of our output image.
    """
    # Open the FITS file
    fits_file = fits.open(str(output_filename))

    # Extract the image data from the FITS file
    # For speed purposes just use Astropy.fits instead of the galfitlib implementation
    image_data_fits = deepcopy(
            fits_file[0].data - float(
                    fits_file[0].header["3_SKY"].split("+")[0].strip()
            )
    )

    # Reposition to use the bottom left corner of the image as the origin for inserting
    # into the dummy array
    x_pos -= model_offset
    y_pos -= model_offset

    dummy_array = np.zeros((height, width))
    dummy_array[x_pos: x_pos + model_dim, y_pos: y_pos + model_dim] = image_data_fits

    # Close the FITS file
    fits_file.close()

    return dummy_array