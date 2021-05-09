from __future__ import annotations

from dataclasses import dataclass, field

from slicereg.commands.utils import Signal
from slicereg.io.imio import ImioAtlasReader
from slicereg.repos.atlas_repo import AtlasRepo


@dataclass
class LoadImioAtlasCommand:
    _repo: AtlasRepo
    _reader: ImioAtlasReader
    atlas_updated: Signal = field(default_factory=Signal)

    def __call__(self, filename: str, resolution_um: int):
        atlas = self._reader.read(path=filename, resolution_um=resolution_um)
        self._repo.set_atlas(atlas=atlas)
        self.atlas_updated.emit(volume=atlas.volume, annotation_volume=None, transform=atlas.shared_space_transform)
