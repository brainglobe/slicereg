from dataclasses import dataclass

from src.core.section.base import BaseSectionRepo, BaseSectionSerializer
from src.core.atlas.load_atlas import load_atlas, BaseLoadAtlasPresenter, BaseAtlasRepo, BaseAtlasSerializer
from src.core.section.load_section import load_section, BaseLoadSectionPresenter
from src.core.section.select_channel import select_channel, BaseSelectChannelPresenter
from src.core.section.move_section import move_section, BaseMoveSectionPresenter


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

    def load_atlas(self, resolution: int) -> None:
        load_atlas(
            repo=self.atlas_repo,
            serializer=self.atlas_serializer,
            presenter=self.load_atlas_presenter,
            resolution=resolution
        )


    def load_section(self, filename: str) -> None:
        load_section(
            section_repo=self.section_repo,
            serializer=self.section_serializer,
            presenter=self.load_section_presenter,
            filename=filename
        )

    def select_channel(self, num: int) -> None:
        select_channel(
            section_repo=self.section_repo,
            presenter=self.select_channel_presenter,
            num=num
        )

    def move_section(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.) -> None:
        move_section(
            section_repo=self.section_repo,
            presenter=self.move_section_presenter,
            x=x, y=y, z=z, rx=rx, ry=ry, rz=rz,
        )
