from dataclasses import dataclass
from typing import NamedTuple

import numpy as np
from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo
from slicereg.core.registration import Registration


class RegisterSectionData(NamedTuple):
    atlas_slice_image: np.ndarray


@dataclass(frozen=True)
class RegisterSectionCommand:
    _repo: BaseRepo

    def __call__(self) -> Result[RegisterSectionData, str]:
        sections = self._repo.get_sections()
        if not sections:
            return Err("No section loaded")
        section = sections[0]

        atlas = self._repo.get_atlas()
        if atlas is None:
            return Err("No atlas loaded")

        registration = Registration(section=section, atlas=atlas)
        atlas_slice_image = registration.slice_atlas().channels[0]
        return Ok(RegisterSectionData(atlas_slice_image=atlas_slice_image))