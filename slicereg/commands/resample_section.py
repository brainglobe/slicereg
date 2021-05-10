from dataclasses import dataclass

from numpy import ndarray

from slicereg.commands.base import BaseSectionRepo
from slicereg.models.registration import Registration
from slicereg.repos.atlas_repo import AtlasRepo


@dataclass(frozen=True)
class ResampleSectionResult:
    resolution_um: float
    section_image: ndarray
    section_transform: ndarray
    atlas_image: ndarray


@dataclass
class ResampleSectionCommand:
    _repo: BaseSectionRepo
    _atlas_repo: AtlasRepo

    def __call__(self, resolution_um: float) -> ResampleSectionResult:
        section = self._repo.sections[0]
        section = section.update(image=section.image.resample(resolution_um=resolution_um))

        atlas = self._atlas_repo.get_atlas()
        if not atlas:
            raise RuntimeError("Atlas not Loaded.")

        registration = Registration(section=section, atlas=atlas)
        self._repo.save_section(section=section)
        return ResampleSectionResult(
            resolution_um=section.image.resolution_um,
            section_image=section.image.channels[0],  # todo: get current channel
            section_transform=registration.image_to_volume_transform,
            atlas_image=registration.slice_atlas().channels[0],
        )
