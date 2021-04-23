from functools import partial

import numpy as np
from hypothesis import given
from hypothesis.strategies import floats
from numpy import cos, sin, testing as npt

from slicereg.models.image_transform import ImageTransformer

sensible_floats = partial(floats, allow_nan=False, allow_infinity=False)


@given(theta=sensible_floats(-1000, 1000))
def test_rotation_matrix_corresponds_to_theta_in_degrees(theta):
    transform = ImageTransformer(theta=theta)
    r = np.radians(theta)
    expected = np.array([
        [cos(r), -sin(r), 0, 0],
        [sin(r), cos(r), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    npt.assert_almost_equal(transform.rot_matrix, expected)


@given(i=floats(), j=floats())
def test_shift_matrix_matches_ishift_jshift_values(i, j):
    transform = ImageTransformer(i_shift=i, j_shift=j)
    expected = np.array([
        [1, 0, 0, i],
        [0, 1, 0, j],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    npt.assert_almost_equal(transform.shift_matrix, expected)


def test_centering_origin_applies_correct_shift_based_on_image_dimensions():
    image = ImageTransformer(i_shift=0, j_shift=0)
    image2 = image.shift_origin_to_center()
    assert image2.i_shift == -0.5 and image2.j_shift == -0.5
