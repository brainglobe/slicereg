from __future__ import annotations

from dataclasses import dataclass

from numpy import ndarray
from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo


@dataclass(frozen=True)
class SelectChannelData:
    section_image: ndarray
    current_channel: int


@dataclass
class SelectChannelCommand:
    _repo: BaseRepo

    def __call__(self, channel: int) -> Result[SelectChannelData, str]:
        sections = self._repo.get_sections()
        if not sections:
            return Err("Section not loaded yet.")
        section = sections[0]
        image = section.image.channels[channel - 1]
        return Ok(SelectChannelData(section_image=image, current_channel=channel))
