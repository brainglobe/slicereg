from functools import partial

import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import given
from hypothesis.strategies import integers, floats

from slicereg.models.image import ImageTransformer, Image
from slicereg.models.registration import ij_homog

sensible_floats = partial(floats, allow_nan=False, allow_infinity=False)

np.random.seed(100)  # todo: replace with SeedGenerator, get better control


@given(chans=integers(1, 8), height=integers(1, 50), width=integers(1, 50))
def test_image_reports_correct_dimensions(chans, height, width):
    image = Image(channels=np.random.random(size=(chans, height, width)))
    assert image.num_channels == chans
    assert image.height == height
    assert image.width == width


@given(chans=integers(1, 3), height=integers(1, 20), width=integers(1, 20))
def test_inds_homog_has_correct_shape(chans, height, width):
    image = Image(channels=np.random.random(size=(chans, height, width)))
    assert image.inds_homog.shape == (4, height * width)


def test_inds_homog_example():
    image = Image(channels=np.empty(shape=(3, 2, 3)))
    expected = np.array([
        [0, 0, 0, 1, 1, 1],
        [0, 1, 2, 0, 1, 2],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
    ])
    npt.assert_equal(image.inds_homog, expected)


@given(width=integers(1, 50), height=integers(1, 50))
def test_full_shift_matrix_is_height_and_width_of_image(width, height):
    image = Image(channels=np.empty(shape=(2, height, width)))
    expected = np.array([
        [1, 0, 0, height],
        [0, 1, 0, width],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    npt.assert_equal(image.full_shift_matrix, expected)


@given(theta=sensible_floats(-1000, 1000))
def test_rotation_matrix_corresponds_to_theta_in_degrees(theta):
    transform = ImageTransformer(theta=theta)
    r = np.radians(theta)
    expected = np.array([
        [np.cos(r), -np.sin(r), 0, 0],
        [np.sin(r),  np.cos(r), 0, 0],
        [        0,          0, 1, 0],
        [        0,          0, 0, 1],
    ])
    npt.assert_almost_equal(transform.rot_matrix, expected)


@given(ishift=floats(), jshift=floats())
def test_shift_matrix_matches_ishift_jshift_values(ishift, jshift):
    transform = ImageTransformer(i_shift=ishift, j_shift=jshift)
    expected = np.array([
        [1, 0, 0, ishift],
        [0, 1, 0, jshift],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    npt.assert_almost_equal(transform.shift_matrix, expected)


def test_centering_origin_applies_correct_shift_based_on_image_dimensions():
    image = ImageTransformer(i_shift=0, j_shift=0)
    image2 = image.shift_origin_to_center()
    assert image2.i_shift == -0.5 and image2.j_shift == -0.5



@given(width=integers(min_value=1, max_value=100), height=integers(min_value=1, max_value=100),
       j_shift=sensible_floats(min_value=-2, max_value=2), i_shift=sensible_floats(min_value=-2, max_value=2),
       )
def test_shift_matrix_is_ij_ordered_and_in_pixel_coordinate_space(width, height, j_shift, i_shift):
    image = ImageTransformer(channels=np.random.random((2, height, width)), i_shift = i_shift, j_shift = j_shift)
    expected_shift_matrix = np.array([
        [1, 0, 0, i_shift * height],
        [0, 1, 0, j_shift * width],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    npt.assert_almost_equal(image.shift_matrix, expected_shift_matrix)



@given(i_shift=sensible_floats(-20, 20), j_shift=sensible_floats(-20, 20), theta=sensible_floats(-10000, 10000))
def test_planes_affine_transform_with_rotation_is_correct_for_all_resolutions(i_shift, j_shift, theta):
    image = ImageTransformer(channels=np.random.random((2, 10, 10)), i_shift=i_shift, j_shift=j_shift, theta=theta)
    expected = image.rot_matrix @ image.shift_matrix
    npt.assert_almost_equal(image.affine_transform, expected)






