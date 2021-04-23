from dataclasses import dataclass, field

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.utils import Signal
from slicereg.models.registration import Registration
from slicereg.repos.atlas_repo import AtlasRepo


@dataclass
class ResampleSectionCommand:
    _repo: BaseSectionRepo
    _atlas_repo: AtlasRepo
    section_resampled: Signal = field(default_factory=Signal)

    def __call__(self, resolution_um: float) -> None:
        section = self._repo.sections[0]
        section = section.update(image=section.image.resample(resolution_um=resolution_um))

        atlas = self._atlas_repo.get_atlas()
        if not atlas:
            return

        registration = Registration(section=section, atlas=atlas)
        self._repo.save_section(section=section)

        self.section_resampled.emit(
            resolution_um=section.image.resolution_um,
            section_image=section.image.channels[0],  # todo: get current channel
            transform=registration.image_to_volume_transform,
            atlas_image=registration.slice_atlas().channels[0],
        )
