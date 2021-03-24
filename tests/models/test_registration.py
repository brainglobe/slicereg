import numpy as np
import pytest

from slicereg.models.registration import register
from slicereg.models.section import Section, ImageData
from slicereg.models.transforms import Plane2D, Plane3D
from slicereg.models.atlas import Atlas


def test_section_registration_to_an_atlas_gets_a_section_that_matches_sections_parameters():
    section = Section(
        image=ImageData(
            channels=np.random.random((3, 4, 5)), 
            pixel_resolution_um=10,
        ),
        plane_2d=Plane2D(x=3, y=5, theta=20),
        plane_3d=Plane3D(x=10, y=-5, z=10),
        )
    atlas = Atlas(volume=np.random.random((5, 5, 5)), resolution_um=20)
    s2 = register(section, atlas)
    assert type(s2) is Section
    assert s2.image.pixel_resolution_um == section.image.pixel_resolution_um
    assert s2.id != section.id and s2 is not section
    assert s2.image.width == section.image.width, f"{s2.image.channels.shape}, {section.image.channels.shape}"
    assert s2.image.height == section.image.height
    assert np.all(np.isclose(s2.affine_transform, section.affine_transform))



def test_section_registration_cuts_correctly():
    volume = np.zeros((3, 3, 3))
    volume[1, 1, 1] = 1 

    atlas = Atlas(
        volume=volume,
        resolution_um=1.,
    )
    section = Section(
        image=ImageData(channels=np.ones((1, 3, 3)), pixel_resolution_um=1.),
        plane_3d=Plane3D(z=1),
    )
    atlas_slice = register(section, atlas).image.channels[0]
    expected_slice = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ])
    assert np.all(atlas_slice == expected_slice)
    

cases = [
    {
        "atlas_res": 1,
        "section_res": 1,
        "pos": {"x": 1, "y": 1, "z": 1},
        "expected": [
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    },
    {
        "atlas_res": 1,
        "section_res": 1,
        "pos": {"x": 0, "y": 1, "z": 1},
        "expected": [
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 19, "y": 8, "z": 15},
    #     "expected": [
    #         [0, 0, 0],
    #         [0, 0, 0],
    #         [1, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 19, "y": 8, "z": 15},
    #     "expected": [
    #         [0, 0, 1],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 19, "y": 19, "z": 15},
    #     "expected": [
    #         [1, 0, 0],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 19, "y": 15, "z": 15},
    #     "expected": [
    #         [1, 1, 1],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 15, "y": 19, "z": 15},
    #     "expected": [
    #         [1, 0, 0],
    #         [1, 0, 0],
    #         [1, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 15, "y": 15, "z": 15},
    #     "expected": [
    #         [1, 1, 1],
    #         [1, 1, 1],
    #         [1, 1, 1],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 9, "y": 8, "z": 15},
    #     "expected": [
    #         [0, 0, 0],
    #         [0, 0, 1],
    #         [0, 0, 1],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 13, "y": 16, "z": 12},
    #     "expected": [
    #         [1, 1, 1],
    #         [1, 1, 1],
    #         [1, 1, 1],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 5, "y": 23, "z": 28},
    #     "expected": [
    #         [0, 0, 0],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 10,
    #     "section_res": 1,
    #     "pos": {"x": 500, "y": 230, "z": 280},
    #     "expected": [
    #         [0, 0, 0],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 4,
    #     "section_res": 2,
    #     "pos": {"x": 5, "y": 3, "z": 5},
    #     "expected": [
    #         [0, 0, 1],
    #         [0, 0, 1],
    #         [0, 0, 1],
    #     ]
    # },
    # {
    #     "atlas_res": 1,
    #     "section_res": 1,
    #     "pos": {"x": 0, "y": 0, "z": 1},
    #     "expected": [
    #         [0, 0, 0],
    #         [0, 1, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 1,
    #     "section_res": 1,
    #     "pos": {"x": 0, "y": 1, "z": 1},
    #     "expected": [
    #         [0, 0, 0],
    #         [1, 0, 0],
    #         [0, 0, 0],
    #     ]
    # },
    # {
    #     "atlas_res": 2,
    #     "section_res": 0.5,  # Not correct, should be 2.  todo: fix
    #     "pos": {"x": 0, "y": 0, "z": 2},
    #     "expected": [
    #         [0, 0, 0],
    #         [0, 1, 0],
    #         [0, 0, 0],
    #     ]
    # },
]
@pytest.mark.parametrize("case", cases)
def test_section_registration_cuts_correctly_with_diff_resolutions(case):
    volume = np.zeros((3, 3, 3))
    volume[1, 1, 1] = 1
    atlas = Atlas(
        volume=volume,
        resolution_um=case['atlas_res'],
    )
    section = Section(
        image=ImageData(
            channels=np.ones((1, 3, 3)), 
            pixel_resolution_um=case["section_res"],
        ),
        plane_3d=Plane3D(**case["pos"]),
    )
    atlas_slice = register(section, atlas).image.channels[0]
    expected_slice = np.array(case['expected']).astype(float)
    try:
        assert np.all(np.isclose(atlas_slice, expected_slice))
    except:
        assert np.all(atlas_slice == expected_slice)  # similar, but nicer printout of arrays in pytest



# different dimensions  
# rotate
# plane_2d: image origin
# (get visibility on atlas indices)