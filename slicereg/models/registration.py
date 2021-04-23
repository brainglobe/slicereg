from dataclasses import dataclass
from typing import Tuple

import numpy as np

from slicereg.models.atlas import Atlas
from slicereg.models.base import FrozenUpdater
from slicereg.models.section import Section
from slicereg.models.image import Image
from slicereg.models.utils import _fancy_index_3d_numba

@dataclass(frozen=True)
class Registration(FrozenUpdater):
    section: Section
    atlas: Atlas

    @property
    def image_to_volume_transform(self) -> np.ndarray:
        """The 4x4 transform for the section image to be in atlas volume coordinates."""
        return np.linalg.inv(self.atlas.shared_space_transform) @ self.section.shared_space_transform

    def slice_atlas(self) -> Image:
        """The Image that results from a slice through the Atlas with Section's transforms and dimensions."""
        si = self.section.image
        width, height = si.width, si.height
        inds = si.inds_homog.astype(float)
        atlas_inds = self.image_to_volume_transform @ inds
        atlas_inds = atlas_inds[:3, :]  # grab just ijk coords
        atlas_inds = atlas_inds.astype(np.int32)  # round to nearest integer, for indexing
        brightness_3d = _fancy_index_3d_numba(volume=self.atlas.volume, inds=atlas_inds.T)
        atlas_slice = Image(channels=brightness_3d.reshape(1, height, width), resolution_um=self.section.image.resolution_um)
        return atlas_slice

