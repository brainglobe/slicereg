from __future__ import annotations

from dataclasses import dataclass

from slicereg.commands.base import BaseSectionRepo, BaseCommand
from slicereg.commands.utils import Signal
from slicereg.repos.atlas_repo import BaseAtlasRepo
from slicereg.models.registration import AtlasSectionRegistration

@dataclass
class MoveSectionCommand(BaseCommand):
    _section_repo: BaseSectionRepo
    _atlas_repo: BaseAtlasRepo
    section_moved: Signal = Signal()

    def __call__(self, x=0., y=0., z=0., rx=0., ry=0., rz=0.):  # type: ignore
        section = \
            self._section_repo.sections[0] \
            .translate(x=x, y=y, z=z) \
            .rotate(rx=rx, ry=ry, rz=rz)

        atlas = self._atlas_repo.get_atlas()
        registration = AtlasSectionRegistration(section=section, atlas=atlas)

        self._section_repo.save_section(section)
        self.section_moved.emit(transform=registration.affine_transform, atlas_slice_image=registration.atlas_slice.channels[0])
