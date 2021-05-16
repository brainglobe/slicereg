from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple

from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo


class MoveType(Enum):
    TRANSLATION = auto()
    ROTATION = auto()


class Axis(Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'


class MoveSectionData2(NamedTuple):
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float


@dataclass(frozen=True)
class MoveSectionCommand2:
    _repo: BaseRepo

    def __call__(self, axis: Axis, value: float, type: MoveType, absolute: bool) -> Result[None, None]:
        try:
            section = self._repo.get_sections()[0]
        except IndexError:
            return Err("No section loaded")
        coord_vals = {
            (MoveType.TRANSLATION, Axis.X): 'x',
            (MoveType.TRANSLATION, Axis.Y): 'y',
            (MoveType.TRANSLATION, Axis.Z): 'z',
            (MoveType.ROTATION, Axis.X): 'rx',
            (MoveType.ROTATION, Axis.Y): 'ry',
            (MoveType.ROTATION, Axis.Z): 'rz',
        }

        coord = coord_vals[(type, axis)]
        if absolute:
            physical = section.physical_transform.update(**{coord: value})
        elif type is MoveType.ROTATION:
            physical = section.physical_transform.rotate(**{coord: value})
        elif type is MoveType.TRANSLATION:
            physical = section.physical_transform.translate(**{coord: value})
        section = section.update(physical_transform=physical)

        self._repo.save_section(section)
        return Ok(MoveSectionData2(
            x=physical.x,
            y=physical.y,
            z=physical.z,
            rx=physical.rx,
            ry=physical.ry,
            rz=physical.rz
        ))