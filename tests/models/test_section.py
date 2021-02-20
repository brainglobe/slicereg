import pytest
from numpy.ma import array, arange
from hypothesis import strategies as st, given
from pytest import approx

from slicereg.models.section import Section
from slicereg.models.image import Plane, SliceImage

cases = [
    ((0, 0), (0., 0., 0.), 1.),
    ((1, 1), (1., -1., 0.), 1.),
    ((2, 3), (3., -2., 0.), 1.),
    ((2, 3), (1.5, -1., 0.), 2.),
    ((2, 3), (1, -0.667, 0.), 3.),
]
@pytest.mark.parametrize("imcoord,atlascoord,res", cases)
def test_can_get_3d_position_from_2d_pixel_coordinate_in_section(imcoord, atlascoord, res):
    section = Section.from_coronal(
        image=SliceImage(
            channels=arange(24).reshape(2, 3, 4),
            pixel_resolution_um=res,
        ),
        pos=(0., 0., 0.),
    )
    i, j = imcoord
    x, y, z = atlascoord
    assert section.pos_from_coord(i=i, j=j) == approx((x, y, z), rel=1e-3)


@given(i=st.integers(), j=st.integers())
def test_nonexistent_image_coords_raise_error_and_doesnt_if_exists(i, j):
    section = Section(
        image=SliceImage(
            channels=arange(180).reshape(2, 3, 30),
            pixel_resolution_um=1
        ),
        plane=Plane(x=0, y=0, theta=0),
    )
    if i < 0 or i >= section.image.height or j < 0 or j >= section.image.width:
        with pytest.raises(ValueError):
            section.pos_from_coord(i=i, j=j)
    else:
        assert section.pos_from_coord(i=i, j=j)


def test_coronal_sections_have_correct_base_rotation():
    section = Section.from_coronal(
        image=SliceImage(
            channels=arange(180).reshape(2, 3, 30),
            pixel_resolution_um=1
        ),
        pos=(0, 0, 0),
    )
    assert section.plane.theta == 0.
