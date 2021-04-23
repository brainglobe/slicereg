from __future__ import annotations

from dataclasses import dataclass, field, replace
from uuid import UUID, uuid4

import numpy as np

from slicereg.models.image import Image
from slicereg.models.image_transform import ImageTransformer
from slicereg.models.transforms import Transform3D


@dataclass(frozen=True)
class Section:
    image: Image
    image_transform: ImageTransformer = field(default_factory=ImageTransformer)
    plane_3d: Transform3D = field(default_factory=Transform3D)
    thickness_um: float = 16.
    id: UUID = field(default_factory=uuid4)

    def translate(self, x: float = 0., y: float = 0., z: float = 0.) -> Section:
        return replace(self, plane_3d=self.plane_3d.translate(x=x, y=y, z=z))

    def rotate(self, rx: float = 0., ry: float = 0., rz: float = 0.) -> Section:
        return replace(self, plane_3d=self.plane_3d.rotate(rx=rx, ry=ry, rz=rz))

    def set_plane_3d(self, **dims) -> Section:
        for dim in dims:
            if dim not in ['x', 'y', 'z', 'rx', 'ry', 'rz']:
                raise TypeError(f'Unknown dimension "{dim}"')

        return replace(self, plane_3d=replace(self.plane_3d, **dims))

    @property
    def _image_transform_matrix(self) -> np.ndarray:
        return self.image_transform.rot_matrix @ (self.image.full_shift_matrix * self.image_transform.shift_matrix)

    @property
    def ij_to_xyz_matrix(self) -> np.ndarray:
        # need -90 degree rotation (ignore left-handed nature of Z coords, since don't exist)
        return np.array([
            [0, 1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    @property
    def affine_transform(self) -> np.ndarray:
        return self.plane_3d.affine_transform @ self._resolution_matrix @ self.ij_to_xyz_matrix @ self.image.affine_transform

    def set_image_origin_to_center(self) -> Section:
        return replace(self, image=self.image.shift_origin_to_center())
