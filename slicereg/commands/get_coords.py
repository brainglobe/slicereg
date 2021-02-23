from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from slicereg.commands.base import BaseCommand, BaseSectionRepo
from slicereg.commands.utils import Signal

class ImageCoord(NamedTuple):
    i: int
    j: int

class AtlasCoord(NamedTuple):
    x: float
    y: float
    z: float

@dataclass
class GetPixelRegistrationDataCommand(BaseCommand):
    _repo: BaseSectionRepo
    coord_data_requested: Signal = Signal()

    def __call__(self, i: int, j: int):  # type: ignore
        sections = self._repo.sections
        if not sections:
            return
        section = sections[0]
        x, y, z = section.pos_from_coord(i=i, j=j)
        self.coord_data_requested.emit(image_coords=ImageCoord(i=i, j=j), atlas_coords=AtlasCoord(x=x, y=y, z=z))
