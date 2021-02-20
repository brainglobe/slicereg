from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Tuple
from uuid import UUID, uuid4
7
from numpy import ndarray
import numpy as np

from slicereg.models.image import Plane, SliceImage
from slicereg.models.math import affine_transform


@dataclass(frozen=True)
class Section:
    image: SliceImage
    plane: Plane
    thickness_um: float = 16.
    position_um: Tuple[float, float, float] = (0., 0., 0.)
    rotation_deg: Tuple[float, float, float] = (0., 0., 0.)
    id: UUID = field(default_factory=uuid4)

    @classmethod
    def from_coronal(cls, image: SliceImage, pos: Tuple[float, float, float] = (0., 0., 0.), **kwargs) -> Section:
        x, y, _ = pos
        return cls(
            image=image,
            plane=Plane(
                x=x,
                y=y,
                theta=0.
            ),
            **kwargs,
        )

    @property
    def affine_transform(self) -> ndarray:
        x, y, z = self.position_um
        rx, ry, rz = self.rotation_deg
        s = self.image.pixel_resolution_um
        return self.plane.affine_transform @ affine_transform(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz, s=s)

    def translate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.position_um
        return replace(self, position_um=(x + dx, y + dy, z + dz))

    def rotate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.rotation_deg
        return replace(self, rotation_deg=(x + dx, y + dy, z + dz))

    def pos_from_coord(self, i: int, j: int) -> Tuple[float, float, float]:
        if not 0 <= i < self.image.height or not 0 <= j < self.image.width:
            raise ValueError(f"Coord ({i, j}) not in image.")

        coords = np.array([[j, i, 0, 0]])
        projection = coords @ self.image.model_matrix
        assert projection.shape == (1, 4)
        return tuple(projection.flatten()[:3])
