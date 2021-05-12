from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from numpy import ndarray

from slicereg.app.repo import BaseRepo
from slicereg.core.image_transform import ImageTransformer
from slicereg.core.physical_transform import PhysicalTransformer
from slicereg.core.registration import Registration
from slicereg.core.section import Section
from slicereg.io.tifffile import OmeTiffImageReader, TiffImageReader


@dataclass(frozen=True)
class LoadImageResult:
    image: ndarray
    transform: ndarray
    resolution_um: float
    atlas_image: ndarray
    num_channels: int


@dataclass
class LoadImageCommand:
    _repo: BaseRepo
    _ome_reader: OmeTiffImageReader
    _tiff_reader: TiffImageReader

    def __call__(self, filename: str) -> Optional[LoadImageResult]:
        filepath = Path(filename)
        atlas = self._repo.get_atlas()
        if not atlas:
            raise RuntimeError('No atlas loaded')

        cx, cy, cz = atlas.center

        if '.ome' in filepath.suffixes:
            image = self._ome_reader.read(filename=str(filepath))
        elif filepath.suffix.lower() in ['.tiff', '.tif']:
            image = self._tiff_reader.read(filename=str(filepath), resolution_um=10)
        else:
            raise ValueError(f"{filepath.suffix} not supported")

        image = image.resample(resolution_um=10)
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
