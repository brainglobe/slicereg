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

@dataclass(frozen=True)
class CenterRequest:
    pass

class MoveSectionData2(NamedTuple):
    superior: float
    anterior: float
    right: float
    rot_longitudinal: float
    rot_anteroposterior: float
    rot_horizontal: float


@dataclass(frozen=True)
class MoveSectionCommand2:
    _repo: BaseRepo

    def __call__(self, request: Union[MoveRequest, ReorientRequest, CenterRequest]) -> Result[MoveSectionData2, str]:
        try:
            section = self._repo.get_sections()[0]
        except IndexError:
            return Err("No section loaded")

        atlas = self._repo.get_atlas()
        if atlas is None:
            return Err("No atlas loaded")

        if isinstance(request, MoveRequest):
            coord_vals = {
                (MoveType.TRANSLATION, Axis.Longitudinal): 'x',
                (MoveType.TRANSLATION, Axis.Anteroposterior): 'y',
                (MoveType.TRANSLATION, Axis.Horizontal): 'z',
                (MoveType.ROTATION, Axis.Longitudinal): 'rx',
                (MoveType.ROTATION, Axis.Anteroposterior): 'ry',
                (MoveType.ROTATION, Axis.Horizontal): 'rz',
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
                physical = section.physical_transform.orient_to_coronal()
            elif orientation is AtlasAxis.AXIAL:
                physical = section.physical_transform.orient_to_axial()
            elif orientation is AtlasAxis.SAGITTAL:
                physical = section.physical_transform.orient_to_sagittal()

        elif isinstance(request, CenterRequest):
            cx, cy, cz = atlas.center
            physical = section.physical_transform.update(x=cx, y=cy, z=cz)

        section = section.update(physical_transform=physical)

        self._repo.save_section(section)
        return Ok(MoveSectionData2(
            superior=physical.x,
            anterior=physical.y,
            right=physical.z,
            rot_longitudinal=physical.rx,
            rot_anteroposterior=physical.ry,
            rot_horizontal=physical.rz
        ))


