from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from slicereg.commands.base import BaseSectionRepo, BaseCommand
from slicereg.commands.utils import Signal


class BaseSelectChannelPresenter(ABC):

    @abstractmethod
    def show(self, channel: int, image: ndarray): ...


@dataclass
class SelectChannelCommand(BaseCommand):
    _repo: BaseSectionRepo
    channel_changed: Signal = Signal()

    def __call__(self, num: int):  # type: ignore
        section = self._repo.sections[0]
        # if section is None:
        #     self._presenter.show_error("No section loaded yet.")
        # try:
        image = section.image.channels[num - 1]
        self.channel_changed.emit(channel=num, image=image)
        # except IndexError:
        #     self._presenter.show_error(f"Section doesn't have a Channel {num}.")
