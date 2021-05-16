from dataclasses import dataclass

from result import Result, Err, Ok

from slicereg.commands.base import BaseRepo
from slicereg.commands.move_section2 import MoveSectionData2


@dataclass(frozen=True)
class CenterSectionCommand:
    _repo: BaseRepo

    def __call__(self) -> Result[MoveSectionData2, str]:
        sections = self._repo.get_sections()
        if not sections:
            return Err("No section loaded")
        section = sections[0]

        atlas = self._repo.get_atlas()
        if atlas is None:
            return Err("No atlas loaded")

        cx, cy, cz = atlas.center
        physical = section.physical_transform.update(x=cx, y=cy, z=cz)
        new_section = section.update(physical_transform=physical)
        self._repo.save_section(section=new_section)

        new_physical = new_section.physical_transform
        return Ok(MoveSectionData2(
            x=new_physical.x,
            y=new_physical.y,
            z=new_physical.z,
            rx=new_physical.rx,
            ry=new_physical.ry,
            rz=new_physical.rz
        ))