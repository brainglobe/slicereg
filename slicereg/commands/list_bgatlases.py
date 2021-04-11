from __future__ import annotations

from dataclasses import dataclass, field

from slicereg.commands.base import BaseCommand
from slicereg.commands.utils import Signal
from slicereg.repos.atlas_repo import BrainglobeAtlasRepo


@dataclass
class ListBgAtlasesCommand(BaseCommand):
    _repo: BrainglobeAtlasRepo
    atlas_list_updated: Signal = field(default_factory=Signal)

    def __call__(self):  # type: ignore
        atlas_names = self._repo.list_available_atlases()
        self.atlas_list_updated.emit(atlas_names=atlas_names)
