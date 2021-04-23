from functools import partial

import numpy as np
from hypothesis import given
from hypothesis.strategies import integers, floats
from numpy import testing as npt

from slicereg.models.image import Image
from slicereg.models.image_transform import ImageTransformer
from slicereg.models.section import Section
from tests.models.test_image import sensible_floats

real_floats = partial(floats, allow_nan=False, allow_infinity=False)


@given(width=integers(min_value=1, max_value=100), height=integers(min_value=1, max_value=100),
       j_shift=sensible_floats(min_value=-2, max_value=2), i_shift=sensible_floats(min_value=-2, max_value=2),
       theta=sensible_floats(-10000, 10000),
       )
def test_shift_matrix_is_ij_ordered_and_in_pixel_coordinate_space(width, height, j_shift, i_shift, theta):
    section = Section(
        image=Image(channels=np.empty((2, height, width)), resolution_um=99,),
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

