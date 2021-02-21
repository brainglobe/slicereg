from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Tuple

from slicereg.commands.base import BaseCommand
from slicereg.commands.utils import Signal
from slicereg.models.atlas import Atlas


class BaseLoadAtlasRepo(ABC):

    @abstractmethod
    def get_atlas(self, resolution: int) -> Atlas: ...

    @abstractmethod
    def get_downloaded_resolutions(self) -> Tuple[int, ...]: ...


@dataclass
class LoadAtlasCommand(BaseCommand):
    _repo: BaseLoadAtlasRepo
    atlas_updated: Signal = field(default_factory=Signal)

    def __call__(self, resolution: int):  # type: ignore
        atlas = self._repo.get_atlas(resolution=resolution)
        self.atlas_updated.emit(volume=atlas.volume, transform=atlas.affine_transform)
