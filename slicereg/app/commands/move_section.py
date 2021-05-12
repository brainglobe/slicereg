from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from numpy import ndarray

from slicereg.app.repo import BaseRepo
from slicereg.core.registration import Registration


@dataclass
class MoveSectionResult:
    transform: ndarray
    atlas_slice_image: ndarray


@dataclass
class MoveSectionCommand:
    _repo: BaseRepo

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.) -> MoveSectionResult:
        try:
            section = self._repo.get_sections()[0]
        except IndexError:
            raise RuntimeError("No section loaded")
        physical = section.physical_transform.translate(x=x, y=y, z=z).rotate(rx=rx, ry=ry, rz=rz)
        section = section.update(physical_transform=physical)

        atlas = self._repo.get_atlas()
        if not atlas:
            raise RuntimeError("No atlas loaded")
        registration = Registration(section=section, atlas=atlas)

        self._repo.save_section(section)
        return MoveSectionResult(
            transform=registration.image_to_volume_transform,
            atlas_slice_image=registration.slice_atlas().channels[0],
        )


@dataclass
class UpdateSectionTransformCommand:
    _repo: BaseRepo

    def __call__(self, res: Optional[int] = None, **dims) -> MoveSectionResult:
        for dim in dims:
            if dim not in ['x', 'y', 'z', 'rx', 'ry', 'rz']:
                raise TypeError(f'Unknown dimension "{dim}"')

        sections = self._repo.get_sections()
        atlas = self._repo.get_atlas()
        if not sections:
            raise RuntimeError('Section is not loaded yet')
        if not atlas:
            raise RuntimeError('Atlas is not loaded yet')
        section = sections[0]

        if res is not None:
            section = section.update(image__resolution_um=res)

        physical = section.physical_transform.update(**dims)
        section = section.update(physical_transform=physical)
        registration = Registration(section=section, atlas=atlas)
        self._repo.save_section(section)
        return MoveSectionResult(
            transform=registration.image_to_volume_transform,
            atlas_slice_image=registration.slice_atlas().channels[0]
        )
