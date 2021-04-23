from functools import partial

import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import given
from hypothesis.strategies import integers, floats
from numpy import arange, sin, cos, radians
from pytest import approx

from slicereg.models.atlas import Atlas
from slicereg.models.transform_image import ImageTransformer
from slicereg.models.registration import Registration
from slicereg.models.section import Section
from slicereg.models.transforms import Transform3D


def test_section_registration_to_an_atlas_gets_an_image_with_same_image_parameters():
    registration = Registration(
        section=Section(
            image=ImageTransformer(
                channels=np.random.random((3, 4, 5)),
                i_shift=3,
                j_shift=5,
                theta=20
            ),
            pixel_resolution_um=10,
            plane_3d=Transform3D(x=10, y=-5, z=10, rx=20, ry=0, rz=-5),
        ),
        atlas=Atlas(
            volume=np.random.random((5, 5, 5)),
            resolution_um=20
        ),
    )

    atlas_slice = registration.atlas_slice
    assert type(atlas_slice) is ImageTransformer
    assert atlas_slice.width == 5 and atlas_slice.height == 4


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
    registration = Registration(
        section=Section(
            image=ImageTransformer(channels=arange(24).reshape(2, 3, 4), i_shift=i_shift, j_shift=j_shift, theta=theta),
            pixel_resolution_um=res,
            plane_3d=Transform3D(x=x, y=y, z=z),
        ),
        atlas=Atlas(
            volume=np.random.random((5, 5, 5)),
            resolution_um=20
        ),
    )
    t = -radians(theta)  # image is left-handed, so flip rotation
    xyz = registration.map_ij_to_xyz(i=i, j=j)  # observed 3D positions

    # do shift first, to make final 2d rotation calculation easier https://academo.org/demos/rotation-about-point/
    j2 = (j + (j_shift * registration.section.image.width))
    i2 = (-i - (i_shift * registration.section.image.height))

    expected = (
        (j2 * cos(t) + i2 * sin(t)) * res + x,
        (i2 * cos(t) - j2 * sin(t)) * res + y,
        z,
    )
    assert approx(xyz == expected)


cases = [
    {
        "atlas_res": 1,
        "section_res": 1,
        "pos": {"x": 0, "y": 0, "z": 1},
        "expected": [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
    },
    {
        "atlas_res": 1,
        "section_res": 1,
        "pos": {"x": 0, "y": -1, "z": 1},
        "expected": [
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    },
    {
        "atlas_res": 1,
        "section_res": 1,
        "pos": {"x": 1, "y": 1, "z": 1},
        "expected": [
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
        ]
    },
    {
        "atlas_res": 10,
        "section_res": 1,
        "pos": {"x": 1, "y": 1, "z": 1},
        "expected": [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    },
    {
        "atlas_res": 10,
        "section_res": 1,
        "pos": {"x": 15, "y": -15, "z": 15},
        "expected": [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
    },
    {
        "atlas_res": 10,
        "section_res": 1,
        "pos": {"x": 8, "y": -9, "z": 15},
        "expected": [
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, 1],
        ]
    },
]


@pytest.mark.parametrize("case", cases)
def test_section_registration_cuts_correctly_with_diff_resolutions(case):
    volume = np.zeros((3, 3, 3))
    volume[1, 1, 1] = 1
    registration = Registration(
        section=Section(
            image=ImageTransformer(channels=np.ones((1, 3, 3))),
            pixel_resolution_um=case["section_res"],
            plane_3d=Transform3D(**case["pos"]),
        ),
        atlas=Atlas(
            volume=volume,
            resolution_um=case['atlas_res'],
        )
    )
    atlas_slice = registration.atlas_slice
    npt.assert_almost_equal(atlas_slice.channels[0], case['expected'])
