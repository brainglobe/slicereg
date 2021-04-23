from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Tuple
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
    id: UUID = field(default_factory=uuid4)

    @property
    def _image_transform_matrix(self) -> np.ndarray:
        return self.image_transform.rot_matrix @ (self.image.full_shift_matrix * self.image_transform.shift_matrix)

    @property
    def affine_transform(self) -> np.ndarray:
        return self.physical_transform.affine_transform @ self.image.resolution_matrix @ ij_to_xyz_matrix @ self._image_transform_matrix

    def map_ij_to_xyz(self, i: int, j: int) -> Tuple[float, float, float]:
        xyzw = self.affine_transform @ ij_homog(i=i, j=j)
        x, y, z = xyzw[:3, 0]
        return x, y, z


def ij_homog(i: int, j: int) -> np.ndarray:
    return np.array([[i, j, 0, 1]]).T
