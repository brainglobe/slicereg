from __future__ import annotations

from dataclasses import dataclass

from numpy import ndarray

from slicereg.app.commands.base import BaseSectionRepo


@dataclass(frozen=True)
class SelectChannelResult:
    section_image: ndarray
    current_channel: int


@dataclass
class SelectChannelCommand:
    _repo: BaseSectionRepo

    def __call__(self, channel: int) -> SelectChannelResult:
        section = self._repo.sections[0]
        image = section.image.channels[channel - 1]
        return SelectChannelResult(section_image=image, current_channel=channel)
