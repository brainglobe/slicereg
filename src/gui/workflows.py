from dataclasses import dataclass

from src.core.load_atlas.load_atlas import LoadAtlasWorkflow
from src.core.load_section.load_section import LoadSectionWorkflow
from src.core.section.base import BaseSectionRepo
from src.core.section.move_section import move_section, BaseMoveSectionPresenter
from src.core.select_channel.select_channel import SelectChannelWorkflow


@dataclass
class WorkflowProvider:
    section_repo: BaseSectionRepo
    load_atlas: LoadAtlasWorkflow
    load_section: LoadSectionWorkflow
    select_channel: SelectChannelWorkflow
    move_section_presenter: BaseMoveSectionPresenter


    def move_section(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.) -> None:
        move_section(
            section_repo=self.section_repo,
            presenter=self.move_section_presenter,
            x=x, y=y, z=z, rx=rx, ry=ry, rz=rz,
        )
