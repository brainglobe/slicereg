from __future__ import annotations

from dataclasses import dataclass, field

from slicereg.commands.utils import Signal
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.repos.atlas_repo import AtlasRepo


@dataclass
class LoadBrainglobeAtlasCommand:
    _repo: AtlasRepo
    _reader: BrainglobeAtlasReader
    atlas_updated: Signal = field(default_factory=Signal)

    def __call__(self, bgatlas_name: str):
        atlas = self._reader.read(path=bgatlas_name)
        self._repo.set_atlas(atlas=atlas)
        self.atlas_updated.emit(volume=atlas.volume, annotation_volume=atlas.annotation_volume, transform=atlas.shared_space_transform)
