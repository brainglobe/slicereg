from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple, Union

from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo
from slicereg.commands.constants import Axis, AtlasAxis


class MoveType(Enum):
    TRANSLATION = auto()
    ROTATION = auto()


@dataclass(frozen=True)
class MoveRequest:
    move_type: MoveType
    axis: Axis
    value: float
    absolute: bool


@dataclass(frozen=True)
class ReorientRequest:
    axis: AtlasAxis


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

    def __call__(self, request: Union[MoveRequest, ReorientRequest]) -> Result[MoveSectionData2, str]:
        try:
            section = self._repo.get_sections()[0]
        except IndexError:
            return Err("No section loaded")

        if isinstance(request, MoveRequest):
            coord_vals = {
                (MoveType.TRANSLATION, Axis.X): 'x',
                (MoveType.TRANSLATION, Axis.Y): 'y',
                (MoveType.TRANSLATION, Axis.Z): 'z',
                (MoveType.ROTATION, Axis.X): 'rx',
                (MoveType.ROTATION, Axis.Y): 'ry',
                (MoveType.ROTATION, Axis.Z): 'rz',
            }

            coord = coord_vals[(request.move_type, request.axis)]
            if request.absolute:
                physical = section.physical_transform.update(**{coord: request.value})
            elif request.move_type is MoveType.ROTATION:
                physical = section.physical_transform.rotate(**{coord: request.value})
            elif request.move_type is MoveType.TRANSLATION:
                physical = section.physical_transform.translate(**{coord: request.value})

        elif isinstance(request, ReorientRequest):
            orientation = request.axis
            if orientation is AtlasAxis.CORONAL:
                physical = section.physical_transform.update(rx=0, ry=90, rz=0)
            elif orientation is AtlasAxis.AXIAL:
                physical = section.physical_transform.update(rx=90, ry=0, rz=-90)
            elif orientation is AtlasAxis.SAGITTAL:
                physical = section.physical_transform.update(rx=0, ry=0, rz=0)

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


