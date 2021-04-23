from dataclasses import dataclass, field

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.utils import Signal
from slicereg.io.tifffile import OmeTiffImageReader
from slicereg.models.image_transform import ImageTransformer
from slicereg.models.registration import Registration
from slicereg.models.section import Section
from slicereg.repos.atlas_repo import AtlasRepo


@dataclass
class LoadImageCommand:
    _repo: BaseSectionRepo
    _atlas_repo: AtlasRepo
    _reader: OmeTiffImageReader
    section_loaded: Signal = field(default_factory=Signal)

    def __call__(self, filename: str) -> None:

        image = self._reader.read(filename=filename)
        image = image.resample(resolution_um=10)
        section = Section(image=image, image_transform=ImageTransformer(i_shift=-0.5, j_shift=-0.5))

        atlas = self._atlas_repo.get_atlas()
        if not atlas:
            return

        registration = Registration(section=section, atlas=atlas)

        self._repo.save_section(section=section)
        self.section_loaded.emit(
            image=section.image.channels[0],
            transform=registration.affine_transform,
            resolution_um=image.resolution_um,
            atlas_image=registration.slice_atlas().channels[0]
        )
