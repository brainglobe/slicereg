from functools import partial

import numpy as np
import numpy.testing as npt
from hypothesis import given
from hypothesis.strategies import integers, floats
from numpy import sin, cos, radians
from pytest import approx

from slicereg.core.image import Image
from slicereg.core.image_transform import ImageTransformer
from slicereg.core.physical_transform import PhysicalTransformer
from slicereg.core.section import Section
from tests.core.test_image import sensible_floats

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


@given(
    i=integers(0, 10000), j=integers(0, 10000),
    i_shift=real_floats(-2, 2), j_shift=real_floats(-2, 2),
    theta=real_floats(-500, 500),
    x=real_floats(-1e5, 1e5), y=real_floats(-1e5, 1e5), z=real_floats(-1e5, 1e5),
    res=real_floats(1e-4, 1000)
)
def test_can_get_3d_position_from_2d_pixel_coordinate_in_section(i, j, i_shift, j_shift, theta, x, y, z, res):
    section = Section(
        image=Image(channels=np.empty((2, 3, 4)), resolution_um=res),
        image_transform=ImageTransformer(i_shift=i_shift, j_shift=j_shift, theta=theta),
        physical_transform=PhysicalTransformer(x=x, y=y, z=z),
    )

    t = -radians(theta)  # image is left-handed, so flip rotation
    xyz = section.map_ij_to_xyz(i=i, j=j)  # observed 3D positions

    # do shift first, to make final 2d rotation calculation easier https://academo.org/demos/rotation-about-point/
    j2 = (j + (j_shift * section.image.width))
    i2 = (-i - (i_shift * section.image.height))

    expected = (
        (j2 * cos(t) + i2 * sin(t)) * res + x,
        (i2 * cos(t) - j2 * sin(t)) * res + y,
        z,
    )
    assert approx(xyz == expected)