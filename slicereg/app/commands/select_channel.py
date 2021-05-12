from __future__ import annotations

from dataclasses import dataclass

from numpy import ndarray

from slicereg.app.repo import BaseRepo


@dataclass(frozen=True)
class SelectChannelResult:
    section_image: ndarray
    current_channel: int


@dataclass
class SelectChannelCommand:
    _repo: BaseRepo

    def __call__(self, channel: int) -> SelectChannelResult:
        sections = self._repo.get_sections()
        if not sections:
            raise RuntimeError("Section not loaded yet.")
        section = sections[0]
        image = section.image.channels[channel - 1]
        return SelectChannelResult(section_image=image, current_channel=channel)
