from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.core.atlas.load_atlas import BaseAtlasRepo
from src.core.registration.models import RegisteredSection
from src.core.section.base import BaseSectionRepo


class BaseSliceAtlasPresenter(ABC):

    @abstractmethod
    def show_ref_image(self, ref_image: ndarray): ...


@dataclass
class SliceAtlasWorkflow:
    section_repo: BaseSectionRepo
    atlas_repo: BaseAtlasRepo
    presenter: BaseSliceAtlasPresenter

    def __call__(self):
        section = RegisteredSection(
            section=self.section_repo.get_section(),
            atlas=self.atlas_repo.get_atlas()
        )
        ref_image = section.slice_atlas()
        self.presenter.show_ref_image(ref_image=ref_image)
