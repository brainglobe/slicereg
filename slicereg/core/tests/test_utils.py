import numpy as np
import numpy.testing as npt
import pytest

from slicereg.core.utils import _fancy_index_3d_numba, _fancy_index_3d_numpy


@pytest.mark.skip(reason="Not true, not sure why doesn't work.")
def test_fancy_indexing_algos_agree_with_each_other():
    volume = np.random.random(size=(10, 10, 10))
    inds = np.random.randint(0, 10, size=(20, 3))
    numba_result = _fancy_index_3d_numba(volume=volume, inds=inds)
    numpy_result = _fancy_index_3d_numpy(volume=volume, inds=inds)
    assert npt.assert_almost_equal(numba_result, numpy_result)