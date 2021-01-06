from abc import ABC, abstractmethod

from numpy import ndarray

from src.core.atlas.load_atlas import BaseAtlasRepo
from src.core.registration.models import RegisteredSection
from src.core.section.base import BaseSectionRepo


class BaseSliceAtlasPresenter(ABC):

    @abstractmethod
    def show_ref_image(self, ref_image: ndarray): ...


def slice_atlas(section_repo: BaseSectionRepo, atlas_repo: BaseAtlasRepo, presenter: BaseSliceAtlasPresenter) -> None:
    section = RegisteredSection(
        section=section_repo.get_section(),
        atlas=atlas_repo.get_atlas()
    )
    ref_image = section.slice_atlas()
    presenter.show_ref_image(ref_image=ref_image)
