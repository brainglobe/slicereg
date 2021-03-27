from dataclasses import dataclass

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.base import BaseCommand
from slicereg.commands.utils import Signal


@dataclass
class ResampleSectionCommand(BaseCommand):
    _repo: BaseSectionRepo
    section_resampled: Signal

    def __call__(self, resolution_um: float) -> None:
        section = self._repo.sections[0]
        new_section = section.resample(resolution_um=resolution_um)
        self._repo.save_section(section=new_section)
        self.section_resampled.emit(
            resolution_um=new_section.image.pixel_resolution_um,
            section_image=new_section.image.channels[0],  # todo: get current channel
            transform=new_section.affine_transform,
        )