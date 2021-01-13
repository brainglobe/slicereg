from __future__ import annotations

from dataclasses import dataclass

from slicereg.workflows.load_atlas.workflow import LoadAtlasWorkflow
from slicereg.workflows.load_section.workflow import LoadImageWorkflow
from slicereg.workflows.move_section.workflow import MoveSectionWorkflow
from slicereg.workflows.select_channel.workflow import SelectChannelWorkflow


@dataclass
class WorkflowProvider:
    load_atlas: LoadAtlasWorkflow
    load_section: LoadImageWorkflow
    select_channel: SelectChannelWorkflow
    move_section: MoveSectionWorkflow
