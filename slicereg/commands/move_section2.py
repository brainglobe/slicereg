from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple, Union

from numpy import ndarray
from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo
from slicereg.commands.constants import Axis, AtlasAxis, Direction
from slicereg.core import Registration


class UpdateSectionRequest(ABC):
    ...

class MoveType(Enum):
    TRANSLATION = auto()
    ROTATION = auto()


@dataclass(frozen=True)
class MoveRequest(UpdateSectionRequest):
    move_type: MoveType
    axis: Axis
    value: float
    absolute: bool


@dataclass(frozen=True)
class TranslateRequest(UpdateSectionRequest):
    direction: Direction
    value: float


@dataclass(frozen=True)
class RotateRequest(UpdateSectionRequest):
    axis: Axis
    value: float


@dataclass(frozen=True)
class ReorientRequest(UpdateSectionRequest):
    axis: AtlasAxis


@dataclass(frozen=True)
class CenterRequest(UpdateSectionRequest):
    pass


@dataclass(frozen=True)
class ResampleRequest(UpdateSectionRequest):
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
    atlas_slice_image: ndarray
    section_transform: ndarray
    coronal_atlas_image: ndarray
    axial_atlas_image: ndarray
    sagittal_atlas_image: ndarray


@dataclass(frozen=True)
class MoveSectionCommand2:
    _repo: BaseRepo

    def __call__(self, request: UpdateSectionRequest) -> Result[MoveSectionData2, str]:
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

        elif isinstance(request, TranslateRequest):
            dir_vals = {
                Direction.Superior: ('x', 1),
                Direction.Inferior: ('x', -1),
                Direction.Anterior: ('y', 1),
                Direction.Posterior: ('y', -1),
                Direction.Right: ('z', 1),
                Direction.Left: ('z', -1),
            }
            coord, transform = dir_vals[request.direction]
            physical = section.physical_transform.translate(**{coord: request.value * transform})
            section = section.update(physical_transform=physical)

        elif isinstance(request, RotateRequest):
            dir_vals = {
                Axis.Longitudinal: 'rx',
                Axis.Anteroposterior: 'ry',
                Axis.Horizontal: 'rz',
            }
            coord = dir_vals[request.axis]
            physical = section.physical_transform.rotate(**{coord: request.value})
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

        registration = Registration(section=section, atlas=atlas)
        atlas_slice_image = registration.slice_atlas().channels[0]

        self._repo.save_section(section)

        return Ok(MoveSectionData2(
            superior=section.physical_transform.x,
            anterior=section.physical_transform.y,
            right=section.physical_transform.z,
            rot_longitudinal=section.physical_transform.rx,
            rot_anteroposterior=section.physical_transform.ry,
            rot_horizontal=section.physical_transform.rz,
            resolution_um=section.image.resolution_um,
            section_image=section.image.channels[0],
            atlas_slice_image=atlas_slice_image,
            section_transform=registration.image_to_volume_transform,
            coronal_atlas_image=atlas.make_coronal_slice_at(y=section.physical_transform.y).channels[0],
            axial_atlas_image=atlas.make_axial_slice_at(x=section.physical_transform.x).channels[0],
            sagittal_atlas_image=atlas.make_sagittal_slice_at(z=section.physical_transform.z).channels[0],
        ))


