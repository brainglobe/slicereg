from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.repositiories.section import read_ome_tiff
from src.use_cases.base import BaseUseCase, BaseSectionRepo, BaseAtlasRepo


class BaseLoadSectionPresenter(ABC):

    @abstractmethod
    def show_section(self, image: ndarray, transform: ndarray, ref_image: ndarray): ...


@dataclass
class LoadSectionUseCase(BaseUseCase):
    section_repo: BaseSectionRepo
    atlas_repo: BaseAtlasRepo
    presenter: BaseLoadSectionPresenter

    def __call__(self, filename: str) -> None:
        section = read_ome_tiff(filename=filename)
        self.section_repo.save_section(section=section)
        atlas = self.atlas_repo.get_current_atlas()
        self.presenter.show_section(
            image=section.channels[0],
            transform=section.affine_transform,
            ref_image=atlas.slice(width=section.width_um, transform=section.affine_transform)
        )
