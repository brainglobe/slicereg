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

    def __call__(self, x=0., y=0., z=0., rot_lateral=0., rot_axial=0., rot_median=0.):  # type: ignore
        section = \
            self._section_repo.sections[0] \
            .translate(x=x, y=y, z=z) \
            .rotate(rot_lateral=rot_lateral, rot_axial=rot_axial, rot_median=rot_median)

        atlas = self._atlas_repo.get_atlas()
        atlas_section = register(section=section, atlas=atlas)

        self._section_repo.save_section(section)
        self.section_moved.emit(transform=section.affine_transform, atlas_slice_image=atlas_section.image.channels[0])
