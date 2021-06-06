from dataclasses import dataclass
from typing import Optional
from pathlib import Path
from uuid import UUID

from numpy import ndarray
from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo, BaseLocalImageReader
from slicereg.core.image import Image
from slicereg.core.image_transform import ImageTransformer
from slicereg.core.section import Section
from slicereg.io.xml.reader import read_quicknii_xml


@dataclass(frozen=True)
class LoadImageData:
    section_id: UUID
    section_image: ndarray
    resolution_um: float
    num_channels: int


@dataclass
class LoadSectionCommand:
    _repo: BaseRepo
    _image_reader: BaseLocalImageReader

    def __call__(self, filename: str, resolution: Optional[float] = None) -> Result[LoadImageData, str]:

        image_filename = read_quicknii_xml(filename).image_path if Path(filename).suffix == '.xml' else filename

        image_data = self._image_reader.read(filename=image_filename)
        if image_data is None:
            return Err("Image failed to load.")

        resolution = resolution if isinstance((resolution := image_data.resolution_um), float) else 1.
        image = Image(channels=image_data.channels, resolution_um=resolution)
        image = image.resample(resolution_um=10)

        section = Section.create(
            image=image,
            image_transform=ImageTransformer(i_shift=-0.5, j_shift=-0.5)
        )

        self._repo.save_section(section=section)
        return Ok(LoadImageData(
            section_id=section.id,
            section_image=section.image.channels[0],
            resolution_um=image.resolution_um,
            num_channels=image.num_channels,
        ))
