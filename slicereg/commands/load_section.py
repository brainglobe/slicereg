from dataclasses import dataclass
from typing import Optional

from numpy import ndarray

from slicereg.commands.base import BaseRepo, BaseLocalImageReader
from slicereg.core.image_transform import ImageTransformer
from slicereg.core.physical_transform import PhysicalTransformer
from slicereg.core.registration import Registration
from slicereg.core.section import Section


@dataclass(frozen=True)
class LoadImageResult:
    image: ndarray
    transform: ndarray
    resolution_um: float
    atlas_image: ndarray
    num_channels: int


@dataclass
class LoadSectionCommand:
    _repo: BaseRepo
    _image_reader: BaseLocalImageReader

    def __call__(self, filename: str, resolution: Optional[float] = None) -> Optional[LoadImageResult]:

        image = self._image_reader.read(filename=filename, resolution=resolution)
        if image is None:
            raise IOError("Image failed to load.")

        atlas = self._repo.get_atlas()
        if not atlas:
            raise RuntimeError('No atlas loaded')

        image = image.resample(resolution_um=10)
        cx, cy, cz = atlas.center

        section = Section(
            image=image,
            image_transform=ImageTransformer(i_shift=-0.5, j_shift=-0.5),
            physical_transform=PhysicalTransformer(x=cx, y=cy, z=cz)
        )

        registration = Registration(section=section, atlas=atlas)

        self._repo.save_section(section=section)
        return LoadImageResult(
            image=section.image.channels[0],
            transform=registration.image_to_volume_transform,
            resolution_um=image.resolution_um,
            atlas_image=registration.slice_atlas().channels[0],
            num_channels=image.num_channels,
        )
