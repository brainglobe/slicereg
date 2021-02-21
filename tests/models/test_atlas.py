import numpy as np
from hypothesis import given
from hypothesis.strategies import integers

from slicereg.models.atlas import Atlas


@given(res=integers(1, 1000), w=integers(1, 100), h=integers(1, 100), d=integers(1, 100))
def test_atlas_matrix_is_scaled_to_um_according_to_resolution_and_shape(res, w, h, d):
    atlas = Atlas(volume=np.random.random((w, h, d)), resolution_um=res)
    expected = [
        [res, 0, 0, -w/2 * res],
        [0, res, 0, -h/2 * res],
        [0, 0, res, -d/2 * res],
        [0, 0, 0, 1],
    ]
    observed = atlas.affine_transform
    assert np.all(np.isclose(observed, np.array(expected)))
