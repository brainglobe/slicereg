import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import integers, floats

from slicereg.models.image import SliceImage

cases = [
    ((2, 3, 2), 2),
    ((6, 30, 10), 6),
]
@pytest.mark.parametrize('shape,num_channels', cases)
def test_image_reports_correct_number_of_channels(shape, num_channels):
    image = SliceImage(channels=np.random.random(size=shape), pixel_resolution_um=12)
    assert image.num_channels == num_channels



cases = [
    ((2, 3, 4), 4),
    ((6, 30, 10), 10),
]
@pytest.mark.parametrize('shape,width', cases)
def test_image_width(shape, width):
    image = SliceImage(channels=np.random.random(size=shape), pixel_resolution_um=12)
    assert image.width == width


cases = [
    ((2, 3, 2), 3),
    ((6, 30, 10), 30),
]
@pytest.mark.parametrize('shape,height', cases)
def test_image_height(shape, height):
    image = SliceImage(channels=np.random.random(size=shape), pixel_resolution_um=12)
    assert image.height == height


@given(width=integers(1, 1000), height=integers(1, 1000), channels=integers(1, 6), res=floats(1, 10, allow_nan=False, allow_infinity=False))
def test_image_scale_matrix_converts_pixel_resolution_to_um_space(width, height, channels, res):
    image = SliceImage(channels=np.random.random(size=(channels, height, width)), pixel_resolution_um=res)
    r = res
    expected = np.array([
        [1/r, 0, 0, 0],
        [0, 1/r, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    assert np.all(np.isclose(image.scale_matrix, expected))
