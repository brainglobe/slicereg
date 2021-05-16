from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple

from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo


class MoveType(Enum):
    TRANSLATION = auto()


class Axis(Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'


class MoveSectionData2(NamedTuple):
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class MoveSectionCommand2:
    _repo: BaseRepo

    def __call__(self, axis: Axis, value: float, type: MoveType, absolute: bool) -> Result[None, None]:
        try:
            section = self._repo.get_sections()[0]
        except IndexError:
            return Err("No section loaded")
        physical = section.physical_transform.update(**{axis.value: value})
        section = section.update(physical_transform=physical)
        self._repo.save_section(section)
        return Ok(MoveSectionData2(x=physical.x, y=physical.y, z=physical.z))