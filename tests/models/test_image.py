from functools import partial

import numpy as np
import numpy.testing as npt
from hypothesis import given
from hypothesis.strategies import integers, floats

from slicereg.models.image import Image

sensible_floats = partial(floats, allow_nan=False, allow_infinity=False)

np.random.seed(100)  # todo: replace with SeedGenerator, get better control


@given(chans=integers(1, 8), height=integers(1, 50), width=integers(1, 50))
def test_image_reports_correct_dimensions(chans, height, width):
    image = Image(channels=np.random.random(size=(chans, height, width)))
    assert image.num_channels == chans
    assert image.height == height
    assert image.width == width


@given(chans=integers(1, 3), height=integers(1, 20), width=integers(1, 20))
def test_inds_homog_has_correct_shape(chans, height, width):
    image = Image(channels=np.random.random(size=(chans, height, width)))
    assert image.inds_homog.shape == (4, height * width)


def test_inds_homog_example():
    image = Image(channels=np.empty(shape=(3, 2, 3)))
    expected = np.array([
        [0, 0, 0, 1, 1, 1],
        [0, 1, 2, 0, 1, 2],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
    ])
    npt.assert_equal(image.inds_homog, expected)


@given(width=integers(1, 50), height=integers(1, 50))
def test_full_shift_matrix_is_height_and_width_of_image(width, height):
    image = Image(channels=np.empty(shape=(2, height, width)))
    expected = np.array([
        [1, 0, 0, height],
        [0, 1, 0, width],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    npt.assert_equal(image.full_shift_matrix, expected)


