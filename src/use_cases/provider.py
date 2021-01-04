from dataclasses import dataclass

from src.use_cases.base import BaseSectionRepo, BaseAtlasRepo
from src.use_cases.load_atlas import LoadAtlasUseCase, BaseLoadAtlasPresenter
from src.use_cases.load_section import LoadSectionUseCase, BaseLoadSectionPresenter
from src.use_cases.select_channel import SelectChannelUseCase, BaseSelectChannelPresenter
from src.use_cases.move_section import MoveSectionUseCase, BaseMoveSectionPresenter


@dataclass
class UseCaseProvider:
    section_repo: BaseSectionRepo
    atlas_repo: BaseAtlasRepo
    load_atlas_presenter: BaseLoadAtlasPresenter
    select_channel_presenter: BaseSelectChannelPresenter
    load_section_presenter: BaseLoadSectionPresenter
    move_section_presenter: BaseMoveSectionPresenter

    @property
    def load_atlas(self) -> LoadAtlasUseCase:
        return LoadAtlasUseCase(atlas_repo=self.atlas_repo, presenter=self.load_atlas_presenter)

    @property
    def load_section(self) -> LoadSectionUseCase:
        return LoadSectionUseCase(section_repo=self.section_repo, atlas_repo=self.atlas_repo, presenter=self.load_section_presenter)

    @property
    def select_channel(self) -> SelectChannelUseCase:
        return SelectChannelUseCase(section_repo=self.section_repo, presenter=self.select_channel_presenter)

    @property
    def move_section(self) -> MoveSectionUseCase:
        return MoveSectionUseCase(section_repo=self.section_repo, presenter=self.move_section_presenter)