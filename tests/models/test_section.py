from functools import partial

import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import integers, floats
from numpy import testing as npt
from pytest import approx

from slicereg.models.image import Image
from slicereg.models.transform_image import ImageTransformer
from slicereg.models.section import Section
from tests.models.test_image import sensible_floats

real_floats = partial(floats, allow_nan=False, allow_infinity=False)


@given(from_resolution=real_floats(10, 50), to_resolution=real_floats(10, 50))
def test_downsampling_image_produces_correct_resolution_and_data_shape(from_resolution, to_resolution):
    section = Section(image=ImageTransformer(channels=np.arange(24).reshape(1, 6, 4)), pixel_resolution_um=from_resolution)
    section2 = section.resample(resolution_um=to_resolution)
    assert section2.pixel_resolution_um == to_resolution
    assert section2.image.num_channels == section.image.num_channels

    scale_ratio = from_resolution / to_resolution
    assert approx(section.image.width * scale_ratio == section2.image.width, abs=1)
    assert approx(section.image.height * scale_ratio == section2.image.height, abs=1)


@given(to_resolution=integers(-10, 0))
def test_downsampling_beyond_dimensions_produces_valueerror(to_resolution):
    section = Section(image=ImageTransformer(channels=np.arange(24).reshape(1, 4, 6)), pixel_resolution_um=12)
    with pytest.raises(ValueError, match=r".* positive.*"):
        section.resample(resolution_um=to_resolution)


@given(from_resolution=integers(1, 200), to_resolution=integers(1, 200))
def test_can_set_pixel_resolution_on_section(from_resolution, to_resolution):
    section = Section(image=ImageTransformer(channels=np.arange(24).reshape(1, 4, 6)), pixel_resolution_um=from_resolution)
    section2 = section.set_pixel_resolution(resolution_um=to_resolution)
    assert section2.pixel_resolution_um == to_resolution


@given(width=integers(min_value=1, max_value=100), height=integers(min_value=1, max_value=100),
       j_shift=sensible_floats(min_value=-2, max_value=2), i_shift=sensible_floats(min_value=-2, max_value=2),
       theta=sensible_floats(-10000, 10000),
       )
def test_shift_matrix_is_ij_ordered_and_in_pixel_coordinate_space(width, height, j_shift, i_shift, theta):
    section = Section(
        image=Image(channels=np.empty((2, height, width))),
        pixel_resolution_um=99,
        image_transform=ImageTransformer(i_shift=i_shift, j_shift=j_shift, theta=theta)
    )
    expected_shift_matrix = np.array([
        [1, 0, 0, i_shift * height],
        [0, 1, 0, j_shift * width],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    expected_image_transform = section.image_transform.rot_matrix @ expected_shift_matrix
    npt.assert_almost_equal(section._image_transform_matrix, expected_image_transform)

