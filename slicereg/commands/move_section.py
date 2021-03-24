from __future__ import annotations

from dataclasses import dataclass

from slicereg.commands.base import BaseSectionRepo, BaseCommand
from slicereg.commands.utils import Signal
from slicereg.repos.atlas_repo import BaseAtlasRepo
from slicereg.models.registration import register

@dataclass
class MoveSectionCommand(BaseCommand):
    _section_repo: BaseSectionRepo
    _atlas_repo: BaseAtlasRepo
    section_moved: Signal = Signal()

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.):
        sections = self._section_repo.sections
        atlas = self._atlas_repo.get_atlas()
        if not sections or not atlas:
            print("not atlas", atlas)
            return
        section = sections[0]
        new_section = section.translate(dx=x, dy=y, dz=z).rotate(dx=rx, dy=ry, dz=rz)

        atlas_section = register(section=section, atlas=atlas)

        self._section_repo.save_section(new_section)
        self.section_moved.emit(transform=new_section.affine_transform, atlas_slice_image=atlas_section.image.channels[0])
