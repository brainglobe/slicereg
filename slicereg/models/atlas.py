from dataclasses import dataclass, field

from numpy import ndarray, newaxis, floor, zeros
from scipy.ndimage import affine_transform
from vispy.util.transforms import scale, translate

from slicereg.models.image import ImageData
from slicereg.models.section import Section
from slicereg.models.transforms import Plane3D


@dataclass
class Atlas:
    volume: ndarray = field(repr=False)
    resolution_um: float

    @property
    def affine_transform(self) -> ndarray:
        w, h, d = self.volume.shape
        return (translate((-w / 2, -h / 2, -d / 2)) @ scale((self.resolution_um,) * 3)).T

    def slice(self, plane: Plane3D) -> Section:
        if plane.rotation == (0, -90, 0):
            if 0 <= plane.x < self.volume.shape[0]:
                slice_image = self.volume[int(floor(plane.x)), :, :][newaxis, :, :]
            else:
                h, w = self.volume.shape[:2]
                slice_image = zeros((1, h, w))

        elif plane.rotation == (90, 0, 0):
            if 0 <= plane.y < self.volume.shape[1]:
                slice_image = self.volume[:, int(floor(plane.y)), :][newaxis, :, :]
            else:
                h, w = self.volume.shape[:2]
                slice_image = zeros((1, h, w))
        elif plane.rotation == (0, 0, 0):
            if 0 <= plane.z < self.volume.shape[2]:
                slice_image = self.volume[:, :, int(floor(plane.z))][newaxis, :, :]
            else:
                h, w = self.volume.shape[:2]
                slice_image = zeros((1, h, w))
        else:
            # new_volume = affine_transform(self.volume, matrix=plane.affine_transform, cval=0.)
            # slice_image = new_volume[:, :, 0][newaxis, :, :]
            raise NotImplementedError(f"No atlas rotation slicing implemented yet., {plane.rotation}")


        return Section(
            image=ImageData(channels=slice_image, pixel_resolution_um=self.resolution_um),
            plane_3d=plane,
            thickness_um=self.resolution_um
        )

