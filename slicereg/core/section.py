from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Tuple, Optional
from uuid import UUID, uuid4

import numpy as np

from slicereg.core.base import FrozenUpdater
from slicereg.core.image import Image
from slicereg.core.image_transform import ImageTransformer, ij_to_xyz_matrix
from slicereg.core.physical_transform import PhysicalTransformer


@dataclass(frozen=True)
class Section(FrozenUpdater):
    image: Image
    registration_image: Image
    image_transform: ImageTransformer
    physical_transform: PhysicalTransformer
    id: UUID

    @classmethod
    def create(
        cls,
        image: Image,
        image_transform: Optional[ImageTransformer] = None,
        physical_transform: Optional[PhysicalTransformer] = None,
        id: Optional[UUID] = None,
    ) -> Section:
        return cls(
            image=image,
            registration_image=image,
            image_transform=ImageTransformer() if image_transform is None else image_transform,
            physical_transform=PhysicalTransformer() if physical_transform is None else physical_transform,
            id=uuid4() if id is None else id,
        )

    @property
    def original_image(self) -> Image:
        return self.image

    @property
    def _image_transform_matrix(self) -> np.ndarray:
        return self.image_transform.rot_matrix @ (self.image.full_shift_matrix * self.image_transform.shift_matrix)

    @property
    def shared_space_transform(self) -> np.ndarray:
        return self.physical_transform.affine_transform @ self.image.resolution_matrix @ ij_to_xyz_matrix @ self._image_transform_matrix

    def map_ij_to_xyz(self, i: int, j: int) -> Tuple[float, float, float]:
        xyzw = self.shared_space_transform @ ij_homog(i=i, j=j)
        x, y, z = xyzw[:3, 0]
        return x, y, z


def ij_homog(i: int, j: int) -> np.ndarray:
    return np.array([[i, j, 0, 1]]).T
