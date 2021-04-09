from dataclasses import dataclass, field

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.base import BaseCommand
from slicereg.commands.utils import Signal
from slicereg.models.registration import AtlasSectionRegistration
from slicereg.repos.atlas_repo import BaseAtlasRepo


@dataclass
class ResampleSectionCommand(BaseCommand):
    _repo: BaseSectionRepo
    _atlas_repo: BaseAtlasRepo
    section_resampled: Signal = field(default_factory=Signal)

    def __call__(self, resolution_um: float) -> None:  # type: ignore
        section = \
            self._repo.sections[0] \
            .resample(resolution_um=resolution_um)

        atlas = self._atlas_repo.get_atlas()
        if not atlas:
            return

        registration = AtlasSectionRegistration(section=section, atlas=atlas)
        self._repo.save_section(section=section)

        self.section_resampled.emit(
            resolution_um=section.pixel_resolution_um,
            section_image=section.image.channels[0],  # todo: get current channel
            transform=registration.affine_transform,
            atlas_image=registration.atlas_slice.channels[0],
        )