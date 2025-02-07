import pytest
# from pathlib import Path

# pj = Path

# import sys

from galfitlib.classes.parameters import *

# from galfitlib import __file__ as galfitlib_file
# LIBRARY_DIR = Path(galfitlib_file).parent.absolute()

# REG_TEST_DIR    = pj(LIBRARY_DIR, "galfitlib", "tests")
# TEST_OUTPUT_DIR = pj(REG_TEST_DIR, "output")

# For these *lesser* classes, I test the str output and the new
# value assignment. Other attributes are checked in/for
# GalfitParameter in test_GalfitParameter.py
def test_component_type():
    comp_type = ComponentType(
            name = "sersic"
    )

    assert comp_type.value == "sersic"
    assert comp_type.fix   == ""
    assert str(comp_type)  == " 0) sersic              # Component type"

    comp_type.value         = "expdisk"
    assert comp_type.value == "expdisk"
    assert str(comp_type)  == " 0) expdisk             # Component type"

def test_header_parameter():
    header_param = HeaderParameter(
            value            = "test.fits",
            name             = "input image",
            parameter_number = "A",
            comment          = "Input data image"
    )
    assert header_param.value == "test.fits"
    assert header_param.fix   == ""
    assert str(header_param)  == "A) test.fits            # Input data image"

    header_param.value         = "test2.fits"
    assert header_param.value == "test2.fits"
    assert str(header_param)  == "A) test2.fits           # Input data image"

def test_num_parameter():
    num_param = NumParameter(
            value            = 10.12345,
            name             = "magnitude",
            parameter_number = 3,
            comment          = "Integrated magnitude"
    )
    assert num_param.value == 10.1235
    assert num_param.fix   == 1
    assert str(num_param)  == " 3) 10.1235     1       # Integrated magnitude"

    num_param.value         = 20.6789111
    assert num_param.value == 20.6789
    assert str(num_param)  == " 3) 20.6789     1       # Integrated magnitude"

def test_skip():
    skip = Skip(
            value = 0
    )
    assert skip.value == 0
    assert skip.fix   == ""
    assert str(skip)  == " Z) 0                   # Skip this model in output image?  (yes=1, no=0)"

    skip.value         = 1
    assert skip.value == 1
    assert str(skip)  == " Z) 1                   # Skip this model in output image?  (yes=1, no=0)"

    with pytest.raises(Exception):
        skip.value    = 2

def test_bending_mode():
    bending_mode = BendingMode(
            mode = 2,
            amplitude = 1.002
    )
    assert bending_mode.mode             == 2
    assert bending_mode.parameter_number == "2"

    assert bending_mode.amplitude == 1.002
    assert bending_mode.value     == 1.002

    assert bending_mode.fix       == 1

    assert str(bending_mode) == "B2) 1.002       1       # Bending mode 2 amplitude"

    bending_mode.mode                     = 3
    assert bending_mode.mode             == 3
    assert bending_mode.parameter_number == "3"
    assert bending_mode.comment          == "Bending mode 3 amplitude"

    bending_mode.amplitude         = 2.004
    assert bending_mode.amplitude == 2.004

    assert str(bending_mode) == "B3) 2.004       1       # Bending mode 3 amplitude"

def test_position():
    position = Position(
            value = (100, 100)
    )
    assert position.value == ntMultiParameter(100, 100)
    assert position.fix   == ntMultiParameter(0, 0)
    assert str(position)  == " 1) 100 100     0  0    # Position x, y"

    position.value         = (200, 200)
    assert position.value == ntMultiParameter(200, 200)
    assert str(position)  == " 1) 200 200     0  0    # Position x, y"

    position.x            = 300
    assert position.value == ntMultiParameter(300, 200)

    position.y            = 400
    assert position.value == ntMultiParameter(300, 400)

    assert str(position)  == " 1) 300 400     0  0    # Position x, y"

def test_fourier_mode():
    fourier_mode = FourierMode(
            mode        = 1,
            amplitude   = 0.05,
            phase_angle = 45
    )


    assert fourier_mode.value       == ntFourier(0.05, 45)
    assert fourier_mode.amplitude   == 0.05
    assert fourier_mode.phase_angle == 45

    assert fourier_mode.fix             == ntFourier(1, 1)
    assert fourier_mode.fix_amplitude   == 1
    assert fourier_mode.fix_phase_angle == 1

    assert fourier_mode.mode == 1
    assert str(fourier_mode) == "F1) 0.0500 45   1  1    # Azim. Fourier mode 1, amplitude, & phase angle"

    fourier_mode.value         = (0.1, 90)
    assert fourier_mode.value == ntFourier(0.1, 90)
    assert str(fourier_mode)  == "F1) 0.1000 90   1  1    # Azim. Fourier mode 1, amplitude, & phase angle"

    fourier_mode.amplitude     = 0.2
    assert fourier_mode.value == ntFourier(0.2, 90)

    fourier_mode.phase_angle   = 180
    assert fourier_mode.value == ntFourier(0.2, 180)

    fourier_mode.mode          = 2
    assert str(fourier_mode)  == "F2) 0.2000 180  1  1    # Azim. Fourier mode 2, amplitude, & phase angle"

def test_image_region_to_fit():
    region = ImageRegionToFit(
            value = (0, 256, 0, 256)
    )
    assert region.value == ntImageRegionToFit(0, 256, 0, 256)

    assert region.xmin  == 0
    assert region.x1    == 0
    assert region.xmax  == 256
    assert region.x2    == 256

    assert region.ymin  == 0
    assert region.y1    == 0
    assert region.ymax  == 256
    assert region.y2    == 256

    assert region.fix   == ntMultiParameter("", "")

    assert str(region)  == "H) 0    256  0    256   # Image region to fit (xmin xmax ymin ymax)"


    region.value         = (10, 246, 10, 246)
    assert region.value == ntImageRegionToFit(10, 246, 10, 246)
    assert str(region)  == "H) 10   246  10   246   # Image region to fit (xmin xmax ymin ymax)"

    region.xmin          = 20
    assert region.value == ntImageRegionToFit(20, 246, 10, 246)

    region.xmax          = 236
    assert region.value == ntImageRegionToFit(20, 236, 10, 246)

    region.ymin          = 20
    assert region.value == ntImageRegionToFit(20, 236, 20, 246)

    region.ymax          = 236
    assert region.value == ntImageRegionToFit(20, 236, 20, 236)

    assert str(region)  == "H) 20   236  20   236   # Image region to fit (xmin xmax ymin ymax)"

def test_crop_region():
    region = ImageRegionToFit(
            value = (45, 145, 45, 145)
    )

    crop_region = CropRegion(
            value = (45, 145, 45, 145)
    )

    assert region == crop_region

def test_convolution_box():
    conv_box = ConvolutionBox(
            value = (52, 52)
    )
    assert conv_box.value == ntConvolutionBox(52, 52)
    assert conv_box.x     == 52
    assert conv_box.y     == 52

    assert conv_box.fix   == ("", "")

    assert str(conv_box)  == "I) 52     52            # Size of the convolution box (x y)"

    conv_box.value         = (100, 100)
    assert conv_box.value == ntConvolutionBox(100, 100)
    assert str(conv_box)  == "I) 100    100           # Size of the convolution box (x y)"

    conv_box.x             = 200
    assert conv_box.value == ntConvolutionBox(200, 100)

    conv_box.y             = 200
    assert conv_box.value == ntConvolutionBox(200, 200)

    assert str(conv_box)  == "I) 200    200           # Size of the convolution box (x y)"

def test_plate_scale():
    plate_scale = PlateScale(
            value = (0.396, 0.396)
    )
    assert plate_scale.value == ntPlateScale(0.396, 0.396)

    assert plate_scale.dx    == 0.396
    assert plate_scale.x     == 0.396

    assert plate_scale.dy    == 0.396
    assert plate_scale.y     == 0.396

    assert plate_scale.fix   == ntMultiParameter("", "")

    assert str(plate_scale)  == "K) 0.396  0.396         # Plate scale (dx dy)   [arcsec per pixel]"

    plate_scale.value         = (0.5, 0.5)
    assert plate_scale.value == ntPlateScale(0.5, 0.5)
    assert str(plate_scale)  == "K) 0.5    0.5           # Plate scale (dx dy)   [arcsec per pixel]"

    plate_scale.dx            = 0.6
    assert plate_scale.value == ntPlateScale(0.6, 0.5)

    plate_scale.dy            = 0.6
    assert plate_scale.value == ntPlateScale(0.6, 0.6)

    assert str(plate_scale)  == "K) 0.6    0.6           # Plate scale (dx dy)   [arcsec per pixel]"
