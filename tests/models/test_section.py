import pytest
from hypothesis.strategies import integers, floats
from numpy.ma import array, arange, sqrt
from hypothesis import strategies as st, given
from pytest import approx

from slicereg.models.section import Section
from slicereg.models.image import ImagePlane, SliceImage

sensible_floats = floats(allow_nan=False, allow_infinity=False)


@given(
    i=integers(0, 2), j=integers(0, 3), # Image coordinates
    dx=sensible_floats, dy=sensible_floats, dz=sensible_floats,  # Section Position offsets
    pixel_resolution=floats(min_value=1e-12, allow_nan=False, allow_infinity=False),
)
def test_can_get_3d_position_from_2d_pixel_coordinate_in_section(i, j, dx, dy, dz, pixel_resolution):
    section = Section.from_coronal(
        image=SliceImage(
            channels=arange(24).reshape(2, 3, 4),
            pixel_resolution_um=pixel_resolution,
        ),
        position_um=(dx, dy, dz),
    )
    ox, oy, oz = section.pos_from_coord(i=i, j=j)  # observed 3D positions
    assert ox == approx((j * 1/pixel_resolution) + dx)
    assert oy == approx((-i * 1/pixel_resolution) + dy)
    assert oz == approx(dz)


cases = [
    # Shifts, no rotation
    ((0, 1), 1., (0., 0.), 0., (1., 0., 0.)),
    ((0, 1), 1., (1., 0.), 0., (2., 0., 0.)),
    ((0, 1), 1., (10., 20.), 0., (11., 20., 0.)),
    ((0, 1), 2., (10., 20.), 0., (5.5, 10., 0.)),
    # Rotations, no shift
    ((0, 1), 1., (0., 0.), 90., (0., 1., 0.)),
    ((0, 1), 1., (0., 0.), -90., (0., -1., 0.)),
    ((0, 1), 1., (0., 0.), 180., (-1., 0., 0.)),
    ((0, 1), 1., (0., 0.), 360., (1., 0., 0.)),
    ((0, 1), 1., (0., 0.), -720., (1., 0., 0.)),
    ((0, 1), 1., (0., 0.), 45., (1./sqrt(2), 1./sqrt(2), 0.)),
    ((0, 6), 1., (0., 0.), 60., (3, 3*sqrt(3), 0.)),
    # Rotations & Shift: Rotation, then Shift
    ((0, 1), 1., (5., 0.), 90., (5., 1., 0.)),
    ((0, 1), 1., (5., 0.), -90., (5., -1., 0.)),
    ((0, 1), 1., (5., 10.), 90., (5., 11., 0.)),
    ((0, 1), 2., (5., 10.), 90., (2.5, 5.5, 0.)),
]
@pytest.mark.parametrize("imcoord, res, shift, theta, atlascoord", cases)
def test_can_get_correct_3d_position_with_image_shifts_and_planar_rotations(imcoord, res, shift, theta, atlascoord):
    x, y = shift
    section = Section.from_coronal(
        image=SliceImage(channels=arange(2400).reshape(2, 30, 40), pixel_resolution_um=res),
        plane=ImagePlane(x=x, y=y, theta=theta),
    )
    i, j = imcoord
    assert section.pos_from_coord(i=i, j=j) == approx(atlascoord)


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
