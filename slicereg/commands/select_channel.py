from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.utils import Signal


class BaseSelectChannelPresenter(ABC):

    @abstractmethod
    def show(self, channel: int, image: ndarray): ...


@dataclass
class SelectChannelCommand:
    _repo: BaseSectionRepo
    channel_changed: Signal = Signal()

    def __call__(self, channel: int):
        section = self._repo.sections[0]
        # if section is None:
        #     self._presenter.show_error("No section loaded yet.")
        # try:
        image = section.image.channels[channel - 1]
        self.channel_changed.emit(channel=channel, image=image)
        # except IndexError:
        #     self._presenter.show_error(f"Section doesn't have a Channel {num}.")
