from dataclasses import dataclass

from numpy import ndarray
from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo
from slicereg.core.registration import Registration


@dataclass(frozen=True)
class ResampleSectionData:
    resolution_um: float
    section_image: ndarray
    section_transform: ndarray
    atlas_image: ndarray


@dataclass
class ResampleSectionCommand:
    _repo: BaseRepo

    def __call__(self, resolution_um: float) -> Result[ResampleSectionData, str]:

        sections = self._repo.get_sections()
        if not sections:
            return Err("Section not loaded.")
        section = sections[0]
        section = section.update(image=section.image.resample(resolution_um=resolution_um))

        atlas = self._repo.get_atlas()
        if not atlas:
            return Err("Atlas not Loaded.")

        registration = Registration(section=section, atlas=atlas)
        self._repo.save_section(section=section)
        return Ok(ResampleSectionData(
            resolution_um=section.image.resolution_um,
            section_image=section.image.channels[0],  # todo: get current channel
            section_transform=registration.image_to_volume_transform,
            atlas_image=registration.slice_atlas().channels[0],
        ))
