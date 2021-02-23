from __future__ import annotations

from dataclasses import dataclass

from slicereg.commands.base import BaseSectionRepo, BaseCommand
from slicereg.commands.utils import Signal


@dataclass
class MoveSectionCommand(BaseCommand):
    _repo: BaseSectionRepo
    section_moved: Signal = Signal()

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.):
        sections = self._repo.sections
        if not sections:
            return
        section = sections[0]
        new_section = section.translate(dx=x, dy=y, dz=z).rotate(dx=rx, dy=ry, dz=rz)

        self._repo.save_section(new_section)
        self.section_moved.emit(transform=new_section.affine_transform)
