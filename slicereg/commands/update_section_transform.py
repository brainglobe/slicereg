from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.utils import Signal
from slicereg.models.registration import Registration
from slicereg.repos.atlas_repo import AtlasRepo


@dataclass
class UpdateSectionTransformCommand:
    _section_repo: BaseSectionRepo
    _atlas_repo: AtlasRepo
    section_moved: Signal = Signal()

    def __call__(self, res: Optional[int] = None, **dims):
        for dim in dims:
            if dim not in ['x', 'y', 'z', 'rx', 'ry', 'rz']:
                raise TypeError(f'Unknown dimension "{dim}"')

        sections = self._section_repo.sections
        atlas = self._atlas_repo.get_atlas()
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
        self._section_repo.save_section(section)
        self.section_moved.emit(
            transform=registration.affine_transform,
            atlas_slice_image=registration.slice_atlas().channels[0]
        )
