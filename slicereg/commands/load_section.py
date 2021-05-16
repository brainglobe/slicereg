from dataclasses import dataclass
from typing import Optional

from numpy import ndarray
from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo, BaseLocalImageReader
from slicereg.core.image import Image
from slicereg.core.image_transform import ImageTransformer
from slicereg.core.physical_transform import PhysicalTransformer
from slicereg.core.registration import Registration
from slicereg.core.section import Section


@dataclass(frozen=True)
class LoadImageData:
    section_image: ndarray
    transform: ndarray
    resolution_um: float
    atlas_image: ndarray
    num_channels: int


@dataclass
class LoadSectionCommand:
    _repo: BaseRepo
    _image_reader: BaseLocalImageReader

    def __call__(self, filename: str, resolution: Optional[float] = None) -> Result[LoadImageData, str]:

        image_data = self._image_reader.read(filename=filename)
        if image_data is None:
            return Err("Image failed to load.")

        atlas = self._repo.get_atlas()
        if not atlas:
            return Err('No atlas loaded')

        resolution = resolution if isinstance((resolution := image_data.resolution_um), float) else 1.
        image = Image(channels=image_data.channels, resolution_um=resolution)
        image = image.resample(resolution_um=10)
        cx, cy, cz = atlas.center

        section = Section(
            image=image,
            image_transform=ImageTransformer(i_shift=-0.5, j_shift=-0.5),
            physical_transform=PhysicalTransformer(x=cx, y=cy, z=cz)
        )

        registration = Registration(section=section, atlas=atlas)

        self._repo.save_section(section=section)
        return Ok(LoadImageData(
            section_image=section.image.channels[0],
            transform=registration.image_to_volume_transform,
            resolution_um=image.resolution_um,
            atlas_image=registration.slice_atlas().channels[0],
            num_channels=image.num_channels,
        ))
