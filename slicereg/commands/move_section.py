from __future__ import annotations

from dataclasses import dataclass

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.utils import Signal
from slicereg.models.registration import Registration
from slicereg.repos.atlas_repo import AtlasRepo


@dataclass
class MoveSectionCommand:
    _section_repo: BaseSectionRepo
    _atlas_repo: AtlasRepo
    section_moved: Signal = Signal()

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.):
        section = self._section_repo.sections[0]
        physical = section.physical_transform.translate(x=x, y=y, z=z).rotate(rx=rx, ry=ry, rz=rz)
        section = section.update(physical_transform=physical)

        atlas = self._atlas_repo.get_atlas()
        registration = Registration(section=section, atlas=atlas)

        self._section_repo.save_section(section)
        self.section_moved.emit(
            transform=registration.image_to_volume_transform,
            atlas_slice_image=registration.slice_atlas().channels[0]
        )
