from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Tuple, cast
from uuid import UUID, uuid4

from numpy import ndarray
import numpy as np

from slicereg.models.image import Plane2D, ImageData
from slicereg.models.math import affine_transform


@dataclass(frozen=True)
class Section:
    image: ImageData
    plane: Plane2D = field(default_factory=Plane2D)
    thickness_um: float = 16.
    position_um: Tuple[float, float, float] = (0., 0., 0.)
    rotation_deg: Tuple[float, float, float] = (0., 0., 0.)
    id: UUID = field(default_factory=uuid4)

    @classmethod
    def from_coronal(cls, image: ImageData, **kwargs) -> Section:
        return cls(image=image, **kwargs)

    @property
    def affine_transform(self) -> ndarray:
        x, y, z = self.position_um
        rx, ry, rz = self.rotation_deg
        return affine_transform(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz, s=1).T

    def translate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.position_um
        return replace(self, position_um=(x + dx, y + dy, z + dz))

    def rotate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.rotation_deg
        return replace(self, rotation_deg=(x + dx, y + dy, z + dz))

    def pos_from_coord(self, i: int, j: int) -> Tuple[float, float, float]:
        projection = self.affine_transform @ self.image.scale_matrix @ self.plane.affine_transform @ self.image.project_coord(i=i, j=j).T
        assert projection.shape == (4, 1)
        pos = tuple(projection[:3, 0])
        assert len(pos) == 3
        return cast(Tuple[float, float, float], pos)  # cast to tell mypy that pos is a 3-tuple (numpy isn't helping out here).
