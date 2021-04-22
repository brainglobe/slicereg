from functools import partial

import numpy as np
import numpy.testing as npt
import pytest
from pytest import approx
from hypothesis import given
from hypothesis.strategies import integers, floats, booleans

from slicereg.models.image import Image, ij_homog

sensible_floats = partial(floats, allow_nan=False, allow_infinity=False)

np.random.seed(100)  # todo: replace with SeedGenerator, get better control

cases = [
    ((2, 3, 2), 2),
    ((6, 30, 10), 6),
]
@pytest.mark.parametrize('shape,num_channels', cases)
def test_image_reports_correct_number_of_channels(shape, num_channels):
    image = Image(channels=np.random.random(size=shape))
    assert image.num_channels == num_channels


cases = [
    ((2, 3, 4), 4),
    ((6, 30, 10), 10),
]
@pytest.mark.parametrize('shape,width', cases)
def test_image_width(shape, width):
    image = Image(channels=np.random.random(size=shape))
    assert image.width == width


cases = [
    ((2, 3, 2), 3),
    ((6, 30, 10), 30),
]
@pytest.mark.parametrize('shape,height', cases)
def test_image_height(shape, height):
    image = Image(channels=np.random.random(size=shape))
    assert image.height == height


@given(height=integers(1, 20), width=integers(1, 20))
def test_inds_homog_has_correct_shape(height, width):
    image = Image(channels=np.random.random(size=(3, height, width)))
    assert image.inds_homog.shape == (4, height * width)


def test_inds_homog_example():
    image = Image(channels=np.random.random(size=(3, 2, 3)))
    expected = np.array([
        [0, 0, 0, 1, 1, 1],
        [0, 1, 2, 0, 1, 2],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
    ])
    npt.assert_equal(image.inds_homog, expected)


@given(theta=sensible_floats(-1000, 1000))
def test_rotation_matrix_corresponds_to_theta_in_degrees(theta):
    image = Image(channels=np.arange(24).reshape(1, 6, 4), theta=theta)
    r = np.radians(theta)
    expected = np.array([
        [np.cos(r), -np.sin(r), 0, 0],
        [np.sin(r),  np.cos(r), 0, 0],
        [        0,          0, 1, 0],
        [        0,          0, 0, 1],
    ])
    npt.assert_almost_equal(image.rot_matrix, expected)


@given(width=integers(min_value=1, max_value=100), height=integers(min_value=1, max_value=100),
       j_shift=sensible_floats(min_value=-2, max_value=2), i_shift=sensible_floats(min_value=-2, max_value=2),
       )
def test_shift_matrix_is_ij_ordered_and_in_pixel_coordinate_space(width, height, j_shift, i_shift):
    image = Image(channels=np.random.random((2, height, width)), i_shift = i_shift, j_shift = j_shift)
    expected_shift_matrix = np.array([
        [1, 0, 0, i_shift * height],
        [0, 1, 0, j_shift * width],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    npt.assert_almost_equal(image.shift_matrix, expected_shift_matrix)


@given(i=integers(), j=integers())
def test_homogonous_coords_are_ij_ordered_and_a_column(i, j):
    coords = ij_homog(i=i, j=j)
    expected = np.array([
        [i],
        [j],
        [0],
        [1],
    ])
    npt.assert_equal(coords, expected)


@given(i_shift=sensible_floats(-20, 20), j_shift=sensible_floats(-20, 20), theta=sensible_floats(-10000, 10000))
def test_planes_affine_transform_with_rotation_is_correct_for_all_resolutions(i_shift, j_shift, theta):
    image = Image(channels=np.random.random((2, 10, 10)), i_shift=i_shift, j_shift=j_shift, theta=theta)
    expected = image.rot_matrix @ image.shift_matrix
    npt.assert_almost_equal(image.affine_transform, expected)


def test_centering_origin_applies_correct_shift_based_on_image_dimensions():
    image = Image(channels=np.random.random((2, 10, 12)), i_shift=0, j_shift=0)
    image2 = image.shift_origin_to_center()
    assert image2.i_shift == -0.5 and image2.j_shift == -0.5



