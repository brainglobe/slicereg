from dataclasses import dataclass

from src.core.load_atlas.load_atlas import LoadAtlasWorkflow
from src.core.load_section.load_section import LoadSectionWorkflow
from src.core.move_section.move_section import MoveSectionWorkflow
from src.core.select_channel.select_channel import SelectChannelWorkflow


@dataclass
class WorkflowProvider:
    load_atlas: LoadAtlasWorkflow
    load_section: LoadSectionWorkflow
    select_channel: SelectChannelWorkflow
    move_section: MoveSectionWorkflow
