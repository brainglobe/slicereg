from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Tuple, cast
from uuid import UUID, uuid4

from numpy import ndarray

from slicereg.models.image import ImageData
from slicereg.models.transforms import Plane2D, Plane3D


@dataclass(frozen=True)
class Section:
    image: ImageData
    plane_2d: Plane2D = field(default_factory=Plane2D)
    plane_3d: Plane3D = field(default_factory=Plane3D)
    thickness_um: float = 16.
    id: UUID = field(default_factory=uuid4)

    def translate(self, dx: float = 0., dy: float = 0., dz: float = 0.) -> Section:
        return replace(self, plane_3d=self.plane_3d.translate(dx=dx, dy=dy, dz=dz))

    def rotate(self, dx: float = 0., dy: float = 0., dz: float =0.) -> Section:
        return replace(self, plane_3d=self.plane_3d.rotate(dx=dx, dy=dy, dz=dz))

    @property
    def affine_transform(self) -> ndarray:
        return self.plane_3d.affine_transform @ self.image.scale_matrix @ self.plane_2d.affine_transform

    def pos_from_coord(self, i: int, j: int) -> Tuple[float, float, float]:
        projection = self.affine_transform @ self.image.project_coord(
            i=i, j=j).T
        assert projection.shape == (4, 1)
        pos = tuple(projection[:3, 0])
        assert len(pos) == 3
        return cast(Tuple[float, float, float], pos)  # cast to tell mypy that pos is a 3-tuple (numpy isn't helping out here).

    def recenter(self) -> Section:
        return replace(self, plane_2d=replace(self.plane_2d, x=-self.image.width / 2, y=-self.image.height / 2))

    def resample(self, resolution_um: float) -> Section:
        return replace(self, image=self.image.resample(resolution_um=resolution_um))

    def with_new_image(self, image: ImageData) -> Section:
        return replace(self, image=image, id=uuid4())