import pytest
from numpy.ma import array, arange
from hypothesis import strategies as st, given
from pytest import approx

from slicereg.models.section import Section
from slicereg.models.image import ImagePlane, SliceImage

cases = [
    ((0, 0), (0., 0., 0.), 1., (0., 0., 0.)),
    ((1, 1), (0., 0., 0.), 1., (1., -1., 0.)),
    ((2, 3), (0., 0., 0.), 1., (3., -2., 0.)),
    ((2, 3), (0., 0., 0.), 2., (1.5, -1., 0.)),
    ((2, 3), (0., 0., 0.), 3., (1, -0.667, 0.)),
    ((1, 1), (0., 0., 10.), 1., (1., -1., 10.)),
    ((2, 3), (5., 0., 50.), 3., (6, -0.667, 50.)),
    ((2, 3), (5., 10., 50.), 3., (6, 9.333, 50.)),
]
@pytest.mark.parametrize("imcoord, pos, res, atlascoord", cases)
def test_can_get_3d_position_from_2d_pixel_coordinate_in_section(imcoord, pos, res, atlascoord):
    section = Section.from_coronal(
        image=SliceImage(
            channels=arange(24).reshape(2, 3, 4),
            pixel_resolution_um=res,
        ),
        position_um=pos,
    )
    i, j = imcoord
    assert section.pos_from_coord(i=i, j=j) == approx(atlascoord, rel=1e-3)


cases = [
    ((0, 1), 1., (0., 0.), 0., (1., 0., 0.)),
    ((0, 1), 1., (1., 0.), 0., (2., 0., 0.)),
    ((0, 1), 1., (10., 20.), 0., (11., 20., 0.)),
]
@pytest.mark.parametrize("imcoord, res, shift, theta, atlascoord", cases)
def test_can_get_correct_3d_position_with_image_shifts_and_planar_rotations(imcoord, res, shift, theta, atlascoord):
    x, y = shift
    section = Section.from_coronal(
        image=SliceImage(channels=arange(24).reshape(2, 3, 4), pixel_resolution_um=res),
        plane=ImagePlane(x=x, y=y, theta=theta),
    )
    i, j = imcoord
    assert section.pos_from_coord(i=i, j=j) == approx(atlascoord, rel=1e-3)


@given(i=st.integers(), j=st.integers())
def test_nonexistent_image_coords_raise_error_and_doesnt_if_exists(i, j):
    section = Section(
        image=SliceImage(
            channels=arange(180).reshape(2, 3, 30),
            pixel_resolution_um=1
        ),
        plane=ImagePlane(x=0, y=0, theta=0),
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
    )
    assert section.plane.theta == 0.
