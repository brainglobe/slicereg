from __future__ import annotations

from dataclasses import dataclass

from numpy import ndarray

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.utils import Signal


@dataclass(frozen=True)
class SelectChannelResult:
    section_image: ndarray
    current_channel: int


@dataclass
class SelectChannelCommand:
    _repo: BaseSectionRepo
    channel_changed: Signal = Signal()

    def __call__(self, channel: int):
        section = self._repo.sections[0]
        image = section.image.channels[channel - 1]
        return SelectChannelResult(section_image=image, current_channel=channel)
