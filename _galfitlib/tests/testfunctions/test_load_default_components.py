import pytest
from pathlib import Path

pj = Path

import sys

from galfitlib import __file__ as galfitlib_file
LIBRARY_DIR = Path(galfitlib_file).parent.absolute()

from galfitlib.functions.load_default_components import *

REG_TEST_DIR    = pj(LIBRARY_DIR, "tests")
TEST_OUTPUT_DIR = pj(REG_TEST_DIR, "output")
# TEST_DATA_DIR = pj(REG_TEST_DIR, "data")
# SAMPLE_DIR = pj(TEST_DATA_DIR, "samples")

import pytest
from galfitlib.functions.load_default_components import *

@pytest.fixture(scope="module")
def setup_load_default_components():
    yield load_default_components()

@pytest.fixture(scope="module")
def setup_function_check_from_default(setup_load_default_components):

    USE_SERSIC      = False
    USE_POWER       = False
    USE_FOURIER     = False
    USE_SKY         = False
    USE_BENDING     = False
    USE_NUKER       = False
    USE_EXPONENTIAL = False
    USE_GAUSSIAN    = False
    USE_FERRER      = False
    USE_KING        = False
    USE_MOFFAT      = False
    USE_EDGEON      = False
    USE_PSF         = False
    USE_LOGPOWER    = False
    USE_TRUNCATION  = False

    if "sersic" in setup_load_default_components:
        USE_SERSIC = True

    if "power" in setup_load_default_components:
        USE_POWER = True

    if "fourier" in setup_load_default_components:
        USE_FOURIER = True

    if "sky" in setup_load_default_components:
        USE_SKY = True

    if "bending" in setup_load_default_components:
        USE_BENDING = True

    if "nuker" in setup_load_default_components:
        USE_NUKER = True

    if "exponential" in setup_load_default_components:
        USE_EXPONENTIAL = True

    if "gaussian" in setup_load_default_components:
        USE_GAUSSIAN = True

    if "ferrer" in setup_load_default_components:
        USE_FERRER = True

    if "king" in setup_load_default_components:
        USE_KING = True

    if "moffat" in setup_load_default_components:
        USE_MOFFAT = True

    if "edgeon" in setup_load_default_components:
        USE_EDGEON = True

    if "psf" in setup_load_default_components:
        USE_PSF = True

    if "logpower" in setup_load_default_components:
        USE_LOGPOWER = True

    if "truncation" in setup_load_default_components:
        USE_TRUNCATION = True

    function_bool_dict = {
        "sersic"      : USE_SERSIC,
        "power"       : USE_POWER,
        "fourier"     : USE_FOURIER,
        "sky"         : USE_SKY,
        "bending"     : USE_BENDING,
        "nuker"       : USE_NUKER,
        "exponential" : USE_EXPONENTIAL,
        "gaussian"    : USE_GAUSSIAN,
        "ferrer"      : USE_FERRER,
        "king"        : USE_KING,
        "moffat"      : USE_MOFFAT,
        "edgeon"      : USE_EDGEON,
        "psf"         : USE_PSF,
        "logpower"    : USE_LOGPOWER,
        "truncation"  : USE_TRUNCATION
    }

    yield function_bool_dict

def test_load_default_components_header(setup_load_default_components):
    # Attempting to set this up agnostic to the choice of defaults

    # Header should/will always be there
    # if "header" in default_components:
    header_params = setup_load_default_components["header"]

    assert header_params         == load_default_header_parameters()

    assert all(
            [
                isinstance(v, HeaderParameter)
                for v in header_params.values()
            ]
    )

    assert "input_image"         in header_params
    assert "output_image"        in header_params
    assert "sigma_image"         in header_params
    assert "psf"                 in header_params
    assert "psf_fine_sampling"   in header_params
    assert "pixel_mask"          in header_params
    assert "constraint_file"     in header_params

    assert "region_to_fit"       in header_params
    assert isinstance(header_params["region_to_fit"], ImageRegionToFit)

    assert "convolution_box"     in header_params
    assert isinstance(header_params["convolution_box"], ConvolutionBox)

    assert "mag_photo_zeropoint" in header_params
    assert "plate_scale"         in header_params
    assert "display_type"        in header_params
    assert "optimize"            in header_params


def test_load_default_components_sersic(
        setup_load_default_components,
        setup_function_check_from_default
):
    # Boolean
    if setup_function_check_from_default["sersic"]:
        sersic_params = setup_load_default_components["sersic"]

        print(sersic_params)
        print(load_default_sersic_parameters())

        # I check the string representation of the dictionaries
        # instead of the dictionaries themselves to avoid an
        # error due to certain values (position) inside the
        # dictionaries being different objects
        assert str(sersic_params) == str(load_default_sersic_parameters())

        assert all(
                [
                    isinstance(v, NumParameter)
                    for k, v in sersic_params.items()
                    if k not in ("position", "skip", "_sersic")
                ]
        )

        assert "_sersic"           in sersic_params
        assert isinstance(sersic_params["_sersic"], ComponentType)
        assert isinstance(sersic_params["_sersic"].value, str)

        assert "position"         in sersic_params
        assert isinstance(sersic_params["position"], Position)
        assert isinstance(sersic_params["position"].value, ntMultiParameter)

        assert "magnitude"        in sersic_params
        assert "effective_radius" in sersic_params
        assert "sersic_index"     in sersic_params
        assert "axis_ratio"       in sersic_params
        assert "position_angle"   in sersic_params
        assert "skip"             in sersic_params
        assert isinstance(sersic_params["skip"], Skip)
        assert isinstance(sersic_params["skip"].value, int)


def test_load_default_components_power(
        setup_load_default_components,
        setup_function_check_from_default
):
    if setup_function_check_from_default["power"]:
        power_params = setup_load_default_components["power"]

        assert power_params == load_default_power_parameters()

        assert all(
                [
                    isinstance(v, NumParameter)
                    for k, v in power_params.items()
                    if k not in ("_power")
                ]
        )

        assert "_power" in power_params
        assert isinstance(power_params["_power"], ComponentType)
        assert isinstance(power_params["_power"].value, str)

        assert "inner_radius"        in power_params
        assert "outer_radius"        in power_params
        assert "cumulative_rotation" in power_params
        assert "powerlaw_index"      in power_params
        assert "inclination"         in power_params
        assert "sky_position_angle"  in power_params

def test_load_default_components_fourier(
        setup_load_default_components,
        setup_function_check_from_default
):
    if setup_function_check_from_default["fourier"]:
        fourier_params = setup_load_default_components["fourier"]

        # Same trick as above
        assert str(fourier_params) == str(load_default_fourier_parameters())

        assert all(
                [
                    isinstance(v, FourierMode)
                    for k, v in fourier_params.items()
                    if k not in ("skip")
                ]
        )

        num_fourier_modes = sum(
                [
                    f"F{i}" in fourier_params for i in range(10)
                ]
        )

        # There should be at least one mode in the default!
        assert num_fourier_modes > 0

        assert "skip"            in fourier_params
        assert isinstance(fourier_params["skip"], Skip)
        assert isinstance(fourier_params["skip"].value, int)

def test_load_default_components_sky(
        setup_load_default_components,
        setup_function_check_from_default
):
    if setup_function_check_from_default["sky"]:
        sky_params = setup_load_default_components["sky"]

        assert all(
                [
                    isinstance(v, NumParameter)
                    for k, v in sky_params.items()
                    if k not in ("skip", "_sky")
                ]
        )

        assert sky_params       == load_default_sky_parameters()

        assert "_sky"           in sky_params
        assert isinstance(sky_params["_sky"], ComponentType)
        assert isinstance(sky_params["_sky"].value, str)

        assert "sky_background" in sky_params
        assert "dsky_dx"        in sky_params
        assert "dsky_dy"        in sky_params
        assert "skip"           in sky_params

def test_load_default_components_bending(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_nuker(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_exponential(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_gaussian(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_ferrer(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_king(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_moffat(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_edgeon(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_psf(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_logpower(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass

def test_load_default_components_truncation(
        setup_load_default_components,
        setup_function_check_from_default
):
    pass
