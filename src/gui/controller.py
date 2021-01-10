from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray

from src.workflows.load_atlas.load_atlas import LoadAtlasWorkflow
from src.workflows.load_section.load_section import LoadSectionWorkflow
from src.workflows.move_section.move_section import MoveSectionWorkflow
from src.workflows.select_channel.select_channel import SelectChannelWorkflow


@dataclass
class Controller:
    load_atlas: LoadAtlasWorkflow
    load_section: LoadSectionWorkflow
    select_channel: SelectChannelWorkflow
    move_section: MoveSectionWorkflow
