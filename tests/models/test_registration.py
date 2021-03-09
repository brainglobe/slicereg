import numpy as np

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
    assert s2.image.width == section.image.width
    assert s2.image.height == section.image.height
    assert np.all(np.isclose(s2.affine_transform, section.affine_transform))
