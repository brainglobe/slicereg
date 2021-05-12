from dataclasses import dataclass, field
from typing import Optional, Dict, List
from uuid import UUID

from slicereg.app.repo import BaseRepo
from slicereg.core.atlas import Atlas
from slicereg.core.section import Section


@dataclass
class InMemoryRepo(BaseRepo):
    _atlas: Optional[Atlas] = None
    _sections: Dict[UUID, Section] = field(default_factory=dict, repr=False)

    def get_sections(self) -> List[Section]:
        return list(self._sections.values())

    def save_section(self, section: Section) -> None:
        self._sections[section.id] = section

    def get_atlas(self) -> Optional[Atlas]:
        return self._atlas
