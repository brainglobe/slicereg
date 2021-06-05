from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple, Union

from numpy import ndarray
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


@dataclass(frozen=True)
class ResampleRequest:
    resolution_um: float


class MoveSectionData2(NamedTuple):
    superior: float
    anterior: float
    right: float
    rot_longitudinal: float
    rot_anteroposterior: float
    rot_horizontal: float
    section_image: ndarray
    resolution_um: float


@dataclass(frozen=True)
class MoveSectionCommand2:
    _repo: BaseRepo

    def __call__(self, request: Union[MoveRequest, ReorientRequest, CenterRequest, ResampleRequest]) -> Result[MoveSectionData2, str]:
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
            section = section.update(physical_transform=physical)

        elif isinstance(request, ReorientRequest):
            orientation = request.axis
            if orientation is AtlasAxis.CORONAL:
                physical = section.physical_transform.orient_to_coronal()
            elif orientation is AtlasAxis.AXIAL:
                physical = section.physical_transform.orient_to_axial()
            elif orientation is AtlasAxis.SAGITTAL:
                physical = section.physical_transform.orient_to_sagittal()
            section = section.update(physical_transform=physical)

        elif isinstance(request, CenterRequest):
            cx, cy, cz = atlas.center
            physical = section.physical_transform.update(x=cx, y=cy, z=cz)
            section = section.update(physical_transform=physical)

        elif isinstance(request, ResampleRequest):
            section = section.update(image=section.image.resample(resolution_um=request.resolution_um))

        self._repo.save_section(section)
        return Ok(MoveSectionData2(
            superior=section.physical_transform.x,
            anterior=section.physical_transform.y,
            right=section.physical_transform.z,
            rot_longitudinal=section.physical_transform.rx,
            rot_anteroposterior=section.physical_transform.ry,
            rot_horizontal=section.physical_transform.rz,
            resolution_um=section.image.resolution_um,
            section_image=section.image.channels[0]
        ))


