import numpy as np
import numpy.testing as npt
import pytest

from slicereg.models.registration import register
from slicereg.models.section import Section, ImageData
from slicereg.models.transforms import AtlasTransform
from slicereg.models.atlas import Atlas


def test_section_registration_to_an_atlas_gets_a_section_with_same_image_parameters():
    section = Section(
        image=ImageData(
            channels=np.random.random((3, 4, 5)), 
            pixel_resolution_um=10,
            y_shift=3,
            x_shift=5,
            theta=20
        ),
        plane_3d=AtlasTransform(right=10, superior=-5, anterior=10),
        )
    atlas = Atlas(volume=np.random.random((5, 5, 5)), resolution_um=20)
    s2 = register(section, atlas)
    assert type(s2) is Section
    assert s2.id != section.id and s2 is not section
    assert s2.image.pixel_resolution_um == section.image.pixel_resolution_um
    assert s2.image.width == section.image.width and s2.image.height == section.image.height

#
#
# cases = [
#     {
#         "atlas_res": 1,
#         "section_res": 1,
#         "pos": {"right": 0, "superior": 0, "anterior": 0},
#         "expected": [
#             [0, 0, 0],
#             [0, 1, 0],
#             [0, 0, 0],
#         ]
#     },
    # {
    #     "atlas_res": 1,
    #     "section_res": 1,
    #     "pos": {"right": 1, "superior": 1, "anterior": 1},
    #     "expected": [
    #         [1, 0, 0],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 1,
    #     "section_res": 1,
    #     "pos": {"i": 1, "j": 0, "z": 1},
    #     "expected": [
    #         [0, 1, 0],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 1,
    #     "section_res": 1,
    #     "pos": {"i": 0, "j": 1, "z": 1},
    #     "expected": [
    #         [0, 0, 0],
    #         [1, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"i": 19, "j": 8, "z": 15},
    #     "expected": [
    #         [0, 0, 1],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"i": 9, "j": 8, "z": 15},
    #     "expected": [
    #         [0, 0, 0],
    #         [0, 0, 1],
    #         [0, 0, 1],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"i": 15, "j": 15, "z": 11},
    #     "expected": [
    #         [1, 1, 1],
    #         [1, 1, 1],
    #         [1, 1, 1],
    #     ]
    # },
    # {
    #     "atlas_res": 4,  # 0:4, 4:8, 8:12
    #     "section_res": 2,
    #     "pos": {"i": 4, "j": 0, "z": 6},
    #     "expected": [
    #         [0, 0, 1],
    #         [0, 0, 1],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 4,  # 0:4, 4:8, 8:12
    #     "section_res": 4,
    #     "pos": {"i": 0, "j": 0, "z": 4},
    #     "expected": [
    #         [0, 0, 0],
    #         [0, 1, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 1,  # 0:4, 4:8, 8:12
    #     "section_res": 2,
    #     "pos": {"i": 1, "j": 1, "z": 1},
    #     "expected": [
    #         [1, 0, 0],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
# ]
# @pytest.mark.parametrize("case", cases)
# def test_section_registration_cuts_correctly_with_diff_resolutions(case):
#     volume = np.zeros((3, 3, 3))
#     volume[1, 1, 1] = 1
#     atlas = Atlas(
#         volume=volume,
#         resolution_um=case['atlas_res'],
#     )
#     section = Section(
#         image=ImageData(
#             channels=np.ones((1, 3, 3)),
#             pixel_resolution_um=case["section_res"],
#         ),
#         plane_3d=AtlasTransform(**case["pos"]),
#     )
#     atlas_section = register(section, atlas)
#     assert npt.assert_almost_equal(atlas_section.image.channels[0], case['expected'])
