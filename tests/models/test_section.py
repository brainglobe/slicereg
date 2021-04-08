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
np.set_printoptions(precision=5, suppress=True)


@given(
    i=integers(0, 1e5), j=integers(0, 1e5),
    i_shift=real_floats(-2, 2), j_shift=real_floats(-2, 2),
    theta=real_floats(-500, 500),
    x=real_floats(-1e5, 1e5), y=real_floats(-1e5, 1e5), z=real_floats(-1e5, 1e5),
    res=real_floats(1e-4, 1000)
)
def test_can_get_3d_position_from_2d_pixel_coordinate_in_section(i, j, i_shift, j_shift, theta, x, y, z, res):
    section = Section(
        image=Image(channels=arange(24).reshape(2, 3, 4), i_shift=i_shift, j_shift=j_shift, theta=theta),
        pixel_resolution_um=res,
        plane_3d=Transform3D(x=x, y=y, z=z),
    )
    t = -radians(theta)  # image is left-handed, so flip rotation
    xyz = section.map_ij_to_xyz(i=i, j=j)  # observed 3D positions

    # do shift first, to make final 2d rotation calculation easier https://academo.org/demos/rotation-about-point/
    j2 = (j + (j_shift * section.image.width))
    i2 = (-i - (i_shift * section.image.height))

    expected = np.array([
        [(j2 * cos(t) + i2 * sin(t)) * res + x],
        [(i2 * cos(t) - j2 * sin(t)) * res + y],
        [z],
        [1],
    ])
    npt.assert_almost_equal(xyz, expected)


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
