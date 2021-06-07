from dataclasses import dataclass
from typing import NamedTuple, Union, List
from uuid import UUID

from numpy import ndarray
from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo
from slicereg.commands.constants import Axis, Plane, Direction
from slicereg.core import Registration, Section
from slicereg.core.physical_transform import PhysicalTransformer

SetPosition = NamedTuple("SetPosition", [('axis', Axis), ('value', float)])
SetRotation = NamedTuple("SetRotation", [('axis', Axis), ('value', float)])
Translate = NamedTuple("Translate", [('direction', Direction), ('value', float)])
Rotate = NamedTuple("Rotate", [('axis', Axis), ('value', float)])
Reorient = NamedTuple("Reorient", [('plane', Plane)])
Center = NamedTuple("Center", [])
Resample = NamedTuple("Resample", [('resolution_um', float)])

UpdateSectionStep = Union[SetPosition, SetRotation, Translate, Rotate, Reorient, Center, Resample]


class UpdateSectionRequest(NamedTuple):
    section_id: UUID
    steps: List[UpdateSectionStep]


class MoveSectionData2(NamedTuple):
    section_id: UUID
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
class UpdateSectionCommand:
    _repo: BaseRepo

    def __call__(self, request: UpdateSectionRequest) -> Result[MoveSectionData2, str]:

        maybe_section = self._repo.get_section(id=request.section_id)
        if maybe_section is None:
            return Err(f"Section not found: {request.section_id}")
        section = maybe_section

        atlas = self._repo.get_atlas()
        if atlas is None:
            return Err("No atlas loaded")

        for step in request.steps:
            if isinstance(step, SetPosition):
                coord = {Axis.Longitudinal: 'x', Axis.Anteroposterior: 'y', Axis.Horizontal: 'z'}[step.axis]
                physical = section.physical_transform.update(**{coord: step.value})
                section = section.update(physical_transform=physical)

            elif isinstance(step, SetRotation):
                coord = {Axis.Longitudinal: 'rx', Axis.Anteroposterior: 'ry', Axis.Horizontal: 'rz'}[step.axis]
                physical = section.physical_transform.update(**{coord: step.value})
                section = section.update(physical_transform=physical)

            elif isinstance(step, Translate):
                dir_vals = {
                    Direction.Superior: ('x', 1),
                    Direction.Inferior: ('x', -1),
                    Direction.Anterior: ('y', 1),
                    Direction.Posterior: ('y', -1),
                    Direction.Right: ('z', 1),
                    Direction.Left: ('z', -1),
                }
                coord, transform = dir_vals[step.direction]
                physical = section.physical_transform.translate(**{coord: step.value * transform})
                section = section.update(physical_transform=physical)

            elif isinstance(step, Rotate):
                coord = {Axis.Longitudinal: 'rx', Axis.Anteroposterior: 'ry', Axis.Horizontal: 'rz'}[step.axis]
                physical = section.physical_transform.rotate(**{coord: step.value})
                section = section.update(physical_transform=physical)

            elif isinstance(step, Reorient):
                funs = {
                    Plane.Coronal: PhysicalTransformer.orient_to_coronal,
                    Plane.Axial: PhysicalTransformer.orient_to_axial,
                    Plane.Sagittal: PhysicalTransformer.orient_to_sagittal,
                }
                physical = funs[step.plane](section.physical_transform)
                section = section.update(physical_transform=physical)

            elif isinstance(step, Center):
                cx, cy, cz = atlas.center
                physical = section.physical_transform.update(x=cx, y=cy, z=cz)
                section = section.update(physical_transform=physical)

            elif isinstance(step, Resample):
                section = section.update(image=section.image.resample(resolution_um=step.resolution_um))

        registration = Registration(section=section, atlas=atlas)
        atlas_slice_image = registration.slice_atlas().channels[0]

        self._repo.save_section(section)

        return Ok(MoveSectionData2(
            section_id=section.id,
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
