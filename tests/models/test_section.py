from functools import partial

import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import given
from hypothesis.strategies import integers, floats
from numpy import arange, sin, cos, radians
from pytest import approx

from slicereg.models.image import Image
from slicereg.models.section import Section
from slicereg.models.transforms import Transform3D

real_floats = partial(floats, allow_nan=False, allow_infinity=False)


@given(from_resolution=real_floats(10, 50), to_resolution=real_floats(10, 50))
def test_downsampling_image_produces_correct_resolution_and_data_shape(from_resolution, to_resolution):
    section = Section(image=Image(channels=np.arange(24).reshape(1, 6, 4)), pixel_resolution_um=from_resolution)
    section2 = section.resample(resolution_um=to_resolution)
    assert section2.pixel_resolution_um == to_resolution
    assert section2.image.num_channels == section.image.num_channels

    scale_ratio = from_resolution / to_resolution
    assert approx(section.image.width * scale_ratio == section2.image.width, abs=1)
    assert approx(section.image.height * scale_ratio == section2.image.height, abs=1)


@given(to_resolution=integers(-10, 0))
def test_downsampling_beyond_dimensions_produces_valueerror(to_resolution):
    section = Section(image=Image(channels=np.arange(24).reshape(1, 4, 6)), pixel_resolution_um=12)
    with pytest.raises(ValueError, match=r".* positive.*"):
        section.resample(resolution_um=to_resolution)


@given(from_resolution=integers(1, 200), to_resolution=integers(1, 200))
def test_can_set_pixel_resolution_on_section(from_resolution, to_resolution):
    section = Section(image=Image(channels=np.arange(24).reshape(1, 4, 6)), pixel_resolution_um=from_resolution)
    section2 = section.set_pixel_resolution(resolution_um=to_resolution)
    assert section2.pixel_resolution_um == to_resolution
