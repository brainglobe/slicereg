from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.section.base import BaseSectionRepo


class BaseSelectChannelPresenter(ABC):

    @abstractmethod
    def update_section_image(self, image: ndarray) -> None: ...

    @abstractmethod
    def show_error(self, msg: str) -> None: ...


@dataclass(frozen=True)
class SelectChannelUseCase:
    section_repo: BaseSectionRepo
    presenter: BaseSelectChannelPresenter

    def __call__(self, num: int) -> None:
        section = self.section_repo.get_section()
        if section is None:
            self.presenter.show_error(msg="No section loaded yet.")
            return
        try:
            image = section.channels[num - 1]
        except IndexError:
            self.presenter.show_error(msg=f"Section doesn't have a Channel {num}.")
            return
        self.presenter.update_section_image(image=image)
