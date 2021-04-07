from functools import partial

import numpy as np
import numpy.testing as npt
import pytest
from pytest import approx
from hypothesis import given
from hypothesis.strategies import integers, floats, booleans

from slicereg.models.image import ImageData


# np.set_printoptions(suppress=True, precision=6)

sensible_floats = partial(floats, allow_nan=False, allow_infinity=False)

np.random.seed(100)  # todo: replace with SeedGenerator, get better control

cases = [
    ((2, 3, 2), 2),
    ((6, 30, 10), 6),
]
@pytest.mark.parametrize('shape,num_channels', cases)
def test_image_reports_correct_number_of_channels(shape, num_channels):
    image = ImageData(channels=np.random.random(size=shape), pixel_resolution_um=12)
    assert image.num_channels == num_channels


cases = [
    ((2, 3, 4), 4),
    ((6, 30, 10), 10),
]
@pytest.mark.parametrize('shape,width', cases)
def test_image_width(shape, width):
    image = ImageData(channels=np.random.random(size=shape), pixel_resolution_um=12)
    assert image.width == width


cases = [
    ((2, 3, 2), 3),
    ((6, 30, 10), 30),
]
@pytest.mark.parametrize('shape,height', cases)
def test_image_height(shape, height):
    image = ImageData(channels=np.random.random(size=shape), pixel_resolution_um=12)
    assert image.height == height


@given(width=integers(1, 1000), height=integers(1, 1000), channels=integers(1, 6),
       r=floats(1, 1000, allow_nan=False, allow_infinity=False))
def test_image_scale_matrix_converts_pixel_resolution_to_um_space(width, height, channels, r):
    image = ImageData(channels=np.random.random(size=(channels, height, width)), pixel_resolution_um=r)
    expected = np.array([
        [r, 0, 0, 0],
        [0, r, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    assert np.all(np.isclose(image.scale_matrix, expected))


@given(theta=sensible_floats(-1000, 1000))
def test_rotation_matrix_corresponds_to_theta_in_degrees(theta):
    image = ImageData(channels=np.arange(24).reshape(1, 6, 4), pixel_resolution_um=123, theta=theta)
    r = np.radians(theta)
    expected = np.array([
        [np.cos(r), -np.sin(r), 0, 0],
        [np.sin(r),  np.cos(r), 0, 0],
        [        0,          0, 1, 0],
        [        0,          0, 0, 1],
    ])
    npt.assert_almost_equal(image.rot_matrix, expected)


@given(width=integers(min_value=1, max_value=100), height=integers(min_value=1, max_value=100),
       x_shift=sensible_floats(min_value=-2, max_value=2), y_shift=sensible_floats(min_value=-2, max_value=2),
       )
def test_shift_matrix_is_ij_ordered_and_in_pixel_coordinate_space(width, height, x_shift, y_shift):
    image = ImageData(channels=np.random.random((2, height, width)), pixel_resolution_um = 10, y_shift = y_shift, x_shift = x_shift)
    expected_shift_matrix = np.array([
        [1, 0, 0, y_shift * height],
        [0, 1, 0, x_shift * width],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    npt.assert_almost_equal(image.shift_matrix, expected_shift_matrix)


@given(to_resolution=sensible_floats(0.5, 200))
def test_downsampling_image_produces_correct_resolution_and_data_shape(to_resolution):
    from_resolution = 12
    image = ImageData(channels=np.arange(24).reshape(1, 6, 4), pixel_resolution_um=from_resolution)
    image2 = image.resample(resolution_um=to_resolution)
    assert image2.pixel_resolution_um == to_resolution
    assert image2.num_channels == image.num_channels

    scale_ratio = from_resolution / to_resolution
    assert approx(image.width * scale_ratio == image2.width, abs=1)
    assert approx(image.height * scale_ratio == image2.height, abs=1)


@given(to_resolution=floats(allow_infinity=False, allow_nan=False, max_value=0))
def test_downsampling_beyond_dimensions_produces_valueerror(to_resolution):
    image = ImageData(channels=np.arange(24).reshape(1, 4, 6), pixel_resolution_um=12)
    with pytest.raises(ValueError, match=r".* positive.*"):
        image.resample(resolution_um=to_resolution)


@given(width=integers(1, 1000), height=integers(1, 1000))
def test_image_aspect_ratio_calculation(width, height):
    image = ImageData(channels=np.random.random((2, height, width)), pixel_resolution_um=10)
    assert approx(image.aspect_ratio == width / height)


@given(y_shift=sensible_floats(), x_shift=sensible_floats(), y_shift2=sensible_floats(), x_shift2=sensible_floats(), theta=sensible_floats(), rot=sensible_floats(), rot_first=booleans())
def test_planar_rotation_and_translate_updates_correct_parameters_with_order_independent(y_shift, x_shift, y_shift2, x_shift2, theta, rot, rot_first):
    image = ImageData(channels=np.random.random((2, 10, 10)), pixel_resolution_um=10, y_shift=y_shift, x_shift=x_shift, theta=theta)
    if rot_first:
        image2 = image.rotate(theta=rot).translate(dy=y_shift2, dx=x_shift2)
    else:
        image2 = image.translate(dy=y_shift2, dx=x_shift2).rotate(theta=rot)
    assert image2.y_shift == y_shift + y_shift2 and image2.x_shift == x_shift + x_shift2 and image2.theta == theta + rot


@given(y_shift=sensible_floats(min_value=-20, max_value=20),
       x_shift=sensible_floats(min_value=-20, max_value=20),
       theta=sensible_floats(-10000, 10000),
       res=sensible_floats(0.5, 10000))
def test_planes_affine_transform_with_rotation_is_correct_for_all_resolutions(y_shift, x_shift, theta, res):
    image = ImageData(channels=np.random.random((2, 10, 10)), pixel_resolution_um=res, y_shift=y_shift, x_shift=x_shift, theta=theta)
    expected = image.scale_matrix @ image.rot_matrix @ image.shift_matrix
    npt.assert_almost_equal(image.affine_transform, expected)


def test_centering_origin_applies_correct_shift_based_on_image_dimensions():
    image = ImageData(channels=np.random.random((2, 10, 12)), pixel_resolution_um=10, y_shift=0, x_shift=0)
    image2 = image.shift_origin_to_center()
    assert image2.y_shift == -0.5 and image2.x_shift == -0.5



