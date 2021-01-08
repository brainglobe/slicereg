from abc import ABC, abstractmethod

from numpy import ndarray

from src.core.models.section import Section


class BaseRepo(ABC):

    @abstractmethod
    def get_section(self) -> Section: ...


class BasePresenter(ABC):

    @abstractmethod
    def update_section_image(self, image: ndarray) -> None: ...

    @abstractmethod
    def show_error(self, msg: str) -> None: ...


class SelectChannelWorkflow:

    def __init__(self, repo: BaseRepo, presenter: BasePresenter):
        self._repo = repo
        self._presenter = presenter

    def __call__(self, num: int) -> None:
        section = self._repo.get_section()
        if section is None:
            self._presenter.show_error(msg="No section loaded yet.")
            return
        try:
            image = section.channels[num - 1]
        except IndexError:
            self._presenter.show_error(msg=f"Section doesn't have a Channel {num}.")
            return
        self._presenter.update_section_image(image=image)
