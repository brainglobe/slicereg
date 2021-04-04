from functools import partial

import numpy as np
import pytest
from pytest import approx
from hypothesis import given
from hypothesis.strategies import integers, floats

from slicereg.models.image import ImageData

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
       res=floats(1, 10, allow_nan=False, allow_infinity=False))
def test_image_scale_matrix_converts_pixel_resolution_to_um_space(width, height, channels, res):
    image = ImageData(channels=np.random.random(size=(channels, height, width)), pixel_resolution_um=res)
    r = res
    expected = np.array([
        [r, 0, 0, 0],
        [0, r, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    assert np.all(np.isclose(image.scale_matrix, expected))


@given(to_resolution=floats(allow_nan=False, allow_infinity=False, min_value=0.5, max_value=200))
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


@given(width=integers(min_value=1, max_value=1000), height=integers(min_value=1, max_value=1000))
def test_image_aspect_ratio_calculation(width, height):
    image = ImageData(channels=np.random.random((2, height, width)), pixel_resolution_um=10)
    assert approx(image.aspect_ratio == width / height)

@given(width=integers(min_value=1, max_value=1000), height=integers(min_value=1, max_value=1000))
def test_image_shape_matrix_calculation(width, height):
    image = ImageData(channels=np.random.random((2, height, width)), pixel_resolution_um=10)
    expected = np.array([
        [1, 0, 0, image.height],
        [0, 1, 0, image.width],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    assert approx(image.shape_matrix == expected)
