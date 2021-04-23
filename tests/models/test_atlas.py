import numpy as np
from pytest import approx
from hypothesis import given
from hypothesis.strategies import integers

from slicereg.models.atlas import Atlas


@given(res=integers(1, 1000), w=integers(1, 100), h=integers(1, 100), d=integers(1, 100))
def test_scale_matrix_is_scaled_to_um_according_to_resolution_and_not_shape(res, w, h, d):
    atlas = Atlas(volume=np.random.random((w, h, d)), resolution_um=res)
    expected = np.array([
        [res, 0, 0, 0],
        [0, res, 0, 0],
        [0, 0, res, 0],
        [0, 0, 0, 1],
    ])
    assert np.all(np.isclose(atlas.scale_matrix, expected))


def test_can_get_atlas_center_in_shared_space():
    atlas = Atlas(volume=np.empty((2, 3, 4)), resolution_um=10)
    assert atlas.center == approx((10, 15, 20))
