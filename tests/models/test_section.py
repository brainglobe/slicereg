import pytest
from hypothesis.strategies import integers, floats
from numpy.core._multiarray_umath import radians
from numpy.ma import array, arange, sqrt, sin, cos
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
    x, y, z = section.pos_from_coord(i=i, j=j)  # observed 3D positions
    assert x == approx((j * 1/pixel_resolution) + dx)
    assert y == approx((-i * 1/pixel_resolution) + dy)
    assert z == approx(dz)


@given(
    j=integers(0, 39),  # image coordinates (e.g. (0, j))
    pixel_resolution=floats(min_value=1e-12, allow_nan=False, allow_infinity=False),
    x_shift=sensible_floats, y_shift=sensible_floats,  # planar shifts
    theta=sensible_floats,  # planar rotations
)
def test_can_get_correct_3d_position_with_image_shifts_and_planar_rotations(j, pixel_resolution, x_shift, y_shift, theta):
    section = Section.from_coronal(
        image=SliceImage(channels=arange(2400).reshape(2, 30, 40), pixel_resolution_um=pixel_resolution),
        plane=ImagePlane(x=x_shift, y=y_shift, theta=theta),
    )
    x, y, z = section.pos_from_coord(i=0, j=j)
    assert x == approx((1 / pixel_resolution) * (j * cos(radians(theta)) + x_shift))
    assert y == approx((1 / pixel_resolution) * (j * sin(radians(theta)) + y_shift))
    assert z == 0



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
