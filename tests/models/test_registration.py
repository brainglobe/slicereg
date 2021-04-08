import numpy as np
import numpy.testing as npt
import pytest

from slicereg.models.registration import register
from slicereg.models.section import Section, Image
from slicereg.models.transforms import Transform3D
from slicereg.models.atlas import Atlas


def test_section_registration_to_an_atlas_gets_an_image_with_same_image_parameters():
    section = Section(
        image=Image(
            channels=np.random.random((3, 4, 5)),
            i_shift=3,
            j_shift=5,
            theta=20
        ),
        pixel_resolution_um=10,
        plane_3d=Transform3D(x=10, y=-5, z=10),
    )
    atlas = Atlas(volume=np.random.random((5, 5, 5)), resolution_um=20)
    atlas_slice = register(section, atlas)
    assert type(atlas_slice) is Image
    assert atlas_slice.width == section.image.width and atlas_slice.height == section.image.height



# cases = [
#     {
#         "atlas_res": 1,
#         "section_res": 1,
#         "pos": {"x": -1, "y": -1, "z": 0},
#         "expected": [
#             [0, 0, 0],
#             [0, 1, 0],
#             [0, 0, 0],
#         ]
#     },
# ]
# @pytest.mark.parametrize("case", cases)
# def test_section_registration_cuts_correctly_with_diff_resolutions(case):
#     volume = np.zeros((3, 3, 3))
#     volume[1, 1, 1] = 1
#     # volume[1, 2, 1] = 2
#     # volume[2, 1, 1] = 3
#     atlas = Atlas(
#         volume=volume,
#         resolution_um=case['atlas_res'],
#     )
#     section = Section(
#         image=Image(channels=np.ones((1, 3, 3))),
#         pixel_resolution_um=case["section_res"],
#         plane_3d=Transform3D(**case["pos"]),
#     )
#     atlas_slice = register(section, atlas)
#     npt.assert_almost_equal(atlas_slice.channels[0], case['expected'])
