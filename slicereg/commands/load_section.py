from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from slicereg.commands.base import BaseSectionRepo, BaseCommand
from slicereg.commands.utils import Signal
from slicereg.models.image import Image
from slicereg.models.section import Section


class BaseSectionReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> Section: ...


@dataclass
class LoadImageCommand(BaseCommand):
    _repo: BaseSectionRepo
    _reader: BaseSectionReader
    section_loaded: Signal = field(default_factory=Signal)

    def __call__(self, filename: str) -> None:  # type: ignore

        log = lambda msg, section: print(
            msg, section,
            section.affine_transform,
            section.image.affine_transform,
            (section.image.height, section.image.width),
            sep="\n", end="\n\n"
        )
        section = self._reader.read(filename=filename)
        log("Loaded", section)
        section = section.set_image_origin_to_center()
        log("Origin Set to Center", section)
        section = section.resample(resolution_um=10)
        log("Resampled", section)

        self._repo.save_section(section=section)
        self.section_loaded.emit(image=section.image.channels[0], transform=section.affine_transform)
