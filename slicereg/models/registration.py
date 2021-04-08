import numpy as np

from slicereg.models.atlas import Atlas
from slicereg.models.section import Section, Image
from slicereg.models.utils import _fancy_index_3d_numba


def register(section: Section, atlas: Atlas) -> Image:
    width, height = section.image.width, section.image.height
    inds = section.image.inds_homog.astype(float)
    atlas_inds = (np.linalg.inv(atlas.affine_transform) @ section.affine_transform) @ inds
    atlas_inds = atlas_inds[:3, :]  # grab just ijk coords
    atlas_inds = atlas_inds.astype(np.int32)  # round to nearest integer, for indexing
    brightness_3d = _fancy_index_3d_numba(volume=atlas.volume, inds=atlas_inds.T)
    atlas_slice = Image(channels=brightness_3d.reshape(1, height, width))
    return atlas_slice
