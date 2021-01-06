from abc import ABC, abstractmethod

from numpy import ndarray

from src.core.section.base import BaseSectionRepo


class BaseSelectChannelPresenter(ABC):

    @abstractmethod
    def update_section_image(self, image: ndarray) -> None: ...

    @abstractmethod
    def show_error(self, msg: str) -> None: ...


def select_channel(section_repo: BaseSectionRepo, presenter: BaseSelectChannelPresenter, num: int) -> None:
    section = section_repo.get_section()
    if section is None:
        presenter.show_error(msg="No section loaded yet.")
        return
    try:
        image = section.channels[num - 1]
    except IndexError:
        presenter.show_error(msg=f"Section doesn't have a Channel {num}.")
        return
    presenter.update_section_image(image=image)
