from dataclasses import dataclass, field

from numpy import ndarray, newaxis, floor, zeros
from scipy.ndimage import affine_transform
from vispy.util.transforms import scale, translate

from slicereg.models.image import ImageData
from slicereg.models.section import Section
from slicereg.models.transforms import AtlasTransform


@dataclass
class Atlas:
    volume: ndarray = field(repr=False)
    resolution_um: float

    @property
    def affine_transform(self) -> ndarray:
        w, h, d = self.volume.shape
        return (translate((-w / 2, -h / 2, -d / 2)) @ scale((self.resolution_um,) * 3)).T

    def slice(self, plane: AtlasTransform) -> Section:
        new_volume = affine_transform(self.volume, matrix=plane.affine_transform, cval=0.)
        slice_image = new_volume[:, :, 0][newaxis, :, :]

        return Section(
            image=ImageData(channels=slice_image, pixel_resolution_um=self.resolution_um),
            plane_3d=plane,
            thickness_um=self.resolution_um
        )

