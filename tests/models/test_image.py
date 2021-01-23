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
