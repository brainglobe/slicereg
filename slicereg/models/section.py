from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Tuple, cast
from uuid import UUID, uuid4

import numpy as np
from scipy import ndimage

from slicereg.models.image import Image, ij_homog
from slicereg.models.transforms import Transform3D


@dataclass(frozen=True)
class Section:
    image: Image
    pixel_resolution_um: float
    plane_3d: Transform3D = field(default_factory=Transform3D)
    thickness_um: float = 16.
    id: UUID = field(default_factory=uuid4)

    def translate(self, x: float = 0., y: float = 0., z: float = 0.) -> Section:
        return replace(self, plane_3d=self.plane_3d.translate(x=x, y=y, z=z))

    def rotate(self, rx: float = 0., ry: float = 0., rz: float =0.) -> Section:
        return replace(self, plane_3d=self.plane_3d.rotate(rx=rx, ry=ry, rz=rz))

    def set_plane_3d(self, **dims) -> Section:
        for dim in dims:
            if dim not in ['x', 'y', 'z', 'rx', 'ry', 'rz']:
                raise TypeError(f'Unknown dimension "{dim}"')

        return replace(self, plane_3d=replace(self.plane_3d, **dims))

    @property
    def _resolution_matrix(self) -> np.ndarray:
        scale = self.pixel_resolution_um
        matrix = np.diag([scale, scale, 1., 1.])
        return matrix

    @property
    def affine_transform(self) -> np.ndarray:
        # need -90 degree rotation (ignore left-handed nature of Z coords, since don't exist)
        ij_to_xyz_matrix = np.array([
            [0, 1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        return self.plane_3d.affine_transform @ self._resolution_matrix @ ij_to_xyz_matrix @ self.image.affine_transform

    def map_ij_to_xyz(self, i: int, j: int) -> Tuple[float, float, float]:
        xyzw = self.affine_transform @ ij_homog(i=i, j=j)
        x, y, z = xyzw[:3, 0]
        return x, y, z

    def set_image_origin_to_center(self) -> Section:
        return replace(self, image=self.image.shift_origin_to_center())

    def resample(self, resolution_um: float) -> Section:
        if resolution_um <= 0:
            raise ValueError("Resolution must be positive.")

        zoom_level = self.pixel_resolution_um / resolution_um
        zoomed_channels = ndimage.zoom(self.image.channels, zoom=(1, zoom_level, zoom_level))
        return replace(self, image=replace(self.image, channels=zoomed_channels), pixel_resolution_um=resolution_um)
