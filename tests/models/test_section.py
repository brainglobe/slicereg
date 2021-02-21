import pytest
from hypothesis import strategies as st, given
from hypothesis.strategies import integers, floats
from numpy import arange, sin, cos, radians
from pytest import approx

from slicereg.models.image import ImageData
from slicereg.models.transforms import Plane2D, Plane3D
from slicereg.models.section import Section

sensible_floats = floats(allow_nan=False, allow_infinity=False)


@given(
    i=integers(0, 2), j=integers(0, 3), # Image coordinates
    dx=sensible_floats, dy=sensible_floats, dz=sensible_floats,  # Section Position offsets
    pixel_resolution=floats(min_value=1e-12, allow_nan=False, allow_infinity=False),
)
def test_can_get_3d_position_from_2d_pixel_coordinate_in_section(i, j, dx, dy, dz, pixel_resolution):
    section = Section(
        image=ImageData(
            channels=arange(24).reshape(2, 3, 4),
            pixel_resolution_um=pixel_resolution,
        ),
        plane_3d=Plane3D(x=dx, y=dy, z=dz),
    )
    x, y, z = section.pos_from_coord(i=i, j=j)  # observed 3D positions
    assert x == approx((j * 1/pixel_resolution) + dx)
    assert y == approx((-i * 1/pixel_resolution) + dy)
    assert z == approx(dz)


@given(
    j=integers(0, 39),  # image coordinates on i-intercept to simplify trig math (e.g. (0, j))
    pixel_resolution=floats(min_value=1e-12, allow_nan=False, allow_infinity=False),
    x_shift=sensible_floats, y_shift=sensible_floats,  # planar shifts
    theta=sensible_floats,  # planar rotations
)
def test_can_get_correct_3d_position_with_image_shifts_and_planar_rotations(j, pixel_resolution, x_shift, y_shift, theta):
    section = Section(
        image=ImageData(channels=arange(2400).reshape(2, 30, 40), pixel_resolution_um=pixel_resolution),
        plane_2d=Plane2D(x=x_shift, y=y_shift, theta=theta),
    )
    x, y, z = section.pos_from_coord(i=0, j=j)
    assert x == approx((1 / pixel_resolution) * (j * cos(radians(theta)) + x_shift))
    assert y == approx((1 / pixel_resolution) * (j * sin(radians(theta)) + y_shift))
    assert z == 0



@given(i=st.integers(), j=st.integers())
def test_nonexistent_image_coords_raise_error_and_doesnt_if_exists(i, j):
    section = Section(
        image=ImageData(
            channels=arange(180).reshape(2, 3, 30),
            pixel_resolution_um=1
        ),
        plane_2d=Plane2D(x=0, y=0, theta=0),
    )
    if i < 0 or i >= section.image.height or j < 0 or j >= section.image.width:
        with pytest.raises(ValueError):
            section.pos_from_coord(i=i, j=j)
    else:
        assert section.pos_from_coord(i=i, j=j)

