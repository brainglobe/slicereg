from copy import copy
from functools import lru_cache
from dataclasses import replace

import numpy as np
from numba import njit, prange

from slicereg.models.section import Section, ImageData
from slicereg.models.atlas import Atlas
from slicereg.models.transforms import AtlasTransform

def register(section: Section, atlas: Atlas) -> Section:
    width, height = section.image.width, section.image.height
    inds = inds_homog(height=height, width=width)
    res = 1 / atlas.resolution_um
    scale_mat = np.diag([res, res, res, 1.])

    brightness_3d = _register(inds, volume=atlas.volume, transform=scale_mat @ section.affine_transform)
    registered_slice = section.with_new_image(
        ImageData(
            channels=brightness_3d.reshape(1, height, width), 
            pixel_resolution_um=section.image.pixel_resolution_um,
        )
    )
    return registered_slice




@lru_cache()
def inds_homog(height, width):
    return np.mgrid[:height, :width, :1, 1:2].reshape(-1, width*height).astype(float)


@njit(parallel=True, fastmath=True)
def _register(inds, volume, transform):
    atlas_coords =  inds.T @ transform.T
    atlas_coords = atlas_coords[:, :3].astype(np.int32)
    
    ii, jj, kk = volume.shape
    vals = np.empty(atlas_coords.shape[0], dtype=volume.dtype)
    for ind in prange(atlas_coords.shape[0]):
        i, j, k = atlas_coords[ind]
        if 0 <= i < ii and 0 <= j < jj and 0 <= k < kk:
            vals[ind] = volume[i, j, k]
        else:
            vals[ind] = 0
    return vals
