from dataclasses import dataclass

from src.core.section.base import BaseSectionRepo, BaseSectionSerializer
from src.core.load_atlas.load_atlas import LoadAtlasWorkflow
from src.core.section.load_section import load_section, BaseLoadSectionPresenter
from src.core.section.select_channel import select_channel, BaseSelectChannelPresenter
from src.core.section.move_section import move_section, BaseMoveSectionPresenter


@dataclass
class WorkflowProvider:
    section_repo: BaseSectionRepo
    load_atlas: LoadAtlasWorkflow
    section_serializer: BaseSectionSerializer
    select_channel_presenter: BaseSelectChannelPresenter
    load_section_presenter: BaseLoadSectionPresenter
    move_section_presenter: BaseMoveSectionPresenter

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
