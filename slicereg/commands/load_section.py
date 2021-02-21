from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from slicereg.commands.base import BaseSectionRepo, BaseCommand
from slicereg.commands.utils import Signal
from slicereg.models.image import ImageData
from slicereg.models.section import Section


class BaseSectionReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> ImageData: ...


@dataclass
class LoadImageCommand(BaseCommand):
    _repo: BaseSectionRepo
    _reader: BaseSectionReader
    section_loaded: Signal = field(default_factory=Signal)

    def __call__(self, filename: str) -> None:  # type: ignore
        slice_image = self._reader.read(filename=filename)
        section = Section(image=slice_image).recenter()
        self._repo.save_section(section=section)
        self.section_loaded.emit(image=section.image.channels[0], transform=section.affine_transform)
