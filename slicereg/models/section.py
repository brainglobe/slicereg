from __future__ import annotations

from dataclasses import dataclass, field, replace
from uuid import UUID, uuid4

import numpy as np

from slicereg.models.image import Image
from slicereg.models.image_transform import ImageTransformer, ij_to_xyz_matrix
from slicereg.models.physical_transform import PhysicalTransformer


@dataclass(frozen=True)
class Section:
    image: Image
    image_transform: ImageTransformer = field(default_factory=ImageTransformer)
    physical_transform: PhysicalTransformer = field(default_factory=PhysicalTransformer)
    thickness_um: float = 16.
    id: UUID = field(default_factory=uuid4)

    @property
    def _image_transform_matrix(self) -> np.ndarray:
        return self.image_transform.rot_matrix @ (self.image.full_shift_matrix * self.image_transform.shift_matrix)

    @property
    def affine_transform(self) -> np.ndarray:
        return self.physical_transform.affine_transform @ self.image.resolution_matrix @ ij_to_xyz_matrix @ self._image_transform_matrix
