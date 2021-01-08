from dataclasses import dataclass

from src.workflows.load_atlas.load_atlas import LoadAtlasWorkflow
from src.workflows.load_section.load_section import LoadSectionWorkflow
from src.workflows.move_section.move_section import MoveSectionWorkflow
from src.workflows.select_channel.select_channel import SelectChannelWorkflow


@dataclass
class WorkflowProvider:
    load_atlas: LoadAtlasWorkflow
    load_section: LoadSectionWorkflow
    select_channel: SelectChannelWorkflow
    move_section: MoveSectionWorkflow
