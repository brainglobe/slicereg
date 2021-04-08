import numpy as np
from numba import njit, prange

from slicereg.models.atlas import Atlas
from slicereg.models.section import Section, Image


def register(section: Section, atlas: Atlas) -> Image:
    width, height = section.image.width, section.image.height
    inds = section.image.inds_homog.astype(float)
    transform = np.linalg.inv(atlas.affine_transform) @ section.affine_transform
    brightness_3d = _register(inds, volume=atlas.volume, transform=transform)
    atlas_slice = Image(channels=brightness_3d.reshape(1, height, width))
    return atlas_slice


@njit(parallel=True, fastmath=True)
def _register(inds, volume, transform):
    atlas_coords = transform @ inds
    atlas_coords = atlas_coords[:3, :].T.astype(np.int32)

    ii, jj, kk = volume.shape
    vals = np.empty(atlas_coords.shape[0], dtype=volume.dtype)
    for ind in prange(atlas_coords.shape[0]):
        i, j, k = atlas_coords[ind]
        if 0 <= i < ii and 0 <= j < jj and 0 <= k < kk:
            vals[ind] = volume[i, j, k]
        else:
            vals[ind] = 0 #np.nan
    return vals
