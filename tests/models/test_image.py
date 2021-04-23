from functools import partial

import numpy as np
import numpy.testing as npt
import pytest
from pytest import approx
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


@given(r=sensible_floats(0.1, 1000))
def test_resolution_matrix_matches_resolution(r):
    image = Image(channels=np.empty((2, 11, 13)), resolution_um=r)
    expected = np.array([
        [r, 0, 0, 0],
        [0, r, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    npt.assert_almost_equal(image.resolution_matrix, expected)

@given(from_resolution=sensible_floats(10, 50), to_resolution=sensible_floats(10, 50))
def test_downsampling_image_produces_correct_resolution_and_data_shape(from_resolution, to_resolution):
    image = Image(channels=np.arange(24).reshape(1, 6, 4), resolution_um=from_resolution)
    image2 = image.resample(resolution_um=to_resolution)
    assert image2.resolution_um == to_resolution
    assert image2.num_channels == image.num_channels  # don't want to lose original channels

    scale_ratio = from_resolution / to_resolution
    assert approx(image.width * scale_ratio == image2.width, abs=1)
    assert approx(image.height * scale_ratio == image2.height, abs=1)


@given(to_resolution=integers(-10, 0))
def test_downsampling_beyond_dimensions_produces_valueerror(to_resolution):
    image = Image(channels=np.arange(24).reshape(1, 4, 6), resolution_um=12)
    with pytest.raises(ValueError, match=r".* positive.*"):
        image.resample(resolution_um=to_resolution)