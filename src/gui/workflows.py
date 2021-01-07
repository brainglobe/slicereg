from dataclasses import dataclass

from src.core.section.base import BaseSectionRepo
from src.core.load_atlas.load_atlas import LoadAtlasWorkflow
from src.core.load_section.load_section import LoadSectionWorkflow
from src.core.section.select_channel import select_channel, BaseSelectChannelPresenter
from src.core.section.move_section import move_section, BaseMoveSectionPresenter


@dataclass
class WorkflowProvider:
    section_repo: BaseSectionRepo
    load_atlas: LoadAtlasWorkflow
    load_section: LoadSectionWorkflow
    select_channel_presenter: BaseSelectChannelPresenter
    move_section_presenter: BaseMoveSectionPresenter

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
