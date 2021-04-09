from dataclasses import dataclass

import numpy as np

from slicereg.models.atlas import Atlas
from slicereg.models.section import Section, Image
from slicereg.models.utils import _fancy_index_3d_numba

@dataclass(frozen=True)
class AtlasSectionRegistration:
    section: Section
    atlas: Atlas

    @property
    def affine_transform(self) -> np.ndarray:
        """The 4x4 transform for the section image to be in atlas volume coordinates."""
        return np.linalg.inv(self.atlas.affine_transform) @ self.section.affine_transform

    @property
    def atlas_slice(self) -> Image:
        """The Image that results from a slice through the Atlas with Section's transforms and dimensions."""
        si = self.section.image
        width, height = si.width, si.height
        inds = si.inds_homog.astype(float)
        atlas_inds = self.affine_transform @ inds
        atlas_inds = atlas_inds[:3, :]  # grab just ijk coords
        atlas_inds = atlas_inds.astype(np.int32)  # round to nearest integer, for indexing
        brightness_3d = _fancy_index_3d_numba(volume=self.atlas.volume, inds=atlas_inds.T)
        atlas_slice = Image(channels=brightness_3d.reshape(1, height, width))
        return atlas_slice
