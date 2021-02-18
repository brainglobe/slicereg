import numpy as np
import pytest

from slicereg.models.section import SliceImage

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