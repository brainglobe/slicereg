from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.utils import Signal
from slicereg.models.registration import AtlasSectionRegistration
from slicereg.models.section import Section
from slicereg.repos.atlas_repo import BaseAtlasRepo


class BaseSectionReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> Section: ...


@dataclass
class LoadImageCommand:
    _repo: BaseSectionRepo
    _atlas_repo: BaseAtlasRepo
    _reader: BaseSectionReader
    section_loaded: Signal = field(default_factory=Signal)

    def __call__(self, filename: str) -> None:

        section = self._reader.read(filename=filename)
        section = section.set_image_origin_to_center()
        section = section.resample(resolution_um=10)

        atlas = self._atlas_repo.get_atlas()
        if not atlas:
            return

        registration = AtlasSectionRegistration(section=section, atlas=atlas)
        registration_transform = registration.affine_transform

        self._repo.save_section(section=section)
        self.section_loaded.emit(image=section.image.channels[0], transform=registration_transform,
                                 resolution_um=section.pixel_resolution_um)
