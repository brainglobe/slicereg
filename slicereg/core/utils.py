import numpy as np
from numba import njit, prange


@njit(parallel=True, fastmath=True)
def _fancy_index_3d_numba(volume: np.ndarray, inds: np.ndarray, default: int = 0) -> np.ndarray:
    ii, jj, kk = volume.shape
    vals = np.empty(inds.shape[0], dtype=volume.dtype)
    for ind in prange(inds.shape[0]):
        i, j, k = inds[ind]
        vals[ind] = volume[i, j, k] if 0 <= i < ii and 0 <= j < jj and 0 <= k < kk else default
    return vals


def _fancy_index_3d_numpy(volume: np.ndarray, inds: np.ndarray) -> np.ndarray:
    return volume.take(np.ravel_multi_index(inds, volume.shape, mode='clip'), mode='clip')
