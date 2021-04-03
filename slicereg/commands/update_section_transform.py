from __future__ import annotations

from dataclasses import dataclass, replace

from slicereg.commands.base import BaseSectionRepo, BaseCommand
from slicereg.commands.utils import Signal
from slicereg.repos.atlas_repo import BaseAtlasRepo
from slicereg.models.registration import register

@dataclass
class UpdateSectionTransformCommand(BaseCommand):
    _section_repo: BaseSectionRepo
    _atlas_repo: BaseAtlasRepo
    section_moved: Signal = Signal()

    def __call__(self, **dims):  # type: ignore
        sections = self._section_repo.sections
        atlas = self._atlas_repo.get_atlas()
        if not sections or not atlas:
            print("not atlas", atlas)
            return
        section = sections[0]
                
        new_section = replace(section, plane_3d=replace(section.plane_3d, **dims))
        atlas_section = register(section=new_section, atlas=atlas)
        print(new_section.plane_3d, atlas_section.plane_3d)
        self._section_repo.save_section(new_section)
        self.section_moved.emit(transform=new_section.affine_transform, atlas_slice_image=atlas_section.image.channels[0])
