from dataclasses import dataclass, field

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.base import BaseCommand
from slicereg.commands.utils import Signal


@dataclass
class ResampleSectionCommand(BaseCommand):
    _repo: BaseSectionRepo
    section_resampled: Signal = field(default_factory=Signal)

    def __call__(self, resolution_um: float) -> None:  # type: ignore
        section = \
            self._repo.sections[0] \
            .resample(resolution_um=resolution_um)
        self._repo.save_section(section=section)

        self.section_resampled.emit(
            resolution_um=section.image.pixel_resolution_um,
            section_image=section.image.channels[0],  # todo: get current channel
            transform=section.affine_transform,
        )