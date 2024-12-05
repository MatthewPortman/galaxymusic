def galfitting(
        feedme_0: Path,
        input_filename_0: Path,
        output_filename_0: Path,
        gname: str,
        x_pos: int,
        y_pos: int,
        model_offset: int,
        notes_chunk: list[tuple[str, float]],
        norm_volume: float,
        i: int
):
    """

    """
    feedme = feedme_0.with_stem(f"{feedme_0.stem}_{i}")

    position = (x_pos, y_pos)

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

    header = GalfitHeader(
            galaxy_name = gname,
            input_image = input_filename_0,
            output_image = output_filename,
            optimize = 1,
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

    fourier = music_to_galaxy_properties(
            bulge_object = bulge,
            disk_object = disk,
            arms_object = arms,
            dict_modify_values = priority_numbers_and_norm_delta
    )
    fourier.component_number = 2

    galaxy_feedme = FeedmeContainer(
            path_to_feedme = feedme,
            header = header,
            bulge = bulge,
            disk = disk,
            arms = arms,
            fourier = fourier,
            sky = Sky(3),
            load_default = False
    )

    galaxy_feedme.to_file()

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
    Processes the output from GALFIT
    """
    # Open the FITS file
    fits_file = fits.open(str(output_filename))

    # Extract the image data from the FITS file
    # For speed purposes just use Astropy.fits instead of my implementation
    image_data_fits = deepcopy(
            fits_file[0].data - float(
                    fits_file[0].header["3_SKY"].split("+")[0].strip()
            )
    )

    x_pos -= model_offset
    y_pos -= model_offset

    dummy_array = np.zeros((height, width))
    dummy_array[x_pos: x_pos + model_dim, y_pos: y_pos + model_dim] = image_data_fits

    # Close the FITS file
    fits_file.close()

    return dummy_array