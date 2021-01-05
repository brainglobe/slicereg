from dataclasses import dataclass

from src.core.section.base import BaseSectionRepo, BaseSectionSerializer
from src.core.atlas.load_atlas import LoadAtlasWorkflow, BaseLoadAtlasPresenter, BaseAtlasRepo, BaseAtlasSerializer
from src.core.section.load_section import LoadSectionWorkflow, BaseLoadSectionPresenter
from src.core.section.select_channel import SelectChannelWorkflow, BaseSelectChannelPresenter
from src.core.section.move_section import MoveSectionWorkflow, BaseMoveSectionPresenter


@dataclass
class WorkflowProvider:
    section_repo: BaseSectionRepo
    atlas_repo: BaseAtlasRepo
    atlas_serializer: BaseAtlasSerializer
    section_serializer: BaseSectionSerializer
    load_atlas_presenter: BaseLoadAtlasPresenter
    select_channel_presenter: BaseSelectChannelPresenter
    load_section_presenter: BaseLoadSectionPresenter
    move_section_presenter: BaseMoveSectionPresenter

    @property
    def load_atlas(self) -> LoadAtlasWorkflow:
        return LoadAtlasWorkflow(
            repo=self.atlas_repo,
            serializer=self.atlas_serializer,
            presenter=self.load_atlas_presenter
        )

    @property
    def load_section(self) -> LoadSectionWorkflow:
        return LoadSectionWorkflow(
            section_repo=self.section_repo,
            serializer=self.section_serializer,
            presenter=self.load_section_presenter
        )

    @property
    def select_channel(self) -> SelectChannelWorkflow:
        return SelectChannelWorkflow(section_repo=self.section_repo, presenter=self.select_channel_presenter)

    @property
    def move_section(self) -> MoveSectionWorkflow:
        return MoveSectionWorkflow(section_repo=self.section_repo, presenter=self.move_section_presenter)
