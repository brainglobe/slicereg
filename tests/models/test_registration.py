from functools import partial

import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import given
from hypothesis.strategies import integers, floats
from numpy import arange, sin, cos, radians
from pytest import approx

from slicereg.models.atlas import Atlas
from slicereg.models.image import Image
from slicereg.models.image_transform import ImageTransformer
from slicereg.models.registration import Registration
from slicereg.models.section import Section
from slicereg.models.physical_transform import PhysicalTransformer


def test_section_registration_to_an_atlas_gets_an_image_with_same_image_parameters():
    registration = Registration(
        section=Section(
            image=Image(channels=np.empty((3, 4, 5)), resolution_um=10),
            image_transform=ImageTransformer(i_shift=3, j_shift=5, theta=20),
            physical_transform=PhysicalTransformer(x=10, y=-5, z=10, rx=20, ry=0, rz=-5),
        ),
        atlas=Atlas(
            volume=np.empty((5, 5, 5)),
            resolution_um=20
        ),
    )

    atlas_slice = registration.slice_atlas()
    assert type(atlas_slice) is ImageTransformer
    assert atlas_slice.width == 5 and atlas_slice.height == 4


real_floats = partial(floats, allow_nan=False, allow_infinity=False)
np.set_printoptions(precision=5, suppress=True)


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
            image=Image(channels=np.ones((1, 3, 3)), resolution_um=case["section_res"]),
            physical_transform=PhysicalTransformer(**case["pos"]),
        ),
        atlas=Atlas(
            volume=volume,
            resolution_um=case['atlas_res'],
        )
    )
    atlas_slice = registration.slice_atlas()
    npt.assert_almost_equal(atlas_slice.channels[0], case['expected'])
