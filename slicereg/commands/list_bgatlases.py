from __future__ import annotations

from dataclasses import dataclass, field

from slicereg.commands.utils import Signal
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader


@dataclass
class ListBgAtlasesCommand:
    _reader: BrainglobeAtlasReader
    atlas_list_updated: Signal = field(default_factory=Signal)

    def __call__(self):
        atlas_names = self._reader.list_available()
        self.atlas_list_updated.emit(atlas_names=atlas_names)
