from __future__ import annotations

from dataclasses import dataclass

from slicereg.application.commands.load_atlas import LoadAtlasCommand
from slicereg.application.commands.load_section import LoadImageCommand
from slicereg.application.commands.move_section import MoveSectionCommand
from slicereg.application.commands.select_channel import SelectChannelCommand


@dataclass
class CommandProvider:
    load_atlas: LoadAtlasCommand
    load_section: LoadImageCommand
    select_channel: SelectChannelCommand
    move_section: MoveSectionCommand
