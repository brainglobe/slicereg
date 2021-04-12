from __future__ import annotations

from dataclasses import dataclass, field

from slicereg.commands.utils import Signal
from slicereg.repos.atlas_repo import BaseAtlasRepo


@dataclass
class LoadAtlasFromFileCommand:
    _repo: BaseAtlasRepo
    atlas_updated: Signal = field(default_factory=Signal)

    def __call__(self, filename: str):
        atlas = self._repo.load_atlas_from_file(filename=filename)
        self._repo.set_atlas(atlas=atlas)
        self.atlas_updated.emit(volume=atlas.volume, transform=atlas.affine_transform)
