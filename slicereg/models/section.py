from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Tuple
from uuid import UUID, uuid4

from numpy import ndarray

from slicereg.models.image import ImagePlane, SliceImage
from slicereg.models.math import affine_transform


@dataclass(frozen=True)
class Section:
    image: SliceImage
    plane: ImagePlane = field(default_factory=ImagePlane)
    thickness_um: float = 16.
    position_um: Tuple[float, float, float] = (0., 0., 0.)
    rotation_deg: Tuple[float, float, float] = (0., 0., 0.)
    id: UUID = field(default_factory=uuid4)

    @classmethod
    def from_coronal(cls, image: SliceImage, **kwargs) -> Section:
        return cls(image=image, **kwargs)

    @property
    def affine_transform(self) -> ndarray:
        x, y, z = self.position_um
        rx, ry, rz = self.rotation_deg
        return (self.plane.affine_transform @ affine_transform(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz, s=1)).T

    def translate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.position_um
        return replace(self, position_um=(x + dx, y + dy, z + dz))

    def rotate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        x, y, z = self.rotation_deg
        return replace(self, rotation_deg=(x + dx, y + dy, z + dz))

    def pos_from_coord(self, i: int, j: int) -> Tuple[float, float, float]:
        projection = self.affine_transform @ self.image.project_coord(i=i, j=j).T
        assert projection.shape == (4, 1)
        return tuple(projection[:3, 0])
