from functools import partial

import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import strategies as st, given
from hypothesis.strategies import integers, floats
from numpy import arange, sin, cos, radians
from pytest import approx

from slicereg.models.image import Image
from slicereg.models.section import Section
from slicereg.models.transforms import AtlasTransform

real_floats = partial(floats, allow_nan=False, allow_infinity=False)

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
        plane_3d=AtlasTransform(x=x, y=y, z=z),
    )
    t = -radians(theta)  # image is left-handed, so flip rotation
    xyz = section.map_ij_to_xyz(i=i, j=j)  # observed 3D positions

    # do shift first, to make final 2d rotation calculation easier https://academo.org/demos/rotation-about-point/
    j2 = ( j + (j_shift * section.image.width))
    i2 = (-i - (i_shift * section.image.height))

    expected = np.array([
        [(j2 * cos(t) + i2 * sin(t)) * res + x],
        [(i2 * cos(t) - j2 * sin(t)) * res + y],
        [z],
        [1],
    ])
    npt.assert_almost_equal(xyz, expected)


np.set_printoptions(precision=5, suppress=True)

#
# @given(width=integers(1, 1000), height=integers(1, 1000), channels=integers(1, 6),
#        r=floats(1, 1000, allow_nan=False, allow_infinity=False))
# def test_image_scale_matrix_converts_pixel_resolution_to_um_space(width, height, channels, r):
#     image = Image(channels=np.random.random(size=(channels, height, width)), pixel_resolution_um=r)
#     expected = np.array([
#         [r, 0, 0, 0],
#         [0, r, 0, 0],
#         [0, 0, 1, 0],
#         [0, 0, 0, 1],
#     ])
#     assert np.all(np.isclose(image.scale_matrix, expected))
#
# @given(i=st.integers(), j=st.integers())
# def test_nonexistent_image_coords_raise_error_and_doesnt_if_exists(i, j):
#     section = Section(
#         image=Image(
#             channels=arange(180).reshape(2, 3, 30),
#             pixel_resolution_um=1
#         ),
#     )
#     if i < 0 or i >= section.image.height or j < 0 or j >= section.image.width:
#         with pytest.raises(ValueError):
#             section.pos_from_coord(i=i, j=j)
#     else:
#         assert section.pos_from_coord(i=i, j=j)
#
#
#
# def test_resample_section_gets_new_section_with_resampled_image():
#     section = Section(image=Image(channels=np.random.random((3, 4, 4)), pixel_resolution_um=12))
#     section2 = section.resample(resolution_um=24)
#     assert isinstance(section2, Section)
#     assert section2.image.pixel_resolution_um == 24
#
#
#
# @given(to_resolution=sensible_floats(0.5, 200))
# def test_downsampling_image_produces_correct_resolution_and_data_shape(to_resolution):
#     from_resolution = 12
#     image = Image(channels=np.arange(24).reshape(1, 6, 4), pixel_resolution_um=from_resolution)
#     image2 = image.resample(resolution_um=to_resolution)
#     assert image2.pixel_resolution_um == to_resolution
#     assert image2.num_channels == image.num_channels
#
#     scale_ratio = from_resolution / to_resolution
#     assert approx(image.width * scale_ratio == image2.width, abs=1)
#     assert approx(image.height * scale_ratio == image2.height, abs=1)
#
#
# @given(to_resolution=floats(allow_infinity=False, allow_nan=False, max_value=0))
# def test_downsampling_beyond_dimensions_produces_valueerror(to_resolution):
#     image = Image(channels=np.arange(24).reshape(1, 4, 6), pixel_resolution_um=12)
#     with pytest.raises(ValueError, match=r".* positive.*"):
#         image.resample(resolution_um=to_resolution)