import numpy as np
from pytest import approx
from hypothesis import given
from hypothesis.strategies import integers

from slicereg.models.atlas import Atlas


@given(res=integers(1, 1000), w=integers(1, 100), h=integers(1, 100), d=integers(1, 100))
def test_scale_matrix_is_scaled_to_um_according_to_resolution_and_not_shape(res, w, h, d):
    atlas = Atlas(volume=np.empty((w, h, d)), resolution_um=res)
    expected = np.array([
        [res, 0, 0, 0],
        [0, res, 0, 0],
        [0, 0, res, 0],
        [0, 0, 0, 1],
    ])
    assert np.all(np.isclose(atlas.scale_matrix, expected))


@given(res=integers(1, 1000), w=integers(1, 100), h=integers(1, 100), d=integers(1, 100))
def test_can_get_atlas_center_in_shared_space(res, w, h, d):
    atlas = Atlas(volume=np.empty((w, h, d)), resolution_um=res)
    assert atlas.center == approx((h * res / 2, -w * res / 2, d * res / 2))


def test_atlas_contains_an_annotation_volume():
    atlas = Atlas(volume=np.empty((5, 4, 6)), annotation_volume=np.empty((5, 4, 6)), resolution_um=10)
    assert atlas.annotation_volume.shape == atlas.volume.shape